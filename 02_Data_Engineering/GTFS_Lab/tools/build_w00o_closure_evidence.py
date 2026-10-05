"""Assemble bounded W00-O closure evidence from completed local runs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "reports" / "evidence" / "windows_client_v1" / "w00"
RUN_NAMES = ("synthetic_scale_runs_20261005", "synthetic_scale_runs_20261005_extended",
             "synthetic_scale_runs_20261005_final")
STAGES = ("INTAKE", "ZIP_EXTRACTION", "INGESTION", "AUDIT", "INTERPRETATION",
          "REPORT_GENERATION", "REPLAY", "CLEANUP")
ABSOLUTE_WINDOWS_PATH = re.compile(r"[A-Za-z]:[\\/][^\s\"',;]+")


def _sanitize_local_paths(value):
    if isinstance(value, dict):
        return {key: _sanitize_local_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_local_paths(item) for item in value]
    if isinstance(value, str):
        return ABSOLUTE_WINDOWS_PATH.sub("LOCAL_PATH_REDACTED", value)
    return value


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(name: str, payload: dict, *, replace_generated: bool = False) -> None:
    path = EVIDENCE / name
    if path.exists() and not replace_generated:
        raise FileExistsError(f"refusing to overwrite existing evidence: {path}")
    path.write_text(json.dumps(_sanitize_local_paths(payload), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def build() -> dict[str, dict]:
    run_data = {name: read(EVIDENCE / name / "resource_scaling_analysis.json") for name in RUN_NAMES}
    final_name = RUN_NAMES[-1]
    final = run_data[final_name]
    previous_scaling_path = EVIDENCE / "resource_scaling_analysis.json"
    previous_rows = ({row["fixture_id"]: row for row in read(previous_scaling_path).get("measurements", [])}
                     if previous_scaling_path.is_file() else {})
    repeat_hashes: dict[int, list[str]] = {}
    fixture_instances = []
    for name in RUN_NAMES:
        for item in run_data[name]["measurements"]:
            fixture = item["fixture"]
            scale = fixture["scale_factor"]
            repeat_hashes.setdefault(scale, []).append(fixture["sha256"])
            fixture_instances.append({"ladder_run": name, "measurement_status": item["status"],
                                      "fixture": fixture})
    initial_failure_path = (EVIDENCE / "synthetic_scale_runs_20261005" /
                            "resource_scaling_analysis.json")
    if initial_failure_path.is_file():
        failed = read(initial_failure_path)
        if failed.get("measurements"):
            item = failed["measurements"][0]
            repeat_hashes.setdefault(item["fixture"]["scale_factor"], []).append(item["fixture"]["sha256"])
            fixture_instances.append({"ladder_run": "external_first_launch_attempt_excluded",
                                      "measurement_status": item["status"],
                                      "fixture": item["fixture"],
                                      "pipeline_exit_status": item["measurement"].get("return_code"),
                                      "exclusion_reason": "Harness invoked module by file path and exited before a valid pipeline run; corrected to module invocation; no next scale launched."})

    fixture_consistency = {str(scale): len(set(hashes)) == 1
                           for scale, hashes in sorted(repeat_hashes.items())}
    if not all(fixture_consistency.values()):
        raise RuntimeError("deterministic fixture SHA-256 changed across repeated runs")

    measurement_rows = []
    stage_peak = {stage: {"peak_private_bytes_sampled": None, "peak_working_set_bytes_sampled": None,
                          "sample_count": 0, "duration_seconds_observed_sum": 0.0}
                  for stage in STAGES}
    peak_record = None
    for row in final["measurements"]:
        measurement = row["measurement"]
        output_root = EVIDENCE / final_name / f"S{row['fixture']['scale_factor']}" / "output"
        run_json_files = list(output_root.rglob("run.json")) if output_root.is_dir() else []
        pipeline_result = read(run_json_files[0]) if len(run_json_files) == 1 else {}
        previous_row = previous_rows.get(row["fixture"]["fixture_id"], {})
        peak = max(measurement["samples"], key=lambda sample: sample["aggregate_private_bytes"], default=None)
        if peak and (peak_record is None or peak["aggregate_private_bytes"] > peak_record["private_bytes"]):
            peak_record = {"scale": row["fixture"]["fixture_id"], "stage": peak["active_stage"],
                           "private_bytes": peak["aggregate_private_bytes"],
                           "working_set_bytes": peak["aggregate_working_set_bytes"],
                           "sampled_at_utc": peak["sampled_at_utc"]}
        measurement_rows.append({
            "fixture_id": row["fixture"]["fixture_id"], "scale_factor": row["fixture"]["scale_factor"],
            "sha256": row["fixture"]["sha256"], "zip_bytes": row["fixture"]["zip_bytes"],
            "uncompressed_bytes": row["fixture"]["uncompressed_bytes"],
            "row_counts_including_header": row["fixture"]["row_counts_including_header"],
            "data_row_counts": row["fixture"]["data_row_counts"],
            "wall_time_s": measurement["wall_time_s"], "cpu_time_s": measurement["cpu_time_s"],
            "peak_process_tree_working_set_bytes_sampled": measurement["working_set_bytes_peak_sampled"],
            "peak_process_tree_private_bytes_sampled": measurement["private_bytes_peak_sampled"],
            "sample_interval_s": measurement["sample_interval_s"], "sample_count": measurement["sample_count"],
            "stage_at_private_peak": peak["active_stage"] if peak else "NOT_CAPTURED",
            "disk_free_delta_bytes_calculated_volume_wide": measurement["disk_free_bytes_delta_calculated"],
            "workspace_tree_growth_bytes": measurement["output_tree_bytes_delta"],
            "temp_tree_growth_bytes": measurement["temp_tree_bytes_delta"],
            "artifact_bytes": row["artifact_bytes"], "exit_status": measurement["return_code"],
            "pipeline_run_id": pipeline_result.get("run_id", previous_row.get("pipeline_run_id")),
            "pipeline_summary": pipeline_result.get("summary", previous_row.get("pipeline_summary")),
            "output_artifact_count": sum(1 for p in output_root.rglob("*") if p.is_file()) if output_root.is_dir() else previous_row.get("output_artifact_count"),
            "preflight": row["preflight"],
        })
        for stage, metrics in measurement["stage_resource_profile"].items():
            bucket = stage_peak.setdefault(stage, {"peak_private_bytes_sampled": None,
                "peak_working_set_bytes_sampled": None, "sample_count": 0,
                "duration_seconds_observed_sum": 0.0})
            bucket["sample_count"] += metrics.get("sample_count", 0)
            value = metrics.get("peak_aggregate_private_bytes_sampled")
            if value is not None:
                bucket["peak_private_bytes_sampled"] = max(bucket["peak_private_bytes_sampled"] or 0, value)
            value = metrics.get("peak_aggregate_working_set_bytes_sampled")
            if value is not None:
                bucket["peak_working_set_bytes_sampled"] = max(bucket["peak_working_set_bytes_sampled"] or 0, value)
            bucket["duration_seconds_observed_sum"] += metrics.get("duration_seconds_observed", 0.0)
    for stage, metrics in stage_peak.items():
        metrics["memory_classification"] = "OBSERVED_SAMPLED" if metrics["peak_private_bytes_sampled"] is not None else "NOT_CAPTURED"
        metrics["duration_classification"] = "OBSERVED_FROM_STAGE_MARKERS" if metrics["duration_seconds_observed_sum"] else "NOT_CAPTURED"
        if not metrics["duration_seconds_observed_sum"]:
            metrics["duration_seconds_observed_sum"] = None

    safety_envelope = {
        "synthetic_run_preflight_minimum_available_ram_gib": 1.0,
        "synthetic_run_preflight_minimum_free_disk_gib": 1.0,
        "maximum_predicted_private_memory_fraction_of_current_available_ram": 0.5,
        "policy": "Before another synthetic scale, require the predicted private-memory peak to remain below half of current available RAM, leaving at least half unclaimed.",
        "dataset_019_large_benchmark_gate_unchanged": {"required_available_ram_gib": 23.613,
            "required_free_disk_gib": 10.0, "historical_peak_private_gib": 18.89,
            "result": "SKIPPED_RESOURCE_SAFETY"},
        "production_hardware_requirement": False,
    }
    synthetic_benchmark = {
        "schema_version": "1.0", "generator_version": final["generator_version"],
        "generator": "tools.synthetic_resource_benchmark.generate_fixture",
        "fixture_design": "One agency and calendar; unique route, stop and trip IDs; 10 stop-times per trip; all trip/route and stop-time/trip/stop references resolve.",
        "repeated_fixture_hashes_identical_by_scale": fixture_consistency,
        "fixture_instances": fixture_instances,
        "final_ladder_run": final_name,
        "final_ladder_status": final["completed_scales"],
        "limitations": ["Synthetic structures exercise the actual TDL engine but do not reproduce the historical DEVELOPMENT dataset 019 workload.",
                        "Zip fixture identity is deterministic within generator version and scale; runtime outputs contain run-specific IDs/timestamps."],
    }
    scaling_analysis = {
        "schema_version": "1.0", "generator_version": final["generator_version"],
        "actual_pipeline": final["actual_pipeline"], "sequential": True,
        "scale_ladder": final["scale_ladder"], "completed_scales": final["completed_scales"],
        "safe_stop_triggered": final["safe_stop_triggered"], "safe_stop_reason": final["safe_stop_reason"],
        "safety_envelope": safety_envelope,
        "resource_growth_classification": final["resource_growth_classification"],
        "measurement_classification": "OBSERVED_SAMPLED process tree at 100 ms; volume-wide free-space delta is calculated and not attributed to the child.",
        "peak_stage_overall": peak_record,
        "stage_analysis": stage_peak,
        "measurements": measurement_rows,
        "replication_runs": [{"run": name, "classification": run_data[name]["resource_growth_classification"],
                              "completed_scales": run_data[name]["completed_scales"],
                              "safe_stop_triggered": run_data[name]["safe_stop_triggered"]}
                             for name in RUN_NAMES],
        "interpretation": "INCONCLUSIVE overall: small synthetic scale sample and early-scale variability prevent a stable category; observed later doubling measurements are broadly proportional but are not a mathematical complexity claim.",
        "historical_problem_reproduced": False,
    }
    memory_root_cause = {
        "schema_version": "1.0", "memory_root_cause": "NOT_REPRODUCED_WITH_SYNTHETIC_WORKLOAD",
        "dataset_019": "SKIPPED_RESOURCE_SAFETY; available RAM remained below 23.613 GiB during W00-R preflight; not rerun.",
        "synthetic_observation": {"scale": peak_record["scale"] if peak_record else None,
            "active_stage_at_peak": peak_record["stage"] if peak_record else "NOT_CAPTURED",
            "peak_private_bytes_sampled": peak_record["private_bytes"] if peak_record else None,
            "interpretation": "Temporal stage correlation only; no measured component attribution."},
        "stage_memory_profile": stage_peak,
        "unmeasured_stages": [stage for stage in ("INTAKE", "INTERPRETATION", "REPLAY", "CLEANUP")
                              if stage_peak.get(stage, {}).get("memory_classification") == "NOT_CAPTURED"],
        "candidate_components": ["ZIP/CSV materialization", "DuckDB process", "Python validation and analysis structures",
                                 "findings and interpretation", "serialization/report construction", "replay duplication"],
        "cause_assigned": False,
        "reason": "The synthetic pipeline did not reproduce the historical high-memory observation. Fast stages also had no sampled peak at the 100 ms interval. No component is blamed from code presence alone.",
    }
    semantic = read(EVIDENCE / "instrumentation_semantic_comparison.json")
    optimization = {
        "schema_version": "1.0", "problem": "Historical dataset 019 memory growth remains a concern; the authorized synthetic workload did not reproduce that problem.",
        "measured_evidence": {"synthetic_growth": final["resource_growth_classification"],
            "peak_stage": peak_record, "dataset_019_executed": False},
        "root_cause_hypothesis": "NOT_ESTABLISHED; no component attribution supported.",
        "expected_effect": "No optimization proposed or implemented.",
        "semantic_risk": "NOT_ASSESSED_FOR_OPTIMIZATION; optimization gate not entered because the resource problem was not reproduced.",
        "optimization_implemented": False, "before_after_improvement": "NOT_APPLICABLE",
        "instrumentation_semantic_comparison": semantic,
        "engine_semantics_changed": False if semantic["semantic_equivalence"] == "PASS" else "NOT_VERIFIED",
        "decision": "Do not optimize without reproducible resource evidence; retain optimization-required gate before W01."}
    package = read(EVIDENCE / "packaging_pyinstaller_onedir.json")
    reclamation = read(EVIDENCE / "subprocess_reclamation.json")
    closure = {
        "schema_version": "1.0", "base_commit": "f53335747562206936e5db7704dfb093844d768e",
        "state": "W00O_READY_FOR_HUMAN_REVIEW",
        "classification": "W00O_BLOCKED_RESOURCE_ROOT_CAUSE_UNKNOWN",
        "w01": "BLOCKED; do not start",
        "synthetic_scale_ladder": ",".join(final["scale_ladder"]),
        "resource_growth": final["resource_growth_classification"],
        "peak_stage": peak_record,
        "memory_root_cause": memory_root_cause["memory_root_cause"],
        "optimization_implemented": False,
        "before_after_improvement": "NOT_APPLICABLE",
        "semantic_equivalence": semantic["semantic_equivalence"],
        "dataset_019": "DEFERRED_FOR_HIGH_MEMORY_ENVIRONMENT",
        "pyinstaller_onedir": "PASS" if package["status"] == "PASS" else "BLOCKED",
        "duckdb_bundled": package["duckdb_bundled"],
        "clean_machine_validation": package["clean_machine_validation"],
        "subprocess_reclamation": reclamation["status"],
        "orphan_processes": len(reclamation["orphan_processes"]),
        "minimum_hardware": "NOT_YET_ESTABLISHED",
        "recommended_hardware": "NOT_YET_ESTABLISHED",
        "functional_engine_changed": True,
        "engine_semantics_changed": "NO",
        "holdout_accessed": "NO",
        "qgis": "NO_IMPLEMENTATION; GIS evidence package boundary retained; GeoPackage primary candidate.",
        "optimization_required_before_w01": True,
        "clean_machine_validation_plan": ["Fresh Windows environment with no Python or development environment installed.",
            "Confirm bundled DuckDB executable and Python runtime load without system PATH dependencies.",
            "Launch packaged worker, run a synthetic audit, and verify all artifacts and hashes.",
            "Confirm subprocess descendants terminate cleanly and no processes remain."],
        "evidence": {name: f"reports/evidence/windows_client_v1/w00/{name}" for name in (
            "synthetic_scale_benchmark.json", "resource_scaling_analysis.json", "memory_root_cause.json",
            "optimization_before_after.json", "packaging_pyinstaller_onedir.json",
            "subprocess_reclamation.json", "instrumentation_semantic_comparison.json")},
    }
    return {"synthetic_scale_benchmark.json": synthetic_benchmark,
            "resource_scaling_analysis.json": scaling_analysis,
            "memory_root_cause.json": memory_root_cause,
            "optimization_before_after.json": optimization,
            "w00o_closure_decision.json": closure}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace-generated", action="store_true",
                        help="refresh only the five closure JSON files assembled by this tool")
    args = parser.parse_args()
    outputs = build()
    for name, payload in outputs.items():
        write_new(name, payload, replace_generated=args.replace_generated)
    print("W00-O evidence assembled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
