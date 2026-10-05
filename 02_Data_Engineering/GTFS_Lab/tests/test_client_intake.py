from __future__ import annotations

import hashlib
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from gtfs_lab.client_intake import InputValidationError, validate_gtfs_zip


TABLES = {
    "agency": "agency_name,agency_url,agency_timezone\nAgencia,https://example.test,Europe/Madrid\n",
    "stops": "stop_id,stop_lat,stop_lon\nS1,40.0,-3.0\n",
    "routes": "route_id,route_type\nR1,3\n",
    "trips": "route_id,service_id,trip_id\nR1,WK,T1\n",
    "stop_times": "trip_id,stop_sequence\nT1,1\n",
}


class ClientIntakeTests(unittest.TestCase):
    def _zip(self, path: Path, tables: dict[str, str] = TABLES) -> None:
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in tables.items():
                archive.writestr(f"{name}.txt", content)

    def test_valid_input_exposes_deterministic_identity_and_leaves_source_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "feed.zip"
            self._zip(source)
            before = source.read_bytes()
            digest = hashlib.sha256(before).hexdigest()
            summary = validate_gtfs_zip(source, now=datetime(2026, 10, 5, tzinfo=timezone.utc))
            self.assertEqual(summary.filename, "feed.zip")
            self.assertEqual(summary.source_sha256, digest)
            self.assertEqual(summary.dataset_id, "GTFS-" + digest[:16])
            self.assertEqual(summary.size_bytes, len(before))
            self.assertEqual(summary.intake_timestamp_utc, "2026-10-05T00:00:00Z")
            self.assertEqual(set(summary.tables), set(TABLES))
            self.assertEqual(source.read_bytes(), before)

    def test_missing_required_table_is_classified_as_invalid_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "feed.zip"
            self._zip(source, {key: value for key, value in TABLES.items() if key != "trips"})
            with self.assertRaisesRegex(InputValidationError, "BLOCKED_INPUT_INVALID.*trips.txt"):
                validate_gtfs_zip(source)

    def test_missing_required_column_is_classified_as_invalid_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "feed.zip"
            tables = dict(TABLES)
            tables["routes"] = "route_id\nR1\n"
            self._zip(source, tables)
            with self.assertRaisesRegex(InputValidationError, "BLOCKED_INPUT_INVALID.*route_type"):
                validate_gtfs_zip(source)

    def test_non_zip_and_malformed_zip_are_classified_as_invalid_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            non_zip = Path(temp) / "feed.txt"
            non_zip.write_text("not a ZIP", encoding="utf-8")
            with self.assertRaisesRegex(InputValidationError, "BLOCKED_INPUT_INVALID"):
                validate_gtfs_zip(non_zip)
            malformed = Path(temp) / "broken.zip"
            malformed.write_bytes(b"not a ZIP")
            with self.assertRaisesRegex(InputValidationError, "BLOCKED_INPUT_INVALID"):
                validate_gtfs_zip(malformed)


if __name__ == "__main__":
    unittest.main()
