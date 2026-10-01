"""Isolated one-dataset worker for the G10 DEVELOPMENT corpus gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from .pipeline import run


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
        "engine_report_sha256": hashlib.sha256(engine_report.read_bytes()).hexdigest(),
    }
    args.result.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
