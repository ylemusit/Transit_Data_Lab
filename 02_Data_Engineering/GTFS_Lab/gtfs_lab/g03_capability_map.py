"""Deterministically derive field capabilities from G03 source metadata."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "spec" / "gtfs_schedule_fields_2026_04_27.json"
CATALOG = ROOT / "spec" / "gtfs_schedule_2026_04_27.json"
OUTPUT = ROOT / "spec" / "gtfs_schedule_field_capability_map_2026_04_27.json"
RUNTIME = Path(__file__).with_name("rule_registry.py")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def derive_capability_map(contract: dict[str, Any], catalog: dict[str, Any], runtime_sha256: str) -> dict[str, Any]:
    fields = []
    counts: dict[str, int] = {}
    for file in sorted(contract["files"], key=lambda row: (row["file_name"].casefold(), row["file_name"])):
        for field in sorted(file["fields"], key=lambda row: row["field_name"]):
            condition = field.get("condition")
            ownership = sorted({item["stage"] for item in field.get("constraint_ownership", [])})
            if condition and condition.get("normalization_status") == "NEEDS_REVIEW":
                primary = "UNRESOLVED_CONDITION"
                reason = "condition normalization_status is NEEDS_REVIEW"
            elif field.get("format_constraints_status") != "EXPLICIT_OFFICIAL" or field.get("range_status") == "NOT_NORMALIZED_REQUIRES_REVIEW":
                primary = "PARTIALLY_EXECUTABLE_G03"
                reason = "G03 format or range metadata is explicitly incomplete"
            else:
                primary = "EXECUTABLE_G03"
                reason = "condition is resolved and G03 type/format/range metadata permits evaluation"
            capabilities = [primary]
            if field.get("empty_value_semantics", {}).get("empty_allowed") == "NOT_SPECIFIED":
                capabilities.append("EMPTY_SEMANTICS_NOT_SPECIFIED")
            if condition and condition.get("normalization_status") == "NEEDS_REVIEW":
                capabilities.append("NEEDS_REVIEW")
            capabilities.extend(f"DEFERRED_{stage.removeprefix('G')}" for stage in ownership if stage in {"G04_IDENTITY_REFERENTIAL", "G05_TEMPORAL", "G06_SEQUENCE", "G07_SPATIAL", "G08_QUALITY"})
            counts[primary] = counts.get(primary, 0) + 1
            fields.append({
                "file_name": file["file_name"], "field_name": field["field_name"],
                "primary_assessment": primary, "capabilities": sorted(set(capabilities)),
                "presence": field["presence"], "condition": condition,
                "type": field["type"], "type_definition_status": next(
                    row["definition"]["status"] for row in contract["type_vocabulary"] if row["token"] == field["type"]),
                "format_constraints_status": field["format_constraints_status"], "range_status": field["range_status"],
                "allowed_values_status": field.get("allowed_values_status"),
                "explicit_enum_value_count": len(field.get("allowed_values") or []),
                "empty_value_semantics": field["empty_value_semantics"],
                "deferred_ownership": [stage for stage in ownership if stage.startswith(("G04", "G05", "G06", "G07", "G08"))],
                "derivation_reason": reason,
                "source_locator": field["source_reference"]["source_locator"],
            })
    inputs = {
        "field_contract_sha256": _sha(CONTRACT), "runtime_sha256": runtime_sha256,
        "catalog_sha256": _sha(CATALOG),
    }
    artifact = {
        "schema_version": "1.0.0", "artifact": "G03_FIELD_CAPABILITY_MAP",
        "status": "CREATED_LOCAL_UNPUBLISHED", "specification_revision": contract["specification_revision"],
        "legal_authority_claimed": False, "inputs": inputs,
        "primary_assessment_counts": dict(sorted(counts.items())), "fields": fields,
    }
    artifact["output_sha256"] = hashlib.sha256((json.dumps(artifact, ensure_ascii=False, indent=2) + "\n").encode()).hexdigest().upper()
    return artifact


def regenerate() -> bytes:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    payload = derive_capability_map(contract, catalog, _sha(RUNTIME))
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


if __name__ == "__main__":
    OUTPUT.write_bytes(regenerate())
