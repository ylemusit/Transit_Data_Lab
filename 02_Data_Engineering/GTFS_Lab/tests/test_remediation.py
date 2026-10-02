from __future__ import annotations

import tempfile
import unittest
import zipfile
import hashlib
from pathlib import Path
from unittest.mock import patch

from gtfs_lab.remediation import (
    AUTHORIZATION, RemediationError, acceptance, attach_reaudit, create_proposal, stable_finding_id,
)


class RemediationV1Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.zip"
        self.derived = self.root / "derived.zip"
        with zipfile.ZipFile(self.source, "w") as archive:
            archive.writestr("agency.txt", "agency_id,agency_name,agency_url,agency_timezone\n1,UTE Rodil,empresarodil.es,Europe/Madrid\n")
            archive.writestr("routes.txt", "route_id,route_type\nr,3\n")
        self.finding = {"rule_id": "GTFS-G03-FIELD-TYPE", "file": "agency.txt", "row_locator": "ROW:1", "field": "agency_url", "observed": "empresarodil.es"}
        self.args = dict(
            source_zip=self.source, derived_zip=self.derived, dataset_id="010",
            source_file="agency.txt", field="agency_url", original_value="empresarodil.es",
            proposed_value="https://empresarodil.es", locator="agency.txt:data_row=1:agency_id=1:agency_url",
            rule_id="GTFS-G03-FIELD-TYPE", finding_id=stable_finding_id(self.finding),
            external_evidence={"url": "https://empresarodil.es", "observed_at_utc": "2026-10-01T04:02:00Z", "claim": "Sitio de Empresa Rodil cargado en HTTPS; la página se identifica como Empresa Rodil."},
            authorization=AUTHORIZATION,
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_case_specific_apply_preserves_source_and_records_diff(self) -> None:
        original = self.source.read_bytes()
        actual_sha = lambda value: hashlib.sha256(value).hexdigest()
        with patch("gtfs_lab.remediation.sha256_bytes", side_effect=lambda value: (
            "3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf"
            if value == original else actual_sha(value)
        )):
            record = create_proposal(**self.args)
        self.assertEqual(original, self.source.read_bytes())
        self.assertTrue(self.derived.is_file())
        self.assertIn("-1,UTE Rodil,empresarodil.es,Europe/Madrid", record["exact_diff"])
        self.assertIn("+1,UTE Rodil,https://empresarodil.es,Europe/Madrid", record["exact_diff"])
        with zipfile.ZipFile(self.derived) as archive:
            self.assertEqual("https://empresarodil.es", archive.read("agency.txt").decode().splitlines()[1].split(",")[2])
            self.assertEqual("route_id,route_type\nr,3\n", archive.read("routes.txt").decode())
        attach_reaudit(record, before_findings=[self.finding], after_findings=[], reproducible=True)
        self.assertEqual("YES", acceptance(record)["ORIGINAL_FINDING_RESOLVED"])

    def test_unapproved_general_missing_scheme_is_rejected(self) -> None:
        args = dict(self.args, dataset_id="other", original_value="other.example", proposed_value="https://other.example")
        with self.assertRaises(RemediationError):
            create_proposal(**args)
        self.assertFalse(self.derived.exists())

    def test_source_hash_mismatch_fails_closed(self) -> None:
        with self.assertRaisesRegex(RemediationError, "source SHA-256"):
            create_proposal(**self.args)


if __name__ == "__main__":
    unittest.main()
