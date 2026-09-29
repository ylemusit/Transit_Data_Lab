"""Small, explicit evaluator for the M03-B GoldenCase V1 target subset."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, TypedDict

from .golden_contract import is_executable_authority

SUPPORTED_TYPES = {"STATUS", "COUNT", "PRESENCE", "ABSENCE"}


class GoldenEvaluationError(ValueError):
    pass


class ExpectationResult(TypedDict):
    expectation_index: int
    type: str
    target: str
    expected: Any
    observed: Any
    status: Literal["PASS", "FAIL", "NOT_EVALUABLE", "EXECUTION_ERROR"]
    message: str


class GoldenCaseResult(TypedDict):
    case_id: str
    case_version: str
    run_id: str
    dataset_id: str
    engine_context: dict[str, Any]
    status: Literal["PASS", "FAIL_EXPECTATION", "NOT_EVALUABLE", "EXECUTION_ERROR"]
    expectation_results: list[ExpectationResult]
    unexpected_differences: list[dict[str, Any]]


def _resolve(payload: Any, target: str) -> tuple[bool, Any]:
    """Resolve only validation.status and validation.rules[rule_id=ID].{status,finding_count,findings}."""
    if not isinstance(payload, dict) or not isinstance(payload.get("validation"), dict):
        raise GoldenEvaluationError("observed output must contain validation object")
    validation = payload["validation"]
    if target == "validation.status":
        return ("status" in validation, validation.get("status"))
    prefix = "validation.rules[rule_id="
    if not target.startswith(prefix) or "]." not in target:
        raise NotImplementedError(f"unsupported target: {target}")
    rule_id, field = target[len(prefix):].split("].", 1)
    if not rule_id or field not in {"status", "finding_count", "findings"}:
        raise NotImplementedError(f"unsupported target: {target}")
    rules = validation.get("rules")
    if not isinstance(rules, list):
        raise GoldenEvaluationError("validation.rules must be a list")
    matches = [r for r in rules if isinstance(r, dict) and r.get("rule_id") == rule_id]
    if len(matches) != 1:
        return False, None
    rule = matches[0]
    if field == "finding_count" and field not in rule and isinstance(rule.get("findings"), list):
        return True, len(rule["findings"])
    return field in rule, rule.get(field)


def evaluate(case: dict[str, Any], case_dir: Path, observed_output: Any, context: dict[str, Any]) -> GoldenCaseResult:
    if not is_executable_authority(case, case_dir):
        raise GoldenEvaluationError("case is not valid executable APPROVED authority")
    if not isinstance(context, dict) or not all(isinstance(context.get(k), str) and context[k] for k in ("run_id", "dataset_id")):
        raise GoldenEvaluationError("run_id and dataset_id are required")
    results: list[ExpectationResult] = []
    unexpected = []
    for index, exp in enumerate(case["expected"]):
        typ, target, expected = exp["type"], exp["target"], exp["value"]
        if typ not in SUPPORTED_TYPES:
            status, observed, message = "NOT_EVALUABLE", None, f"unsupported expectation type: {typ}"
        else:
            try:
                present, observed = _resolve(observed_output, target)
                if typ == "PRESENCE": matched = present and observed is not None
                elif typ == "ABSENCE": matched = not present or observed is None
                elif typ == "COUNT": matched = type(observed) is int and type(expected) is int and observed == expected
                else: matched = type(observed) is str and type(expected) is str and observed == expected
                status = "PASS" if matched else "FAIL"
                message = "expectation matched" if matched else "observed value differs or target is absent"
                if not matched: unexpected.append({"expectation_index": index, "target": target, "expected": expected, "observed": observed})
            except NotImplementedError as exc:
                status, observed, message = "NOT_EVALUABLE", None, str(exc)
            except GoldenEvaluationError as exc:
                status, observed, message = "EXECUTION_ERROR", None, str(exc)
        results.append({"expectation_index": index, "type": typ, "target": target, "expected": expected, "observed": observed, "status": status, "message": message})
    if any(x["status"] == "EXECUTION_ERROR" for x in results): overall = "EXECUTION_ERROR"
    elif any(x["status"] == "FAIL" for x in results): overall = "FAIL_EXPECTATION"
    elif any(x["status"] == "NOT_EVALUABLE" for x in results): overall = "NOT_EVALUABLE"
    else: overall = "PASS"
    return {"case_id": case["case_id"], "case_version": case["case_version"], "run_id": context["run_id"], "dataset_id": context["dataset_id"], "engine_context": context.get("engine_context", {}), "status": overall, "expectation_results": results, "unexpected_differences": unexpected}
