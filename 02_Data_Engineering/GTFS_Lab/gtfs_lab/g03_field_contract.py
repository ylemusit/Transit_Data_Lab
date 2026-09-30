"""Fail-closed loader and validator for the G03 field-level GTFS contract."""
from __future__ import annotations

from datetime import datetime
import json
import math
from pathlib import Path
import re
from collections import Counter
from typing import Any

from .g03_structure import CATALOG_RELATIVE_PATH, EXPECTED_REVISION, load_official_catalog

FIELD_CONTRACT_RELATIVE_PATH = Path("spec") / "gtfs_schedule_fields_2026_04_27.json"
EXPECTED_SCHEMA_VERSION = "1.0.0"
PRESENCE_VOCABULARY = {
    "REQUIRED", "CONDITIONALLY_REQUIRED", "OPTIONAL", "RECOMMENDED", "CONDITIONALLY_FORBIDDEN"
}
OWNERSHIP_VOCABULARY = {
    "G03_STRUCTURE", "G03_SCHEMA", "G03_TYPE_FORMAT", "G04_IDENTITY_REFERENTIAL",
    "G05_TEMPORAL", "G06_SEQUENCE", "G07_SPATIAL", "G08_QUALITY", "DEFERRED_V1", "NEEDS_REVIEW",
}
CONDITION_OPERATORS = {
    "FILE_PRESENT", "FILE_ABSENT", "FIELD_PRESENT", "FIELD_VALUE_EQUALS", "FIELD_VALUE_IN",
    "ENTITY_EXISTS", "PARENT_ENTITY_EXISTS", "RELATED_FILE_PRESENT", "ONE_OF_FILES_PRESENT",
    "DEPENDENT_FIELDS", "ALL", "ANY", "NOT", "ALL_SERVICE_DATES_DEFINED",
}
COMPOSITE_CONDITION_OPERATORS = {"ALL", "ANY", "NOT"}
EMPTY_VALUE_STATES = {"UNKNOWN", "NOT_SPECIFIED", "SOURCE_MENTIONS_EMPTY"}
EMPTY_MEANING_STATES = {
    "UNKNOWN", "NOT_SPECIFIED", "NEEDS_REVIEW", "EXPLICIT", "SAME_AS_ENUM_VALUE",
    "SAME_AS_NUMERIC_VALUE", "NO_PUBLIC_CODE", "UNDEFINED", "DEFAULT_VALUE", "UNAVAILABLE",
}
RANGE_STATES = {"NORMATIVE_RANGE", "RECOMMENDED_RANGE", "NO_EXPLICIT_RANGE", "NOT_NORMALIZED_REQUIRES_REVIEW"}
PINNED_FIELD_COUNTS = {
    "agency.txt": 9, "stops.txt": 16, "routes.txt": 14, "trips.txt": 13,
    "stop_times.txt": 18, "calendar.txt": 10, "calendar_dates.txt": 3,
    "shapes.txt": 5, "frequencies.txt": 5, "transfers.txt": 8, "pathways.txt": 12,
    "levels.txt": 3, "translations.txt": 7, "feed_info.txt": 9,
}
PINNED_TYPE_SOURCE_MAP = {
    "Color": "COLOR", "Date": "DATE", "Email": "EMAIL", "Enum": "ENUM", "Float": "FLOAT",
    "ID": "ID", "Language code": "LANGUAGE_CODE", "Latitude": "LATITUDE", "Longitude": "LONGITUDE",
    "Non-negative float": "NON_NEGATIVE_FLOAT", "Non-negative integer": "NON_NEGATIVE_INTEGER",
    "Non-null integer": "NON_NULL_INTEGER", "Phone number": "PHONE_NUMBER", "Positive float": "POSITIVE_FLOAT",
    "Positive integer": "POSITIVE_INTEGER", "Text": "TEXT",
    "Text or URL or Email or Phone number": "TEXT_OR_URL_OR_EMAIL_OR_PHONE_NUMBER",
    "Time": "TIME", "Timezone": "TIMEZONE", "Unique ID": "UNIQUE_ID", "URL": "URL",
    "Foreign ID": "FOREIGN_ID",
    "Foreign ID referencing agency.agency_id": "FOREIGN_ID",
    "Foreign ID referencing booking_rules.booking_rule_id": "FOREIGN_ID",
    "Foreign ID referencing calendar.service_id or ID": "FOREIGN_ID",
    "Foreign ID referencing calendar.service_id or calendar_dates.service_id": "FOREIGN_ID",
    "Foreign ID referencing id from locations.geojson": "FOREIGN_ID",
    "Foreign ID referencing levels.level_id": "FOREIGN_ID",
    "Foreign ID referencing location_groups.location_group_id": "FOREIGN_ID",
    "Foreign ID referencing routes.route_id": "FOREIGN_ID",
    "Foreign ID referencing shapes.shape_id": "FOREIGN_ID",
    "Foreign ID referencing stops.stop_id": "FOREIGN_ID",
    "Foreign ID referencing trips.trip_id": "FOREIGN_ID",
}


class FieldContractError(RuntimeError):
    """Raised when the field contract or its G01 parent is unsafe to consume."""


def _fail(message: str) -> None:
    raise FieldContractError(message)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _validate_condition_expression(expression: Any, expected_operator: str, field_name: str) -> None:
    if not isinstance(expected_operator, str) or expected_operator not in CONDITION_OPERATORS:
        _fail(f"invalid condition operator for {field_name}: {expected_operator!r}")
    if not isinstance(expression, dict) or expression.get("op") != expected_operator:
        _fail(f"malformed condition expression for {field_name}")
    if expected_operator in {"ALL", "ANY"}:
        children = expression.get("conditions")
        if not isinstance(children, list) or not children:
            _fail(f"composite condition requires child conditions for {field_name}")
        for child in children:
            if not isinstance(child, dict):
                _fail(f"malformed child condition for {field_name}")
            _validate_condition_expression(child, child.get("op"), field_name)
        return
    if expected_operator == "NOT":
        child = expression.get("condition")
        if not isinstance(child, dict):
            _fail(f"NOT condition requires one child condition for {field_name}")
        _validate_condition_expression(child, child.get("op"), field_name)
        return
    if expected_operator == "FIELD_VALUE_EQUALS":
        if not expression.get("field") or "value" not in expression:
            _fail(f"FIELD_VALUE_EQUALS requires field and value for {field_name}")
    elif expected_operator == "FIELD_VALUE_IN":
        if not expression.get("field") or not isinstance(expression.get("values"), list) or not expression["values"]:
            _fail(f"FIELD_VALUE_IN requires field and values for {field_name}")
    elif not any(expression.get(key) for key in ("file", "field", "subject", "entity", "target", "files")):
        _fail(f"condition has no subject for {field_name}")


def validate_field_contract(
    payload: dict[str, Any],
    *,
    catalog: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate structure and cross-check every contract file against authoritative G01 scope."""
    if not isinstance(payload, dict):
        _fail("field contract root must be an object")
    if payload.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        _fail(f"unexpected field contract schema_version: {payload.get('schema_version')!r}")
    if payload.get("specification_revision") != EXPECTED_REVISION:
        _fail(f"field contract revision must be {EXPECTED_REVISION}")
    official = payload.get("official_reference_url")
    if official != "https://gtfs.org/documentation/schedule/reference/":
        _fail("field contract must cite the official GTFS Schedule Reference")
    if payload.get("specification_name") != "GTFS Schedule":
        _fail("field contract specification_name must be GTFS Schedule")
    if payload.get("legal_authority_claimed") is not False:
        _fail("legal_authority_claimed must be false")
    if payload.get("parent_file_catalog") != CATALOG_RELATIVE_PATH.name:
        _fail("field contract parent catalog mismatch")
    parent_version = payload.get("parent_file_catalog_schema_version")
    if parent_version != "1.0.0":
        _fail("field contract parent catalog schema version mismatch")
    try:
        retrieved = datetime.fromisoformat(str(payload.get("retrieved_at", "")).replace("Z", "+00:00"))
    except ValueError as exc:
        raise FieldContractError("retrieved_at must be an ISO-8601 timestamp") from exc
    if retrieved.tzinfo is None:
        _fail("retrieved_at must include a timezone")
    snapshot_hash = payload.get("source_snapshot_sha256")
    if not isinstance(snapshot_hash, str) or not re.fullmatch(r"[A-F0-9]{64}", snapshot_hash):
        _fail("source_snapshot_sha256 must be an uppercase SHA-256 digest")

    vocabulary = payload.get("presence_vocabulary")
    if not isinstance(vocabulary, list) or set(vocabulary) != PRESENCE_VOCABULARY or len(vocabulary) != len(PRESENCE_VOCABULARY):
        _fail("presence_vocabulary must exactly match the adopted GTFS vocabulary")
    type_rows = payload.get("type_vocabulary")
    if not isinstance(type_rows, list) or not type_rows:
        _fail("type_vocabulary must be a non-empty list")
    type_tokens: set[str] = set()
    type_source_map: dict[str, str] = {}
    declared_type_counts: dict[str, int] = {}
    for item in type_rows:
        if not isinstance(item, dict) or not isinstance(item.get("token"), str):
            _fail("type_vocabulary entries require a token")
        token = item["token"]
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", token) or token in type_tokens:
            _fail(f"invalid or duplicate type token: {token!r}")
        type_tokens.add(token)
        if not isinstance(item.get("official_source_types"), list) or not item["official_source_types"]:
            _fail(f"type token {token} must retain official source types")
        if not isinstance(item.get("observed_field_count"), int) or item["observed_field_count"] < 1:
            _fail(f"type token {token} must have a positive observed field count")
        definition = item.get("definition")
        if not isinstance(definition, dict) or not definition.get("summary") or definition.get("status") not in {"EXPLICIT", "PARTIAL", "NEEDS_REVIEW"}:
            _fail(f"type definition metadata is malformed for {token}")
        if definition.get("source_locator") != official + "#field-types":
            _fail(f"type definition source locator is missing for {token}")
        for source_type in item["official_source_types"]:
            if not isinstance(source_type, str) or not source_type or source_type in type_source_map:
                _fail(f"duplicate or invalid official type label: {source_type!r}")
            type_source_map[source_type] = token
        declared_type_counts[token] = item["observed_field_count"]
    if type_source_map != PINNED_TYPE_SOURCE_MAP:
        _fail("type vocabulary does not match the official types observed for the pinned revision")

    parent = catalog if catalog is not None else load_official_catalog()
    files = payload.get("files")
    if not isinstance(files, list):
        _fail("files must be a list")
    file_names: list[str] = []
    field_total = 0
    observed_types: Counter[str] = Counter()
    observed_presence: Counter[str] = Counter()
    for file_entry in files:
        if not isinstance(file_entry, dict):
            _fail("file definitions must be objects")
        name = file_entry.get("file_name")
        if not isinstance(name, str) or not name or name.casefold() not in parent:
            _fail(f"field contract file does not exist in G01: {name!r}")
        if name in file_names:
            _fail(f"duplicate file definition: {name}")
        file_names.append(name)
        parent_entry = parent[name.casefold()]
        if not str(parent_entry.get("tdl_v1_support", "")).startswith("FULL_V1_TECHNICAL"):
            _fail(f"deferred G01 file cannot become full V1 through field contract: {name}")
        expected_anchor = parent_entry.get("reference_anchor")
        if file_entry.get("reference_anchor") != expected_anchor:
            _fail(f"file reference anchor mismatch for {name}")
        fields = file_entry.get("fields")
        if not isinstance(fields, list) or not fields:
            _fail(f"file {name} must contain field definitions")
        if len(fields) != PINNED_FIELD_COUNTS.get(name):
            _fail(f"field count differs from official reference for {name}")
        identities: set[str] = set()
        for field in fields:
            if not isinstance(field, dict):
                _fail(f"field definitions for {name} must be objects")
            field_name = field.get("field_name")
            if not isinstance(field_name, str) or not field_name:
                _fail(f"missing field_name in {name}")
            if field_name in identities:
                _fail(f"duplicate field definition: {name}.{field_name}")
            identities.add(field_name)
            field_total += 1
            presence = field.get("presence")
            if not isinstance(presence, str) or presence not in PRESENCE_VOCABULARY:
                _fail(f"unknown presence vocabulary for {name}.{field_name}: {presence!r}")
            observed_presence[presence] += 1
            token = field.get("type")
            if not isinstance(token, str) or token not in type_tokens:
                _fail(f"unknown type token for {name}.{field_name}: {token!r}")
            source_type = field.get("type_source")
            if not isinstance(source_type, str) or type_source_map.get(source_type) != token:
                _fail(f"official type label does not map to normalized type for {name}.{field_name}")
            observed_types[token] += 1
            source = field.get("source_reference")
            if not isinstance(source, dict):
                _fail(f"missing source reference for {name}.{field_name}")
            if source.get("file_name") != name or source.get("field_name") != field_name:
                _fail(f"source reference identity mismatch for {name}.{field_name}")
            if source.get("specification_revision") != EXPECTED_REVISION:
                _fail(f"source reference revision mismatch for {name}.{field_name}")
            anchor = source.get("reference_anchor")
            if not isinstance(anchor, str) or not anchor.startswith(official + "#"):
                _fail(f"missing or invalid reference anchor for {name}.{field_name}")
            if anchor != file_entry.get("reference_anchor"):
                _fail(f"field reference anchor does not match its official file section: {name}.{field_name}")
            if source.get("type_source") != field.get("type_source") or not source.get("presence_source") or not source.get("source_locator"):
                _fail(f"source locator or normalized source label missing for {name}.{field_name}")

            condition = field.get("condition")
            if presence in {"CONDITIONALLY_REQUIRED", "CONDITIONALLY_FORBIDDEN"}:
                if not isinstance(condition, dict) or not isinstance(condition.get("source_reference"), dict):
                    _fail(f"conditional presence requires retained condition metadata: {name}.{field_name}")
                condition_source = condition["source_reference"]
                if (
                    condition_source.get("file_name") != name
                    or condition_source.get("field_name") != field_name
                    or condition_source.get("reference_anchor") != anchor
                    or condition_source.get("specification_revision") != EXPECTED_REVISION
                ):
                    _fail(f"conditional source locator mismatch: {name}.{field_name}")
                operator = condition.get("operator")
                if operator is not None and (not isinstance(operator, str) or operator not in CONDITION_OPERATORS):
                    _fail(f"invalid condition operator for {name}.{field_name}: {operator!r}")
                if operator is None and condition.get("normalization_status") != "NEEDS_REVIEW":
                    _fail(f"unresolved condition must be marked NEEDS_REVIEW: {name}.{field_name}")
                if operator is not None:
                    _validate_condition_expression(condition.get("expression"), operator, f"{name}.{field_name}")
            elif condition is not None:
                _fail(f"unconditional presence cannot carry condition metadata: {name}.{field_name}")

            policy = field.get("presence_policy")
            if policy is not None:
                if presence not in {"CONDITIONALLY_REQUIRED", "CONDITIONALLY_FORBIDDEN"} or not isinstance(policy, dict):
                    _fail(f"presence policy is only valid for conditional fields: {name}.{field_name}")
                if policy.get("default") not in {"OPTIONAL", "RECOMMENDED", "UNKNOWN"}:
                    _fail(f"invalid conditional presence default: {name}.{field_name}")
                rules = policy.get("rules")
                if not isinstance(rules, list) or not rules:
                    _fail(f"conditional presence policy requires rules: {name}.{field_name}")
                for rule in rules:
                    if not isinstance(rule, dict) or rule.get("effect") not in {"REQUIRED", "FORBIDDEN", "OPTIONAL", "RECOMMENDED"}:
                        _fail(f"invalid conditional presence effect: {name}.{field_name}")
                    expression = rule.get("when")
                    if not isinstance(expression, dict):
                        _fail(f"conditional presence rule requires an expression: {name}.{field_name}")
                    _validate_condition_expression(expression, expression.get("op"), f"{name}.{field_name}")

            empty = field.get("empty_value_semantics")
            if not isinstance(empty, dict) or not (
                isinstance(empty.get("empty_allowed"), bool)
                or isinstance(empty.get("empty_allowed"), str) and empty.get("empty_allowed") in EMPTY_VALUE_STATES
            ):
                _fail(f"invalid empty-value semantics for {name}.{field_name}")
            if empty.get("header_presence") != "FIELD_DECLARED_IN_HEADER":
                _fail(f"contradictory header-presence semantics for {name}.{field_name}")
            if empty.get("empty_has_semantic_value") not in EMPTY_MEANING_STATES:
                _fail(f"invalid empty-value meaning for {name}.{field_name}")

            allowed = field.get("allowed_values")
            allowed_status = field.get("allowed_values_status")
            if token == "ENUM":
                if allowed is None:
                    if allowed_status not in {"NOT_SPECIFIED_OR_UNPARSED_SOURCE", "DEFINED_BY_FIELD_REFERENCE"}:
                        _fail(f"enum metadata is malformed for {name}.{field_name}")
                    if allowed_status == "NOT_SPECIFIED_OR_UNPARSED_SOURCE" and (
                        "Valid options are:" in source.get("description_source", "")
                        or "Allowed values are:" in source.get("description_source", "")
                    ):
                        _fail(f"explicit enum definition was not normalized: {name}.{field_name}")
                elif not isinstance(allowed, list) or not allowed or allowed_status != "EXPLICIT_OFFICIAL_LIST":
                    _fail(f"enum allowed_values must be a non-empty explicitly sourced list: {name}.{field_name}")
                else:
                    values: set[str] = set()
                    for option in allowed:
                        if not isinstance(option, dict) or not isinstance(option.get("value"), str) or not option["value"]:
                            _fail(f"malformed enum option for {name}.{field_name}")
                        if option["value"] in values:
                            _fail(f"duplicate enum option for {name}.{field_name}: {option['value']}")
                        values.add(option["value"])
                if allowed_status == "DEFINED_BY_FIELD_REFERENCE":
                    reference = field.get("allowed_values_reference")
                    if not isinstance(reference, dict) or reference.get("file_name") not in (set(file_names) | {name}):
                        _fail(f"enum field reference is malformed: {name}.{field_name}")
                    target_name = reference.get("field_name")
                    target_file = next((row for row in files if row.get("file_name") == reference.get("file_name")), None)
                    target_field = next((row for row in target_file.get("fields", []) if row.get("field_name") == target_name), None) if target_file else None
                    if not target_field or target_field.get("type") != "ENUM" or not target_field.get("allowed_values"):
                        _fail(f"enum domain reference does not resolve to an explicit official enum: {name}.{field_name}")
            elif allowed is not None:
                _fail(f"non-enum field cannot declare enum allowed_values: {name}.{field_name}")

            range_value = field.get("range")
            range_status = field.get("range_status")
            if not isinstance(range_status, str) or range_status not in RANGE_STATES:
                _fail(f"invalid range status for {name}.{field_name}")
            if range_value is None:
                if range_status in {"NORMATIVE_RANGE", "RECOMMENDED_RANGE"}:
                    _fail(f"range status contradicts missing range definition: {name}.{field_name}")
            else:
                if not isinstance(range_value, dict) or range_status not in {"NORMATIVE_RANGE", "RECOMMENDED_RANGE"}:
                    _fail(f"malformed range definition for {name}.{field_name}")
                minimum, maximum = range_value.get("min"), range_value.get("max")
                if minimum is not None and not _is_number(minimum):
                    _fail(f"invalid range minimum for {name}.{field_name}")
                if maximum is not None and not _is_number(maximum):
                    _fail(f"invalid range maximum for {name}.{field_name}")
                if minimum is not None and maximum is not None and minimum > maximum:
                    _fail(f"contradictory range bounds for {name}.{field_name}")

            format_status = field.get("format_constraints_status")
            if not isinstance(format_status, str) or format_status not in {"NOT_SPECIFIED", "NOT_NORMALIZED_REQUIRES_REVIEW", "EXPLICIT_OFFICIAL"}:
                _fail(f"invalid format constraint status for {name}.{field_name}")
            scope = field.get("g03_validation_scope")
            if not isinstance(scope, str) or scope not in OWNERSHIP_VOCABULARY:
                _fail(f"invalid G03 scope ownership for {name}.{field_name}: {scope!r}")
            ownership = field.get("constraint_ownership")
            if not isinstance(ownership, list) or not ownership:
                _fail(f"missing constraint ownership for {name}.{field_name}")
            for constraint in ownership:
                stage = constraint.get("stage") if isinstance(constraint, dict) else None
                if not isinstance(stage, str) or stage not in OWNERSHIP_VOCABULARY:
                    _fail(f"invalid ownership classification for {name}.{field_name}")
            target = field.get("reference_target")
            if token == "FOREIGN_ID" and target is None and field.get("reference_target_status") != "NOT_SPECIFIED":
                _fail(f"foreign identifier target must be explicit or marked unspecified: {name}.{field_name}")
            if empty.get("empty_allowed") is True and not empty.get("source_evidence"):
                _fail(f"empty value is allowed without official source evidence: {name}.{field_name}")

    if observed_types != Counter({token: count for token, count in declared_type_counts.items()}):
        _fail("type_vocabulary observed counts do not match field definitions")
    if payload.get("presence_counts") != dict(sorted(observed_presence.items())):
        _fail("presence_counts do not match field definitions")
    expected_full = {name for name, item in parent.items() if str(item.get("tdl_v1_support", "")).startswith("FULL_V1_TECHNICAL")}
    expected_deferred = [name for name, item in parent.items() if str(item.get("tdl_v1_support", "")).startswith("DEFERRED")]
    if set(file_names) != expected_full:
        missing = sorted(expected_full - set(file_names))
        extra = sorted(set(file_names) - expected_full)
        _fail(f"field contract coverage differs from G01 FULL V1 scope; missing={missing}, extra={extra}")
    deferred = payload.get("FIELD_METADATA_DEFERRED")
    if deferred != expected_deferred:
        _fail("FIELD_METADATA_DEFERRED must exactly preserve G01 deferred files")
    complete = payload.get("FIELD_METADATA_COMPLETE_FOR_G03")
    if not isinstance(complete, list) or not set(complete).issubset(set(file_names)):
        _fail("FIELD_METADATA_COMPLETE_FOR_G03 must list only contract files")
    if complete:
        _fail("files cannot be marked complete while this contract has unresolved normalization gaps")

    extension = payload.get("extension_policy")
    if not isinstance(extension, dict) or extension.get("status") not in {"NORMATIVELY_RESOLVED", "NOT_NORMATIVELY_RESOLVED"}:
        _fail("extension policy must be explicitly resolved or marked NOT_NORMATIVELY_RESOLVED")
    if extension.get("status") == "NOT_NORMATIVELY_RESOLVED" and extension.get("unknown_header_action") != "DO_NOT_FAIL_SOLELY_FOR_EXTRA_FIELD":
        _fail("unresolved extension policy cannot reject extra headers")

    summary = payload.get("coverage_summary")
    if not isinstance(summary, dict) or summary.get("normalized_files") != len(files) or summary.get("normalized_fields") != field_total:
        _fail("coverage_summary counts do not match the contract")
    return {
        "status": "VALIDATED_WITH_METADATA_GAPS",
        "specification_revision": EXPECTED_REVISION,
        "parent_catalog_schema_version": parent_version,
        "normalized_files": len(files),
        "normalized_fields": field_total,
        "deferred_files": len(deferred),
        "field_metadata_complete_for_g03": complete,
        "extension_policy": extension["status"],
        "header_schema_unlocked": False,
        "field_type_unlocked": False,
    }


def load_field_contract(
    contract_path: Path | None = None,
    catalog_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load JSON and validate it against the checked-in G01 parent catalog."""
    root = Path(__file__).resolve().parents[1]
    path = contract_path or root / FIELD_CONTRACT_RELATIVE_PATH
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FieldContractError(f"G03 field contract is missing: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FieldContractError(f"G03 field contract cannot be parsed: {path}: {exc}") from exc
    parent = load_official_catalog(catalog_path or root / CATALOG_RELATIVE_PATH)
    result = validate_field_contract(payload, catalog=parent)
    return payload, result
