"""Conservative, explicit preflight for the W00-R development benchmark."""
from __future__ import annotations

import argparse
import ctypes
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import time

HISTORICAL_PEAK_GIB = 18.89
RAM_HEADROOM_FACTOR = 1.25
MIN_FREE_DISK_GIB = 10.0
MAX_SYSTEM_CPU_PERCENT = 25.0


def _available_ram_bytes() -> int | None:
    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(status)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None
        return int(status.ullAvailPhys)
    except Exception:
        return None


def _cpu_pressure() -> float | None:
    try:
        kernel = ctypes.windll.kernel32
        class FILETIME(ctypes.Structure):
            _fields_ = [("low", ctypes.c_ulong), ("high", ctypes.c_ulong)]
        def read():
            idle, kernel_time, user = FILETIME(), FILETIME(), FILETIME()
            if not kernel.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel_time), ctypes.byref(user)):
                return None
            conv = lambda v: (v.high << 32) | v.low
            return conv(idle), conv(kernel_time), conv(user)
        first = read(); time.sleep(0.25); second = read()
        if not first or not second:
            return None
        total = (second[1] + second[2]) - (first[1] + first[2])
        idle_delta = second[0] - first[0]
        return 100.0 * (1 - idle_delta / total) if total > 0 else None
    except Exception:
        return None


def evaluate(*, expected_root: Path, work_dir: Path, volume_path: Path,
             benchmark_class: str = "large") -> dict:
    expected_root, work_dir = expected_root.resolve(), work_dir.resolve()
    available = _available_ram_bytes()
    disk_free = shutil.disk_usage(volume_path.resolve()).free
    cpu = _cpu_pressure()
    if benchmark_class not in {"large", "synthetic"}:
        raise ValueError("benchmark_class must be large or synthetic")
    ram_required_gib = HISTORICAL_PEAK_GIB * RAM_HEADROOM_FACTOR if benchmark_class == "large" else 1.0
    disk_required_gib = MIN_FREE_DISK_GIB if benchmark_class == "large" else 1.0
    ram_required = int(ram_required_gib * (1024 ** 3))
    try:
        work_dir.relative_to(expected_root)
        workdir_ok = work_dir != expected_root
    except ValueError:
        workdir_ok = False
    checks = {
        "physical_ram_available": {"status": "PASS" if available is not None and available >= ram_required else "FAIL",
                                   "observed_bytes": available, "required_bytes": ram_required,
                                   "classification": "OBSERVED" if available is not None else "NOT_CAPTURED"},
        "disk_free": {"status": "PASS" if disk_free >= int(disk_required_gib * 1024 ** 3) else "FAIL",
                      "observed_bytes": disk_free, "required_bytes": int(disk_required_gib * 1024 ** 3),
                      "classification": "OBSERVED"},
        "expected_working_directory": {"status": "PASS" if workdir_ok else "FAIL",
                                       "expected_root": str(expected_root), "work_dir": str(work_dir),
                                       "classification": "OBSERVED"},
        "system_pressure": {"status": "PASS" if cpu is not None and cpu <= MAX_SYSTEM_CPU_PERCENT else "FAIL",
                            "cpu_busy_percent_sampled": cpu, "maximum_percent": MAX_SYSTEM_CPU_PERCENT,
                            "classification": "OBSERVED_SAMPLED" if cpu is not None else "NOT_CAPTURED"},
    }
    passed = all(item["status"] == "PASS" for item in checks.values())
    return {"schema_version": "1.0", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "PASS" if passed else "BENCHMARK_BLOCKED_BY_RESOURCE_SAFETY",
            "benchmark_class": benchmark_class,
            "policy": {"historical_dataset_019_peak_private_gib": HISTORICAL_PEAK_GIB,
                       "available_ram_headroom_factor": RAM_HEADROOM_FACTOR,
                       "minimum_available_ram_gib": round(ram_required_gib, 3),
                       "minimum_free_disk_gib": disk_required_gib,
                       "maximum_sampled_system_cpu_busy_percent": MAX_SYSTEM_CPU_PERCENT,
                       "note": "Experimental development gate only; not a production hardware requirement."},
            "checks": checks}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected-root", type=Path, required=True)
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--volume", type=Path, required=True)
    p.add_argument("--benchmark-class", choices=("large", "synthetic"), default="large")
    p.add_argument("--json", type=Path, required=True)
    a = p.parse_args()
    result = evaluate(expected_root=a.expected_root, work_dir=a.work_dir,
                      volume_path=a.volume, benchmark_class=a.benchmark_class)
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    return 0 if result["status"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
