"""Deterministic presentation of independent GTFS Audit Engine stage results."""
from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from .g03_structure import load_official_catalog

STAGES = ("g03", "g04", "g05", "g06", "g07", "g08")


def build_engine_report(run_result: Mapping[str, Any]) -> dict[str, Any]:
    """Build a machine-readable report without normalizing or mutating M02 data."""
    dataset = run_result.get("dataset", {})
    stages: list[dict[str, Any]] = []
    finding_rows: list[dict[str, Any]] = []
    recommendation_findings: list[dict[str, Any]] = []
    limitations: list[str] = []
    not_evaluable: list[dict[str, str]] = []
    for stage in STAGES:
        result = run_result.get(stage)
        if not isinstance(result, Mapping):
            stages.append({"stage": stage.upper(), "status": "NOT_EVALUABLE", "rules": []})
            not_evaluable.append({"stage": stage.upper(), "reason": "stage result unavailable"})
            continue
        rules = []
        for rule in result.get("rules", []):
            rule_id = str(rule.get("rule_id", "UNKNOWN_RULE"))
            status = str(rule.get("status", "NOT_EVALUABLE"))
            rules.append({
                "rule_id": rule_id,
                "semantic_version": rule.get("semantic_version", rule.get("version")),
                "authority": rule.get("authority"),
                "severity": rule.get("severity"),
                "requirement": rule.get("requirement"),
                "status": status,
                "coverage": rule.get("coverage"),
                "recommendation_met": rule.get("recommendation_met"),
            })
            if status in {"NOT_EVALUABLE", "INSPECTION_ERROR"}:
                not_evaluable.append({"stage": stage.upper(), "rule_id": rule_id, "status": status})
            for finding in rule.get("findings", []):
                normalized_finding = {
                    "stage": stage.upper(), "rule_id": rule_id,
                    "semantic_version": rule.get("semantic_version", rule.get("version")),
                    "authority": rule.get("authority"), "severity": rule.get("severity"),
                    "requirement": rule.get("requirement"), **finding,
                }
                if stage == "g08":
                    recommendation_findings.append(normalized_finding)
                else:
                    finding_rows.append(normalized_finding)
        rules.sort(key=lambda row: row["rule_id"])
        stages.append({"stage": stage.upper(), "status": result.get("status", "NOT_EVALUABLE"), "rules": rules})
        for limitation in result.get("limitations", []):
            limitations.append(f"{stage.upper()}: {limitation}")
        if result.get("coverage_limitation"):
            limitations.append(f"{stage.upper()}: {result['coverage_limitation']}")
    finding_rows.sort(key=lambda row: (
        row["stage"], row["rule_id"], str(row.get("source_file", "")),
        str(row.get("record_locator", row.get("row_locator", ""))),
        json.dumps(row, sort_keys=True, ensure_ascii=False, default=str),
    ))
    recommendation_findings.sort(key=lambda row: (
        row["rule_id"], str(row.get("source_file", "")),
        json.dumps(row, sort_keys=True, ensure_ascii=False, default=str),
    ))
    g03 = run_result.get("g03", {})
    catalog = run_result.get("g03_file_catalog", {})
    observed_members = {
        str(row.get("official_identity", "")).casefold(): row
        for row in catalog.get("members", [])
        if isinstance(row, Mapping) and row.get("official_identity")
    } if isinstance(catalog, Mapping) else {}
    official = load_official_catalog()
    deferred = sorted(
        row["file_name"] for row in official.values()
        if str(row["tdl_v1_support"]).startswith("DEFERRED")
    )
    deferred_observed = sorted(name for name in deferred if name.casefold() in observed_members)
    feature_support = [{
        "file_name": row["file_name"],
        "support": "DEFERRED" if str(row["tdl_v1_support"]).startswith("DEFERRED") else "SUPPORTED",
        "root_member_present": row["file_name"].casefold() in observed_members,
    } for row in sorted(official.values(), key=lambda item: item["file_name"].casefold())]
    legacy = run_result.get("validation", {})
    report = {
        "schema_version": "1.0.0",
        "report_type": "GTFS_AUDIT_ENGINE_V1",
        "dataset": {"dataset_id": dataset.get("dataset_id"), "source_sha256": dataset.get("source_sha256")},
        "technical_evaluation": {"stages": stages, "findings": finding_rows},
        "recommendation_findings": recommendation_findings,
        "recommendation_outcomes": [
            {"rule_id": rule["rule_id"], "status": rule["status"],
             "recommendation_met": rule.get("recommendation_met")}
            for stage in stages if stage["stage"] == "G08" for rule in stage["rules"]
        ],
        "coverage": [
            {"stage": stage["stage"], "rule_id": rule["rule_id"], "coverage": rule.get("coverage")}
            for stage in stages for rule in stage["rules"] if rule.get("coverage") is not None
        ],
        "known_gaps": not_evaluable,
        "deferred_features": deferred,
        "deferred_features_observed": deferred_observed,
        "official_feature_support": feature_support,
        "limitations": sorted(set(limitations)),
        "legacy_relationship": {
            "legacy_validation_status": legacy.get("status"),
            "legacy_finding_count": legacy.get("finding_count", len(legacy.get("findings", []))),
            "g04_overlap_observations": g03.get("legacy_comparison", run_result.get("g04", {}).get("legacy_comparison", [])),
            "equivalence_claimed": False,
        },
        "persistence_boundary": {
            "m02_modified": False,
            "m02_tracks_engine_report_artifacts": False,
            "engine_stages_added_to_legacy_validation": False,
        },
        "legal_boundary": "Technical results only; no legal compliance or certification conclusion.",
    }
    return report


def render_engine_report(report: Mapping[str, Any]) -> str:
    """Render a stable human-readable summary from the machine report."""
    lines = [
        "# GTFS Audit Engine V1 — informe técnico",
        "",
        f"- Dataset: `{report['dataset'].get('dataset_id') or 'N/D'}`",
        f"- SHA-256: `{report['dataset'].get('source_sha256') or 'N/D'}`",
        "- Alcance: resultados técnicos independientes G03–G08.",
        "",
        "## Estados por etapa",
        "",
        "| Etapa | Estado | Reglas |",
        "|---|---|---:|",
    ]
    for stage in report["technical_evaluation"]["stages"]:
        lines.append(f"| {stage['stage']} | {stage['status']} | {len(stage['rules'])} |")
    lines.extend(["", "## Reglas y cobertura", "", "| Etapa | Regla | Estado | Autoridad | Cobertura | Recomendación |", "|---|---|---|---|---|---|"])
    for stage in report["technical_evaluation"]["stages"]:
        for rule in stage["rules"]:
            coverage = rule.get("coverage")
            coverage_state = coverage.get("state", "N/D") if isinstance(coverage, Mapping) else "N/D"
            lines.append(f"| {stage['stage']} | `{rule['rule_id']}` | {rule['status']} | {rule.get('authority') or 'N/D'} | {coverage_state} | {rule.get('recommendation_met', 'N/D')} |")
    lines.extend(["", "## Hallazgos", ""])
    if report["technical_evaluation"]["findings"]:
        for finding in report["technical_evaluation"]["findings"]:
            locator = finding.get("record_locator", finding.get("row_locator", ""))
            source = finding.get("source_file", finding.get("file", ""))
            lines.append(f"- `{finding['stage']}` `{finding['rule_id']}` {source} {locator}: {finding.get('technical_reason', finding.get('recommendation', finding.get('reason', 'finding'))) }")
    else:
        lines.append("- Ninguno.")
    lines.extend(["", "## Recomendaciones G08", ""])
    if report["recommendation_findings"]:
        for finding in report["recommendation_findings"]:
            lines.append(f"- `{finding['rule_id']}` (`{finding.get('authority')}`, `{finding.get('severity')}`): {finding.get('recommendation', finding.get('reason', 'recomendación no satisfecha'))}")
    else:
        lines.append("- Ninguna no satisfecha.")
    lines.extend(["", "## Gaps y features diferidas", ""])
    gaps = report["known_gaps"]
    lines.extend([f"- No evaluable / error de inspección: {len(gaps)}"])
    deferred = report["deferred_features"]
    lines.append(f"- Features oficiales diferidas: {len(deferred)}; presentes en este archivo: {len(report['deferred_features_observed'])}")
    for feature in deferred:
        lines.append(f"  - `{feature}`")
    lines.extend(["", "## Límites", ""])
    lines.append("- La recomendación G08 permanece separada de los fallos de conformidad.")
    lines.append("- `NOT_EVALUABLE`, `NOT_APPLICABLE`, errores de inspección, cobertura parcial y features diferidas se mantienen explícitos.")
    lines.append("- No se calcula score global ni se declara equivalencia total con legacy.")
    lines.append("- Los resultados son técnicos; no concluyen cumplimiento ni certificación jurídica.")
    lines.extend(["", "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""])
    return "\n".join(lines)
