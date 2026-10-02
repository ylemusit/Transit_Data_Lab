"""Synthetic evidence for controlled intake, replay and NOT_OK preservation."""
from __future__ import annotations

import argparse
import json
import stat
import tempfile
from pathlib import Path

from .client_workflow_e2e import write_fixture
from gtfs_lab.core import sha256_file
from gtfs_lab.test_bank import run_case, rebuild_register


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    if args.evidence.exists():
        raise FileExistsError("No sobrescribir evidencia")
    with tempfile.TemporaryDirectory(prefix="tb-") as folder:
        root = Path(folder)
        try:
            received = root / "Cliente con espacios" / "Autobús y ñ"
            received.mkdir(parents=True)
            source = received / ("Autobús de prueba — líneas y horarios " + "x" * 80 + ".zip")
            write_fixture(source)
            original_hash = sha256_file(source)
            bank = root / "BANK"
            accepted = run_case(source, bank, provenance="SYNTHETIC", metadata={"dataset_title": "Autobús de prueba"})
            assert accepted["result"] == "OK", accepted
            assert all(accepted["gates"].values())
            assert sha256_file(source) == original_hash
            corrupt = received / "inválido.zip"
            corrupt.write_bytes(b"not a ZIP")
            rejected = run_case(corrupt, bank, provenance="SYNTHETIC")
            assert rejected["result"] == "NOT_OK"
            assert rejected["failures"][0]["category"] == "ZIP"
            rows = rebuild_register(bank)
            assert [row["case_id"] for row in rows] == ["00001", "00002"]
            assert [row["result"] for row in rows] == ["OK", "NOT_OK"]
            delivery = bank / accepted["case_path"] / "DELIVERY"
            manifest_path = delivery / "bank_delivery_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            seal = json.loads((delivery / "bank_delivery_seal.json").read_text())
            assert seal["manifest_sha256"] == sha256_file(manifest_path)
            for name, expected in manifest["artifacts"].items():
                artifact = delivery / name
                assert sha256_file(artifact) == expected["sha256"]
                assert artifact.stat().st_size == expected["size_bytes"]
            workflow = delivery / "workflow"
            workflow_manifest = json.loads((workflow / "audit_manifest.json").read_text())
            workflow_seal = json.loads((workflow / "delivery_seal.json").read_text())
            assert workflow_seal["audit_manifest_sha256"] == sha256_file(workflow / "audit_manifest.json")
            for name, expected in workflow_manifest["delivery_artifacts"].items():
                assert sha256_file(workflow / name) == expected["sha256"]
            schema = json.loads((Path(__file__).resolve().parents[1] / "spec" / "test_bank_registry_v1.schema.json").read_text())
            for row in rows:
                assert set(schema["$defs"]["case"]["required"]) <= row.keys()
            failures = [json.loads(line) for line in (bank / "REGISTRY" / "FAILURE_REGISTER.jsonl").read_text().splitlines()]
            assert len(failures) == 1
            for failure in failures:
                assert set(schema["$defs"]["failure"]["required"]) <= failure.keys()
                assert failure["category"] == "ZIP" and failure["status"] == "OPEN"
            evidence = {"contract": "TDLTestBankSyntheticE2E", "version": "1.0.0", "result": "PASS",
                        "synthetic_only": True, "holdout_accessed": False,
                        "CASE_ALLOCATED": "YES", "SHORT_WORKSPACE": "YES",
                        "SOURCE_HASHED": "YES", "SOURCE_IMMUTABLE": "YES",
                        "AUDIT": "COMPLETED", "DELIVERY": "GENERATED", "REPLAY": "PASS",
                        "CASE_CLASSIFICATION": "OK", "REGISTRY_UPDATED": "YES",
                        "FAILURE_REGISTRY_VALID": "YES", "DELIVERY_HASHES": "VERIFIED",
                        "SEALS": "VERIFIED", "OPERATOR_SPECIFIC_CODE": "NO",
                        "REAL_OPERATOR_DATA": "NO", "HOLDOUT": "NOT_ACCESSED",
                        "long_unicode_original_retained": True, "source_immutable": True,
                        "accepted": accepted, "rejected": rejected,
                        "register_json_csv_jsonl_generated": all((bank / "REGISTRY" / name).is_file() for name in
                            ("TEST_BANK_REGISTER.json", "TEST_BANK_REGISTER.csv", "FAILURE_REGISTER.jsonl"))}
            args.evidence.parent.mkdir(parents=True, exist_ok=True)
            args.evidence.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"result": "PASS", "cases": 2, "findings": accepted["findings"]}))
        finally:
            for path in root.rglob("*"):
                if path.is_file():
                    path.chmod(stat.S_IREAD | stat.S_IWRITE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
