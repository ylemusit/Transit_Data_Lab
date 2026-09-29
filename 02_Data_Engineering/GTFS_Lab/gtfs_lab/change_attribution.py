"""Deterministic ChangeAttribution 1.0.0 contract for comparing audit snapshots."""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .audit_contract import AuditContractError, stable_finding_id

CONTRACT_VERSION = "1.0.0"
RUNTIME_KEYS = {"audit_id", "run_id", "runtime_id", "timestamp", "created_at_utc", "execution_directory", "output_path", "machine_path"}
IMPLEMENTATION_FIELDS = {
    "engine.git_commit": "ENGINE_IMPLEMENTATION_CHANGE",
    "engine.parser_version": "PARSER_IMPLEMENTATION_CHANGE",
    "engine.validator_version": "VALIDATOR_IMPLEMENTATION_CHANGE",
    "engine.gtfs_lab_version": "ENGINE_IMPLEMENTATION_CHANGE",
    "compliance.evaluator_version": "COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE",
    "compliance.evaluator_sha256": "COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE",
}
IDENTITY_GROUPS = ("dataset", "engine", "rules", "compliance", "configuration")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _runtime_only(value: Any, path: tuple[str, ...] = ()) -> Any:
    if isinstance(value, dict):
        is_snapshot = not path
        return {
            k: _runtime_only(v, path + (k,))
            for k, v in sorted(value.items())
            if not (is_snapshot and k in RUNTIME_KEYS) and k != "runtime"
        }
    if isinstance(value, list):
        return [_runtime_only(item, path + ("[]",)) for item in value]
    return value


def _identity_differences(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    differences = []
    for group in IDENTITY_GROUPS:
        a, b = left.get(group, {}), right.get(group, {})
        if not isinstance(a, dict) or not isinstance(b, dict):
            raise ValueError(f"identity.{group} must be an object when supplied")
        for key in sorted(set(a) | set(b)):
            av, bv = a.get(key), b.get(key)
            if key.endswith("sha256"):
                for value in (av, bv):
                    if value is not None and (not isinstance(value, str) or not SHA256_RE.fullmatch(value)):
                        raise ValueError(f"identity.{group}.{key} must be a 64-character SHA-256 when supplied")
                if isinstance(av, str): av = av.lower()
                if isinstance(bv, str): bv = bv.lower()
            if av != bv:
                differences.append({"identity": f"{group}.{key}", "baseline": av, "candidate": bv})
    return differences


def _finding_key(finding: dict[str, Any]) -> str:
    explicit = finding.get("finding_id")
    if isinstance(explicit, str) and explicit:
        return explicit
    try:
        return stable_finding_id(finding)
    except (AuditContractError, AttributeError, TypeError):
        raise ValueError("finding requires finding_id or a valid M01 stable finding identity")


def _findings(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = snapshot.get("findings", [])
    if not isinstance(raw, list):
        raise ValueError("findings must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("each finding must be an object")
        key = _finding_key(item)
        if key in indexed and _canonical(indexed[key]) != _canonical(item):
            raise ValueError(f"conflicting findings share stable identity: {key}")
        indexed[key] = item
    return indexed


def _compare_findings(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    before, after = _findings(baseline), _findings(candidate)
    changes = []
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key), after.get(key)
        if old is None:
            changes.append({"finding_id": key, "change": "NEW_FINDING"})
        elif new is None:
            changes.append({"finding_id": key, "change": "RESOLVED_FINDING"})
        else:
            old_status = old.get("lifecycle_state", old.get("status"))
            new_status = new.get("lifecycle_state", new.get("status"))
            if old_status != new_status:
                changes.append({"finding_id": key, "change": "FINDING_STATUS_CHANGE", "baseline_status": old_status, "candidate_status": new_status})
            elif _canonical(_runtime_only(old, ("finding",))) != _canonical(_runtime_only(new, ("finding",))):
                changes.append({"finding_id": key, "change": "FINDING_EVIDENCE_CHANGE"})
    return {"changed": bool(changes), "changes": changes}


def _compare_results(baseline: Any, candidate: Any) -> dict[str, Any]:
    if not isinstance(baseline, dict) or not isinstance(candidate, dict):
        return {"status": "NOT_COMPARABLE", "changed": None, "differences": []}
    before, after = baseline.get("rules"), candidate.get("rules")
    if not isinstance(before, list) or not isinstance(after, list):
        return {"status": "NOT_COMPARABLE", "changed": None, "differences": []}
    def by_id(rows: list[Any]) -> dict[str, dict[str, Any]]:
        output = {}
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("rule_id"), str) or not row["rule_id"] or row["rule_id"] in output:
                raise ValueError("each result rule needs a unique non-empty rule_id")
            output[row["rule_id"]] = row
        return output
    old_rows, new_rows = by_id(before), by_id(after)
    differences = []
    for rule_id in sorted(set(old_rows) | set(new_rows)):
        old, new = old_rows.get(rule_id), new_rows.get(rule_id)
        if old is None:
            differences.append({"rule_id": rule_id, "change": "RULE_NEW"})
        elif new is None:
            differences.append({"rule_id": rule_id, "change": "RULE_REMOVED"})
        else:
            a, b = old.get("status"), new.get("status")
            if a != b:
                differences.append({"rule_id": rule_id, "change": "STATUS_CHANGED", "baseline_status": a, "candidate_status": b})
            elif _finding_count(old) != _finding_count(new):
                differences.append({"rule_id": rule_id, "change": "FINDING_COUNT_CHANGED", "baseline_count": _finding_count(old), "candidate_count": _finding_count(new)})
            elif _result_finding_set(old) != _result_finding_set(new):
                differences.append({"rule_id": rule_id, "change": "FINDING_SET_CHANGED"})
    return {"status": differences[0]["change"] if len(differences) == 1 else ("UNCHANGED_STATUS" if not differences else "MULTIPLE_CHANGES"), "changed": bool(differences), "differences": differences}


def _finding_count(rule: dict[str, Any]) -> int | None:
    count = rule.get("finding_count")
    if type(count) is int:
        return count
    findings = rule.get("findings")
    return len(findings) if isinstance(findings, list) else None


def _result_finding_set(rule: dict[str, Any]) -> tuple[str, ...] | None:
    findings = rule.get("findings")
    if not isinstance(findings, list):
        return None
    return tuple(sorted(_finding_key(f) for f in findings if isinstance(f, dict)))


def compare(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Compare two snapshots containing audit_id, identity, result and findings.

    Missing identity values are retained as unknown; they never prove a cause.
    Runtime metadata is excluded from semantic comparison.
    """
    for name, snapshot in (("baseline", baseline), ("candidate", candidate)):
        if not isinstance(snapshot, dict) or not isinstance(snapshot.get("audit_id"), str) or not snapshot["audit_id"]:
            raise ValueError(f"{name} requires a non-empty audit_id")
        if not isinstance(snapshot.get("identity"), dict):
            raise ValueError(f"{name}.identity must be an object")
    identity_differences = _identity_differences(baseline["identity"], candidate["identity"])
    result_change = _compare_results(baseline.get("result"), candidate.get("result"))
    finding_change = _compare_findings(baseline, candidate)
    changed_identity_paths = {item["identity"] for item in identity_differences}
    causes: set[str] = set()

    if "dataset.source_sha256" in changed_identity_paths and baseline["identity"].get("dataset", {}).get("source_sha256") and candidate["identity"].get("dataset", {}).get("source_sha256"):
        causes.add("DATASET_CHANGE")
    for path in changed_identity_paths:
        if path in IMPLEMENTATION_FIELDS:
            causes.add(IMPLEMENTATION_FIELDS[path])
    if changed_identity_paths & {"rules.ruleset_id", "rules.ruleset_version"}:
        causes.add("RULESET_CHANGE")
    if changed_identity_paths & {"rules.rule_version", "rules.definition_sha256", "compliance.semantic_rule_version"}:
        causes.add("RULE_SEMANTIC_CHANGE")
    if "compliance.package_sha256" in changed_identity_paths:
        causes.add("COMPLIANCE_PACKAGE_CHANGE")
    if any(path.startswith("compliance.reference") for path in changed_identity_paths):
        causes.add("REFERENCE_CHANGE")
    if any(path.startswith("configuration.") for path in changed_identity_paths):
        causes.add("CONFIGURATION_CHANGE")
    if "dataset.lineage_id" in changed_identity_paths or "dataset.dataset_id" in changed_identity_paths:
        # Identity metadata alone is insufficient evidence of changed source bytes.
        if not ("dataset.source_sha256" in changed_identity_paths and "DATASET_CHANGE" in causes):
            causes.add("UNATTRIBUTED_CHANGE")

    runtime_changed = _canonical(_runtime_only(baseline)) == _canonical(_runtime_only(candidate)) and baseline != candidate
    semantic_changed = result_change["changed"] is True or finding_change["changed"]
    if not causes and semantic_changed:
        causes.add("UNATTRIBUTED_CHANGE")
    if not causes and runtime_changed:
        causes.add("RUNTIME_ONLY_CHANGE")
    if not causes:
        causes.add("NO_CHANGE")

    dataset_hashes = [baseline["identity"].get("dataset", {}).get("source_sha256"), candidate["identity"].get("dataset", {}).get("source_sha256")]
    missing = [f"{side}.dataset.source_sha256" for side, value in zip(("baseline", "candidate"), dataset_hashes) if not value]
    evidence_status = "MISSING_IDENTITY" if missing else ("SUPPORTED" if causes - {"NO_CHANGE", "RUNTIME_ONLY_CHANGE", "UNATTRIBUTED_CHANGE"} else "NO_CAUSAL_EVIDENCE")
    attribution = next(iter(causes)) if len(causes) == 1 else "MULTIPLE_CAUSES"
    comparison_id = "CA-" + hashlib.sha256(f"{baseline['audit_id']}\0{candidate['audit_id']}".encode()).hexdigest()[:16]
    return {
        "comparison_id": comparison_id,
        "contract_version": CONTRACT_VERSION,
        "baseline_audit_id": baseline["audit_id"],
        "candidate_audit_id": candidate["audit_id"],
        "baseline_identity": _runtime_only(baseline["identity"]),
        "candidate_identity": _runtime_only(candidate["identity"]),
        "identity_differences": identity_differences,
        "dataset_change": "DATASET_CHANGE" in causes,
        "engine_change": any(x.endswith("IMPLEMENTATION_CHANGE") for x in causes),
        "rules_change": bool(changed_identity_paths & {"rules.ruleset_id", "rules.ruleset_version", "rules.rule_version", "rules.definition_sha256", "compliance.semantic_rule_version"}),
        "configuration_change": "CONFIGURATION_CHANGE" in causes,
        "reference_change": "REFERENCE_CHANGE" in causes,
        "result_change": result_change,
        "finding_change": finding_change,
        "attribution": attribution,
        "supported_causes": sorted(causes),
        "confidence_or_evidence_status": {"status": evidence_status, "missing_identity": missing},
        "evidence_refs": [f"identity.{item['identity']}" for item in identity_differences],
        "unresolved_reasons": ["result changed without a supported identity cause"] if "UNATTRIBUTED_CHANGE" in causes and semantic_changed else [],
    }
