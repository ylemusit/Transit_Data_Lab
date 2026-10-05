"""Verify natural completion and controlled tree cancellation for W00-O."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from tools.resource_measurement import measure, _windows_process_snapshot
from tools.subprocess_feasibility import run as run_cancellation


def check(work: Path) -> dict:
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    output, temp = work / "normal-output", work / "normal-temp"
    output.mkdir(parents=True, exist_ok=True)
    stage_file = work / "normal-stages.jsonl"
    result = measure([sys.executable, "-m", "tools.synthetic_resource_child"],
                     output_dir=output, temp_dir=temp, stage_file=stage_file, interval=0.05)
    observed_pids = sorted({pid for sample in result["samples"]
                            for pid in sample["descendant_pids"]})
    final_snapshot = _windows_process_snapshot()
    remaining = [pid for pid in observed_pids if pid in final_snapshot]
    cancellation_path = work / "controlled_cancellation.json"
    cancellation = run_cancellation(cancellation_path)
    return {
        "schema_version": "1.0",
        "normal_completion": {
            "worker_exit_status": result["return_code"],
            "worker_pid": result["root_pid"],
            "observed_tree_pids": observed_pids,
            "resource_monitor_samples": result["sample_count"],
            "tree_absent_after_completion": not remaining,
            "remaining_observed_pids": remaining,
            "output_bytes_delta": result["output_tree_bytes_delta"],
            "temp_bytes_delta": result["temp_tree_bytes_delta"],
            "stage_resource_profile": result["stage_resource_profile"],
            "resource_reclamation": "PROCESS_ADDRESS_SPACE_RELEASE_INFERRED_FROM_TREE_EXIT; OS_FREE_RAM_DELTA_NOT_ATTRIBUTABLE",
        },
        "controlled_cancellation": cancellation,
        "orphan_processes": (cancellation.get("orphan_processes", []) + remaining),
        "status": "PASS" if result["return_code"] == 0 and not remaining
        and cancellation.get("cancellation") == "PASS"
        and cancellation.get("memory_reclamation") == "PASS_PROCESS_TREE_ABSENCE_OBSERVED"
        and cancellation.get("parent_process_alive_after_worker_exit") is True else "FAIL",
        "limitations": ["Process exit is observed; returned physical RAM bytes are not isolated from system activity.",
                        "The process-tree monitor samples Windows snapshots; very short-lived descendants can fall between samples."],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.work)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
