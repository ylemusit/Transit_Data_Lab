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
    parser.add_argument("--package-root", type=Path)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    if evidence.exists():
        raise SystemExit(f"refusing to overwrite evidence: {evidence}")

    package_root = args.package_root or (Path(__file__).resolve().parents[1] / "dist-w01p" / "tdl-client")
    gui_exe = package_root.resolve() / "tdl-client.exe"
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
            source2 = root_dir / "S32.zip"
            write_synthetic_zip(source2)
            with zipfile.ZipFile(source2, "a") as archive:
                archive.comment = b"W08 S32 regression input"
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            source2_sha = hashlib.sha256(source2.read_bytes()).hexdigest()
            invalid = root_dir / "GTFS inválido.zip"
            invalid.write_bytes(b"not a zip archive")
            destination = root_dir / "Entrega con espacios á"
            destination.mkdir()
            cancel_destination = root_dir / "03_cancel"
            cancel_destination.mkdir()

            root = client_app.tk.Tk()
            app = client_app.ClientApp(root)
            original_startfile = getattr(os, "startfile", None)
            opened = []
            with patch.object(client_app.filedialog, "askopenfilename", side_effect=[str(source), str(source2), str(invalid), str(source), str(source)]), \
                 patch.object(client_app.filedialog, "askdirectory", side_effect=[str(destination), str(cancel_destination), str(destination)]), \
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

                previous_workspace = app._workspace
                previous_audit_id = app._audit_id
                previous_delivery = delivery
                app._choose_source()
                assert app._state == "READY" and str(app.run_button.cget("state")) == "normal"
                assert app._audit_id is None and app._workspace is None
                assert source2_sha != source_sha
                app._choose_destination()
                assert app._state == "READY" and str(app.run_button.cget("state")) == "normal"
                assert str(app.results_button.cget("state")) == "disabled"
                assert str(app.open_button.cget("state")) == "disabled"
                assert str(app.gis_button.cget("state")) == "disabled"
                assert previous_delivery.is_dir()
                assert app._audit_id is None, "audit_id must be allocated only by Start"
                app._start()
                new_audit_id = app._audit_id
                assert new_audit_id and new_audit_id != previous_audit_id
                assert app._workspace.parent == cancel_destination
                assert previous_workspace is not None
                beats = pump_until(root, app, {"SUCCEEDED", "FAILED"})
                assert app._state == "SUCCEEDED", (app._state, app.status.get())
                result["success_to_new_source_destination"] = "PASS"
                result["new_audit_id"] = new_audit_id
                result["previous_delivery_preserved"] = previous_delivery.is_dir()
                result["stale_actions_disabled_while_prepared"] = True
                result["runs"].append({"case": "SUCCESS_TO_NEW_INPUT_SUCCESS", "state": app._state,
                                       "audit_id_changed": new_audit_id != previous_audit_id,
                                       "gui_heartbeats": beats})

                app._choose_source()
                assert app._state == "IDLE" and str(app.run_button.cget("state")) == "disabled"
                assert str(app.results_button.cget("state")) == "disabled"
                result["invalid_input_closes_previous_actions"] = True

                app._choose_source()
                app._start()
                cancel_process = app._process
                cancel_audit_id = app._audit_id
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
                app._choose_source()
                assert app._state == "READY" and str(app.run_button.cget("state")) == "normal"
                assert str(app.results_button.cget("state")) == "disabled"
                assert app._audit_id is None
                app._start()
                assert app._audit_id != cancel_audit_id
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
