"""Compare baseline and instrumented synthetic client audit semantics."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


RUNNER = r'''import json, sys
from pathlib import Path
from gtfs_lab import VERSION
from gtfs_lab.client_workflow import WORKFLOW_VERSION, run_client_audit
result = run_client_audit(Path(sys.argv[1]), Path(sys.argv[2]),
    client_project_id="w00o-synthetic-semantic-comparison", audit_id="same-synthetic-audit",
    source_provenance="SYNTHETIC")
print(json.dumps({"result": result, "versions": {"workflow": WORKFLOW_VERSION, "engine": VERSION}}))
'''


def _json_file(root: Path, name: str) -> dict:
    matches = list(root.rglob(name))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one {name}; found {len(matches)}")
    return json.loads(matches[0].read_text(encoding="utf-8"))


def _run(lab: Path, fixture: Path, workspace: Path) -> tuple[dict, Path]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(lab) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    proc = subprocess.run([sys.executable, "-c", RUNNER, str(fixture), str(workspace)],
                          cwd=lab, env=env, capture_output=True, text=True, check=True)
    payload = json.loads(proc.stdout.splitlines()[-1])
    result = payload["result"]
    result["_versions"] = payload["versions"]
    return result, Path(result["delivery_directory"])


def _projection(result: dict, delivery: Path) -> dict:
    engine = _json_file(delivery, "engine_report.json")
    validation = _json_file(delivery, "validation.json")
    interpretation = _json_file(delivery, "AUDIT_CONSOLIDATED.json")
    manifest = json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))
    dataset_identity = manifest.get("dataset_identity", {})
    artifacts = manifest.get("delivery_artifacts", {})
    evidence_paths = sorted(
        name for name in artifacts
        if name.startswith("engine_run/input/")
        or name in {"engine_run/engine_report.json", "engine_run/engine_report.md"}
    )
    return {
        "source_identity": {"sha256": result["source_sha256"], "status": result["status"],
                            "source_immutable": result["source_immutable"]},
        "dataset_identity": {key: dataset_identity.get(key) for key in (
            "dataset_id", "source_sha256", "source_size_bytes", "source_filename",
            "source_provenance", "workflow_version")},
        "evidence_references": {
            "source_sha256": dataset_identity.get("source_sha256"),
            "source_size_bytes": dataset_identity.get("source_size_bytes"),
            "artifacts": {name: {key: artifacts[name].get(key) for key in ("sha256", "size_bytes")}
                          for name in evidence_paths},
        },
        "raw_findings": validation["findings"],
        "family_accounting": {"finding_count": validation["finding_count"],
                              "status": validation["status"],
                              "rules": [{k: rule.get(k) for k in ("rule_id", "version", "scope", "severity",
                                        "status", "checked_rows", "finding_count", "source_reference",
                                        "evaluator_sha256")}
                                        for rule in validation["rules"]]},
        "interpretation": {k: interpretation.get(k) for k in (
            "contract_version", "interpretation_status", "coverage", "finding_families")},
        "report_semantics": {"schema_version": engine.get("schema_version"),
                             "report_type": engine.get("report_type"),
                             "coverage": engine.get("coverage"),
                             "technical_evaluation": engine.get("technical_evaluation"),
                             "recommendation_outcomes": engine.get("recommendation_outcomes")},
        "contract_versions": {"workflow": result.get("_versions", {}).get("workflow"),
                              "engine": result.get("_versions", {}).get("engine"),
                              "interpretation": interpretation.get("contract_version")},
    }


def compare(baseline_lab: Path, instrumented_lab: Path, fixture: Path, work: Path) -> dict:
    baseline_lab, instrumented_lab = baseline_lab.resolve(), instrumented_lab.resolve()
    fixture, work = fixture.resolve(), work.resolve()
    baseline, baseline_delivery = _run(baseline_lab, fixture, work / "baseline")
    instrumented, instrumented_delivery = _run(instrumented_lab, fixture, work / "instrumented")
    before = _projection(baseline, baseline_delivery)
    after = _projection(instrumented, instrumented_delivery)
    checks = {key: before[key] == after[key] for key in before}
    return {"schema_version": "1.0", "baseline_commit": "f53335747562206936e5db7704dfb093844d768e",
            "fixture_sha256": before["source_identity"]["sha256"],
            "baseline_status": baseline["status"], "instrumented_status": instrumented["status"],
            "checks": checks, "semantic_equivalence": "PASS" if all(checks.values()) else "FAIL",
            "optimization_implemented": True,
            "optimization_before_after_improvement": "NOT_MEASURED_BY_THIS_COMPARATOR; SEE W00P BENCHMARK",
            "replay_semantics": "NOT_APPLICABLE; both are initial audits, not replay",
            "projection": "raw findings, family/rule accounting, interpretation, evidence references, dataset identity, report semantics and versions",
            "baseline_delivery": str(baseline_delivery), "instrumented_delivery": str(instrumented_delivery)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-lab", type=Path, required=True)
    parser.add_argument("--instrumented-lab", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    result = compare(args.baseline_lab, args.instrumented_lab, args.fixture, args.work)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["semantic_equivalence"])
    return 0 if result["semantic_equivalence"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
