"""GoldenCase 1.0.0 metadata contract; expectations are never inferred here."""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

CONTRACT_VERSION = "1.0.0"
STATUSES = {"DRAFT", "UNDER_REVIEW", "APPROVED", "SUPERSEDED", "RETIRED"}
EXPECTATION_TYPES = {"EXACT", "SEMANTIC", "STATUS", "COUNT", "PRESENCE", "ABSENCE", "RELATION", "HASH"}
AUTHORITIES = {"TDL_CONTRACT", "GTFS_SPECIFICATION", "COMPLIANCE_FROZEN_SCOPE", "HUMAN_REVIEW", "SYNTHETIC_INVARIANT"}
PROVENANCE = {"SYNTHETIC", "PUBLIC_DATASET", "OPERATOR_PROVIDED", "DERIVED_FIXTURE"}
CHANGE_REASONS = {"DATASET_CORRECTION", "SPEC_INTERPRETATION_CHANGED", "RULESET_CHANGED", "ENGINE_DEFECT_CORRECTED", "GOLDEN_CASE_DEFECT", "SCOPE_CHANGED"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class GoldenCaseError(ValueError):
    pass


def has_approved_status(case: Any) -> bool:
    """Return only whether the object declares the APPROVED lifecycle status."""
    return isinstance(case, dict) and case.get("status") == "APPROVED"


def is_executable_authority(case: dict[str, Any], base_dir: Path) -> bool:
    """Validate a complete case before treating APPROVED as executable authority."""
    validate_case(case, base_dir)
    return has_approved_status(case)


def _utc(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0
    except (ValueError, OverflowError):
        return False


def validate_case(case: dict[str, Any], base_dir: Path) -> None:
    if not isinstance(case, dict):
        raise GoldenCaseError("case must be an object")
    for key in ("case_id", "case_version", "purpose"):
        if not isinstance(case.get(key), str) or not case[key].strip():
            raise GoldenCaseError(f"{key} must be non-empty")
    if case.get("contract_version") != CONTRACT_VERSION:
        raise GoldenCaseError("unknown contract_version")
    if case.get("status") not in STATUSES:
        raise GoldenCaseError("unknown status")
    if not _utc(case.get("created_at_utc")):
        raise GoldenCaseError("created_at_utc must be timezone-aware UTC")
    inp = case.get("input")
    if not isinstance(inp, dict) or not all(isinstance(inp.get(k), str) and inp[k].strip() for k in ("filename", "sha256", "format", "provenance")):
        raise GoldenCaseError("input requires filename, sha256, format and provenance")
    if not SHA256_RE.fullmatch(inp["sha256"]):
        raise GoldenCaseError("input sha256 must be 64 hexadecimal characters")
    if inp["provenance"] not in PROVENANCE:
        raise GoldenCaseError("unknown input provenance")
    if inp["format"] != "GTFS_STATIC_ZIP":
        raise GoldenCaseError("unsupported input format")
    rel = Path(inp["filename"])
    if rel.is_absolute() or PurePosixPath(inp["filename"]).is_absolute() or PureWindowsPath(inp["filename"]).is_absolute() or ".." in rel.parts:
        raise GoldenCaseError("input filename must be a relative repository path")
    input_path = (base_dir / rel).resolve()
    if not input_path.is_relative_to(base_dir.resolve()):
        raise GoldenCaseError("input filename resolves outside its case directory")
    if not input_path.is_file():
        raise GoldenCaseError("input file does not exist")
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    if digest.lower() != inp["sha256"].lower():
        raise GoldenCaseError("input sha256 does not match")
    if not isinstance(case.get("scope"), list) or not case["scope"] or any(not isinstance(x, str) or not x.strip() for x in case["scope"]):
        raise GoldenCaseError("scope must be an explicit non-empty list")
    if not isinstance(case.get("excluded_expectations"), list):
        raise GoldenCaseError("excluded_expectations must be an explicit list")
    expectations = case.get("expected")
    if not isinstance(expectations, list) or not expectations:
        raise GoldenCaseError("expected must be a non-empty structured list")
    for exp in expectations:
        if not isinstance(exp, dict) or exp.get("type") not in EXPECTATION_TYPES or not exp.get("target") or "value" not in exp:
            raise GoldenCaseError("each expectation needs type, target and value")
        if exp.get("auto_accepted") is True or exp.get("source") in {"CURRENT_OUTPUT", "AUTO_GENERATED"}:
            raise GoldenCaseError("automatic/current-output expectations are forbidden")
        if exp.get("authority") not in AUTHORITIES:
            raise GoldenCaseError("each expectation needs a valid authority")
    authority = case.get("authority")
    if not isinstance(authority, dict) or authority.get("basis") not in AUTHORITIES:
        raise GoldenCaseError("authority.basis is required and must be recognized")
    review = case.get("review")
    if not isinstance(review, dict):
        raise GoldenCaseError("review object is required")
    if case["status"] == "APPROVED":
        if not all(isinstance(review.get(k), str) and review[k].strip() for k in ("reviewed_by", "review_basis")) or not _utc(review.get("reviewed_at_utc")):
            raise GoldenCaseError("APPROVED requires reviewer, UTC review time and basis")
    engine = case.get("engine_context")
    if not isinstance(engine, dict) or not all(isinstance(engine.get(k), str) and engine[k].strip() for k in ("gtfs_lab_version", "validator_version", "ruleset_id", "ruleset_version")):
        raise GoldenCaseError("engine_context provenance fields are required")
    if case.get("golden_expectation_source") in {"AUTO_GENERATED", "CURRENT_OUTPUT", "AUTO_ACCEPTED"}:
        raise GoldenCaseError("auto-generated golden expectation marker is forbidden")
