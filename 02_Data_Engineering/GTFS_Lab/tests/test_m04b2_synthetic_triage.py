from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "02_Data_Engineering" / "GTFS_Lab"))
ENGINE_PATH = ROOT / "tools" / "compliance_v1_engine.py"
spec = importlib.util.spec_from_file_location("compliance_v1_engine_m04b2", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)

GTFS = {
    "trips.txt": b"trip_id,route_id,service_id\nt1,r1,s1\n",
    "stops.txt": b"stop_id,location_type\ns1,0\n",
    "stop_times.txt": b"trip_id,stop_id,stop_sequence\nt1,s1,1\n",
}


def run_compliance(stop_times: bytes):
    return engine.inspect_gtfs({**GTFS, "stop_times.txt": stop_times}, "v", "v")


def write_shapes_zip(path: Path, content: bytes):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("shapes.txt", content)


class M04B2SyntheticTriageTests(unittest.TestCase):
    def validate_shapes(self, archive):
        from gtfs_lab.ingestion import _validate_member
        info = archive.getinfo("shapes.txt")
        return _validate_member(archive, info, "shapes")

    def test_ingestion_empty_whitespace_quoted_and_immutable(self):
        samples = [
            (b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\nA,43.1,-5.8,1\n", 0),
            (b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n\n\nA,43.1,-5.8,1\n\n", 3),
            (b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n  \nA,43.1,-5.8,1\n", 1),
            (b'shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n"A,""B",43.1,-5.8,1\n', 0),
        ]
        for content, empty_count in samples:
            with self.subTest(empty_count=empty_count, sample=content[:55]), tempfile.TemporaryDirectory() as temp:
                source = Path(temp) / "source.zip"
                write_shapes_zip(source, content)
                before = hashlib.sha256(source.read_bytes()).hexdigest()
                with zipfile.ZipFile(source) as archive:
                    raw, _, _, rows, warnings = self.validate_shapes(archive)
                from gtfs_lab.ingestion import load_dataset
                context = load_dataset(source, Path(temp) / "runs")
                self.assertEqual(raw, content)
                self.assertEqual(rows, 1)
                self.assertEqual(context.dataset.parser_version, "gtfs-lab-csv/2")
                self.assertEqual(context.tables["shapes"].read_bytes(), content)
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
                empty_warning = next((w for w in warnings if w.startswith("EMPTY_CSV_RECORD_IGNORED table=shapes.txt")), None)
                if empty_count:
                    self.assertIsNotNone(empty_warning)
                    self.assertIn(f"count={empty_count}", empty_warning)
                    self.assertIn("count=", warnings[0])
                    self.assertIn("lines=", warnings[0])
                    self.assertIn(empty_warning, context.warnings)
                else:
                    self.assertIsNone(empty_warning)

    def test_malformed_nonempty_rows_still_fail(self):
        from gtfs_lab.ingestion import IngestionError
        samples = [
            b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\nA,43.1\n",
            b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\nA,43.1,-5.8,1,extra\n",
            b"shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n,,,,extra\n",
            b'shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n"   "\n',
        ]
        for content in samples:
            with self.subTest(sample=content[-30:]), tempfile.TemporaryDirectory() as temp:
                source = Path(temp) / "source.zip"
                write_shapes_zip(source, content)
                with zipfile.ZipFile(source) as archive, self.assertRaises(IngestionError):
                    self.validate_shapes(archive)

    def test_compliance_accepts_blank_rows_and_is_deterministic(self):
        payload = b"trip_id,stop_id,stop_sequence\nt1,s1,1\n\n  \nt1,s1,2\n"
        first, second = run_compliance(payload), run_compliance(payload)
        self.assertEqual(first, second)
        self.assertEqual(first["result"], "PASS")

    def test_rows_at_old_limits_and_materially_above(self):
        for rows in (9_999, 10_000, 10_001, 25_000, 100_000):
            with self.subTest(rows=rows):
                content = b"trip_id,stop_id,stop_sequence\n" + b"t1,s1,1\n" * rows
                answer = run_compliance(content)
                self.assertEqual(answer["result"], "PASS")
                self.assertFalse(answer["legal_conclusion_allowed"])

    def test_byte_sizes_around_old_limit(self):
        for size in (1024 * 1024 - 1, 1024 * 1024, 1024 * 1024 + 1):
            with self.subTest(bytes=size):
                header = b"trip_id,stop_id,stop_sequence,note\n"
                row_prefix = b"t1,s1,1,"
                count = 9
                filler_bytes = size - len(header) - count * (len(row_prefix) + 1)
                each, remainder = divmod(filler_bytes, count)
                content = header + b"".join(
                    row_prefix + b"x" * (each + (index < remainder)) + b"\n"
                    for index in range(count)
                )
                self.assertEqual(len(content), size)
                self.assertEqual(run_compliance(content)["result"], "PASS")

    def test_combined_large_row_and_byte_case(self):
        rows = 100_001
        content = b"trip_id,stop_id,stop_sequence,note\n" + b"t1,s1,1,0123456789\n" * rows
        self.assertGreater(len(content), 1024 * 1024)
        answer = run_compliance(content)
        self.assertEqual(answer["result"], "PASS")

    def test_path_adapter_scales_and_emits_processing_evidence(self):
        from gtfs_lab.compliance_adapter import inspect_fixed_stop_references
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tables = {
                "trips": root / "trips.txt",
                "stops": root / "stops.txt",
                "stop_times": root / "stop_times.txt",
            }
            tables["trips"].write_bytes(GTFS["trips.txt"])
            tables["stops"].write_bytes(GTFS["stops.txt"])
            large = b"trip_id,stop_id,stop_sequence,note\n" + b"t1,s1,1,0123456789\n" * 100_001
            tables["stop_times"].write_bytes(large)
            ctx = SimpleNamespace(
                tables=tables,
                dataset=SimpleNamespace(dataset_id="synthetic", source_sha256="0" * 64),
            )
            answer = inspect_fixed_stop_references(ctx)
            self.assertEqual(answer["result"], "PASS")
            self.assertEqual(answer["rule_version"], "compliance-v1/1")
            self.assertEqual(answer["evaluator_version"], "compliance-v1/2")
            self.assertEqual(answer["findings"], [])
            self.assertEqual(len(large.splitlines()) - 1, 100_001)
            self.assertGreater(len(large), 1024 * 1024)

    def test_single_record_resource_limit(self):
        prefix = b"trip_id,stop_id,stop_sequence,note\nt1,s1,1,"
        content = prefix + b"x" * engine.MAX_RECORD_BYTES + b"\n"
        self.assertEqual(run_compliance(content)["result"], "INSPECTION_ERROR")

    def test_file_row_and_column_guards_remain_active(self):
        with patch.object(engine, "MAX_GTFS_FILE_BYTES", 1):
            self.assertEqual(run_compliance(GTFS["stop_times.txt"])["result"], "INSPECTION_ERROR")
        with patch.object(engine, "MAX_ROWS", 1):
            content = b"trip_id,stop_id,stop_sequence\nt1,s1,1\nt1,s1,2\n"
            self.assertEqual(run_compliance(content)["result"], "INSPECTION_ERROR")
        with patch.object(engine, "MAX_COLUMNS", 2):
            self.assertEqual(run_compliance(GTFS["stop_times.txt"])["result"], "INSPECTION_ERROR")
        with patch.object(engine, "MAX_FIELD_BYTES", 1):
            self.assertEqual(run_compliance(GTFS["stop_times.txt"])["result"], "INSPECTION_ERROR")


if __name__ == "__main__":
    unittest.main()
