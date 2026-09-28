from __future__ import annotations

import json
import os
import tempfile
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
) -> tuple[list[dict[str, Any]], int, int]:
    unique: dict[str, dict[str, Any]] = {}
    conflicts = 0
    source_mismatches = 0
    for source_finding in occurrences:
        finding = dict(source_finding)
        evidence = dict(finding.get("evidence") or {})
        source_hash = evidence.get("source_sha256")
        if source_hash is not None and str(source_hash).lower() != str(dataset["source_sha256"]).lower():
            source_mismatches += 1
            continue
        evidence["source_sha256"] = dataset["source_sha256"]
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
    return list(unique.values()), conflicts, source_mismatches


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
    normalized, conflicts, source_mismatches = _normalize_findings(
        occurrences, run_id=ctx.run_id, dataset=result["dataset"]
    )
    unique_count = len(normalized)
    reconciliation = {
        "source_finding_occurrences": len(occurrences),
        "normalized_unique_findings": unique_count,
        "identical_duplicates_collapsed": len(occurrences) - unique_count - conflicts - source_mismatches,
        "conflicting_duplicates": conflicts,
        "rejected_source_mismatch_occurrences": source_mismatches,
    }
    normalized_payload = {
        "status": (
            "NORMALIZED"
            if integrity_verified and conflicts == 0 and source_mismatches == 0
            else "REJECTED_CONFLICTING_DUPLICATES"
            if conflicts
            else "REJECTED_FINDING_SOURCE_MISMATCH"
            if source_mismatches
            else "REJECTED_INPUT_INTEGRITY"
        ),
        "audit_id": f"TDL-{ctx.run_id}",
        "run_id": ctx.run_id,
        "dataset_id": ctx.dataset.dataset_id,
        "source_sha256": ctx.dataset.source_sha256,
        "reconciliation": reconciliation,
        "findings": normalized,
    }
    write_json(audit_dir / "findings.normalized.json", normalized_payload)
    if not integrity_verified or conflicts or source_mismatches:
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
    missing_artifacts = [
        reference
        for reference in artifacts.values()
        if not (audit_dir / reference).resolve().is_file()
    ]
    if missing_artifacts:
        raise RuntimeError(f"audit artifacts are missing before manifest commit: {missing_artifacts}")
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
    manifest_path = audit_dir / "audit_manifest.json"
    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=audit_dir,
            prefix=".audit_manifest.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = temporary.name
            temporary.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        with open(temporary_path, "r", encoding="utf-8") as persisted:
            validate_audit_manifest(json.load(persisted))
        os.replace(temporary_path, manifest_path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
    return {"manifest_status": "ACCEPTED", **reconciliation}
