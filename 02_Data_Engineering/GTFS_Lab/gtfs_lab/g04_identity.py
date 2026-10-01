"""G04 identity and populated-reference checks driven by the frozen inventory."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .rule_registry import (ApplicabilityExpression, ApplicabilityOperator, RequirementKind,
    RuleAuthority, RuleCategory, RuleDefinition, RuleRegistry, Severity, SpecificationReference)

REVISION = "2026-04-27"
INVENTORY = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_g04_identity_references_2026_04_27.json"
RULES = {
    "GTFS-G04-PRIMARY-KEY-UNIQUENESS": (RuleCategory.IDENTITY, "EXPLICIT_PRIMARY_KEY_UNIQUENESS"),
    "GTFS-G04-REFERENCE-EXISTENCE": (RuleCategory.REFERENTIAL, "POPULATED_FOREIGN_REFERENCE_EXISTENCE"),
    "GTFS-G04-IDENTITY-DOMAIN": (RuleCategory.IDENTITY, "LOGICAL_IDENTITY_DOMAIN_RESOLUTION"),
    "GTFS-G04-CONTEXTUAL-REFERENCE": (RuleCategory.REFERENTIAL, "TRANSLATIONS_CONTEXTUAL_REFERENCE"),
}


def _registry() -> RuleRegistry:
    return RuleRegistry([RuleDefinition(
        rule_id=rule_id, semantic_version="1.0.0", category=category,
        authority=RuleAuthority.GTFS_REQUIRED, severity=Severity.ERROR,
        requirement=RequirementKind.REQUIRED, applicable_files=("GTFS Schedule files",),
        specification_reference=SpecificationReference("GTFS Schedule Reference", REVISION, coverage),
        applicability=ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT, signal="archive.inspection_ready"),
        evaluator_identity=f"gtfs_lab.g04_identity.{rule_id.lower()}/1", evaluator=evaluate_g04,
        declared_coverage=(coverage,)) for rule_id, (category, coverage) in RULES.items()]).freeze()


def _inventory() -> dict[str, Any]:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if payload.get("specification_revision") != REVISION or payload.get("status") != "CREATED_LOCAL_UNPUBLISHED":
        raise ValueError("G04 inventory identity or frozen status mismatch")
    input_paths = {"field_contract_sha256": "gtfs_schedule_fields_2026_04_27.json",
        "capability_map_sha256": "gtfs_schedule_field_capability_map_2026_04_27.json",
        "g01_file_catalog_sha256": "gtfs_schedule_2026_04_27.json"}
    for identity, name in input_paths.items():
        path = INVENTORY.parent / name
        import hashlib
        if hashlib.sha256(path.read_bytes()).hexdigest().upper() != payload["inputs"].get(identity):
            raise ValueError(f"Frozen G04 input hash mismatch: {path.name}")
    return payload


def _rows(ctx, file_name: str) -> tuple[list[str], list[dict[str, str]]] | None:
    table_name = file_name.removesuffix(".txt")
    path = ctx.tables.get(table_name)
    if path is None:
        return None
    metadata = getattr(ctx.dataset, "files", {}).get(file_name, {})
    encoding = metadata.get("encoding") or "utf-8-sig"
    with path.open("r", encoding=encoding, newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        if not reader.fieldnames:
            raise ValueError(f"Missing parsed header: {file_name}")
        return list(reader.fieldnames), list(reader)


def _finding(rule_id: str, file_name: str, row: int, fields: list[str], observed: Any,
             expected: str, source: str, reason: str) -> dict[str, Any]:
    return {"rule_id": rule_id, "source_file": file_name, "record_locator": f"data_row:{row}",
        "source_fields": fields, "observed_identifier_or_reference": observed,
        "expected_identity_or_target_domain": expected, "specification_reference": source,
        "technical_reason": reason}


def _g03_csv_evidence(g03_result: dict | None, file_name: str) -> tuple[str, set[int]]:
    """Return G03 CSV evidence state and structurally invalid data-row numbers."""
    if g03_result is None:
        return "COMPLETE", set()  # isolated unit use; production passes G03 explicitly
    component = g03_result.get("csv_structure")
    if not isinstance(component, dict):
        return "INSPECTION_ERROR", set()
    target = file_name.casefold()
    inspected = next((row for row in component.get("files_inspected", component.get("inspected", []))
                      if str(row.get("file", "")).casefold() == target), None)
    if inspected is None:
        return "NOT_EVALUABLE", set()
    bad_rows: set[int] = set()
    whole_table_bad = False
    for finding in component.get("findings", []):
        if str(finding.get("file", "")).casefold() != target:
            continue
        locator = str(finding.get("row_locator", ""))
        if locator.startswith("ROW:") and locator[4:].isdigit():
            bad_rows.add(int(locator[4:]))
        else:
            whole_table_bad = True
    if inspected.get("status") != "PASS" and not bad_rows:
        whole_table_bad = True
    if whole_table_bad:
        return "NOT_EVALUABLE", set()
    return ("PARTIAL" if bad_rows else "COMPLETE"), bad_rows


def _g03_field_evidence(g03_result: dict | None, file_name: str, field_name: str) -> tuple[bool, set[int]]:
    """Return whether G03 lacks a usable field parser and its invalid row numbers."""
    if g03_result is None:
        return False, set()
    component = g03_result.get("field_types")
    if not isinstance(component, dict):
        return True, set()
    file_key, field_key = file_name.casefold(), field_name.casefold()
    bad_rows = set()
    for finding in component.get("findings", []):
        if (str(finding.get("file", "")).casefold() == file_key
                and str(finding.get("field", "")).casefold() == field_key):
            locator = str(finding.get("row_locator", ""))
            if locator.startswith("ROW:") and locator[4:].isdigit():
                bad_rows.add(int(locator[4:]))
    unavailable = any(
        str(item.get("file", "")).casefold() == file_key
        and str(item.get("field", "")).casefold() == field_key
        for item in component.get("not_evaluable", [])
    )
    return unavailable, bad_rows


def evaluate_g04(ctx, g03_result: dict | None = None, legacy_result: dict | None = None) -> dict:
    """Evaluate primary keys, references, SERVICE_ID and contextual translations."""
    registry = _registry()
    result = {"status": "INSPECTION_ERROR", "rules": [], "findings": [], "rule_versions": registry.identity_map()["rule_versions"]}
    try:
        if g03_result is not None and g03_result.get("status") == "INSPECTION_ERROR":
            result["error"] = "G03 archive inspection failed; G04 cannot consume structural evidence."
            for definition in registry:
                result["rules"].append({"rule_id": definition.rule_id,
                    "semantic_version": definition.semantic_version, "category": definition.category.value,
                    "status": "INSPECTION_ERROR", "coverage": {"evaluated": 0, "not_evaluable": 0,
                    "not_applicable": 0, "state": "UNAVAILABLE"}, "findings": [],
                    "specification_reference": f"GTFS Schedule Reference {REVISION}", "evaluator_executed": True})
            return result
        inventory = _inventory()
        field_contract = json.loads((INVENTORY.parent / "gtfs_schedule_fields_2026_04_27.json").read_text(encoding="utf-8"))
        required_fields = {
            file["file_name"]: {field["field_name"] for field in file["fields"]
                if field["presence"] == "REQUIRED"}
            for file in field_contract["files"]
        }
        # Keep only the most recently used tables. The previous unbounded cache
        # retained every parsed row dictionary, which multiplied memory on large feeds.
        cache: dict[str, tuple[list[str], list[dict[str, str]]] | None] = {}
        def rows(name):
            if name in cache:
                parsed = cache.pop(name)
                cache[name] = parsed
                return parsed
            parsed = _rows(ctx, name)
            cache[name] = parsed
            if len(cache) > 2:
                cache.pop(next(iter(cache)))
            return parsed
        findings: dict[str, list[dict]] = {key: [] for key in RULES}
        statuses: dict[str, list[str]] = {key: [] for key in RULES}
        # Optional empty key components have a definite value in the ordered tuple.
        for key in inventory["primary_keys"]:
            file_name, components, kind = key["file_name"], key["component_fields"], key["key_type"]
            if kind == "NONE":
                continue
            parsed = rows(file_name)
            rule = "GTFS-G04-PRIMARY-KEY-UNIQUENESS"
            if parsed is None:
                statuses[rule].append("NOT_APPLICABLE"); continue
            table_state, bad_rows = _g03_csv_evidence(g03_result, file_name)
            if table_state == "INSPECTION_ERROR":
                statuses[rule].append("INSPECTION_ERROR"); continue
            if table_state == "NOT_EVALUABLE":
                statuses[rule].append("NOT_EVALUABLE"); continue
            headers, records = parsed
            required = required_fields[file_name]
            if kind == "ALL_FIELDS" or not components or any(c in required and c not in headers for c in components):
                statuses[rule].append("NOT_EVALUABLE"); continue
            component_errors = [_g03_field_evidence(g03_result, file_name, component)
                for component in components if component in headers]
            if any(unavailable for unavailable, _ in component_errors):
                statuses[rule].append("NOT_EVALUABLE"); continue
            bad_type_rows = set().union(*(bad for _, bad in component_errors))
            seen: dict[tuple[str, ...], int] = {}
            unresolved = bool(bad_rows or bad_type_rows)
            for index, record in enumerate(records, 1):
                if index in bad_rows or index in bad_type_rows:
                    statuses[rule].append("NOT_EVALUABLE"); continue
                values = tuple(record.get(c) or "" for c in components)
                if any(value == "" for component, value in zip(components, values) if component in required):
                    unresolved = True
                    statuses[rule].append("NOT_EVALUABLE"); continue
                if values in seen:
                    findings[rule].append(_finding(rule, file_name, index, components, list(values),
                        f"unique ordered key {components}", key["source_locator"],
                        f"Primary key duplicates data row {seen[values]}; ordered component tuple is preserved."))
                    statuses[rule].append("FAIL_TECHNICAL")
                else:
                    seen[values] = index
            if records and not unresolved and len(seen) == len(records): statuses[rule].append("PASS")
            elif not records: statuses[rule].append("NOT_APPLICABLE")
        # Logical SERVICE_ID domain follows calendar/calendar_dates availability rules.
        domain_rule = "GTFS-G04-IDENTITY-DOMAIN"
        calendar, dates, trips = rows("calendar.txt"), rows("calendar_dates.txt"), rows("trips.txt")
        service_ids: set[str] = set()
        domain_source_complete = False
        if calendar is not None:
            cal_state, cal_bad_rows = _g03_csv_evidence(g03_result, "calendar.txt")
            if cal_state == "NOT_EVALUABLE":
                statuses[domain_rule].append("NOT_EVALUABLE")
            elif cal_state == "INSPECTION_ERROR":
                statuses[domain_rule].append("INSPECTION_ERROR")
            else:
                cal_field_unavailable, cal_type_bad = _g03_field_evidence(g03_result,"calendar.txt","service_id")
                if cal_field_unavailable:statuses[domain_rule].append("NOT_EVALUABLE")
                cal_bad_rows |= cal_type_bad
                for _ in cal_bad_rows:
                    statuses[domain_rule].append("NOT_EVALUABLE")
                if "service_id" in calendar[0] and not cal_field_unavailable:
                    service_ids.update(record.get("service_id") for index, record in enumerate(calendar[1], 1)
                        if index not in cal_bad_rows and record.get("service_id"))
                    domain_source_complete = cal_state == "COMPLETE" and not cal_type_bad
                else:
                    statuses[domain_rule].append("NOT_EVALUABLE")
            # With both files present, calendar_dates.service_id references calendar.service_id.
            # In dates-only mode it contributes identities and is not checked as a foreign key.
            if dates is not None:
                dates_state, dates_bad_rows = _g03_csv_evidence(g03_result, "calendar_dates.txt")
                if dates_state == "INSPECTION_ERROR":
                    statuses[domain_rule].append("INSPECTION_ERROR")
                elif dates_state == "NOT_EVALUABLE":
                    statuses[domain_rule].append("NOT_EVALUABLE")
                elif "service_id" not in dates[0]:
                    statuses[domain_rule].append("NOT_EVALUABLE")
                else:
                    dates_field_unavailable, dates_type_bad = _g03_field_evidence(g03_result,"calendar_dates.txt","service_id")
                    if dates_field_unavailable:statuses[domain_rule].append("NOT_EVALUABLE")
                    dates_bad_rows |= dates_type_bad
                    for _ in dates_bad_rows:
                        statuses[domain_rule].append("NOT_EVALUABLE")
                    populated_dates = [] if dates_field_unavailable else [(index, record.get("service_id") or "")
                        for index, record in enumerate(dates[1], 1)
                        if index not in dates_bad_rows and record.get("service_id")]
                    if not populated_dates and not dates_bad_rows:
                        statuses[domain_rule].append("NOT_APPLICABLE")
                    for index, ref in populated_dates:
                        if ref in service_ids:
                            statuses[domain_rule].append("PASS")
                        elif domain_source_complete:
                            findings[domain_rule].append(_finding(domain_rule, "calendar_dates.txt", index,
                                ["service_id"], ref, "calendar.service_id",
                                "https://gtfs.org/documentation/schedule/reference/#calendar_datestxt (Field Definitions table, row 1)",
                                "calendar_dates.service_id does not resolve to calendar.service_id while both calendar files are present."))
                            statuses[domain_rule].append("FAIL_TECHNICAL")
                        else:
                            statuses[domain_rule].append("NOT_EVALUABLE")
        elif dates is not None:
            dates_state, dates_bad_rows = _g03_csv_evidence(g03_result, "calendar_dates.txt")
            if dates_state == "NOT_EVALUABLE":
                statuses[domain_rule].append("NOT_EVALUABLE")
            elif dates_state == "INSPECTION_ERROR":
                statuses[domain_rule].append("INSPECTION_ERROR")
            else:
                dates_field_unavailable, dates_type_bad = _g03_field_evidence(g03_result,"calendar_dates.txt","service_id")
                if dates_field_unavailable:statuses[domain_rule].append("NOT_EVALUABLE")
                dates_bad_rows |= dates_type_bad
                for _ in dates_bad_rows:
                    statuses[domain_rule].append("NOT_EVALUABLE")
                if "service_id" in dates[0] and not dates_field_unavailable:
                    service_ids.update(record.get("service_id") for index, record in enumerate(dates[1], 1)
                        if index not in dates_bad_rows and record.get("service_id"))
                    domain_source_complete = dates_state == "COMPLETE"
                else:
                    statuses[domain_rule].append("NOT_EVALUABLE")
        if trips is None:
            statuses[domain_rule].append("NOT_EVALUABLE")
        else:
            trips_state, trips_bad_rows = _g03_csv_evidence(g03_result, "trips.txt")
            if trips_state == "INSPECTION_ERROR":
                statuses[domain_rule].append("INSPECTION_ERROR")
            elif trips_state == "NOT_EVALUABLE":
                statuses[domain_rule].append("NOT_EVALUABLE")
            elif "service_id" not in trips[0]:
                statuses[domain_rule].append("NOT_EVALUABLE")
            elif calendar is None and dates is None:
                statuses[domain_rule].append("NOT_EVALUABLE")
            else:
                trips_field_unavailable, trips_type_bad = _g03_field_evidence(g03_result,"trips.txt","service_id")
                if trips_field_unavailable:statuses[domain_rule].append("NOT_EVALUABLE")
                trips_bad_rows |= trips_type_bad
                for _ in trips_bad_rows:
                    statuses[domain_rule].append("NOT_EVALUABLE")
                populated_trips = [] if trips_field_unavailable else [(index, record.get("service_id") or "")
                    for index, record in enumerate(trips[1], 1)
                    if index not in trips_bad_rows and record.get("service_id")]
                if not populated_trips and not trips_bad_rows:
                    statuses[domain_rule].append("NOT_APPLICABLE")
                for index, ref in populated_trips:
                    if ref in service_ids:
                        statuses[domain_rule].append("PASS")
                    elif domain_source_complete:
                        findings[domain_rule].append(_finding(domain_rule, "trips.txt", index, ["service_id"], ref,
                            "SERVICE_ID", "G01/G04 SERVICE_ID logical domain", "Populated service_id does not resolve in the available domain."))
                        statuses[domain_rule].append("FAIL_TECHNICAL")
                    else:
                        statuses[domain_rule].append("NOT_EVALUABLE")
        # Ordinary references and self references consume the reviewed inventory.
        ref_rule = "GTFS-G04-REFERENCE-EXISTENCE"
        constraints = [x for x in inventory["field_constraints"] if x.get("constraint_kind") == "REFERENTIAL_EXISTENCE"]
        for constraint in constraints:
            source = constraint["source_file"]
            target_files = constraint.get("physical_target_files", [])
            src, = (rows(source),)
            if constraint.get("logical_target_domain") == "SERVICE_ID":
                continue
            if src is None: statuses[ref_rule].append("NOT_APPLICABLE"); continue
            source_state, source_bad_rows = _g03_csv_evidence(g03_result, source)
            if source_state == "INSPECTION_ERROR":
                statuses[ref_rule].append("INSPECTION_ERROR"); continue
            if source_state == "NOT_EVALUABLE":
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            for _ in source_bad_rows:
                statuses[ref_rule].append("NOT_EVALUABLE")
            field = constraint["source_field"]
            if field not in src[0]: statuses[ref_rule].append("NOT_EVALUABLE"); continue
            source_field_unavailable, source_type_bad_rows = _g03_field_evidence(g03_result, source, field)
            if source_field_unavailable:
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            for _ in source_type_bad_rows:
                statuses[ref_rule].append("NOT_EVALUABLE")
            populated = [(index, record.get(field) or "") for index, record in enumerate(src[1], 1)
                if index not in source_bad_rows and index not in source_type_bad_rows and record.get(field)]
            if not populated:
                if not source_bad_rows and not source_type_bad_rows: statuses[ref_rule].append("NOT_APPLICABLE")
                continue
            target_name = target_files[0] if len(target_files) == 1 else None
            if constraint.get("target_deferred") or not target_name:
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            target = rows(target_name)
            if target is None:
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            target_state, target_bad_rows = _g03_csv_evidence(g03_result, target_name)
            if target_state == "INSPECTION_ERROR":
                statuses[ref_rule].append("INSPECTION_ERROR"); continue
            if target_state == "NOT_EVALUABLE":
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            target_fields = constraint.get("target_fields", [])
            target_field = target_fields[0] if len(target_fields) == 1 else None
            if not target_field or target_field not in target[0]:
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            target_field_unavailable, target_type_bad_rows = _g03_field_evidence(g03_result, target_name, target_field)
            if target_field_unavailable:
                statuses[ref_rule].append("NOT_EVALUABLE"); continue
            target_ids = {record.get(target_field) for index, record in enumerate(target[1], 1)
                if index not in target_bad_rows and index not in target_type_bad_rows and record.get(target_field)}
            for index, value in populated:
                if value in target_ids: statuses[ref_rule].append("PASS")
                elif target_bad_rows or target_type_bad_rows: statuses[ref_rule].append("NOT_EVALUABLE")
                else:
                    findings[ref_rule].append(_finding(ref_rule, source, index, [field], value,
                        f"{target_name}.{target_field}", constraint.get("trace_source_locator", "GTFS Schedule Reference"), "Populated reference has no matching target identity."))
                    statuses[ref_rule].append("FAIL_TECHNICAL")
        # Contextual matching uses only declared record_id and optional record_sub_id.
        contextual_rule = "GTFS-G04-CONTEXTUAL-REFERENCE"
        policies = {p["table_name"]: p for p in inventory["contextual_reference_policies"]}
        translations = rows("translations.txt")
        if translations is not None:
            source_state, source_bad_rows = _g03_csv_evidence(g03_result, "translations.txt")
            if source_state == "INSPECTION_ERROR":
                statuses[contextual_rule].append("INSPECTION_ERROR")
                source_bad_rows = set(range(1, len(translations[1]) + 1))
            elif source_state == "NOT_EVALUABLE":
                statuses[contextual_rule].append("NOT_EVALUABLE")
                source_bad_rows = set(range(1, len(translations[1]) + 1))
            else:
                for _ in source_bad_rows:
                    statuses[contextual_rule].append("NOT_EVALUABLE")
            h, records = translations
            source_type_evidence={field:_g03_field_evidence(g03_result,"translations.txt",field)
                for field in ("table_name","record_id","record_sub_id")}
            source_type_unavailable=any(unavailable for unavailable,_ in source_type_evidence.values())
            source_type_bad_rows=set().union(*(bad for _,bad in source_type_evidence.values()))
            if source_type_unavailable:
                statuses[contextual_rule].append("NOT_EVALUABLE")
            elif not {"table_name", "record_id", "record_sub_id"}.issubset(h): statuses[contextual_rule].append("NOT_EVALUABLE")
            else:
                for index, record in enumerate(records, 1):
                    if index in source_bad_rows or index in source_type_bad_rows:
                        statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    selector = record.get("table_name") or ""
                    policy = policies.get(selector)
                    if policy is None or selector == "UNKNOWN_OR_UNOFFICIAL_SELECTOR":
                        statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    if selector == "feed_info": statuses[contextual_rule].append("NOT_APPLICABLE"); continue
                    if policy.get("support_status") == "DEFERRED": statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    target_file = policy.get("target_file")
                    target = rows(target_file) if target_file else None
                    recid_field = policy.get("record_id", {}).get("field")
                    sub_field = policy.get("record_sub_id", {}).get("field")
                    if target is None or recid_field not in target[0]: statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    target_state, target_bad_rows = _g03_csv_evidence(g03_result, target_file)
                    if target_state == "INSPECTION_ERROR": statuses[contextual_rule].append("INSPECTION_ERROR"); continue
                    if target_state == "NOT_EVALUABLE": statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    identity_fields = [recid_field] + ([sub_field] if sub_field and policy["record_sub_id"].get("primary_key_component") else [])
                    values = [record.get("record_id") or ""] + ([record.get("record_sub_id") or ""] if len(identity_fields) > 1 else [])
                    if any(not value for value in values): statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    target_field_evidence = [_g03_field_evidence(g03_result, target_file, field)
                        for field in identity_fields]
                    if any(unavailable for unavailable, _ in target_field_evidence):
                        statuses[contextual_rule].append("NOT_EVALUABLE"); continue
                    target_type_bad_rows = set().union(*(bad for _, bad in target_field_evidence))
                    target_keys = {tuple(row.get(f, "") for f in identity_fields)
                        for target_row, row in enumerate(target[1], 1)
                        if target_row not in target_bad_rows and target_row not in target_type_bad_rows}
                    if tuple(values) in target_keys: statuses[contextual_rule].append("PASS")
                    elif target_bad_rows or target_type_bad_rows: statuses[contextual_rule].append("NOT_EVALUABLE")
                    else:
                        findings[contextual_rule].append(_finding(contextual_rule, "translations.txt", index,
                            ["table_name", "record_id"] + (["record_sub_id"] if len(values) > 1 else []),
                            {"selector": selector, "identity": values}, f"{target_file} {identity_fields}",
                            policy.get("source_locator", "GTFS Schedule Reference"), "Contextual record identity does not resolve."))
                        statuses[contextual_rule].append("FAIL_TECHNICAL")
        for rule_id, definition in ((r.rule_id, r) for r in registry):
            local = statuses[rule_id]
            status = _aggregate(local, bool(findings[rule_id]))
            result["rules"].append({"rule_id": rule_id, "semantic_version": definition.semantic_version,
                "category": definition.category.value, "status": status, "coverage": {"evaluated": local.count("PASS") + local.count("FAIL_TECHNICAL"),
                "not_evaluable": local.count("NOT_EVALUABLE"), "not_applicable": local.count("NOT_APPLICABLE"), "state": "PARTIAL" if "NOT_EVALUABLE" in local else "FULL"},
                "specification_reference": f"GTFS Schedule Reference {REVISION}", "findings": findings[rule_id],
                "evaluator_executed": True})
        result["findings"] = [f for rows_ in findings.values() for f in rows_]
        result["status"] = _aggregate([r["status"] for r in result["rules"]], bool(result["findings"]))
        legacy_map = (("GTFS-REF-TRIP-ROUTE", ref_rule), ("GTFS-REF-SERVICE", domain_rule),
            ("GTFS-REF-SHAPE", ref_rule), ("GTFS-UNIQUE-PRIMARY-ID", "GTFS-G04-PRIMARY-KEY-UNIQUENESS"))
        legacy_findings = (legacy_result or {}).get("findings", [])
        comparison = []
        for legacy_id, g04_id in legacy_map:
            g04_findings = findings[g04_id]
            old = [f for f in legacy_findings if f.get("rule_id") == legacy_id]
            matched = 0
            for current in g04_findings:
                row_number = int(current["record_locator"].split(":", 1)[1])
                fields = current["source_fields"]
                observed = current["observed_identifier_or_reference"]
                for prior in old:
                    legacy_row = prior.get("row_locator", "")
                    legacy_row_number = int(legacy_row.split(":", 1)[1]) - 1 if legacy_row.startswith("record:") else None
                    old_value = prior.get("observed_value")
                    if (prior.get("table") == current["source_file"] and legacy_row_number == row_number
                            and prior.get("field") in fields
                            and (old_value == observed or isinstance(observed, list) and old_value in observed)):
                        matched += 1
                        break
            comparison.append({"legacy_rule_id": legacy_id, "g04_rule_id": g04_id,
                "legacy_findings": len(old), "g04_findings": len(g04_findings),
                "matching_finding_pairs": matched, "comparison": "OVERLAP_NOT_EQUIVALENCE",
                "legacy_preserved": True})
        result["legacy_comparison"] = comparison
        result["inventory_sha256"] = inventory["output_sha256"]
        return result
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        for rule_id, definition in ((r.rule_id, r) for r in registry):
            result["rules"].append({"rule_id": rule_id, "semantic_version": definition.semantic_version,
                "category": definition.category.value, "status": "INSPECTION_ERROR", "findings": [],
                "specification_reference": f"GTFS Schedule Reference {REVISION}", "evaluator_executed": True})
        return result


def _aggregate(statuses: list[str], has_findings: bool = False) -> str:
    if "FAIL_TECHNICAL" in statuses or has_findings: return "FAIL_TECHNICAL"
    if "INSPECTION_ERROR" in statuses: return "INSPECTION_ERROR"
    if "NOT_EVALUABLE" in statuses: return "NOT_EVALUABLE"
    if not statuses or all(s == "NOT_APPLICABLE" for s in statuses): return "NOT_APPLICABLE"
    return "PASS"
