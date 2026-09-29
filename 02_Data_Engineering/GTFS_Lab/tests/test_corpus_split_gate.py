import copy
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gtfs_lab.corpus_split_gate import (
    SplitGateError,
    canonical_split_sha,
    validate_persisted_lineage_review,
    validate_split,
)


def fixture():
    inventory = {
        "dataset_count": 2,
        "datasets": [
            {"dataset_id": "001", "zip_sha256": "a" * 64},
            {"dataset_id": "002", "zip_sha256": "b" * 64},
        ],
        "structural_relationships": [],
    }
    split = {
        "split_id": "TEST",
        "split_version": "1.0.0",
        "contract_version": "CorpusSplit 1.0.0",
        "created_at_utc": "2026-09-29T00:00:00Z",
        "method": "TEST_FIXTURE",
        "selection_basis": "synthetic unit test only",
        "status": "UNDER_REVIEW",
        "review": {},
        "datasets": [
            {"dataset_id": "001", "source_sha256": "a" * 64, "family_or_lineage": "A", "assignment": "DEVELOPMENT"},
            {"dataset_id": "002", "source_sha256": "b" * 64, "family_or_lineage": "B", "assignment": "HOLDOUT"},
        ],
    }
    split["split_sha256"] = canonical_split_sha(split["datasets"])
    lineage = {"pairs": [{"dataset_a": "001", "dataset_b": "002", "can_be_opposite_split_sides": "YES"}]}
    return inventory, split, lineage


def approved_fixture():
    families = {
        **{f"{i:03d}": "FAMILY_A_SMALL_BASIC" for i in range(1, 8)},
        **{f"{i:03d}": "FAMILY_B_SME_OPERATIONAL" for i in range(8, 13)},
        **{f"{i:03d}": "FAMILY_C_COMPLEX_REGIONAL" for i in range(13, 16)},
        **{f"{i:03d}": "FAMILY_D_MATURE_BENCHMARK" for i in range(16, 21)},
    }
    holdout = {"006", "008", "013", "015", "017", "018"}
    inventory = {
        "dataset_count": 20,
        "datasets": [
            {"dataset_id": dataset_id, "zip_sha256": f"{int(dataset_id):064x}", "family": family}
            for dataset_id, family in families.items()
        ],
        "structural_relationships": [],
    }
    split_datasets = [
        {
            "dataset_id": dataset_id,
            "source_sha256": f"{int(dataset_id):064x}",
            "family_or_lineage": "LINEAGE-013-015" if dataset_id in {"013", "015"} else f"DATASET-{dataset_id}",
            "assignment": "HOLDOUT" if dataset_id in holdout else "DEVELOPMENT",
        }
        for dataset_id in families
    ]
    split = {
        "split_id": "TDL-CORPUS-SPLIT-V1",
        "split_version": "1.0.0",
        "contract_version": "CorpusSplit 1.0.0",
        "created_at_utc": "2026-09-29T00:00:00Z",
        "method": "APPROVED_TEST_FIXTURE",
        "selection_basis": "synthetic approved split fixture",
        "status": "APPROVED",
        "review": {
            "reviewed_by": "Yeison Arbey Carrillo Lemus",
            "reviewed_at_utc": "2026-09-29T12:21:55Z",
            "review_basis": (
                "Se aprueba explícitamente USE_6_DATASET_5_LINEAGE_SPLIT y se acepta: "
                "6 datasets HOLDOUT; 5 unidades lineage independientes; 14 DEVELOPMENT; "
                "013/015 como unidad atómica; y las limitaciones conocidas de provenance y exposición previa."
            ),
        },
        "datasets": split_datasets,
    }
    split["split_sha256"] = canonical_split_sha(split_datasets)
    pairs = [{
        "pair_id": "013-015", "dataset_a": "013", "dataset_b": "015",
        "source_lineage_assessment": "SAME_SOURCE_LINEAGE", "relationship_domain": "SOURCE_LINEAGE",
        "can_be_opposite_split_sides": "NO",
    }]
    for a, b in itertools.combinations(families, 2):
        if (a, b) != ("013", "015") and len(pairs) < 29:
            pairs.append({
                "pair_id": f"{a}-{b}", "dataset_a": a, "dataset_b": b,
                "source_lineage_assessment": "LIKELY_INDEPENDENT_SOURCE", "relationship_domain": "NONE",
                "can_be_opposite_split_sides": "YES",
            })
    lineage = {
        "schema_version": "1.0.0", "review": "M04-A2", "pair_count": len(pairs), "pairs": pairs,
        "counts": {"YES": 28, "NO": 1, "UNRESOLVED": 0}, "blocking_pairs": ["013-015"],
    }
    return inventory, split, lineage


class CorpusSplitGateTests(unittest.TestCase):
    def test_accepts_clean_under_review_contract(self):
        inventory, split, lineage = fixture()
        self.assertEqual(validate_split(inventory, split, lineage), "TDL_CORPUS_SPLIT_GATE_PASS")

    def test_rejects_duplicate_sha_across_sides(self):
        inventory, split, lineage = fixture()
        split["datasets"][1]["source_sha256"] = "a" * 64
        inventory["datasets"][1]["zip_sha256"] = "a" * 64
        inventory["structural_relationships"] = [{"dataset_ids": ["001", "002"], "exact_zip_duplicate": True, "shared_identifier_counts": {}}]
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "duplicate source hash")

    def test_rejects_same_lineage_across_sides(self):
        inventory, split, lineage = fixture()
        split["datasets"][1]["family_or_lineage"] = "A"
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "lineage split")

    def test_rejects_result_leakage(self):
        inventory, split, lineage = fixture()
        split["finding_count"] = 0
        self.assert_rejected(inventory, split, lineage, "result leakage")

    def test_rejects_atomic_lineage_pair_across_sides(self):
        inventory, split, lineage = fixture()
        inventory["datasets"].extend([
            {"dataset_id": "013", "zip_sha256": "c" * 64},
            {"dataset_id": "015", "zip_sha256": "d" * 64},
        ])
        inventory["dataset_count"] = 4
        split["datasets"].extend([
            {"dataset_id": "013", "source_sha256": "c" * 64, "family_or_lineage": "LINEAGE-013-015", "assignment": "DEVELOPMENT"},
            {"dataset_id": "015", "source_sha256": "d" * 64, "family_or_lineage": "LINEAGE-013-015", "assignment": "HOLDOUT"},
        ])
        inventory["structural_relationships"] = [{"dataset_ids": ["013", "015"], "exact_zip_duplicate": False, "shared_identifier_counts": {}}]
        lineage["pairs"].append({"dataset_a": "013", "dataset_b": "015", "can_be_opposite_split_sides": "NO"})
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "lineage split")

    def test_rejects_missing_dataset(self):
        inventory, split, lineage = fixture()
        split["datasets"].pop()
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "missing datasets")

    def test_rejects_duplicate_dataset(self):
        inventory, split, lineage = fixture()
        split["datasets"].append(copy.deepcopy(split["datasets"][0]))
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "duplicate dataset")

    def test_rejects_shared_structural_ids_across_sides(self):
        inventory, split, lineage = fixture()
        inventory["structural_relationships"] = [{"dataset_ids": ["001", "002"], "exact_zip_duplicate": False, "shared_identifier_counts": {"stops.txt": 1}}]
        self.assertEqual(validate_split(inventory, split, lineage), "TDL_CORPUS_SPLIT_GATE_PASS")

    def assert_rejected(self, inventory, split, lineage, message):
        with self.assertRaisesRegex(SplitGateError, message):
            validate_split(inventory, split, lineage)

    def test_rejects_strong_lineage_across_sides(self):
        inventory, split, lineage = fixture()
        inventory["structural_relationships"] = [{"dataset_ids": ["001", "002"], "exact_zip_duplicate": False, "shared_identifier_counts": {"stops.txt": 1}}]
        lineage["pairs"][0]["can_be_opposite_split_sides"] = "NO"
        self.assert_rejected(inventory, split, lineage, "source lineage prevents")

    def test_unresolved_material_lineage_cannot_cross_sides(self):
        inventory, split, lineage = fixture()
        inventory["structural_relationships"] = [{"dataset_ids": ["001", "002"], "exact_zip_duplicate": False, "shared_identifier_counts": {"trips.txt": 1}}]
        lineage["pairs"][0]["can_be_opposite_split_sides"] = "UNRESOLVED"
        self.assert_rejected(inventory, split, lineage, "lineage decision unresolved")

    def test_rejects_forged_review(self):
        inventory, split, lineage = fixture()
        split["review"] = {"reviewed_by": "forged"}
        self.assert_rejected(inventory, split, lineage, "review must be empty")

    def test_rejects_assignment_change_without_rehash(self):
        inventory, split, lineage = fixture()
        split["datasets"][0]["assignment"] = "HOLDOUT"
        self.assert_rejected(inventory, split, lineage, "split_sha256 mismatch")

    def test_accepts_approved_frozen_split_contract(self):
        inventory, split, lineage = approved_fixture()
        self.assertEqual(validate_split(inventory, split, lineage), "TDL_CORPUS_SPLIT_GATE_PASS")

    def test_persisted_lineage_gate_accepts_reviewed_matrix(self):
        _inventory, _split, lineage = approved_fixture()
        self.assertEqual(validate_persisted_lineage_review(lineage), "M04A2_LINEAGE_REVIEW_PASS")

    def test_approved_contract_rejects_known_exposure_in_holdout(self):
        inventory, split, lineage = approved_fixture()
        rows = {row["dataset_id"]: row for row in split["datasets"]}
        rows["006"]["assignment"] = "DEVELOPMENT"
        rows["002"]["assignment"] = "HOLDOUT"
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "known-development-exposure")

    def test_approved_contract_rejects_unresolved_persisted_lineage(self):
        inventory, split, lineage = approved_fixture()
        lineage["pairs"][1]["can_be_opposite_split_sides"] = "UNRESOLVED"
        lineage["counts"] = {"YES": 27, "NO": 1, "UNRESOLVED": 1}
        lineage["blocking_pairs"] = sorted(["013-015", lineage["pairs"][1]["pair_id"]])
        self.assert_rejected(inventory, split, lineage, "unresolved decisions")

    def test_approved_contract_rejects_incomplete_human_review(self):
        inventory, split, lineage = approved_fixture()
        split["review"].pop("reviewed_at_utc")
        self.assert_rejected(inventory, split, lineage, "approved review must contain")

    def test_approved_contract_requires_dataset_018_in_holdout(self):
        inventory, split, lineage = approved_fixture()
        rows = {row["dataset_id"]: row for row in split["datasets"]}
        rows["018"]["assignment"] = "DEVELOPMENT"
        rows["001"]["assignment"] = "HOLDOUT"
        split["split_sha256"] = canonical_split_sha(split["datasets"])
        self.assert_rejected(inventory, split, lineage, "approved HOLDOUT must be exactly")

    def test_approved_contract_rejects_runtime_outputs(self):
        inventory, split, lineage = approved_fixture()
        split["runtime_outputs"] = []
        self.assert_rejected(inventory, split, lineage, "result leakage")

    def test_approved_contract_rejects_absolute_paths(self):
        inventory, split, lineage = approved_fixture()
        split["source_path"] = "C:\\private\\feed.zip"
        self.assert_rejected(inventory, split, lineage, "absolute path forbidden")


if __name__ == "__main__":
    unittest.main()
