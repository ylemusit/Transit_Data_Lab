"""Inventory W00 evidence for review. This tool never deletes or hashes files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict

MANIFEST_GENERATOR_VERSION = "1.0.0"


CLASSES = {
    "MUST_VERSION": "Diagnostic source, compact W00-M decision/policy, and review manifests.",
    "REPRODUCIBLE_DO_NOT_VERSION": "Generated fixtures/output reproducible from the recorded generator and parameters.",
    "LOCAL_EVIDENCE_PRESERVE": "Compact measurements, safety checks, semantic evidence, or selected raw diagnostic output.",
    "SAFE_TO_REMOVE_AFTER_MANIFEST": "Exact generated scratch/output candidates; human review is required before deletion.",
}


def classify(path: str) -> tuple[str, str]:
    parts = path.split("/")
    if path in {"w00_generated_evidence_policy.json", "proposed_cleanup_manifest.json",
                "memory_root_cause_w00m.json", "w00m_execution_manifest.json", ".gitignore"}:
        return "MUST_VERSION", "Compact W00-M evidence policy, result, inventory, or output exclusion rule."
    if path.endswith((".py", ".spec")):
        return "MUST_VERSION", "Diagnostic source/tooling or packaging specification."
    if "output" in parts or "audit_output" in parts:
        return "SAFE_TO_REMOVE_AFTER_MANIFEST", "Generated audit output; preserve fixture, measurements, and summaries."
    if "build" in parts or "dist" in parts:
        return "SAFE_TO_REMOVE_AFTER_MANIFEST", "Reproducible local packaging output; preserve spec, hooks, and assessment."
    if path.endswith(("old_serialization.json", "new_serialization.json")):
        return "REPRODUCIBLE_DO_NOT_VERSION", "Large deterministic serializer outputs; SHA-256 equivalence is recorded separately."
    if parts[0] == "json_streaming_optimization" and parts[1].startswith(("semantic_complete", "semantic_final", "semantic_after_streaming")):
        return "REPRODUCIBLE_DO_NOT_VERSION", "Synthetic comparison output; the compact semantic result is retained separately."
    if parts[0] in {"semantic_compare_work", "semantic_compare_work_v2"}:
        return "SAFE_TO_REMOVE_AFTER_MANIFEST", "Comparison scratch; semantic result and fixture identity are retained separately."
    if parts[0] == "semantic_compare_w00m_s1" and "work" in parts:
        return "LOCAL_EVIDENCE_PRESERVE", "W00-M bounded comparison scratch retained pending human review."
    if parts[0] == "__pycache__":
        return "SAFE_TO_REMOVE_AFTER_MANIFEST", "Reproducible interpreter cache; not evidence."
    if parts[0] in {"synthetic_scale_runs_20261005_final", "synthetic_scale_runs_20261005_extended"} and "output" in parts:
        return "SAFE_TO_REMOVE_AFTER_MANIFEST", "Complete generated audit output; preserve sibling fixture, stages, preflight, and scale analysis."
    if parts[0].startswith("synthetic_scale_runs_") and "output" in parts:
        return "REPRODUCIBLE_DO_NOT_VERSION", "Generated complete audit output; retain locally pending classification."
    if parts[0].startswith("synthetic_scale_runs_"):
        return "LOCAL_EVIDENCE_PRESERVE", "Fixture identity, stage/resource log, preflight, or scale summary."
    if parts[0].startswith(("memory_diag_s4", "semantic_compare_w00m_s1")):
        return "LOCAL_EVIDENCE_PRESERVE", "Direct W00-M diagnostic or semantic evidence; retain pending review."
    if parts[0] in {"pyinstaller_probe", "debug_s1", "subprocess_reclamation_work"}:
        return "LOCAL_EVIDENCE_PRESERVE", "W00 packaging or diagnostic evidence; local only."
    if parts[0] in {"smoke-output", "smoke-temp"}:
        return "REPRODUCIBLE_DO_NOT_VERSION", "Reproducible smoke output."
    if path.endswith((".zip", ".duckdb")):
        return "REPRODUCIBLE_DO_NOT_VERSION", "Generated fixture/database; regenerate from source and manifest."
    if path.endswith((".py", ".spec")):
        return "MUST_VERSION", "Diagnostic source, probe, or packaging specification."
    return "LOCAL_EVIDENCE_PRESERVE", "Compact W00 measurement, decision, preflight, or report."


def build(root: Path) -> tuple[dict, dict]:
    root = root.resolve()
    policy = {
        "schema_version": "1.0.0", "date": "2026-10-05",
        "manifest_generator_version": MANIFEST_GENERATOR_VERSION,
        "scope": "reports/evidence/windows_client_v1/w00/**",
        "full_synthetic_outputs_versioned": "NO", "deletion_performed": "NO",
        "recursive_deletion_authorized": "NO", "classes": CLASSES,
        "retention_requirements": ["generator version", "parameters and scale factors",
            "fixture SHA-256", "row counts", "runtime/resource measurements and sampling interval",
            "semantic comparison", "manifest", "commands"],
        "human_gate": "Proposal only. Review exact paths before any cleanup; no deletion is performed.",
        "cleanup_manifest": "reports/evidence/windows_client_v1/w00/proposed_cleanup_manifest.json",
    }
    (root / "w00_generated_evidence_policy.json").write_text(
        json.dumps(policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    files, totals = [], defaultdict(lambda: {"files": 0, "bytes": 0})
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "proposed_cleanup_manifest.json":
            continue
        relative = path.relative_to(root).as_posix()
        classification, reason = classify(relative)
        try:
            size = path.stat().st_size
        except OSError:
            size = None
        files.append({"path": relative, "bytes": size, "classification": classification,
                      "rationale": reason, "deletion_performed": False})
        totals[classification]["files"] += 1
        if size is not None:
            totals[classification]["bytes"] += size
    manifest = {
        "schema_version": "1.0.0", "date": "2026-10-05",
        "manifest_generator_version": MANIFEST_GENERATOR_VERSION,
        "scope": "reports/evidence/windows_client_v1/w00/**",
        "inventory_method": "Path and size metadata only; generated contents are not read and no bulk hashes are calculated.",
        "manifest_self_entry": "Omitted because its own size would be self-referential.",
        "total_files": len(files), "total_bytes": sum(row["bytes"] or 0 for row in files),
        "classification_totals": dict(totals), "proposed_only": True,
        "deletion_performed": False, "recursive_deletion_authorized": False,
        "human_gate": "Review exact paths before any cleanup. Re-inventory immediately before any later authorized deletion.",
        "preserve_reproduction_evidence": policy["retention_requirements"], "files": files,
    }
    (root / "proposed_cleanup_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return policy, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    _, manifest = build(args.evidence_root)
    print(json.dumps({"files": manifest["total_files"], "bytes": manifest["total_bytes"],
                      "classifications": manifest["classification_totals"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
