from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path("02_Data_Engineering/NeTEx_Lab").resolve()))
from netex_lab.audit import audit  # noqa: E402
from netex_lab.report import json_report, markdown_report  # noqa: E402
from netex_lab.schema import SCHEMA_PATH  # noqa: E402


FIXTURES = Path("02_Data_Engineering/NeTEx_Lab/tests/fixtures")
EXPECTED = {
    "valid_minimal.xml": ("WELL_FORMED", "XSD_VALID"),
    "malformed.xml": ("NOT_WELL_FORMED", "XSD_NOT_EVALUABLE"),
    "xsd_invalid.xml": ("WELL_FORMED", "XSD_INVALID"),
    "broken_reference_candidate.xml": ("WELL_FORMED", "XSD_INVALID"),
    "duplicate_id_candidate.xml": ("WELL_FORMED", "XSD_INVALID"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    original_hashes = {path.name: sha256(path) for path in sorted(FIXTURES.glob("*.xml"))}
    cases = []
    for name in ("valid_minimal.xml", "malformed.xml", "xsd_invalid.xml", "broken_reference_candidate.xml", "duplicate_id_candidate.xml"):
        source = FIXTURES / name
        first = audit(source, SCHEMA_PATH)
        second = audit(source, SCHEMA_PATH)
        serialized = json_report(first)
        if serialized != json_report(second) or markdown_report(first) != markdown_report(second):
            raise AssertionError(f"Replay mismatch for {name}")
        if str(source.resolve().parent) in serialized:
            raise AssertionError(f"Absolute path leaked into report for {name}")
        expected_well_formedness, expected_xsd = EXPECTED[name]
        record = first["records"][0]
        if (record["well_formedness"], record["xsd_validation"]) != (expected_well_formedness, expected_xsd):
            raise AssertionError(f"Unexpected layer status for {name}")
        if name == "duplicate_id_candidate.xml" and not any(
            item["rule_id"] == "NETEX-IDENTITY-001" and item["status"] == "HUMAN_REVIEW_REQUIRED"
            for item in first["findings"]
        ):
            raise AssertionError("Duplicate identifier did not remain a review-only diagnostic")
        if name == "broken_reference_candidate.xml" and any(
            "REFERENCE" in item["rule_id"] for item in first["findings"]
        ):
            raise AssertionError("Unmapped reference was incorrectly asserted")
        cases.append({"source_file": name, "source_sha256": sha256(source),
                      "well_formedness": record["well_formedness"],
                      "xsd_validation": record["xsd_validation"],
                      "finding_status_counts": first["rule_execution_summary"],
                      "replay": "PASS"})
    with tempfile.TemporaryDirectory() as temp:
        zip_path = Path(temp) / "synthetic.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.write(FIXTURES / "valid_minimal.xml", "feed.xml")
        zipped = audit(zip_path, SCHEMA_PATH)
        zipped_replay = audit(zip_path, SCHEMA_PATH)
        if zipped["records"][0]["xsd_validation"] != "XSD_VALID" or json_report(zipped) != json_report(zipped_replay):
            raise AssertionError("ZIP E2E or replay failed")
        if str(zip_path.parent) in json_report(zipped):
            raise AssertionError("Absolute ZIP input path leaked into report")
    after_hashes = {path.name: sha256(path) for path in sorted(FIXTURES.glob("*.xml"))}
    if original_hashes != after_hashes:
        raise AssertionError("Synthetic source fixture changed during replay")
    return {"e2e_version": "1.0.0", "corpus_type": "SYNTHETIC_DEVELOPMENT",
            "schema_identity": audit(FIXTURES / "valid_minimal.xml", SCHEMA_PATH)["schema_identity"],
            "cases": cases, "zip_intake": "PASS", "zip_replay": "PASS", "deterministic_replay": "PASS",
            "source_immutable": True, "holdout_accessed": False,
            "public_feed_accessed": False, "operator_specific_code": False,
            "absolute_paths_in_report": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.evidence.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"e2e": "PASS", "case_count": len(result["cases"]), "replay": result["deterministic_replay"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
