from __future__ import annotations

import hashlib
import json
from pathlib import Path


FIXTURES = Path("02_Data_Engineering/NeTEx_Lab/tests/fixtures")
CASES = [
    ("NETEX-SYN-001", "valid_minimal.xml", "XSD-valid PublicationDelivery", "PASS", "SYNTHETIC"),
    ("NETEX-SYN-002", "malformed.xml", "Malformed XML", "FAIL_TECHNICAL", "SYNTHETIC"),
    ("NETEX-SYN-003", "xsd_invalid.xml", "Well-formed, XSD-invalid XML", "FAIL_TECHNICAL", "SYNTHETIC"),
    ("NETEX-SYN-004", "broken_reference_candidate.xml", "Reference target candidate", "NOT_EVALUABLE", "SYNTHETIC"),
    ("NETEX-SYN-005", "duplicate_id_candidate.xml", "Duplicate identifier candidate", "HUMAN_REVIEW_REQUIRED", "SYNTHETIC"),
    ("NETEX-SYN-006", "temporal_inconsistency_candidate.xml", "Temporal inconsistency candidate", "NOT_EVALUABLE", "SYNTHETIC"),
    ("NETEX-SYN-007", "dtd_external.xml", "DTD/entity security rejection", "FAIL_TECHNICAL", "SYNTHETIC"),
]


def main() -> int:
    records = []
    for case_id, name, purpose, expected, source_type in CASES:
        path = FIXTURES / name
        records.append({"case_id": case_id, "path": f"tests/fixtures/{name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "source_type": source_type, "corpus_split": "DEVELOPMENT", "purpose": purpose,
                        "expected_layer_status": expected,
                        "limitation": "A candidate fixture is not a normative EPIP assertion unless an implemented, sourced rule evaluates it."})
    manifest = {"corpus_version": "1.0.0", "cases": records,
                "holdout_accessed": False, "operator_specific_fixtures": False,
                "public_feed_accessed": False}
    target = Path("02_Data_Engineering/NeTEx_Lab/tests/fixtures/corpus_manifest.json")
    target.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
