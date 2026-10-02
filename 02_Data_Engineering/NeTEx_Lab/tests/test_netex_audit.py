from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from netex_lab.audit import audit
from netex_lab.intake import IntakeError, parse_xml, read_sources
from netex_lab.report import json_report, markdown_report
from netex_lab.rules import RULES, validate_registry
from netex_lab.schema import SCHEMA_PATH


VALID_XML = b'''<?xml version="1.0" encoding="UTF-8"?>
<PublicationDelivery xmlns="http://www.netex.org.uk/netex" version="2.0">
  <PublicationTimestamp>2026-10-02T00:00:00Z</PublicationTimestamp>
  <ParticipantRef>TDL-DEVELOPMENT</ParticipantRef>
</PublicationDelivery>'''


class IntakeTests(unittest.TestCase):
    def test_rejects_dtd_and_external_entities(self):
        payload = b'<!DOCTYPE a [<!ENTITY x SYSTEM "file:///secret">]><a>&x;</a>'
        with self.assertRaises(IntakeError):
            parse_xml(payload)
        with self.assertRaises(IntakeError):
            parse_xml(payload.decode("ascii").encode("utf-16"))

    def test_zip_paths_are_checked_before_xml_is_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("../escape.xml", VALID_XML)
            with self.assertRaises(IntakeError):
                read_sources(path)
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("C:/escape.xml", VALID_XML)
            with self.assertRaises(IntakeError):
                read_sources(path)

    def test_zip_identity_and_order_are_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("b.xml", VALID_XML)
                archive.writestr("a.xml", VALID_XML)
            kind, members, digest = read_sources(path)
            self.assertEqual(kind, "ZIP")
            self.assertEqual([item.name for item in members], ["a.xml", "b.xml"])
            self.assertEqual(len(digest), 64)


class AuditTests(unittest.TestCase):
    def test_registry_has_typed_traceable_rules(self):
        validate_registry()
        self.assertTrue(all(rule["authority"] and rule["evidence_contract"] for rule in RULES))

    def test_valid_xsd_is_not_reported_as_epip_conformant(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "valid.xml"
            source.write_bytes(VALID_XML)
            result = audit(source, SCHEMA_PATH)
        record = result["records"][0]
        self.assertEqual(record["well_formedness"], "WELL_FORMED")
        self.assertEqual(record["xsd_validation"], "XSD_VALID")
        profile = [item for item in result["findings"] if item["rule_id"] == "NETEX-PROFILE-001"]
        self.assertEqual(profile[0]["status"], "HUMAN_REVIEW_REQUIRED")
        self.assertNotIn("EPIP_CONFORMANT", json_report(result))

    def test_malformed_and_xsd_invalid_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            malformed = Path(tmp) / "malformed.xml"
            malformed.write_text("<a>", encoding="utf-8")
            result = audit(malformed, SCHEMA_PATH)
        self.assertEqual(result["records"][0]["well_formedness"], "NOT_WELL_FORMED")
        self.assertEqual(result["records"][0]["xsd_validation"], "XSD_NOT_EVALUABLE")

        with tempfile.TemporaryDirectory() as tmp:
            invalid = Path(tmp) / "invalid.xml"
            invalid.write_text("<wrong-root/>", encoding="utf-8")
            result = audit(invalid, SCHEMA_PATH)
        self.assertEqual(result["records"][0]["well_formedness"], "WELL_FORMED")
        self.assertEqual(result["records"][0]["xsd_validation"], "XSD_INVALID")

    def test_replay_and_reports_are_deterministic_and_redact_absolute_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "repeat.xml"
            source.write_bytes(VALID_XML)
            first = audit(source, SCHEMA_PATH)
            second = audit(source, SCHEMA_PATH)
        self.assertEqual(json_report(first), json_report(second))
        self.assertEqual(markdown_report(first), markdown_report(second))
        self.assertNotIn(tmp, json_report(first))

    def test_duplicate_identifier_is_review_only(self):
        fixture = Path(__file__).parent / "fixtures" / "duplicate_id_candidate.xml"
        result = audit(fixture, SCHEMA_PATH)
        findings = [item for item in result["findings"] if item["rule_id"] == "NETEX-IDENTITY-001"]
        self.assertTrue(findings)
        self.assertTrue(all(item["status"] == "HUMAN_REVIEW_REQUIRED" for item in findings))
        self.assertTrue(all(item["authority"] == "L4_TDL_RECOMMENDATION" for item in findings))

    def test_unmapped_reference_is_inventoried_but_not_called_broken(self):
        fixture = Path(__file__).parent / "fixtures" / "broken_reference_candidate.xml"
        result = audit(fixture, SCHEMA_PATH)
        inventory = result["records"][0]["structural_inventory"]
        self.assertEqual(inventory["reference_attribute_count"], 1)
        self.assertEqual(inventory["reference_samples"][0]["value"], "not-present")
        self.assertFalse(any("REFERENCE" in item["rule_id"] for item in result["findings"]))
        self.assertEqual(result["records"][0]["xsd_validation"], "XSD_INVALID")

    def test_schema_identity_manifest_pins_every_local_dependency(self):
        manifest = json.loads((Path(__file__).parents[3] / "01_Research_Standards" / "NeTEx" / "schemas" / "v2.0.0" / "schema_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["dependency_count"], 458)
        self.assertEqual(manifest["commit"], "a94e5e1752bcc13aabb8a1f3d018dc08e6978f42")


if __name__ == "__main__":
    unittest.main()
