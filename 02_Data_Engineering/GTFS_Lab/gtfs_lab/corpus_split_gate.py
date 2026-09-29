"""Validate a proposed development/holdout split without running validators."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from .corpus_lineage_review import validate as validate_lineage_matrix


ASSIGNMENTS = {"DEVELOPMENT", "HOLDOUT"}
RESULT_KEYS = {
    "finding_count", "validation_status", "validator_findings", "result_summary",
    "findings", "results", "run_id", "runtime_id", "runtime_output", "runtime_outputs",
    "execution_output", "output_path", "result", "validation", "scores",
}
TOP_LEVEL_KEYS = {
    "split_id", "split_version", "contract_version", "created_at_utc", "method", "selection_basis",
    "datasets", "split_sha256", "status", "review",
}
DATASET_KEYS = {
    "dataset_id", "source_sha256", "family_or_lineage", "assignment",
    "assignment_basis", "leakage_risk", "confidence",
}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
KNOWN_DEVELOPMENT_EXPOSURE_IDS = {"002", "005", "014", "019", "020"}
APPROVED_HOLDOUT_IDS = {"006", "008", "013", "015", "017", "018"}
ATOMIC_LINEAGE_IDS = {"013", "015"}
APPROVED_REVIEWER = "Yeison Arbey Carrillo Lemus"


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
    if split.get("split_version") != "1.0.0" or split.get("contract_version") != "CorpusSplit 1.0.0":
        raise SplitGateError("unknown split contract version")
    status = split.get("status")
    review = split.get("review")
    if status == "UNDER_REVIEW":
        if review != {}:
            raise SplitGateError("review must be empty while under review")
    elif status == "APPROVED":
        _validate_approved_review(review)
    else:
        raise SplitGateError("status must be UNDER_REVIEW or APPROVED")

    datasets = split.get("datasets")
    if not isinstance(datasets, list):
        raise SplitGateError("datasets must be a list")
    expected = {row["dataset_id"]: row for row in inventory.get("datasets", [])}
    if inventory.get("dataset_count") != len(expected):
        raise SplitGateError("inventory dataset_count mismatch")
    if status == "APPROVED" and (inventory.get("dataset_count") != 20 or len(expected) != 20):
        raise SplitGateError("approved split requires exactly 20 inventory datasets")
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
        if status == "APPROVED":
            expected_lineage = "LINEAGE-013-015" if dataset_id in ATOMIC_LINEAGE_IDS else f"DATASET-{dataset_id}"
            if lineage != expected_lineage:
                raise SplitGateError(f"approved lineage identity mismatch for dataset {dataset_id}")
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
    if status == "APPROVED":
        validate_persisted_lineage_review(lineage_review)
        _validate_approved_allocation(inventory, split, assignments, pair_decisions)
    for relation in inventory.get("structural_relationships", []):
        a, b = relation["dataset_ids"]
        if assignments[a] != assignments[b]:
            decision = pair_decisions.get(tuple(sorted((a, b))))
            if relation.get("exact_zip_duplicate") or decision == "NO":
                raise SplitGateError(f"source lineage prevents opposite assignments: {a},{b}")
            if decision != "YES":
                raise SplitGateError(f"lineage decision unresolved across assignments: {a},{b}")
    for pair, decision in pair_decisions.items():
        a, b = pair
        if decision == "NO" and a in assignments and b in assignments and assignments[a] != assignments[b]:
            raise SplitGateError(f"source lineage prevents opposite assignments: {a},{b}")

    if split.get("split_sha256") != canonical_split_sha(datasets):
        raise SplitGateError("split_sha256 mismatch")
    return "TDL_CORPUS_SPLIT_GATE_PASS"


def _validate_approved_review(review: Any) -> None:
    required = {"reviewed_by", "reviewed_at_utc", "review_basis"}
    if not isinstance(review, dict) or set(review) != required:
        raise SplitGateError("approved review must contain reviewed_by, reviewed_at_utc, and review_basis")
    if review.get("reviewed_by") != APPROVED_REVIEWER:
        raise SplitGateError("approved reviewer does not match the recorded human decision")
    timestamp = review.get("reviewed_at_utc")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise SplitGateError("reviewed_at_utc must be a UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(timestamp[:-1] + "+00:00")
    except ValueError as exc:
        raise SplitGateError("reviewed_at_utc must be a valid ISO-8601 UTC timestamp") from exc
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise SplitGateError("reviewed_at_utc must be UTC")
    basis = review.get("review_basis")
    required_basis = (
        "USE_6_DATASET_5_LINEAGE_SPLIT", "6 datasets HOLDOUT",
        "5 unidades lineage independientes", "14 DEVELOPMENT", "013/015",
        "unidad atómica", "provenance", "exposición previa",
    )
    if not isinstance(basis, str) or any(token.casefold() not in basis.casefold() for token in required_basis):
        raise SplitGateError("review_basis does not record all approved split trade-offs")


def _validate_approved_allocation(
    inventory: dict[str, Any],
    split: dict[str, Any],
    assignments: dict[str, str],
    pair_decisions: dict[tuple[str, str], str],
) -> None:
    holdout = {dataset_id for dataset_id, assignment in assignments.items() if assignment == "HOLDOUT"}
    development = set(assignments) - holdout
    if holdout & KNOWN_DEVELOPMENT_EXPOSURE_IDS:
        raise SplitGateError("known-development-exposure dataset cannot be in approved HOLDOUT")
    if holdout != APPROVED_HOLDOUT_IDS:
        raise SplitGateError("approved HOLDOUT must be exactly 006,008,013,015,017,018")
    if len(development) != 14 or len(holdout) != 6:
        raise SplitGateError("approved split must contain 14 DEVELOPMENT and 6 HOLDOUT datasets")
    if not ATOMIC_LINEAGE_IDS <= holdout:
        raise SplitGateError("approved HOLDOUT must keep lineage 013/015 together")
    if pair_decisions.get(("013", "015")) != "NO":
        raise SplitGateError("approved HOLDOUT requires the persisted NO lineage decision for 013/015")
    if any(decision == "UNRESOLVED" for decision in pair_decisions.values()):
        raise SplitGateError("approved split requires zero unresolved lineage decisions")
    lineage_units = {
        next(row["family_or_lineage"] for row in split["datasets"] if row["dataset_id"] == dataset_id)
        for dataset_id in holdout
    }
    if len(lineage_units) != 5:
        raise SplitGateError("approved HOLDOUT must contain exactly 5 lineage units")
    inventory_rows = {row["dataset_id"]: row for row in inventory["datasets"]}
    families = {inventory_rows[dataset_id].get("family", "").replace("FAMILY_", "")[0] for dataset_id in holdout}
    if not set("ABCD") <= families:
        raise SplitGateError("approved HOLDOUT must cover families A, B, C, and D")


def validate_persisted_lineage_review(lineage_review: dict[str, Any]) -> str:
    """Validate the persisted M04-A2 decision matrix without rebuilding it from source archives."""
    if lineage_review.get("schema_version") != "1.0.0" or lineage_review.get("review") != "M04-A2":
        raise SplitGateError("lineage review contract identity is invalid")
    contract_errors = validate_lineage_matrix(lineage_review)
    if contract_errors:
        raise SplitGateError("lineage review contract invalid: " + "; ".join(contract_errors))
    pair_decisions: dict[tuple[str, str], str] = {}
    for row in lineage_review.get("pairs", []):
        pair = tuple(sorted((row.get("dataset_a"), row.get("dataset_b"))))
        decision = row.get("can_be_opposite_split_sides")
        if None in pair or pair in pair_decisions:
            raise SplitGateError("lineage review has missing or duplicate pair identity")
        if decision not in {"YES", "NO", "UNRESOLVED"}:
            raise SplitGateError("lineage review has an invalid split decision")
        pair_decisions[pair] = decision
    if lineage_review.get("pair_count") != len(pair_decisions) or len(pair_decisions) != 29:
        raise SplitGateError("lineage review must contain the 29 persisted pair decisions")
    counts = {value: sum(decision == value for decision in pair_decisions.values()) for value in ("YES", "NO", "UNRESOLVED")}
    if lineage_review.get("counts") != counts:
        raise SplitGateError("lineage review counts do not match persisted pair decisions")
    blocking = sorted(row["pair_id"] for row in lineage_review["pairs"] if row["can_be_opposite_split_sides"] != "YES")
    if lineage_review.get("blocking_pairs") != blocking:
        raise SplitGateError("lineage review blocking_pairs do not match persisted decisions")
    if pair_decisions.get(("013", "015")) != "NO":
        raise SplitGateError("lineage review must keep 013/015 as a NO pair")
    if any(decision == "UNRESOLVED" for decision in pair_decisions.values()):
        raise SplitGateError("lineage review contains unresolved decisions")
    return "M04A2_LINEAGE_REVIEW_PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--split", type=Path)
    parser.add_argument("--lineage-review", type=Path, required=True)
    parser.add_argument("--lineage-review-only", action="store_true")
    args = parser.parse_args()
    lineage_review = json.loads(args.lineage_review.read_text(encoding="utf-8"))
    if args.lineage_review_only:
        try:
            print(validate_persisted_lineage_review(lineage_review))
        except SplitGateError as exc:
            print(f"M04A2_LINEAGE_REVIEW_FAIL: {exc}")
            return 1
        return 0
    if args.inventory is None or args.split is None:
        parser.error("--inventory and --split are required unless --lineage-review-only is set")
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    split = json.loads(args.split.read_text(encoding="utf-8"))
    try:
        print(validate_split(inventory, split, lineage_review))
    except SplitGateError as exc:
        print(f"TDL_CORPUS_SPLIT_GATE_FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
