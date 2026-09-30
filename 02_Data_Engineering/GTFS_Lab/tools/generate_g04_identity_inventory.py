"""Build the scope-only G04 inventory from frozen G01/G03 contracts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec"
CONTRACT_PATH = SPEC / "gtfs_schedule_fields_2026_04_27.json"
CAPABILITY_PATH = SPEC / "gtfs_schedule_field_capability_map_2026_04_27.json"
CATALOG_PATH = SPEC / "gtfs_schedule_2026_04_27.json"
OUTPUT = SPEC / "gtfs_schedule_g04_identity_references_2026_04_27.json"
REVISION = "2026-04-27"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def target_parts(value: str) -> tuple[str, str] | None:
    match = re.fullmatch(r"([^.#()]+)\.([^.#()]+)", value)
    if not match:
        return None
    file_name, field_name = match.groups()
    if "." not in file_name:
        file_name += ".txt"
    return file_name, field_name


def primary_key_parts(file_name: str, declaration: str) -> dict[str, Any]:
    """Normalize only the explicit primary-key notation in the pinned catalog."""
    value = declaration.strip()
    if value.lower().startswith("none"):
        return {"key_type": "NONE", "component_fields": []}
    if value.startswith("*"):
        return {"key_type": "ALL_FIELDS", "component_fields": []}
    value = re.sub(r"\s*\([^)]*\)\s*$", "", value)
    components = [part.strip().strip("`") for part in re.split(r"\s*\+\s*|\s*,\s*", value) if part.strip()]
    if not components:
        raise ValueError(f"Unrecognized primary key declaration for {file_name}: {declaration}")
    return {"key_type": "SINGLE_FIELD" if len(components) == 1 else "COMPOSITE",
            "component_fields": components}


def contextual_policies(support: dict[str, str], catalog: dict[str, Any], primary_keys: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Selectors and component roles transcribed from the pinned translations reference."""
    direct = {
        "agency": ("agency_id", None), "stops": ("stop_id", None),
        "routes": ("route_id", None), "trips": ("trip_id", None),
        "stop_times": ("trip_id", "stop_sequence"),
        "pathways": ("pathway_id", None), "levels": ("level_id", None),
        "attributions": ("attribution_id", None),
    }
    recommended = {
        "calendar": ("service_id", None), "calendar_dates": ("service_id", "date"),
        "fare_attributes": ("fare_id", None), "fare_rules": ("fare_id", "route_id"),
        "shapes": ("shape_id", None), "frequencies": ("trip_id", "start_time"),
        "transfers": ("from_stop_id", "to_stop_id"),
    }
    policies = []
    declared_keys = {row["file_name"]: row for row in primary_keys}
    for entry in catalog["files"]:
        name = entry["file_name"]
        if name not in declared_keys:
            declared_keys[name] = {**primary_key_parts(name, entry.get("primary_key", "")), "file_name": name}
    for selector, mapping, basis in [
        *((name, pair, "EXPLICIT_REFERENCE_MAPPING") for name, pair in direct.items()),
        *((name, pair, "REFERENCE_RECOMMENDATION") for name, pair in recommended.items()),
    ]:
        pk = declared_keys.get(selector + ".txt", {"key_type": "NOT_DECLARED", "component_fields": []})
        primary_components = pk["component_fields"]
        status = "EXECUTABLE_IN_PRINCIPLE" if support.get(selector + ".txt", "").startswith("FULL_V1_TECHNICAL") else "NOT_EVALUABLE / DEFERRED_TARGET"
        policies.append({
            "table_name": selector,
            "mapping_basis": basis,
            "target_file": selector + ".txt",
            "target_primary_key_type": pk["key_type"],
            "target_primary_key": primary_components,
            "record_id": {"field": mapping[0], "role": "PRIMARY_RECORD_SELECTOR", "primary_key_component": mapping[0] in primary_components},
            "record_sub_id": ({"field": mapping[1], "role": "SECONDARY_RECORD_SELECTOR", "primary_key_component": mapping[1] in primary_components, "status": "APPLICABLE"}
                               if mapping[1] else {"field": None, "role": "NOT_APPLICABLE", "status": "NOT_APPLICABLE"}),
            "support_status": support.get(selector + ".txt", "NOT_IN_G01_CATALOG"),
            "evaluability": status,
            "source_locator": f"https://gtfs.org/documentation/schedule/reference/#translationstxt (record_id/record_sub_id table, {selector})",
            "operator_failure_on_deferred": False,
        })
    policies.extend([
        {"table_name": "feed_info", "target_file": "feed_info.txt", "support_status": support.get("feed_info.txt"),
         "evaluability": "NOT_APPLICABLE / RECORD_ID_FORBIDDEN", "record_id": {"status": "FORBIDDEN"},
         "record_sub_id": {"status": "FORBIDDEN"}, "source_locator": "https://gtfs.org/documentation/schedule/reference/#translationstxt (record_id and record_sub_id conditions)"},
        {"table_name": "UNKNOWN_OR_UNOFFICIAL_SELECTOR", "target_file": None, "support_status": "UNRESOLVED",
         "evaluability": "NOT_EVALUABLE / CONTEXTUAL_TARGET_UNRESOLVED", "record_id": {"status": "UNRESOLVED"},
         "record_sub_id": {"status": "UNRESOLVED"}, "operator_failure_on_deferred": False,
         "source_locator": "https://gtfs.org/documentation/schedule/reference/#translationstxt (allowed table_name values and unofficial fields note)"},
    ])
    return policies


def derive() -> dict[str, Any]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    capability = json.loads(CAPABILITY_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    fields = {(row["file_name"], row["field_name"]): row for row in capability["fields"]}
    support = {row["file_name"]: row["tdl_v1_support"] for row in catalog["files"]}
    full = {name for name, value in support.items() if value.startswith("FULL_V1_TECHNICAL")}
    deferred = {name for name, value in support.items() if value.startswith("DEFERRED")}
    primary_keys: list[dict[str, Any]] = []
    official_primary_keys = {"transfers.txt": "from_stop_id + to_stop_id + from_trip_id + to_trip_id + from_route_id + to_route_id"}
    for file in sorted(catalog["files"], key=lambda x: (x["file_name"].casefold(), x["file_name"])):
        if not file["tdl_v1_support"].startswith("FULL_V1_TECHNICAL"):
            continue
        declaration = official_primary_keys.get(file["file_name"], file.get("primary_key"))
        if not declaration:
            raise ValueError(f"Missing explicit primary key declaration for {file['file_name']}")
        normalized = primary_key_parts(file["file_name"], declaration)
        # These components own uniqueness as a tuple. Component meanings such as sequence
        # order remain with their declared stage owners.
        primary_keys.append({
            "file_name": file["file_name"], **normalized,
            "declaration": declaration,
            "catalog_declaration": file.get("primary_key"),
            "source_locator": f"{file['reference_anchor']} (Dataset Attributes, Primary key)",
            "support_status": file["tdl_v1_support"],
            "g04_evaluability": "EXECUTABLE_IN_PRINCIPLE" if normalized["key_type"] not in {"NONE", "ALL_FIELDS"} else "SCOPE_ONLY_REVIEW_REQUIRED",
            "component_ownership": ([{"field": field_name, "semantic_owner": "G07_SPATIAL_SEQUENCE" if file["file_name"] == "shapes.txt" else "G06_SEQUENCE_ORDER", "uniqueness_owner": "G04"}
                                     for field_name in normalized["component_fields"] if field_name.endswith("_sequence")]
                                    + [{"field": field_name, "semantic_owner": "G05_TEMPORAL", "uniqueness_owner": "G04"}
                                       for field_name in normalized["component_fields"] if field_name in {"date", "start_time"}]
                                    + [{"field": field_name, "semantic_owner": "G04_IDENTITY", "uniqueness_owner": "G04"}
                                       for field_name in normalized["component_fields"] if not field_name.endswith("_sequence") and field_name not in {"date", "start_time"}]),
            "uniqueness_ownership": "G04_COMPLETE_KEY", "reason": "Uniqueness applies to the complete explicitly declared primary key; component semantics remain with their named owner.",
        })
    records: list[dict[str, Any]] = []
    identity_domains = [{
        "domain_id": "SERVICE_ID",
        "domain_kind": "MULTI_SOURCE_IDENTITY_DOMAIN",
        "contributors": [
            {"file": "calendar.txt", "field": "service_id", "role": "IDENTITY_DOMAIN_CONTRIBUTOR"},
            {"file": "calendar_dates.txt", "field": "service_id", "role": "CONDITIONAL_IDENTITY_OR_REFERENCE",
             "condition": "If calendar.txt is present, values may reference calendar.service_id; if absent, populated values can establish SERVICE_ID identities."},
        ],
        "consumers": [{"file": "trips.txt", "field": "service_id", "role": "FOREIGN_REFERENCE"}],
    }]

    for file in sorted(contract["files"], key=lambda x: (x["file_name"].casefold(), x["file_name"])):
        for field in sorted(file["fields"], key=lambda x: x["field_name"]):
            name, field_name, token = file["file_name"], field["field_name"], field["type"]
            ownership = field.get("constraint_ownership", [])
            g04_owned = any(item.get("stage") == "G04_IDENTITY_REFERENTIAL" for item in ownership)
            if token not in {"UNIQUE_ID", "FOREIGN_ID"} and not g04_owned:
                continue
            source = field["source_reference"]
            presence = field.get("presence", "UNKNOWN")
            condition = field.get("condition")
            cap = fields[(name, field_name)]
            common = {
                "source_file": name,
                "source_field": field_name,
                "normalized_type": token,
                "identity_family": ("FIELD_UNIQUE_ID" if token == "UNIQUE_ID" else
                                    "CONTEXTUAL_FOREIGN_REFERENCE" if name == "translations.txt" and field_name in {"record_id", "record_sub_id"} else
                                    "FOREIGN_REFERENCE" if token == "FOREIGN_ID" else "G04_OWNED_FIELD"),
                "source_reference": source,
                "source_locator": source["source_locator"],
                "g03_presence_classification": presence,
                "populated_value_applicability": "NON_EMPTY_VALUES_ONLY; EMPTY_SEMANTICS_REMAIN_WITH_G03_OR_DECLARED_OWNER",
                "condition_status": condition.get("normalization_status", "CONDITION_NOT_DECLARED") if condition else "CONDITION_NOT_DECLARED",
                "proposed_g04_ownership": "IDENTITY_UNIQUENESS" if token == "UNIQUE_ID" else ("REFERENTIAL_EXISTENCE" if g04_owned else "UNRESOLVED_OWNERSHIP"),
                "g03_capability_classification": cap["primary_assessment"],
                "source_constraint_ownership": ownership,
            }
            if token == "UNIQUE_ID":
                record = {
                    **common,
                    "constraint_id": f"UNIQUE:{name}:{field_name}",
                    "constraint_kind": "UNIQUENESS",
                    "identity_role": "PRIMARY_OR_UNIQUE_ID",
                    "target_files": [name],
                    "target_fields": [field_name],
                    "target_inside_full_v1_technical": name in full,
                    "target_deferred": name in deferred,
                    "cross_stage_dependencies": ["G03 populated-value/presence input"],
                    "condition_status": condition.get("normalization_status", "NEEDS_REVIEW") if condition else "UNCONDITIONAL",
                    "proposed_evaluability": "EXECUTABLE_IF_SOURCE_FILE_AVAILABLE" if name in full else "NOT_EVALUABLE_DEFERRED_TARGET",
                    "reason": "UNIQUE_ID token supplies explicit uniqueness semantics; evaluate only populated values. No composite row identity or sequence constraint inferred.",
                }
                service_contributor = name == "calendar.txt" and field_name == "service_id"
                record.update({"source_identity": {"file": name, "field": field_name},
                               "target_identity": {"file": name, "field": field_name},
                               "logical_target_domain": "SERVICE_ID" if service_contributor else None,
                               "physical_target_files": [name],
                               "role": "IDENTITY_DOMAIN_CONTRIBUTOR", "condition": condition,
                               "evaluability": record["proposed_evaluability"],
                               "deferred_status": "DEFERRED" if name in deferred else "NOT_DEFERRED",
                               "cross_stage_ownership": cross_stage_ownership(ownership),
                               "trace_source_locator": source["source_locator"]})
                records.append(record)
            if token != "FOREIGN_ID" and not g04_owned:
                continue
            raw_targets = field.get("reference_target")
            raw_targets = raw_targets if isinstance(raw_targets, list) else ([raw_targets] if raw_targets else [])
            parsed = [target_parts(value) for value in raw_targets]
            unresolved = not raw_targets or any(item is None for item in parsed)
            targets = [item for item in parsed if item]
            target_files = sorted({item[0] for item in targets})
            target_fields = sorted({item[1] for item in targets})
            union = len(targets) > 1 and not unresolved
            simple_single = len(targets) == 1 and not unresolved
            self_ref = simple_single and target_files == [name]
            missing_catalog = sorted(set(target_files) - set(support))
            deferred_targets = sorted(set(target_files) & deferred)
            outside_full = sorted(set(target_files) - full)
            service_dates = name == "calendar_dates.txt" and field_name == "service_id"
            trips_service = name == "trips.txt" and field_name == "service_id"
            contextual_translation = name == "translations.txt" and field_name in {"record_id", "record_sub_id"}
            if service_dates:
                identity_role, evaluability = "CONDITIONAL_IDENTITY_OR_REFERENCE", "CONDITIONAL_ON_CALENDAR_PRESENCE"
            elif trips_service:
                identity_role, evaluability = "FOREIGN_REFERENCE", "EXECUTABLE_IF_SERVICE_ID_DOMAIN_COMPLETE"
            elif contextual_translation:
                identity_role, evaluability = "CONTEXTUAL_TARGET_UNRESOLVED", "NOT_EVALUABLE_CONTEXTUAL_TARGET_UNRESOLVED"
                unresolved = True
            elif unresolved:
                identity_role, evaluability = "UNRESOLVED_REFERENCE", "NOT_EVALUABLE_UNRESOLVED_TARGET"
            elif union:
                identity_role, evaluability = "MULTI_PARENT_REFERENCE", "EXECUTABLE_IF_UNION_DOMAIN_AVAILABLE"
            elif self_ref:
                identity_role, evaluability = "SELF_REFERENCE", "EXECUTABLE_IF_SOURCE_FILE_AVAILABLE"
            elif deferred_targets:
                identity_role, evaluability = "FOREIGN_REFERENCE", "NOT_EVALUABLE_DEFERRED_TARGET"
            else:
                identity_role, evaluability = "FOREIGN_REFERENCE", "EXECUTABLE_IF_SOURCE_AND_PARENT_AVAILABLE"
            if field_name == "parent_station" and self_ref:
                identity_role = "PARENT_REFERENCE"
            if missing_catalog and not service_dates and not trips_service and not contextual_translation:
                evaluability = "NOT_EVALUABLE_UNRESOLVED_TARGET_CATALOG_COVERAGE"
            if service_dates:
                target_files, target_fields, deferred_targets, outside_full = [], [], [], []
                unresolved = False
                reason = "calendar_dates.service_id contributes SERVICE_ID identities when calendar.txt is absent; when calendar.txt is present, values may reference calendar.service_id. It is not a mandatory independent parent."
            elif trips_service:
                target_files, target_fields, deferred_targets, outside_full = ["calendar.txt", "calendar_dates.txt"], ["service_id"], [], []
                unresolved = False
                reason = "The conceptual target is SERVICE_ID, constructed from calendar.service_id and conditionally calendar_dates.service_id; calendar_dates.txt is not an independent mandatory parent."
            elif unresolved:
                reason = "Target is not unambiguously encoded by normalized metadata; no target inferred."
            else:
                reason = "Target is explicit in the field contract."
            if union and not service_dates and not trips_service:
                reason = "Contract explicitly lists alternative target entities; this is one union-domain constraint, not independent mandatory parents."
            if deferred_targets:
                reason += " Deferred target coverage must yield NOT_EVALUABLE, never an operator failure."
            if self_ref:
                reason += " Same-file entity reference; parent validity is evaluated only if explicitly specified, with no invented graph restrictions."
            cross = sorted({item.get("stage") for item in ownership if item.get("stage") not in {"G04_IDENTITY_REFERENTIAL", "G03_TYPE_FORMAT", "G03_SCHEMA"}})
            record = {
                **common,
                "constraint_id": f"REFERENCE:{name}:{field_name}",
                "constraint_kind": "REFERENTIAL_EXISTENCE",
                "identity_role": identity_role,
                "target_files": target_files,
                "target_fields": target_fields,
                "target_inside_full_v1_technical": bool(target_files) and not outside_full and not unresolved,
                "target_deferred": bool(deferred_targets),
                "cross_stage_dependencies": cross + ["G03 populated-value/presence input"],
                "proposed_evaluability": evaluability,
                "reason": reason,
                "unresolved_target_tokens": [value for value, item in zip(raw_targets, parsed) if item is None],
                "target_files_missing_from_g01_catalog": missing_catalog,
                "deferred_target_files": deferred_targets,
            }
            record.update({"source_identity": {"file": name, "field": field_name},
                           "target_identity": {"domain": "SERVICE_ID"} if trips_service else None,
                           "logical_target_domain": "SERVICE_ID" if trips_service or service_dates else None,
                           "physical_target_files": target_files,
                           "role": identity_role, "condition": condition,
                           "evaluability": evaluability,
                           "deferred_status": "DEFERRED" if deferred_targets else "NOT_DEFERRED",
                           "cross_stage_ownership": cross_stage_ownership(ownership),
                           "trace_source_locator": source["source_locator"]})
            if contextual_translation:
                record["physical_target_files"] = []
                record["target_files"] = []
                record["target_fields"] = []
                record["target_identity"] = None
                record["contextual_target_candidates"] = [
                    {"contract_token": value,
                     "status": "DEFERRED_CANDIDATE" if "deferred domain" in value else "CONTEXTUAL_UNRESOLVED_CANDIDATE",
                     "operator_failure": False}
                    for value in raw_targets
                ]
                record["deferred_target_candidates"] = [value for value in raw_targets if "deferred domain" in value]
            if service_dates:
                record["constraint_kind"] = "IDENTITY_DOMAIN_CONTRIBUTION_WITH_CONDITIONAL_REFERENCE"
                record["target_files"] = ["calendar.txt"]
                record["target_fields"] = ["service_id"]
                record["target_identity"] = {"domain": "SERVICE_ID", "physical_target_files": ["calendar.txt"]}
            records.append(record)
    records.sort(key=lambda x: (x["source_file"].casefold(), x["source_file"], x["source_field"], x["constraint_kind"]))
    ids = [row["constraint_id"] for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate constraint identity")
    artifact: dict[str, Any] = {
        "schema_version": "1.0.0",
        "artifact": "G04_IDENTITY_REFERENTIAL_CONSTRAINT_INVENTORY",
        "status": "CREATED_LOCAL_UNPUBLISHED",
        "specification_revision": REVISION,
        "base_commit": "137ff4ed38da65fb3fb61f9804d729a1cee51feb",
        "legal_authority_claimed": False,
        "inputs": {
            "field_contract_sha256": sha(CONTRACT_PATH),
            "capability_map_sha256": sha(CAPABILITY_PATH),
            "g01_file_catalog_sha256": sha(CATALOG_PATH),
        },
        "identity_domains": identity_domains,
        "counts": {
            "field_level_identity_reference_candidates": len(records),
            "unique_id_fields": sum(row["normalized_type"] == "UNIQUE_ID" for row in records),
            "foreign_id_fields": sum(row["normalized_type"] == "FOREIGN_ID" for row in records),
            "single_field_primary_keys": sum(row["key_type"] == "SINGLE_FIELD" for row in primary_keys),
            "composite_primary_keys": sum(row["key_type"] == "COMPOSITE" for row in primary_keys),
            "identity_domains": len(identity_domains),
            "ordinary_foreign_references": sum(row["constraint_kind"] == "REFERENTIAL_EXISTENCE" and row["identity_role"] not in {"CONTEXTUAL_TARGET_UNRESOLVED", "UNRESOLVED_REFERENCE"} for row in records),
            "contextual_reference_policies": len(contextual_policies(support, catalog, primary_keys)),
            "deferred_target_references": sum(row["evaluability"] == "NOT_EVALUABLE / DEFERRED_TARGET" for row in contextual_policies(support, catalog, primary_keys)),
            "unresolved_contextual_references": sum(row["evaluability"] == "NOT_EVALUABLE / CONTEXTUAL_TARGET_UNRESOLVED" for row in contextual_policies(support, catalog, primary_keys)),
        },
        "field_constraints": records,
        "field_level_identity_reference_candidates": records,
        "primary_keys": primary_keys,
        "contextual_reference_policies": contextual_policies(support, catalog, primary_keys),
    }
    artifact["output_sha256"] = hashlib.sha256((json.dumps(artifact, ensure_ascii=False, indent=2) + "\n").encode()).hexdigest().upper()
    return artifact


def cross_stage_ownership(ownership: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [item for item in ownership if item.get("stage") != "G04_IDENTITY_REFERENTIAL"]


def main() -> int:
    data = (json.dumps(derive(), ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if "--check" in sys.argv:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data:
            print("G04 inventory is stale or differs from deterministic regeneration")
            return 1
        print("G04 inventory deterministic regeneration: PASS")
        return 0
    OUTPUT.write_bytes(data)
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
