import csv
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.synthetic_resource_benchmark import generate_fixture, predicted_peak_exceeds_envelope


class SyntheticResourceBenchmarkTests(unittest.TestCase):
    def test_same_scale_is_byte_deterministic_and_records_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = generate_fixture(root / "first.zip", 2)
            second = generate_fixture(root / "second.zip", 2)
            self.assertEqual(first["sha256"], second["sha256"])
            self.assertEqual(first["scale_factor"], 2)
            self.assertEqual(first["data_row_counts"]["stop_times.txt"], 2000)
            self.assertEqual(first["row_counts_including_header"]["stop_times.txt"], 2001)
            self.assertEqual(first["zip_bytes"], (root / "first.zip").stat().st_size)

    def test_relational_references_resolve_and_scale_preserves_unique_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "feed.zip"
            manifest = generate_fixture(fixture, 1)
            with zipfile.ZipFile(fixture) as archive:
                rows = {name: list(csv.DictReader(archive.read(name).decode().splitlines()))
                        for name in ("routes.txt", "stops.txt", "trips.txt", "stop_times.txt")}
            routes = {row["route_id"] for row in rows["routes.txt"]}
            stops = {row["stop_id"] for row in rows["stops.txt"]}
            trips = {row["trip_id"]: row["route_id"] for row in rows["trips.txt"]}
            self.assertEqual(len(trips), len(rows["trips.txt"]))
            self.assertTrue(all(route in routes for route in trips.values()))
            self.assertTrue(all(row["trip_id"] in trips and row["stop_id"] in stops
                                for row in rows["stop_times.txt"]))
            self.assertEqual(manifest["data_row_counts"]["stop_times.txt"], len(rows["stop_times.txt"]))

    def test_refuses_to_overwrite_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "feed.zip"
            fixture.write_bytes(b"preserve")
            with self.assertRaises(FileExistsError):
                generate_fixture(fixture, 1)
            self.assertEqual(fixture.read_bytes(), b"preserve")

    def test_next_scale_prediction_preserves_half_available_ram(self):
        available = 10 * 1024**3
        self.assertFalse(predicted_peak_exceeds_envelope(4 * 1024**3, available))
        self.assertTrue(predicted_peak_exceeds_envelope(5 * 1024**3, available))


if __name__ == "__main__":
    unittest.main()
