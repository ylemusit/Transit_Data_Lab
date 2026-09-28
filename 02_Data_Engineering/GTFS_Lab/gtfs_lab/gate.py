from __future__ import annotations
import json, zipfile
from pathlib import Path
from .core import sha256_file
from .compliance_adapter import inspect_fixed_stop_references
from .ingestion import IngestionError, load_dataset
from .validation import validate
from .pipeline import record_ingestion_error, run

BASE = {
 "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\na,Agency,https://example.test,Europe/Madrid\n",
 "stops.txt": "stop_id,stop_name,stop_lat,stop_lon,location_type\ns1,Stop 1,43.0,-5.0,0\ns2,Stop 2,43.1,-5.1,0\n",
 "routes.txt": "route_id,agency_id,route_short_name,route_type\nr1,a,R1,3\n",
 "trips.txt": "route_id,service_id,trip_id,shape_id,direction_id\nr1,s1,t1,sh1,0\nr1,s1,t2,sh2,1\n",
 "stop_times.txt": "trip_id,arrival_time,departure_time,stop_id,stop_sequence\nt1,25:00:00,25:00:00,s1,1\nt1,25:10:00,25:10:00,s2,2\n",
 "calendar_dates.txt": "service_id,date,exception_type\ns1,20261001,1\n",
 "shapes.txt": "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\nsh1,43.0,-5.0,1\nsh1,43.1,-5.1,2\nsh2,43.0,-5.0,1\nsh2,43.1,-5.1,2\n",
}

def _make_zip(path: Path, files: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 28, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, content.encode("utf-8"))

def create_fixtures(root: Path) -> dict[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    variants = {"VALID_MINIMAL": dict(BASE), "ORPHAN_TRIP": dict(BASE), "ORPHAN_STOP": dict(BASE), "ORPHAN_ROUTE": dict(BASE), "BAD_SERVICE_REFERENCE": dict(BASE), "BAD_SHAPE_REFERENCE": dict(BASE), "MALFORMED_CSV": dict(BASE), "MISSING_FILE": dict(BASE), "PARTIAL_FEED": dict(BASE), "UNSUPPORTED_TABLE": dict(BASE)}
    variants["UNSUPPORTED_TABLE"]["experimental.txt"] = "custom_id,value\nx,1\n"
    variants["ORPHAN_TRIP"]["stop_times.txt"] = BASE["stop_times.txt"].replace("t1,", "ghost,")
    variants["ORPHAN_STOP"]["stop_times.txt"] = BASE["stop_times.txt"].replace(",s1,", ",ghost,")
    variants["ORPHAN_ROUTE"]["trips.txt"] = BASE["trips.txt"].replace("r1,a,R1", "r1,a,R1").replace("r1,s1,t1", "ghost,s1,t1")
    variants["BAD_SERVICE_REFERENCE"]["trips.txt"] = BASE["trips.txt"].replace(",s1,t1,", ",ghost,t1,")
    variants["BAD_SHAPE_REFERENCE"]["trips.txt"] = BASE["trips.txt"].replace("r1,s1,t1,sh1", "r1,s1,t1,ghost")
    variants["MALFORMED_CSV"]["stops.txt"] = "stop_id,stop_name,stop_lat,stop_lon\ns1,\"broken,43,-5\n"
    variants["MISSING_HEADER"]=dict(BASE); variants["MISSING_HEADER"]["routes.txt"] = "agency_id,route_short_name\na,R1\n"
    del variants["MISSING_FILE"]["stop_times.txt"]
    del variants["PARTIAL_FEED"]["shapes.txt"]; del variants["PARTIAL_FEED"]["calendar_dates.txt"]
    out = {}
    for name, files in variants.items():
        path = root / f"{name}.zip"; _make_zip(path, files); out[name] = path
    return out

def run_gate(output: Path, protected_paths: list[Path] | None = None) -> dict:
    protected_paths = protected_paths or []
    protected_before = {str(p.resolve()): sha256_file(p.resolve()) for p in protected_paths}
    fixtures = create_fixtures(output / "fixtures")
    expected = {"VALID_MINIMAL": ("PASS", "PASS"), "ORPHAN_TRIP": ("FAIL_TECHNICAL", "V1-RULE-GTFS"), "ORPHAN_STOP": ("FAIL_TECHNICAL", "V1-RULE-GTFS"), "ORPHAN_ROUTE": ("FAIL_TECHNICAL", "GTFS-REF-TRIP-ROUTE"), "BAD_SERVICE_REFERENCE": ("FAIL_TECHNICAL", "GTFS-REF-SERVICE"), "BAD_SHAPE_REFERENCE": ("FAIL_TECHNICAL", "GTFS-REF-SHAPE"), "MALFORMED_CSV": ("INGESTION_ERROR", None), "MISSING_HEADER": ("INGESTION_ERROR", None), "MISSING_FILE": ("FAIL_TECHNICAL", "GTFS-STRUCT-REQUIRED"), "PARTIAL_FEED": ("FAIL_TECHNICAL", "GTFS-STRUCT-SERVICE-CALENDAR"), "UNSUPPORTED_TABLE": ("PASS", "PASS")}
    rows = []
    e2e_ok = False
    directional_ok = False
    for name, zip_path in fixtures.items():
        try:
            ctx = load_dataset(zip_path, output / "runs")
            result = validate(ctx)
            compliance = inspect_fixed_stop_references(ctx)
            if name == "VALID_MINIMAL":
                repeat = load_dataset(zip_path, output / "repeat")
                repeat_ok = repeat.dataset.dataset_id == ctx.dataset.dataset_id and repeat.dataset.source_sha256 == ctx.dataset.source_sha256
                rows.append({"fixture": "REPRODUCIBLE_DATASET_ID", "status": "PASS" if repeat_ok else "FAIL", "expected": ctx.dataset.dataset_id, "actual": repeat.dataset.dataset_id})
                # Build the complete chain once from synthetic input, including isolated DuckDB and GIS artifacts.
                full = run(zip_path, output / "e2e", route_id="r1")
                direction = run(zip_path, output / "directional", route_id="r1", direction_id="0")
                e2e_ok = all(full["summary"].get(key) == "PASS" for key in ("ingestion", "integrity", "validation", "analysis", "gis", "database", "compliance_v1"))
                directional_ok = direction["summary"]["gis"] == "PASS" and direction["compliance_v1"]["result"] == "PASS"
            expected_status, expected_rule = expected[name]
            actual_status = compliance["result"] if expected_rule == "V1-RULE-GTFS" else result["status"]
            if expected_rule and expected_rule != "PASS":
                rule_findings = compliance["findings"] if expected_rule == "V1-RULE-GTFS" else result["findings"]
                actual_rule = expected_rule if (compliance["result"] == "FAIL_TECHNICAL" if expected_rule == "V1-RULE-GTFS" else any(f["rule_id"] == expected_rule for f in rule_findings)) else None
            elif expected_rule == "PASS": actual_rule = "PASS" if actual_status == "PASS" else None
            else: actual_rule = None
            passed = actual_status == expected_status and actual_rule == expected_rule
            if expected_rule == "V1-RULE-GTFS" and compliance["result"] == "FAIL_TECHNICAL":
                passed = passed and bool(compliance["findings"]) and all(f.get("dataset_id") == ctx.dataset.dataset_id and f.get("evidence", {}).get("source_zip_sha256") for f in compliance["findings"])
            unsupported_status = ctx.inventory.get("NOT_SUPPORTED:experimental.txt") if name == "UNSUPPORTED_TABLE" else None
            if name == "UNSUPPORTED_TABLE": passed = passed and unsupported_status == "NOT_SUPPORTED"
            trip_ids = set()
            if "trips" in ctx.tables:
                import csv
                with ctx.tables["trips"].open("r", encoding="utf-8-sig", newline="") as f:
                    trip_ids = {r.get("trip_id", "") for r in csv.DictReader(f)}
            string_ids_ok = "t1" in trip_ids
            passed = passed and string_ids_ok
            rows.append({"fixture": name, "status": "PASS" if passed else "FAIL", "expected": expected_status, "actual": actual_status, "expected_rule": expected_rule, "actual_rule": actual_rule, "compliance_evaluator": compliance.get("evaluator_sha256"), "string_ids_preserved": string_ids_ok, "unsupported_file_status": unsupported_status})
        except IngestionError as exc:
            passed = expected[name][0] == "INGESTION_ERROR"
            error_run = record_ingestion_error(zip_path, output / "ingestion_errors", exc)
            passed = passed and error_run["run_id"] and error_run["validation"]["status"] == "SKIPPED_BY_DEPENDENCY" and not error_run["validation"]["findings"]
            rows.append({"fixture": name, "status": "PASS" if passed else "FAIL", "expected": expected[name][0], "actual": exc.code, "expected_rule": None, "actual_rule": None, "run_id": error_run["run_id"], "error": str(exc)})
    # ZIP traversal/duplicate archive entries fail before CSV parsing.
    unsafe_path = output / "unsafe.zip"
    with zipfile.ZipFile(unsafe_path, "w") as zf: zf.writestr("../stops.txt", "x")
    try: load_dataset(unsafe_path, output / "unsafe-run"); unsafe_status = "FAIL"
    except IngestionError: unsafe_status = "PASS"
    rows.append({"fixture": "ZIP_PATH_TRAVERSAL", "status": unsafe_status, "expected": "INGESTION_ERROR", "actual": "INGESTION_ERROR" if unsafe_status == "PASS" else "ACCEPTED"})
    duplicate_path = output / "duplicate.zip"
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(duplicate_path, "w") as zf:
            zf.writestr("stops.txt", BASE["stops.txt"]); zf.writestr("stops.txt", BASE["stops.txt"])
    try: load_dataset(duplicate_path, output / "duplicate-run"); duplicate_status = "FAIL"
    except IngestionError: duplicate_status = "PASS"
    rows.append({"fixture": "ZIP_DUPLICATE_MEMBER", "status": duplicate_status, "expected": "INGESTION_ERROR", "actual": "INGESTION_ERROR" if duplicate_status == "PASS" else "ACCEPTED"})
    directional_files = list((output / "directional").glob("*/exports/routes/*dir_0*"))
    route_kml = any(p.suffix == ".kml" for p in directional_files)
    route_geojson = any(p.suffix == ".geojson" for p in directional_files)
    protected_after = {str(p.resolve()): sha256_file(p.resolve()) for p in protected_paths}
    protected_unchanged = protected_before == protected_after
    directional_ok = directional_ok and route_kml and route_geojson
    result = {"gate": "GTFS_LAB_V1_CURRENT_GATE", "status": "PASS" if all(x["status"] == "PASS" for x in rows) and e2e_ok and directional_ok and protected_unchanged else "FAIL_BLOCKING", "fixtures": rows, "e2e_synthetic": "PASS" if e2e_ok else "FAIL_LOCAL", "directional_gis": "PASS" if directional_ok else "FAIL_LOCAL", "protected_hashes_before": protected_before, "protected_hashes_after": protected_after, "protected_state_unchanged": protected_unchanged, "writes": "only within gate output directory"}
    (output / "gate.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, default=Path("runs/gate")); p.add_argument("--protect", type=Path, action="append", default=[]); a = p.parse_args()
    print(json.dumps(run_gate(a.output, a.protect), ensure_ascii=False, indent=2))
