"""Client-facing report projection over authoritative audit artifacts."""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from typing import Any


REPORT_CONTRACT = "TDL_CLIENT_REPORT_V1"
SECTIONS = (
    "Portada", "Identificación de la auditoría", "Resumen ejecutivo", "Alcance",
    "Jurisdicción", "Fecha de corte", "Exclusiones", "Metodología",
    "Perfil del dataset", "Validación técnica GTFS", "Matriz completa de validaciones",
    "Evaluación regulatoria / Compliance", "Fuentes normativas aplicables", "No aplicable",
    "No evaluable", "Fuentes superseded / repealed / version unknown", "Hallazgos técnicos",
    "Familias consolidadas", "Evidencia", "Impacto", "Interpretación", "Recomendaciones",
    "Remediación", "GIS / revisión geográfica", "Publication readiness", "Limitaciones",
    "Trazabilidad / reproducibilidad", "Disclaimer", "Anexos técnicos",
)


def _as_rows(value: Any) -> list[Mapping[str, Any]]:
    return [row for row in value if isinstance(row, Mapping)] if isinstance(value, list) else []


def _rule_row(rule: Mapping[str, Any], *, domain: str, stage: str,
              finding_refs: Mapping[str, list[str]]) -> dict[str, Any]:
    rule_id = str(rule.get("rule_id") or "UNKNOWN_RULE")
    result = str(rule.get("status") or "NOT_EVALUABLE")
    if result == "NOT_APPLICABLE":
        applicability = "NOT_APPLICABLE"
    else:
        raw_applicability = rule.get("applicability")
        requirement = rule.get("requirement")
        if isinstance(raw_applicability, str) and raw_applicability in {"APPLICABLE", "NOT_APPLICABLE", "CONDITIONAL"}:
            applicability = str(raw_applicability)
        elif requirement == "CONDITIONALLY_REQUIRED":
            applicability = "CONDITIONAL"
        else:
            applicability = None
    evaluability = "NOT_EVALUABLE" if result in {
        "NOT_EVALUABLE", "INSPECTION_ERROR", "DEFERRED", "OUT_OF_SCOPE",
    } else "EVALUABLE"
    return {
        "rule_id": rule_id,
        "domain": str(rule.get("domain") or domain),
        "description": str(rule.get("description") or rule.get("requirement") or rule_id),
        "requirement": rule.get("requirement"),
        "stage": stage,
        "applicability": applicability,
        "applicability_basis": ("RULE_ARTIFACT" if rule.get("applicability") is not None
                                else "CONDITIONALLY_REQUIRED" if rule.get("requirement") == "CONDITIONALLY_REQUIRED"
                                else "NOT_PROVIDED_BY_SOURCE"),
        "evaluability": evaluability,
        "result": result,
        "severity": rule.get("severity"),
        "finding_count": int(rule.get("finding_count", len(_as_rows(rule.get("findings")))) or 0),
        "evidence_refs": finding_refs.get(rule_id, []),
        "source_ref": rule.get("specification_reference") or rule.get("source_ref"),
        "authority": rule.get("authority"),
        "semantic_version": rule.get("semantic_version", rule.get("version")),
    }


def _aggregate_engine_result(stages: list[Mapping[str, Any]]) -> str:
    """Summarize mandatory GTFS engine stages without using the legacy summary."""
    statuses: list[str] = []
    for stage in stages:
        if str(stage.get("stage", "")).upper() == "G08":
            # G08 contains recommendations, not technical conformance failures.
            continue
        status = stage.get("status")
        if isinstance(status, str) and status:
            statuses.append(status)
        rules = _as_rows(stage.get("rules"))
        statuses.extend(str(rule.get("status") or "NOT_EVALUABLE") for rule in rules)
        if not isinstance(status, str) and not rules:
            statuses.append("NOT_EVALUABLE")
    if not statuses:
        return "NOT_EVALUABLE"
    if any(status in {"FAIL", "FAIL_TECHNICAL"} for status in statuses):
        return "FAIL_TECHNICAL"
    if "INSPECTION_ERROR" in statuses:
        return "INSPECTION_ERROR"
    if any(status in {"NOT_EVALUABLE", "SKIPPED_BY_DEPENDENCY"} for status in statuses):
        return "NOT_EVALUABLE"
    if any(status not in {"PASS", "NOT_APPLICABLE"} for status in statuses):
        return "NOT_EVALUABLE"
    return "PASS"


def build_client_report(manifest: Mapping[str, Any], run: Mapping[str, Any],
                        findings: list[Mapping[str, Any]], interpretation: Mapping[str, Any] | None,
                        remediation: Mapping[str, Any], comparison: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build a deterministic, bounded report view without changing engine evidence."""
    engine = run.get("engine_report") if isinstance(run.get("engine_report"), Mapping) else {}
    identity = manifest.get("dataset_identity") if isinstance(manifest.get("dataset_identity"), Mapping) else {}
    findings_by_rule: dict[str, list[str]] = {}
    for index, finding in enumerate(findings):
        findings_by_rule.setdefault(str(finding.get("rule_id") or "UNKNOWN_RULE"), []).append(
            f"findings.json#/findings/{index}")
    matrix: list[dict[str, Any]] = []
    tech = engine.get("technical_evaluation") if isinstance(engine.get("technical_evaluation"), Mapping) else {}
    stage_rows = _as_rows(tech.get("stages"))
    for stage_row in stage_rows:
        stage = str(stage_row.get("stage") or "UNKNOWN")
        for rule in _as_rows(stage_row.get("rules")):
            matrix.append(_rule_row(rule, domain=stage, stage=stage, finding_refs=findings_by_rule))
    validation = run.get("validation") if isinstance(run.get("validation"), Mapping) else {}
    legacy_result = validation.get("status") or (run.get("summary") or {}).get("validation", "NOT_EVALUABLE")
    legacy_summary_result = (run.get("summary") or {}).get("validation", "NOT_EVALUABLE")
    legacy_summary_consistency = ("CONSISTENT" if legacy_result == legacy_summary_result
                                  else "CONFLICT" if legacy_result != "NOT_EVALUABLE" and legacy_summary_result != "NOT_EVALUABLE"
                                  else "NOT_COMPARABLE")
    for rule in _as_rows(validation.get("rules")):
        matrix.append(_rule_row(rule, domain=str(rule.get("scope") or "GTFS"), stage="LEGACY",
                                finding_refs=findings_by_rule))
    compliance = run.get("compliance_v1") if isinstance(run.get("compliance_v1"), Mapping) else {}
    if compliance:
        compliance_rule = {"rule_id": compliance.get("rule_id", "COMPLIANCE_V1"),
                           "status": compliance.get("result", "NOT_EVALUABLE"),
                           "description": "Referencias GTFS de parada fija dentro del alcance acotado de Compliance V1",
                           "domain": "COMPLIANCE", "semantic_version": compliance.get("rule_version"),
                           "applicability": "CONDITIONAL",
                           "specification_reference": compliance.get("reference_sha256")}
        matrix.append(_rule_row(compliance_rule, domain="COMPLIANCE", stage="COMPLIANCE_V1",
                                finding_refs=findings_by_rule))
    matrix.sort(key=lambda row: (row["stage"], row["rule_id"]))

    results = {row["result"] for row in matrix}
    accounting_gap = (interpretation.get("coverage", {}).get("accounting_gap")
                      if isinstance(interpretation, Mapping)
                      and isinstance(interpretation.get("coverage"), Mapping) else None)
    recognized_results = {"PASS", "FAIL", "FAIL_TECHNICAL", "NOT_APPLICABLE", "NOT_EVALUABLE",
                          "INSPECTION_ERROR", "DEFERRED", "OUT_OF_SCOPE", "SKIPPED_BY_DEPENDENCY"}
    engine_gaps = _as_rows(engine.get("known_gaps"))
    missing_applicability = any(row["applicability"] is None for row in matrix)
    audit_engine_result = _aggregate_engine_result(stage_rows)
    if (audit_engine_result in {"INSPECTION_ERROR", "NOT_EVALUABLE"}
            or results & {"INSPECTION_ERROR", "NOT_EVALUABLE"} or results - recognized_results
            or engine_gaps or missing_applicability or not matrix or accounting_gap != 0):
        readiness = "NO ES POSIBLE EMITIR CONCLUSIÓN"
    elif audit_engine_result == "FAIL_TECHNICAL" or results & {"FAIL", "FAIL_TECHNICAL"}:
        readiness = "REQUIERE CORRECCIÓN ANTES DE PUBLICACIÓN"
    elif results & {"NOT_APPLICABLE", "DEFERRED", "OUT_OF_SCOPE"} or findings:
        readiness = "APTO CON OBSERVACIONES"
    else:
        readiness = "APTO PARA PUBLICACIÓN SEGÚN ALCANCE EVALUADO"

    coverage = interpretation.get("coverage", {}) if isinstance(interpretation, Mapping) else {}
    coverage = coverage if isinstance(coverage, Mapping) else {}
    source_hash = compliance.get("reference_sha256")
    source_status = "VERSION_UNKNOWN"
    return {
        "contract": REPORT_CONTRACT,
        "sections": list(SECTIONS),
        "audit": {
            "audit_id": manifest.get("audit_id"), "client_project_id": manifest.get("client_project_id"),
            "dataset_id": identity.get("dataset_id"), "source_filename": identity.get("source_filename"),
            "source_sha256": identity.get("source_sha256"), "source_size_bytes": identity.get("source_size_bytes"),
            "ingestion_timestamp_utc": identity.get("ingestion_timestamp_utc"),
            "jurisdiction": "No declarada en el contrato de auditoría; no se infiere jurisdicción legal.",
            "cutoff_date": str(run.get("started_at_utc") or "NOT_EVALUABLE"),
            "workflow_status": manifest.get("status"),
        },
        "scope": {"protocol": "GTFS Schedule", "stages": ["G03", "G04", "G05", "G06", "G07", "G08"],
                  "excluded": ["GTFS-RT", "SIRI", "NeTEx", "certificación administrativa o legal"],
                  "legal_conclusion_allowed": False},
        "summary": {"technical_result": audit_engine_result,
                    "legacy_result": legacy_result,
                    "legacy_summary_result": legacy_summary_result,
                    "legacy_summary_consistency": legacy_summary_consistency,
                    "audit_engine_result": audit_engine_result,
                    "compliance_result": compliance.get("result", "NOT_EVALUABLE"),
                    "finding_count": len(findings), "publication_readiness": readiness,
                    "accounting": {key: coverage.get(key) for key in (
                        "raw_finding_count", "consolidated_occurrence_count",
                        "unclassified_occurrence_count", "accounting_gap")}},
        "validation_matrix": matrix,
        "compliance": {"result": compliance.get("result", "NOT_EVALUABLE"),
                       "rule_id": compliance.get("rule_id"), "rule_version": compliance.get("rule_version"),
                       "evaluator_version": compliance.get("evaluator_version"),
                       "evaluator_sha256": compliance.get("evaluator_sha256"),
                       "reference_sha256": source_hash,
                       "legal_conclusion_allowed": False},
        "sources": ([{"identity": "Compliance V1 captured technical reference", "source_type": "TECHNICAL_SPECIFICATION",
                       "source_status": source_status, "version": "VERSION_UNKNOWN",
                       "sha256": source_hash, "applicability": "CONDITIONAL",
                       "note": "El artefacto no identifica versión normativa ni jurisdicción; este estado no interpreta vigencia jurídica."}]
                    if source_hash else []),
        "not_applicable": [row for row in matrix if row["applicability"] == "NOT_APPLICABLE"],
        "not_evaluable": [row for row in matrix if row["evaluability"] == "NOT_EVALUABLE"],
        "findings": list(findings),
        "finding_origin_counts": dict(sorted(Counter(str(row.get("origin", "UNKNOWN")) for row in findings).items())),
        "interpretation": {"status": manifest.get("audit_interpretation", {}).get("status"),
                           "accounting_gap": coverage.get("accounting_gap"),
                           "families": interpretation.get("finding_families", []) if isinstance(interpretation, Mapping) else []},
        "remediation": dict(remediation),
        "comparison": dict(comparison) if comparison else None,
        "gis": run.get("gis", {}),
        "traceability": {"dataset_identity": "dataset_identity.json", "manifest": "audit_manifest.json",
                         "seal": "delivery_seal.json", "engine_report": "engine_run/engine_report.json",
                         "findings": "findings.json", "interpretation": "AUDIT_CONSOLIDATED.json"},
        "limitations": ["La evaluación es técnica, independiente y limitada al alcance y evidencia enumerados.",
                        "Un finding técnico no constituye por sí mismo incumplimiento legal.",
                        "No se infieren fuentes vigentes, derogadas o supersedidas si el artefacto no aporta esos estados.",
                        "El motor y sus artefactos persistidos son autoritativos; este modelo solo proyecta sus resultados."],
    }


def render_client_report(report: Mapping[str, Any]) -> str:
    audit = report["audit"]
    summary = report["summary"]
    lines = ["# Informe de auditoría técnico-regulatoria GTFS", "",
             "Evaluación independiente, limitada al alcance y a la evidencia identificados. No es una certificación administrativa ni jurídica.", "",
             "## 1. Portada", "", "**Transit Data Lab — Auditoría técnico-regulatoria**", "",
             "## 2. Identificación de la auditoría", "",
             f"- Auditoría: `{audit.get('audit_id')}` · Dataset: `{audit.get('dataset_id')}`",
             f"- Archivo: `{audit.get('source_filename')}` ({audit.get('source_size_bytes')} bytes)",
             f"- SHA-256: `{audit.get('source_sha256')}` · Inicio UTC: `{audit.get('ingestion_timestamp_utc')}`",
             f"- Estado workflow: `{audit.get('workflow_status')}`", "",
             "## 3. Resumen ejecutivo", "",
             f"Motor técnico GTFS G03–G07: **{summary['audit_engine_result']}**. Validación legacy: **{summary['legacy_result']}** (resumen legacy: {summary['legacy_summary_result']}; coherencia interna: {summary['legacy_summary_consistency']}). Compliance V1: **{summary['compliance_result']}**. Hallazgos: **{summary['finding_count']}**.",
             f"Conclusión de publicación según alcance evaluado: **{summary['publication_readiness']}**.",
             "No se calcula puntuación global de calidad ni de cumplimiento legal.", "",
             "## 4. Alcance", "", "GTFS Schedule; resultados legacy, G03–G08 y Compliance V1 se identifican por separado.", "",
             "## 5. Jurisdicción", "", audit["jurisdiction"], "",
             "## 6. Fecha de corte", "", f"Inicio de ejecución: `{audit['cutoff_date']}`. No se atribuye fecha de vigencia normativa.", "",
             "## 7. Exclusiones", "", *[f"- {item}" for item in report["scope"]["excluded"]], "",
             "## 8. Metodología", "", "Ingesta con identidad SHA-256, ejecución de reglas registradas, interpretación y consolidación derivadas, artefactos sellados. La interpretación no modifica los findings brutos.", "",
             "## 9. Perfil del dataset", "", f"Identidad `{audit.get('dataset_id')}`; tamaño {audit.get('source_size_bytes')} bytes; procedencia declarada por intake.", "",
             "## 10. Validación técnica GTFS", "", f"Motor G03–G07: `{summary['audit_engine_result']}`. Validación legacy: `{summary['legacy_result']}`; resumen legacy: `{summary['legacy_summary_result']}` (coherencia interna: {summary['legacy_summary_consistency']}). Véase la matriz completa y los artefactos de ambos orígenes.", "",
             "## 11. Matriz completa de validaciones", "",
             "| Dominio / etapa | Regla | Descripción | Requisito | Aplicabilidad | Evaluabilidad | Resultado | Severidad* | Hallazgos | Evidencia | Fuente |",
             "|---|---|---|---|---|---|---|---|---:|---|---|"]
    for row in report["validation_matrix"]:
        refs = ", ".join(row["evidence_refs"]) or "—"
        cells = (row["domain"], row["rule_id"], row["description"], row.get("requirement") or "—", row["applicability"] or "NO DISPONIBLE EN ARTEFACTO", row["evaluability"], row["result"], row.get("severity") or "—", str(row["finding_count"]), refs, str(row.get("source_ref") or "—"))
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
    lines.extend(["", "*Aplicabilidad se informa desde el artefacto; si falta, se indica como no disponible. Severity sólo se muestra cuando la regla fuente la define.*", "",
                  "## 12. Evaluación regulatoria / Compliance", "",
                  f"Compliance V1: `{report['compliance']['result']}` ({report['compliance'].get('rule_id') or 'sin ID'}); evaluador `{report['compliance'].get('evaluator_version') or 'VERSION_UNKNOWN'}`. `legal_conclusion_allowed = false`.", "",
                  "## 13. Fuentes normativas aplicables", "", "No se adjunta una determinación de fuentes normativas aplicables a esta auditoría. La referencia técnica capturada no basta para inferir aplicabilidad jurídica.", "",
                  "## 14. No aplicable", "", *([f"- `{row['rule_id']}` ({row['stage']})" for row in report["not_applicable"]] or ["- No hay reglas marcadas NOT_APPLICABLE."]), "",
                  "## 15. No evaluable", "", *([f"- `{row['rule_id']}` ({row['stage']}): {row['result']}" for row in report["not_evaluable"]] or ["- No hay reglas marcadas NOT_EVALUABLE."]), "",
                  "## 16. Fuentes superseded / repealed / version unknown", "",
                  *([f"- {s['identity']}: `{s['source_status']}`; versión `{s['version']}`; SHA-256 `{s['sha256']}`. {s['note']}" for s in report["sources"]] or ["- El artefacto no aporta estados de fuente."]), "",
                  "## 17. Hallazgos técnicos", "", f"Se entregan {len(report['findings'])} findings con origen separado: `{report['finding_origin_counts']}`. Consulte `findings.json`.", "",
                  "## 18. Familias consolidadas", "", f"Estado de interpretación: `{report['interpretation'].get('status')}`; familias: {len(report['interpretation']['families'])}.", "",
                  "## 19. Evidencia", "", "Cada fila de la matriz enlaza los findings asociados. Los artefactos de motor, evidencia y manifests se conservan en la entrega.", "",
                  "## 20. Impacto", "", "El informe no infiere impacto operativo global. Consulte el impacto directo y sus límites en `AUDIT_CONSOLIDATED.json`.", "",
                  "## 21. Interpretación", "", f"Brecha contable findings: `{report['interpretation'].get('accounting_gap')}`; el artefacto consolidado mantiene la clasificación e incertidumbre.", "",
                  "## 22. Recomendaciones", "", "Revise cada recomendación con el contexto del titular del feed; no se prescribe corrección automática.", "",
                  "## 23. Remediación", "", f"Decisión: `{report['remediation'].get('decision')}`. {report['remediation'].get('reason', '')}", "",
                  "## 24. GIS / revisión geográfica", "", f"Estados GIS: `{report['gis']}`. GeoJSON/KML están disponibles cuando los produjo el motor; QGIS es externo y opcional.", "",
                  "## 25. Publication readiness", "", f"**{summary['publication_readiness']}**. Conclusión limitada a las reglas, versión, datos y evidencia de esta ejecución.", "",
                  "## 26. Limitaciones", "", *[f"- {item}" for item in report["limitations"]], "",
                  "## 27. Trazabilidad / reproducibilidad", "", *[f"- {key}: `{value}`" for key, value in report["traceability"].items()], "",
                  "## 28. Disclaimer", "", "Esta auditoría técnico-regulatoria es independiente y acotada por alcance y evidencia. No es certificación oficial, validación de autoridad competente, garantía de aceptación NAP ni declaración de cumplimiento legal.", "",
                  "## 29. Anexos técnicos", "", "La entrega incluye manifiesto, sello, runs, informe de motor, matriz JSON, findings y artefacto de interpretación. Los artefactos del motor prevalecen sobre esta presentación.", "",
                  "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""])
    return "\n".join(lines)
