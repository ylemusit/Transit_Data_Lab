"""G03 file catalog inspection backed by the normalized G01 catalog."""
from __future__ import annotations

import json
import csv
import io
from pathlib import Path, PurePosixPath
import zipfile
import math
import re
from datetime import datetime
from urllib.parse import urlsplit


from .rule_registry import (
    ApplicabilityExpression,
    ApplicabilityOperator,
    RequirementKind,
    RuleAuthority,
    RuleCategory,
    RuleDefinition,
    RuleRegistry,
    Severity,
    SpecificationReference,
    evaluate_applicability,
)

CATALOG_RELATIVE_PATH = Path("spec") / "gtfs_schedule_2026_04_27.json"
EXPECTED_SCHEMA_VERSION = "1.0.0"
EXPECTED_REVISION = "2026-04-27"
EXPECTED_FILE_COUNT = 32
SUPPORTED_TEXT_ENCODINGS = ("utf-8-sig", "utf-8", "cp1252")

_G03_RULES = {
    "GTFS-G03-CSV-STRUCTURE": ("STRUCTURE", "CSV_PARSE_AND_ROW_WIDTH"),
    "GTFS-G03-HEADER-SCHEMA": ("SCHEMA", "G01_FIELD_CONTRACT"),
    "GTFS-G03-FILE-PRESENCE": ("STRUCTURE", "G01_FILE_PRESENCE_CONDITIONS"),
    "GTFS-G03-FIELD-TYPE": ("TYPE_FORMAT", "G01_FIELD_TYPE_CONTRACT"),
}


def load_official_catalog(path: Path | None = None) -> dict[str, dict]:
    """Load and strictly validate G01's normalized official file catalog."""
    catalog_path = path or Path(__file__).resolve().parents[1] / CATALOG_RELATIVE_PATH
    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"G01 GTFS Schedule catalog is missing: {catalog_path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"G01 GTFS Schedule catalog cannot be parsed: {catalog_path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("G01 GTFS Schedule catalog root must be an object")
    if payload.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        raise RuntimeError(f"Unexpected G01 catalog schema_version: {payload.get('schema_version')!r}")
    spec = payload.get("specification")
    if not isinstance(spec, dict) or spec.get("revision_date") != EXPECTED_REVISION:
        raise RuntimeError(f"G01 catalog must declare specification revision {EXPECTED_REVISION}")
    files = payload.get("files")
    if not isinstance(files, list) or len(files) != EXPECTED_FILE_COUNT:
        raise RuntimeError(f"G01 catalog must contain exactly {EXPECTED_FILE_COUNT} file entries")
    identities: dict[str, dict] = {}
    for entry in files:
        if not isinstance(entry, dict):
            raise RuntimeError("G01 catalog file entries must be objects")
        name = entry.get("file_name")
        support = entry.get("tdl_v1_support")
        if not isinstance(name, str) or not name or PurePosixPath(name).name != name:
            raise RuntimeError(f"Invalid official file identity in G01 catalog: {name!r}")
        key = name.casefold()
        if key in identities:
            raise RuntimeError(f"Duplicate official file identity in G01 catalog: {name}")
        if not isinstance(support, str) or not support.strip():
            raise RuntimeError(f"Missing tdl_v1_support for official file: {name}")
        if not (support.startswith("FULL_V1_TECHNICAL") or support.startswith("DEFERRED")):
            raise RuntimeError(f"Unexpected tdl_v1_support for official file {name}: {support!r}")
        identities[key] = entry
    if len(identities) != EXPECTED_FILE_COUNT:
        raise RuntimeError(f"G01 catalog must contain {EXPECTED_FILE_COUNT} unique file identities")
    return identities


def _catalog_registry() -> RuleRegistry:
    return RuleRegistry([
        RuleDefinition(
            rule_id="GTFS-G03-FILE-CATALOG",
            semantic_version="1.0.0",
            category=RuleCategory.STRUCTURE,
            authority=RuleAuthority.GTFS_REQUIRED,
            severity=Severity.INFO,
            requirement=RequirementKind.REQUIRED,
            applicable_files=("ZIP archive",),
            specification_reference=SpecificationReference(
                "GTFS Schedule Reference", EXPECTED_REVISION, "File names and file extensions"
            ),
            applicability=ApplicabilityExpression(
                ApplicabilityOperator.SIGNAL_PRESENT, signal="archive.inspection_ready"
            ),
            evaluator_identity="gtfs_lab.g03_structure.inspect_archive_catalog/1",
            evaluator=inspect_archive_catalog,
            declared_coverage=("ZIP_MEMBER_DISCOVERY", "FILE_EXTENSION_DISCOVERY", "OFFICIAL_FILE_SUPPORT_CLASSIFICATION"),
        )
    ]).freeze()


def inspect_archive_catalog(ctx, catalog_path: Path | None = None) -> dict:
    """Inventory members and report official identity separately from support."""
    official = load_official_catalog(catalog_path)
    members: list[dict] = []
    try:
        with zipfile.ZipFile(ctx.source_zip) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                path = PurePosixPath(info.filename.replace("\\", "/"))
                entry = official.get(path.name.casefold()) if path.parent == PurePosixPath(".") else None
                member = {"path": info.filename, "extension": path.suffix}
                if path.parent != PurePosixPath("."):
                    member.update({"classification": "NESTED_MEMBER", "official_identity": None,
                                   "official_presence": None, "official_condition": None, "tdl_v1_support": None})
                elif entry is None:
                    member.update({"classification": "UNKNOWN_EXTENSION_OR_FILE", "official_identity": None,
                                   "official_presence": None, "official_condition": None, "tdl_v1_support": None})
                else:
                    support = entry["tdl_v1_support"]
                    supported = support.startswith("FULL_V1_TECHNICAL")
                    member.update({
                        "classification": "OFFICIAL_V1_SUPPORTED" if supported else "OFFICIAL_DEFERRED",
                        "official_identity": entry["file_name"],
                        "official_presence": entry.get("official_presence"),
                        "official_condition": entry.get("official_condition"),
                        "tdl_v1_support": support,
                    })
                members.append(member)
        members.sort(key=lambda member: (member["path"].casefold(), member["path"]))
        registry = _catalog_registry()
        rule = registry["GTFS-G03-FILE-CATALOG"]
        applicability = evaluate_applicability(rule.applicability, {"archive.inspection_ready": True})
        return {
            **registry.identity_map(), "rule_id": rule.rule_id, "semantic_version": rule.semantic_version,
            "applicability_trace": list(applicability.trace), "status": "PASS", "evaluator_executed": True,
            "checked_members": len(members), "members": members,
            "official_catalog_coverage": "COMPLETE", "catalog_revision": EXPECTED_REVISION,
            "limitation": "El inventario clasifica identidad y cobertura TDL V1; los archivos diferidos y desconocidos no generan por sí mismos findings de conformidad. No valida CSV, cabeceras, presencia condicional ni tipos/formatos.",
        }
    except (OSError, zipfile.BadZipFile) as exc:
        registry = _catalog_registry()
        rule = registry["GTFS-G03-FILE-CATALOG"]
        return {
            **registry.identity_map(), "rule_id": rule.rule_id, "semantic_version": rule.semantic_version,
            "status": "INSPECTION_ERROR", "evaluator_executed": True, "checked_members": 0,
            "members": [], "official_catalog_coverage": "COMPLETE", "catalog_revision": EXPECTED_REVISION,
            "limitation": "No se pudo enumerar el archivo ZIP.", "error": f"{type(exc).__name__}: {exc}",
        }


def _rule_registry() -> RuleRegistry:
    rules = list(_catalog_registry())
    evaluators = {
        "GTFS-G03-CSV-STRUCTURE": _evaluate_csv,
        "GTFS-G03-HEADER-SCHEMA": _evaluate_schema,
        "GTFS-G03-FILE-PRESENCE": _evaluate_presence,
        "GTFS-G03-FILE-RESTRICTIONS": _evaluate_restrictions,
        "GTFS-G03-FIELD-TYPE": _evaluate_types,
    }
    definitions = (
        ("GTFS-G03-CSV-STRUCTURE", RuleCategory.STRUCTURE, RuleAuthority.GTFS_REQUIRED,
         RequirementKind.REQUIRED, "CSV syntax and record width", "inspect_csv_structure/1",
         ("TEXT_DECODING", "CSV_PARSE", "HEADER_EXISTS", "HEADER_UNIQUENESS", "ROW_WIDTH")),
        ("GTFS-G03-HEADER-SCHEMA", RuleCategory.SCHEMA, RuleAuthority.GTFS_REQUIRED,
         RequirementKind.REQUIRED, "File and field definitions", "inspect_header_schema/1",
         ("REQUIRED_FIELDS", "UNKNOWN_FIELDS", "CONDITIONAL_FIELDS")),
        ("GTFS-G03-FILE-PRESENCE", RuleCategory.STRUCTURE, RuleAuthority.GTFS_CONDITIONAL,
         RequirementKind.CONDITIONALLY_REQUIRED, "File presence and conditional presence", "inspect_file_presence/1",
         ("REQUIRED", "CONDITIONALLY_REQUIRED", "OPTIONAL", "RECOMMENDED", "CONDITIONALLY_FORBIDDEN")),
        ("GTFS-G03-FILE-RESTRICTIONS", RuleCategory.STRUCTURE, RuleAuthority.GTFS_CONDITIONAL,
         RequirementKind.PROHIBITED_WHEN, "Conditionally forbidden files", "inspect_file_restrictions/1",
         ("CONDITIONALLY_FORBIDDEN",)),
        ("GTFS-G03-FIELD-TYPE", RuleCategory.TYPE_FORMAT, RuleAuthority.GTFS_REQUIRED,
         RequirementKind.REQUIRED, "Local field types and formats", "inspect_field_types/1",
         ("LEXICAL_TYPES", "ENUMS", "LOCAL_RANGES")),
    )
    for rule_id, category, authority, requirement, section, identity, coverage in definitions:
        rules.append(RuleDefinition(
            rule_id=rule_id, semantic_version="1.1.0" if rule_id == "GTFS-G03-HEADER-SCHEMA" else "1.0.0",
            category=category, authority=authority,
            severity=Severity.ERROR, requirement=requirement,
            applicable_files=("applicable GTFS Schedule files",),
            specification_reference=SpecificationReference("GTFS Schedule Reference", EXPECTED_REVISION, section),
            applicability=ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT, signal="archive.inspection_ready"),
            evaluator_identity=f"gtfs_lab.g03_structure.{identity}", evaluator=evaluators[rule_id],
            declared_coverage=(coverage + ("CONDITIONAL_ROW_PRESENCE",)
                               if rule_id == "GTFS-G03-HEADER-SCHEMA" else coverage),
        ))
    return RuleRegistry(rules).freeze()


def _metadata_gap() -> dict:
    return {
        "status": "G03_SPEC_METADATA_GAP",
        "missing_metadata": [
            "per-file declared field list with normative specification references",
            "per-field presence kind: REQUIRED, CONDITIONALLY_REQUIRED, OPTIONAL, RECOMMENDED or CONDITIONALLY_FORBIDDEN",
            "field nullability and empty-value semantics",
            "field lexical type/format and local range constraints",
            "enumeration values and conditional enum domains",
            "extensions policy defining when additional headers are allowed or forbidden",
            "condition expressions and runtime evidence requirements at field scope",
        ],
        "source_contract": f"G01 catalog {EXPECTED_REVISION} contains file-level metadata only; no per-file fields contract",
    }


def _evaluate_csv(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict, members: list[str]) -> dict:
    return _inspect_csv(source_zip, files, official)


def _evaluate_schema(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict, members: list[str]) -> dict:
    from .g03_field_contract import load_field_contract
    from .g03_condition_runtime import evaluate_presence_policy
    contract, _ = load_field_contract(catalog_path=Path(__file__).resolve().parents[1] / CATALOG_RELATIVE_PATH)
    capabilities = _load_capability_map()
    by_file = {row["file_name"].casefold(): row["fields"] for row in contract["files"]}
    caps = {(row["file_name"].casefold(), row["field_name"]): row for row in capabilities["fields"]}
    findings, decisions, unevaluable, conditional_rows = [], [], [], []
    for key, info in sorted(files.items()):
        entry = official.get(key)
        if not entry or not entry["tdl_v1_support"].startswith("FULL_V1_TECHNICAL") or key not in by_file:
            continue
        try:
            text, _ = _decode_text(_read_zip_member(source_zip, info))
            reader = csv.reader(io.StringIO(text, newline=""), strict=True)
            header = next(reader, None)
        except (UnicodeError, csv.Error):
            unevaluable.append({"file": entry["file_name"], "reason": "CSV_STRUCTURE_UNAVAILABLE"})
            continue
        if header is None:
            unevaluable.append({"file": entry["file_name"], "reason": "HEADER_UNAVAILABLE"})
            continue
        declared = {f["field_name"]: f for f in by_file[key]}
        actual = set(header)
        conditional_fields = {name: field for name, field in declared.items() if field.get("presence_policy")}
        if conditional_fields:
            for row_number, values in enumerate(reader, 1):
                if not values or len(values) != len(header):
                    continue  # CSV structure owns malformed row width; do not use partial signals.
                row = dict(zip(header, values))
                for name, field in conditional_fields.items():
                    resolution = evaluate_presence_policy(field["presence_policy"], row, actual)
                    effect = resolution["effect"]
                    if resolution["truth"] == "UNKNOWN":
                        unevaluable.append({"file": entry["file_name"], "field": name,
                                            "record": row_number, "reason": "CONDITION_UNKNOWN",
                                            "trace": resolution["trace"]})
                        continue
                    observed = row.get(name)
                    conditional_rows.append({"file": entry["file_name"], "field": name,
                                              "record": row_number, "effect": effect,
                                              "observed": observed if name in actual else "HEADER_ABSENT",
                                              "truth": resolution["truth"], "trace": resolution["trace"]})
                    violation = (effect == "REQUIRED" and (name not in actual or observed == "")) or (
                        effect == "FORBIDDEN" and name in actual and observed != ""
                    )
                    if violation:
                        findings.append(_finding(
                            "GTFS-G03-HEADER-SCHEMA", entry["file_name"], f"ROW:{row_number}", name,
                            observed if name in actual else "HEADER_ABSENT", effect,
                            field["source_reference"]["source_locator"],
                            f"Conditional field presence policy requires {effect.lower()} at this record",
                        ))
        for name, field in declared.items():
            map_row = caps.get((key, name))
            assessment = map_row.get("primary_assessment") if map_row else None
            if assessment == "UNRESOLVED_CONDITION":
                unevaluable.append({"file": entry["file_name"], "field": name, "reason": "UNRESOLVED_CONDITION"})
            elif field["presence"] == "REQUIRED" and name not in actual:
                findings.append(_finding("GTFS-G03-HEADER-SCHEMA", entry["file_name"], "HEADER", name,
                                         "ABSENT", "required header present", field["source_reference"]["source_locator"],
                                         "Normative contract marks this header REQUIRED"))
            decisions.append({"file": entry["file_name"], "field": name, "assessment": assessment,
                              "presence": field["presence"], "header_present": name in actual})
        # Extension policy is unresolved: retain unknown headers as observations, never findings.
        for name in sorted(actual - set(declared)):
            decisions.append({"file": entry["file_name"], "field": name, "assessment": "UNKNOWN_HEADER",
                              "status": "NOT_EVALUABLE_EXTENSION_POLICY"})
            unevaluable.append({"file": entry["file_name"], "field": name, "reason": "UNRESOLVED_EXTENSION_POLICY"})
    status = "FAIL_TECHNICAL" if findings else "NOT_EVALUABLE" if unevaluable or not decisions else "PASS"
    return {"status": status, "findings": findings, "decisions": decisions,
            "conditional_rows": conditional_rows, "not_evaluable": unevaluable,
            "evaluator_executed": True, "capability_map_revision": capabilities["specification_revision"],
            "coverage_limitation": "Conditional header requirements with unresolved predicates are NOT_EVALUABLE; unknown headers are observed but not rejected while extension policy is unresolved."}


def _evaluate_presence(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict, members: tuple[list[str], dict]) -> dict:
    member_names, csv_result = members
    return _presence(files, official, member_names, csv_result)


def _evaluate_restrictions(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict, members: tuple[list[str], dict]) -> dict:
    result = _evaluate_presence(source_zip, files, official, members)
    findings = [finding for finding in result["findings"]
                if finding["rule_id"] == "GTFS-G03-FILE-RESTRICTIONS"]
    return {**result, "status": "FAIL_TECHNICAL" if findings else "PASS", "findings": findings}


def _evaluate_types(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict, members: list[str]) -> dict:
    from .g03_field_contract import load_field_contract
    from .g03_capability_map import EXECUTABLE_TYPE_VALIDATORS
    contract, _ = load_field_contract(catalog_path=Path(__file__).resolve().parents[1] / CATALOG_RELATIVE_PATH)
    capabilities = _load_capability_map()
    rows = {(row["file_name"].casefold(), row["field_name"]): row for row in capabilities["fields"]}
    findings, checked, not_evaluable = [], 0, []
    for key, info in sorted(files.items()):
        entry = official.get(key)
        if not entry or not entry["tdl_v1_support"].startswith("FULL_V1_TECHNICAL"):
            continue
        file_contract = next((f for f in contract["files"] if f["file_name"].casefold() == key), None)
        if not file_contract:
            continue
        try:
            text, _ = _decode_text(_read_zip_member(source_zip, info))
            reader = csv.reader(io.StringIO(text, newline=""), strict=True)
            header = next(reader, None)
            if header is None: continue
            positions = {name: i for i, name in enumerate(header)}
            values = {f["field_name"]: [] for f in file_contract["fields"] if f["field_name"] in positions}
            for record in reader:
                if record:
                    for name in values:
                        index = positions[name]
                        if index < len(record): values[name].append(record[index])
        except (UnicodeError, csv.Error):
            not_evaluable.append({"file": entry["file_name"], "reason": "CSV_STRUCTURE_UNAVAILABLE"}); continue
        for field in file_contract["fields"]:
            name = field["field_name"]
            cap = rows.get((key, name))
            if name not in positions or not cap or cap.get("primary_assessment") == "UNRESOLVED_CONDITION":
                continue
            if "UNRESOLVED_TYPE_FORMAT" in cap.get("capabilities", []) or field.get("format_constraints_status") != "EXPLICIT_OFFICIAL":
                not_evaluable.append({"file": entry["file_name"], "field": name, "reason": "UNRESOLVED_TYPE_FORMAT"}); continue
            if field.get("g03_validation_scope") != "G03_TYPE_FORMAT":
                continue
            if field["type"] not in EXECUTABLE_TYPE_VALIDATORS:
                not_evaluable.append({"file": entry["file_name"], "field": name,
                                      "reason": "UNSUPPORTED_LEXICAL_VALIDATOR"})
                continue
            allowed = {x["value"] for x in field.get("allowed_values") or []}
            for row_no, value in enumerate(values[name], 1):
                if value == "":
                    continue  # empty semantics are deliberately not inferred
                if not _field_type_valid(field, value):
                    findings.append(_finding("GTFS-G03-FIELD-TYPE", entry["file_name"], f"ROW:{row_no}", name,
                                             value, field["type"], field["source_reference"]["source_locator"],
                                             "Value does not satisfy the executable official lexical type"))
                elif field["type"] == "ENUM" and allowed and value not in allowed:
                    findings.append(_finding("GTFS-G03-FIELD-TYPE", entry["file_name"], f"ROW:{row_no}", name,
                                             value, "one of the explicitly sourced enum values", field["source_reference"]["source_locator"],
                                             "Value is outside the explicitly sourced enum domain"))
                elif field.get("range") and field.get("range_status") == "NORMATIVE_RANGE":
                    number = float(value)
                    bounds = field["range"]
                    if bounds.get("min") is not None and number < bounds["min"] or bounds.get("max") is not None and number > bounds["max"]:
                        findings.append(_finding("GTFS-G03-FIELD-TYPE", entry["file_name"], f"ROW:{row_no}", name,
                                                 value, f"range {bounds}", field["source_reference"]["source_locator"],
                                                 "Value is outside the explicit normative range"))
                checked += 1
    return {"status": "FAIL_TECHNICAL" if findings else "NOT_EVALUABLE" if not checked or not_evaluable else "PASS",
            "findings": findings, "checked_values": checked, "not_evaluable": not_evaluable,
            "evaluator_executed": True, "capability_map_revision": capabilities["specification_revision"],
            "coverage_limitation": "Only values with executable G03 capability and explicit normalized format constraints are checked; empty-value semantics and G04/G05/G07 ownership are not inferred."}


def _load_capability_map() -> dict:
    path = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_field_capability_map_2026_04_27.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    fields = payload.get("fields")
    if not isinstance(fields, list):
        raise RuntimeError("G03 capability map fields must be a list")
    counts = {}
    for row in fields:
        status = row.get("primary_assessment")
        if status not in {"EXECUTABLE_G03", "PARTIALLY_EXECUTABLE_G03", "UNRESOLVED_CONDITION"}:
            raise RuntimeError(f"Unexpected primary capability: {status!r}")
        counts[status] = counts.get(status, 0) + 1
        if not row.get("derivation_reason"):
            raise RuntimeError(f"G03 capability map field lacks derivation reason: {row.get('file_name')}.{row.get('field_name')}")
    if counts != payload.get("primary_assessment_counts"):
        raise RuntimeError(f"G03 capability map counts mismatch: {counts}")
    return payload


def aggregate_g03_statuses(components: dict[str, dict]) -> dict:
    """Aggregate relevant component results without hiding partial evaluation."""
    statuses = [row.get("status", "NOT_EVALUABLE") for row in components.values()]
    counts = {status: statuses.count(status) for status in (
        "PASS", "FAIL_TECHNICAL", "NOT_EVALUABLE", "NOT_APPLICABLE", "INSPECTION_ERROR"
    )}
    applicable = len(statuses) - counts["NOT_APPLICABLE"]
    if counts["FAIL_TECHNICAL"]:
        status = "FAIL_TECHNICAL"
    elif counts["INSPECTION_ERROR"]:
        status = "INSPECTION_ERROR"
    elif counts["NOT_EVALUABLE"]:
        status = "NOT_EVALUABLE"
    elif applicable == 0:
        status = "NOT_APPLICABLE"
    else:
        status = "PASS"
    evaluated = counts["PASS"] + counts["FAIL_TECHNICAL"]
    coverage = "NO_APPLICABLE_CASES" if applicable == 0 else (
        "PARTIAL" if counts["NOT_EVALUABLE"] else "FULL"
    )
    return {"status": status, "coverage": {
        "evaluated_count": evaluated,
        "not_evaluable_count": counts["NOT_EVALUABLE"],
        "not_applicable_count": counts["NOT_APPLICABLE"],
        "failed_count": counts["FAIL_TECHNICAL"],
        "total_applicable_count": applicable,
        "coverage_state": coverage,
    }}


def _field_type_valid(field: dict, value: str) -> bool:
    kind = field["type"]
    try:
        if kind in {"TEXT", "ID", "UNIQUE_ID", "FOREIGN_ID", "URL", "LANGUAGE_CODE", "TIMEZONE", "COLOR", "ENUM", "PHONE_NUMBER", "EMAIL", "TEXT_OR_URL_OR_EMAIL_OR_PHONE_NUMBER"}:
            if kind == "URL":
                parsed = urlsplit(value); return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
            if kind == "TIMEZONE": return bool(value) and " " not in value and "\\t" not in value
            if kind == "COLOR": return bool(re.fullmatch(r"[0-9A-Fa-f]{6}", value))
            return True
        if kind == "DATE":
            datetime.strptime(value, "%Y%m%d"); return len(value) == 8
        if kind == "TIME": return bool(re.fullmatch(r"\d{1,2}:\d{2}:\d{2}", value)) and int(value.split(":")[1]) < 60 and int(value.split(":")[2]) < 60
        if kind in {"NON_NEGATIVE_INTEGER", "POSITIVE_INTEGER", "NON_NULL_INTEGER"}:
            n = int(value); return str(n) == value and (kind != "NON_NEGATIVE_INTEGER" or n >= 0) and (kind != "POSITIVE_INTEGER" or n > 0)
        if kind in {"FLOAT", "NON_NEGATIVE_FLOAT", "POSITIVE_FLOAT", "LATITUDE", "LONGITUDE"}:
            n = float(value)
            if not math.isfinite(n): return False
            if kind == "NON_NEGATIVE_FLOAT" and n < 0 or kind == "POSITIVE_FLOAT" and n <= 0: return False
            bounds = field.get("range") if field.get("range_status") == "NORMATIVE_RANGE" else None
            return not bounds or (bounds.get("min") is None or n >= bounds["min"]) and (bounds.get("max") is None or n <= bounds["max"])
    except (ValueError, OverflowError): return False
    return True


def _decode_text(raw: bytes) -> tuple[str, str]:
    for encoding in SUPPORTED_TEXT_ENCODINGS:
        try:
            return raw.decode(encoding, errors="strict"), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeError("bytes are not valid UTF-8 or Windows-1252 text")


def _zip_files(source: Path) -> tuple[dict[str, zipfile.ZipInfo], list[str]]:
    """Index root-level TXT members under the ingestion size ceilings without loading them."""
    from .ingestion import MAX_MEMBER, MAX_TOTAL
    files: dict[str, zipfile.ZipInfo] = {}
    members: list[str] = []
    total = 0
    with zipfile.ZipFile(source) as archive:
        seen: set[str] = set()
        for info in archive.infolist():
            if info.is_dir():
                continue
            members.append(info.filename)
            normalized = info.filename.replace("\\", "/")
            key = normalized.casefold()
            if key in seen:
                raise ValueError(f"duplicate archive member: {info.filename}")
            seen.add(key)
            total += info.file_size
            if info.file_size > MAX_MEMBER or total > MAX_TOTAL:
                raise ValueError("archive size limit exceeded")
            path = PurePosixPath(normalized)
            if path.parent == PurePosixPath(".") and path.suffix.casefold() == ".txt":
                files[path.name.casefold()] = info
    return files, members


def _read_zip_member(source: Path, info: zipfile.ZipInfo) -> bytes:
    with zipfile.ZipFile(source) as archive:
        return archive.read(info)


def _finding(rule_id: str, file_name: str, locator: str, field: str | None,
             observed, expected: str, reference: str, reason: str) -> dict:
    return {"rule_id": rule_id, "file": file_name, "row_locator": locator, "field": field,
            "observed": observed, "expected": expected, "specification_reference": reference,
            "reason": reason}


def _condition_trace(signal: str, observed, expected=None, *, present: bool = False) -> list[dict]:
    expression = (ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT, signal=signal)
                  if present else ApplicabilityExpression(ApplicabilityOperator.SIGNAL_EQUALS,
                                                          signal=signal, expected=expected))
    return list(evaluate_applicability(expression, {signal: observed}).trace)


def _inspect_csv(source_zip: Path, files: dict[str, zipfile.ZipInfo], official: dict[str, dict]) -> dict:
    findings: list[dict] = []
    inspected = []
    statuses: list[str] = []
    condition_signals: dict[str, bool | None] = {
        "field:pathways.pathway_mode=5": False,
        "field:routes.network_id": False,
    }
    for member_name, info in sorted(files.items()):
        entry = official.get(member_name)
        if entry is None or not entry["tdl_v1_support"].startswith("FULL_V1_TECHNICAL"):
            continue
        raw = _read_zip_member(source_zip, info)
        ref = entry.get("reference_anchor", "GTFS Schedule Reference")
        display = entry["file_name"]
        try:
            text, encoding = _decode_text(raw)
        except UnicodeError as exc:
            findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, "FILE", None,
                                     "UNDECODABLE", "UTF-8/Windows-1252 decodable text", ref, str(exc)))
            statuses.append("FAIL_TECHNICAL")
            inspected.append({"file": display, "status": "FAIL_TECHNICAL", "encoding": None, "data_rows": 0})
            if display == "pathways.txt":
                condition_signals["field:pathways.pathway_mode=5"] = None
            elif display == "routes.txt":
                condition_signals["field:routes.network_id"] = None
            continue
        try:
            reader = csv.reader(io.StringIO(text, newline=""), strict=True)
            header = next(reader, None)
            if header is None:
                findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, "HEADER", None,
                                         "EMPTY_FILE", "header row", ref, "The file has no CSV header record"))
                statuses.append("FAIL_TECHNICAL")
                inspected.append({"file": display, "status": "FAIL_TECHNICAL", "encoding": encoding, "data_rows": 0})
                if display == "pathways.txt":
                    condition_signals["field:pathways.pathway_mode=5"] = None
                elif display == "routes.txt":
                    condition_signals["field:routes.network_id"] = None
                continue
            if display == "pathways.txt":
                if "pathway_mode" in header:
                    condition_signals["field:pathways.pathway_mode=5"] = False
                    pathway_mode_index = header.index("pathway_mode")
                else:
                    condition_signals["field:pathways.pathway_mode=5"] = None
                    pathway_mode_index = None
            else:
                pathway_mode_index = None
            if display == "routes.txt":
                condition_signals["field:routes.network_id"] = "network_id" in header
            if not header or any(not item.strip() for item in header):
                findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, "HEADER", None,
                                         header, "non-empty header names", ref, "Header is empty or contains an empty name"))
            duplicates = sorted({item for item in header if header.count(item) > 1})
            for name in duplicates:
                findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, "HEADER", name,
                                         name, "unique header name", ref, "Duplicate CSV header name"))
            rows = 0
            for row in reader:
                if row == []:
                    continue
                rows += 1
                if pathway_mode_index is not None and len(row) > pathway_mode_index and row[pathway_mode_index] == "5":
                    condition_signals["field:pathways.pathway_mode=5"] = True
                if len(row) != len(header):
                    findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, f"ROW:{rows}", None,
                                             len(row), f"{len(header)} columns", ref, "CSV row width differs from header"))
                    if pathway_mode_index is not None and len(row) <= pathway_mode_index:
                        condition_signals["field:pathways.pathway_mode=5"] = None
            local = [item for item in findings if item["file"] == display and item["rule_id"] == "GTFS-G03-CSV-STRUCTURE"]
            status = "FAIL_TECHNICAL" if local else "PASS"
            statuses.append(status)
            inspected.append({"file": display, "status": status, "encoding": encoding,
                              "header_columns": len(header), "data_rows": rows, "headers": header})
        except csv.Error as exc:
            findings.append(_finding("GTFS-G03-CSV-STRUCTURE", display, "FILE", None,
                                     "MALFORMED_CSV", "well-formed CSV quoting", ref, str(exc)))
            statuses.append("FAIL_TECHNICAL")
            inspected.append({"file": display, "status": "FAIL_TECHNICAL", "encoding": encoding, "data_rows": 0})
            if display == "pathways.txt":
                condition_signals["field:pathways.pathway_mode=5"] = None
            elif display == "routes.txt":
                condition_signals["field:routes.network_id"] = None
    status = "FAIL_TECHNICAL" if "FAIL_TECHNICAL" in statuses else "PASS"
    return {"status": status, "files_inspected": inspected, "findings": findings,
            "checked_files": len(inspected), "signals": condition_signals, "evaluator_executed": True}


def _presence(files: dict[str, zipfile.ZipInfo], official: dict[str, dict], archive_members: list[str] = (), csv_result: dict | None = None) -> dict:
    findings: list[dict] = []
    decisions: list[dict] = []
    signals: dict[str, bool | str | None] = {}
    present_names = {key for key in files}
    for member in archive_members:
        path = PurePosixPath(member.replace("\\", "/"))
        if path.parent == PurePosixPath("."):
            present_names.add(path.name.casefold())
    for key, entry in official.items():
        signals[f"file:{key[:-4]}"] = key in present_names
    # G01 conditions use evidence captured during the streaming CSV pass.
    condition_signals = (csv_result or {}).get("signals", {})
    pathway_mode_5: bool | None = condition_signals.get("field:pathways.pathway_mode=5", False)
    signals["field:pathways.pathway_mode=5"] = pathway_mode_5
    # Flex qualification requires interpreting locations.geojson; existence alone is insufficient.
    flex_condition: bool | None = False if "locations.geojson" not in present_names else None
    decisions.append({"file": "stops.txt", "requirement": "CONDITIONALLY_REQUIRED",
                      "condition": "Optional only when qualifying demand-responsive zones exist in locations.geojson",
                      "truth": "FALSE" if flex_condition is False else "UNKNOWN",
                      "reason": "locations.geojson absent" if flex_condition is False else "Flex zone qualification is outside V1 coverage",
                      "applicability_trace": _condition_trace("flex.qualifying_zone_exists", flex_condition, True)})
    if "stops.txt" not in present_names and flex_condition is False:
        findings.append(_finding("GTFS-G03-FILE-PRESENCE", "stops.txt", "FILE", None, "ABSENT",
                                 "present unless qualifying Flex zones make it optional",
                                 official["stops.txt"].get("reference_anchor", "GTFS Schedule Reference"),
                                 "Required fixed-stop file is absent"))
    # Direct normalized G01 conditions: translations -> feed_info; pathways mode 5 -> levels.
    for required_file, trigger, description in (
        ("feed_info.txt", "translations.txt", "Required when translations.txt is present"),
        ("levels.txt", "field:pathways.pathway_mode=5", "Required when pathways.pathway_mode=5 is present"),
    ):
        truth = signals["file:" + trigger[:-4]] if trigger.endswith(".txt") else signals[trigger]
        truth_name = "UNKNOWN" if truth is None else "TRUE" if truth else "FALSE"
        trigger_signal = "file:" + trigger[:-4] if trigger.endswith(".txt") else trigger
        trace = _condition_trace(trigger_signal, truth, True if trigger.startswith("field:") else None,
                                 present=trigger.endswith(".txt"))
        decisions.append({"file": required_file, "requirement": "CONDITIONALLY_REQUIRED",
                          "condition": description, "truth": truth_name,
                          "reason": "condition evaluated from G01 trigger", "applicability_trace": trace})
        if truth is True and required_file not in present_names:
            findings.append(_finding("GTFS-G03-FILE-PRESENCE", required_file, "FILE", None, "ABSENT",
                                     description, official[required_file].get("reference_anchor", "GTFS Schedule Reference"),
                                     "Conditionally required file is absent"))
        elif truth is False and required_file not in present_names:
            fallback = "RECOMMENDED" if required_file == "feed_info.txt" else "OPTIONAL"
            decisions.append({"file": required_file, "requirement": fallback, "truth": "NOT_APPLICABLE",
                              "reason": "conditional trigger is false; absence is not a failure"})
    if "pathways.txt" in present_names and pathway_mode_5 is None:
        decisions.append({"file": "levels.txt", "requirement": "CONDITIONALLY_REQUIRED", "truth": "UNKNOWN",
                          "condition": "pathways.pathway_mode=5", "reason": "pathways field cannot be parsed"})
    route_network_field: bool | None = condition_signals.get("field:routes.network_id", False)
    for forbidden_file in ("networks.txt", "route_networks.txt"):
        truth = "UNKNOWN" if route_network_field is None else "TRUE" if route_network_field else "FALSE"
        decisions.append({"file": forbidden_file, "requirement": "CONDITIONALLY_FORBIDDEN",
                          "condition": "Forbidden if routes.network_id is present", "truth": truth,
                          "reason": "field presence read from routes.txt header",
                          "applicability_trace": _condition_trace("field:routes.network_id", route_network_field, True)})
        if route_network_field is True and forbidden_file in present_names:
            findings.append(_finding("GTFS-G03-FILE-RESTRICTIONS", forbidden_file, "FILE", None, "PRESENT",
                                     "absent when routes.network_id is present",
                                     official[forbidden_file].get("reference_anchor", "GTFS Schedule Reference"),
                                     "G01 declares this file conditionally forbidden"))
    # Calendar condition: calendar_dates is directly required if calendar is absent.
    if "calendar.txt" not in present_names and "calendar_dates.txt" not in present_names:
        findings.append(_finding("GTFS-G03-FILE-PRESENCE", "calendar_dates.txt", "FILE", None, "ABSENT",
                                 "calendar_dates.txt when calendar.txt is absent",
                                 official["calendar_dates.txt"].get("reference_anchor", "GTFS Schedule Reference"),
                                 "G01 declares calendar_dates required when calendar is absent"))
    if "calendar.txt" not in present_names and "calendar_dates.txt" not in present_names:
        findings.append(_finding("GTFS-G03-FILE-PRESENCE", "calendar.txt", "FILE", None, "ABSENT",
                                 "calendar.txt or all service dates in calendar_dates.txt",
                                 official["calendar.txt"].get("reference_anchor", "GTFS Schedule Reference"),
                                 "calendar_dates.txt is also absent, so its conditional alternative cannot be satisfied"))
    decisions.extend([
        {"file": "calendar.txt", "requirement": "CONDITIONALLY_REQUIRED", "truth": "UNKNOWN" if "calendar.txt" not in present_names and "calendar_dates.txt" in present_names else "TRUE" if "calendar.txt" in present_names else "FALSE", "condition": "Required unless all service dates are defined in calendar_dates.txt", "reason": "all service dates requires service entity semantics outside G03"},
        {"file": "calendar_dates.txt", "requirement": "CONDITIONALLY_REQUIRED", "truth": "TRUE" if "calendar.txt" not in present_names and "calendar_dates.txt" in present_names else "FALSE" if "calendar.txt" in present_names else "UNKNOWN", "condition": "Required if calendar.txt is absent; optional otherwise", "reason": "G01 presence condition"},
    ])
    for key, entry in official.items():
        requirement = entry.get("official_presence")
        if key in present_names:
            continue
        if requirement == "REQUIRED":
            findings.append(_finding("GTFS-G03-FILE-PRESENCE", entry["file_name"], "FILE", None, "ABSENT",
                                     "file present", entry.get("reference_anchor", "GTFS Schedule Reference"),
                                     "G01 declares this file required"))
            decisions.append({"file": entry["file_name"], "requirement": requirement, "truth": "TRUE",
                              "reason": "required file absent"})
        elif requirement == "OPTIONAL":
            decisions.append({"file": entry["file_name"], "requirement": requirement, "truth": "NOT_APPLICABLE", "reason": "optional file absent"})
        elif requirement == "RECOMMENDED":
            decisions.append({"file": entry["file_name"], "requirement": requirement, "truth": "NOT_APPLICABLE", "reason": "recommended file absent; no failure"})
    status = "FAIL_TECHNICAL" if findings else "NOT_EVALUABLE" if any(item["truth"] == "UNKNOWN" for item in decisions) else "PASS"
    return {"status": status, "decisions": sorted(decisions, key=lambda row: row["file"]),
            "findings": findings, "evaluator_executed": True,
            "coverage_limitation": "Flex qualification and calendar all-service-date semantics remain unevaluated where required evidence crosses the G03 boundary."}


def inspect_g03_archive(source_zip: Path, catalog_path: Path | None = None) -> dict:
    """Run G03's independent archive preflight without producing legacy findings."""
    registry = _rule_registry()
    identities = registry.identity_map()
    try:
        official = load_official_catalog(catalog_path)
        files, member_names = _zip_files(source_zip)
        catalog_ctx = type("CatalogContext", (), {"source_zip": source_zip})()
        catalog = registry["GTFS-G03-FILE-CATALOG"].evaluator(catalog_ctx, catalog_path)
        csv_result = registry["GTFS-G03-CSV-STRUCTURE"].evaluator(source_zip, files, official, member_names)
        schema = registry["GTFS-G03-HEADER-SCHEMA"].evaluator(source_zip, files, official, member_names)
        presence = registry["GTFS-G03-FILE-PRESENCE"].evaluator(source_zip, files, official, (member_names, csv_result))
        gaps = registry["GTFS-G03-FIELD-TYPE"].evaluator(source_zip, files, official, member_names)
        restrictions = registry["GTFS-G03-FILE-RESTRICTIONS"].evaluator(
            source_zip, files, official, (member_names, csv_result))
        rules = []
        for rule_id, component in (
            ("GTFS-G03-FILE-CATALOG", catalog),
            ("GTFS-G03-CSV-STRUCTURE", csv_result),
            ("GTFS-G03-HEADER-SCHEMA", schema),
            ("GTFS-G03-FILE-PRESENCE", presence),
            ("GTFS-G03-FILE-RESTRICTIONS", restrictions),
            ("GTFS-G03-FIELD-TYPE", gaps),
        ):
            rule = registry[rule_id]
            disposition, applicability = registry.execution_disposition(rule, {"archive.inspection_ready": True})
            rules.append({"rule_id": rule_id, "semantic_version": identities["rule_versions"][rule_id],
                          "category": rule.category.value, "authority": rule.authority.value,
                          "severity": rule.severity.value, "requirement": rule.requirement.value,
                          "applicability": disposition if isinstance(disposition, str) else disposition.value,
                          "applicability_trace": list(applicability.trace),
                          "evaluator_identity": rule.evaluator_identity,
                          "status": component.get("status", "NOT_EVALUABLE"),
                          "evaluator_executed": component.get("evaluator_executed", False),
                          "specification_reference": f"GTFS Schedule Reference {EXPECTED_REVISION}",
                          "findings": component.get("findings", [])})
        rules.sort(key=lambda row: row["rule_id"])
        aggregate = aggregate_g03_statuses({"csv_structure": csv_result, "file_presence": presence,
                                            "header_schema": schema, "field_types": gaps,
                                            "file_restrictions": restrictions})
        return {**identities, "status": aggregate["status"], "coverage": aggregate["coverage"],
                "evaluator_executed": True, "archive_members": sorted(member_names, key=lambda x: (x.casefold(), x)),
                "file_catalog": catalog, "csv_structure": csv_result, "header_schema": schema,
                "file_presence": presence, "field_types": gaps, "rules": rules,
                "legacy_overlap": [
                    {"legacy_rule_id": "GTFS-STRUCT-REQUIRED", "comparison": "LEGACY_PARTIAL_OVERLAP", "reason": "legacy assumes stops.txt universally required; G03 models Flex condition"},
                    {"legacy_rule_id": "GTFS-STRUCT-SERVICE-CALENDAR", "comparison": "LEGACY_PARTIAL_OVERLAP", "reason": "legacy tests either calendar file; G03 uses conditional semantics"},
                    {"legacy_rule_id": "GTFS-REF-TRIP-ROUTE", "comparison": "OUTSIDE_G03", "reason": "foreign-key existence is G04"},
                    {"legacy_rule_id": "GTFS-REF-SERVICE", "comparison": "OUTSIDE_G03", "reason": "service ID reference existence is G04"},
                    {"legacy_rule_id": "GTFS-REF-SHAPE", "comparison": "OUTSIDE_G03", "reason": "shape ID reference existence is G04"},
                    {"legacy_rule_id": "GTFS-UNIQUE-PRIMARY-ID", "comparison": "OUTSIDE_G03", "reason": "cross-row uniqueness is G04"},
                    {"legacy_rule_id": "GTFS-COORDINATE-RANGE", "comparison": "LEGACY_PARTIAL_OVERLAP", "reason": "local coordinate ranges belong in G03 but await field type/range metadata in G01"},
                ],
                "coverage_limitations": [schema["coverage_limitation"], gaps["coverage_limitation"], presence["coverage_limitation"]]}
    except Exception as exc:
        return {**identities, "status": "INSPECTION_ERROR", "evaluator_executed": True,
                "file_catalog": {"status": "INSPECTION_ERROR", "findings": []},
                "csv_structure": {"status": "INSPECTION_ERROR", "findings": []},
                "header_schema": {"status": "NOT_EVALUABLE", "findings": []},
                "file_presence": {"status": "NOT_EVALUABLE", "findings": []},
                "field_types": {"status": "NOT_EVALUABLE", "findings": []},
                "rules": [{"rule_id": rule.rule_id, "semantic_version": rule.semantic_version,
                           "status": "INSPECTION_ERROR", "evaluator_executed": False,
                           "specification_reference": f"GTFS Schedule Reference {EXPECTED_REVISION}", "findings": []}
                          for rule in registry],
                "error": f"{type(exc).__name__}: {exc}"}
