import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gtfs_lab"))
from corpus_provenance import validate


def fixture():
    datasets = [
        {"dataset_id": f"{i:03}", "evidence_sources": [{"type": "LOCAL_METADATA_FILE", "path": "metadata.json"}],
         "provenance_confidence": "UNKNOWN", "timestamp_semantics": "UNKNOWN", "capture_date": "UNKNOWN"}
        for i in range(1, 21)
    ]
    pairs = [
        {"dataset_a": f"{i:03}", "dataset_b": f"{i + 1:03}", "classification": "UNRESOLVED",
         "confidence": "UNKNOWN", "independence_decision": "UNRESOLVED",
         "can_be_opposite_split_sides": "UNRESOLVED", "reason": "Evidence insufficient."}
        for i in range(1, 30)
    ]
    return {"dataset_count": 20, "datasets": datasets}, {"baseline_pair_count": 28,
        "baseline_pairs": ["-".join(sorted((p["dataset_a"], p["dataset_b"]))) for p in pairs[:28]],
        "pair_count": 29, "pairs": pairs}


class ProvenanceGateTests(unittest.TestCase):
    def test_accepts_complete_unknowns_and_unresolved_pairs(self):
        self.assertEqual(validate(*fixture()), [])

    def test_rejects_capture_date_inferred_from_filename(self):
        p, r = fixture()
        p["datasets"][0]["capture_date"] = "2025-10-29"
        p["datasets"][0]["evidence_sources"] = [{"type": "FILENAME_PATTERN"}]
        self.assertTrue(any("inferred from filename" in e for e in validate(p, r)))

    def test_rejects_relation_independent_without_basis(self):
        p, r = fixture()
        r["pairs"][0].update(classification="INDEPENDENT", independence_decision="YES", reason="")
        self.assertTrue(any("lacks basis" in e for e in validate(p, r)))

    def test_rejects_validator_output(self):
        p, r = fixture()
        p["datasets"][0]["finding_count"] = 2
        self.assertTrue(any("validator output" in e for e in validate(p, r)))

    def test_rejects_omitted_dataset(self):
        p, r = fixture()
        p["datasets"].pop()
        p["dataset_count"] = 19
        self.assertTrue(any("20 unique datasets" in e for e in validate(p, r)))

    def test_rejects_missing_original_relationship_pair(self):
        p, r = fixture()
        r["baseline_pairs"].pop()
        r["baseline_pair_count"] = 27
        self.assertTrue(any("28 original" in e for e in validate(p, r)))

    def test_rejects_absolute_paths(self):
        p, r = fixture()
        p["datasets"][0]["evidence_sources"][0]["path"] = "C:/private/feed.zip"
        self.assertTrue(any("absolute path" in e for e in validate(p, r)))


if __name__ == "__main__":
    unittest.main()
