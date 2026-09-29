from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path

from .golden_contract import GoldenCaseError, is_executable_authority
from .golden_evaluator import GoldenEvaluationError, evaluate


def run_gate() -> dict:
    checks = []
    def add(name: str, ok: bool) -> None: checks.append({"check": name, "status": "PASS" if ok else "FAIL"})
    with tempfile.TemporaryDirectory(prefix="tdl-golden-evaluator-") as tmp:
        base = Path(tmp); (base / "input.zip").write_bytes(b"synthetic evaluator contract input")
        case = {"case_id":"evaluator-synthetic", "case_version":"1.0.0", "contract_version":"1.0.0", "status":"APPROVED", "purpose":"Temporary evaluator gate only", "created_at_utc":"2026-09-29T00:00:00Z", "input":{"filename":"input.zip","sha256":hashlib.sha256((base / "input.zip").read_bytes()).hexdigest(),"format":"GTFS_STATIC_ZIP","provenance":"SYNTHETIC"}, "scope":["evaluator behavior"], "expected":[], "excluded_expectations":[], "authority":{"basis":"SYNTHETIC_INVARIANT"}, "review":{"reviewed_by":"synthetic-gate-only","reviewed_at_utc":"2026-09-29T00:00:00Z","review_basis":"temporary gate fixture; not corpus approval"}, "engine_context":{"gtfs_lab_version":"gate","validator_version":"gate","ruleset_id":"gate","ruleset_version":"1"}}
        observed = {"validation":{"status":"FAIL_TECHNICAL","rules":[{"rule_id":"R","status":"FAIL_TECHNICAL","finding_count":1,"findings":[{"rule_id":"R"}]}]}}
        context = {"run_id":"synthetic-run","dataset_id":"synthetic-dataset"}
        def one(typ, target, value):
            c = copy.deepcopy(case); c["expected"] = [{"type":typ,"target":target,"value":value,"authority":"SYNTHETIC_INVARIANT"}]
            return evaluate(c, base, observed, context)
        passing_result = one("STATUS","validation.rules[rule_id=R].status","FAIL_TECHNICAL")
        add("status_pass", passing_result["status"] == "PASS")
        add("golden_case_result_contract", set(passing_result) == {"case_id", "case_version", "run_id", "dataset_id", "engine_context", "status", "expectation_results", "unexpected_differences"} and set(passing_result["expectation_results"][0]) == {"expectation_index", "type", "target", "expected", "observed", "status", "message"})
        add("status_fail", one("STATUS","validation.status","PASS")["status"] == "FAIL_EXPECTATION")
        add("count_pass", one("COUNT","validation.rules[rule_id=R].finding_count",1)["status"] == "PASS")
        add("count_fail_and_no_string_coercion", one("COUNT","validation.rules[rule_id=R].finding_count","1")["status"] == "FAIL_EXPECTATION")
        add("unsupported_target_not_evaluable", one("STATUS","validation.rules[*].status","PASS")["status"] == "NOT_EVALUABLE")
        case["expected"] = [{"type":"STATUS","target":"validation.status","value":"PASS","authority":"SYNTHETIC_INVARIANT"}]
        malformed = evaluate(case, base, {}, context)
        add("malformed_result_execution_error", malformed["status"] == "EXECUTION_ERROR" and all(x["status"] == "EXECUTION_ERROR" for x in malformed["expectation_results"]))
        draft = copy.deepcopy(case); draft["status"] = "UNDER_REVIEW"; draft["review"] = {}
        try: evaluate(draft, base, observed, context); rejected = False
        except (GoldenCaseError, GoldenEvaluationError): rejected = True
        add("non_approved_rejected_as_authority", rejected)
        invalid = copy.deepcopy(case); invalid["contract_version"] = "9"
        try: is_executable_authority(invalid, base); rejected_invalid = False
        except (GoldenCaseError, TypeError): rejected_invalid = True
        add("invalid_approved_contract_rejected", rejected_invalid)
        case["expected"] = [{"type":"PRESENCE","target":"validation.rules[rule_id=R].findings","value":True,"authority":"SYNTHETIC_INVARIANT"}]
        add("presence_pass", evaluate(case, base, observed, context)["status"] == "PASS")
        case["expected"] = [{"type":"ABSENCE","target":"validation.rules[rule_id=missing].findings","value":True,"authority":"SYNTHETIC_INVARIANT"}]
        add("absence_pass", evaluate(case, base, observed, context)["status"] == "PASS")
    return {"gate":"TDL_GOLDEN_EVALUATOR_GATE", "status":"PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL", "check_count":len(checks), "checks":checks, "approved_corpus_cases":2, "corpus_cases_executed_by_this_gate":0, "note":"El gate prueba evaluator con casos sintéticos temporales; TDL_GOLDEN_REGRESSION_GATE ejecuta el corpus aprobado."}


def main() -> int:
    result=run_gate(); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
