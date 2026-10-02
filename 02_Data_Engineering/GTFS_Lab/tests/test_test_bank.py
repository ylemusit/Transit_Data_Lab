from __future__ import annotations

import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.core import sha256_file
from gtfs_lab.test_bank import DEFAULT_TEST_BANK_ROOT, _locked, rebuild_register, run_case


class TestBankTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tb-")
        self.root = Path(self.temp.name)
        self.source = self.root / ("Autobús_ñ_" + "a" * 140 + ".zip")
        with zipfile.ZipFile(self.source, "w") as archive:
            archive.writestr("agency.txt", "agency_name\nEjemplo\n")
        self.bank = self.root / "BANK"
        self.calls = 0
        self.mode = "ok"

    def tearDown(self):
        # SOURCE read-only is part of the contract, including on Windows.
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(stat.S_IWRITE | stat.S_IREAD)
        self.temp.cleanup()

    def runner(self, source, workspace, **kwargs):
        self.calls += 1
        self.assertTrue((self.bank / "ACTIVE" / kwargs["audit_id"]).is_dir())
        self.assertFalse((self.bank / "OK" / f"{kwargs['audit_id']}_OK").exists())
        self.assertRegex(source.name, r"^\d{5}\.zip$")
        base = workspace / kwargs["client_project_id"] / kwargs["audit_id"]
        engine = base / "audit" / "engine_runs" / "RUN"
        delivery = base / "delivery"
        engine.mkdir(parents=True)
        (delivery / "engine_run").mkdir(parents=True)
        (delivery / "report").mkdir()
        content = {"findings": ["finding"], "v": self.calls if self.mode == "replay" else 1}
        (engine / "engine_report.json").write_text(json.dumps(content), encoding="utf-8")
        run = {"run_id": "RUN", "errors": [], "database": {"status": "FAIL_LOCAL" if self.mode == "duckdb" else "PASS"}}
        (delivery / "engine_run" / "run.json").write_text(json.dumps(run), encoding="utf-8")
        (delivery / "report" / "client_report.md").write_text("Informe", encoding="utf-8")
        (delivery / "findings.json").write_text('{"findings": ["finding"]}', encoding="utf-8")
        artifacts = {path.relative_to(delivery).as_posix(): {"sha256": sha256_file(path), "size_bytes": path.stat().st_size}
                     for path in delivery.rglob("*") if path.is_file()}
        manifest = {"status": "COMPLETED_WITH_FINDINGS", "artifacts_sha256_verified": True,
                    "dataset_identity": {"source_sha256": sha256_file(source)}, "delivery_artifacts": artifacts}
        (delivery / "audit_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (delivery / "delivery_seal.json").write_text(json.dumps({"artifacts_verified": True,
                    "audit_manifest_sha256": sha256_file(delivery / "audit_manifest.json")}), encoding="utf-8")
        if self.mode == "tamper":
            (delivery / "findings.json").write_text("altered", encoding="utf-8")
        if self.mode == "source":
            self.source.write_bytes(b"changed")
        return {"status": "COMPLETED_WITH_FINDINGS", "delivery_directory": str(delivery), "findings_count": 1}

    def execute(self, **kwargs):
        with patch("gtfs_lab.test_bank.run_client_audit", side_effect=self.runner):
            return run_case(self.source, self.bank, **kwargs)

    def test_findings_are_ok_identity_retained_normalized_paths_and_seal(self):
        original = self.source.read_bytes()
        record = self.execute(metadata={"dataset_title": "Autobús sintético", "retrieved_time": "2026-10-02T13:32:43Z"})
        self.assertEqual(record["result"], "OK")
        self.assertEqual(record["findings"], 1)
        case = self.bank / "OK" / "00001_OK"
        identity = json.loads((case / "EVIDENCE" / "original_identity.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["original_filename"], self.source.name)
        self.assertEqual(identity["original_path"], str(self.source.resolve()))
        self.assertIn("NOT_PUBLISHER_TIMESTAMPS", identity["FILESYSTEM_METADATA"]["reliability"])
        self.assertEqual((case / "SOURCE" / "00001.zip").read_bytes(), original)
        self.assertEqual(self.source.read_bytes(), original)
        public = (case / "DELIVERY" / "original_identity.json").read_text(encoding="utf-8")
        self.assertNotIn(str(self.root), public)
        self.assertTrue((case / "DELIVERY" / "Autobús_sintético_Auditoria_TDL.md").is_file())
        delivery_manifest = case / "DELIVERY" / "bank_delivery_manifest.json"
        seal = json.loads((case / "DELIVERY" / "bank_delivery_seal.json").read_text())
        self.assertEqual(seal["manifest_sha256"], sha256_file(delivery_manifest))
        rows = rebuild_register(self.bank)
        self.assertEqual(rows[0]["result"], "OK")

    def test_same_content_gets_distinct_execution_ids(self):
        first, second = self.execute(), self.execute()
        self.assertEqual((first["case_id"], second["case_id"]), ("00001", "00002"))
        self.assertEqual(first["source_sha256"], second["source_sha256"])

    def test_corrupt_zip_is_registered_not_ok(self):
        self.source.write_bytes(b"invalid zip")
        record = self.execute()
        self.assertEqual(record["result"], "NOT_OK")
        self.assertEqual(record["failures"][0]["category"], "ZIP")
        self.assertEqual(self.calls, 0)
        self.assertTrue((self.bank / "NOT_OK" / "00001_NOT_OK" / "SOURCE" / "00001.zip").is_file())

    def test_unsafe_zip_never_calls_engine(self):
        with zipfile.ZipFile(self.source, "w") as archive:
            archive.writestr("../agency.txt", "x")
        self.assertEqual(self.execute()["result"], "NOT_OK")
        self.assertEqual(self.calls, 0)

    def test_duckdb_failure_cannot_be_accepted(self):
        self.mode = "duckdb"
        record = self.execute()
        self.assertEqual(record["result"], "NOT_OK")
        self.assertIn("DuckDB", record["failures"][0]["observed"])
        self.assertEqual(record["failures"][0]["category"], "DUCKDB")

    def test_delivery_tampering_fails_closed(self):
        self.mode = "tamper"
        record = self.execute()
        self.assertEqual(record["result"], "NOT_OK")
        self.assertFalse(record["gates"]["DELIVERY_GENERATED"])

    def test_replay_mismatch_is_not_ok(self):
        self.mode = "replay"
        record = self.execute()
        self.assertEqual(record["result"], "NOT_OK")
        self.assertEqual(record["failures"][0]["category"], "REPLAY")
        self.assertEqual(record["replay"], "FAIL")

    def test_changed_original_detected_even_if_frozen_source_survives(self):
        self.mode = "source"
        record = self.execute()
        self.assertEqual(record["result"], "NOT_OK")
        self.assertFalse(record["gates"]["SOURCE_IMMUTABLE"])

    def test_historical_resolved_incidents_do_not_fail_new_successful_case(self):
        record = self.execute(historical_failures=[{"phase": "HISTORICAL", "category": "WINDOWS",
            "observed": "Deep path failed", "status": "RESOLVED", "resolution": "Short workspace"}])
        self.assertEqual(record["result"], "OK")
        self.assertEqual(record["pipeline_failures"], 0)
        self.assertEqual(record["historical_pipeline_failures"], 1)
        event = json.loads((self.bank / "REGISTRY" / "FAILURE_REGISTER.jsonl").read_text())
        self.assertEqual(event["failure_id"], "FAIL-00001-001")

    def test_open_historical_incident_blocks_ok(self):
        record = self.execute(historical_failures=[{"phase": "HISTORICAL", "category": "UNKNOWN", "observed": "pending"}])
        self.assertEqual(record["result"], "NOT_OK")

    def test_lock_and_long_root_fail_before_reservation(self):
        (self.bank / "REGISTRY").mkdir(parents=True)
        (self.bank / "REGISTRY" / "bank.lock").write_text("another process")
        with self.assertRaises(FileExistsError):
            self.execute()
        self.assertEqual((self.bank / "REGISTRY" / "bank.lock").read_text(), "another process")
        with self.assertRaises(ValueError):
            run_case(self.source, self.root / ("x" * 100))

    def test_exhaustion_never_recycles_ids(self):
        (self.bank / "REGISTRY" / "RESERVATIONS" / "99999").mkdir(parents=True)
        with self.assertRaises(ValueError):
            self.execute()

    def test_rebuild_repairs_exports_and_treats_interrupted_finalization_as_active(self):
        self.execute()
        case = self.bank / "OK" / "00001_OK"
        case.rename(self.bank / "ACTIVE" / "00001")
        (self.bank / "REGISTRY" / "TEST_BANK_REGISTER.json").write_text("broken")
        records = rebuild_register(self.bank)
        self.assertEqual(records[0]["result"], "ACTIVE")
        self.assertEqual(self.execute()["case_id"], "00002")

    def test_invalid_metadata_does_not_allocate_case(self):
        with self.assertRaises(ValueError):
            self.execute(metadata={"api_key": "not-a-real-key"})
        self.assertFalse(self.bank.exists())


    def test_not_ok_consumes_id_even_when_case_is_lost(self):
        self.source.write_bytes(b"bad zip")
        first = self.execute()
        self.assertEqual(first["case_id"], "00001")
        case = self.bank / first["case_path"]
        case.rename(self.root / "archived_case")
        self.assertEqual(self.execute()["case_id"], "00002")

    def test_registry_contract_and_delivery_hashes_after_classification(self):
        record = self.execute(metadata={"dataset_title": "Synthetic", "publisher": "Fixture"})
        self.assertEqual(record["dataset_sha256"], sha256_file(self.source))
        self.assertEqual(record["original_metadata"]["publisher"], "Fixture")
        self.assertRegex(record["tdl_commit"], r"^[a-f0-9]{40}$")
        self.assertEqual(record["case_result"], "OK")
        self.assertEqual(record["finding_count"], 1)
        delivery = self.bank / record["case_path"] / "DELIVERY"
        manifest = json.loads((delivery / "bank_delivery_manifest.json").read_text())
        for name, expected in manifest["artifacts"].items():
            self.assertEqual(sha256_file(delivery / name), expected["sha256"])
        identity = json.loads((delivery / "original_identity.json").read_text())
        self.assertEqual(identity["TDL_CASE_REFERENCE"], record["case_id"])

    def test_exclusion_in_another_process(self):
        import subprocess
        import sys
        with _locked(self.bank):
            result = subprocess.run([sys.executable, "-m", "gtfs_lab.test_bank",
                                     "--bank", str(self.bank), "--rebuild"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("BLOCKED", result.stdout)
            self.assertFalse((self.bank / "REGISTRY" / "RESERVATIONS").exists())
        self.assertEqual(rebuild_register(self.bank), [])

    def test_default_and_controlled_override(self):
        self.assertEqual(DEFAULT_TEST_BANK_ROOT.as_posix(), "C:/TDL/BANK")
        self.assertEqual(self.execute()["controlled_short_workspace"], True)


if __name__ == "__main__":
    unittest.main()
