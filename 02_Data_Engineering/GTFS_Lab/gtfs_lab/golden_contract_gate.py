from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from .golden_contract import GoldenCaseError, has_approved_status, is_executable_authority, validate_case


def run_gate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    repo_area = Path(__file__).resolve().parents[1]
    example_dir = repo_area / "golden" / "cases" / "contract-smoke"
    example = json.loads((example_dir / "case.json").read_text(encoding="utf-8-sig"))
    validate_case(example, example_dir)
    checks.append({"check": "versioned_draft_example_hash_and_contract_valid", "status": "PASS"})
    with tempfile.TemporaryDirectory(prefix="tdl-golden-contract-") as tmp:
        base = Path(tmp)
        input_path = base / "input.zip"
        input_path.write_bytes(b"contract gate synthetic placeholder; not a GTFS archive")
        valid = {
            "case_id": "m03a-contract-smoke", "case_version": "1.0.0", "contract_version": "1.0.0",
            "status": "DRAFT", "purpose": "Validate contract shape only", "created_at_utc": "2026-09-29T00:00:00Z",
            "input": {"filename": "input.zip", "sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(), "format": "GTFS_STATIC_ZIP", "provenance": "SYNTHETIC"},
            "scope": ["contract metadata only"], "expected": [{"type": "STATUS", "target": "validation.status", "value": "PASS", "authority": "SYNTHETIC_INVARIANT"}],
            "excluded_expectations": ["full output bytes", "run_id", "timestamps", "local paths", "machine metadata"],
            "authority": {"basis": "SYNTHETIC_INVARIANT"}, "review": {},
            "engine_context": {"gtfs_lab_version": "1.0.0-dev", "validator_version": "1", "ruleset_id": "gtfs-lab-v1", "ruleset_version": "1"},
        }
        validate_case(valid, base)
        lifecycle_ok = not has_approved_status(valid)
        for status in ("UNDER_REVIEW", "SUPERSEDED", "RETIRED"):
            lifecycle_ok = lifecycle_ok and not has_approved_status({"status": status})
        approved = copy.deepcopy(valid)
        approved.update(status="APPROVED", review={"reviewed_by": "Reviewer", "reviewed_at_utc": "2026-09-29T00:00:00Z", "review_basis": "manual"})
        lifecycle_ok = lifecycle_ok and has_approved_status(approved) and is_executable_authority(approved, base)
        checks.append({"check": "approved_lifecycle_status_is_distinct_from_valid_executable_authority", "status": "PASS" if lifecycle_ok else "FAIL"})
        invalid_authority_cases = {
            "approved_authority_missing_review": {**copy.deepcopy(valid), "status": "APPROVED"},
            "incomplete_approved_authority_contract": {"status": "APPROVED"},
        }
        for name, candidate in invalid_authority_cases.items():
            try:
                authority = is_executable_authority(candidate, base)
            except (GoldenCaseError, TypeError):
                authority = False
            checks.append({"check": name, "status": "PASS" if not authority else "FAIL"})
        mutations = {
            "sha_absent": lambda c: c["input"].pop("sha256"),
            "sha_incorrect": lambda c: c["input"].update(sha256="0" * 64),
            "input_missing": lambda c: c["input"].update(filename="missing.zip"),
            "status_unknown": lambda c: c.update(status="PASS"),
            "approved_without_reviewer": lambda c: c.update(status="APPROVED"),
            "naive_review_timestamp": lambda c: (c.update(status="APPROVED"), c["review"].update(reviewed_by="Reviewer", reviewed_at_utc="2026-09-29T00:00:00", review_basis="manual")),
            "expectation_without_type": lambda c: c["expected"][0].pop("type"),
            "absolute_windows_path": lambda c: c["input"].update(filename="C:\\machine\\input.zip"),
            "absolute_posix_path": lambda c: c["input"].update(filename="/etc/passwd"),
            "parent_traversal_path": lambda c: c["input"].update(filename="../input.zip"),
            "empty_case_id": lambda c: c.update(case_id=" "),
            "unknown_contract_version": lambda c: c.update(contract_version="9.0.0"),
            "current_output_auto_accept": lambda c: c["expected"][0].update(source="CURRENT_OUTPUT"),
            "expectation_missing_authority": lambda c: c["expected"][0].pop("authority"),
        }
        for name, mutate in mutations.items():
            candidate = copy.deepcopy(valid)
            mutate(candidate)
            try:
                validate_case(candidate, base)
            except (GoldenCaseError, TypeError):
                checks.append({"check": name, "status": "PASS"})
            else:
                checks.append({"check": name, "status": "FAIL"})
    enforced_checks = len(checks)
    return {"gate": "TDL_GOLDEN_CASE_CONTRACT_GATE", "contract_version": "1.0.0", "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL", "checks": checks, "check_count": enforced_checks, "enforced_checks": enforced_checks, "pass_count": sum(c["status"] == "PASS" for c in checks), "limitations": {"approved_mutation_detection": "NOT_ENFORCED_IN_M03A"}, "executable_approved_cases": 0}


def main() -> int:
    result = run_gate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
