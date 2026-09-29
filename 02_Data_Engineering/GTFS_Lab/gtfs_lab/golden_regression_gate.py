"""Execute approved Golden cases and prove expectation mismatches are detected."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .golden_contract import is_executable_authority
from .golden_evaluator import evaluate
from .pipeline import run


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_gate(output: Path) -> dict[str, Any]:
    area = Path(__file__).resolve().parents[1]
    golden = area / "golden"
    manifest = json.loads((golden / "corpus_v1.json").read_text(encoding="utf-8"))
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    summaries = []
    for entry in manifest.get("cases", []):
        case_dir = (golden / entry["path"]).resolve()
        case_path = case_dir / "case.json"
        case = json.loads(case_path.read_text(encoding="utf-8"))
        item: dict[str, Any] = {
            "case_id": case.get("case_id"), "case_version": case.get("case_version"),
            "input_sha256": case.get("input", {}).get("sha256"), "case_sha256": _sha(case_path),
            "result_status": "EXECUTION_ERROR", "expectation_results": [],
            "run_id": None, "dataset_id": None, "engine_context": {},
        }
        try:
            if not is_executable_authority(case, case_dir):
                raise ValueError("case is not executable APPROVED authority")
            result = run(case_dir / case["input"]["filename"], output / "runs")
            context = {
                "run_id": result["run_id"], "dataset_id": result["dataset"]["dataset_id"],
                "engine_context": {
                    "gtfs_lab_version": result["gtfs_lab_version"],
                    "validator_version": result["validator_version"],
                    "ruleset_id": "gtfs-lab-v1", "ruleset_version": "1",
                },
            }
            golden_result = evaluate(case, case_dir, result, context)
            item.update({"result_status": golden_result["status"], "expectation_results": golden_result["expectation_results"], "run_id": golden_result["run_id"], "dataset_id": golden_result["dataset_id"], "engine_context": golden_result["engine_context"]})
        except Exception as exc:
            item["error"] = f"{type(exc).__name__}: {exc}"
        summaries.append(item)

    negative = {"count_mismatch": False, "status_mismatch": False}
    for entry in manifest.get("cases", []):
        case_dir = golden / entry["path"]
        case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
        if not is_executable_authority(case, case_dir):
            continue
        for expectation in case["expected"]:
            observed = {"validation": {"rules": []}}
            for expected in case["expected"]:
                rule_id = expected["target"].split("rule_id=", 1)[1].split("].", 1)[0]
                rule = next((r for r in observed["validation"]["rules"] if r["rule_id"] == rule_id), None)
                if rule is None:
                    rule = {"rule_id": rule_id}
                    observed["validation"]["rules"].append(rule)
                field = expected["target"].split("].", 1)[1]
                rule[field] = expected["value"]
            if expectation["type"] == "STATUS":
                rule_id = expectation["target"].split("rule_id=", 1)[1].split("].", 1)[0]
                next(r for r in observed["validation"]["rules"] if r["rule_id"] == rule_id)["status"] = "PASS"
                kind = "status_mismatch"
            elif expectation["type"] == "COUNT":
                rule_id = expectation["target"].split("rule_id=", 1)[1].split("].", 1)[0]
                next(r for r in observed["validation"]["rules"] if r["rule_id"] == rule_id)["finding_count"] = 2
                kind = "count_mismatch"
            else:
                continue
            negative[kind] = negative[kind] or evaluate(case, case_dir, observed, {"run_id": "negative-test", "dataset_id": "synthetic"})["status"] == "FAIL_EXPECTATION"

    checks = [
        {"check": "two_approved_cases_executed", "status": "PASS" if len(summaries) == 2 and all(x["result_status"] == "PASS" for x in summaries) else "FAIL"},
        {"check": "count_expected_1_observed_2_fails", "status": "PASS" if negative["count_mismatch"] else "FAIL"},
        {"check": "status_expected_fail_observed_pass_fails", "status": "PASS" if negative["status_mismatch"] else "FAIL"},
    ]
    result = {"gate": "TDL_GOLDEN_REGRESSION_GATE", "status": "PASS" if all(x["status"] == "PASS" for x in checks) else "FAIL", "output_directory": str(output), "cases": summaries, "negative_regression": {**negative, "mutation_source": "observed payload sintético en memoria"}, "checks": checks, "limitations": ["Los casos son fixtures sintéticos; el gate comprueba el contrato técnico TDL y no constituye validación legal ni completa de GTFS.", "La evidencia de ejecución se escribe fuera de golden/."]}
    (output / "golden_regression_gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("runs/golden_regression"))
    args = parser.parse_args()
    result = run_gate(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
