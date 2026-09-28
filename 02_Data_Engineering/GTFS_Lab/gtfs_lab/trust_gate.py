from __future__ import annotations

import json

from .audit_contract import (
    AuditContractError,
    build_audit_manifest,
    normalize_finding,
    normalize_rule_result,
    normalize_validation_payload,
    stable_finding_id,
    validate_audit_manifest,
    validate_finding_transition,
)
from .core import RuleResult, result_dict


def _expect_contract_error(fn) -> None:
    try:
        fn()
    except AuditContractError:
        return
    raise AssertionError("expected AuditContractError")


def _base_finding(source_sha256: str = "a" * 64) -> dict:
    return {
        "rule_id": "GTFS-TEST-001",
        "table": "stops.txt",
        "row_locator": "record:2",
        "field": "stop_name",
        "observed_value": "Estación Ñandú",
        "expected_condition": "valor único y trazable",
        "technical_message": "fixture unicode",
        "evidence": {"source_sha256": source_sha256},
    }


def _reviewed_finding(state: str) -> dict:
    finding = _base_finding()
    finding.update(
        {
            "lifecycle_state": state,
            "review_required": True,
            "reviewed_by": "gate-reviewer",
            "review_evidence": {
                "reviewed_at_utc": "2026-09-28T15:00:00+00:00",
                "basis": "synthetic gate review evidence",
            },
        }
    )
    return finding


def run_gate() -> dict:
    checks: list[dict[str, str]] = []

    dataset = {
        "dataset_id": "GTFS-0123456789abcdef",
        "source_filename": "fixture.zip",
        "source_sha256": "a" * 64,
        "ingestion_timestamp_utc": "2026-09-28T00:00:00+00:00",
        "parser_version": "gtfs-lab-csv/1",
    }
    preservation_evidence = {
        "verified": True,
        "source_sha256": dataset["source_sha256"],
        "method": "gate-fixture-hash-verification",
    }
    manifest = build_audit_manifest(
        run_id="GTFSRUN-0123456789abcdef",
        dataset=dataset,
        gtfs_lab_version="gate-fixture",
        validator_version="1.0.0",
        original_preserved=True,
        preservation_evidence=preservation_evidence,
    )
    validate_audit_manifest(manifest)
    assert manifest["source_sha256"] == dataset["source_sha256"]
    assert manifest["parser_version"] == dataset["parser_version"]
    checks.append({"check": "manifest_derived_from_dataset_identity", "status": "PASS"})

    missing_hash_dataset = dict(dataset)
    missing_hash_dataset["source_sha256"] = None
    _expect_contract_error(
        lambda: build_audit_manifest(
            run_id="GTFSRUN-MISSINGHASH",
            dataset=missing_hash_dataset,
            gtfs_lab_version="gate-fixture",
            validator_version="1.0.0",
            original_preserved=True,
            preservation_evidence={"verified": True, "source_sha256": None},
        )
    )
    checks.append({"check": "missing_manifest_hash_rejected", "status": "PASS"})

    _expect_contract_error(
        lambda: build_audit_manifest(
            run_id="GTFSRUN-UNVERIFIED",
            dataset=dataset,
            gtfs_lab_version="gate-fixture",
            validator_version="1.0.0",
            original_preserved=True,
            preservation_evidence={"verified": False, "source_sha256": dataset["source_sha256"]},
        )
    )
    checks.append({"check": "unverified_preservation_rejected", "status": "PASS"})

    finding = _base_finding()
    first_id = stable_finding_id(finding)
    second_id = stable_finding_id(dict(finding))
    assert first_id == second_id
    unicode_copy = json.loads(json.dumps(finding, ensure_ascii=False))
    assert stable_finding_id(unicode_copy) == first_id
    changed_dataset = _base_finding("b" * 64)
    assert stable_finding_id(changed_dataset) != first_id
    _expect_contract_error(lambda: stable_finding_id(_base_finding("")))
    checks.append({"check": "finding_identity_hash_unicode_and_dataset_sensitive", "status": "PASS"})

    validate_finding_transition("DETECTED", "REPRODUCED")
    validate_finding_transition("REPRODUCED", "EVIDENCE_ATTACHED")
    validate_finding_transition("EVIDENCE_ATTACHED", "REVIEWED")
    validate_finding_transition("REVIEWED", "CONFIRMED")
    validate_finding_transition("CONFIRMED", "REPORTED")
    _expect_contract_error(lambda: validate_finding_transition("DETECTED", "REPORTED"))
    _expect_contract_error(lambda: validate_finding_transition("REPORTED", "DETECTED"))
    checks.append({"check": "finding_lifecycle_transitions_enforced", "status": "PASS"})

    for state in ("DATA_AMBIGUITY", "REQUIRES_CONTEXT", "REVIEWED", "CONFIRMED", "REPORTED"):
        missing_reviewer = _base_finding()
        missing_reviewer["lifecycle_state"] = state
        _expect_contract_error(lambda f=missing_reviewer: normalize_finding(f))

        explicit_false = _base_finding()
        explicit_false["lifecycle_state"] = state
        explicit_false["review_required"] = False
        _expect_contract_error(lambda f=explicit_false: normalize_finding(f))

        missing_evidence = _base_finding()
        missing_evidence.update(
            {"lifecycle_state": state, "review_required": True, "reviewed_by": "gate-reviewer"}
        )
        _expect_contract_error(lambda f=missing_evidence: normalize_finding(f))

        valid_reviewed = normalize_finding(_reviewed_finding(state))
        assert valid_reviewed["review_required"] is True
        assert valid_reviewed["reviewed_by"] == "gate-reviewer"
        assert valid_reviewed["review_evidence"]["basis"]
    checks.append({"check": "human_review_states_require_reviewer_and_evidence", "status": "PASS"})

    incomplete_review_evidence = _reviewed_finding("REVIEWED")
    incomplete_review_evidence["review_evidence"] = {"reviewed_at_utc": "2026-09-28T15:00:00+00:00"}
    _expect_contract_error(lambda: normalize_finding(incomplete_review_evidence))
    checks.append({"check": "incomplete_review_evidence_rejected", "status": "PASS"})

    actual_rule_result = RuleResult(
        rule_id="GTFS-TEST-001",
        version="1.0.0",
        scope="STRUCTURAL",
        severity="ERROR",
        description="fixture",
        source_reference="fixture",
        status="FAIL_TECHNICAL",
        checked_rows=1,
        finding_count=999,
        findings=[finding],
    )
    actual_payload = result_dict(actual_rule_result)
    normalized = normalize_rule_result(actual_payload)
    assert normalized["finding_count"] == 1
    assert normalized["findings"][0]["lifecycle_state"] == "DETECTED"
    assert normalized["findings"][0]["finding_id"] == first_id
    checks.append({"check": "actual_rule_result_roundtrip_normalized", "status": "PASS"})

    repeated = normalize_validation_payload(
        {"rules": [actual_payload], "findings": [finding], "finding_count": 2}
    )
    assert repeated["finding_count"] == 1
    assert len(repeated["findings"]) == 1
    checks.append({"check": "identical_repeated_findings_deduplicated_explicitly", "status": "PASS"})

    conflicting = dict(finding)
    conflicting["technical_message"] = "different representation"
    _expect_contract_error(
        lambda: normalize_validation_payload(
            {"rules": [actual_payload], "findings": [conflicting]}
        )
    )
    checks.append({"check": "conflicting_duplicate_findings_rejected", "status": "PASS"})

    _expect_contract_error(
        lambda: normalize_rule_result(
            {
                "rule_id": "GTFS-TEST-INVALID",
                "severity": "ERROR",
                "status": "UNKNOWN",
                "findings": [],
            }
        )
    )
    checks.append({"check": "invalid_rule_status_rejected", "status": "PASS"})

    return {
        "gate": "TDL_TRUST_CONTRACT_GATE",
        "status": "PASS",
        "checks": checks,
        "check_count": len(checks),
    }


def main() -> int:
    result = run_gate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
