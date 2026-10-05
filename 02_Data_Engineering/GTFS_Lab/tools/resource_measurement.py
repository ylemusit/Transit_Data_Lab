"""Measure one child process without changing its arguments or environment."""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence


class _FILETIME(ctypes.Structure):
    _fields_ = [("low", ctypes.c_ulong), ("high", ctypes.c_ulong)]


class _COUNTERS(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong), ("page_faults", ctypes.c_ulong),
        ("peak_working_set", ctypes.c_size_t), ("working_set", ctypes.c_size_t),
        ("peak_paged_pool", ctypes.c_size_t), ("paged_pool", ctypes.c_size_t),
        ("peak_nonpaged_pool", ctypes.c_size_t), ("nonpaged_pool", ctypes.c_size_t),
        ("pagefile", ctypes.c_size_t), ("peak_pagefile", ctypes.c_size_t),
        ("private_usage", ctypes.c_size_t),
    ]


def _windows_sample(process: subprocess.Popen[bytes]) -> dict[str, int] | None:
    if os.name != "nt":
        return None
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(_COUNTERS), ctypes.c_ulong]
    psapi.GetProcessMemoryInfo.restype = ctypes.c_int
    kernel.GetProcessTimes.argtypes = [ctypes.c_void_p, ctypes.POINTER(_FILETIME), ctypes.POINTER(_FILETIME),
                                       ctypes.POINTER(_FILETIME), ctypes.POINTER(_FILETIME)]
    kernel.GetProcessTimes.restype = ctypes.c_int
    counters = _COUNTERS()
    counters.cb = ctypes.sizeof(counters)
    handle = ctypes.c_void_p(process._handle)  # noqa: SLF001 - Windows Popen handle
    if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
        return None
    created, exited, kernel_time, user_time = _FILETIME(), _FILETIME(), _FILETIME(), _FILETIME()
    cpu_us = None
    if kernel.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                              ctypes.byref(kernel_time), ctypes.byref(user_time)):
        ticks = lambda ft: (ft.high << 32) | ft.low
        cpu_us = (ticks(kernel_time) + ticks(user_time)) // 10
    return {
        "working_set_bytes": counters.working_set,
        "private_bytes": counters.private_usage,
        "cpu_time_us": cpu_us if cpu_us is not None else -1,
    }


def _windows_process_snapshot() -> dict[int, dict[str, int | None]]:
    """Return process metrics keyed by PID. Fail closed to an empty snapshot."""
    if os.name != "nt":
        return {}
    from ctypes import wintypes

    TH32CS_SNAPPROCESS = 0x00000002
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    PROCESS_VM_READ = 0x0010
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    snap = kernel.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == INVALID_HANDLE_VALUE:
        return {}
    rows: dict[int, dict[str, int | None]] = {}
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        ok = kernel.Process32FirstW(snap, ctypes.byref(entry))
        while ok:
            pid, ppid = int(entry.th32ProcessID), int(entry.th32ParentProcessID)
            handle = kernel.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, pid)
            metrics: dict[str, int | None] = {"parent_pid": ppid, "process_name": str(entry.szExeFile),
                                               "working_set_bytes": None,
                                               "private_bytes": None, "cpu_time_us": None}
            if handle:
                try:
                    counters = _COUNTERS()
                    counters.cb = ctypes.sizeof(counters)
                    if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                        metrics["working_set_bytes"] = int(counters.working_set)
                        metrics["private_bytes"] = int(counters.private_usage)
                    created, exited, kernel_time, user_time = _FILETIME(), _FILETIME(), _FILETIME(), _FILETIME()
                    if kernel.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                              ctypes.byref(kernel_time), ctypes.byref(user_time)):
                        ticks = lambda ft: (ft.high << 32) | ft.low
                        metrics["process_start_filetime"] = ticks(created)
                        metrics["cpu_time_us"] = (ticks(kernel_time) + ticks(user_time)) // 10
                finally:
                    kernel.CloseHandle(handle)
            rows[pid] = metrics
            ok = kernel.Process32NextW(snap, ctypes.byref(entry))
    finally:
        kernel.CloseHandle(snap)
    return rows


def _descendants(snapshot: dict[int, dict], root_pid: int) -> set[int]:
    result, parents = {root_pid}, {pid: row.get("parent_pid") for pid, row in snapshot.items()}
    changed = True
    while changed:
        changed = False
        for pid, parent in parents.items():
            if parent in result and pid not in result:
                result.add(pid)
                changed = True
    return result


def _active_stage(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        active: list[str] = []
        for line in lines:
            row = json.loads(line)
            name = row.get("stage")
            if row.get("state") == "START" and name:
                active.append(str(name))
            elif row.get("state") == "END" and name in active:
                active.remove(str(name))
        return active[-1] if active else ("BETWEEN_STAGES" if lines else None)
    except (OSError, json.JSONDecodeError):
        return None
    return None


def _stage_events(path: Path | None) -> list[dict]:
    if path is None or not path.is_file():
        return []
    events = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return events


def _active_stage_metrics(path: Path | None) -> dict | None:
    events = _stage_events(path)
    for row in reversed(events):
        if row.get("state") == "START" and isinstance(row.get("metrics"), dict):
            if row.get("stage") == _active_stage(path):
                return row["metrics"]
    return None


def _tree_bytes(path: Path | None) -> int | None:
    if path is None or not path.exists():
        return None
    total = 0
    for root, _, files in os.walk(path):
        for name in files:
            try:
                total += (Path(root) / name).stat().st_size
            except OSError:
                pass
    return total


def measure(command: Sequence[str], *, output_dir: Path | None = None,
            temp_dir: Path | None = None, stage_file: Path | None = None,
            interval: float = 1.0, env_overrides: Mapping[str, str] | None = None) -> dict:
    if not command:
        raise ValueError("command must not be empty")
    if output_dir is not None:
        output_dir = output_dir.resolve()
    if temp_dir is not None:
        temp_dir = temp_dir.resolve()
    if stage_file is not None:
        stage_file = stage_file.resolve()
    if temp_dir is not None:
        temp_dir.mkdir(parents=True, exist_ok=True)
    before_output, before_temp = _tree_bytes(output_dir), _tree_bytes(temp_dir)
    volume_path = (output_dir or temp_dir or Path.cwd()).resolve()
    while not volume_path.exists() and volume_path != volume_path.parent:
        volume_path = volume_path.parent
    disk_before = shutil.disk_usage(volume_path)
    start_utc = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    samples: list[dict] = []
    process_history: dict[int, dict] = {}
    root_pid: int | None = None
    root_exit_observed_utc: str | None = None
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        child_env = os.environ.copy()
        if env_overrides:
            child_env.update(env_overrides)
        if stage_file is not None:
            child_env["TDL_RESOURCE_STAGE_FILE"] = str(stage_file)
        if output_dir is not None:
            child_env["TDL_RESOURCE_OUTPUT"] = str(output_dir)
        if temp_dir is not None:
            child_env.update({"TEMP": str(temp_dir), "TMP": str(temp_dir), "TMPDIR": str(temp_dir)})
        with subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, env=child_env) as proc:
            root_pid = proc.pid
            while True:
                timestamp = datetime.now(timezone.utc).isoformat()
                if proc.poll() is not None and root_exit_observed_utc is None:
                    root_exit_observed_utc = timestamp
                snapshot = _windows_process_snapshot()
                pids = _descendants(snapshot, proc.pid) if snapshot else {proc.pid}
                if proc.poll() is not None and (not snapshot or pids == {proc.pid}):
                    break
                sampled = []
                for pid in pids:
                    row = snapshot.get(pid) if snapshot else None
                    if pid == proc.pid and row is None:
                        root = _windows_sample(proc)
                        row = {"parent_pid": None, **(root or {})}
                    if row:
                        saved = process_history.setdefault(pid, {"pid": pid, "first_seen_utc": timestamp,
                                                                 "last_seen_utc": timestamp, "samples": 0})
                        saved["last_seen_utc"], saved["samples"] = timestamp, saved["samples"] + 1
                        saved["parent_pid"] = row.get("parent_pid")
                        saved["process_name"] = row.get("process_name")
                        saved["process_start_filetime"] = row.get("process_start_filetime")
                        saved["process_end_time"] = "NOT_CAPTURED; process may have exited between samples"
                        for key in ("working_set_bytes", "private_bytes", "cpu_time_us"):
                            value = row.get(key)
                            if value is not None:
                                saved[key] = value
                                peak_key = "peak_sampled_" + key
                                saved[peak_key] = max(saved.get(peak_key, 0), value)
                        sampled.append(row)
                ws = [r["working_set_bytes"] for r in sampled if r.get("working_set_bytes") is not None]
                priv = [r["private_bytes"] for r in sampled if r.get("private_bytes") is not None]
                cpu = [r["cpu_time_us"] for r in sampled if r.get("cpu_time_us") is not None]
                root_row = snapshot.get(proc.pid) if snapshot else None
                sample = {"sampled_at_utc": timestamp, "elapsed_s": round(time.perf_counter() - started, 3),
                          "root_pid": proc.pid, "descendant_pids": sorted(pids),
                          "root_working_set_bytes": root_row.get("working_set_bytes") if root_row else None,
                          "root_private_bytes": root_row.get("private_bytes") if root_row else None,
                          "aggregate_working_set_bytes": sum(ws), "aggregate_private_bytes": sum(priv),
                          "aggregate_cpu_time_us": sum(cpu),
                          "captured_process_count": len(sampled),
                          "active_stage": _active_stage(stage_file) or "NOT_CAPTURED",
                          "stage_metrics": _active_stage_metrics(stage_file)}
                samples.append(sample)
                time.sleep(interval)
            # Keep final return code and any root data after process termination.
            process_history.setdefault(proc.pid, {"pid": proc.pid, "first_seen_utc": start_utc,
                                                   "last_seen_utc": datetime.now(timezone.utc).isoformat(), "samples": 0})
            process_history[proc.pid]["exit_status"] = proc.returncode
            if proc.returncode is not None and root_exit_observed_utc is None:
                root_exit_observed_utc = datetime.now(timezone.utc).isoformat()
            process_history[proc.pid]["process_end_time"] = root_exit_observed_utc or datetime.now(timezone.utc).isoformat()
        stdout_bytes, stderr_bytes = os.fstat(stdout_file.fileno()).st_size, os.fstat(stderr_file.fileno()).st_size
    elapsed = time.perf_counter() - started
    after_output, after_temp = _tree_bytes(output_dir), _tree_bytes(temp_dir)
    disk_after = shutil.disk_usage(volume_path)
    private_values = [s["aggregate_private_bytes"] for s in samples]
    working_values = [s["aggregate_working_set_bytes"] for s in samples]
    cpu_values = [s["aggregate_cpu_time_us"] for s in samples]
    stage_profile: dict[str, dict] = {}
    for sample in samples:
        stage = sample["active_stage"]
        if stage == "NOT_CAPTURED" or stage == "BETWEEN_STAGES":
            continue
        row = stage_profile.setdefault(stage, {"sample_count": 0, "peak_aggregate_working_set_bytes_sampled": 0,
                                                "peak_aggregate_private_bytes_sampled": 0,
                                                "classification": "OBSERVED_SAMPLED"})
        row["sample_count"] += 1
        row["peak_aggregate_working_set_bytes_sampled"] = max(row["peak_aggregate_working_set_bytes_sampled"], sample["aggregate_working_set_bytes"])
        row["peak_aggregate_private_bytes_sampled"] = max(row["peak_aggregate_private_bytes_sampled"], sample["aggregate_private_bytes"])
        row.setdefault("root_private_bytes_samples", [])
        row["root_private_bytes_samples"].append(sample.get("root_private_bytes"))
        row.setdefault("root_working_set_bytes_samples", [])
        row["root_working_set_bytes_samples"].append(sample.get("root_working_set_bytes"))
        if sample.get("stage_metrics") is not None:
            row["latest_stage_metrics"] = sample["stage_metrics"]
    event_starts: dict[str, list[datetime]] = {}
    for event in _stage_events(stage_file):
        try:
            stamp = datetime.fromisoformat(event["timestamp_utc"].replace("Z", "+00:00"))
        except (KeyError, ValueError, TypeError):
            continue
        name = str(event.get("stage", "UNKNOWN"))
        if isinstance(event.get("metrics"), dict):
            row = stage_profile.setdefault(name, {"sample_count": 0,
                "peak_aggregate_working_set_bytes_sampled": None,
                "peak_aggregate_private_bytes_sampled": None,
                "classification": "NOT_CAPTURED"})
            row.setdefault("stage_metrics_events", []).append({
                "state": event.get("state"), "timestamp_utc": event.get("timestamp_utc"),
                "metrics": event["metrics"]
            })
        if event.get("state") == "START":
            event_starts.setdefault(name, []).append(stamp)
            stage_profile.setdefault(name, {"sample_count": 0,
                "peak_aggregate_working_set_bytes_sampled": None,
                "peak_aggregate_private_bytes_sampled": None,
                "classification": "NOT_CAPTURED"})
        elif event.get("state") == "END" and event_starts.get(name):
            start_stamp = event_starts[name].pop(0)
            row = stage_profile.setdefault(name, {"sample_count": 0,
                "peak_aggregate_working_set_bytes_sampled": None,
                "peak_aggregate_private_bytes_sampled": None,
                "classification": "NOT_CAPTURED"})
            row["duration_seconds_observed"] = round(row.get("duration_seconds_observed", 0.0) +
                                                     (stamp - start_stamp).total_seconds(), 6)
            row["duration_classification"] = "OBSERVED_FROM_STAGE_MARKERS"
    return {
        "schema_version": "1.0",
        "started_at_utc": start_utc,
        "command_executable": Path(command[0]).name,
        "command_arguments": "REDACTED",
        "return_code": proc.returncode,
        "root_pid": root_pid,
        "processes": list(process_history.values()),
        "samples": samples,
        "stage_resource_profile": stage_profile,
        "stage_events": _stage_events(stage_file),
        "wall_time_s": round(elapsed, 3),
        "cpu_time_s": round((max(cpu_values) - min(cpu_values)) / 1_000_000, 3) if len(cpu_values) > 1 else None,
        "working_set_bytes_peak_sampled": max(working_values, default=None),
        "private_bytes_peak_sampled": max(private_values, default=None),
        "sample_interval_s": interval,
        "sample_count": len(samples),
        "stdout_bytes": stdout_bytes,
        "stderr_bytes": stderr_bytes,
        "output_tree_bytes_before": before_output,
        "output_tree_bytes_after": after_output,
        "output_tree_bytes_delta": after_output - before_output if after_output is not None and before_output is not None else None,
        "temp_tree_bytes_before": before_temp,
        "temp_tree_bytes_after": after_temp,
        "temp_tree_bytes_delta": after_temp - before_temp if after_temp is not None and before_temp is not None else None,
        "disk_usage_path_scope": str(volume_path.drive or volume_path.anchor or "UNKNOWN_VOLUME"),
        "disk_total_bytes_before": disk_before.total,
        "disk_total_bytes_after": disk_after.total,
        "disk_free_bytes_before": disk_before.free,
        "disk_free_bytes_after": disk_after.free,
        "disk_free_bytes_delta_calculated": disk_after.free - disk_before.free,
        "measurements": {
            "wall_time": "OBSERVED",
            "cpu_time": "OBSERVED_SAMPLED" if len(cpu_values) > 1 else "NOT_CAPTURED",
            "working_set_peak": "OBSERVED_SAMPLED" if samples else "NOT_CAPTURED",
            "private_bytes_peak": "OBSERVED_SAMPLED" if samples else "NOT_CAPTURED",
            "output_tree_delta": "OBSERVED" if before_output is not None and after_output is not None else "NOT_CAPTURED",
            "temp_tree_delta": "OBSERVED" if before_temp is not None and after_temp is not None else "NOT_CAPTURED",
            "disk_usage_before_after": "OBSERVED",
            "disk_free_delta": "CALCULATED; volume-wide and not attributed to child process",
            "descendant_processes": "OBSERVED_SAMPLED" if os.name == "nt" and samples else "NOT_CAPTURED",
            "aggregate_process_tree_working_set": "OBSERVED_SAMPLED" if samples else "NOT_CAPTURED",
            "aggregate_process_tree_private_memory": "OBSERVED_SAMPLED" if samples else "NOT_CAPTURED",
            "process_tree_peak": "OBSERVED_SAMPLED; not an exact OS high-water mark" if samples else "NOT_CAPTURED",
            "per_process_working_set_and_private_memory": "OBSERVED_SAMPLED" if process_history else "NOT_CAPTURED",
            "process_start_time": "OBSERVED_FILETIME_AND_FIRST_SAMPLE" if os.name == "nt" else "NOT_CAPTURED",
            "root_process_end_time": "OBSERVED_AFTER_EXIT; timestamp resolution bounded by sampling" if process_history.get(root_pid or -1, {}).get("process_end_time") else "NOT_CAPTURED",
            "descendant_process_end_time": "NOT_CAPTURED_IF_EXITED_BETWEEN_SAMPLES",
            "root_process_exit_status": "OBSERVED" if proc.returncode is not None else "NOT_CAPTURED",
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--temp-dir", type=Path)
    parser.add_argument("--stage-file", type=Path)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        result = measure(command, output_dir=args.output_dir, temp_dir=args.temp_dir,
                         stage_file=args.stage_file, interval=args.interval)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["return_code"] == 0 else int(result["return_code"] or 1)


if __name__ == "__main__":
    raise SystemExit(main())
