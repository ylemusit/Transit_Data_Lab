"""ChangeAttribution 1.1.0: independent semantic versions by stable rule ID.

Legacy ChangeAttribution 1.0.0 is never mutated or inferred from old evidence.
"""
from __future__ import annotations

import re
from typing import Any

from .change_attribution import compare as compare_legacy

CONTRACT_VERSION = "1.1.0"
VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


def _versions(snapshot: dict[str, Any]) -> dict[str, str]:
    rules = snapshot.get("identity", {}).get("rules", {})
    versions = rules.get("rule_versions")
    if not isinstance(versions, dict):
        raise ValueError("ChangeAttribution 1.1.0 requires rules.rule_versions")
    for rule_id, version in versions.items():
        if not isinstance(rule_id, str) or not VERSION_RE.fullmatch(rule_id) or not isinstance(version, str) or not VERSION_RE.fullmatch(version):
            raise ValueError("invalid per-rule semantic identity")
    return dict(sorted(versions.items()))


def compare(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    before_contract = baseline.get("change_attribution_contract_version", "1.0.0")
    after_contract = candidate.get("change_attribution_contract_version", "1.0.0")
    if before_contract == after_contract == "1.0.0":
        return compare_legacy(baseline, candidate)
    if before_contract != "1.1.0" or after_contract != "1.1.0":
        return {"contract_version": CONTRACT_VERSION, "comparability": "NOT_COMPARABLE",
                "reason": "historical per-rule versions cannot be inferred"}
    before, after = _versions(baseline), _versions(candidate)
    # Reuse legacy result/finding comparison, but remove unsupported scalar
    # attribution from a private copy and replace it with the version map.
    import copy
    old, new = copy.deepcopy(baseline), copy.deepcopy(candidate)
    for snapshot in (old, new):
        rules = snapshot["identity"]["rules"]
        rules.pop("rule_versions", None)
        rules.pop("rule_version", None)
        rules.pop("definition_sha256", None)
        snapshot.pop("change_attribution_contract_version", None)
    result = compare_legacy(old, new)
    changes = []
    for rule_id in sorted(set(before) | set(after)):
        if rule_id not in before:
            changes.append({"rule_id": rule_id, "change": "RULE_ADDED", "candidate_version": after[rule_id]})
        elif rule_id not in after:
            changes.append({"rule_id": rule_id, "change": "RULE_REMOVED", "baseline_version": before[rule_id]})
        elif before[rule_id] != after[rule_id]:
            changes.append({"rule_id": rule_id, "change": "RULE_SEMANTIC_CHANGE", "baseline_version": before[rule_id], "candidate_version": after[rule_id]})
    causes = set(result["supported_causes"])
    if changes:
        causes.discard("NO_CHANGE")
        causes.discard("RUNTIME_ONLY_CHANGE")
        # A legacy unattributed result can be explained by the new per-rule
        # identity. Unattributed dataset metadata cannot: a lineage or dataset
        # ID change with unchanged source bytes remains independently unknown.
        unresolved_dataset_identity = any(
            row["identity"] in {"dataset.lineage_id", "dataset.dataset_id"}
            for row in result["identity_differences"]
        ) and "DATASET_CHANGE" not in causes
        if not unresolved_dataset_identity:
            causes.discard("UNATTRIBUTED_CHANGE")
        causes.add("RULE_SEMANTIC_CHANGE")
        result["identity_differences"].extend(
            {"identity": f"rules.rule_versions.{row['rule_id']}",
             "baseline": before.get(row["rule_id"]), "candidate": after.get(row["rule_id"])}
            for row in changes
        )
        result["evidence_refs"].extend(f"identity.rules.rule_versions.{row['rule_id']}" for row in changes)
        if result["confidence_or_evidence_status"]["status"] == "NO_CAUSAL_EVIDENCE":
            result["confidence_or_evidence_status"]["status"] = "SUPPORTED"
        if unresolved_dataset_identity and not result["unresolved_reasons"]:
            result["unresolved_reasons"].append("dataset identity changed without a supported source change")
        if "UNATTRIBUTED_CHANGE" not in causes:
            result["unresolved_reasons"] = [
                reason for reason in result["unresolved_reasons"]
                if reason != "result changed without a supported identity cause"
            ]
    result.update(contract_version=CONTRACT_VERSION, comparability="COMPARABLE",
                  per_rule_changes=changes, rules_change=bool(changes),
                  supported_causes=sorted(causes),
                  attribution=next(iter(causes)) if len(causes) == 1 else "MULTIPLE_CAUSES")
    return result
