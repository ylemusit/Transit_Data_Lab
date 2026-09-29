import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gtfs_lab"))
from corpus_lineage_review import build, validate


def evidence_pair(shared_agency=None, shared_stops=None, shared_stop_names=None, shared_trips=None, same_hash=False,
                  operators=("Operator A", "Operator B"), publishers=("Publisher A", "Publisher B"),
                  publisher_urls=("https://a.example/feed", "https://b.example/feed")):
    hashes = ["a" * 64, "a" * 64 if same_hash else "b" * 64]
    provenance = {"datasets": [
        {"dataset_id": "001", "zip_sha256": hashes[0], "operator_declared": operators[0], "source_dataset_id": "UNKNOWN", "source_url": "UNKNOWN",
         "agency_identity": [{"agency_id": shared_agency[0] if shared_agency else "a", "agency_name": operators[0]}]},
        {"dataset_id": "002", "zip_sha256": hashes[1], "operator_declared": operators[1], "source_dataset_id": "UNKNOWN", "source_url": "UNKNOWN",
         "agency_identity": [{"agency_id": shared_agency[0] if shared_agency else "b", "agency_name": operators[1]}]},
    ]}
    relation = {"pair_id": "001-002", "dataset_a": "001", "dataset_b": "002",
        "shared_agency_ids": shared_agency or [], "shared_route_ids": [], "shared_stop_ids": shared_stops or [],
        "shared_agency_names": [], "shared_route_short_long_names": [], "shared_stop_names": shared_stop_names or [],
        "shared_trip_ids": shared_trips or [], "trip_overlap_ratio": 0.0 if not shared_trips else 0.9,
        "feed_info_comparison": {"publisher_a": publishers[0], "publisher_b": publishers[1],
            "publisher_url_a": publisher_urls[0], "publisher_url_b": publisher_urls[1]},
        "route_overlap_ratio": 0.0}
    return build(provenance, {"pairs": [relation]})["pairs"][0]


class CorpusLineageReviewTests(unittest.TestCase):
    def test_generic_agency_id_one_is_not_source_lineage(self):
        row = evidence_pair(shared_agency=["1"], operators=("Operator A", "Operator B"))
        self.assertEqual(row["source_lineage_assessment"], "LIKELY_INDEPENDENT_SOURCE")
        self.assertEqual(row["can_be_opposite_split_sides"], "YES")

    def test_single_salamanca_stop_id_does_not_block(self):
        row = evidence_pair(shared_stops=["SALAMANCA"])
        self.assertEqual(row["source_lineage_assessment"], "LIKELY_INDEPENDENT_SOURCE")
        self.assertEqual(row["can_be_opposite_split_sides"], "YES")
        self.assertEqual(row["generic_id_collision"], "GENERIC_ID_COLLISION")

    def test_same_zip_is_blocked_as_same_lineage(self):
        row = evidence_pair(same_hash=True)
        self.assertEqual(row["source_lineage_assessment"], "SAME_SOURCE_LINEAGE")
        self.assertEqual(row["can_be_opposite_split_sides"], "NO")

    def test_shared_network_stops_with_independent_sources_are_allowed(self):
        row = evidence_pair(shared_stops=["0001", "0002"], publishers=("Publisher A", "Publisher B"))
        self.assertEqual(row["relationship_domain"], "NETWORK_STRUCTURE")
        self.assertEqual(row["source_lineage_assessment"], "LIKELY_INDEPENDENT_SOURCE")
        self.assertEqual(row["can_be_opposite_split_sides"], "YES")

    def test_material_trip_overlap_is_blocked(self):
        row = evidence_pair(shared_trips=["trip-1"])
        self.assertEqual(row["source_lineage_assessment"], "LIKELY_SAME_LINEAGE")
        self.assertEqual(row["can_be_opposite_split_sides"], "NO")

    def test_review_rejects_yes_without_positive_evidence(self):
        review = {"pairs": [{"pair_id": "001-002", "dataset_a": "001", "dataset_b": "002",
            "source_lineage_assessment": "NO_LINEAGE_EVIDENCE", "relationship_domain": "NONE",
            "can_be_opposite_split_sides": "YES", "contradictory_independence_signals": []}]}
        review["pairs"] *= 29
        self.assertTrue(any("positive independence" in e for e in validate(review)))


if __name__ == "__main__":
    unittest.main()
