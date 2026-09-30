"""Typed G02 rule-registry identities shared by GTFS phase evaluators."""
from .rule_registry import (
    ApplicabilityExpression, ApplicabilityOperator, RequirementKind, RuleAuthority,
    RuleCategory, RuleDefinition, RuleRegistry, Severity, SpecificationReference,
)

REVISION = "2026-04-27"

def build_phase_registry(specs, evaluator, phase):
    definitions=[]
    for spec in specs:
        rule_id, category, coverage, files = spec[:4]
        authority, severity, requirement = spec[4:] if len(spec)>4 else (RuleAuthority.GTFS_REQUIRED,Severity.ERROR,RequirementKind.REQUIRED)
        definitions.append(RuleDefinition(
            rule_id=rule_id, semantic_version="1.0.0", category=RuleCategory(category),
            authority=RuleAuthority(authority), severity=Severity(severity),
            requirement=RequirementKind(requirement), applicable_files=tuple(files),
            specification_reference=SpecificationReference("GTFS Schedule Reference", REVISION, coverage),
            applicability=ApplicabilityExpression(ApplicabilityOperator.SIGNAL_PRESENT,signal="archive.inspection_ready"),
            evaluator_identity=f"gtfs_lab.{phase}.{rule_id.lower()}/1", evaluator=evaluator,
            declared_coverage=(coverage,)))
    return RuleRegistry(definitions).freeze()
