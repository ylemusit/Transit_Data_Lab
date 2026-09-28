from __future__ import annotations

import json

from .audit_contract import (
    AuditContractError,
    build_audit_manifest,
    normalize_rule_result,
    stable_finding_id,
    validate_audit_manifest,
)


def _expect_contract_error(fn) -> None:
    try:
        fn()
    except AuditContractError:
        return
    raise AssertionError("expected AuditContractError")


def run_gate() -> dict:
    checks: list[dict[str, str]] = []

    dataset = {
        "dataset_id": "GTFS-0123456789abcdef",
        "source_filename": "fixture.zip",
        "source_sha256": "a" * 64,
        "ingestion_timestamp_utc": "2026-09-28T00:00:00+00:00",
        "parser_version": "gtfs-lab-csv/1",
    }
    manifest = build_audit_manifest(
        run_id="GTFSRUN-0123456789abcdef",
        dataset=dataset,
        gtfs_lab_version="gate-fixture",
        validator_version="1.0.0",
    )
    validate_audit_manifest(manifest)
    checks.append({"check": "valid_manifest", "status": "PASS"})

    invalid_manifest = dict(manifest)
    invalid_manifest["source_sha256"] = "not-a-sha"
    _expect_contract_error(lambda: validate_audit_manifest(invalid_manifest))
    checks.append({"check": "invalid_sha_rejected", "status": "PASS"})

    finding = {
        "rule_id": "GTFS-TEST-001",
        "table": "stops.txt",
        "row_locator": "record:2",
        "field": "stop_id",
        "observed_value": "A",
        "expected_condition": "unique",
        "technical_message": "fixture",
        "evidence": {"source_sha256": "a" * 64},
    }
    first_id = stable_finding_id(finding)
    second_id = stable_finding_id(dict(finding))
    assert first_id == second_id
    checks.append({"check": "finding_id_deterministic", "status": "PASS"})

    normalized = normalize_rule_result(
        {
            "rule_id": "GTFS-TEST-001",
            "version": "1.0.0",
            "scope": "STRUCTURAL",
            "severity": "ERROR",
            "description": "fixture",
            "source_reference": "fixture",
            "status": "FAIL_TECHNICAL",
            "checked_rows": 1,
            "finding_count": 999,
            "findings": [finding],
        }
    )
    assert normalized["finding_count"] == 1
    assert normalized["findings"][0]["lifecycle_state"] == "DETECTED"
    assert normalized["findings"][0]["finding_id"] == first_id
    checks.append({"check": "rule_result_normalized", "status": "PASS"})

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
