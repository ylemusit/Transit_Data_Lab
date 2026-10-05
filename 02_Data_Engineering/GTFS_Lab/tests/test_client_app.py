from __future__ import annotations

import unittest
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

from gtfs_lab.client_app import (
    ClientApp, WindowsInstanceLock, classify_execution_result, classify_worker_exit,
    family_detail_payload, family_row_values, result_summary_text,
)


class WorkerExitClassificationTests(unittest.TestCase):
    def test_user_cancellation_wins_over_nonzero_return_code(self) -> None:
        self.assertEqual(classify_worker_exit(True, 1), "CANCELLED")

    def test_nonzero_return_without_cancellation_is_failure(self) -> None:
        self.assertEqual(classify_worker_exit(False, 1), "FAILED")

    def test_zero_return_without_cancellation_is_success(self) -> None:
        self.assertEqual(classify_worker_exit(False, 0), "SUCCEEDED")

    def test_cancellation_intent_also_wins_if_worker_races_to_zero(self) -> None:
        self.assertEqual(classify_worker_exit(True, 0), "CANCELLED")


class ExecutionOutcomeClassificationTests(unittest.TestCase):
    def test_distinguishes_input_audit_application_and_human_review_outcomes(self) -> None:
        self.assertEqual(classify_execution_result(False, 2, {"status": "BLOCKED_INPUT_INVALID"}), "BLOCKED_INPUT_INVALID")
        self.assertEqual(classify_execution_result(False, 2, {"status": "BLOCKED_TECHNICAL"}), "AUDIT_FAILED")
        self.assertEqual(classify_execution_result(False, 2, None), "APPLICATION_FAILED")
        self.assertEqual(classify_execution_result(False, 0, {"status": "HUMAN_REVIEW_REQUIRED"}), "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(classify_execution_result(True, 0, {"status": "COMPLETED"}), "CANCELLED")


class NewRunPreparationTests(unittest.TestCase):
    def test_terminal_states_rearm_valid_inputs_and_detach_previous_run(self) -> None:
        class Button:
            def __init__(self) -> None:
                self.state = "normal"

            def configure(self, *, state: str) -> None:
                self.state = state

        with tempfile.TemporaryDirectory() as folder:
            old_delivery = Path(folder) / "previous-delivery"
            old_delivery.mkdir()
            (old_delivery / "preserved.txt").write_text("keep", encoding="utf-8")
            for terminal in (
                "SUCCEEDED", "CANCELLED", "BLOCKED_INPUT_INVALID", "AUDIT_FAILED",
                "APPLICATION_FAILED", "HUMAN_REVIEW_REQUIRED",
            ):
                app = SimpleNamespace(
                    _state=terminal, _workspace=old_delivery.parent, _audit_id="old-audit",
                    _stdout_path=Path(folder) / "old.stdout", _stderr_path=Path(folder) / "old.stderr",
                    _technical_log_path=Path(folder) / "old.technical", _stage_path=Path(folder) / "old.stages",
                    _stage_offset=4, _active_stage="AUDIT", _intake=object(),
                    destination=SimpleNamespace(get=lambda: folder),
                    run_button=Button(), open_button=Button(), results_button=Button(), gis_button=Button(),
                )
                app._prepare_new_run = lambda: ClientApp._prepare_new_run(app)
                app._show_intake = lambda _intake: None
                ClientApp._refresh_ready_state(app)
                self.assertEqual(app._state, "READY", terminal)
                self.assertEqual(app.run_button.state, "normal", terminal)
                self.assertIsNone(app._workspace, terminal)
                self.assertIsNone(app._audit_id, terminal)
                self.assertEqual(app.open_button.state, "disabled", terminal)
                self.assertEqual(app.results_button.state, "disabled", terminal)
                self.assertEqual(app.gis_button.state, "disabled", terminal)
            self.assertEqual((old_delivery / "preserved.txt").read_text(encoding="utf-8"), "keep")


class ExecutionStageTests(unittest.TestCase):
    def test_stage_markers_produce_truthful_stage_text_without_percentages(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "stages.jsonl"
            path.write_text(json.dumps({"stage": "AUDIT", "state": "START"}) + "\n", encoding="utf-8")
            app = SimpleNamespace(
                _stage_path=path, _stage_offset=0, _active_stage=None,
                status=SimpleNamespace(value="", set=lambda value: setattr(app.status, "value", value)),
            )
            ClientApp._refresh_execution_stage(app)
            self.assertIn("Auditoría GTFS", app.status.value)
            self.assertNotIn("%", app.status.value)

    def test_completed_stage_clears_active_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "stages.jsonl"
            path.write_text("\n".join(json.dumps({"stage": "AUDIT", "state": state}) for state in ("START", "END")) + "\n", encoding="utf-8")
            app = SimpleNamespace(
                _stage_path=path, _stage_offset=0, _active_stage=None,
                status=SimpleNamespace(value="", set=lambda value: setattr(app.status, "value", value)),
            )
            ClientApp._refresh_execution_stage(app)
            self.assertIsNone(app._active_stage)


class ResultsViewModelTests(unittest.TestCase):
    def test_summary_uses_persisted_coverage_and_keeps_legal_boundary(self) -> None:
        summary = result_summary_text(
            {"status": "COMPLETED_WITH_FINDINGS", "dataset_identity": {"dataset_id": "GTFS-abc", "source_filename": "feed.zip", "source_sha256": "abc"}},
            {"interpretation_status": "COMPLETE", "coverage": {"raw_finding_count": 8, "consolidated_occurrence_count": 6, "unclassified_occurrence_count": 2, "accounting_gap": 0}},
        )
        self.assertIn("Hallazgos brutos: 8", summary)
        self.assertIn("Brecha contable: 0", summary)
        self.assertIn("no constituyen por sí solos", summary)

    def test_family_row_uses_authoritative_family_fields(self) -> None:
        values = family_row_values({
            "rule_id": "G07", "raw_occurrence_count": 3, "affected_entity_count": 2,
            "patterns": [{"classification": "SPATIAL_ANOMALY"}],
            "operational_impact": {"direct_affected": {"entity_type": "shape", "entity_count": 2}},
        })
        self.assertEqual(values, ("G07", 3, 2, "SPATIAL_ANOMALY", "shape: 2 directas"))

    def test_family_details_include_matching_source_recommendations_and_evidence(self) -> None:
        family = {"rule_id": "G07", "stage": "G07", "source_file": "shapes.txt", "evidence_refs": [{"source_sha256": "abc"}]}
        findings = [
            {"rule_id": "G07", "stage": "G07", "source_file": "shapes.txt", "recommendation": "Review shape geometry"},
            {"rule_id": "G06", "stage": "G06", "source_file": "trips.txt", "recommendation": "unrelated"},
        ]
        details = family_detail_payload(family, findings)
        self.assertEqual(len(details["source_findings"]), 1)
        self.assertEqual(details["source_findings"][0]["recommendation"], "Review shape geometry")
        self.assertIn("evidence_refs", details["family"])


@unittest.skipUnless(os.name == "nt", "worker tree termination is Windows-specific")
class WorkerTreeTerminationTests(unittest.TestCase):
    def test_cancellation_terminates_worker_and_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            child_pid_file = Path(temp) / "child.pid"
            worker_code = (
                "import subprocess,sys,time; "
                "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
                "open(sys.argv[1],'w').write(str(child.pid)); time.sleep(60)"
            )
            process = subprocess.Popen([sys.executable, "-c", worker_code, str(child_pid_file)])
            try:
                deadline = time.monotonic() + 10
                while not child_pid_file.exists() and time.monotonic() < deadline:
                    time.sleep(0.05)
                self.assertTrue(child_pid_file.exists(), "worker did not start its child process")
                child_pid = child_pid_file.read_text(encoding="utf-8")
                harness = SimpleNamespace(_termination_result=None, _log_event=lambda *_args, **_kwargs: None)
                ClientApp._terminate_process_tree(harness, process)
                self.assertIsNotNone(process.poll(), "worker process is still running")
                tasks = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {child_pid}", "/FO", "CSV", "/NH"],
                    check=True, capture_output=True, text=True, timeout=10,
                ).stdout
                self.assertNotIn(f'"{child_pid}"', tasks, "worker descendant is still running")
                self.assertTrue(harness._termination_result["descendant_termination_attempted"])
            finally:
                if process.poll() is None:
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=10)


class WindowsInstanceLockTests(unittest.TestCase):
    def test_rejects_duplicate_and_allows_restart_after_release(self) -> None:
        first = WindowsInstanceLock()
        second = None
        third = None
        try:
            self.assertTrue(first.acquired)
            second = WindowsInstanceLock()
            self.assertFalse(second.acquired)
            second.release()
            first.release()
            third = WindowsInstanceLock()
            self.assertTrue(third.acquired)
        finally:
            if second is not None:
                second.release()
            if third is not None:
                third.release()
            first.release()
if __name__ == "__main__":
    unittest.main()
