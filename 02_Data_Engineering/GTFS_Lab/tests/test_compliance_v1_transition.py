from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import compliance_v1_engine as v2
from compliance_v1_transition_candidate import PREDECESSOR_DB_SHA256, build_candidate
from m06_b02_pack import DB as COMPLIANCE_DB

BASE = "8d4f2ad7fa0545b76dd5d5ec5503890ed0c396d9"
FIELDS = (
    "result", "reason", "locator", "observed", "legal_conclusion_allowed",
    "dataset_sha256", "dataset_id",
)


def load_v1():
    source = subprocess.check_output(
        ["git", "show", f"{BASE}:tools/compliance_v1_engine.py"],
        cwd=ROOT, text=True, encoding="utf-8",
    )
    temp = tempfile.TemporaryDirectory()
    path = Path(temp.name) / "compliance_v1_engine_frozen.py"
    # Keep the Git blob's LF bytes; text-mode writes normalize line endings on Windows.
    path.write_bytes(source.encode("utf-8"))
    spec = importlib.util.spec_from_file_location("compliance_v1_engine_frozen", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return temp, module


class ComplianceV1TransitionTests(unittest.TestCase):
    def test_frozen_synthetic_fixture_semantic_projection(self):
        temp, v1 = load_v1()
        self.addCleanup(temp.cleanup)
        self.assertEqual(v1.VERSION, "compliance-v1/1")
        self.assertEqual(v2.VERSION, "compliance-v1/2")
        evidence = ROOT / "03_Compliance/reports/evidence/compliance_v1_20260928"
        fixtures = ROOT / "03_Compliance/fixtures/compliance_v1"
        sources = evidence / "sources"
        cases = json.loads((fixtures / "manifest.json").read_text(encoding="utf-8"))
        gtfs_version = cases[0]["version"]
        netex_version = next(c["version"] for c in cases if c["standard"] == "NETEX")
        self.assertEqual(len(cases), 28)
        for case in cases:
            with self.subTest(case=case["id"]):
                evaluated = dict(case, directory=fixtures / case["id"])
                old = v1.evaluate(evaluated, sources, gtfs_version, netex_version)
                new = v2.evaluate(evaluated, sources, gtfs_version, netex_version)
                self.assertEqual(
                    {key: old.get(key) for key in FIELDS},
                    {key: new.get(key) for key in FIELDS},
                )

    def test_expanded_domain_clears_prototype_row_and_byte_caps(self):
        temp, v1 = load_v1()
        self.addCleanup(temp.cleanup)
        version = "fixture-v"
        large_trips = (
            b"trip_id,route_id,service_id,extra\n"
            + b"".join(
                f"t{i},r,s,{('x' * 105)}\n".encode("ascii")
                for i in range(10000)
            )
        )
        self.assertGreater(len(large_trips), 1024 * 1024)
        one_trip = b"trip_id,route_id,service_id\nt0,r,s\n"
        stops = b"stop_id,location_type\ns,0\n"
        times = b"trip_id,stop_id,stop_sequence\nt0,s,1\n"
        for name, trips in (("over_byte_cap", large_trips), ("over_row_cap", one_trip + b"".join(
                f"t{i},r,s\n".encode("ascii") for i in range(1, 10001)))):
            files = {"trips.txt": trips, "stops.txt": stops, "stop_times.txt": times}
            with self.subTest(case=name):
                old = v1.inspect_gtfs(files, version, version)
                new = v2.inspect_gtfs(files, version, version)
                self.assertEqual(old["result"], "INSPECTION_ERROR")
                self.assertEqual(new["result"], "PASS")

    def test_candidate_generator_replays_with_lineage_and_guards(self):
        if not COMPLIANCE_DB.is_file():
            self.skipTest(
                "Requires the separately backed-up Compliance V1 database at "
                f"{COMPLIANCE_DB} (SHA-256 {PREDECESSOR_DB_SHA256}); "
                "a clean checkout intentionally does not contain or generate it."
            )
        with COMPLIANCE_DB.open("rb") as database:
            database_sha256 = hashlib.file_digest(database, "sha256").hexdigest().upper()
        self.assertEqual(
            PREDECESSOR_DB_SHA256,
            database_sha256,
            "Restored Compliance V1 database does not match the frozen transition input.",
        )
        package_a, manifest_a = build_candidate()
        package_b, manifest_b = build_candidate()
        self.assertEqual(package_a, package_b)
        self.assertEqual(manifest_a["candidate_package_sha256"], manifest_b["candidate_package_sha256"])
        self.assertEqual(manifest_a["candidate_status"], "UNDER_REVIEW")
        self.assertEqual(manifest_a["approval_status"], "UNDER_REVIEW_NOT_APPROVED")
        self.assertEqual(manifest_a["transition_reason"], "IMPLEMENTATION_CHANGE")
        self.assertEqual(manifest_a["rule_version_before"], manifest_a["rule_version_after"])
        self.assertEqual(manifest_a["evaluator_version_after"], "compliance-v1/2")
        for rule in package_a["tables"]["audit.rules"]:
            contract = json.loads(rule["validation_expression"])
            self.assertEqual(contract["configuration"], "gtfs_max_file_bytes=536870912; gtfs_max_rows=1000000; gtfs_max_logical_record_bytes=4194304; gtfs_max_field_bytes=131072; gtfs_max_columns=256; netex_max_bytes=1048576; complete declared scope required; limits are implementation guards")


if __name__ == "__main__":
    unittest.main()
