from __future__ import annotations

from typing import Any

from .audit_contract import (
    build_audit_manifest,
    normalize_finding,
    validate_audit_manifest,
)
from .core import RunContext, sha256_file, write_json


def _finding_occurrences(validation: dict[str, Any]) -> list[dict[str, Any]]:
    occurrences = [
        finding
        for rule in validation.get("rules", [])
        for finding in rule.get("findings", [])
    ]
    occurrences.extend(validation.get("findings", []))
    return occurrences


def _normalize_findings(
    occurrences: list[dict[str, Any]], *, run_id: str, dataset: dict[str, Any]
) -> tuple[list[dict[str, Any]], int]:
    unique: dict[str, dict[str, Any]] = {}
    conflicts = 0
    for source_finding in occurrences:
        finding = dict(source_finding)
        evidence = dict(finding.get("evidence") or {})
        evidence.setdefault("source_sha256", dataset["source_sha256"])
        finding["evidence"] = evidence
        normalized = normalize_finding(finding)
        comparable = dict(normalized)
        comparable.update(
            audit_id=f"TDL-{run_id}",
            run_id=run_id,
            dataset_id=dataset.get("dataset_id"),
            source_sha256=dataset["source_sha256"],
        )
        existing = unique.get(normalized["finding_id"])
        if existing is None:
            unique[normalized["finding_id"]] = comparable
        elif existing != comparable:
            conflicts += 1
    return list(unique.values()), conflicts


def persist_audit(ctx: RunContext, result: dict[str, Any]) -> dict[str, Any]:
    """Dual-write M02 audit evidence without changing any V1 payload."""
    audit_dir = ctx.work_dir / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    source_hash_after = sha256_file(ctx.source_zip)
    expected_hash = ctx.dataset.source_sha256
    integrity_verified = source_hash_after == expected_hash
    rules = result["validation"].get("rules", [])
    executed_rule_versions = {
        str(rule["rule_id"]): str(rule["version"])
        for rule in rules
        if rule.get("rule_id") and rule.get("version")
    }
    rule_versions = sorted(set(executed_rule_versions.values()))
    rule_ids = sorted({str(rule["rule_id"]) for rule in rules if rule.get("rule_id")})
    executed_scopes = sorted({str(rule["scope"]) for rule in rules if rule.get("scope")})
    occurrences = _finding_occurrences(result["validation"])
    normalized, conflicts = _normalize_findings(
        occurrences, run_id=ctx.run_id, dataset=result["dataset"]
    )
    unique_count = len(normalized)
    reconciliation = {
        "source_finding_occurrences": len(occurrences),
        "normalized_unique_findings": unique_count,
        "identical_duplicates_collapsed": len(occurrences) - unique_count - conflicts,
        "conflicting_duplicates": conflicts,
    }
    normalized_payload = {
        "status": "ACCEPTED" if conflicts == 0 else "REJECTED_CONFLICTING_DUPLICATES",
        "audit_id": f"TDL-{ctx.run_id}",
        "run_id": ctx.run_id,
        "dataset_id": ctx.dataset.dataset_id,
        "source_sha256": ctx.dataset.source_sha256,
        "reconciliation": reconciliation,
        "findings": normalized,
    }
    write_json(audit_dir / "findings.normalized.json", normalized_payload)
    if not integrity_verified or conflicts:
        return {"manifest_status": "NOT_ACCEPTED", **reconciliation}

    artifacts = {
        "run": "../run.json",
        "validation": "../validation.json",
        "analysis": "../analysis.json",
        "report": "../report.md",
        "findings_normalized": "findings.normalized.json",
    }
    export_files = sorted(path for path in (ctx.work_dir / "exports").rglob("*") if path.is_file())
    for index, path in enumerate(export_files, start=1):
        artifacts[f"gis_export_{index}"] = "../" + path.relative_to(ctx.work_dir).as_posix()
    database_path = ctx.work_dir / "dataset.duckdb"
    if database_path.is_file():
        artifacts["database"] = "../dataset.duckdb"
    ruleset_id = "gtfs-lab-v1"
    manifest = build_audit_manifest(
        run_id=ctx.run_id,
        dataset=ctx.dataset.__dict__,
        gtfs_lab_version=result["gtfs_lab_version"],
        validator_version=result["validator_version"],
        ruleset_id=ruleset_id,
        scope=executed_scopes,
        excluded=["LEGAL_CERTIFICATION", "SIRI", "GTFS_RT", "NETEX"],
        original_preserved=True,
        preservation_evidence={
            "verified": True,
            "status": "INPUT_INTEGRITY_VERIFIED",
            "method": "sha256_input_before_and_after_pipeline",
            "source_sha256": expected_hash,
            "source_sha256_after_pipeline": source_hash_after,
        },
        artifacts=artifacts,
    )
    manifest.update(
        {
            "ruleset_version": ",".join(rule_versions),
            "executed_rule_ids": rule_ids,
            "executed_rule_versions": executed_rule_versions,
            "run_outcome": dict(result["summary"]),
            "reconciliation": reconciliation,
        }
    )
    validate_audit_manifest(manifest)
    write_json(audit_dir / "audit_manifest.json", manifest)
    return {"manifest_status": "ACCEPTED", **reconciliation}
