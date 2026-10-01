"""Run GTFS Audit Engine V1 against only the frozen DEVELOPMENT corpus split."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from .corpus_split_gate import validate_split

def _run_isolated(source: Path, work_root: Path) -> dict[str, Any]:
    """Run exactly one dataset in a child process so process state cannot accumulate."""
    output = work_root / "runs"
    result_path = work_root / "result.json"
    process = subprocess.run(
        [sys.executable, "-m", "gtfs_lab.g10_worker", "--source", str(source),
         "--output", str(output), "--result", str(result_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr[-3000:] or f"G10 worker exited {process.returncode}")
    return json.loads(result_path.read_text(encoding="utf-8"))


def build_cross_dataset_comparison(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-run status and finding counts without reading source feeds."""
    completed = [row for row in records if row.get("execution_status") == "COMPLETED"]
    comparison: dict[str, Any] = {"stage_status_counts": {}, "rule_status_counts": {},
                                  "finding_counts_by_rule": {}}
    for stage in ("g03", "g04", "g05", "g06", "g07", "g08"):
        comparison["stage_status_counts"][stage] = dict(sorted(Counter(
            row.get("stages", {}).get(stage, {}).get("status", "NOT_EVALUABLE")
            for row in completed
        ).items()))
    rule_statuses: dict[str, Counter] = {}
    finding_counts: Counter = Counter()
    for dataset in completed:
        for stage in dataset.get("stages", {}).values():
            for rule in stage.get("rules", []):
                rule_id = rule.get("rule_id", "UNKNOWN_RULE")
                rule_statuses.setdefault(rule_id, Counter())[rule.get("status", "NOT_EVALUABLE")] += 1
            finding_counts.update(stage.get("finding_counts_by_rule", {}))
    comparison["rule_status_counts"] = {
        rule_id: dict(sorted(counts.items())) for rule_id, counts in sorted(rule_statuses.items())
    }
    comparison["finding_counts_by_rule"] = dict(sorted(finding_counts.items()))
    return comparison


def evaluate_development_corpus(
    *, inventory_path: Path, split_path: Path, lineage_review_path: Path, source_root: Path,
) -> dict[str, Any]:
    """Hash-check and evaluate DEVELOPMENT members; HOLDOUT paths are never opened."""
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    split = json.loads(split_path.read_text(encoding="utf-8"))
    lineage_review = json.loads(lineage_review_path.read_text(encoding="utf-8"))
    validate_split(inventory, split, lineage_review)
    development_ids = sorted(
        row["dataset_id"] for row in split.get("datasets", [])
        if row.get("assignment") == "DEVELOPMENT"
    )
    metadata = {row["dataset_id"]: row for row in inventory.get("datasets", [])}
    if not development_ids or any(dataset_id not in metadata for dataset_id in development_ids):
        raise ValueError("DEVELOPMENT split does not match corpus inventory")
    root = source_root.resolve(strict=True)
    records: list[dict[str, Any]] = []
    for dataset_id in development_ids:
        item = metadata[dataset_id]
        source = (root / item["zip_relative_path"]).resolve()
        if not source.is_relative_to(root):
            raise ValueError(f"DEVELOPMENT path escapes source root: {dataset_id}")
        if not source.is_file():
            raise FileNotFoundError(f"DEVELOPMENT dataset missing: {dataset_id}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        expected = str(item["zip_sha256"]).lower()
        if digest != expected:
            raise ValueError(f"DEVELOPMENT hash mismatch: {dataset_id}")
        started = time.perf_counter()
        try:
            with tempfile.TemporaryDirectory(prefix=f"gtfs-audit-g10-{dataset_id}-") as temporary:
                result = _run_isolated(source, Path(temporary))
            records.append({"dataset_id": dataset_id, "source_sha256": digest,
                            "execution_status": "COMPLETED",
                            "duration_seconds": round(time.perf_counter() - started, 3), **result})
        except Exception as exc:  # capture one corpus failure without losing prior records
            records.append({"dataset_id": dataset_id, "source_sha256": digest,
                            "execution_status": "PIPELINE_ERROR",
                            "duration_seconds": round(time.perf_counter() - started, 3),
                            "error_type": type(exc).__name__, "error": str(exc)})
    completed = [row for row in records if row["execution_status"] == "COMPLETED"]
    comparison = build_cross_dataset_comparison(records)
    stability: dict[str, Any] = {"status": "NOT_RUN"}
    if completed:
        first_id = completed[0]["dataset_id"]
        first_metadata = metadata[first_id]
        first_source = (root / first_metadata["zip_relative_path"]).resolve()
        first_hash = hashlib.sha256(first_source.read_bytes()).hexdigest()
        try:
            with tempfile.TemporaryDirectory(prefix=f"gtfs-audit-g10-stability-{first_id}-") as temporary:
                repeated = _run_isolated(first_source, Path(temporary))
            same = (first_hash == completed[0]["source_sha256"]
                    and repeated["engine_report_sha256"] == completed[0].get("engine_report_sha256"))
            stability = {"status": "PASS" if same else "FAIL", "dataset_id": first_id,
                         "engine_report_sha256": repeated.get("engine_report_sha256")}
        except Exception as exc:
            stability = {"status": "FAIL", "dataset_id": first_id,
                         "error_type": type(exc).__name__, "error": str(exc)}
    failed_count = sum(row["execution_status"] != "COMPLETED" for row in records)
    return {
        "schema_version": "1.0.0",
        "gate": "GTFS_AUDIT_ENGINE_V1_G10_DEVELOPMENT",
        "corpus_execution_status": "COMPLETED" if failed_count == 0 else "PARTIAL",
        "split_id": split.get("split_id"),
        "split_sha256": split.get("split_sha256"),
        "inventory_version": inventory.get("inventory_version"),
        "scope": "DEVELOPMENT_ONLY",
        "holdout_accessed": False,
        "expected_dataset_count": len(development_ids),
        "completed_dataset_count": sum(row["execution_status"] == "COMPLETED" for row in records),
        "failed_dataset_count": failed_count,
        "stability_check": stability,
        "cross_dataset_comparison": comparison,
        "datasets": records,
        "operator_specific_code_changes": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--split", type=Path, required=True)
    parser.add_argument("--lineage-review", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = evaluate_development_corpus(
        inventory_path=args.inventory, split_path=args.split,
        lineage_review_path=args.lineage_review, source_root=args.source_root,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "gate", "corpus_execution_status", "scope", "expected_dataset_count", "completed_dataset_count", "failed_dataset_count", "stability_check", "holdout_accessed"
    )}, ensure_ascii=False))
    return 0 if report["failed_dataset_count"] == 0 and report["stability_check"]["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
