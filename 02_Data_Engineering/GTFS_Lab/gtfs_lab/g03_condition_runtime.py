"""Row-level G03 condition evaluation using the G02 three-valued evaluator."""
from __future__ import annotations

from typing import Any, Mapping

from .rule_registry import (
    ApplicabilityExpression,
    ApplicabilityTruth,
    SpecificationCondition,
    SpecificationConditionOperator,
    compile_specification_condition,
    evaluate_applicability,
)


def _json_value(value: Any) -> Any:
    """Return trace values in the same shape after JSON serialization."""
    if isinstance(value, Mapping):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _compile(expression: Mapping[str, Any]) -> ApplicabilityExpression:
    op = SpecificationConditionOperator(expression["op"])
    if op in {SpecificationConditionOperator.ALL, SpecificationConditionOperator.ANY}:
        return compile_specification_condition(SpecificationCondition(
            op, conditions=tuple(_as_specification_condition(child) for child in expression["conditions"])
        ))
    if op == SpecificationConditionOperator.NOT:
        return compile_specification_condition(SpecificationCondition(
            op, conditions=(_as_specification_condition(expression["condition"]),)
        ))
    return compile_specification_condition(_as_specification_condition(expression))


def _as_specification_condition(expression: Mapping[str, Any]) -> SpecificationCondition:
    """Build the typed G02 tree; values remain strings as read from CSV."""
    op = SpecificationConditionOperator(expression["op"])
    if op in {SpecificationConditionOperator.ALL, SpecificationConditionOperator.ANY}:
        return SpecificationCondition(op, conditions=tuple(_as_specification_condition(x) for x in expression["conditions"]))
    if op == SpecificationConditionOperator.NOT:
        return SpecificationCondition(op, conditions=(_as_specification_condition(expression["condition"]),))
    subject = expression.get("field") or expression.get("subject")
    if not subject:
        raise ValueError(f"condition {op.value} requires a field subject")
    if op == SpecificationConditionOperator.FIELD_PRESENT:
        return SpecificationCondition(op, subject=f"field:{subject}")
    if op == SpecificationConditionOperator.FIELD_VALUE_IN:
        return SpecificationCondition(op, subject=f"field:{subject}", values=tuple(expression["values"]))
    if op == SpecificationConditionOperator.FIELD_VALUE_EQUALS:
        return SpecificationCondition(op, subject=f"field:{subject}", value=expression["value"])
    raise ValueError(f"condition operator is not row-evaluable in G03: {op.value}")


def evaluate_presence_policy(
    policy: Mapping[str, Any], row: Mapping[str, str], header: set[str]
) -> dict[str, Any]:
    """Resolve ordered conditional presence rules to TRUE/FALSE/UNKNOWN and an effect.

    Missing headers produce UNKNOWN. Empty cells remain the exact empty string; the
    specification expression, rather than a global empty-value assumption, decides
    whether that value is meaningful.
    """
    signals: dict[str, Any] = {}
    for name in set(header) | set(row):
        signals[f"field:{name}"] = row.get(name) if name in header else None
    trace: list[dict[str, Any]] = []
    unknown = False
    # A later FALSE is unrelated evidence and cannot erase an earlier UNKNOWN.
    # TRUE is decisive for this ordered alternative policy; its trace retains all
    # prior UNKNOWN evaluations so the resolution is auditable.
    for rule in policy.get("rules", []):
        result = evaluate_applicability(_compile(rule["when"]), signals)
        trace.append({"effect": rule["effect"], "truth": result.truth.value, "trace": _json_value(result.trace)})
        if result.truth == ApplicabilityTruth.TRUE and not unknown:
            return {"truth": "TRUE", "effect": rule["effect"], "trace": trace}
        if result.truth == ApplicabilityTruth.TRUE:
            # An earlier unresolved rule may take precedence. A later matching
            # rule is not evidence that resolves that earlier condition.
            continue
        if result.truth == ApplicabilityTruth.UNKNOWN:
            unknown = True
    if unknown or policy.get("default") == "UNKNOWN":
        return {"truth": "UNKNOWN", "effect": None, "trace": trace}
    return {"truth": "FALSE", "effect": policy.get("default", "OPTIONAL"), "trace": trace}
