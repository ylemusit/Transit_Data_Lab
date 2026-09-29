"""Persist the M05-C result by referring to frozen M04 evidence, read-only."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gtfs_lab.audit_comparison import (
    RECORD_CONTRACT, RECORD_CONTRACT_VERSION, _canonical_bytes, _digest,
    render_comparison_report, verify_comparison_record,
)

SOURCES = {
    "baseline_summary": "reports/evidence/holdout_evaluation_v1/first_evaluation_summary.json",
    "candidate_summary": "reports/evidence/holdout_evaluation_v2/evaluation_summary.json",
    "historical_summary": "reports/evidence/m05c_historical_proof/summary.json",
}
OUT = ROOT / "reports/evidence/comparisons/M05C-HISTORICAL-PROOF-V1"


def source_snapshot(side: str) -> dict:
    reference = SOURCES[f"{side}_summary"]
    return {
        "snapshot_contract": "M05CHistoricalSourceSnapshot",
        "snapshot_contract_version": "1.0.0",
        "audit_id": "M04-B1-HOLDOUT" if side == "baseline" else "M04-B3-HOLDOUT",
        "source_ref": reference,
        "source_sha256": hashlib.sha256((ROOT / reference).read_bytes()).hexdigest(),
    }


def build_record(created_at_utc: str) -> tuple[dict, dict, dict]:
    baseline, candidate = source_snapshot("baseline"), source_snapshot("candidate")
    historical_bytes = (ROOT / SOURCES["historical_summary"]).read_bytes()
    summary = json.loads(historical_bytes.decode("utf-8"))
    rows = [{"dataset_id": row["dataset_id"], "lineage_unit": row["lineage_unit"],
             "result_change": row["result_change"]["status"], "attribution": row["attribution"],
             "supported_causes": row["supported_causes"], "evidence_state": row["evidence_state"],
             "comparability": row["comparability"]["status"], "evidence_refs": row["evidence_refs"]}
            for row in summary["datasets"]]
    causes = sorted({cause for row in rows for cause in row["supported_causes"]})
    reasons = sorted({reason for row in summary["datasets"] for reason in row["comparability"]["reasons"]})
    comparison = {
        "comparison_id": "M05C-HISTORICAL-PROOF-V1",
        "snapshot_contract_version": "M05CHistoricalSourceSnapshot/1.0.0",
        "change_attribution_contract_version": summary["comparison_engine_version"],
        "baseline_audit_id": baseline["audit_id"], "candidate_audit_id": candidate["audit_id"],
        "comparability": {"status": "PARTIALLY_COMPARABLE", "reasons": reasons},
        "identity_differences": [],
        "result_change": {"status": "HISTORICAL_MIXED", "changed": True,
                          "differences": [{"dataset_id": row["dataset_id"], "status": row["result_change"]} for row in rows]},
        "finding_change": {"changed": None, "changes": []},
        "attribution": "HISTORICAL_MIXED", "supported_causes": causes,
        "evidence_status": "PARTIAL", "evidence_refs": [ref for row in rows for ref in row["evidence_refs"]],
        "unresolved_reasons": reasons, "historical_rows": rows,
        "source_sha256": {"baseline": baseline["source_sha256"], "candidate": candidate["source_sha256"],
                          "historical_summary": hashlib.sha256(historical_bytes).hexdigest()},
    }
    payload = {"comparison_id": comparison["comparison_id"], "baseline_audit_id": baseline["audit_id"],
               "candidate_audit_id": candidate["audit_id"], "comparison": comparison,
               "source_artifacts": SOURCES}
    record = {**payload, "record_contract": RECORD_CONTRACT, "record_contract_version": RECORD_CONTRACT_VERSION,
              "created_at_utc": created_at_utc}
    record["integrity"] = {"baseline_snapshot_sha256": _digest(baseline),
                           "candidate_snapshot_sha256": _digest(candidate),
                           "comparison_payload_sha256": _digest(payload),
                           "record_sha256": _digest(record)}
    verify_historical_record(record)
    return record, baseline, candidate


def verify_historical_record(record: dict) -> bool:
    baseline, candidate = source_snapshot("baseline"), source_snapshot("candidate")
    historical_sha = hashlib.sha256((ROOT / SOURCES["historical_summary"]).read_bytes()).hexdigest()
    if record["comparison"]["source_sha256"] != {
        "baseline": baseline["source_sha256"], "candidate": candidate["source_sha256"],
        "historical_summary": historical_sha,
    }:
        return False
    return verify_comparison_record(record, baseline, candidate)


def main() -> None:
    existing_path = OUT / "comparison.json"
    old = json.loads(existing_path.read_text(encoding="utf-8")) if existing_path.exists() else None
    if old is not None and not verify_historical_record(old):
        raise RuntimeError("COMPARISON_HASH_MISMATCH: historical record")
    legacy_timestamp = "2026-09-29T00:00:00Z"
    if old is not None and old.get("created_at_utc") == legacy_timestamp:
        created_at = datetime.fromtimestamp(existing_path.stat().st_ctime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    else:
        created_at = old["created_at_utc"] if old is not None else datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    record, _, _ = build_record(created_at)
    data, report = _canonical_bytes(record), render_comparison_report(record)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, expected in (("comparison.json", data), ("report.md", report)):
        target = OUT / name
        if target.exists() and target.read_bytes() != expected:
            if name != "comparison.json" or old is None or old.get("created_at_utc") != legacy_timestamp or old.get("integrity") != record["integrity"]:
                raise RuntimeError(f"COMPARISON_RECORD_CONFLICT: {target}")
            target.write_bytes(expected)
        if not target.exists():
            target.write_bytes(expected)


if __name__ == "__main__":
    main()
