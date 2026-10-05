"""Create and safely profile deterministic relational synthetic GTFS fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from tools.benchmark_safety import evaluate
from tools.resource_measurement import measure

GENERATOR_VERSION = "1.0.0"
MAX_PREDICTED_PRIVATE_RAM_FRACTION = 0.5
BASE_ROWS = {"agency.txt": 1, "routes.txt": 10, "stops.txt": 500,
             "trips.txt": 100, "stop_times.txt": 1000, "calendar.txt": 1}


def predicted_peak_exceeds_envelope(predicted_private_bytes: int, available_ram_bytes: int) -> bool:
    """Keep at least half of currently available RAM outside the next scale prediction."""
    return predicted_private_bytes >= int(available_ram_bytes * MAX_PREDICTED_PRIVATE_RAM_FRACTION)


def _table_contents(scale: int) -> dict[str, str]:
    if scale < 1:
        raise ValueError("scale must be >= 1")
    routes = [f"R{i}" for i in range(10 * scale)]
    stops = [f"S{i}" for i in range(500 * scale)]
    trips = [f"T{i}" for i in range(100 * scale)]
    return {
        "agency.txt": "agency_id,agency_name,agency_url,agency_timezone\nA,Synthetic Transit,https://example.test,Europe/Madrid\n",
        "routes.txt": "route_id,agency_id,route_short_name,route_type\n" + "".join(
            f"{route},A,{i + 1},3\n" for i, route in enumerate(routes)),
        "stops.txt": "stop_id,stop_name,stop_lat,stop_lon\n" + "".join(
            f"{stop},Synthetic Stop {i},40.{i % 10000:04d},-3.{i % 10000:04d}\n"
            for i, stop in enumerate(stops)),
        "trips.txt": "route_id,service_id,trip_id\n" + "".join(
            f"{routes[i % len(routes)]},WK,{trip}\n" for i, trip in enumerate(trips)),
        "stop_times.txt": "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n" + "".join(
            f"{trip},{8 + seq // 60:02d}:{seq % 60:02d}:00,{8 + seq // 60:02d}:{seq % 60:02d}:00,{stops[(i * 10 + seq) % len(stops)]},{seq + 1}\n"
            for i, trip in enumerate(trips) for seq in range(10)),
        "calendar.txt": "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\nWK,1,1,1,1,1,0,0,20260101,20261231\n",
    }


def generate_fixture(path: Path, scale: int) -> dict:
    path = path.resolve()
    if path.exists():
        raise FileExistsError(f"refusing to overwrite fixture: {path}")
    content = _table_contents(scale)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, value in sorted(content.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, value.encode("utf-8"))
    uncompressed = sum(len(value.encode("utf-8")) for value in content.values())
    data_rows = {name: (BASE_ROWS[name] if name in {"agency.txt", "calendar.txt"}
                        else BASE_ROWS[name] * scale) for name in BASE_ROWS}
    counts = {name: value + 1 for name, value in data_rows.items()}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"fixture_id": f"synthetic-gtfs-s{scale}", "generator_version": GENERATOR_VERSION,
            "scale_factor": scale, "zip_bytes": path.stat().st_size,
            "uncompressed_bytes": uncompressed, "row_counts_including_header": counts,
            "data_row_counts": data_rows, "sha256": digest,
            "relational_structure": "unique IDs; all route, trip, service and stop-time references resolve"}


def _run_pipeline(fixture: Path, output: Path) -> int:
    from gtfs_lab.pipeline import run
    result = run(fixture, output)
    print(json.dumps({"run_id": result["run_id"], "summary": result["summary"]}))
    return 0


def run_ladder(root: Path, scales: list[int], interval: float) -> dict:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    rows, stop_reason = [], "MAX_CONFIGURED_SCALE_REACHED"
    previous = None
    safe_stop = False
    for scale in scales:
        fixture_dir = root / f"S{scale}"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        fixture = fixture_dir / "synthetic_gtfs.zip"
        manifest = generate_fixture(fixture, scale)
        preflight = evaluate(expected_root=root, work_dir=fixture_dir / "preflight",
                             volume_path=fixture_dir, benchmark_class="synthetic")
        preflight_path = fixture_dir / "safety_preflight.json"
        preflight_path.write_text(json.dumps(preflight, indent=2) + "\n", encoding="utf-8")
        if preflight["status"] != "PASS":
            safe_stop, stop_reason = True, f"S{scale}_PREFLIGHT_FAILED"
            rows.append({"fixture": manifest, "preflight": preflight, "status": "SKIPPED_SAFETY"})
            break
        output, temp, stage_file = fixture_dir / "output", fixture_dir / "temp", fixture_dir / "stages.jsonl"
        command = [sys.executable, "-m", "tools.synthetic_resource_benchmark", "--run-fixture",
                   str(fixture), "--output", str(output)]
        before_disk = shutil.disk_usage(fixture_dir).free
        result = measure(command, output_dir=output, temp_dir=temp,
                         stage_file=stage_file, interval=interval)
        after_disk = shutil.disk_usage(fixture_dir).free
        item = {"fixture": manifest, "preflight": preflight, "measurement": result,
                "disk_growth_bytes_calculated": before_disk - after_disk,
                "artifact_bytes": sum(p.stat().st_size for p in output.rglob("*") if p.is_file()),
                "status": "PASS" if result["return_code"] == 0 else "FAIL"}
        rows.append(item)
        if result["return_code"] != 0:
            safe_stop, stop_reason = True, f"S{scale}_PIPELINE_EXIT_{result['return_code']}"
            break
        available = preflight["checks"]["physical_ram_available"]["observed_bytes"] or 0
        ceiling = int(available * MAX_PREDICTED_PRIVATE_RAM_FRACTION)
        measured_peak = result.get("private_bytes_peak_sampled") or 0
        if measured_peak >= ceiling:
            safe_stop, stop_reason = True, f"S{scale}_OBSERVED_PRIVATE_MEMORY_REACHED_50_PERCENT_AVAILABLE_RAM"
            break
        if scale != scales[-1]:
            next_scale = scales[scales.index(scale) + 1]
            predicted = int(measured_peak * next_scale / scale)
            if predicted_peak_exceeds_envelope(predicted, available):
                safe_stop, stop_reason = True, f"PREDICTED_S{next_scale}_PRIVATE_MEMORY_{predicted}_BYTES_EXCEEDS_50_PERCENT_AVAILABLE_RAM_{ceiling}_BYTES"
                break
        previous = item
    return {"schema_version": "1.0", "generator_version": GENERATOR_VERSION,
            "actual_pipeline": "gtfs_lab.pipeline.run", "sequential": True,
            "safety_envelope": {"minimum_available_ram_gib_per_synthetic_run": 1.0,
                                "minimum_free_disk_gib_per_synthetic_run": 1.0,
                                "maximum_predicted_private_memory_fraction_of_current_available_ram": MAX_PREDICTED_PRIVATE_RAM_FRACTION,
                                "rationale": "Keep at least half the presently available physical RAM unclaimed by the predicted next synthetic scale; independent from the stricter large-feed and dataset-019 gate."},
            "scale_ladder": [f"S{x}" for x in scales], "completed_scales": [r["fixture"]["fixture_id"] for r in rows if r["status"] == "PASS"],
            "safe_stop_triggered": safe_stop, "safe_stop_reason": stop_reason,
            "measurements": rows, "resource_growth_classification": _classify(rows),
            "previous_scale_record": previous}


def _classify(rows: list[dict]) -> str:
    passed = [r for r in rows if r["status"] == "PASS"]
    if len(passed) < 3:
        return "INCONCLUSIVE"
    ratios = []
    for before, after in zip(passed, passed[1:]):
        s0, s1 = before["fixture"]["scale_factor"], after["fixture"]["scale_factor"]
        m0 = before["measurement"].get("private_bytes_peak_sampled") or 0
        m1 = after["measurement"].get("private_bytes_peak_sampled") or 0
        if m0:
            ratios.append((m1 / m0) / (s1 / s0))
    if len(ratios) < 2:
        return "INCONCLUSIVE"
    return "LINEAR" if all(.5 <= x <= 1.5 for x in ratios) else "SUPERLINEAR" if all(x > 1.5 for x in ratios) else "INCONCLUSIVE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", type=Path)
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--ladder", type=Path)
    parser.add_argument("--scales", default="1,2,4,8,16,32,64,128")
    parser.add_argument("--interval", type=float, default=0.1)
    parser.add_argument("--run-fixture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.run_fixture:
        return _run_pipeline(args.run_fixture, args.output)
    if args.generate:
        record = generate_fixture(args.generate, args.scale)
        if args.manifest:
            args.manifest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record))
        return 0
    scales = [int(x) for x in args.scales.split(",")]
    if not scales or any(s < 1 for s in scales) or scales != sorted(set(scales)):
        parser.error("scales must be unique positive integers in ascending order")
    result = run_ladder(args.ladder, scales, args.interval)
    (args.ladder / "resource_scaling_analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
