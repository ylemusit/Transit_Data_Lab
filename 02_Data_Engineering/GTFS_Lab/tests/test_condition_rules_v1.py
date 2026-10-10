from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from gtfs_lab.condition_rules_v1 import audit_agency_conditions


class AgencyConditionRuleTests(unittest.TestCase):
    def feed(self, agency: str, routes: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "feed.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("agency.txt", agency)
            archive.writestr("routes.txt", routes)
        return path

    def test_multi_agency_feed_requires_ids_and_resolves_route_reference(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone,agency_id\nA,https://a.example,Europe/Madrid,A\nB,https://b.example,Europe/Madrid,B\n",
            "route_id,route_type,agency_id\nr1,3,B\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual({"G-PLAN-01": "PASS", "G-PLAN-02": "PASS"}, statuses)
        self.assertEqual([], result["findings"])

    def test_missing_agency_header_makes_route_reference_not_evaluable(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone\nA,https://a.example,Europe/Madrid\nB,https://b.example,Europe/Madrid\n",
            "route_id,route_type,agency_id\nr1,3,missing\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual("FAIL_TECHNICAL", statuses["G-PLAN-01"])
        # The rule abstains on reference validity because the agency IDs are unavailable.
        self.assertEqual("NOT_EVALUABLE", statuses["G-PLAN-02"])
        self.assertTrue(any(row["locator"] == "header:agency_id" for row in result["findings"]))

    def test_supplied_orphan_route_agency_id_fails(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone,agency_id\nA,https://a.example,Europe/Madrid,A\nB,https://b.example,Europe/Madrid,B\n",
            "route_id,route_type,agency_id\nr1,3,missing\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual("FAIL_TECHNICAL", statuses["G-PLAN-02"])
        self.assertTrue(any(row["observed"] == "UNKNOWN_AGENCY_ID:missing" for row in result["findings"]))

    def test_single_agency_can_omit_agency_id(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone\nA,https://a.example,Europe/Madrid\n",
            "route_id,route_type\nr1,3\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual({"G-PLAN-01": "PASS", "G-PLAN-02": "PASS"}, statuses)

    def test_unknown_agency_cardinality_abstains(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone,agency_id\n",
            "route_id,route_type,agency_id\nr1,3,A\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual({"G-PLAN-01": "NOT_EVALUABLE", "G-PLAN-02": "NOT_EVALUABLE"}, statuses)

    def test_route_agency_id_is_required_when_agency_cardinality_is_multiple(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone,agency_id\nA,https://a.example,Europe/Madrid,A\nB,https://b.example,Europe/Madrid,B\n",
            "route_id,route_type\nr1,3\n",
        )
        result = audit_agency_conditions(source)
        statuses = {row["rule_id"]: row["status"] for row in result["rule_results"]}
        self.assertEqual("FAIL_TECHNICAL", statuses["G-PLAN-02"])

    def test_feed_hash_and_rule_identity_are_deterministic(self):
        source = self.feed(
            "agency_name,agency_url,agency_timezone,agency_id\nA,https://a.example,Europe/Madrid,A\nB,https://b.example,Europe/Madrid,B\n",
            "route_id,route_type,agency_id\nr1,3,A\n",
        )
        first = audit_agency_conditions(source)
        second = audit_agency_conditions(source)
        self.assertEqual(first, second)
        self.assertEqual("TDL_GTFS_CONDITIONAL_RULES_V1", first["contract"])
        self.assertEqual("GTFS_FIXED_FIELD_DEFINITION", first["reference"]["authority"])


if __name__ == "__main__":
    unittest.main()
