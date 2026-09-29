"""Read-only adapter and proof runner for persisted M04 B1/B3 evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .change_attribution import CONTRACT_VERSION as CHANGE_ATTRIBUTION_VERSION
from .change_attribution import compare as compare_change_attribution

DATASET_IDS = ("006", "008", "013", "015", "017", "018")
LINEAGE = {
    "006": "DATASET-006", "008": "DATASET-008", "013": "LINEAGE-013-015",
    "015": "LINEAGE-013-015", "017": "DATASET-017", "018": "DATASET-018",
}
V1_PARSER = "gtfs-lab-csv/1"
V2_PARSER = "gtfs-lab-csv/2"
V1_EVALUATOR_SHA = "efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70"
V2_EVALUATOR_SHA = "60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb"
V2_PACKAGE_SHA = "8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b"


def _rows(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = summary.get("datasets")
    if not isinstance(rows, list):
        raise ValueError("historical summary.datasets must be a list")
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("dataset_id"), str):
            raise ValueError("historical dataset row is malformed")
        if row["dataset_id"] in result:
            raise ValueError("historical summary has duplicate dataset IDs")
        result[row["dataset_id"]] = row
    return result


def build_historical_m04_snapshot(
    dataset_id: str,
    summary: dict[str, Any],
    *,
    side: str,
    evidence_ref: str,
) -> dict[str, Any]:
    """Adapt one persisted B1 or B3 summary row; absent V1 results stay absent."""
    if side not in {"baseline", "candidate"}:
        raise ValueError("side must be baseline or candidate")
    row = _rows(summary).get(dataset_id)
    if row is None:
        raise ValueError(f"dataset {dataset_id} is missing from {side} summary")
    row_index = next(i for i, item in enumerate(summary["datasets"]) if item["dataset_id"] == dataset_id)
    is_v1 = side == "baseline"
    raw_rules = row.get("rule_results" if is_v1 else "rule_results_v2")
    if raw_rules is None and not is_v1:
        raw_rules = row.get("rule_results")
    if raw_rules is None:
        raw_rules = []
    if not isinstance(raw_rules, list):
        raise ValueError(f"dataset {dataset_id} {side} rule results are malformed")
    rules = []
    for item in raw_rules:
        if not isinstance(item, dict) or not isinstance(item.get("rule_id"), str) or not isinstance(item.get("status"), str):
            raise ValueError(f"dataset {dataset_id} {side} contains malformed rule result")
        rules.append({
            "rule_id": item["rule_id"],
            "status": item["status"],
            "finding_count": item.get("finding_count"),
        })
    sha = row.get("source_sha256")
    if not isinstance(sha, str) or len(sha) != 64:
        raise ValueError(f"dataset {dataset_id} {side} has no persisted source SHA-256")
    if row.get("lineage_unit") != LINEAGE[dataset_id]:
        raise ValueError(f"dataset {dataset_id} lineage conflicts with frozen M04 split")
    if is_v1:
        engine_source = summary.get("engine_identity", {})
        parser = engine_source.get("parser_version")
        compliance = {
            "semantic_rule_version": "compliance-v1/1",
            "evaluator_version": "legacy evaluator",
            "evaluator_sha256": engine_source.get("compliance_evaluator_sha256"),
            # B1 has no package identity; omit the optional field on both sides below.
            "package_sha256": None,
            "reference_sha256": None,
        }
        ruleset = engine_source.get("ruleset_id")
        ruleset_version = "1"
        validator = engine_source.get("validator_version")
        engine_version = engine_source.get("gtfs_lab_version")
        audit_id = f"M04-B1-{dataset_id}"
    else:
        engine_source = summary.get("engine_identity", {})
        parser = engine_source.get("parser")
        compliance = {
            "semantic_rule_version": engine_source.get("semantic_rule_version"),
            "evaluator_version": engine_source.get("evaluator"),
            "evaluator_sha256": engine_source.get("evaluator_sha256"),
            # Package identity was not recorded in B1, so it cannot prove a change.
            "package_sha256": None,
            "reference_sha256": None,
        }
        ruleset = "gtfs-lab-v1"
        ruleset_version = "1"
        validator = engine_source.get("validator")
        engine_version = None
        audit_id = f"M04-B3-{dataset_id}"
    if parser not in {V1_PARSER, V2_PARSER}:
        raise ValueError(f"dataset {dataset_id} has unsupported persisted parser identity")
    if (is_v1 and compliance["evaluator_sha256"] != V1_EVALUATOR_SHA) or (
        not is_v1 and (compliance["evaluator_sha256"] != V2_EVALUATOR_SHA
                       or engine_source.get("compliance_package_sha256") != V2_PACKAGE_SHA)
    ):
        raise ValueError(f"dataset {dataset_id} compliance identity differs from historical contract")
    return {
        "snapshot_contract": "AuditComparisonSnapshot",
        "snapshot_contract_version": "1.0.0",
        "audit_id": audit_id,
        "identity": {
            "dataset": {"source_sha256": sha, "dataset_id": dataset_id, "lineage_id": LINEAGE[dataset_id]},
            # Commit and GTFS_Lab version are not comparable across these persisted records.
            "engine": {"git_commit": None, "parser_version": parser,
                       "validator_version": validator, "gtfs_lab_version": None},
            "rules": {"ruleset_id": ruleset, "ruleset_version": ruleset_version,
                      "rule_version": None, "rule_versions": {str(r["rule_id"]): str(summary_version)
                          for r, summary_version in zip(raw_rules, [x.get("version", "") for x in raw_rules])}},
            "compliance": compliance,
            "configuration": {"sha256": None},
        },
        "result": {"rules": rules},
        "findings": [],
        "historical_source": {"evidence_ref": evidence_ref, "json_pointer": f"/datasets/{row_index}",
                              "dataset_id": dataset_id, "side": side},
    }


def compare_historical_summaries(v1: dict[str, Any], v2: dict[str, Any], *, refs: dict[str, str]) -> dict[str, Any]:
    before, after = _rows(v1), _rows(v2)
    output = []
    for dataset_id in DATASET_IDS:
        old = build_historical_m04_snapshot(dataset_id, v1, side="baseline", evidence_ref=refs["baseline"])
        new = build_historical_m04_snapshot(dataset_id, v2, side="candidate", evidence_ref=refs["candidate"])
        old_versions = old["identity"]["rules"]["rule_versions"]
        new_versions = new["identity"]["rules"]["rule_versions"]
        if old_versions != new_versions and (
            old["identity"]["rules"]["rule_version"] is None
            or new["identity"]["rules"]["rule_version"] is None
        ):
            comparison = {
                "result_change": {"status": "NOT_COMPARABLE", "changed": None, "differences": []},
                "attribution": "NOT_COMPARABLE", "supported_causes": [],
                "comparability": {"status": "NOT_COMPARABLE", "reasons": [
                    "RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0"]},
            }
        elif not old["result"]["rules"] or not new["result"]["rules"]:
            comparison = {
                "result_change": {"status": "NOT_COMPARABLE", "changed": None, "differences": []},
                "attribution": "NOT_COMPARABLE", "supported_causes": [],
                "comparability": {"status": "NOT_COMPARABLE", "reasons": ["HISTORICAL_RESULTS_UNAVAILABLE"]},
            }
        else:
            attributed = compare_change_attribution(old, new)
            # B3 did not persist gtfs_lab_version and B1 did not persist warnings.
            # The comparison uses available M05-A identities and keeps those omissions explicit.
            comparison = {
                "result_change": attributed["result_change"],
                "attribution": attributed["attribution"],
                "supported_causes": attributed["supported_causes"],
                "comparability": {"status": "PARTIALLY_COMPARABLE", "reasons": [
                    "CANDIDATE_ENGINE_GTFS_LAB_VERSION_NOT_PERSISTED",
                    "BASELINE_WARNING_LIST_NOT_PERSISTED"]},
            }
        old_hash, new_hash = before[dataset_id]["source_sha256"].lower(), after[dataset_id]["source_sha256"].lower()
        hash_state = "MATCH" if old_hash == new_hash else "MISMATCH"
        evidence_state = {
            "NOT_COMPARABLE": "NOT_COMPARABLE",
            "PARTIALLY_COMPARABLE": "PARTIAL",
            "COMPARABLE": "SUFFICIENT",
        }[comparison["comparability"]["status"]]
        output.append({
            "dataset_id": dataset_id,
            "lineage_unit": LINEAGE[dataset_id],
            "source_sha256": {"baseline": old_hash, "candidate": new_hash, "status": hash_state},
            "pipeline_status": {"baseline": before[dataset_id].get("pipeline_status"),
                                "candidate": "PIPELINE_COMPLETED" if after[dataset_id].get("rule_results_v2") else None},
            "result_change": comparison["result_change"],
            "attribution": comparison["attribution"],
            "supported_causes": comparison["supported_causes"],
            "evidence_state": evidence_state,
            "comparability": comparison["comparability"],
            "evidence_refs": [old["historical_source"], new["historical_source"]],
            "historical_support": {
                "baseline_warnings": before[dataset_id].get("warnings", "NOT_PERSISTED_IN_B1_SUMMARY"),
                "candidate_warnings": after[dataset_id].get("warnings_v2", []),
                "baseline_execution_errors": before[dataset_id].get("execution_errors", []),
                "candidate_execution_errors": after[dataset_id].get("execution_errors_v2", []),
            },
            "supporting_historical_interpretation": (
                v2.get("classifications", {}).get("dataset_008") if dataset_id == "008" else None
            ),
        })
    return {
        "contract": "M05C_HistoricalProof",
        "version": "1.0.0",
        "comparison_engine": "ChangeAttribution",
        "comparison_engine_version": CHANGE_ATTRIBUTION_VERSION,
        "adapter": "read-only persisted M04 B1/B3 summary adapter",
        "baseline": refs["baseline"],
        "candidate": refs["candidate"],
        "lineage": {"dataset_count": 6, "independent_lineage_unit_count": 5, "linked_dataset_ids": ["013", "015"]},
        "datasets": output,
        "verdict": "M05C_HISTORICAL_PROOF_READY_FOR_REVIEW",
        "limitations": [
            "Dataset 008 has no persisted B1 rule results; ChangeAttribution 1.0.0 reports NOT_COMPARABLE.",
            "B1 warning lists were not persisted; warning comparison is unavailable.",
            "ChangeAttribution 1.0.0 does not expose a secondary result-interpretation label; the M04-B3 warning and historical evaluator classification remain supporting evidence.",
        ],
    }


def render_markdown(proof: dict[str, Any]) -> str:
    lines = ["# M05-C — Prueba histórica M04 B1 → B3", "",
             f"Veredicto: `{proof['verdict']}`. Evidencia persistida; no se reejecutó HOLDOUT.", "",
             f"Base: `{proof['baseline']}`", f"Candidata: `{proof['candidate']}`", "",
             "| Dataset | SHA fuente | Cambio de resultados | Atribución M05-A | Causas admitidas | Evidencia | Lineage |",
             "|---|---|---|---|---|---|---|"]
    for item in proof["datasets"]:
        state = item["result_change"]["status"]
        causes = ", ".join(item["supported_causes"]) or "—"
        lines.append(f"| {item['dataset_id']} | {item['source_sha256']['status']} | {state} | {item['attribution']} | {causes} | {item['evidence_state']} | {item['lineage_unit']} |")
    lines += ["", "## Notas de evidencia", "",
              "- 008: B1 registró `PIPELINE_FAILED` en `shapes.txt`, registro 1869; no persistió resultados de reglas. B3 registra `EMPTY_CSV_RECORD_IGNORED` y 8 PASS. La clasificación histórica guardada es `PARSER_IMPLEMENTATION_CHANGE`; `NEWLY_OBSERVABLE_DATA_RESULT` queda como interpretación de apoyo. M05-A declara el par no comparable.",
              "- 013, 015, 017 y 018: la identidad de parser también cambió globalmente. La atribución refleja todos los cambios de identidad admitidos por M05-A; no se fuerza una causa única.",
              "- 013 y 015 forman una unidad de lineage; son seis datasets y cinco unidades independientes.",
              "- Las advertencias V1 no están persistidas en B1. No se reconstruyen findings ni listas faltantes.",
              "- La identidad de paquete no se compara porque B1 no la persistió. B3 tampoco persistió la versión global GTFS_Lab; la evidencia queda `PARTIAL`.",
              "- `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0` se conserva como límite contractual; ante esa condición la salida es `NOT_COMPARABLE`.", "",
              "Fuentes: " + proof["baseline"] + "; " + proof["candidate"] + ".", "",
              "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""]
    return "\n".join(lines)


def run(evidence_dir: Path, output_dir: Path) -> dict[str, Any]:
    v1_path = evidence_dir / "holdout_evaluation_v1" / "first_evaluation_summary.json"
    v2_path = evidence_dir / "holdout_evaluation_v2" / "evaluation_summary.json"
    v1, v2 = json.loads(v1_path.read_text(encoding="utf-8")), json.loads(v2_path.read_text(encoding="utf-8"))
    refs = {"baseline": v1_path.as_posix(), "candidate": v2_path.as_posix()}
    proof = compare_historical_summaries(v1, v2, refs=refs)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return proof


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=Path("reports/evidence"))
    parser.add_argument("--output", type=Path, default=Path("reports/evidence/m05c_historical_proof"))
    args = parser.parse_args()
    proof = run(args.evidence, args.output)
    report = args.output.parent.parent / "TDL_M05C_HISTORICAL_PROOF.md"
    report.write_text(render_markdown(proof), encoding="utf-8")
    print(proof["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
