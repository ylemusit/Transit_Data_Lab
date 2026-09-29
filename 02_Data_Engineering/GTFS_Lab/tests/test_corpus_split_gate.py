import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gtfs_lab"))
from corpus_split_gate import SplitGateError, canonical_split_sha, validate_split


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


if __name__ == "__main__":
    unittest.main()
