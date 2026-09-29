"""Read-only productive comparison of persisted GTFS_Lab audit evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit_contract import AuditContractError, stable_finding_id, validate_audit_manifest
from .change_attribution import CONTRACT_VERSION as CHANGE_ATTRIBUTION_VERSION
from .change_attribution import compare as compare_change_attribution
from .change_attribution_v1_1 import compare as compare_change_attribution_v1_1

SNAPSHOT_CONTRACT_VERSION = "1.0.0"
SNAPSHOT_CONTRACT = "AuditComparisonSnapshot"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
FINDING_RUNTIME_KEYS = {"audit_id", "run_id", "runtime_id", "timestamp", "created_at_utc", "execution_directory", "output_path", "machine_path", "dataset_id", "source_sha256"}


class ComparisonError(ValueError):
    """An explicit, fail-closed audit comparison error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ComparisonError("SNAPSHOT_INVALID", f"missing {label}: {path.name}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ComparisonError("SNAPSHOT_INVALID", f"cannot read {label}: {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ComparisonError("SNAPSHOT_INVALID", f"{label} must be a JSON object")
    return value


def _artifact_path(run_dir: Path, audit_dir: Path, reference: Any, label: str) -> Path:
    if not isinstance(reference, str) or not reference.strip():
        raise ComparisonError("SNAPSHOT_INVALID", f"manifest artifact {label} is missing")
    candidate = (audit_dir / reference).resolve()
    try:
        candidate.relative_to(run_dir.resolve())
    except ValueError as exc:
        raise ComparisonError("SNAPSHOT_INVALID", f"manifest artifact {label} escapes audit directory") from exc
    if not candidate.is_file():
        raise ComparisonError("SNAPSHOT_INVALID", f"manifest artifact {label} is unavailable")
    return candidate


def _sha256(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ComparisonError("SNAPSHOT_INVALID", f"{field} is not a valid SHA-256")
    return value.lower()


def _canonical_findings(findings: Any, field: str) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        raise ComparisonError("SNAPSHOT_INVALID", f"{field} must be a list")
    output = []
    seen: dict[str, str] = {}
    for item in findings:
        if not isinstance(item, dict):
            raise ComparisonError("FINDING_IDENTITY_INVALID", f"{field} contains a non-object finding")
        try:
            expected_id = stable_finding_id(item)
            finding_id = item.get("finding_id")
            if finding_id is not None and finding_id != expected_id:
                raise ComparisonError("FINDING_IDENTITY_INVALID", f"{field} finding_id does not match M01 stable identity")
        except (AuditContractError, TypeError, AttributeError) as exc:
            raise ComparisonError("FINDING_IDENTITY_INVALID", f"{field} finding has invalid M01 stable identity: {exc}") from exc
        finding_id = expected_id
        canonical_item = {key: value for key, value in item.items() if key not in FINDING_RUNTIME_KEYS}
        canonical_item["finding_id"] = finding_id
        encoded = json.dumps(canonical_item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if finding_id in seen and seen[finding_id] != encoded:
            raise ComparisonError("FINDING_IDENTITY_INVALID", f"{field} contains conflicting duplicate finding_id {finding_id}")
        seen[finding_id] = encoded
        output.append(item)
    return [json.loads(seen[key]) for key in sorted(seen)]


def _canonical_rules(validation: dict[str, Any], source_sha256: str) -> list[dict[str, Any]]:
    rules = validation.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ComparisonError("NOT_COMPARABLE", "validation.rules must be a non-empty list")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in rules:
        if not isinstance(raw, dict):
            raise ComparisonError("SNAPSHOT_INVALID", "validation.rules contains a non-object row")
        rule_id = raw.get("rule_id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise ComparisonError("SNAPSHOT_INVALID", "each rule result requires a non-empty rule_id")
        if rule_id in by_id:
            raise ComparisonError("DUPLICATE_RULE_ID", f"duplicate result rule_id: {rule_id}")
        if not isinstance(raw.get("status"), str) or not raw["status"]:
            raise ComparisonError("SNAPSHOT_INVALID", f"rule {rule_id} has no status")
        source_findings = raw.get("findings", [])
        if isinstance(source_findings, list):
            enriched = []
            for finding in source_findings:
                if not isinstance(finding, dict):
                    enriched.append(finding)
                    continue
                copied = dict(finding)
                evidence = dict(copied.get("evidence") or {})
                declared_hash = evidence.get("source_sha256")
                if declared_hash is not None and str(declared_hash).lower() != source_sha256:
                    raise ComparisonError("SNAPSHOT_INVALID", f"rule {rule_id} finding source hash differs from AuditManifest")
                # M02 explicitly attaches the manifest dataset hash when a finding omits it.
                evidence["source_sha256"] = source_sha256
                copied["evidence"] = evidence
                enriched.append(copied)
            source_findings = enriched
        findings = _canonical_findings(source_findings, f"rule {rule_id}.findings")
        by_id[rule_id] = {
            "rule_id": rule_id,
            "status": raw["status"],
            "finding_count": len(findings),
            "findings": findings,
        }
    return [by_id[key] for key in sorted(by_id)]


def build_audit_snapshot(run_directory: str | Path) -> dict[str, Any]:
    """Build a canonical input snapshot from one persisted, accepted audit run."""
    run_dir = Path(run_directory).expanduser().resolve()
    audit_dir = run_dir / "audit"
    manifest = _read_json(audit_dir / "audit_manifest.json", "AuditManifest")
    try:
        validate_audit_manifest(manifest)
    except (AuditContractError, KeyError, TypeError) as exc:
        raise ComparisonError("SNAPSHOT_INVALID", f"invalid AuditManifest: {exc}") from exc
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ComparisonError("SNAPSHOT_INVALID", "AuditManifest artifacts must be an object")
    run = _read_json(_artifact_path(run_dir, audit_dir, artifacts.get("run"), "run"), "run artifact")
    validation = _read_json(_artifact_path(run_dir, audit_dir, artifacts.get("validation"), "validation"), "validation artifact")
    normalized = _read_json(_artifact_path(run_dir, audit_dir, artifacts.get("findings_normalized"), "findings_normalized"), "normalized findings")
    if run.get("run_id") != manifest.get("run_id") or normalized.get("audit_id") != manifest.get("audit_id"):
        raise ComparisonError("SNAPSHOT_INVALID", "run, findings, and AuditManifest identities do not agree")
    run_dataset = run.get("dataset")
    if not isinstance(run_dataset, dict) or run_dataset.get("dataset_id") != manifest.get("dataset_id") or str(run_dataset.get("source_sha256", "")).lower() != str(manifest.get("source_sha256", "")).lower():
        raise ComparisonError("SNAPSHOT_INVALID", "run dataset identity does not agree with AuditManifest")
    if normalized.get("status") != "NORMALIZED":
        raise ComparisonError("SNAPSHOT_INVALID", "normalized findings artifact is not accepted")
    normalized_sha = _sha256(normalized.get("source_sha256"), "findings.normalized.source_sha256")
    if normalized_sha != str(manifest.get("source_sha256", "")).lower():
        raise ComparisonError("SNAPSHOT_INVALID", "normalized findings source hash differs from AuditManifest")

    source_sha = _sha256(manifest.get("source_sha256"), "dataset.source_sha256")
    all_findings = _canonical_findings(normalized.get("findings"), "findings.normalized")
    rules = _canonical_rules(validation, source_sha or "")
    raw_rule_versions = manifest.get("executed_rule_versions")
    raw_rule_ids = manifest.get("executed_rule_ids")
    if not isinstance(raw_rule_versions, dict) or not isinstance(raw_rule_ids, list):
        raise ComparisonError("SNAPSHOT_INVALID", "AuditManifest executed rule identity is malformed")
    actual_rule_ids = {rule["rule_id"] for rule in rules}
    if set(raw_rule_ids) != actual_rule_ids or set(raw_rule_versions) != actual_rule_ids:
        raise ComparisonError("SNAPSHOT_INVALID", "AuditManifest and validation rule identities do not agree")
    validation_versions = {str(rule["rule_id"]): str(rule.get("version", "")) for rule in validation["rules"]}
    rule_versions = {str(key): str(value) for key, value in raw_rule_versions.items()}
    if rule_versions != validation_versions:
        raise ComparisonError("SNAPSHOT_INVALID", "AuditManifest and validation rule versions do not agree")
    rule_versions = dict(sorted(rule_versions.items()))
    normalized_ids = {item["finding_id"] for item in all_findings}
    result_ids = {item["finding_id"] for rule in rules for item in rule["findings"]}
    if normalized_ids != result_ids:
        raise ComparisonError("SNAPSHOT_INVALID", "validation and normalized finding sets do not reconcile")

    compliance_result = run.get("compliance_v1") or {}
    if not isinstance(compliance_result, dict):
        raise ComparisonError("SNAPSHOT_INVALID", "run.compliance_v1 must be an object when supplied")
    compliance_sha = _sha256(compliance_result.get("evaluator_sha256"), "compliance.evaluator_sha256")
    reference_sha = _sha256(compliance_result.get("reference_sha256"), "compliance.reference_sha256")
    package_sha = _sha256(compliance_result.get("package_sha256"), "compliance.package_sha256")
    identity = {
        "dataset": {
            "source_sha256": source_sha,
            "dataset_id": manifest.get("dataset_id"),
            "lineage_id": None,
        },
        "engine": {
            "git_commit": None,
            "parser_version": manifest.get("parser_version"),
            "validator_version": manifest.get("validator_version"),
            "gtfs_lab_version": manifest.get("gtfs_lab_version"),
        },
        "rules": {
            "ruleset_id": manifest.get("ruleset_id"),
            "ruleset_version": manifest.get("ruleset_version"),
            "rule_version": next(iter(set(rule_versions.values()))) if len(set(rule_versions.values())) == 1 else None,
            "rule_versions": rule_versions,
        },
        "compliance": {
            "semantic_rule_version": compliance_result.get("rule_version"),
            "evaluator_version": compliance_result.get("evaluator_version"),
            "evaluator_sha256": compliance_sha,
            "package_sha256": package_sha,
            "reference_sha256": reference_sha,
        },
        "configuration": {"sha256": None},
    }
    missing_identity = [
        f"{group}.{key}"
        for group, fields in identity.items()
        for key, value in fields.items()
        if value is None or value == ""
    ]
    return {
        "snapshot_contract": SNAPSHOT_CONTRACT,
        "snapshot_contract_version": SNAPSHOT_CONTRACT_VERSION,
        **({"change_attribution_contract_version": manifest["change_attribution_contract_version"]}
           if "change_attribution_contract_version" in manifest else {}),
        "audit_id": manifest["audit_id"],
        "identity": identity,
        "result": {"rules": rules},
        "findings": all_findings,
        "missing_identity": missing_identity,
    }


def _compatibility(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    contracts = (baseline.get("change_attribution_contract_version", "1.0.0"),
                 candidate.get("change_attribution_contract_version", "1.0.0"))
    if contracts not in (("1.0.0", "1.0.0"), ("1.1.0", "1.1.0")):
        reasons.append("CHANGE_ATTRIBUTION_CONTRACTS_NOT_COMPARABLE")
    for side, snapshot in (("baseline", baseline), ("candidate", candidate)):
        if snapshot.get("snapshot_contract") != SNAPSHOT_CONTRACT:
            reasons.append(f"{side}:SNAPSHOT_CONTRACT_UNSUPPORTED")
        if snapshot.get("snapshot_contract_version") != SNAPSHOT_CONTRACT_VERSION:
            reasons.append(f"{side}:SNAPSHOT_VERSION_UNSUPPORTED")
        result_rules = snapshot.get("result", {}).get("rules") if isinstance(snapshot.get("result"), dict) else None
        if not isinstance(result_rules, list) or not result_rules:
            reasons.append(f"{side}:RESULTS_UNAVAILABLE")
        identity = snapshot.get("identity")
        if not isinstance(identity, dict):
            reasons.append(f"{side}:IDENTITY_UNAVAILABLE")
            continue
        for path in ("dataset.source_sha256", "engine.parser_version", "engine.validator_version", "engine.gtfs_lab_version", "rules.ruleset_id", "rules.ruleset_version"):
            group, key = path.split(".")
            value = identity.get(group, {}).get(key) if isinstance(identity.get(group), dict) else None
            if value is None or value == "":
                reasons.append(f"{side}:MISSING_REQUIRED_IDENTITY:{path}")
    baseline_rules = baseline.get("identity", {}).get("rules", {}) if isinstance(baseline.get("identity"), dict) else {}
    candidate_rules = candidate.get("identity", {}).get("rules", {}) if isinstance(candidate.get("identity"), dict) else {}
    if isinstance(baseline_rules, dict) and isinstance(candidate_rules, dict):
        before_versions = baseline_rules.get("rule_versions")
        after_versions = candidate_rules.get("rule_versions")
        if (baseline.get("change_attribution_contract_version", "1.0.0") == "1.0.0"
                and candidate.get("change_attribution_contract_version", "1.0.0") == "1.0.0"
                and isinstance(before_versions, dict) and isinstance(after_versions, dict) and before_versions != after_versions
                and (baseline_rules.get("rule_version") is None or candidate_rules.get("rule_version") is None)):
            reasons.append("RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0")
    if reasons:
        return {"status": "NOT_COMPARABLE", "reasons": sorted(reasons)}
    def optional_missing(snapshot: dict[str, Any]) -> set[str]:
        identity = snapshot["identity"]
        return {
            f"{group}.{key}"
            for group in ("dataset", "engine", "rules", "compliance", "configuration")
            for key, value in identity.get(group, {}).items()
            if value is None or value == ""
        }
    missing_optional = sorted(optional_missing(baseline) | optional_missing(candidate))
    return {"status": "PARTIALLY_COMPARABLE" if missing_optional else "COMPARABLE", "reasons": [], "missing_optional_identity": missing_optional}


def compare_audits(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Validate snapshot compatibility, then apply ChangeAttribution 1.0.0."""
    for name, snapshot in (("baseline", baseline), ("candidate", candidate)):
        if not isinstance(snapshot, dict):
            raise ComparisonError("SNAPSHOT_INVALID", f"{name} snapshot must be an object")
        if not isinstance(snapshot.get("audit_id"), str) or not snapshot["audit_id"].strip():
            raise ComparisonError("SNAPSHOT_INVALID", f"{name} requires a non-empty audit_id")
    comparability = _compatibility(baseline, candidate)
    if comparability["status"] == "NOT_COMPARABLE":
        return {
            "comparison_id": _comparison_id(baseline, candidate),
            "snapshot_contract_version": SNAPSHOT_CONTRACT_VERSION,
            "change_attribution_contract_version": "1.1.0" if any(
                snapshot.get("change_attribution_contract_version") == "1.1.0" for snapshot in (baseline, candidate)
            ) else CHANGE_ATTRIBUTION_VERSION,
            "baseline_audit_id": baseline.get("audit_id"),
            "candidate_audit_id": candidate.get("audit_id"),
            "comparability": comparability,
            "identity_differences": [],
            "result_change": {"status": "NOT_COMPARABLE", "changed": None, "differences": []},
            "finding_change": {"changed": None, "changes": []},
            "attribution": "NOT_COMPARABLE",
            "supported_causes": [],
            "evidence_status": "INSUFFICIENT",
            "evidence_refs": [],
            "unresolved_reasons": comparability["reasons"],
        }
    try:
        versions = (baseline.get("change_attribution_contract_version", "1.0.0"), candidate.get("change_attribution_contract_version", "1.0.0"))
        attribution = compare_change_attribution(baseline, candidate) if versions == ("1.0.0", "1.0.0") else compare_change_attribution_v1_1(baseline, candidate)
    except ValueError as exc:
        message = str(exc)
        code = "DUPLICATE_RULE_ID" if "unique non-empty rule_id" in message else "FINDING_IDENTITY_INVALID" if "finding" in message else "SNAPSHOT_INVALID"
        raise ComparisonError(code, message) from exc
    return {
        "comparison_id": attribution["comparison_id"],
        "snapshot_contract_version": SNAPSHOT_CONTRACT_VERSION,
        "change_attribution_contract_version": attribution["contract_version"],
        "baseline_audit_id": attribution["baseline_audit_id"],
        "candidate_audit_id": attribution["candidate_audit_id"],
        "comparability": comparability,
        "identity_differences": attribution["identity_differences"],
        "result_change": attribution["result_change"],
        "finding_change": attribution["finding_change"],
        "attribution": attribution["attribution"],
        **({"per_rule_changes": attribution["per_rule_changes"]} if "per_rule_changes" in attribution else {}),
        "supported_causes": attribution["supported_causes"],
        "evidence_status": attribution["confidence_or_evidence_status"]["status"],
        "evidence_refs": attribution["evidence_refs"],
        "unresolved_reasons": attribution["unresolved_reasons"],
    }


def _comparison_id(baseline: dict[str, Any], candidate: dict[str, Any]) -> str:
    pair = f"{baseline.get('audit_id', '')}\0{candidate.get('audit_id', '')}"
    return "CA-" + hashlib.sha256(pair.encode("utf-8")).hexdigest()[:16]


def compare_audit_directories(baseline_directory: str | Path, candidate_directory: str | Path) -> dict[str, Any]:
    return compare_audits(build_audit_snapshot(baseline_directory), build_audit_snapshot(candidate_directory))


RECORD_CONTRACT = "AuditComparisonRecord"
RECORD_CONTRACT_VERSION = "1.0.0"


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def verify_comparison_record(record: dict[str, Any], baseline: dict[str, Any], candidate: dict[str, Any]) -> bool:
    if record.get("record_contract") != RECORD_CONTRACT or record.get("record_contract_version") != RECORD_CONTRACT_VERSION:
        raise ComparisonError("COMPARISON_RECORD_INVALID", "unsupported comparison record contract")
    integrity = record.get("integrity", {})
    payload = {key: record[key] for key in ("comparison_id", "baseline_audit_id", "candidate_audit_id", "comparison", "source_artifacts")}
    expected = {"baseline_snapshot_sha256": _digest(baseline), "candidate_snapshot_sha256": _digest(candidate),
                "comparison_payload_sha256": _digest(payload),
                "record_sha256": _digest({key: value for key, value in record.items() if key != "integrity"})}
    if integrity != expected:
        raise ComparisonError("COMPARISON_HASH_MISMATCH", "comparison record integrity verification failed")
    return True


def render_comparison_report(record: dict[str, Any]) -> bytes:
    """Render the compact comparison record as deterministic UTF-8 Markdown."""
    result = record["comparison"]
    finding = result.get("finding_change", {})
    changes = finding.get("changes", [])
    groups = {
        "Findings added": [x for x in changes if x.get("change") == "NEW_FINDING"],
        "Findings resolved": [x for x in changes if x.get("change") == "RESOLVED_FINDING"],
        "Findings changed": [x for x in changes if x.get("change") not in {"NEW_FINDING", "RESOLVED_FINDING"}],
    }
    lines = ["# Audit comparison", "", f"- Comparison: `{record['comparison_id']}`",
             f"- Baseline: `{record['baseline_audit_id']}`",
             f"- Candidate: `{record['candidate_audit_id']}`",
             f"- Comparability: `{result['comparability']['status']}`",
             f"- Attribution: `{result['attribution']}`", "", "## What changed", "",
             f"- Result change: `{result['result_change'].get('status')}`; changed=`{result['result_change'].get('changed')}`",
             f"- Finding change: changed=`{finding.get('changed')}`",
             f"- Supported causes: {', '.join(result.get('supported_causes', [])) or 'none recorded'}", "", "## Identity differences", ""]
    for difference in result.get("identity_differences", []):
        before = json.dumps(difference.get("baseline"), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        after = json.dumps(difference.get("candidate"), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        lines.append(f"- `{difference.get('identity')}`: `{before}` → `{after}`")
    if not result.get("identity_differences"):
        lines.append("- None recorded")
    lines.extend(["", "## Result differences", ""])
    for difference in result["result_change"].get("differences", []):
        rendered = json.dumps(difference, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if isinstance(difference, (dict, list)) else str(difference)
        lines.append(f"- `{rendered}`")
    if not result["result_change"].get("differences"):
        lines.append("- None recorded")
    lines.append("")
    if "historical_rows" in result:
        lines.extend(["## Historical comparisons", ""])
        for row in result["historical_rows"]:
            lines.append(f"- Dataset `{row['dataset_id']}`: result `{row['result_change']}`; attribution `{row['attribution']}`; causes `{', '.join(row['supported_causes']) or 'none'}`; evidence `{row['evidence_state']}`.")
        lines.append("")
    for title, rows in groups.items():
        lines.extend([f"## {title}", "", *(f"- `{row.get('finding_id', 'unknown')}`: `{row.get('change')}`" for row in rows)])
        if not rows:
            lines.append("- None")
        lines.append("")
    lines.extend(["## Unresolved causes", "", *(f"- `{x}`" for x in result.get("unresolved_reasons", []))])
    if not result.get("unresolved_reasons"):
        lines.append("- None")
    lines.extend(["", "## Evidence references", "", *(f"- `{x}`" for x in record["source_artifacts"].values())])
    if not record["source_artifacts"]:
        lines.append("- None")
    lines.extend(["", "## Contracts", "", f"- Record: `{record['record_contract']} {record['record_contract_version']}`",
                  f"- Snapshot: `{result['snapshot_contract_version']}`",
                  f"- Change attribution: `{result['change_attribution_contract_version']}`", ""])
    return "\n".join(lines).encode("utf-8")


def persist_comparison(directory: str | Path, baseline: dict[str, Any], candidate: dict[str, Any], *,
                       source_artifacts: dict[str, str] | None = None,
                       created_at_utc: str | None = None) -> dict[str, Any]:
    """Persist a compact, content-addressed record and report, idempotently."""
    comparison = compare_audits(baseline, candidate)
    refs = dict(sorted((source_artifacts or {}).items()))
    required_refs = {"baseline_run", "baseline_manifest", "candidate_run", "candidate_manifest"}
    if not required_refs <= refs.keys() or any(not isinstance(key, str) or not key.strip() or not isinstance(value, str) or not value.strip() for key, value in refs.items()):
        raise ComparisonError("EVIDENCE_REFERENCE_INVALID", "baseline and candidate run/manifest paths are required")
    def resolve_ref(value: str) -> Path:
        reference = Path(value)
        return (reference if reference.is_absolute() else Path(directory) / reference).resolve()
    for side in ("baseline", "candidate"):
        run_ref = resolve_ref(refs[f"{side}_run"])
        manifest_ref = resolve_ref(refs[f"{side}_manifest"])
        if not run_ref.is_dir() or not manifest_ref.is_file() or not manifest_ref.is_relative_to(run_ref):
            raise ComparisonError("EVIDENCE_REFERENCE_INVALID", f"{side} run/manifest references are unavailable or unrelated")
    comparison_id = comparison["comparison_id"]
    payload = {"comparison_id": comparison_id, "baseline_audit_id": baseline["audit_id"],
               "candidate_audit_id": candidate["audit_id"], "comparison": comparison,
               "source_artifacts": refs}
    record = {**payload, "record_contract": RECORD_CONTRACT, "record_contract_version": RECORD_CONTRACT_VERSION,
              "created_at_utc": created_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")}
    record["integrity"] = {"baseline_snapshot_sha256": _digest(baseline),
                           "candidate_snapshot_sha256": _digest(candidate),
                           "comparison_payload_sha256": _digest(payload),
                           "record_sha256": _digest(record)}
    folder = Path(directory) / "reports" / "evidence" / "comparisons" / comparison_id
    json_path, report_path = folder / "comparison.json", folder / "report.md"
    data = _canonical_bytes(record)
    report = render_comparison_report(record)
    try:
        folder.mkdir(parents=True, exist_ok=True)
        if json_path.exists():
            existing = json_path.read_bytes()
            try:
                old = json.loads(existing.decode("utf-8"))
                old_payload = {key: old[key] for key in payload}
                old_integrity = old["integrity"]
                if old["record_contract"] != RECORD_CONTRACT or old["record_contract_version"] != RECORD_CONTRACT_VERSION or existing != _canonical_bytes(old):
                    raise ComparisonError("COMPARISON_RECORD_INVALID", comparison_id)
                if old_integrity["comparison_payload_sha256"] != _digest(old_payload):
                    raise ComparisonError("COMPARISON_HASH_MISMATCH", comparison_id)
                if old_integrity["record_sha256"] != _digest({key: value for key, value in old.items() if key != "integrity"}):
                    raise ComparisonError("COMPARISON_HASH_MISMATCH", comparison_id)
            except (KeyError, TypeError, ValueError, UnicodeError) as exc:
                if isinstance(exc, ComparisonError):
                    raise
                raise ComparisonError("COMPARISON_RECORD_INVALID", comparison_id) from exc
            if any(old_integrity[key] != record["integrity"][key] for key in ("baseline_snapshot_sha256", "candidate_snapshot_sha256", "comparison_payload_sha256")) or old_payload != payload:
                raise ComparisonError("COMPARISON_RECORD_CONFLICT", comparison_id)
            # The creation time belongs to the first successful write.
            data = existing
            old_report = render_comparison_report(old)
            if old_report != report:
                raise ComparisonError("COMPARISON_RECORD_CONFLICT", comparison_id)
            report = old_report
        else:
            fd, tmp_name = tempfile.mkstemp(prefix=".comparison-", dir=folder)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(data); stream.flush(); os.fsync(stream.fileno())
                try:
                    os.link(tmp_name, json_path)
                except FileExistsError:
                    raise ComparisonError("COMPARISON_RECORD_CONFLICT", comparison_id)
            finally:
                if os.path.exists(tmp_name): os.unlink(tmp_name)
        if report_path.exists() and report_path.read_bytes() != report:
            raise ComparisonError("COMPARISON_RECORD_CONFLICT", comparison_id)
        if not report_path.exists():
            report_path.write_bytes(report)
    except ComparisonError:
        raise
    except OSError as exc:
        raise ComparisonError("WRITE_FAILED", str(exc)) from exc
    return {"record": json.loads(data.decode("utf-8")), "path": str(json_path), "report_path": str(report_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two persisted GTFS_Lab audit runs (read-only).")
    parser.add_argument("baseline", type=Path, help="persisted baseline run directory")
    parser.add_argument("candidate", type=Path, help="persisted candidate run directory")
    parser.add_argument("--persist", type=Path, help="persist JSON and Markdown under this evidence root")
    args = parser.parse_args()
    try:
        if args.persist:
            result = persist_comparison(args.persist, build_audit_snapshot(args.baseline), build_audit_snapshot(args.candidate),
                                        source_artifacts={"baseline_run": str(args.baseline.resolve()), "baseline_manifest": str((args.baseline / "audit" / "audit_manifest.json").resolve()),
                                                          "candidate_run": str(args.candidate.resolve()), "candidate_manifest": str((args.candidate / "audit" / "audit_manifest.json").resolve())})["record"]["comparison"]
        else:
            result = compare_audit_directories(args.baseline, args.candidate)
    except ComparisonError as exc:
        print(json.dumps({"error": exc.code, "message": str(exc)}, ensure_ascii=False, sort_keys=True, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result["comparability"]["status"] != "NOT_COMPARABLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
