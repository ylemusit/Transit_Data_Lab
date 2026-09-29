from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .golden_contract import GoldenCaseError, is_executable_authority, validate_case


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def corpus_identity(entries: list[dict[str, str]]) -> str:
    identity = [{k: e[k] for k in ("case_id", "case_version", "case_sha256", "input_sha256")} for e in entries]
    identity.sort(key=lambda e: (e["case_id"], e["case_version"]))
    return hashlib.sha256(_canonical(identity)).hexdigest()


def run_gate() -> dict[str, Any]:
    area = Path(__file__).resolve().parents[1]
    golden_dir = area / "golden"
    manifest_path = golden_dir / "corpus_v1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks: list[dict[str, str]] = []
    def add(name: str, ok: bool) -> None: checks.append({"check": name, "status": "PASS" if ok else "FAIL"})
    add("manifest_identity_and_contract", manifest.get("corpus_id") == "TDL_GOLDEN_CORPUS_V1" and manifest.get("corpus_version") == "1.0.0" and manifest.get("contract_version") == "1.0.0")
    add("manifest_status_approved", manifest.get("status") == "APPROVED" and isinstance(manifest.get("created_at_utc"), str) and manifest["created_at_utc"].endswith("Z"))
    entries = manifest.get("cases")
    add("manifest_cases_list", isinstance(entries, list))
    seen: set[tuple[str, str]] = set(); computed = []; all_approved = True; hashes_ok = True; valid = True; executable = True; authority_chain = True
    if not isinstance(entries, list): entries = []
    for entry in entries:
        try:
            rel = Path(entry["path"]); case_path = golden_dir / rel / "case.json"
            if rel.is_absolute() or ".." in rel.parts or not case_path.resolve().is_relative_to(golden_dir.resolve()): raise ValueError("unsafe case path")
            case_bytes = case_path.read_bytes(); case = json.loads(case_bytes.decode("utf-8-sig")); case_dir = case_path.parent
            validate_case(case, case_dir)
            executable &= is_executable_authority(case, case_dir)
            authority_chain &= case.get("authority", {}).get("basis") == "GTFS_SPECIFICATION" and all(x.get("authority") == "TDL_CONTRACT" for x in case.get("expected", []))
            input_sha = case["input"]["sha256"].lower(); case_sha = hashlib.sha256(case_bytes).hexdigest()
            valid &= entry.get("case_id") == case["case_id"] and entry.get("case_version") == case["case_version"]
            valid &= entry.get("case_sha256") == case_sha and entry.get("input_sha256") == input_sha
            hashes_ok &= entry.get("sha256") == input_sha
            valid &= entry.get("status") == case.get("status")
            all_approved &= case["status"] == "APPROVED"
            key = (case["case_id"], case["case_version"])
            if key in seen: valid = False
            seen.add(key)
            if case.get("golden_expectation_source") in {"CURRENT_OUTPUT", "AUTO_GENERATED", "AUTO_ACCEPTED"}: valid = False
            if case.get("expectation_defined_before_observation") is not True: valid = False
            if not all(isinstance(case.get("review", {}).get(k), str) and case["review"][k].strip() for k in ("reviewed_by", "review_basis", "reviewed_at_utc")): valid = False
            if "observed" in case or "run_id" in case or "runtime_output" in case: valid = False
            computed.append({"case_id": key[0], "case_version": key[1], "case_sha256": case_sha, "input_sha256": input_sha})
        except (OSError, KeyError, ValueError, TypeError, GoldenCaseError, json.JSONDecodeError):
            valid = False; hashes_ok = False; all_approved = False; executable = False; authority_chain = False
    add("all_cases_exist_and_match_contract", valid)
    add("lifecycle_all_approved_and_review_complete", all_approved and executable)
    add("semantic_and_expectation_authorities_separated", authority_chain)
    add("unique_case_version_and_no_duplicate_entries", len(seen) == len(entries) and len({e.get("path") for e in entries}) == len(entries))
    add("input_and_case_hashes_match", hashes_ok and valid)
    expected_identity = corpus_identity(computed)
    add("corpus_sha256_reproducible", manifest.get("corpus_sha256") == expected_identity)
    expected_files = {manifest_path.resolve()}
    # M03-A's versioned contract smoke example remains outside the corpus manifest.
    smoke_dir = golden_dir / "cases" / "contract-smoke"
    expected_files.update({(smoke_dir / "case.json").resolve(), (smoke_dir / "input.zip").resolve()})
    for entry in entries:
        try:
            case_dir = golden_dir / entry["path"]
            case_data = json.loads((case_dir / "case.json").read_text(encoding="utf-8-sig"))
            expected_files.add((case_dir / "case.json").resolve())
            expected_files.add((case_dir / case_data["input"]["filename"]).resolve())
        except (OSError, KeyError, json.JSONDecodeError):
            pass
    actual_files = {p.resolve() for p in golden_dir.rglob("*") if p.is_file()}
    add("no_runtime_outputs_in_corpus", actual_files == expected_files)
    add("approved_count_exactly_two", sum(1 for e in entries if e.get("status") == "APPROVED") == 2)
    return {"gate": "TDL_GOLDEN_CORPUS_GATE", "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL", "case_count": len(entries), "approved_count": sum(1 for e in entries if e.get("status") == "APPROVED"), "corpus_sha256": expected_identity, "checks": checks, "limitations": ["El gate comprueba contrato, hashes y consistencia de los datos de review; no autentica criptográficamente la identidad del reviewer ni autoridad normativa.", "La aprobación humana queda ligada a los case_sha256 incluidos en corpus V1."]}


def main() -> int:
    result = run_gate(); print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
