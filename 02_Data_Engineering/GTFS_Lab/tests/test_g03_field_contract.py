from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from gtfs_lab.g03_field_contract import (
    FieldContractError,
    load_field_contract,
    validate_field_contract,
)


class G03FieldContractTests(unittest.TestCase):
    def setUp(self):
        self.payload, self.result = load_field_contract()

    def field(self, file_name: str, field_name: str) -> dict:
        file_entry = next(item for item in self.payload["files"] if item["file_name"] == file_name)
        return next(item for item in file_entry["fields"] if item["field_name"] == field_name)

    def invalid(self, mutate, message: str):
        payload = copy.deepcopy(self.payload)
        mutate(payload)
        with self.assertRaisesRegex(FieldContractError, message):
            validate_field_contract(payload)

    def test_valid_contract_loads_against_g01_and_stays_blocked(self):
        self.assertEqual("VALIDATED_WITH_METADATA_GAPS", self.result["status"])
        self.assertEqual("2026-04-27", self.result["specification_revision"])
        self.assertEqual(14, self.result["normalized_files"])
        self.assertEqual(132, self.result["normalized_fields"])
        self.assertEqual([], self.result["field_metadata_complete_for_g03"])
        self.assertFalse(self.result["header_schema_unlocked"])
        self.assertFalse(self.result["field_type_unlocked"])

    def test_revision_and_parent_catalog_must_match(self):
        self.invalid(lambda p: p.update(specification_revision="2026-04-28"), "revision")
        self.invalid(lambda p: p.update(parent_file_catalog="other.json"), "parent catalog mismatch")
        self.invalid(lambda p: p.update(parent_file_catalog_schema_version="2.0.0"), "parent catalog schema")

    def test_duplicate_file_is_rejected(self):
        self.invalid(lambda p: p["files"].append(copy.deepcopy(p["files"][0])), "duplicate file definition")

    def test_duplicate_field_is_rejected(self):
        def duplicate(payload):
            fields = payload["files"][0]["fields"]
            fields[-1] = copy.deepcopy(fields[0])
        self.invalid(
            duplicate,
            "duplicate field definition",
        )

    def test_unknown_presence_and_type_are_rejected(self):
        self.invalid(lambda p: self._field_in(p, "agency.txt", "agency_name").update(presence="MUST"), "unknown presence")
        self.invalid(lambda p: self._field_in(p, "agency.txt", "agency_name").update(type="MAGIC"), "unknown type token")
        self.invalid(
            lambda p: p["type_vocabulary"].append(
                {
                    "token": "MAGIC",
                    "official_source_types": ["Magic"],
                    "observed_field_count": 1,
                    "definition": {
                        "summary": "A magic value.",
                        "status": "EXPLICIT",
                        "source_locator": "https://gtfs.org/documentation/schedule/reference/#field-types",
                    },
                }
            ),
            "type vocabulary does not match",
        )

    def test_malformed_condition_is_rejected(self):
        def mutate(payload):
            field = self._field_in(payload, "agency.txt", "agency_id")
            field["presence"] = "CONDITIONALLY_REQUIRED"
            field["condition"] = {
                "operator": "FIELD_VALUE_EQUALS",
                "expression": {"op": "FIELD_VALUE_EQUALS", "file": "agency.txt"},
                "normalization_status": "NORMALIZED",
                "source_reference": {
                    "file_name": "agency.txt",
                    "field_name": "agency_id",
                    "reference_anchor": "https://gtfs.org/documentation/schedule/reference/#agencytxt",
                    "specification_revision": "2026-04-27",
                    "source_locator": "official field row",
                },
            }
        self.invalid(mutate, "FIELD_VALUE_EQUALS requires field and value")

    def test_missing_source_reference_is_rejected(self):
        self.invalid(
            lambda p: self._field_in(p, "agency.txt", "agency_name").update(source_reference={}),
            "source reference identity mismatch|missing or invalid reference anchor",
        )

    def test_malformed_enum_and_range_are_rejected(self):
        self.invalid(
            lambda p: self._field_in(p, "agency.txt", "cemv_support").update(
                allowed_values=[{"value": "0"}, {"value": "0"}],
                allowed_values_status="EXPLICIT_OFFICIAL_LIST",
            ),
            "duplicate enum option",
        )
        self.invalid(
            lambda p: self._field_in(p, "stops.txt", "stop_lat").update(
                range={"min": 90, "max": -90}, range_status="NORMATIVE_RANGE"
            ),
            "contradictory range bounds",
        )

    def test_deferred_g01_file_cannot_be_promoted(self):
        payload = copy.deepcopy(self.payload)
        deferred = next(
            item for item in json.loads(
                (Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_2026_04_27.json").read_text(encoding="utf-8")
            )["files"] if item["tdl_v1_support"] == "DEFERRED"
        )
        payload["files"][0]["file_name"] = deferred["file_name"]
        with self.assertRaisesRegex(FieldContractError, "deferred G01 file"):
            validate_field_contract(payload)

    def test_extension_policy_stays_unresolved_and_does_not_reject_extra_headers(self):
        self.assertEqual("NOT_NORMATIVELY_RESOLVED", self.payload["extension_policy"]["status"])
        self.assertEqual("DO_NOT_FAIL_SOLELY_FOR_EXTRA_FIELD", self.payload["extension_policy"]["unknown_header_action"])

    def test_serialization_and_source_order_are_deterministic(self):
        canonical = json.dumps(self.payload, ensure_ascii=False, indent=2) + "\n"
        contract_path = Path(__file__).resolve().parents[1] / "spec" / "gtfs_schedule_fields_2026_04_27.json"
        self.assertEqual(canonical, contract_path.read_text(encoding="utf-8"))
        self.assertEqual(
            [item["file_name"] for item in self.payload["files"]],
            [item["file_name"] for item in self.payload["files"]],
        )

    @staticmethod
    def _field_in(payload: dict, file_name: str, field_name: str) -> dict:
        file_entry = next(item for item in payload["files"] if item["file_name"] == file_name)
        return next(item for item in file_entry["fields"] if item["field_name"] == field_name)


if __name__ == "__main__":
    unittest.main()
