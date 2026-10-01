"""Isolated one-dataset worker for the G10 DEVELOPMENT corpus gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from .pipeline import run


def _bounded_reason_evidence(component: dict, *, sample_limit: int = 5) -> dict:
    """Keep exact grouped reason counts with only a small row sample."""
    rows = component.get("not_evaluable", [])
    grouped: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        grouped[(str(row.get("file", "UNKNOWN_FILE")),
                 str(row.get("field", "")),
                 str(row.get("reason", "UNSPECIFIED")))] += 1
    return {
        "status": component.get("status", "NOT_EVALUABLE"),
        "not_evaluable_count": len(rows),
        "reason_counts": [
            {"file": file_name, "field": field_name or None, "reason_code": reason, "count": count}
            for (file_name, field_name, reason), count in sorted(grouped.items())
        ],
        "sample": [
            {key: value for key, value in row.items() if key not in {"observed", "value"}}
            for row in rows[:sample_limit]
        ],
        "sample_limit": sample_limit,
    }


def _bounded_findings_evidence(component: dict, *, sample_limit: int = 5) -> dict:
    """Summarize findings without retaining row-level payloads."""
    rows = component.get("findings", [])
    grouped: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        grouped[(str(row.get("file", row.get("source_file", "UNKNOWN_FILE"))),
                 str(row.get("field", "")),
                 str(row.get("reason_code", row.get("code", row.get("rule_id", "UNSPECIFIED")))))] += 1
    inspected = component.get("files_inspected", component.get("inspected", []))
    return {
        "status": component.get("status", "NOT_EVALUABLE"),
        "finding_count": len(rows),
        "reason_counts": [
            {"file": file_name, "field": field_name or None, "reason_code": reason, "count": count}
            for (file_name, field_name, reason), count in sorted(grouped.items())
        ],
        "sample": [
            {key: value for key, value in row.items() if key not in {"observed", "value", "observed_identifier_or_reference"}}
            for row in rows[:sample_limit]
        ],
        "sample_limit": sample_limit,
        "file_statuses": [
            {"file": row.get("file"), "status": row.get("status"),
             "row_count": row.get("data_rows", row.get("row_count")),
             "finding_count": row.get("finding_count")}
            for row in inspected
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    engine_report = args.output / result["run_id"] / "engine_report.json"
    record = {
        "run_id": result["run_id"],
        "ingestion_status": result.get("ingestion", {}).get("status"),
        "legacy_validation_status": result.get("validation", {}).get("status"),
        "legacy_finding_count": result.get("validation", {}).get("finding_count", 0),
        "stages": {
            stage: {
                "status": result.get(stage, {}).get("status", "NOT_EVALUABLE"),
                "rule_status_counts": dict(sorted(Counter(
                    rule.get("status", "NOT_EVALUABLE")
                    for rule in result.get(stage, {}).get("rules", [])
                ).items())),
                "not_evaluable_rule_count": sum(
                    rule.get("status") == "NOT_EVALUABLE"
                    for rule in result.get(stage, {}).get("rules", [])
                ),
                "inspection_error_rule_count": sum(
                    rule.get("status") == "INSPECTION_ERROR"
                    for rule in result.get(stage, {}).get("rules", [])
                ),
                "finding_count": sum(
                    len(rule.get("findings", [])) for rule in result.get(stage, {}).get("rules", [])
                ),
                "finding_counts_by_rule": {
                    rule.get("rule_id", "UNKNOWN_RULE"): len(rule.get("findings", []))
                    for rule in result.get(stage, {}).get("rules", [])
                },
                "rules": [{
                    "rule_id": rule.get("rule_id"),
                    "status": rule.get("status"),
                    "coverage": rule.get("coverage"),
                    "recommendation_met": rule.get("recommendation_met"),
                } for rule in result.get(stage, {}).get("rules", [])],
                "finding_samples": [
                    {key: value for key, value in finding.items()
                     if key not in {"observed", "observed_identifier_or_reference"}}
                    for rule in result.get(stage, {}).get("rules", [])
                    for finding in rule.get("findings", [])[:5]
                ][:20],
                "finding_sample_limit": 20,
            }
            for stage in ("g03", "g04", "g05", "g06", "g07", "g08")
        },
        "g03_component_statuses": {
            component: result.get("g03", {}).get(component, {}).get("status", "NOT_EVALUABLE")
            for component in ("file_catalog", "csv_structure", "header_schema", "file_presence", "field_types")
        },
        "g03_checked_type_values": result.get("g03", {}).get("field_types", {}).get("checked_values", 0),
        "g03_conditional_rows_total": result.get("g03", {}).get("header_schema", {}).get("conditional_rows_total", 0),
        "g03_conditional_rows_sampled": len(result.get("g03", {}).get("header_schema", {}).get("conditional_rows", [])),
        "g03_precondition_evidence": {
            "csv_structure": _bounded_findings_evidence(result.get("g03", {}).get("csv_structure", {})),
            "field_type_findings": _bounded_findings_evidence(result.get("g03", {}).get("field_types", {})),
            **{
                component: _bounded_reason_evidence(result.get("g03", {}).get(component, {}))
                for component in ("header_schema", "field_types")
            },
        },
        "engine_report_sha256": hashlib.sha256(engine_report.read_bytes()).hexdigest(),
    }
    args.result.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
