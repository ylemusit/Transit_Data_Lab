from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from gtfs_lab.interpretation.consolidation import build_result, semantic_fingerprint
from gtfs_lab.interpretation.reporting import render_markdown


HASH = "a" * 64


class AuditInterpretationRuntimeTests(unittest.TestCase):
    def _zip(self, root: Path) -> Path:
        path = root / "synthetic.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("shapes.txt", "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\n"
                "s1,0,0,1,1\ns1,0,0,2,1\ns2,0,0,1,1\ns2,0,0.000001,2,1\ns3,0,0,1,2\ns3,0,0.00001,2,1\n")
            archive.writestr("routes.txt", "route_id\nr1\nr2\n")
            archive.writestr("trips.txt", "route_id,service_id,trip_id,shape_id\nr1,svc1,t1,s1\nr1,svc2,t2,s1\nr2,svc2,t3,s2\n")
            archive.writestr("calendar.txt", "service_id\nsvc1\nsvc2\n")
            archive.writestr("stops.txt", "stop_id\np1\np2\n")
            archive.writestr("stop_times.txt", "trip_id,arrival_time,departure_time,stop_id,stop_sequence\nt1,08:00:00,08:00:00,p1,1\nt2,09:00:00,09:00:00,p2,1\n")
        return path

    @staticmethod
    def _finding(shape: str, row: int, previous: float, current: float) -> dict:
        return {"origin": "AUDIT_ENGINE", "rule_id": "GTFS-G07-DISTANCE-PROGRESSION", "stage": "G07",
                "source_file": "shapes.txt", "technical_status": "FAIL_TECHNICAL",
                "record_locator": f"data_row:{row}", "observed": {"shape_id": shape, "previous": previous, "current": current}}

    @staticmethod
    def _identity() -> dict:
        return {"dataset_id": "synthetic", "sha256": HASH}

    def test_g07_equal_duplicate_quantization_and_decrease(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = self._zip(Path(temp))
            findings = [self._finding("s1", 2, 1, 1), self._finding("s2", 4, 1, 1), self._finding("s3", 6, 2, 1)]
            result = build_result(dataset_identity=self._identity(), audit_execution_id="run-1", engine_version="1.0",
                                  findings=findings, zip_path=str(archive))
        classifications = {family["patterns"][0]["classification"] for family in result["finding_families"]}
        self.assertEqual(classifications, {"EXACT_DUPLICATE_GEOMETRY", "QUANTIZATION_COMPATIBLE", "DISTANCE_DECREASE"})
        quant = next(family for family in result["finding_families"] if family["patterns"][0]["classification"] == "QUANTIZATION_COMPATIBLE")
        self.assertEqual(quant["inferences"][0]["kind"], "INFERRED")
        self.assertIn("0-0.25m=1", quant["calculations"][-1]["statement"])
        self.assertIn("precisión shape_dist_traveled=INTEGER_ONLY", quant["calculations"][-1]["statement"])
        self.assertEqual(result["coverage"]["accounting_gap"], 0)

    def test_shape_usage_propagates_without_inflating_findings(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = self._zip(Path(temp))
            finding = self._finding("s1", 2, 1, 1)
            result = build_result(dataset_identity=self._identity(), audit_execution_id="run-1", engine_version="1.0",
                                  findings=[finding], zip_path=str(archive))
        family = result["finding_families"][0]
        impact = family["operational_impact"]
        self.assertEqual(impact["direct_affected"]["entity_count"], 1)
        propagated = {item["entity_type"]: item["entity_count"] for item in impact["propagated_usage"]}
        self.assertEqual(propagated, {"route": 1, "service": 2, "trip": 2})
        self.assertEqual(family["raw_occurrence_count"], 1)

    def test_g07_all_distance_buckets_and_mixed_precision(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "buckets.zip"
            points = []
            findings = []
            longitudes = [0, .000001, .000003, .000005, .000008, .000010]
            for index, longitude in enumerate(longitudes):
                shape = f"bucket-{index}"
                seq = index * 2 + 1
                points.extend([f"{shape},0,0,{seq},1.1", f"{shape},0,{longitude},{seq + 1},1.1"])
                findings.append(self._finding(shape, seq + 1, 1.1, 1.1))
            points.extend(["increase,0,0,1,1", "increase,0,0.01,2,2"])
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("shapes.txt", "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\n" + "\n".join(points) + "\n")
            result = build_result(dataset_identity=self._identity(), audit_execution_id="run-1", engine_version="1.0",
                                  findings=findings, zip_path=str(archive))
        family = next(f for f in result["finding_families"] if f["patterns"][0]["classification"] == "QUANTIZATION_COMPATIBLE")
        statement = family["calculations"][-1]["statement"]
        self.assertIn("precisión shape_dist_traveled=MIXED", statement)
        for bucket in ("0=1", "0-0.25m=1", "0.25-0.50m=1", "0.50-0.75m=1", "0.75-1m=1", ">1m=1"):
            self.assertIn(bucket, statement)

    def test_malformed_relationship_is_not_propagated_as_existing_route(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "malformed.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("shapes.txt", "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\ns1,0,0,1,1\ns1,0,0,2,1\n")
                zf.writestr("routes.txt", "route_id\nr1\n")
                zf.writestr("trips.txt", "route_id,service_id,trip_id,shape_id\nmissing-route,missing-service,t1,s1\n")
            result = build_result(dataset_identity=self._identity(), audit_execution_id="run-1", engine_version="1.0",
                                  findings=[self._finding("s1", 2, 1, 1)], zip_path=str(archive))
        propagated = result["finding_families"][0]["operational_impact"]["propagated_usage"]
        self.assertEqual(propagated, [{"entity_type": "trip", "entity_count": 1}])

    def test_unknown_accounting_and_collision_safe_deterministic_ids(self):
        values = [
            {"rule_id": "UNKNOWN-RULE", "file": "mystery.txt", "technical_status": "FAIL_TECHNICAL", "record_locator": "row:1"},
            {"origin": "LEGACY", "rule_id": "L1", "file": "stops.txt", "technical_status": "FAIL_TECHNICAL", "stop_id": "p1"},
            {"origin": "LEGACY", "rule_id": "L1", "file": "stops.txt", "technical_status": "NOT_EVALUABLE", "stop_id": "p1"},
        ]
        first = build_result(dataset_identity=self._identity(), audit_execution_id="run-a", engine_version="1.0", findings=values)
        second = build_result(dataset_identity=self._identity(), audit_execution_id="run-b", engine_version="1.0", findings=list(reversed(values)))
        self.assertEqual(first["coverage"], {"raw_finding_count": 3, "consolidated_occurrence_count": 2, "unclassified_occurrence_count": 1, "accounting_gap": 0})
        self.assertEqual(len({family["family_id"] for family in first["finding_families"]}), 3)
        self.assertEqual({family["family_id"] for family in first["finding_families"]}, {family["family_id"] for family in second["finding_families"]})
        self.assertEqual(semantic_fingerprint(first), semantic_fingerprint(second))
        self.assertIn("## 14. Evidence References", render_markdown(first))

    def test_mixed_pattern_and_missing_context_are_safe(self):
        findings = [{"origin": "AUDIT_ENGINE", "rule_id": "G-X", "stage": "G04", "file": "trips.txt",
                     "technical_status": "FAIL_TECHNICAL", "trip_id": "t1", "pattern_id": "MIXED_PATTERN"}]
        result = build_result(dataset_identity=self._identity(), audit_execution_id="run-1", engine_version="1.0", findings=findings)
        family = result["finding_families"][0]
        self.assertEqual(family["patterns"][0]["classification"], "MIXED_PATTERN")
        self.assertIsNone(family["population"]["population_count"])
        self.assertIsNone(family["affected_percentage"])


if __name__ == "__main__":
    unittest.main()
