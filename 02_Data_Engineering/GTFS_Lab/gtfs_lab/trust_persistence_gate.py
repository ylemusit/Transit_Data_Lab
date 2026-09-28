from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .audit_contract import stable_finding_id, validate_audit_manifest
from .audit_persistence import _normalize_findings
from .core import sha256_file
from .gate import create_fixtures
from .ingestion import IngestionError, load_dataset
from .pipeline import record_ingestion_error, run


def run_gate(output: Path, protected_paths: list[Path] | None = None) -> dict[str, Any]:
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    protected_paths = protected_paths or []
    before = {str(path.resolve()): sha256_file(path.resolve()) for path in protected_paths}
    fixtures = create_fixtures(output / "fixtures")
    result = run(fixtures["ORPHAN_TRIP"], output / "runs")
    run_dir = output / "runs" / result["run_id"]
    manifest_path = run_dir / "audit" / "audit_manifest.json"
    findings_path = run_dir / "audit" / "findings.normalized.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    normalized = json.loads(findings_path.read_text(encoding="utf-8"))
    validate_audit_manifest(manifest)
    disk_run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    disk_validation = json.loads((run_dir / "validation.json").read_text(encoding="utf-8"))
    source_hash = sha256_file(fixtures["ORPHAN_TRIP"])
    declared_artifacts_exist = all((run_dir / "audit" / rel).resolve().exists() for rel in manifest["artifacts"].values())
    linkage_ok = all(
        item["audit_id"] == manifest["audit_id"]
        and item["run_id"] == manifest["run_id"]
        and item["dataset_id"] == manifest["dataset_id"]
        and item["source_sha256"] == manifest["source_sha256"]
        for item in normalized["findings"]
    )
    ids_v1 = [item["finding_id"] for item in normalized["findings"]]
    result2 = run(fixtures["ORPHAN_TRIP"], output / "repeat")
    repeat = json.loads(
        (output / "repeat" / result2["run_id"] / "audit" / "findings.normalized.json").read_text(encoding="utf-8")
    )
    stable_ids = ids_v1 == [item["finding_id"] for item in repeat["findings"]]
    source_finding = normalized["findings"][0]
    distinct_dataset_id = stable_finding_id(source_finding) != stable_finding_id(
        {**source_finding, "evidence": {**source_finding.get("evidence", {}), "source_sha256": "0" * 64 if source_hash != "0" * 64 else "1" * 64}}
    )

    unique, conflicts = _normalize_findings(
        [source_finding, dict(source_finding)], run_id=result["run_id"], dataset=result["dataset"]
    )
    conflict_copy = dict(source_finding)
    conflict_copy["technical_message"] = "conflicting synthetic representation"
    conflicted, conflict_count = _normalize_findings(
        [source_finding, conflict_copy], run_id=result["run_id"], dataset=result["dataset"]
    )
    different_dataset = load_dataset(fixtures["ORPHAN_STOP"], output / "different_dataset")

    error_root = output / "ingestion_error"
    error_result = record_ingestion_error(fixtures["MALFORMED_CSV"], error_root, IngestionError("synthetic malformed input"))
    error_dir = error_root / error_result["run_id"]
    error_manifest_absent = not (error_dir / "audit" / "audit_manifest.json").exists()
    error_state_correct = error_result["ingestion"]["status"] == "INGESTION_ERROR" and error_manifest_absent
    dataset_fields_match = all(
        disk_run["dataset"].get(run_key) == manifest.get(manifest_key)
        for run_key, manifest_key in (
            ("dataset_id", "dataset_id"),
            ("source_filename", "source_filename"),
            ("source_sha256", "source_sha256"),
            ("ingestion_timestamp_utc", "dataset_ingestion_timestamp_utc"),
            ("parser_version", "parser_version"),
            ("gtfs_lab_version", "gtfs_lab_version"),
        )
    )
    disk_analysis = json.loads((run_dir / "analysis.json").read_text(encoding="utf-8"))
    v1_unchanged = (
        disk_run == result
        and disk_run["run_id"] == manifest["run_id"]
        and dataset_fields_match
        and disk_validation == result["validation"]
        and disk_analysis == result["analysis"]
        and (run_dir / "analysis.json").is_file()
        and (run_dir / "report.md").is_file()
        and (run_dir / "exports").is_dir()
        and (run_dir / "dataset.duckdb").is_file()
    )
    after = {str(path.resolve()): sha256_file(path.resolve()) for path in protected_paths}
    checks = {
        "synthetic_completed_run_persists_manifest": manifest.get("run_id") == result["run_id"],
        "manifest_validates_m01_contract": True,
        "source_hash_matches": manifest["source_sha256"] == source_hash,
        "dataset_and_run_identity_match": manifest["dataset_id"] == disk_run["dataset"]["dataset_id"] and manifest["run_id"] == disk_run["run_id"],
        "executed_versions_and_rules_present": bool(manifest.get("ruleset_version")) and manifest.get("executed_rule_versions") == {x["rule_id"]: x["version"] for x in disk_validation["rules"]} and set(manifest.get("executed_rule_ids", [])) == {x["rule_id"] for x in disk_validation["rules"]},
        "run_outcome_derived_from_pipeline": manifest.get("run_outcome") == disk_run.get("summary"),
        "input_integrity_evidence_matches": manifest["preservation_evidence"].get("status") == "INPUT_INTEGRITY_VERIFIED" and manifest["preservation_evidence"].get("source_sha256_after_pipeline") == source_hash,
        "declared_artifacts_exist": declared_artifacts_exist,
        "normalization_reproducible_and_linked": normalized["status"] == "ACCEPTED" and linkage_ok and stable_ids,
        "identical_duplicates_reconciled": conflicts == 0 and len(unique) == 1,
        "conflicting_duplicates_rejected": conflict_count > 0 and len(conflicted) == 1,
        "ingestion_error_has_no_manifest": error_state_correct,
        "different_source_hash_changes_finding_identity": distinct_dataset_id,
        "different_dataset_produces_distinct_identity": different_dataset.dataset.dataset_id != result["dataset"]["dataset_id"],
        "v1_outputs_remain_present_and_contractually_intact": v1_unchanged,
        "protected_hashes_unchanged": before == after,
    }
    gate = {
        "gate": "TDL_TRUST_PERSISTENCE_GATE",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": [{"check": name, "status": "PASS" if passed else "FAIL"} for name, passed in checks.items()],
        "manifest_example": str(manifest_path),
        "findings_reconciliation": normalized["reconciliation"],
        "protected_hashes_before": before,
        "protected_hashes_after": after,
    }
    (output / "gate.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return gate


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("runs/trust_persistence_gate"))
    parser.add_argument("--protect", type=Path, action="append", default=[])
    args = parser.parse_args()
    result = run_gate(args.output, args.protect)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
