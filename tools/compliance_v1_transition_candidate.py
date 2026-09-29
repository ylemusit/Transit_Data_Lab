"""Build a review-only Compliance V1 evaluator identity transition candidate.

This writes only to a new evidence directory. It never persists into the
authoritative Compliance database or replaces the frozen package.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from compliance_v1_engine import VERSION
from compliance_v1_pack import EVIDENCE, build_package

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate"
PREDECESSOR_PACKAGE_SHA256 = "2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981"
PREDECESSOR_DB_SHA256 = "4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B"
PREDECESSOR_FREEZE_SHA256 = "3BBB6D87500608364972CFE841D6B2D3D03558FC73F1960A28579905FAEC6A3E"
EVALUATOR_SHA256 = "60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb"
TRANSITION_ID = "COMPLIANCE_V1_IMPLEMENTATION_TRANSITION_V1_TO_V2"
CONFIG = (
    "gtfs_max_file_bytes=536870912; gtfs_max_rows=1000000; "
    "gtfs_max_logical_record_bytes=4194304; gtfs_max_field_bytes=131072; "
    "gtfs_max_columns=256; netex_max_bytes=1048576; "
    "complete declared scope required; limits are implementation guards"
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def candidate_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")


def build_candidate() -> tuple[dict, dict]:
    if VERSION != "compliance-v1/2":
        raise RuntimeError(f"unexpected evaluator version: {VERSION}")
    evaluator_sha = sha_bytes((ROOT / "tools/compliance_v1_engine.py").read_bytes())
    if evaluator_sha != EVALUATOR_SHA256:
        raise RuntimeError("candidate evaluator source hash mismatch")
    historical = json.loads((EVIDENCE / "package.json").read_text(encoding="utf-8"))
    historical_sha = sha_bytes((EVIDENCE / "package.json").read_bytes())
    if historical_sha != PREDECESSOR_PACKAGE_SHA256:
        raise RuntimeError("frozen package identity mismatch")

    package = build_package()
    for row in package["tables"]["audit.rules"]:
        contract = json.loads(row["validation_expression"])
        contract["configuration"] = CONFIG
        contract["evaluator"] = VERSION
        contract["evaluator_sha256"] = evaluator_sha
        row["validation_expression"] = json.dumps(contract, sort_keys=True, ensure_ascii=False)
    # Re-derive the package so the candidate is proven deterministic.
    repeated = build_package()
    for row in repeated["tables"]["audit.rules"]:
        contract = json.loads(row["validation_expression"])
        contract["configuration"] = CONFIG
        contract["evaluator"] = VERSION
        contract["evaluator_sha256"] = evaluator_sha
        row["validation_expression"] = json.dumps(contract, sort_keys=True, ensure_ascii=False)
    if package != repeated:
        raise RuntimeError("candidate package generator replay mismatch")

    manifest = {
        "transition_id": TRANSITION_ID,
        "candidate_status": "UNDER_REVIEW",
        "predecessor_package": PREDECESSOR_PACKAGE_SHA256,
        "predecessor_package_sha256": PREDECESSOR_PACKAGE_SHA256,
        "candidate_package_sha256": sha_bytes(candidate_bytes(package)),
        "transition_reason": "IMPLEMENTATION_CHANGE",
        "technical_reason": [
            "incremental CSV processing",
            "removed prototype 10000-row and 1 MiB GTFS inspection limits",
            "explicit implementation resource guards; no semantic rule change",
        ],
        "package_schema_version": package["version"],
        "generator_identity": {
            "package_generator_path": "tools/compliance_v1_pack.py",
            "package_generator_sha256": sha_bytes((ROOT / "tools/compliance_v1_pack.py").read_bytes()),
            "transition_builder_path": "tools/compliance_v1_transition_candidate.py",
            "transition_builder_sha256": sha_bytes(Path(__file__).read_bytes()),
            "replay": "PASS",
        },
        "rule_id": "V1-RULE-GTFS",
        "rule_version_before": "compliance-v1/1",
        "rule_version_after": "compliance-v1/1",
        "evaluator_version_before": "compliance-v1/1",
        "evaluator_version_after": VERSION,
        "evaluator_sha_before": json.loads((EVIDENCE / "freeze.json").read_text(encoding="utf-8"))["files"]["tools/compliance_v1_engine.py"].lower(),
        "evaluator_sha_after": evaluator_sha,
        "reference_spec_identity_unchanged": True,
        "historical_package_unchanged": True,
        "historical_db_sha256": PREDECESSOR_DB_SHA256,
        "historical_freeze_sha256": PREDECESSOR_FREEZE_SHA256,
        "approval_status": "UNDER_REVIEW_NOT_APPROVED",
        "authoritative_current_pointer_changed": False,
        "holdout_accessed": False,
        "candidate_replay_status": "PASS",
    }
    if manifest["evaluator_sha_before"] != "efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70":
        raise RuntimeError("historical evaluator identity mismatch")
    return package, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    package, manifest = build_candidate()
    package_bytes = candidate_bytes(package)
    package_path = output / "package_candidate.json"
    package_path.write_bytes(package_bytes)
    manifest["candidate_package_file_sha256"] = sha_bytes(package_bytes)
    (output / "transition_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS", "output": str(output), **manifest}, indent=2))


if __name__ == "__main__":
    main()
