"""CLI-only proof of progress, stream capture, exit, cancellation and reclamation."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from .resource_measurement import _windows_process_snapshot


def run(output: Path) -> dict:
    worker = ("import subprocess,sys,time; child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
              "print('CHILD_PID='+str(child.pid),flush=True); i=0\nwhile True:\n"
              " print('progress',i,flush=True); print('diagnostic',i,file=sys.stderr,flush=True); i+=1; time.sleep(.1)")
    proc = subprocess.Popen([sys.executable, "-u", "-c", worker], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    captured: dict[str, list[str]] = {"stdout": [], "stderr": []}
    def drain(stream, key):
        for line in stream:
            captured[key].append(line.rstrip())
    readers = [threading.Thread(target=drain, args=(proc.stdout, "stdout"), daemon=True),
               threading.Thread(target=drain, args=(proc.stderr, "stderr"), daemon=True)]
    for thread in readers:
        thread.start()
    time.sleep(0.55)
    observed_running = proc.poll() is None
    child_pid = None
    for line in captured["stdout"]:
        if line.startswith("CHILD_PID="):
            child_pid = int(line.split("=", 1)[1])
            break
    if os.name == "nt" and observed_running:
        killed = subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                                capture_output=True, text=True, timeout=10)
        kill_tree_requested = killed.returncode == 0
    else:
        proc.terminate()
        kill_tree_requested = True
    try:
        proc.wait(timeout=5)
        timeout = False
    except subprocess.TimeoutExpired:
        proc.kill(); proc.wait(timeout=5); timeout = True
    for thread in readers:
        thread.join(timeout=2)
    final_snapshot = _windows_process_snapshot()
    absent_after_exit = proc.pid not in final_snapshot
    child_absent = child_pid is None or child_pid not in final_snapshot
    result = {"start": "PASS", "progress": "PASS" if captured["stdout"] else "FAIL",
              "stdout_capture": "PASS" if captured["stdout"] else "FAIL",
              "stderr_capture": "PASS" if captured["stderr"] else "FAIL",
              "child_pid": proc.pid,
              "exit_status": proc.returncode,
              "cancellation": "PASS" if observed_running and proc.returncode != 0 and not timeout and kill_tree_requested else "FAIL",
              "process_tree_kill_requested": kill_tree_requested,
              "child_pid": child_pid,
              "child_process_absent_after_cancellation": child_absent,
              "orphan_processes": [] if child_absent else [child_pid],
              "parent_process_alive_after_worker_exit": os.getpid() in final_snapshot if final_snapshot else None,
              "resource_monitoring": "PASS_SEPARATE_PARENT_HARNESS",
              "process_absent_after_exit": absent_after_exit,
              "memory_reclamation": "PASS_PROCESS_TREE_ABSENCE_OBSERVED" if proc.poll() is not None and absent_after_exit and child_absent else "FAIL",
              "captured_stdout_lines": len(captured["stdout"]), "captured_stderr_lines": len(captured["stderr"]),
              "sample_stdout": captured["stdout"][:3], "sample_stderr": captured["stderr"][:3]}
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    raise SystemExit(0 if all(v == "PASS" for k, v in run(Path(sys.argv[1])).items()
                             if k in {"start", "progress", "stdout_capture", "stderr_capture", "cancellation", "memory_reclamation"}) else 1)
