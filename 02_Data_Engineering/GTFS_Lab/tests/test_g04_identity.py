import tempfile
import unittest
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from gtfs_lab.g04_identity import _aggregate, _g03_csv_evidence, evaluate_g04
from gtfs_lab.pipeline import record_ingestion_error


class G04IdentityTests(unittest.TestCase):
    def test_current_g03_file_inspected_contract_is_consumed(self):
        g03 = {"csv_structure": {"files_inspected": [
            {"file": "routes.txt", "status": "PASS"}], "findings": []}}
        self.assertEqual(("COMPLETE", set()), _g03_csv_evidence(g03, "routes.txt"))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tables = {}

    def tearDown(self):
        self.temp.cleanup()

    def table(self, name, header, *rows):
        path = self.root / f"{name}.txt"
        path.write_text(header + "\n" + "\n".join(rows) + ("\n" if rows else ""), encoding="utf-8")
        self.tables[name] = path

    def run_g04(self):
        return evaluate_g04(SimpleNamespace(tables=self.tables, dataset=SimpleNamespace(files={})))

    @staticmethod
    def rule(result, suffix):
        return next(r for r in result["rules"] if r["rule_id"].endswith(suffix))

    def test_single_primary_key_unique_and_duplicate(self):
        self.table("routes", "route_id,route_type", "r,3")
        self.assertEqual(self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")["status"], "PASS")
        self.table("routes", "route_id,route_type", "r,3", "r,3")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "FAIL_TECHNICAL")
        self.assertEqual(rule["findings"][0]["observed_identifier_or_reference"], ["r"])

    def test_uses_ingestion_encoding_metadata(self):
        self.table("routes", "route_id,route_long_name", "r,Café")
        ctx = SimpleNamespace(tables=self.tables,
            dataset=SimpleNamespace(files={"routes.txt": {"encoding": "cp1252"}}))
        self.assertEqual(self.rule(evaluate_g04(ctx), "PRIMARY-KEY-UNIQUENESS")["status"], "PASS")

    def test_composite_key_order_and_empty_identity(self):
        self.table("stop_times", "trip_id,stop_sequence", "t,1", "t,2")
        self.assertEqual(self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")["status"], "PASS")
        self.table("stop_times", "trip_id,stop_sequence", "t,1", "t,1")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["findings"][0]["observed_identifier_or_reference"], ["t", "1"])
        self.table("stop_times", "trip_id,stop_sequence", ",", ",")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "NOT_EVALUABLE")

    def test_transfers_duplicate_with_empty_optional_key_components(self):
        header = "from_stop_id,to_stop_id,from_trip_id,to_trip_id,from_route_id,to_route_id"
        self.table("transfers", header, "a,b,,,,", "a,b,,,,", "a,b,t,,,")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "FAIL_TECHNICAL")
        findings = [f for f in rule["findings"] if f["source_file"] == "transfers.txt"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["record_locator"], "data_row:2")
        self.assertEqual(findings[0]["observed_identifier_or_reference"], ["a", "b", "", "", "", ""])
        self.assertGreater(rule["coverage"]["evaluated"], 0)

        self.table("transfers", "from_stop_id,to_stop_id", "a,b", "a,b")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "FAIL_TECHNICAL")
        self.assertEqual([f["source_file"] for f in rule["findings"]], ["transfers.txt"])

    def test_translations_duplicate_with_empty_optional_key_components(self):
        header = "table_name,field_name,language,record_id,record_sub_id,field_value"
        self.table("translations", header, "stops,stop_name,es,s,,", "stops,stop_name,es,s,,",
            "stops,stop_name,es,other,,")
        rule = self.rule(self.run_g04(), "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "FAIL_TECHNICAL")
        findings = [f for f in rule["findings"] if f["source_file"] == "translations.txt"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["record_locator"], "data_row:2")
        self.assertEqual(findings[0]["observed_identifier_or_reference"],
            ["stops", "stop_name", "es", "s", "", ""])
        self.assertGreater(rule["coverage"]["evaluated"], 0)

    def test_g03_invalid_optional_key_component_is_not_compared(self):
        header = "from_stop_id,to_stop_id,from_trip_id,to_trip_id,from_route_id,to_route_id"
        self.table("transfers", header, "a,b,bad,,,", "a,b,bad,,,")
        g03 = {
            "status": "FAIL_TECHNICAL",
            "csv_structure": {"inspected": [{"file": "transfers.txt", "status": "PASS", "data_rows": 2}],
                "findings": []},
            "field_types": {"findings": [
                {"file": "transfers.txt", "field": "from_trip_id", "row_locator": "ROW:1"},
                {"file": "transfers.txt", "field": "from_trip_id", "row_locator": "ROW:2"}],
                "not_evaluable": []},
        }
        result = evaluate_g04(SimpleNamespace(tables=self.tables, dataset=SimpleNamespace(files={})), g03)
        rule = self.rule(result, "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(rule["status"], "NOT_EVALUABLE")
        self.assertFalse([f for f in rule["findings"] if f["source_file"] == "transfers.txt"])

    def test_reference_pass_orphan_and_missing_parent_never_pass(self):
        self.table("trips", "route_id,service_id,trip_id", "r,s,t")
        self.table("routes", "route_id,route_type", "r,3")
        rule = self.rule(self.run_g04(), "REFERENCE-EXISTENCE")
        self.assertGreater(rule["coverage"]["evaluated"], 0)
        self.assertGreater(rule["coverage"]["not_evaluable"], 0)
        self.table("routes", "route_id,route_type", "other,3")
        self.assertEqual(self.rule(self.run_g04(), "REFERENCE-EXISTENCE")["status"], "FAIL_TECHNICAL")
        self.tables.pop("routes")
        self.assertEqual(self.rule(self.run_g04(), "REFERENCE-EXISTENCE")["status"], "NOT_EVALUABLE")

    def test_frequency_trip_reference_uses_g04_parent_coverage(self):
        self.table("trips", "trip_id", "t")
        self.table("frequencies", "trip_id,start_time", "t,08:00:00", "orphan,09:00:00")
        refs=self.rule(self.run_g04(), "REFERENCE-EXISTENCE")
        finding=next(f for f in refs["findings"] if f["source_file"]=="frequencies.txt")
        self.assertEqual(finding["record_locator"],"data_row:2")
        self.assertEqual(finding["observed_identifier_or_reference"],"orphan")

    def test_g03_incomplete_parent_cannot_create_orphan_finding(self):
        self.table("routes", "route_id,route_type", "r,3", "damaged,3,extra")
        self.table("trips", "route_id,service_id,trip_id", "missing,s,t1", "r,s,t2")
        self.table("calendar", "service_id", "s")
        g03 = {
            "status": "FAIL_TECHNICAL",
            "csv_structure": {
                "status": "FAIL_TECHNICAL",
                "inspected": [
                    {"file": "routes.txt", "status": "FAIL_TECHNICAL", "data_rows": 2},
                    {"file": "trips.txt", "status": "PASS", "data_rows": 2},
                    {"file": "calendar.txt", "status": "PASS", "data_rows": 1},
                ],
                "findings": [{"file": "routes.txt", "row_locator": "ROW:2"}],
            },
            "field_types": {"findings": [], "not_evaluable": []},
        }
        result = evaluate_g04(SimpleNamespace(tables=self.tables, dataset=SimpleNamespace(files={})), g03)
        refs = self.rule(result, "REFERENCE-EXISTENCE")
        self.assertEqual(refs["status"], "NOT_EVALUABLE")
        self.assertGreater(refs["coverage"]["not_evaluable"], 0)
        self.assertFalse(refs["findings"])

    def test_g03_invalid_service_id_is_not_compared_to_logical_domain(self):
        self.table("calendar","service_id","s")
        self.table("trips","service_id,trip_id","broken,t")
        g03={"status":"FAIL_TECHNICAL",
            "csv_structure":{"inspected":[{"file":"calendar.txt","status":"PASS","data_rows":1},{"file":"trips.txt","status":"PASS","data_rows":1}],"findings":[]},
            "field_types":{"findings":[{"file":"trips.txt","field":"service_id","row_locator":"ROW:1"}],"not_evaluable":[]}}
        result=evaluate_g04(SimpleNamespace(tables=self.tables,dataset=SimpleNamespace(files={})),g03)
        domain=self.rule(result,"IDENTITY-DOMAIN")
        self.assertEqual(domain["status"],"NOT_EVALUABLE")
        self.assertFalse(domain["findings"])

    def test_g03_invalid_key_components_are_not_compared_as_identity(self):
        self.table("stop_times", "trip_id,stop_sequence", "t,invalid", "t,invalid")
        g03 = {
            "status": "FAIL_TECHNICAL",
            "csv_structure": {
                "inspected": [{"file": "stop_times.txt", "status": "PASS", "data_rows": 2}],
                "findings": [],
            },
            "field_types": {
                "findings": [
                    {"file": "stop_times.txt", "field": "stop_sequence", "row_locator": "ROW:1"},
                    {"file": "stop_times.txt", "field": "stop_sequence", "row_locator": "ROW:2"},
                ],
                "not_evaluable": [],
            },
        }
        result = evaluate_g04(SimpleNamespace(tables=self.tables, dataset=SimpleNamespace(files={})), g03)
        keys = self.rule(result, "PRIMARY-KEY-UNIQUENESS")
        self.assertEqual(keys["status"], "NOT_EVALUABLE")
        self.assertFalse(keys["findings"])

    def test_populated_optional_reference_and_deferred_parent(self):
        self.table("trips", "route_id,service_id,trip_id,shape_id", "r,s,t,sh")
        self.table("shapes", "shape_id,shape_pt_sequence", "sh,1")
        result = self.run_g04()
        refs = self.rule(result, "REFERENCE-EXISTENCE")
        self.assertTrue(any("shape_id" in f["source_fields"] for f in refs["findings"]) is False)
        self.table("shapes", "shape_id,shape_pt_sequence", "other,1")
        self.assertEqual(self.rule(self.run_g04(), "REFERENCE-EXISTENCE")["status"], "FAIL_TECHNICAL")
        self.table("stop_times", "trip_id,stop_sequence,pickup_booking_rule_id", "t,1,b")
        refs = self.rule(self.run_g04(), "REFERENCE-EXISTENCE")
        self.assertGreater(refs["coverage"]["not_evaluable"], 0)

    def test_empty_deferred_reference_does_not_reduce_coverage(self):
        self.table("stop_times", "trip_id,stop_sequence,stop_id,location_id,location_group_id,pickup_booking_rule_id,drop_off_booking_rule_id", "t,1,s,,,,")
        self.table("trips", "trip_id,route_id,shape_id", "t,r,")
        self.table("routes", "route_id", "r")
        self.table("shapes", "shape_id", )
        self.table("stops", "stop_id,level_id,parent_station", "s,,")
        self.table("levels", "level_id")
        empty = self.rule(self.run_g04(), "REFERENCE-EXISTENCE")
        self.assertEqual(empty["findings"], [])
        self.table("stop_times", "trip_id,stop_sequence,stop_id,location_id,location_group_id,pickup_booking_rule_id,drop_off_booking_rule_id", "t,1,s,,,booking,")
        populated = self.rule(self.run_g04(), "REFERENCE-EXISTENCE")
        self.assertEqual(populated["status"], "NOT_EVALUABLE")
        self.assertEqual(populated["coverage"]["not_evaluable"], empty["coverage"]["not_evaluable"] + 1)

    def test_service_domain_calendar_and_alternate_calendar(self):
        self.table("trips", "route_id,service_id,trip_id", "r,s,t")
        self.table("calendar", "service_id", "s")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "PASS")
        self.table("calendar_dates", "service_id,date,exception_type", "s,20260101,1")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "PASS")
        self.tables.pop("calendar")
        self.table("calendar_dates", "service_id,date,exception_type", "s,20260101,1")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "PASS")
        self.table("calendar_dates", "service_id,date,exception_type", "other,20260101,1")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "FAIL_TECHNICAL")

    def test_calendar_dates_references_calendar_only_when_both_are_present(self):
        self.table("trips", "route_id,service_id,trip_id", "r,s,t")
        self.table("calendar", "service_id", "s")
        self.table("calendar_dates", "service_id,date,exception_type", "orphan,20260101,1")
        rule = self.rule(self.run_g04(), "IDENTITY-DOMAIN")
        self.assertEqual(rule["status"], "FAIL_TECHNICAL")
        finding, = [f for f in rule["findings"] if f["source_file"] == "calendar_dates.txt"]
        self.assertEqual(finding["record_locator"], "data_row:1")
        self.assertEqual(finding["expected_identity_or_target_domain"], "calendar.service_id")
        self.table("calendar_dates", "service_id,date,exception_type", "s,20260101,1")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "PASS")
        self.tables.pop("calendar")
        self.table("trips", "route_id,service_id,trip_id", "r,orphan,t")
        self.table("calendar_dates", "service_id,date,exception_type", "orphan,20260101,1")
        self.assertEqual(self.rule(self.run_g04(), "IDENTITY-DOMAIN")["status"], "PASS")

    def test_self_reference(self):
        self.table("stops", "stop_id,parent_station", "child,parent", "parent,")
        self.assertGreater(self.rule(self.run_g04(), "REFERENCE-EXISTENCE")["coverage"]["evaluated"], 0)
        self.table("stops", "stop_id,parent_station", "child,missing")
        self.assertEqual(self.rule(self.run_g04(), "REFERENCE-EXISTENCE")["status"], "FAIL_TECHNICAL")

    def test_contextual_composite_and_deferred_unresolved_feed_info(self):
        self.table("translations", "table_name,record_id,record_sub_id", "stop_times,t,1")
        self.table("stop_times", "trip_id,stop_sequence", "t,1")
        self.assertEqual(self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")["status"], "PASS")
        self.table("translations", "table_name,record_id,record_sub_id", "stop_times,t,2")
        self.assertEqual(self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")["status"], "FAIL_TECHNICAL")
        self.table("translations", "table_name,record_id,record_sub_id", "attributions,a,")
        self.assertEqual(self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")["status"], "NOT_EVALUABLE")
        self.table("translations", "table_name,record_id,record_sub_id", "feed_info,,")
        self.assertEqual(self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")["status"], "NOT_APPLICABLE")
        self.table("translations", "table_name,record_id,record_sub_id", "custom,x,")
        self.assertEqual(self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")["status"], "NOT_EVALUABLE")

    def test_contextual_simple_key_target(self):
        self.table("translations", "table_name,record_id,record_sub_id", "routes,r,")
        self.table("routes", "route_id,route_type", "r,3")
        rule = self.rule(self.run_g04(), "CONTEXTUAL-REFERENCE")
        self.assertEqual(rule["status"], "PASS")

    def test_g03_invalid_contextual_source_id_is_not_reported_as_orphan(self):
        self.table("translations", "table_name,record_id,record_sub_id", "routes,broken,")
        self.table("routes", "route_id,route_type", "r,3")
        g03={"status":"FAIL_TECHNICAL",
            "csv_structure":{"inspected":[{"file":"translations.txt","status":"PASS","data_rows":1},{"file":"routes.txt","status":"PASS","data_rows":1}],"findings":[]},
            "field_types":{"findings":[{"file":"translations.txt","field":"record_id","row_locator":"ROW:1"}],"not_evaluable":[]}}
        result=evaluate_g04(SimpleNamespace(tables=self.tables,dataset=SimpleNamespace(files={})),g03)
        contextual=self.rule(result,"CONTEXTUAL-REFERENCE")
        self.assertEqual(contextual["status"],"NOT_EVALUABLE")
        self.assertFalse(contextual["findings"])

    def test_findings_are_locatable_and_inventory_failure_is_visible(self):
        self.table("routes", "route_id,route_type", "r,3", "r,3")
        finding = self.run_g04()["findings"][0]
        self.assertTrue({"rule_id", "source_file", "record_locator", "source_fields",
            "observed_identifier_or_reference", "expected_identity_or_target_domain",
            "specification_reference", "technical_reason"}.issubset(finding))
        with patch("gtfs_lab.g04_identity.INVENTORY", self.root / "absent.json"):
            self.assertEqual(self.run_g04()["status"], "INSPECTION_ERROR")

    def test_aggregate_status_and_coverage_precedence(self):
        self.assertEqual(_aggregate(["PASS", "NOT_APPLICABLE"]), "PASS")
        self.assertEqual(_aggregate(["PASS", "FAIL_TECHNICAL"]), "FAIL_TECHNICAL")
        self.assertEqual(_aggregate(["PASS", "NOT_EVALUABLE"]), "NOT_EVALUABLE")
        self.assertEqual(_aggregate(["INSPECTION_ERROR", "NOT_EVALUABLE"]), "INSPECTION_ERROR")
        self.assertEqual(_aggregate(["NOT_EVALUABLE"], has_findings=True), "FAIL_TECHNICAL")

    def test_ingestion_error_marks_g04_skipped_by_dependency(self):
        bad_zip = self.root / "bad.zip"
        bad_zip.write_bytes(b"not a zip")
        result = record_ingestion_error(bad_zip, self.root / "failed-runs", ValueError("synthetic"))
        self.assertEqual(result["g04"], {"status": "SKIPPED_BY_DEPENDENCY"})
        self.assertEqual(result["summary"]["g04"], "SKIPPED_BY_DEPENDENCY")
        for phase in ("g05","g06","g07"):
            self.assertEqual(result[phase],{"status":"SKIPPED_BY_DEPENDENCY"})
            self.assertEqual(result["summary"][phase],"SKIPPED_BY_DEPENDENCY")
        saved = self.root / "failed-runs" / result["run_id"] / "run.json"
        self.assertEqual(json.loads(saved.read_text(encoding="utf-8"))["g04"], result["g04"])


if __name__ == "__main__":
    unittest.main()
