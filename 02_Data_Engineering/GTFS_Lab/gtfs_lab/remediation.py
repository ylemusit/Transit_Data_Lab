"""Instance-scoped, evidence-backed remediation for DEVELOPMENT datasets.

This module deliberately has no generic URL scheme inference. A proposal must
carry a case-specific human authorization and external evidence before apply.
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import io
import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT = "TDL_REMEDIATION_ENGINE_V1"
AUTHORIZATION = "HUMAN_APPROVED_CASE_SPECIFIC"
SAFE = "SAFE_DETERMINISTIC"
APPROVED_SOURCE_SHA256 = "3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf"


class RemediationError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_finding_id(finding: dict[str, Any]) -> str:
    """Stable identity for G03 findings, which predate the M01 finding envelope."""
    explicit = finding.get("finding_id")
    if isinstance(explicit, str) and explicit:
        return explicit
    keys = ("rule_id", "file", "row_locator", "field", "observed")
    identity = {key: finding.get(key) for key in keys}
    if not identity["rule_id"] or not identity["file"] or not identity["row_locator"]:
        raise RemediationError("finding lacks stable rule/file/locator identity")
    encoded = json.dumps(identity, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "G03-" + hashlib.sha256(encoded).hexdigest()


def _csv_location(payload: bytes, field: str, expected: str) -> tuple[str, int]:
    text = payload.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text, newline="")))
    hits = [(n, row.get(field)) for n, row in enumerate(rows, start=2) if row.get(field) == expected]
    if len(hits) != 1:
        raise RemediationError(f"expected exactly one {field}={expected!r}; found {len(hits)}")
    return text, hits[0][0]


def create_proposal(*, source_zip: Path, derived_zip: Path, dataset_id: str,
                    source_file: str, field: str, original_value: str,
                    proposed_value: str, locator: str, rule_id: str,
                    finding_id: str, external_evidence: dict[str, Any],
                    authorization: str) -> dict[str, Any]:
    """Validate and apply one authorized exact-cell change to a copied ZIP."""
    if authorization != AUTHORIZATION:
        raise RemediationError("case-specific human authorization is required")
    if not (source_zip.is_file() and source_zip.resolve() != derived_zip.resolve()):
        raise RemediationError("source must exist and derived path must be distinct")
    if not all(isinstance(external_evidence.get(k), str) and external_evidence[k].strip()
               for k in ("url", "observed_at_utc", "claim")):
        raise RemediationError("external evidence requires url, observed_at_utc, and claim")
    if dataset_id != "010" or source_file != "agency.txt" or field != "agency_url" or original_value != "empresarodil.es" or proposed_value != "https://empresarodil.es":
        raise RemediationError("no approved instance policy matches this proposal")
    if external_evidence["url"] != "https://empresarodil.es":
        raise RemediationError("external evidence URL does not match the approved case")
    expected_finding_id = stable_finding_id({
        "rule_id": rule_id, "file": source_file, "row_locator": "ROW:1",
        "field": field, "observed": original_value,
    })
    if finding_id != expected_finding_id or rule_id != "GTFS-G03-FIELD-TYPE":
        raise RemediationError("originating finding identity does not match the approved case")
    source_zip = source_zip.resolve()
    derived_zip = derived_zip.resolve()
    if derived_zip.exists():
        raise RemediationError("derived output already exists; refusing overwrite")
    before_bytes = source_zip.read_bytes()
    before_sha = sha256_bytes(before_bytes)
    if before_sha != APPROVED_SOURCE_SHA256:
        raise RemediationError("source SHA-256 does not match approved DEVELOPMENT dataset 010")
    with zipfile.ZipFile(io.BytesIO(before_bytes), "r") as zin:
        infos = zin.infolist()
        matches = [i for i in infos if i.filename == source_file]
        if len(matches) != 1:
            raise RemediationError("source archive must contain exactly one agency.txt")
        raw = zin.read(matches[0])
        text, row_number = _csv_location(raw, field, original_value)
        if f"data_row={row_number - 1}" not in locator:
            raise RemediationError("locator does not match the observed CSV row")
        old_cell = original_value.encode("utf-8")
        if raw.count(old_cell) != 1:
            raise RemediationError("source cell is not byte-unique; refusing ambiguous edit")
        updated = raw.replace(old_cell, proposed_value.encode("utf-8"), 1)
        _csv_location(updated, field, proposed_value)
        diff = "".join(difflib.unified_diff(
            text.splitlines(keepends=True), updated.decode("utf-8-sig").splitlines(keepends=True),
            fromfile=f"original/{source_file}", tofile=f"derived/{source_file}"))
        derived_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(derived_zip, "x") as zout:
            zout.comment = zin.comment
            for info in infos:
                content = updated if info.filename == source_file else zin.read(info)
                zout.writestr(info, content)
    derived_bytes = derived_zip.read_bytes()
    if source_zip.read_bytes() != before_bytes:
        derived_zip.unlink(missing_ok=True)
        raise RemediationError("source archive changed during remediation")
    now = datetime.now(timezone.utc).isoformat()
    return {
        "contract": CONTRACT, "contract_version": "1.0.0", "status": "APPLIED",
        "dataset_id": dataset_id, "original_value": original_value,
        "proposed_value": proposed_value, "source_file": source_file,
        "locator": locator, "csv_row_number": row_number,
        "originating_rule_id": rule_id, "originating_finding_id": finding_id,
        "external_evidence": external_evidence, "safety_classification": SAFE,
        "authorization": authorization, "source_path": str(source_zip),
        "derived_path": str(derived_zip), "before_sha256": before_sha,
        "derived_sha256": sha256_bytes(derived_bytes), "exact_diff": diff,
        "applied_at_utc": now, "original_dataset_unchanged": source_zip.read_bytes() == before_bytes,
        "reaudit": None,
    }


def attach_reaudit(record: dict[str, Any], *, before_findings: list[dict[str, Any]],
                   after_findings: list[dict[str, Any]], reproducible: bool) -> dict[str, Any]:
    """Record finding attribution using stable JSON identities from the audit output."""
    before = {stable_finding_id(f): f for f in before_findings}
    after = {stable_finding_id(f): f for f in after_findings}
    resolved = [before[k] for k in sorted(before.keys() - after.keys())]
    unchanged = [before[k] for k in sorted(before.keys() & after.keys())]
    new = [after[k] for k in sorted(after.keys() - before.keys())]
    record["reaudit"] = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "reproducible": bool(reproducible), "resolved_findings": resolved,
        "unchanged_findings": unchanged, "new_findings": new,
        "result_comparison": "PASS" if not new else "FAIL_NEW_FINDINGS",
    }
    return record


def acceptance(record: dict[str, Any]) -> dict[str, str]:
    reaudit = record.get("reaudit") or {}
    original_resolved = any(stable_finding_id(f) == record.get("originating_finding_id")
                            for f in reaudit.get("resolved_findings", []))
    return {
        "ORIGINAL_DATASET_UNCHANGED": "YES" if record.get("original_dataset_unchanged") else "NO",
        "DERIVED_DATASET_CREATED": "YES" if Path(record.get("derived_path", "")).is_file() else "NO",
        "CHANGE_ATTRIBUTION_COMPLETE": "YES" if all(record.get(k) for k in (
            "original_value", "proposed_value", "source_file", "locator", "originating_rule_id",
            "external_evidence", "safety_classification", "before_sha256", "derived_sha256", "exact_diff", "authorization")) else "NO",
        "ORIGINAL_FINDING_RESOLVED": "YES" if original_resolved else "NO",
        "NEW_UNRELATED_FINDINGS": str(len(reaudit.get("new_findings", []))),
        "REAUDIT_REPRODUCIBLE": "YES" if reaudit.get("reproducible") else "NO",
    }


def persist_evidence(record: dict[str, Any], path: Path) -> None:
    """Persist the complete case record without replacing prior evidence."""
    if path.exists():
        raise RemediationError("evidence output already exists; refusing overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def main() -> int:
    raise SystemExit("Remediation V1 is invoked through create_proposal(); see the contract report.")
