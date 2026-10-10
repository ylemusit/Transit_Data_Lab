"""Opt-in, versioned GTFS agency-condition checks; separate from frozen V1."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from .core import sha256_file
from .ingestion import IngestionError, _decode, _validate_member, inspect_zip


CONTRACT = "TDL_GTFS_CONDITIONAL_RULES_V1"
RULES = {
    "G-PLAN-01": {"version": "1.0.0", "scope": "agency.txt multi-agency identity condition"},
    "G-PLAN-02": {"version": "1.0.0", "scope": "routes.txt agency_id condition and reference"},
}
AUTHORITY = "GTFS_FIXED_FIELD_DEFINITION"
SPEC_PATH = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_2026_04_27.json"


def _read_table(archive: zipfile.ZipFile, info: zipfile.ZipInfo, table: str) -> tuple[list[str], list[dict[str, str]]]:
    raw, header, _encoding, _row_count, _warnings = _validate_member(archive, info, table)
    text, _encoding = _decode(raw)
    reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
    rows: list[dict[str, str]] = []
    for row in reader:
        if row is None:
            continue
        rows.append({str(key): value or "" for key, value in row.items() if key is not None})
    return header, rows


def _finding(source_hash: str, rule_id: str, file_name: str, locator: str,
             status: str, observed: Any, expected: str, reason: str) -> dict[str, Any]:
    identity = "|".join((source_hash, rule_id, file_name, locator, status, str(observed)))
    return {
        "finding_id": hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20],
        "rule_id": rule_id,
        "rule_version": RULES[rule_id]["version"],
        "authority": AUTHORITY,
        "status": status,
        "source_file": file_name,
        "locator": locator,
        "observed": observed,
        "expected": expected,
        "evidence": {"source_sha256": source_hash},
        "reason": reason,
    }


def audit_agency_conditions(input_path: str | Path) -> dict[str, Any]:
    """Evaluate only the two documented agency_id branches on a local GTFS ZIP."""
    path = Path(input_path).resolve(strict=True)
    source_hash = sha256_file(path)
    findings: list[dict[str, Any]] = []
    statuses = {rule_id: "NOT_EVALUABLE" for rule_id in RULES}
    reasons: dict[str, str] = {}

    def add(rule: str, file_name: str, locator: str, status: str,
            observed: Any, expected: str, reason: str) -> None:
        findings.append(_finding(source_hash, rule, file_name, locator, status, observed, expected, reason))

    try:
        selected, _warnings, _unsupported = inspect_zip(path)
        if "agency" not in selected:
            raise IngestionError("agency.txt is absent")
        with zipfile.ZipFile(path) as archive:
            agency_header, agencies = _read_table(archive, selected["agency"], "agency")
            routes_data = None
            if "routes" in selected:
                try:
                    routes_data = _read_table(archive, selected["routes"], "routes")
                except (IngestionError, csv.Error, UnicodeError) as exc:
                    reasons["G-PLAN-02"] = f"routes.txt could not be interpreted: {type(exc).__name__}"

        if not agencies:
            raise IngestionError("agency.txt has no data rows; agency cardinality is unknown")
        agency_ids_available = "agency_id" in agency_header
        agency_ids = [row.get("agency_id", "") for row in agencies] if agency_ids_available else []
        agency_count = len(agencies)
        multi_agency = agency_count > 1

        agency_issues = []
        if multi_agency and not agency_ids_available:
            agency_issues.append(("header:agency_id", "MISSING_HEADER", "agency_id must be present when multiple agencies are supplied"))
        elif multi_agency:
            for index, value in enumerate(agency_ids, start=2):
                if value == "":
                    agency_issues.append((f"row:{index}:agency_id", "EMPTY_VALUE", "each agency row needs an agency_id in a multi-agency feed"))
        if agency_issues:
            statuses["G-PLAN-01"] = "FAIL_TECHNICAL"
            for locator, observed, reason in agency_issues:
                add("G-PLAN-01", "agency.txt", locator, "FAIL_TECHNICAL", observed,
                    "agency_id required when more than one agency is present", reason)
        else:
            statuses["G-PLAN-01"] = "PASS"

        if routes_data is None:
            reasons.setdefault("G-PLAN-02", "routes.txt is absent or could not be interpreted")
            add("G-PLAN-02", "routes.txt", "table", "NOT_EVALUABLE", reasons["G-PLAN-02"],
                "routes and agency identity must be interpretable", reasons["G-PLAN-02"])
        else:
            routes_header, routes = routes_data
            has_route_agency_id = "agency_id" in routes_header
            route_issues: list[tuple[str, str, str]] = []
            unknown_context: list[tuple[str, str]] = []
            if multi_agency and not has_route_agency_id:
                route_issues.append(("header:agency_id", "MISSING_HEADER", "routes agency_id is required when multiple agencies are supplied"))
            elif multi_agency:
                for index, row in enumerate(routes, start=2):
                    value = row.get("agency_id", "")
                    if value == "":
                        route_issues.append((f"row:{index}:agency_id", "EMPTY_VALUE", "every route must identify an agency in a multi-agency feed"))
                    elif not agency_ids_available or any(value_id == "" for value_id in agency_ids):
                        unknown_context.append((f"row:{index}:agency_id", value))
                    elif value not in set(agency_ids):
                        route_issues.append((f"row:{index}:agency_id", f"UNKNOWN_AGENCY_ID:{value}", "route agency_id must reference an agency_id in agency.txt"))
            elif has_route_agency_id:
                known_ids = {value for value in agency_ids if value}
                for index, row in enumerate(routes, start=2):
                    value = row.get("agency_id", "")
                    if value and (not agency_ids_available or not known_ids):
                        unknown_context.append((f"row:{index}:agency_id", value))
                    elif value and value not in known_ids:
                        route_issues.append((f"row:{index}:agency_id", f"UNKNOWN_AGENCY_ID:{value}", "a supplied route agency_id must reference agency.txt"))

            if route_issues:
                statuses["G-PLAN-02"] = "FAIL_TECHNICAL"
                for locator, observed, reason in route_issues:
                    add("G-PLAN-02", "routes.txt", locator, "FAIL_TECHNICAL", observed,
                        "conditional agency_id presence and supplied references must be valid", reason)
            elif unknown_context:
                statuses["G-PLAN-02"] = "NOT_EVALUABLE"
                for locator, value in unknown_context:
                    add("G-PLAN-02", "routes.txt", locator, "NOT_EVALUABLE", value,
                        "agency reference must be resolvable within supplied agency.txt", "agency identity context is incomplete")
            else:
                statuses["G-PLAN-02"] = "PASS"

    except (OSError, zipfile.BadZipFile, IngestionError, csv.Error, UnicodeError) as exc:
        reason = f"agency cardinality could not be established: {type(exc).__name__}"
        reasons.setdefault("G-PLAN-01", reason)
        reasons.setdefault("G-PLAN-02", reason)
        for rule_id in RULES:
            if not any(row["rule_id"] == rule_id for row in findings):
                add(rule_id, "agency.txt" if rule_id == "G-PLAN-01" else "routes.txt", "table",
                    "NOT_EVALUABLE", reason, "required agency context interpretable", reason)

    for rule_id, reason in reasons.items():
        if statuses[rule_id] == "NOT_EVALUABLE" and not any(row["rule_id"] == rule_id for row in findings):
            add(rule_id, "routes.txt" if rule_id == "G-PLAN-02" else "agency.txt", "table",
                "NOT_EVALUABLE", reason, "rule prerequisites available", reason)

    spec_hash = hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest() if SPEC_PATH.is_file() else None
    return {
        "contract": CONTRACT,
        "version": "1.0.0",
        "dataset_identity": {"source_filename": path.name, "source_sha256": source_hash},
        "reference": {"authority": AUTHORITY, "specification": "GTFS Schedule capture 2026-04-27",
                      "specification_sha256": spec_hash},
        "rule_results": [{"rule_id": rule_id, "rule_version": RULES[rule_id]["version"],
                           "scope": RULES[rule_id]["scope"], "status": statuses[rule_id],
                           "finding_count": sum(row["rule_id"] == rule_id for row in findings),
                           "reason": reasons.get(rule_id)} for rule_id in RULES],
        "findings": sorted(findings, key=lambda row: (row["rule_id"], row["source_file"], row["locator"], row["finding_id"])),
        "limitations": ["Opt-in addendum; does not alter GTFS Audit Engine V1 or legacy validation.",
                        "Only the agency_id cardinality/reference branches G-PLAN-01/02 are evaluated."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the opt-in GTFS agency-condition audit addendum V1.")
    parser.add_argument("input", type=Path, help="GTFS Schedule ZIP")
    parser.add_argument("--json", type=Path, required=True, help="Output JSON path")
    args = parser.parse_args()
    result = audit_agency_conditions(args.input)
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
