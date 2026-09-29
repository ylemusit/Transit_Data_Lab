"""Validate a proposed development/holdout split without running validators."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ASSIGNMENTS = {"DEVELOPMENT", "HOLDOUT"}
RESULT_KEYS = {
    "finding_count", "validation_status", "validator_findings", "result_summary",
    "findings", "results", "run_id", "result", "validation", "scores",
}
TOP_LEVEL_KEYS = {
    "split_id", "split_version", "created_at_utc", "method", "selection_basis",
    "datasets", "split_sha256", "status", "review",
}
DATASET_KEYS = {
    "dataset_id", "source_sha256", "family_or_lineage", "assignment",
    "assignment_basis", "leakage_risk", "confidence",
}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class SplitGateError(ValueError):
    pass


def canonical_split_sha(datasets: list[dict[str, Any]]) -> str:
    identity = [
        {
            "dataset_id": row["dataset_id"],
            "source_sha256": row["source_sha256"].lower(),
            "family_or_lineage": row["family_or_lineage"],
            "assignment": row["assignment"],
        }
        for row in sorted(datasets, key=lambda item: item["dataset_id"])
    ]
    payload = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key, child
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def validate_split(inventory: dict[str, Any], split: dict[str, Any], lineage_review: dict[str, Any]) -> str:
    for path, key, value in _walk(split):
        if key.lower() in RESULT_KEYS:
            raise SplitGateError(f"result leakage field: {path}.{key}")
        if isinstance(value, str) and (Path(value).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", value)):
            raise SplitGateError(f"absolute path forbidden: {path}.{key}")
    required_top = TOP_LEVEL_KEYS - {"status", "review"}
    if required_top - set(split):
        raise SplitGateError("split contract fields missing")
    if set(split) - TOP_LEVEL_KEYS:
        raise SplitGateError("unknown split contract fields")
    if split.get("split_version") != "1.0.0":
        raise SplitGateError("unknown split contract version")
    if split.get("status") != "UNDER_REVIEW":
        raise SplitGateError("status must be UNDER_REVIEW")
    if split.get("review") != {}:
        raise SplitGateError("review must be empty while under review")

    datasets = split.get("datasets")
    if not isinstance(datasets, list):
        raise SplitGateError("datasets must be a list")
    expected = {row["dataset_id"]: row for row in inventory.get("datasets", [])}
    if inventory.get("dataset_count") != len(expected):
        raise SplitGateError("inventory dataset_count mismatch")
    seen: set[str] = set()
    assignments: dict[str, str] = {}
    lineages: dict[str, str] = {}
    hash_assignments: dict[str, str] = {}

    for row in datasets:
        if set(row) - DATASET_KEYS:
            raise SplitGateError("unknown dataset contract fields")
        dataset_id = row.get("dataset_id")
        if dataset_id not in expected:
            raise SplitGateError(f"unknown dataset: {dataset_id}")
        if dataset_id in seen:
            raise SplitGateError(f"duplicate dataset: {dataset_id}")
        seen.add(dataset_id)
        assignment = row.get("assignment")
        if assignment not in ASSIGNMENTS:
            raise SplitGateError(f"invalid assignment for dataset {dataset_id}")
        source_hash = str(row.get("source_sha256", "")).lower()
        if not HEX_SHA256.fullmatch(source_hash) or source_hash != expected[dataset_id].get("zip_sha256", "").lower():
            raise SplitGateError(f"source hash mismatch for dataset {dataset_id}")
        lineage = row.get("family_or_lineage")
        if not isinstance(lineage, str) or not lineage.strip():
            raise SplitGateError(f"missing lineage for dataset {dataset_id}")
        if lineage in lineages and lineages[lineage] != assignment:
            raise SplitGateError(f"lineage split across assignments: {lineage}")
        lineages[lineage] = assignment
        if source_hash in hash_assignments and hash_assignments[source_hash] != assignment:
            raise SplitGateError(f"duplicate source hash across assignments: {source_hash}")
        hash_assignments[source_hash] = assignment
        assignments[dataset_id] = assignment

    missing = sorted(set(expected) - seen)
    if missing:
        raise SplitGateError(f"missing datasets: {','.join(missing)}")

    pair_decisions = {
        tuple(sorted((row["dataset_a"], row["dataset_b"]))): row["can_be_opposite_split_sides"]
        for row in lineage_review.get("pairs", [])
    }
    for relation in inventory.get("structural_relationships", []):
        a, b = relation["dataset_ids"]
        if assignments[a] != assignments[b]:
            decision = pair_decisions.get(tuple(sorted((a, b))))
            if relation.get("exact_zip_duplicate") or decision == "NO":
                raise SplitGateError(f"source lineage prevents opposite assignments: {a},{b}")
            if decision != "YES":
                raise SplitGateError(f"lineage decision unresolved across assignments: {a},{b}")

    if split.get("split_sha256") != canonical_split_sha(datasets):
        raise SplitGateError("split_sha256 mismatch")
    return "TDL_CORPUS_SPLIT_GATE_PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--split", type=Path, required=True)
    parser.add_argument("--lineage-review", type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    split = json.loads(args.split.read_text(encoding="utf-8"))
    lineage_review = json.loads(args.lineage_review.read_text(encoding="utf-8"))
    try:
        print(validate_split(inventory, split, lineage_review))
    except SplitGateError as exc:
        print(f"TDL_CORPUS_SPLIT_GATE_FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
