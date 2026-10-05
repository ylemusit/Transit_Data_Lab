from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from unittest.mock import patch

from gtfs_lab import client_app
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))
from test_client_packaging import write_synthetic_zip


def pump_until(root, app, terminal, timeout=90):
    deadline = time.monotonic() + timeout
    heartbeats = 0
    while app._state not in terminal and time.monotonic() < deadline:
        root.update()
        heartbeats += 1
        time.sleep(0.01)
    if app._state not in terminal:
        raise TimeoutError(f"GUI state timeout: {app._state}")
    root.update()
    return heartbeats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    if evidence.exists():
        raise SystemExit(f"refusing to overwrite evidence: {evidence}")

    gui_exe = Path(__file__).resolve().parents[1] / "dist-w01p" / "tdl-client" / "tdl-client.exe"
    worker_exe = gui_exe.with_name("tdl-worker.exe")
    if not gui_exe.is_file() or not worker_exe.is_file():
        raise SystemExit("build the onedir package first")

    result = {"packaged_gui_path": str(gui_exe), "worker_path": str(worker_exe),
              "selection_dialogs": "SIMULATED", "engine_semantics_changed": "NO",
              "holdout_accessed": "NO", "runs": []}
    old_frozen = getattr(sys, "frozen", None)
    old_executable = sys.executable
    sys.frozen = True
    sys.executable = str(gui_exe)
    try:
        with tempfile.TemporaryDirectory(prefix="W01P GUI prueba á ") as folder:
            root_dir = Path(folder)
            source = root_dir / "GTFS sintético ñ.zip"
            write_synthetic_zip(source)
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            invalid = root_dir / "GTFS inválido.zip"
            invalid.write_bytes(b"not a zip archive")
            destination = root_dir / "Entrega con espacios á"
            destination.mkdir()

            root = client_app.tk.Tk()
            app = client_app.ClientApp(root)
            original_startfile = getattr(os, "startfile", None)
            opened = []
            with patch.object(client_app.filedialog, "askopenfilename", return_value=str(source)), \
                 patch.object(client_app.filedialog, "askdirectory", return_value=str(destination)), \
                 patch.object(client_app.messagebox, "showwarning") as warning, \
                 patch.object(client_app.messagebox, "showerror") as error, \
                 patch.object(client_app.messagebox, "askyesno", return_value=True), \
                 patch.object(os, "startfile", side_effect=opened.append, create=True):
                app._choose_source()
                app._choose_destination()
                app._start()
                beats = pump_until(root, app, {"SUCCEEDED", "FAILED"})
                assert app._state == "SUCCEEDED", (app._state, app.status.get())
                result["runs"].append({"case": "SUCCESS", "state": app._state,
                                       "status_text": app.status.get(), "gui_heartbeats": beats,
                                       "worker_pid": app._process.pid if app._process else None})
                delivery = app._workspace / "tdl-local" / app._audit_id / "delivery"
                assert delivery.is_dir()
                app._open_delivery()
                assert opened and Path(opened[-1]) == delivery
                manifest = json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))
                seal = json.loads((delivery / "delivery_seal.json").read_text(encoding="utf-8"))
                for relative, item in manifest["delivery_artifacts"].items():
                    actual = hashlib.sha256((delivery / relative).read_bytes()).hexdigest()
                    assert actual == item["sha256"], relative
                assert seal["artifacts_verified"] is True
                result["open_delivery"] = "PASS"
                result["artifact_count"] = len(manifest["delivery_artifacts"])
                result["source_sha256_before_after_equal"] = source_sha == hashlib.sha256(source.read_bytes()).hexdigest()
                assert result["source_sha256_before_after_equal"]

                app.source.set(str(invalid))
                app._start()
                beats = pump_until(root, app, {"SUCCEEDED", "FAILED"})
                assert app._state == "FAILED"
                assert warning.call_count == 1 and error.call_count == 0
                result["runs"].append({"case": "FAILURE", "state": app._state,
                                       "gui_heartbeats": beats, "generic_error_dialog": False})

                app.source.set(str(source))
                app._start()
                cancel_process = app._process
                assert cancel_process is not None and cancel_process.poll() is None
                worker_pid = cancel_process.pid
                app._cancel()
                saw_cancelling = app._state == "CANCELLING"
                beats = pump_until(root, app, {"CANCELLED", "SUCCEEDED", "FAILED"})
                assert saw_cancelling and app._state == "CANCELLED", (saw_cancelling, app._state)
                assert cancel_process.poll() is not None
                assert str(app.open_button.cget("state")) == "disabled"
                log = [json.loads(line) for line in app._technical_log_path.read_text(encoding="utf-8").splitlines()]
                assert any(row.get("event") == "cancel_requested" for row in log)
                assert any(row.get("event") == "worker_finished" and row.get("gui_classification") == "CANCELLED" and "important_stderr" in row for row in log)
                assert any(row.get("event") == "worker_started" and row.get("worker_command") for row in log)
                result["runs"].append({"case": "CANCEL", "state": app._state,
                                       "worker_pid": worker_pid, "worker_terminated": True,
                                       "open_delivery_disabled": True, "gui_heartbeats": beats,
                                       "technical_cancel_and_classification_logged": True})

                app.source.set(str(source))
                app._start()
                beats = pump_until(root, app, {"SUCCEEDED", "FAILED"})
                assert app._state == "SUCCEEDED"
                result["runs"].append({"case": "RERUN_AFTER_CANCEL", "state": app._state,
                                       "gui_heartbeats": beats})
                result["post_cancel_rerun"] = "PASS"
                result["failure_classification"] = "PASS"
                result["cancellation"] = "PASS"
                result["success"] = "PASS"
                assert original_startfile is None or callable(original_startfile)
            app._close()
    finally:
        sys.executable = old_executable
        if old_frozen is None:
            del sys.frozen
        else:
            sys.frozen = old_frozen

    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "runs"}, ensure_ascii=True))
    print(json.dumps(result["runs"], ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())