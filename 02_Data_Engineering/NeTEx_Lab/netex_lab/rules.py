from __future__ import annotations

from typing import TypedDict

from .contracts import STATUSES


class RuleSpec(TypedDict):
    rule_id: str
    version: str
    authority: str
    requirement_id: str | None
    scope: str
    applicability: str
    evaluation_type: str
    family: str
    severity: str
    evidence_contract: str
    status_vocabulary: list[str]


RULES: tuple[RuleSpec, ...] = (
    {
        "rule_id": "NETEX-XML-001", "version": "1.0.0", "authority": "L4_TDL_TECHNICAL",
        "requirement_id": "NETEX-REQ-XML-01", "scope": "all XML inputs",
        "applicability": "ALWAYS", "evaluation_type": "DIRECT_XML",
        "family": "XSD", "severity": "ERROR", "evidence_contract": "parser state and source SHA-256",
        "status_vocabulary": ["PASS", "FAIL_TECHNICAL", "INSPECTION_ERROR"],
    },
    {
        "rule_id": "NETEX-XSD-001", "version": "1.0.0", "authority": "L4_PINNED_SCHEMA_ARTIFACT",
        "requirement_id": "NETEX-REQ-XSD-01", "scope": "NeTEx v2.0.0 publication schema",
        "applicability": "WELL_FORMED_XML", "evaluation_type": "DIRECT_XSD",
        "family": "XSD", "severity": "ERROR", "evidence_contract": "schema identity and validator log",
        "status_vocabulary": ["PASS", "FAIL_TECHNICAL", "NOT_EVALUABLE", "INSPECTION_ERROR"],
    },
    {
        "rule_id": "NETEX-PROFILE-001", "version": "1.0.0", "authority": "L3_EPIP_2026",
        "requirement_id": "NETEX-REQ-EPIP-UNKNOWN", "scope": "EPIP 2026 constraints beyond XSD",
        "applicability": "REGULAR_SCHEDULED_BUS", "evaluation_type": "PROFILE_CONSTRAINT",
        "family": "PROFILE", "severity": "REVIEW", "evidence_contract": "normative text and mapped assertion required",
        "status_vocabulary": ["NOT_EVALUABLE", "HUMAN_REVIEW_REQUIRED"],
    },
    {
        "rule_id": "NETEX-IDENTITY-001", "version": "1.0.0", "authority": "L4_TDL_RECOMMENDATION",
        "requirement_id": None, "scope": "duplicate object identifiers in one publication",
        "applicability": "IDENTIFIED_OBJECTS", "evaluation_type": "SEMANTIC_DIAGNOSTIC",
        "family": "IDENTITY", "severity": "ADVISORY", "evidence_contract": "object identifiers and locations",
        "status_vocabulary": ["PASS", "HUMAN_REVIEW_REQUIRED"],
    },
)


def validate_registry() -> None:
    seen: set[str] = set()
    for rule in RULES:
        if rule["rule_id"] in seen:
            raise ValueError(f"Duplicate rule id: {rule['rule_id']}")
        seen.add(rule["rule_id"])
        for key in ("version", "authority", "scope", "evaluation_type", "family", "evidence_contract"):
            if not rule.get(key):
                raise ValueError(f"Missing {key} on {rule['rule_id']}")
        unknown_statuses = set(rule["status_vocabulary"]) - STATUSES
        if unknown_statuses:
            raise ValueError(f"Unknown statuses on {rule['rule_id']}: {sorted(unknown_statuses)}")
        if rule["authority"] not in {"L1", "L2", "L3", "L3_EPIP_2026", "L4_TDL_TECHNICAL", "L4_PINNED_SCHEMA_ARTIFACT", "L4_TDL_RECOMMENDATION"}:
            raise ValueError(f"Unrecognized authority on {rule['rule_id']}")
