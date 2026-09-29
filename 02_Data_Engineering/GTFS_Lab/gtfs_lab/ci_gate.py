"""Machine-readable CI gate; the historical execution CLI remains unchanged.

Exit 0: policy satisfied. Exit 2: technical, inspection or resource failure.
Exit 3: invalid invocation/configuration. Findings policy is explicit.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ingestion import IngestionError
from .pipeline import record_ingestion_error, run


def classify(summary: dict, *, findings_policy: str = "fail") -> dict:
    if findings_policy not in ("fail", "allow"):
        return {"status": "CONFIGURATION_ERROR", "exit_code": 3}
    if not isinstance(summary, dict):
        return {"status": "CONFIGURATION_ERROR", "exit_code": 3}
    required = ("ingestion", "integrity", "validation", "analysis", "gis", "database", "compliance_v1")
    if any(key not in summary for key in required):
        return {"status": "CONFIGURATION_ERROR", "exit_code": 3}
    values = set(summary.values())
    if "INGESTION_ERROR" in values or "INSPECTION_ERROR" in values:
        return {"status": "INSPECTION_ERROR", "exit_code": 2}
    if "FAIL_TECHNICAL" in values or "FAIL" in values:
        return {"status": "FAIL_TECHNICAL", "exit_code": 2}
    if "RESOURCE_ERROR" in values:
        return {"status": "RESOURCE_ERROR", "exit_code": 2}
    if "CONFIGURATION_ERROR" in values:
        return {"status": "CONFIGURATION_ERROR", "exit_code": 3}
    if "NOT_EVALUABLE" in values or "SKIPPED_BY_DEPENDENCY" in values:
        return {"status": "NOT_EVALUABLE", "exit_code": 2}
    if any(summary[key] != "PASS" for key in required):
        return {"status": "INSPECTION_ERROR", "exit_code": 2}
    findings = summary.get("findings", 0)
    if type(findings) is not int or findings < 0:
        return {"status": "CONFIGURATION_ERROR", "exit_code": 3}
    if findings:
        return {"status": "AUDIT_WITH_FINDINGS", "exit_code": 2 if findings_policy == "fail" else 0}
    return {"status": "AUDIT_PASS", "exit_code": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--findings-policy", choices=("fail", "allow"), default="fail")
    args = parser.parse_args()
    try:
        try:
            result = run(args.zip, args.output)
        except IngestionError as exc:
            result = record_ingestion_error(args.zip, args.output, exc)
        gate = classify(result["summary"], findings_policy=args.findings_policy)
        gate.update(run_id=result["run_id"], summary=result["summary"], findings_policy=args.findings_policy)
    except (OSError, ValueError) as exc:
        gate = {"status": "CONFIGURATION_ERROR", "exit_code": 3, "error": str(exc)}
    except Exception as exc:
        gate = {"status": "INSPECTION_ERROR", "exit_code": 2, "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(gate, ensure_ascii=False))
    return gate["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
