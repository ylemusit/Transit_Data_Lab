"""Typed, immutable-at-execution rule contracts for GTFS Audit Engine V1.

G02 architecture only: this registry is intentionally not connected to the
legacy productive validator.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re
from typing import Any, Callable, Iterable, Mapping


_RULE_ID = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
_SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")


class RuleCategory(StrEnum):
    STRUCTURE = "STRUCTURE"
    SCHEMA = "SCHEMA"
    TYPE_FORMAT = "TYPE_FORMAT"
    IDENTITY = "IDENTITY"
    REFERENTIAL = "REFERENTIAL"
    TEMPORAL = "TEMPORAL"
    SEQUENCE = "SEQUENCE"
    SPATIAL = "SPATIAL"
    DATA_CONSISTENCY = "DATA_CONSISTENCY"
    QUALITY = "QUALITY"


class RuleAuthority(StrEnum):
    GTFS_REQUIRED = "GTFS_REQUIRED"
    GTFS_CONDITIONAL = "GTFS_CONDITIONAL"
    GTFS_RECOMMENDED = "GTFS_RECOMMENDED"
    TDL_QUALITY = "TDL_QUALITY"


class RequirementKind(StrEnum):
    REQUIRED = "REQUIRED"
    CONDITIONALLY_REQUIRED = "CONDITIONALLY_REQUIRED"
    OPTIONAL = "OPTIONAL"
    RECOMMENDED = "RECOMMENDED"
    PROHIBITED_WHEN = "PROHIBITED_WHEN"


class Severity(StrEnum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class RuleStatus(StrEnum):
    PASS = "PASS"
    FAIL_TECHNICAL = "FAIL_TECHNICAL"
    NOT_EVALUABLE = "NOT_EVALUABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INSPECTION_ERROR = "INSPECTION_ERROR"


class ApplicabilityTruth(StrEnum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


class ApplicabilityOperator(StrEnum):
    SIGNAL_PRESENT = "SIGNAL_PRESENT"
    SIGNAL_EQUALS = "SIGNAL_EQUALS"
    ALL = "ALL"
    ANY = "ANY"
    NOT = "NOT"


class SpecificationConditionOperator(StrEnum):
    """G01 condition vocabulary; each leaf maps to a typed runtime signal."""
    FILE_PRESENT = "FILE_PRESENT"
    FILE_ABSENT = "FILE_ABSENT"
    FIELD_PRESENT = "FIELD_PRESENT"
    FIELD_VALUE_EQUALS = "FIELD_VALUE_EQUALS"
    FIELD_VALUE_IN = "FIELD_VALUE_IN"
    ENTITY_EXISTS = "ENTITY_EXISTS"
    PARENT_ENTITY_EXISTS = "PARENT_ENTITY_EXISTS"
    RELATED_FILE_PRESENT = "RELATED_FILE_PRESENT"
    ONE_OF_FILES_PRESENT = "ONE_OF_FILES_PRESENT"
    DEPENDENT_FIELDS = "DEPENDENT_FIELDS"
    ALL = "ALL"
    ANY = "ANY"
    NOT = "NOT"
    ALL_SERVICE_DATES_DEFINED = "ALL_SERVICE_DATES_DEFINED"


@dataclass(frozen=True)
class SpecificationCondition:
    """A G01 condition compiled to the generalized runtime signal model."""
    operator: SpecificationConditionOperator | str
    subject: str | None = None
    value: Any = None
    values: tuple[Any, ...] = ()
    conditions: tuple["SpecificationCondition", ...] = ()

    def __post_init__(self) -> None:
        try:
            operator = SpecificationConditionOperator(self.operator)
        except ValueError as exc:
            raise ValueError(f"unsupported G01 condition operator: {self.operator!r}") from exc
        object.__setattr__(self, "operator", operator)
        if operator in {SpecificationConditionOperator.ALL, SpecificationConditionOperator.ANY}:
            if not self.conditions or self.subject is not None:
                raise ValueError(f"{operator.value} requires child conditions")
        elif operator == SpecificationConditionOperator.NOT:
            if len(self.conditions) != 1 or self.subject is not None:
                raise ValueError("NOT requires exactly one child condition")
        elif operator == SpecificationConditionOperator.FIELD_VALUE_IN:
            if not self.subject or not self.values or self.conditions:
                raise ValueError("FIELD_VALUE_IN requires a subject and values")
        elif not self.subject or self.conditions:
            raise ValueError(f"{operator.value} requires a subject")


def compile_specification_condition(condition: SpecificationCondition) -> ApplicabilityExpression:
    """Compile G01 conditions losslessly to signal predicates and boolean operators.

    The caller constructs normalized signals (e.g. file presence as bool,
    field value as a scalar, membership as bool) from its feed inspection.
    """
    op = SpecificationConditionOperator(condition.operator)
    if op in {SpecificationConditionOperator.ALL, SpecificationConditionOperator.ANY, SpecificationConditionOperator.NOT}:
        runtime = {SpecificationConditionOperator.ALL: ApplicabilityOperator.ALL,
                   SpecificationConditionOperator.ANY: ApplicabilityOperator.ANY,
                   SpecificationConditionOperator.NOT: ApplicabilityOperator.NOT}[op]
        return ApplicabilityExpression(runtime, conditions=tuple(compile_specification_condition(c) for c in condition.conditions))
    if op == SpecificationConditionOperator.FILE_ABSENT:
        return ApplicabilityExpression(ApplicabilityOperator.NOT, conditions=(ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT, signal=condition.subject),))
    if op == SpecificationConditionOperator.FIELD_VALUE_IN:
        return ApplicabilityExpression(ApplicabilityOperator.SIGNAL_EQUALS, signal=condition.subject, expected={"in": condition.values})
    if op in {SpecificationConditionOperator.FIELD_VALUE_EQUALS, SpecificationConditionOperator.ALL_SERVICE_DATES_DEFINED}:
        expected = condition.value if op == SpecificationConditionOperator.FIELD_VALUE_EQUALS else True
        return ApplicabilityExpression(ApplicabilityOperator.SIGNAL_EQUALS, signal=condition.subject, expected=expected)
    return ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT, signal=condition.subject)


class CoverageState(StrEnum):
    FEATURE_NOT_PRESENT = "FEATURE_NOT_PRESENT"
    FEATURE_PRESENT_FULLY_AUDITED = "FEATURE_PRESENT_FULLY_AUDITED"
    FEATURE_PRESENT_PARTIALLY_AUDITED = "FEATURE_PRESENT_PARTIALLY_AUDITED"
    FEATURE_PRESENT_DEFERRED = "FEATURE_PRESENT_DEFERRED"


@dataclass(frozen=True)
class SpecificationReference:
    specification: str
    revision: str
    section: str

    def __post_init__(self) -> None:
        if not all(isinstance(v, str) and v.strip() for v in (self.specification, self.revision, self.section)):
            raise ValueError("specification reference fields must be non-empty strings")


@dataclass(frozen=True)
class ApplicabilityExpression:
    operator: ApplicabilityOperator | str
    signal: str | None = None
    expected: Any = None
    conditions: tuple["ApplicabilityExpression", ...] = ()

    def __post_init__(self) -> None:
        try:
            operator = ApplicabilityOperator(self.operator)
        except ValueError as exc:
            raise ValueError(f"unsupported applicability operator: {self.operator!r}") from exc
        object.__setattr__(self, "operator", operator)
        if operator in {ApplicabilityOperator.SIGNAL_PRESENT, ApplicabilityOperator.SIGNAL_EQUALS}:
            if not isinstance(self.signal, str) or not self.signal.strip() or self.conditions:
                raise ValueError(f"{operator.value} requires a signal and no child conditions")
        elif operator == ApplicabilityOperator.NOT:
            if len(self.conditions) != 1 or self.signal is not None:
                raise ValueError("NOT requires exactly one child condition")
        elif not self.conditions or self.signal is not None:
            raise ValueError(f"{operator.value} requires one or more child conditions")
        if any(not isinstance(item, ApplicabilityExpression) for item in self.conditions):
            raise ValueError("applicability conditions must be expressions")


@dataclass(frozen=True)
class ApplicabilityResult:
    truth: ApplicabilityTruth
    status: RuleStatus | None
    trace: tuple[Mapping[str, Any], ...]


def evaluate_applicability(expression: ApplicabilityExpression, signals: Mapping[str, Any]) -> ApplicabilityResult:
    trace: list[dict[str, Any]] = []

    def evaluate(node: ApplicabilityExpression) -> ApplicabilityTruth:
        op = ApplicabilityOperator(node.operator)
        if op in {ApplicabilityOperator.SIGNAL_PRESENT, ApplicabilityOperator.SIGNAL_EQUALS}:
            present = node.signal in signals
            observed = signals.get(node.signal)
            if not present or observed is None:
                truth = ApplicabilityTruth.UNKNOWN
            elif op == ApplicabilityOperator.SIGNAL_PRESENT:
                truth = ApplicabilityTruth.TRUE if bool(observed) else ApplicabilityTruth.FALSE
            else:
                if isinstance(node.expected, Mapping) and set(node.expected) == {"in"}:
                    truth = ApplicabilityTruth.TRUE if observed in node.expected["in"] else ApplicabilityTruth.FALSE
                else:
                    truth = ApplicabilityTruth.TRUE if observed == node.expected else ApplicabilityTruth.FALSE
            trace.append({"operator": op.value, "condition": node.signal, "observed": observed if present else "MISSING", "expected": node.expected if op == ApplicabilityOperator.SIGNAL_EQUALS else None, "truth": truth.value})
            return truth
        children = [evaluate(child) for child in node.conditions]
        if op == ApplicabilityOperator.ALL:
            truth = ApplicabilityTruth.FALSE if ApplicabilityTruth.FALSE in children else ApplicabilityTruth.UNKNOWN if ApplicabilityTruth.UNKNOWN in children else ApplicabilityTruth.TRUE
        elif op == ApplicabilityOperator.ANY:
            truth = ApplicabilityTruth.TRUE if ApplicabilityTruth.TRUE in children else ApplicabilityTruth.UNKNOWN if ApplicabilityTruth.UNKNOWN in children else ApplicabilityTruth.FALSE
        else:
            value = children[0]
            truth = {ApplicabilityTruth.TRUE: ApplicabilityTruth.FALSE, ApplicabilityTruth.FALSE: ApplicabilityTruth.TRUE, ApplicabilityTruth.UNKNOWN: ApplicabilityTruth.UNKNOWN}[value]
        trace.append({"operator": op.value, "truth": truth.value, "children": [item.value for item in children]})
        return truth

    truth = evaluate(expression)
    status = {ApplicabilityTruth.TRUE: None, ApplicabilityTruth.FALSE: RuleStatus.NOT_APPLICABLE, ApplicabilityTruth.UNKNOWN: RuleStatus.NOT_EVALUABLE}[truth]
    return ApplicabilityResult(truth, status, tuple(trace))


RuleEvaluator = Callable[[Any], Any]


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    semantic_version: str
    category: RuleCategory | str
    authority: RuleAuthority | str
    severity: Severity | str
    requirement: RequirementKind | str
    applicable_files: tuple[str, ...]
    specification_reference: SpecificationReference
    applicability: ApplicabilityExpression
    evaluator_identity: str
    evaluator: RuleEvaluator
    declared_coverage: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str) or not _RULE_ID.fullmatch(self.rule_id):
            raise ValueError(f"invalid or empty rule ID: {self.rule_id!r}")
        if not isinstance(self.semantic_version, str) or not _SEMVER.fullmatch(self.semantic_version):
            raise ValueError(f"invalid semantic version: {self.semantic_version!r}")
        for field_name, enum_type in (("category", RuleCategory), ("authority", RuleAuthority), ("severity", Severity), ("requirement", RequirementKind)):
            try:
                object.__setattr__(self, field_name, enum_type(getattr(self, field_name)))
            except ValueError as exc:
                raise ValueError(f"unsupported {field_name}: {getattr(self, field_name)!r}") from exc
        if not isinstance(self.specification_reference, SpecificationReference):
            raise ValueError("specification_reference must be a SpecificationReference")
        if not isinstance(self.applicability, ApplicabilityExpression):
            raise ValueError("applicability must be an ApplicabilityExpression")
        object.__setattr__(self, "applicable_files", tuple(self.applicable_files))
        object.__setattr__(self, "declared_coverage", tuple(self.declared_coverage))
        if not callable(self.evaluator) or not isinstance(self.evaluator_identity, str) or not self.evaluator_identity.strip():
            raise ValueError("evaluator and evaluator_identity are required")
        if not self.applicable_files or any(not isinstance(value, str) or not value.strip() for value in self.applicable_files):
            raise ValueError("applicable_files must contain non-empty names")
        if not self.declared_coverage or any(not isinstance(value, str) or not value.strip() for value in self.declared_coverage):
            raise ValueError("declared_coverage must contain non-empty feature names")


class RuleRegistry:
    """Mutable during composition; ``freeze`` seals the exact execution set."""

    def __init__(self, rules: Iterable[RuleDefinition] = ()) -> None:
        self._rules: dict[str, RuleDefinition] = {}
        self._frozen = False
        for rule in rules:
            self.register(rule)

    def register(self, rule: RuleDefinition) -> None:
        if self._frozen:
            raise RuntimeError("registry is frozen; register() is forbidden")
        if not isinstance(rule, RuleDefinition):
            raise TypeError("registry accepts RuleDefinition instances")
        if rule.rule_id in self._rules:
            raise ValueError(f"duplicate rule ID: {rule.rule_id}")
        self._rules[rule.rule_id] = rule

    def freeze(self) -> "RuleRegistry":
        self._rules = dict(sorted(self._rules.items()))
        self._frozen = True
        return self

    @property
    def frozen(self) -> bool:
        return self._frozen

    def __iter__(self):
        return iter(tuple(self._rules[key] for key in sorted(self._rules)))

    def __len__(self) -> int:
        return len(self._rules)

    def __getitem__(self, rule_id: str) -> RuleDefinition:
        return self._rules[rule_id]

    def identity_map(self) -> dict[str, dict[str, str]]:
        if not self._frozen:
            raise RuntimeError("freeze registry before publishing execution identity")
        return {"rule_versions": {rule.rule_id: rule.semantic_version for rule in self}}

    def execution_disposition(self, rule: RuleDefinition, signals: Mapping[str, Any]) -> tuple[str | RuleStatus, ApplicabilityResult]:
        if not self._frozen:
            raise RuntimeError("freeze registry before execution")
        result = evaluate_applicability(rule.applicability, signals)
        if result.truth == ApplicabilityTruth.FALSE or result.truth == ApplicabilityTruth.UNKNOWN:
            return result.status, result
        return "EVALUATE", result


@dataclass(frozen=True)
class RuleCoverage:
    feature: str
    presence: str
    audit_support: str
    state: CoverageState | str

    def __post_init__(self) -> None:
        if not isinstance(self.feature, str) or not self.feature.strip():
            raise ValueError("coverage feature must be non-empty")
        try:
            object.__setattr__(self, "state", CoverageState(self.state))
        except ValueError as exc:
            raise ValueError(f"unsupported coverage state: {self.state!r}") from exc
        if self.presence not in {"PRESENT", "ABSENT", "UNKNOWN"}:
            raise ValueError("presence must be PRESENT, ABSENT, or UNKNOWN")
        if self.audit_support not in {"FULL", "PARTIAL", "DEFERRED", "NONE"}:
            raise ValueError("audit_support must be FULL, PARTIAL, DEFERRED, or NONE")
        expected = {
            CoverageState.FEATURE_NOT_PRESENT: ("ABSENT", "NONE"),
            CoverageState.FEATURE_PRESENT_FULLY_AUDITED: ("PRESENT", "FULL"),
            CoverageState.FEATURE_PRESENT_PARTIALLY_AUDITED: ("PRESENT", "PARTIAL"),
            CoverageState.FEATURE_PRESENT_DEFERRED: ("PRESENT", "DEFERRED"),
        }[self.state]
        if (self.presence, self.audit_support) != expected:
            raise ValueError("coverage state conflicts with feature presence or audit support")


def legacy_status_to_engine(status: str) -> RuleStatus:
    """Explicit adapter; legacy WARNING is preserved as a legacy-only status."""
    if status == "WARNING":
        raise ValueError("legacy WARNING has no implicit engine-native equivalent")
    try:
        return RuleStatus(status)
    except ValueError as exc:
        raise ValueError(f"invalid engine-native RuleResult status: {status!r}") from exc
