from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from types import SimpleNamespace

from gtfs_lab.g03_structure import (
    EXPECTED_FILE_COUNT,
    EXPECTED_REVISION,
    load_official_catalog,
    inspect_archive_catalog,
    inspect_g03_archive,
)
from gtfs_lab.gate import create_fixtures
from gtfs_lab.pipeline import run
from gtfs_lab.pipeline import record_ingestion_error

SPEC = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_2026_04_27.json"


class G03FileCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_catalog(self, payload, name="catalog.json"):
        path = self.root / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def make_zip(self, names):
        path = self.root / "feed.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for name in names:
                archive.writestr(name, "")
        return SimpleNamespace(source_zip=path)

    def test_official_catalog_loads_with_expected_count_revision_and_unique_identities(self):
        catalog = load_official_catalog(SPEC)
        self.assertEqual(EXPECTED_FILE_COUNT, len(catalog))
        self.assertEqual(EXPECTED_REVISION, json.loads(SPEC.read_text(encoding="utf-8"))["specification"]["revision_date"])
        self.assertEqual(len(catalog), len({name.casefold() for name in catalog}))

    def test_supported_deferred_unknown_and_nested_classification(self):
        ctx = self.make_zip(["agency.txt", "fare_attributes.txt", "vendor.txt", "sub/stops.txt"])
        result = inspect_archive_catalog(ctx)
        by_path = {item["path"]: item for item in result["members"]}
        self.assertEqual("OFFICIAL_V1_SUPPORTED", by_path["agency.txt"]["classification"])
        self.assertEqual("OFFICIAL_DEFERRED", by_path["fare_attributes.txt"]["classification"])
        self.assertEqual("DEFERRED", by_path["fare_attributes.txt"]["tdl_v1_support"])
        self.assertEqual("UNKNOWN_EXTENSION_OR_FILE", by_path["vendor.txt"]["classification"])
        self.assertEqual("NESTED_MEMBER", by_path["sub/stops.txt"]["classification"])
        self.assertEqual("fare_attributes.txt", by_path["fare_attributes.txt"]["official_identity"])
        self.assertEqual("COMPLETE", result["official_catalog_coverage"])
        self.assertNotIn("findings", result)

    def test_all_official_deferred_files_remain_official(self):
        catalog = load_official_catalog(SPEC)
        deferred = [entry["file_name"] for entry in catalog.values() if entry["tdl_v1_support"].startswith("DEFERRED")]
        result = inspect_archive_catalog(self.make_zip(deferred))
        self.assertTrue(result["members"])
        self.assertTrue(all(row["classification"] == "OFFICIAL_DEFERRED" for row in result["members"]))

    def test_member_order_is_deterministic(self):
        a = inspect_archive_catalog(self.make_zip(["z.txt", "agency.txt", "a.bin"]))["members"]
        b = inspect_archive_catalog(self.make_zip(["a.bin", "z.txt", "agency.txt"]))["members"]
        self.assertEqual([row["path"] for row in a], [row["path"] for row in b])

    def test_pipeline_keeps_catalog_additive_to_legacy_findings(self):
        fixtures = create_fixtures(self.root / "fixtures")
        result = run(fixtures["ORPHAN_TRIP"], self.root / "runs")
        catalog = result["g03_file_catalog"]
        self.assertEqual("PASS", catalog["status"])
        self.assertNotIn("GTFS-G03-FILE-CATALOG", {rule["rule_id"] for rule in result["validation"]["rules"]})
        self.assertTrue(result["validation"]["findings"])
        self.assertEqual(len(result["validation"]["findings"]), result["validation"]["finding_count"])
        self.assertTrue(all(item["rule_id"] != "GTFS-G03-FILE-CATALOG" for item in result["validation"]["findings"]))

    def test_missing_and_malformed_catalog_fail_explicitly(self):
        with self.assertRaisesRegex(RuntimeError, "missing"):
            load_official_catalog(self.root / "absent.json")
        malformed = self.root / "bad.json"
        malformed.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "cannot be parsed"):
            load_official_catalog(malformed)

    def test_schema_revision_count_and_duplicate_identity_are_rejected(self):
        base = json.loads(SPEC.read_text(encoding="utf-8"))
        cases = []
        bad = copy.deepcopy(base); bad["schema_version"] = "9.0.0"; cases.append((bad, "schema_version"))
        bad = copy.deepcopy(base); bad["specification"]["revision_date"] = "2026-04-28"; cases.append((bad, "revision"))
        bad = copy.deepcopy(base); bad["files"].pop(); cases.append((bad, "exactly 32"))
        bad = copy.deepcopy(base); bad["files"][1]["file_name"] = bad["files"][0]["file_name"]; cases.append((bad, "Duplicate"))
        for index, (payload, message) in enumerate(cases):
            with self.subTest(message=message), self.assertRaisesRegex(RuntimeError, message):
                load_official_catalog(self.write_catalog(payload, f"bad-{index}.json"))

    def make_g03_zip(self, members):
        path = self.root / "g03.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for name, payload in members.items():
                archive.writestr(name, payload)
        return path

    def test_g03_catalog_rule_identity_and_execution_contract(self):
        result = inspect_g03_archive(self.make_g03_zip({"agency.txt": "agency_name\nA\n"}))
        self.assertIn("GTFS-G03-FILE-CATALOG", result["rule_versions"])
        self.assertEqual("GTFS-G03-FILE-CATALOG", result["file_catalog"]["rule_id"])
        self.assertTrue(result["file_catalog"]["evaluator_executed"])
        self.assertEqual(sorted(row["rule_id"] for row in result["rules"]),
                         [row["rule_id"] for row in result["rules"]])

    def test_csv_valid_header_only_and_inconsistent_width(self):
        valid = inspect_g03_archive(self.make_g03_zip({"agency.txt": "agency_name\nA\n"}))
        self.assertEqual("PASS", valid["csv_structure"]["status"])
        header_only = inspect_g03_archive(self.make_g03_zip({"agency.txt": "agency_name\n"}))
        self.assertEqual("PASS", header_only["csv_structure"]["status"])
        malformed_width = inspect_g03_archive(self.make_g03_zip({"agency.txt": "agency_name,agency_url\nA\n"}))
        self.assertEqual("FAIL_TECHNICAL", malformed_width["csv_structure"]["status"])
        finding = malformed_width["csv_structure"]["findings"][0]
        self.assertEqual("ROW:1", finding["row_locator"])
        self.assertIn("specification_reference", finding)

    def test_csv_malformed_quotes_empty_duplicate_headers_and_empty_file(self):
        cases = {
            "broken quote": "agency_name\n\"broken\n",
            "empty header": ",agency_url\nA,x\n",
            "duplicate header": "agency_name,agency_name\nA,B\n",
            "empty file": "",
        }
        for label, contents in cases.items():
            with self.subTest(label=label):
                result = inspect_g03_archive(self.make_g03_zip({"agency.txt": contents}))
                self.assertEqual("FAIL_TECHNICAL", result["csv_structure"]["status"])

    def test_csv_unsupported_text_encoding_is_technical_failure(self):
        result = inspect_g03_archive(self.make_g03_zip({"agency.txt": b"agency_name\n\x81\n"}))
        self.assertEqual("FAIL_TECHNICAL", result["csv_structure"]["status"])
        self.assertEqual("UNDECODABLE", result["csv_structure"]["findings"][0]["observed"])

    def test_header_schema_and_field_types_use_capability_map(self):
        result = inspect_g03_archive(self.make_g03_zip({
            "agency.txt": "agency_name,agency_url,agency_timezone,cemv_support,imaginary_column\n"
                         "Transit,https://example.org,Europe/Madrid,9,x\n"}))
        self.assertEqual("NOT_EVALUABLE", result["header_schema"]["status"])
        self.assertEqual("FAIL_TECHNICAL", result["field_types"]["status"])
        self.assertTrue(result["header_schema"]["evaluator_executed"])
        self.assertEqual("NOT_EVALUABLE", next(row for row in result["rules"] if row["rule_id"] == "GTFS-G03-HEADER-SCHEMA")["status"])
        self.assertEqual("NOT_EVALUABLE_EXTENSION_POLICY", next(
            row["status"] for row in result["header_schema"]["decisions"]
            if row.get("assessment") == "UNKNOWN_HEADER"))
        self.assertFalse(any(row["field"] == "agency_id" for row in result["header_schema"]["findings"]))

    def test_checked_value_plus_unsupported_type_is_not_evaluable(self):
        result = inspect_g03_archive(self.make_g03_zip({
            "agency.txt": "agency_name,agency_timezone\nTransit,Europe/Madrid\n"}))
        self.assertEqual("NOT_EVALUABLE", result["field_types"]["status"])
        self.assertEqual(1, result["field_types"]["checked_values"])
        self.assertTrue(any(row["field"] == "agency_timezone" and
                            row["reason"] == "UNSUPPORTED_LEXICAL_VALIDATOR"
                            for row in result["field_types"]["not_evaluable"]))

    def test_partial_type_coverage_with_failure_preserves_failure(self):
        result = inspect_g03_archive(self.make_g03_zip({
            "agency.txt": "agency_name,agency_url,agency_timezone\nTransit,ftp://invalid,Europe/Madrid\n"}))
        self.assertEqual("FAIL_TECHNICAL", result["field_types"]["status"])
        self.assertTrue(result["field_types"]["not_evaluable"])

    def test_row_condition_runtime_applies_required_effects(self):
        path = self.root / "conditional.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("stops.txt", "stop_id,stop_name,stop_lat,stop_lon,location_type\nS1,,,,0\n")
        result = inspect_g03_archive(path)
        findings = result["header_schema"]["findings"]
        self.assertTrue(any(item["field"] == "stop_name" and item["row_locator"] == "ROW:1" for item in findings))
        self.assertTrue(any(item["field"] == "stop_lat" and item["row_locator"] == "ROW:1" for item in findings))
        self.assertTrue(any(item["field"] == "stop_lon" and item["row_locator"] == "ROW:1" for item in findings))

    def test_header_required_and_type_constraints_are_normative(self):
        result = inspect_g03_archive(self.make_g03_zip({
            "agency.txt": "agency_name,agency_timezone,cemv_support\nTransit,Europe/Madrid,9\n"}))
        self.assertTrue(any(row["field"] == "agency_url" for row in result["header_schema"]["findings"]))
        self.assertTrue(any(row["field"] == "cemv_support" for row in result["field_types"]["findings"]))

    def test_presence_required_optional_and_flex_awareness(self):
        complete = {"agency.txt": "agency_name\nA\n", "stops.txt": "stop_id\ns\n",
                    "routes.txt": "route_id\nr\n", "trips.txt": "trip_id\nt\n",
                    "stop_times.txt": "trip_id\nt\n", "calendar.txt": "service_id\ns\n"}
        result = inspect_g03_archive(self.make_g03_zip(complete))
        self.assertEqual("PASS", result["file_presence"]["status"])
        self.assertTrue(any(row["requirement"] == "OPTIONAL" and row["truth"] == "NOT_APPLICABLE"
                            for row in result["file_presence"]["decisions"]))
        without_stops = {key: value for key, value in complete.items() if key != "stops.txt"}
        missing = inspect_g03_archive(self.make_g03_zip(without_stops))
        self.assertTrue(any(row["file"] == "stops.txt" for row in missing["file_presence"]["findings"]))
        flex = dict(without_stops)
        flex["locations.geojson"] = '{"type":"FeatureCollection","features":[]}'
        flex_result = inspect_g03_archive(self.make_g03_zip(flex))
        self.assertFalse(any(row["file"] == "stops.txt" for row in flex_result["file_presence"]["findings"]))
        self.assertTrue(any(row["truth"] == "UNKNOWN" for row in flex_result["file_presence"]["decisions"]))

    def test_conditional_feed_info_and_levels_presence(self):
        base = {"agency.txt": "agency_name\nA\n", "stops.txt": "stop_id\ns\n",
                "routes.txt": "route_id\nr\n", "trips.txt": "trip_id\nt\n",
                "stop_times.txt": "trip_id\nt\n", "calendar.txt": "service_id\ns\n"}
        for name, trigger in (("feed_info.txt", "translations.txt"), ("levels.txt", "pathways.txt")):
            data = dict(base)
            data[trigger] = "table_name,field_name,language\nstops,stop_name,es\n" if trigger == "translations.txt" else "pathway_id,pathway_mode\np,5\n"
            result = inspect_g03_archive(self.make_g03_zip(data))
            self.assertTrue(any(row["file"] == name for row in result["file_presence"]["findings"]))

    def test_conditional_forbidden_network_files_follow_routes_network_id_header(self):
        data = {"agency.txt": "agency_name\nA\n", "stops.txt": "stop_id\ns\n",
                "routes.txt": "route_id,network_id\nr,n\n", "trips.txt": "trip_id\nt\n",
                "stop_times.txt": "trip_id\nt\n", "calendar.txt": "service_id\ns\n",
                "networks.txt": "network_id\nn\n"}
        result = inspect_g03_archive(self.make_g03_zip(data))
        self.assertTrue(any(row["rule_id"] == "GTFS-G03-FILE-RESTRICTIONS" and row["file"] == "networks.txt" and row["observed"] == "PRESENT"
                            for row in result["file_presence"]["findings"]))
        data.pop("networks.txt")
        result = inspect_g03_archive(self.make_g03_zip(data))
        self.assertFalse(any(row["file"] == "networks.txt" for row in result["file_presence"]["findings"]))

    def test_presence_unknown_trigger_is_not_reported_as_failure(self):
        data = {"agency.txt": "agency_name\nA\n", "stops.txt": "stop_id\ns\n",
                "routes.txt": "route_id\nr\n", "trips.txt": "trip_id\nt\n",
                "stop_times.txt": "trip_id\nt\n", "calendar.txt": "service_id\ns\n",
                "pathways.txt": "pathway_id,pathway_mode\n\"broken\n"}
        result = inspect_g03_archive(self.make_g03_zip(data))
        self.assertFalse(any(row["file"] == "levels.txt" for row in result["file_presence"]["findings"]))

    def test_g03_is_separate_from_legacy_findings_and_visible_for_bad_csv_ingestion(self):
        malformed = self.make_g03_zip({"agency.txt": "agency_name\n\"broken\n"})
        result = inspect_g03_archive(malformed)
        self.assertEqual("FAIL_TECHNICAL", result["csv_structure"]["status"])
        self.assertTrue(result["rules"])
        self.assertNotIn("GTFS-G03-CSV-STRUCTURE", {row["rule_id"] for row in result["file_presence"]["findings"]})
        failed_run = record_ingestion_error(malformed, self.root / "failed-run", RuntimeError("malformed synthetic CSV"))
        self.assertEqual("FAIL_TECHNICAL", failed_run["g03"]["csv_structure"]["status"])
        self.assertTrue((self.root / "failed-run" / failed_run["run_id"] / "run.json").is_file())


if __name__ == "__main__":
    unittest.main()
