"""Integrity, scope and portable delivery regression checks for 07/08."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.audit_delivery_v1 import (contained, digest, generate, model_netex, seal,
                                    semantic_digest, validate_model, verify_delivery, write)


class ModelChecks(unittest.TestCase):
    def setUp(self): self.model = model_netex()
    def altered(self, change):
        model = deepcopy(self.model); change(model); model["semantic_sha256"] = semantic_digest(model)
        with self.assertRaises(ValueError): validate_model(model)
    def test_historical_scope(self):
        validate_model(self.model)
        self.assertIsNone(self.model["identity"]["audit_execution_id"])
        self.assertEqual(self.model["conclusion"]["unique_control_counts"], {"FAIL_TECHNICAL": 1, "NOT_EVALUABLE": 1})
    def test_digest_tampering(self):
        self.model["label"] = "altered"
        with self.assertRaises(ValueError): validate_model(self.model)
    def test_unbound_source(self): self.altered(lambda m: m["identity"].update(source_sha256="0"*64))
    def test_orphan_case(self): self.altered(lambda m: m["controls"][0].update(case_ids=[]))
    def test_double_control(self): self.altered(lambda m: m["controls"].append(deepcopy(m["controls"][0])))
    def test_missing_control(self): self.altered(lambda m: m["controls"].pop())
    def test_false_release(self): self.altered(lambda m: m.update(release_state="PUBLIC_READY"))
    def test_inflated_count(self): self.altered(lambda m: m["conclusion"]["unique_control_counts"].update(FAIL_TECHNICAL=2))
    def test_unsafe_paths(self):
        for value in ("../secret", "C:/secret", "/secret", "a\\b"):
            with self.subTest(value=value), self.assertRaises(ValueError): contained(Path.cwd(), value)


class PortableChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tdl_delivery_")
        self.root = Path(self.temp.name) / "original"
        generate("NETEX", self.root)
    def tearDown(self): self.temp.cleanup()
    def test_relocation_without_checkout(self):
        relocated = self.root.with_name("other folder with spaces"); self.root.rename(relocated)
        result = subprocess.run([sys.executable, str(relocated / "VERIFICAR.py")], cwd=relocated,
                                capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)["standalone"])
        self.assertEqual(verify_delivery(relocated)["result"], "PASS")
    def test_changed_artifact(self):
        (self.root / "03_SOURCE_DELIVERY/malformed.xml").write_text("altered")
        with self.assertRaises(ValueError): verify_delivery(self.root)
    def test_unlisted_file(self):
        (self.root / "unexpected.txt").write_text("unexpected")
        with self.assertRaises(ValueError): verify_delivery(self.root)
    def test_resealed_inconsistent_view(self):
        path = self.root / "VIEW_CONSISTENCY.json"; value = json.loads(path.read_text())
        value["views"][0]["unique_control_counts"] = {"PASS": 2}; write(path, value); seal(self.root)
        with self.assertRaises(ValueError): verify_delivery(self.root)
    def test_resealed_external_index(self):
        (self.root / "INDEX.html").write_text('<a href="https://example.invalid">outside</a>')
        seal(self.root)
        with self.assertRaises(ValueError): verify_delivery(self.root)
    def test_pdf_identity(self):
        path = self.root / "01_DIRECCION/Informe_direccion.pdf"
        data = path.read_bytes(); model = json.loads((self.root / "02_MODELO/REPORT_MODEL.json").read_text())
        path.write_bytes(data.replace(model["semantic_sha256"].encode(), b"0"*64)); seal(self.root)
        with self.assertRaises(ValueError): verify_delivery(self.root)


if __name__ == "__main__": unittest.main()
