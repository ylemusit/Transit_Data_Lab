import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from gtfs_lab.g05_temporal import evaluate_g05
from gtfs_lab.g06_operations import evaluate_g06
from gtfs_lab.g07_spatial import evaluate_g07
from gtfs_lab.phase_runtime_contract import build_phase_registry
from gtfs_lab import g05_temporal, g06_operations, g07_spatial


class LaterPhaseRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.tables={}
        self.ctx=SimpleNamespace(tables=self.tables,dataset=SimpleNamespace(files={}))
    def tearDown(self): self.tmp.cleanup()
    def table(self,name,header,*rows):
        p=self.root/f"{name}.txt";p.write_text(header+"\n"+"\n".join(rows)+"\n",encoding="utf-8");self.tables[name]=p
    def run_g06(self): return evaluate_g06(self.ctx,g05_result=evaluate_g05(self.ctx))

    def test_g05_date_and_service_day_time_ranges(self):
        self.table("calendar","service_id,start_date,end_date","s,20260102,20260101")
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,25:00:00,24:00:00,600")
        result=evaluate_g05(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("CALENDAR-RANGE"))["status"],"FAIL_TECHNICAL")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-TIME-RANGE"))["status"],"FAIL_TECHNICAL")

    def test_g05_builds_calendar_dates_with_exceptions(self):
        self.table("calendar","service_id,start_date,end_date,monday,tuesday,wednesday,thursday,friday,saturday,sunday","s,20260101,20260105,1,0,0,1,0,0,0")
        self.table("calendar_dates","service_id,date,exception_type","s,20260104,1","s,20260105,2")
        result=evaluate_g05(self.ctx)
        effective=result["service_dates_by_service_id"]["s"]
        self.assertEqual(effective["weekly_periods"],[{"start_date":"2026-01-01","end_date":"2026-01-05","weekdays":[0,3]}])
        self.assertTrue(effective["exceptions"]["2026-01-04"])
        self.assertFalse(effective["exceptions"]["2026-01-05"])
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("SERVICE-DATE-SET"))["status"],"PASS")

    def test_g05_dates_only_defines_active_days(self):
        self.table("calendar_dates","service_id,date,exception_type","s,20260104,1","s,20260105,2")
        result=evaluate_g05(self.ctx)
        self.assertEqual(result["service_dates_by_service_id"],{"s":{"weekly_periods":[],"exceptions":{"2026-01-04":True,"2026-01-05":False}}})

    def test_g05_does_not_expose_partial_service_date_materialization(self):
        self.table("calendar","service_id,start_date,end_date,monday,tuesday,wednesday,thursday,friday,saturday,sunday",
                   "valid,20260101,20260105,1,0,0,0,0,0,0","invalid,20260110,20260101,1,0,0,0,0,0,0")
        result=evaluate_g05(self.ctx)
        rule=next(r for r in result["rules"] if r["rule_id"].endswith("SERVICE-DATE-SET"))
        self.assertEqual(rule["status"],"NOT_EVALUABLE")
        self.assertEqual(result["service_dates_by_service_id"],{})

    def test_g05_defers_pickup_window_order_without_normative_must(self):
        self.table("stop_times","trip_id,start_pickup_drop_off_window,end_pickup_drop_off_window",
                   "t,08:00:00,09:00:00","u,10:00:00,09:00:00")
        result=evaluate_g05(self.ctx)
        rule=next(r for r in result["rules"] if r["rule_id"].endswith("PICKUP-WINDOW-ORDER-REVIEW"))
        self.assertEqual(rule["status"],"NOT_EVALUABLE")
        self.assertEqual(rule["category"],"QUALITY")
        self.assertEqual(rule["coverage"]["not_evaluable"],2)
        self.assertEqual(rule["findings"],[])

    def test_g05_feed_range_and_g03_coverage(self):
        self.table("feed_info","feed_start_date,feed_end_date","20260103,20260102")
        result=evaluate_g05(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("FEED-RANGE"))["status"],"FAIL_TECHNICAL")
        g03={"status":"FAIL_TECHNICAL","csv_structure":{"inspected":[{"file":"feed_info.txt","status":"FAIL_TECHNICAL"}],"findings":[]},"field_types":{"findings":[],"not_evaluable":[]}}
        self.assertEqual(next(r for r in evaluate_g05(self.ctx,g03)["rules"] if r["rule_id"].endswith("FEED-RANGE"))["status"],"NOT_EVALUABLE")

    def test_g05_unresolved_g04_identity_blocks_calendar_materialization(self):
        self.table("calendar_dates","service_id,date,exception_type","s,20260104,1")
        g04={"rules":[{"rule_id":"GTFS-G04-PRIMARY-KEY-UNIQUENESS","status":"NOT_EVALUABLE"}]}
        result=evaluate_g05(self.ctx,g04_result=g04)
        service_rule=next(r for r in result["rules"] if r["rule_id"].endswith("SERVICE-DATE-SET"))
        self.assertEqual(service_rule["status"],"NOT_EVALUABLE")
        self.assertEqual(result["service_dates_by_service_id"],{})

    def test_g06_sequence_gaps_allowed_and_frequency_touching_allowed(self):
        self.table("stop_times","trip_id,stop_sequence","t,1","t,4")
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,08:00:00,09:00:00,600","t,09:00:00,10:00:00,600")
        result=self.run_g06()
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("STOP-SEQUENCE"))["status"],"PASS")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))["status"],"PASS")

    def test_g06_does_not_claim_unanchored_time_monotonicity_as_gtfs_failure(self):
        self.table("stop_times","trip_id,stop_sequence,arrival_time,departure_time","t,1,10:00:00,10:00:00","t,2,09:00:00,09:00:00")
        result=self.run_g06()
        rule=next(r for r in result["rules"] if r["rule_id"].endswith("TRIP-TIME-ORDER-REVIEW"))
        self.assertEqual(rule["status"],"NOT_EVALUABLE")
        self.assertEqual(rule["category"],"QUALITY")
        self.assertEqual(result["findings"],[])

    def test_g06_uses_sequence_values_not_csv_row_order(self):
        self.table("stop_times","trip_id,stop_sequence,arrival_time,departure_time","t,2,09:00:00,09:00:00","t,1,08:00:00,08:00:00")
        result=self.run_g06()
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("STOP-SEQUENCE"))["status"],"PASS")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("TRIP-TIME-ORDER-REVIEW"))["status"],"NOT_EVALUABLE")

    def test_g06_exact_times_end_boundary(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs,exact_times","t,08:00:00,10:00:00,600,1")
        result=self.run_g06()
        frequency=next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))
        self.assertEqual(frequency["status"],"FAIL_TECHNICAL")

    def test_g06_zero_length_frequency_scope_is_not_evaluable_without_exact_times(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,08:00:00,08:00:00,600")
        result=self.run_g06()
        frequency=next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))
        self.assertEqual(frequency["status"],"NOT_EVALUABLE")
        self.assertEqual(frequency["findings"],[])
        self.assertTrue(any(review["authority"]=="TDL_QUALITY" for review in result["deferred_rule_reviews"]))

    def test_g06_zero_length_exact_times_one_is_technical_failure(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs,exact_times","t,08:00:00,08:00:00,600,1")
        result=self.run_g06()
        frequency=next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))
        self.assertEqual(frequency["status"],"FAIL_TECHNICAL")
        self.assertEqual(len(frequency["findings"]),1)

    def test_g06_frequency_overlap_and_nonpositive_headway(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,08:00:00,09:30:00,600","t,09:00:00,10:00:00,600")
        result=self.run_g06()
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))["status"],"FAIL_TECHNICAL")

    def test_g06_does_not_duplicate_g05_bad_frequency_range(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,10:00:00,09:00:00,600")
        g05=evaluate_g05(self.ctx)
        g06=evaluate_g06(self.ctx,g05_result=g05)
        self.assertEqual(next(r for r in g05["rules"] if r["rule_id"].endswith("FREQUENCY-TIME-RANGE"))["status"],"FAIL_TECHNICAL")
        frequency=next(r for r in g06["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))
        self.assertEqual(frequency["status"],"NOT_EVALUABLE")
        self.assertEqual(frequency["findings"],[])

    def test_g06_rejects_nonpositive_headway(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs","t,08:00:00,09:00:00,0")
        self.assertEqual(next(r for r in self.run_g06()["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))["status"],"FAIL_TECHNICAL")

    def test_g06_empty_trip_ids_do_not_merge_frequency_groups(self):
        self.table("frequencies","trip_id,start_time,end_time,headway_secs",",08:00:00,09:00:00,600",",08:30:00,09:30:00,600")
        rule=next(r for r in self.run_g06()["rules"] if r["rule_id"].endswith("FREQUENCY-OPERATIONS"))
        self.assertEqual(rule["status"],"NOT_EVALUABLE")
        self.assertEqual(rule["findings"],[])

    def test_g07_bounds_order_and_distance(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled","s,1,40,-3,0","s,3,91,-3,10","s,5,41,-3,9")
        result=evaluate_g07(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("SHAPE-SEQUENCE"))["status"],"PASS")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("COORDINATE-BOUNDS"))["status"],"FAIL_TECHNICAL")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"FAIL_TECHNICAL")

    def test_g07_orders_distance_by_sequence_not_csv_row(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled","s,5,40,-3,10","s,1,39,-4,0")
        result=evaluate_g07(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("SHAPE-SEQUENCE"))["status"],"PASS")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"PASS")

    def test_g07_checks_available_distances_across_blank_rows(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled",
                   "s,1,40,-3,0","s,2,40,-3,","s,3,41,-4,5")
        rules=evaluate_g07(self.ctx)["rules"]
        self.assertEqual(next(r for r in rules if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"PASS")

    def test_g07_unparseable_coordinate_is_not_evaluable(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon","s,1,not-a-latitude,-3")
        rules=evaluate_g07(self.ctx)["rules"]
        coordinate=next(r for r in rules if r["rule_id"].endswith("COORDINATE-BOUNDS"))
        self.assertEqual(coordinate["status"],"NOT_EVALUABLE")
        self.assertEqual(coordinate["findings"],[])

    def test_g07_coordinate_bounds_are_inclusive(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon","s,1,-90,-180","s,2,90,180")
        result=evaluate_g07(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("COORDINATE-BOUNDS"))["status"],"PASS")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"NOT_APPLICABLE")

    def test_g07_empty_shape_ids_do_not_merge_distance_groups(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled",",1,40,-3,0",",2,41,-4,1")
        rules=evaluate_g07(self.ctx)["rules"]
        self.assertEqual(next(r for r in rules if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"NOT_EVALUABLE")

    def test_g07_defers_sequence_order_when_g04_finds_duplicate_identity(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled",
            "s,1,40,-3,0","s,1,41,-4,1","other,1,42,-5,0","other,2,43,-6,1")
        g04={"rules":[{"rule_id":"GTFS-G04-PRIMARY-KEY-UNIQUENESS","status":"FAIL_TECHNICAL","findings":[
            {"source_file":"shapes.txt","record_locator":"data_row:2",
             "observed_identifier_or_reference":["s","1"]}]}]}
        rules=evaluate_g07(self.ctx,g04_result=g04)["rules"]
        sequence=next(r for r in rules if r["rule_id"].endswith("SHAPE-SEQUENCE"))
        distance=next(r for r in rules if r["rule_id"].endswith("DISTANCE-PROGRESSION"))
        self.assertEqual(sequence["status"],"PASS")
        self.assertEqual(sequence["coverage"]["evaluated"],4)
        self.assertEqual(distance["status"],"NOT_EVALUABLE")
        self.assertEqual(distance["coverage"]["evaluated"],1)
        self.assertEqual(distance["coverage"]["not_evaluable"],2)

    def test_g07_absent_shapes_not_applicable(self):
        self.assertEqual(evaluate_g07(self.ctx)["status"],"NOT_APPLICABLE")

    def test_phase_results_preserve_registry_identity_and_execution(self):
        for result in (evaluate_g05(self.ctx),evaluate_g06(self.ctx),evaluate_g07(self.ctx)):
            self.assertTrue(result["rule_versions"])
            self.assertEqual(set(result["rule_versions"]),{rule["rule_id"] for rule in result["rules"]})
            self.assertTrue(all(rule["evaluator_executed"] for rule in result["rules"]))

    def test_g05_g07_rules_have_complete_typed_registry_definitions(self):
        phases=((g05_temporal,"g05_temporal",evaluate_g05),
                (g06_operations,"g06_operations",evaluate_g06),
                (g07_spatial,"g07_spatial",evaluate_g07))
        for module,phase,evaluator in phases:
            with self.subTest(phase=phase):
                registry=build_phase_registry(module.RULE_SPECS,evaluator,phase)
                self.assertTrue(registry.frozen)
                self.assertEqual(set(module.RULES),{definition.rule_id for definition in registry})
                self.assertEqual({"rule_versions":{rule_id:"1.0.0" for rule_id in module.RULES}},registry.identity_map())
                for definition in registry:
                    self.assertTrue(definition.category.value)
                    self.assertTrue(definition.authority.value)
                    self.assertTrue(definition.severity.value)
                    self.assertTrue(definition.requirement.value)
                    self.assertTrue(definition.applicable_files)
                    self.assertEqual("2026-04-27",definition.specification_reference.revision)
                    self.assertEqual(evaluator,definition.evaluator)
                    self.assertEqual(f"gtfs_lab.{phase}.{definition.rule_id.lower()}/1",definition.evaluator_identity)

    def test_g07_rejects_negative_sequence_and_distance(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon,shape_dist_traveled","s,-1,40,-3,-2")
        result=evaluate_g07(self.ctx)
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("SHAPE-SEQUENCE"))["status"],"FAIL_TECHNICAL")
        self.assertEqual(next(r for r in result["rules"] if r["rule_id"].endswith("DISTANCE-PROGRESSION"))["status"],"FAIL_TECHNICAL")

    def test_g07_does_not_classify_g03_invalid_shape_rows(self):
        self.table("shapes","shape_id,shape_pt_sequence,shape_pt_lat,shape_pt_lon","s,1,91,-3")
        g03={"status":"FAIL_TECHNICAL","csv_structure":{"inspected":[{"file":"shapes.txt","status":"PASS"}],"findings":[]},"field_types":{"findings":[{"file":"shapes.txt","field":"shape_pt_lat","row_locator":"ROW:1"}],"not_evaluable":[]}}
        self.assertEqual(evaluate_g07(self.ctx,g03)["status"],"NOT_EVALUABLE")


if __name__=="__main__": unittest.main()
