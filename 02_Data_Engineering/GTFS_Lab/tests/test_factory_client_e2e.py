import json
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from tools.factory_client_e2e import (
    generation_step_record,
    inspect_delivery_content,
    inspect_factory_zip,
    workflow_delivery_relative_path,
)


class DeliveryContentScanTests(unittest.TestCase):
    def test_clean_text_and_urls_pass_without_echoing_local_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "report.md").write_text("Consulta https://example.com/ruta", encoding="utf-8")

            result = inspect_delivery_content(root)

        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["path_matches"])

    def test_windows_local_path_in_text_is_detected_without_disclosure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "report.txt").write_text(r"Origen: P:\TransitDataLab\privado\feed.zip", encoding="utf-8")

            result = inspect_delivery_content(root)

        self.assertEqual("FAIL_PATH_FOUND", result["status"])
        self.assertEqual([{"file": "report.txt", "match_count": 1}], result["path_matches"])
        self.assertNotIn(temporary, json.dumps(result))

    def test_unreadable_pdf_is_reported_as_partial(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "client_report.pdf").write_bytes(b"%PDF test fixture")
            with patch("tools.factory_client_e2e._extract_pdf_text", return_value=None):
                result = inspect_delivery_content(root)

        self.assertEqual("PARTIAL_UNSCANNED_CONTENT", result["status"])
        self.assertEqual("NOT_AVAILABLE", result["pdf_text_scan"])
        self.assertEqual(1, result["pdf_files"])

    def test_extracted_pdf_text_is_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "client_report.pdf").write_bytes(b"%PDF test fixture")
            with patch("tools.factory_client_e2e._extract_pdf_text", return_value=r"Archivo C:\private\feed.zip"):
                result = inspect_delivery_content(root)

        self.assertEqual("FAIL_PATH_FOUND", result["status"])
        self.assertEqual([{"file": "client_report.pdf", "match_count": 1}], result["path_matches"])


class ReceiptPrivacyTests(unittest.TestCase):
    def test_generator_stdout_is_hashed_without_storing_local_paths(self):
        stdout = r"Generado en P:\private\source\feed.zip"

        record = generation_step_record(r"C:\runtime\python.exe", Path("generador.py"), "--generar-gtfs", 0, stdout)
        encoded = json.dumps(record)

        self.assertNotIn("P:\\private", encoded)
        self.assertNotIn("C:\\runtime", encoded)
        self.assertEqual(1, record["stdout_line_count"])
        self.assertEqual(64, len(record["stdout_sha256"]))

    def test_workflow_delivery_path_is_relative_and_scoped(self):
        with tempfile.TemporaryDirectory() as temporary:
            evidence = Path(temporary) / "evidence"
            delivery = evidence / "workflow" / "delivery"
            delivery.mkdir(parents=True)

            relative = workflow_delivery_relative_path(str(delivery), evidence)

        self.assertEqual("workflow/delivery", relative)
        self.assertNotIn(temporary, relative)

    def test_workflow_delivery_outside_evidence_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence"
            outside = root / "outside"
            outside.mkdir()

            with self.assertRaises(RuntimeError):
                workflow_delivery_relative_path(str(outside), evidence)


class FactoryZipIdentityTests(unittest.TestCase):
    def test_content_manifest_is_stable_when_zip_timestamps_change(self):
        names = {"agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "locations.geojson"}
        names.update(f"fixture_{index:02d}.txt" for index in range(26))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archives = [root / "first.zip", root / "second.zip"]
            timestamps = [(2026, 1, 1, 0, 0, 0), (2026, 1, 1, 0, 2, 0)]
            for archive_path, timestamp in zip(archives, timestamps):
                with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    for name in sorted(names):
                        info = zipfile.ZipInfo(name, date_time=timestamp)
                        info.compress_type = zipfile.ZIP_DEFLATED
                        archive.writestr(info, name.encode("utf-8"))
            zip_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in archives]

            first = inspect_factory_zip(archives[0])
            second = inspect_factory_zip(archives[1])

        self.assertEqual(32, first["entry_count"])
        self.assertNotEqual(zip_hashes[0], zip_hashes[1])
        self.assertEqual(first["member_content_sha256"], second["member_content_sha256"])
        self.assertEqual(first["content_manifest_sha256"], second["content_manifest_sha256"])


if __name__ == "__main__":
    unittest.main()
