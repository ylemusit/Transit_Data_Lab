from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
import json

MANIFEST_VERSION = "1.1.0"
RULE_RESULT_STATUSES = {"PASS", "FAIL_TECHNICAL", "WARNING", "NOT_EVALUABLE", "INSPECTION_ERROR"}
FINDING_LIFECYCLE_STATES = {
    "DETECTED",
    "REPRODUCED",
    "EVIDENCE_ATTACHED",
    "REVIEWED",
    "CONFIRMED",
    "REPORTED",
    "FALSE_POSITIVE",
    "TOOL_DEFECT",
    "DATA_AMBIGUITY",
    "REQUIRES_CONTEXT",
}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "ERROR", "WARNING"}
REVIEW_REQUIRED_STATES = {"DATA_AMBIGUITY", "REQUIRES_CONTEXT", "REVIEWED", "CONFIRMED", "REPORTED"}
TERMINAL_FINDING_STATES = {"REPORTED", "FALSE_POSITIVE", "TOOL_DEFECT"}
ALLOWED_FINDING_TRANSITIONS = {
    "DETECTED": {"REPRODUCED", "FALSE_POSITIVE", "TOOL_DEFECT", "DATA_AMBIGUITY", "REQUIRES_CONTEXT"},
    "REPRODUCED": {"EVIDENCE_ATTACHED", "FALSE_POSITIVE", "TOOL_DEFECT", "DATA_AMBIGUITY", "REQUIRES_CONTEXT"},
    "EVIDENCE_ATTACHED": {"REVIEWED", "FALSE_POSITIVE", "TOOL_DEFECT", "DATA_AMBIGUITY", "REQUIRES_CONTEXT"},
    "DATA_AMBIGUITY": {"REVIEWED", "FALSE_POSITIVE", "TOOL_DEFECT", "REQUIRES_CONTEXT"},
    "REQUIRES_CONTEXT": {"REVIEWED", "FALSE_POSITIVE", "TOOL_DEFECT", "DATA_AMBIGUITY"},
    "REVIEWED": {"CONFIRMED", "FALSE_POSITIVE", "TOOL_DEFECT", "DATA_AMBIGUITY", "REQUIRES_CONTEXT"},
    "CONFIRMED": {"REPORTED", "FALSE_POSITIVE", "TOOL_DEFECT"},
    "REPORTED": set(),
    "FALSE_POSITIVE": set(),
    "TOOL_DEFECT": set(),
}


@dataclass(frozen=True)
class AuditManifest:
    audit_id: str
    manifest_version: str
    created_at_utc: str
    run_id: str
    dataset_id: str | None
    source_filename: str
    source_sha256: str
    dataset_ingestion_timestamp_utc: str | None
    gtfs_lab_version: str
    parser_version: str
    validator_version: str
    ruleset_id: str
    scope: list[str] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    original_preserved: bool = False
    preservation_evidence: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)


class AuditContractError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _valid_sha256(value: str | None) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def build_audit_manifest(
    *,
    run_id: str,
    dataset: dict[str, Any],
    gtfs_lab_version: str,
    validator_version: str,
    ruleset_id: str = "gtfs-lab-v1",
    scope: list[str] | None = None,
    excluded: list[str] | None = None,
    original_preserved: bool,
    preservation_evidence: dict[str, Any] | None = None,
    artifacts: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Derive repeated identity fields from DatasetIdentity/run data; do not restate them independently."""
    manifest = AuditManifest(
        audit_id=f"TDL-{run_id}",
        manifest_version=MANIFEST_VERSION,
        created_at_utc=_utc_now(),
        run_id=run_id,
        dataset_id=dataset.get("dataset_id"),
        source_filename=str(dataset.get("source_filename") or ""),
        source_sha256=str(dataset.get("source_sha256") or ""),
        dataset_ingestion_timestamp_utc=dataset.get("ingestion_timestamp_utc"),
        gtfs_lab_version=gtfs_lab_version,
        parser_version=str(dataset.get("parser_version") or "UNKNOWN"),
        validator_version=validator_version,
        ruleset_id=ruleset_id,
        scope=list(scope or ["TECHNICAL_CONFORMANCE", "DATA_QUALITY", "GEOSPATIAL_REVIEW"]),
        excluded=list(excluded or ["LEGAL_CERTIFICATION", "SIRI", "GTFS_RT", "NETEX"]),
        original_preserved=original_preserved,
        preservation_evidence=dict(preservation_evidence or {}),
        artifacts=dict(artifacts or {}),
    )
    data = asdict(manifest)
    validate_audit_manifest(data)
    return data


def validate_audit_manifest(manifest: dict[str, Any]) -> None:
    required = {
        "audit_id",
        "manifest_version",
        "created_at_utc",
        "run_id",
        "source_filename",
        "source_sha256",
        "gtfs_lab_version",
        "parser_version",
        "validator_version",
        "ruleset_id",
        "scope",
        "excluded",
        "original_preserved",
        "preservation_evidence",
    }
    missing = sorted(required - set(manifest))
    if missing:
        raise AuditContractError(f"audit manifest missing required fields: {', '.join(missing)}")
    if not manifest["audit_id"] or not manifest["run_id"]:
        raise AuditContractError("audit_id and run_id must be non-empty")
    if not manifest["source_filename"]:
        raise AuditContractError("source_filename must be non-empty")
    if not _valid_sha256(manifest.get("source_sha256")):
        raise AuditContractError("source_sha256 is mandatory and must be a 64-character hexadecimal SHA-256")
    if manifest["original_preserved"] is not True:
        raise AuditContractError("accepted audit manifests require original_preserved=true based on verified evidence")
    evidence = manifest.get("preservation_evidence")
    if not isinstance(evidence, dict) or evidence.get("verified") is not True:
        raise AuditContractError("preservation_evidence.verified=true is required")
    if evidence.get("source_sha256") != manifest["source_sha256"]:
        raise AuditContractError("preservation evidence source_sha256 must match manifest source_sha256")
    if not isinstance(manifest["scope"], list) or not isinstance(manifest["excluded"], list):
        raise AuditContractError("scope and excluded must be lists")


def stable_finding_id(finding: dict[str, Any]) -> str:
    evidence = finding.get("evidence") or {}
    source_hash = evidence.get("source_sha256")
    if not _valid_sha256(source_hash):
        raise AuditContractError("finding identity requires evidence.source_sha256")
    identity = {
        "source_sha256": source_hash.lower(),
        "rule_id": finding.get("rule_id"),
        "table": finding.get("table"),
        "row_locator": finding.get("row_locator"),
        "field": finding.get("field"),
        "observed_value": finding.get("observed_value"),
        "expected_condition": finding.get("expected_condition"),
    }
    if not identity["rule_id"] or not identity["table"] or not identity["row_locator"]:
        raise AuditContractError("finding identity requires rule_id, table and stable row_locator")
    payload = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return "TDLF-" + sha256(payload.encode("utf-8")).hexdigest()[:20]


def validate_finding_transition(previous_state: str, next_state: str) -> None:
    if previous_state not in FINDING_LIFECYCLE_STATES or next_state not in FINDING_LIFECYCLE_STATES:
        raise AuditContractError("finding lifecycle transition contains unknown state")
    if previous_state == next_state:
        return
    if next_state not in ALLOWED_FINDING_TRANSITIONS[previous_state]:
        raise AuditContractError(f"invalid finding lifecycle transition: {previous_state} -> {next_state}")


def normalize_finding(finding: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(finding)
    normalized.setdefault("finding_id", stable_finding_id(finding))
    expected_id = stable_finding_id(finding)
    if normalized["finding_id"] != expected_id:
        raise AuditContractError("finding_id does not match deterministic finding identity")
    normalized.setdefault("lifecycle_state", "DETECTED")
    if normalized["lifecycle_state"] not in FINDING_LIFECYCLE_STATES:
        raise AuditContractError(f"invalid lifecycle_state: {normalized['lifecycle_state']}")
    required_review = normalized["lifecycle_state"] in REVIEW_REQUIRED_STATES
    normalized.setdefault("review_required", required_review)
    if required_review and normalized["review_required"] is not True:
        raise AuditContractError(f"{normalized['lifecycle_state']} requires human review")
    if normalized["lifecycle_state"] == "REPORTED" and normalized.get("reviewed_by") in (None, ""):
        raise AuditContractError("REPORTED findings require reviewed_by")
    return normalized


def normalize_rule_result(result: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(result)
    status = str(normalized.get("status") or "")
    severity = str(normalized.get("severity") or "")
    if status not in RULE_RESULT_STATUSES:
        raise AuditContractError(f"invalid RuleResult status: {status}")
    if severity not in SEVERITIES:
        raise AuditContractError(f"invalid RuleResult severity: {severity}")
    findings = [normalize_finding(item) for item in normalized.get("findings", [])]
    normalized["findings"] = findings
    normalized["finding_count"] = len(findings)
    normalized.setdefault("checked_rows", 0)
    normalized["review_required"] = any(bool(item.get("review_required")) for item in findings)
    return normalized


def _merge_finding(findings_by_id: dict[str, dict[str, Any]], finding: dict[str, Any]) -> None:
    finding_id = finding["finding_id"]
    existing = findings_by_id.get(finding_id)
    if existing is None:
        findings_by_id[finding_id] = finding
        return
    if existing != finding:
        raise AuditContractError(
            f"conflicting duplicate finding {finding_id}; repeated rule/top-level findings must be identical"
        )


def normalize_validation_payload(validation: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(validation)
    rules = [normalize_rule_result(rule) for rule in normalized.get("rules", [])]
    findings_by_id: dict[str, dict[str, Any]] = {}
    for rule in rules:
        for finding in rule["findings"]:
            _merge_finding(findings_by_id, finding)
    for finding in normalized.get("findings", []):
        _merge_finding(findings_by_id, normalize_finding(finding))
    normalized["rules"] = rules
    normalized["findings"] = list(findings_by_id.values())
    normalized["finding_count"] = len(normalized["findings"])
    return normalized
