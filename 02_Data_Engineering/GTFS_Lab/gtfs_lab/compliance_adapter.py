from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from .core import RunContext

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENGINE_PATH = PROJECT_ROOT / "tools" / "compliance_v1_engine.py"
SOURCES_DIR = PROJECT_ROOT / "03_Compliance" / "reports" / "evidence" / "compliance_v1_20260928" / "sources"
MANIFEST_PATH = SOURCES_DIR.parent / "source_manifest.json"
EXPECTED_ENGINE_SHA256 = "60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb"
EXPECTED_SPEC_SHA256 = "1ff40b8001b180bd023dd6f1899907aecbcb4600c8dbcb6fc6c841a50839b147"
RULE_ID = "V1-RULE-GTFS"

def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _load_engine():
    data = ENGINE_PATH.read_bytes()
    actual_engine_sha = _sha(data)
    if actual_engine_sha != EXPECTED_ENGINE_SHA256:
        raise RuntimeError("TRUSTED_EVALUATOR_HASH_MISMATCH")
    source_hash = _sha((SOURCES_DIR / "gtfs_reference.md").read_bytes())
    if source_hash != EXPECTED_SPEC_SHA256:
        raise RuntimeError("TRUSTED_SOURCE_HASH_MISMATCH")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_hashes = {s.get("path"): s.get("sha256") for s in manifest.get("sources", [])}
    if manifest_hashes.get("gtfs_reference.md") != EXPECTED_SPEC_SHA256:
        raise RuntimeError("TRUSTED_SOURCE_MANIFEST_MISMATCH")
    spec = importlib.util.spec_from_file_location("transit_data_lab_compliance_v1_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("TRUSTED_EVALUATOR_LOAD_FAILURE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, "GTFS-SNAPSHOT-SHA256:" + EXPECTED_SPEC_SHA256

def inspect_fixed_stop_references(ctx: RunContext) -> dict:
    """Call the hash-pinned Compliance V1 implementation without modifying it."""
    try:
        engine, expected_version = _load_engine()
        files = {f"{name}.txt": path for name, path in ctx.tables.items() if name in {"trips", "stops", "stop_times"}}
        result = engine.inspect_gtfs(files, expected_version, expected_version, complete=True)
        data_hash = engine.dataset_hash_paths(files)
        result.update({"rule_id": RULE_ID, "rule_version": "compliance-v1/1", "evaluator_version": engine.VERSION, "evaluator_sha256": EXPECTED_ENGINE_SHA256, "reference_sha256": EXPECTED_SPEC_SHA256, "dataset_id": ctx.dataset.dataset_id, "source_zip_sha256": ctx.dataset.source_sha256, "inspection_dataset_sha256": data_hash, "provenance": "Invocación del motor Compliance V1 v2 sobre archivos de ingestión; regla semántica sin cambios", "scope_limit_bytes_per_file": 512 * 1024 * 1024, "scope_limit_rows": engine.MAX_ROWS, "scope_limit_record_bytes": engine.MAX_RECORD_BYTES, "legal_conclusion_allowed": False})
    except Exception as exc:
        result = {"result": "INSPECTION_ERROR", "reason": f"{type(exc).__name__}:{exc}", "locator": "input", "observed": "INDETERMINATE", "legal_conclusion_allowed": False, "rule_id": RULE_ID, "rule_version": "compliance-v1/1", "evaluator_version": "compliance-v1/2", "evaluator_sha256": None, "reference_sha256": EXPECTED_SPEC_SHA256, "dataset_id": ctx.dataset.dataset_id, "source_zip_sha256": ctx.dataset.source_sha256, "inspection_dataset_sha256": None, "provenance": "Compliance V1 adapter failed safely before a technical conclusion", "scope_limit_bytes_per_file": 512 * 1024 * 1024, "scope_limit_rows": 1_000_000, "scope_limit_record_bytes": 4 * 1024 * 1024}
    result["findings"] = []
    result["integration_status"] = "PASS" if result.get("evaluator_sha256") == EXPECTED_ENGINE_SHA256 and result.get("rule_id") == RULE_ID else "FAIL_LOCAL"
    if result["result"] == "FAIL_TECHNICAL":
        reason = result.get("reason", "TECHNICAL_REFERENCE_FAILURE")
        locator = result.get("locator", "stop_times.txt")
        result["findings"].append({"dataset_id": ctx.dataset.dataset_id, "rule_id": RULE_ID, "table": "stop_times.txt", "row_locator": locator, "field": "trip_id/stop_id", "observed_value": result.get("observed", "ABSENCE_CONFIRMED"), "expected_condition": "trip_id references trips.trip_id; stop_id references fixed stops.txt platform", "technical_message": reason, "evidence": {"source_zip_sha256": ctx.dataset.source_sha256, "inspection_dataset_sha256": result.get("inspection_dataset_sha256"), "evaluator_sha256": result.get("evaluator_sha256"), "rule_version": result.get("rule_version")}})
    return result
