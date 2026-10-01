"""Optional, non-normative GTFS recommended-field checks (G08)."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .rule_registry import (
    ApplicabilityExpression,
    ApplicabilityOperator,
    RequirementKind,
    RuleAuthority,
    RuleCategory,
    RuleDefinition,
    RuleRegistry,
    Severity,
    SpecificationReference,
)

REVISION = "2026-04-27"
REFERENCE = "https://gtfs.org/documentation/schedule/reference/#feed_infotxt"
RULES = {
    "GTFS-G08-FEED-START-DATE-DECLARED": "feed_start_date",
    "GTFS-G08-FEED-END-DATE-DECLARED": "feed_end_date",
    "GTFS-G08-FEED-VERSION-DECLARED": "feed_version",
}
_APPLICABILITY = ApplicabilityExpression(
    ApplicabilityOperator.SIGNAL_PRESENT, signal="archive.inspection_ready"
)


def _registry() -> RuleRegistry:
    return RuleRegistry(
        RuleDefinition(
            rule_id=rule_id,
            semantic_version="1.0.0",
            category=RuleCategory.QUALITY,
            authority=RuleAuthority.GTFS_RECOMMENDED,
            severity=Severity.INFO,
            requirement=RequirementKind.RECOMMENDED,
            applicable_files=("feed_info.txt",),
            specification_reference=SpecificationReference(
                "GTFS Schedule Reference", REVISION, "feed_info.txt Field Definitions"
            ),
            applicability=_APPLICABILITY,
            evaluator_identity=f"gtfs_lab.g08_quality.{rule_id.lower()}/1",
            evaluator=evaluate_g08,
            declared_coverage=(f"feed_info.txt:{field}:header_declaration",),
        )
        for rule_id, field in RULES.items()
    ).freeze()


def register_g08_rules(registry: RuleRegistry | None = None) -> RuleRegistry:
    """Return a deterministic frozen G08 registry, or add its rules to a mutable registry."""
    target = registry if registry is not None else RuleRegistry()
    for definition in _registry():
        target.register(definition)
    return target if registry is not None else target.freeze()


def evaluate_g08(
    feed_info_headers: Sequence[str] | None,
    *,
    g03_feed_info_status: str | None,
    enabled_rule_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Evaluate declarations only; recommendation outcome is separate from RuleStatus.

    ``None`` headers represents a missing file only when G03 says NOT_APPLICABLE.
    A header-absent recommendation remains technical PASS with recommendation_met=False.
    """
    registry = _registry()
    enabled = set(RULES if enabled_rule_ids is None else enabled_rule_ids)
    unknown = enabled - RULES.keys()
    if unknown:
        raise ValueError(f"unknown G08 rule IDs: {sorted(unknown)}")
    headers = set(feed_info_headers or ())
    rules: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for definition in registry:
        rule_id = definition.rule_id
        field = RULES[rule_id]
        if rule_id not in enabled:
            status, reason, met = "NOT_EVALUABLE", "rule disabled by caller", None
        elif feed_info_headers is None and g03_feed_info_status == "NOT_APPLICABLE":
            status, reason, met = "NOT_APPLICABLE", "feed_info.txt is absent", None
        elif feed_info_headers is None or g03_feed_info_status != "PASS":
            status, reason, met = "NOT_EVALUABLE", "G03 did not establish reliable feed_info.txt structure", None
        else:
            met = field in headers
            status = "PASS"
            reason = "recommended field is declared" if met else "recommendation unmet; informational only"
        finding = None
        if met is False:
            finding = {
                "rule_id": rule_id,
                "semantic_version": definition.semantic_version,
                "authority": definition.authority.value,
                "severity": definition.severity.value,
                "source_file": "feed_info.txt",
                "source_fields": [field],
                "observed": "HEADER_ABSENT",
                "recommendation": f"Declare recommended field {field} in feed_info.txt when relevant.",
                "specification_reference": REFERENCE,
            }
            findings.append(finding)
        coverage = (
            {"feature": f"feed_info.txt:{field}:header_declaration", "presence": "ABSENT",
             "audit_support": "NONE", "state": "FEATURE_NOT_PRESENT"}
            if status == "NOT_APPLICABLE" else
            {"feature": f"feed_info.txt:{field}:header_declaration", "presence": "UNKNOWN",
             "audit_support": "NONE", "state": "UNKNOWN"}
            if status == "NOT_EVALUABLE" else
            {"feature": f"feed_info.txt:{field}:header_declaration", "presence": "PRESENT",
             "audit_support": "FULL", "state": "FEATURE_PRESENT_FULLY_AUDITED"}
        )
        rules.append({
            "rule_id": rule_id,
            "semantic_version": definition.semantic_version,
            "category": definition.category.value,
            "authority": definition.authority.value,
            "severity": definition.severity.value,
            "requirement": definition.requirement.value,
            "status": status,
            "recommendation_met": met,
            "reason": reason,
            "coverage": coverage,
            "specification_reference": REFERENCE,
            "findings": [finding] if finding else [],
        })
    statuses = [rule["status"] for rule in rules]
    status = ("INSPECTION_ERROR" if "INSPECTION_ERROR" in statuses else
              "NOT_EVALUABLE" if "NOT_EVALUABLE" in statuses else
              "NOT_APPLICABLE" if statuses and all(value == "NOT_APPLICABLE" for value in statuses) else
              "PASS")
    return {
        "status": status,
        "rules": rules,
        "findings": findings,
        "rule_versions": registry.identity_map()["rule_versions"],
        "limitations": [
            "Checks header declaration only; does not judge values or field relevance.",
            "Recommendation outcome is separate from technical evaluation status.",
            "G03 structural and value coverage remains authoritative.",
        ],
    }


def evaluate_g08_run(ctx: Any, g03_result: Mapping[str, Any]) -> dict[str, Any]:
    """Adapt G03 structural and presence evidence into the G08 input contract."""
    if g03_result.get("status") == "INSPECTION_ERROR":
        return _inspection_error()
    component = g03_result.get("csv_structure")
    presence = g03_result.get("file_presence")
    if not isinstance(component, Mapping) or not isinstance(presence, Mapping):
        return evaluate_g08(None, g03_feed_info_status="NOT_EVALUABLE")
    inspected = next((row for row in component.get("files_inspected", [])
                      if str(row.get("file", "")).casefold() == "feed_info.txt"), None)
    if ctx.tables.get("feed_info") is None:
        decisions = [row for row in presence.get("decisions", [])
                     if row.get("file") == "feed_info.txt"]
        if any(row.get("truth") == "NOT_APPLICABLE" for row in decisions):
            return evaluate_g08(None, g03_feed_info_status="NOT_APPLICABLE")
        return evaluate_g08(None, g03_feed_info_status="NOT_EVALUABLE")
    if inspected is None:
        return evaluate_g08(None, g03_feed_info_status="NOT_EVALUABLE")
    return evaluate_g08(inspected.get("headers"), g03_feed_info_status=inspected.get("status"))


def _inspection_error() -> dict[str, Any]:
    registry = _registry()
    rules = [{
        "rule_id": definition.rule_id,
        "semantic_version": definition.semantic_version,
        "category": definition.category.value,
        "authority": definition.authority.value,
        "severity": definition.severity.value,
        "requirement": definition.requirement.value,
        "status": "INSPECTION_ERROR",
        "recommendation_met": None,
        "coverage": {"feature": definition.declared_coverage[0], "presence": "UNKNOWN",
                     "audit_support": "NONE", "state": "FEATURE_PRESENT_DEFERRED"},
        "findings": [],
    } for definition in registry]
    return {"status": "INSPECTION_ERROR", "rules": rules, "findings": [],
            "rule_versions": registry.identity_map()["rule_versions"],
            "limitations": ["G03 archive inspection failed; G08 was not evaluated."]}
