"""Deterministic presentation PDF generated from sealed workflow data."""
from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


def _text(value: object, *, limit: int = 800) -> str:
    from .client_workflow import _redact_path_text

    return escape(_redact_path_text(str(value))[:limit]).replace("\n", "<br/>")


def _family_rows(interpretation: dict[str, Any] | None,
                 findings: list[dict[str, Any]]) -> list[list[str]]:
    if not interpretation:
        return []
    rows: list[list[str]] = []
    recommendations: dict[tuple[str, str, str], str] = {}
    for finding in findings:
        recommendation = finding.get("recommendation")
        key = (str(finding.get("rule_id", "")), str(finding.get("stage", "")),
               str(finding.get("source_file", "")))
        if recommendation and key not in recommendations:
            recommendations[key] = str(recommendation)
    for family in interpretation.get("finding_families", []):
        impact = family.get("operational_impact", {})
        direct = impact.get("direct_affected", {}) if isinstance(impact, dict) else {}
        patterns = family.get("patterns", [])
        pattern = patterns[0].get("classification", "NOT_EVALUABLE") if patterns else "NOT_EVALUABLE"
        references = family.get("evidence_refs", [])
        evidence_ref = references[0] if references else {}
        rows.append([
            str(family.get("rule_id", "—")),
            str(family.get("raw_occurrence_count", 0)),
            str(direct.get("entity_type", "—")),
            str(direct.get("entity_count", "—")),
            str(pattern),
            recommendations.get((str(family.get("rule_id", "")), str(family.get("stage", "")),
                                 str(family.get("source_file", ""))), "Consultar artefactos fuente"),
            str(evidence_ref.get("source_file", family.get("source_file", "—"))),
        ])
    return rows


def write_professional_pdf(path: Path, manifest: dict[str, Any],
                           interpretation: dict[str, Any] | None,
                           run: dict[str, Any], findings: list[dict[str, Any]], *,
                           report_model: dict[str, Any] | None = None) -> None:
    """Write a print-friendly report; JSON/manifest remain authoritative."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle,
    )
    import reportlab

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    regular = font_dir / "Vera.ttf"
    bold = font_dir / "VeraBd.ttf"
    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError("No se encuentran las fuentes Unicode empaquetadas de ReportLab")
    if "TDLVera" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("TDLVera", str(regular)))
        pdfmetrics.registerFont(TTFont("TDLVera-Bold", str(bold)))

    width, height = A4
    margin_x, top_margin, bottom_margin = 20 * mm, 22 * mm, 18 * mm
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TDLTitle", parent=styles["Title"], fontName="TDLVera-Bold",
                              fontSize=21, leading=27, textColor=colors.HexColor("#18344F"), alignment=TA_LEFT, spaceAfter=8))
    styles.add(ParagraphStyle(name="TDLHeading", parent=styles["Heading2"], fontName="TDLVera-Bold",
                              fontSize=12, leading=16, textColor=colors.HexColor("#18344F"), spaceBefore=12, spaceAfter=5))
    styles.add(ParagraphStyle(name="TDLBody", parent=styles["BodyText"], fontName="TDLVera",
                              fontSize=8.6, leading=12, spaceAfter=4))
    styles.add(ParagraphStyle(name="TDLSmall", parent=styles["BodyText"], fontName="TDLVera",
                              fontSize=7.2, leading=9, textColor=colors.HexColor("#526171")))
    styles.add(ParagraphStyle(name="TDLCell", parent=styles["BodyText"], fontName="TDLVera",
                              fontSize=7, leading=9, wordWrap="CJK"))
    styles.add(ParagraphStyle(name="TDLCellHead", parent=styles["BodyText"], fontName="TDLVera-Bold",
                              fontSize=7, leading=9, textColor=colors.white))

    def decorate(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D7DEE6"))
        canvas.line(margin_x, 14 * mm, width - margin_x, 14 * mm)
        canvas.setFont("TDLVera", 7)
        canvas.setFillColor(colors.HexColor("#526171"))
        canvas.drawString(margin_x, 10 * mm, "Transit Data Lab | Informe técnico GTFS | Todos los derechos reservados")
        canvas.drawRightString(width - margin_x, 10 * mm, f"Página {doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(str(output), pagesize=A4, leftMargin=margin_x, rightMargin=margin_x,
                          topMargin=top_margin, bottomMargin=bottom_margin,
                          title="Informe de auditoría GTFS", author="Yeison Arbey Carrillo Lemus",
                          subject="Informe de presentación derivado de evidencia técnica")
    frame = Frame(margin_x, bottom_margin, width - 2 * margin_x, height - top_margin - bottom_margin,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body")
    doc.addPageTemplates([PageTemplate(id="tdl", frames=frame, onPage=decorate)])

    identity = manifest.get("dataset_identity", {})
    identity = identity if isinstance(identity, dict) else {}
    coverage = interpretation.get("coverage", {}) if interpretation else {}
    coverage = coverage if isinstance(coverage, dict) else {}
    audit_id = manifest.get("audit_id", "NOT_EVALUABLE")
    versions = manifest.get("engine_versions", {})
    client_version = versions.get("client_application", "NOT_EVALUABLE") if isinstance(versions, dict) else "NOT_EVALUABLE"
    story = [Paragraph("Informe de auditoría GTFS", styles["TDLTitle"]),
             Paragraph(f"Cliente { _text(client_version) } | Resumen profesional derivado de artefactos técnicos; no es una certificación legal.", styles["TDLBody"]),
             Spacer(1, 5 * mm)]
    metadata = [
        ["Identidad dataset", identity.get("dataset_id", "NOT_EVALUABLE"), "Estado", manifest.get("status", "NOT_EVALUABLE")],
        ["Archivo fuente", identity.get("source_filename", "NOT_EVALUABLE"), "Auditoría", audit_id],
        ["SHA-256", identity.get("source_sha256", "NOT_EVALUABLE"), "Recibido UTC", identity.get("ingestion_timestamp_utc", "NOT_EVALUABLE")],
    ]
    info = Table([[Paragraph(_text(x, limit=240), styles["TDLCell"]) for x in row] for row in metadata],
                 colWidths=[30 * mm, 67 * mm, 24 * mm, 49 * mm])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F5")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#EAF0F5")),
        ("FONTNAME", (0, 0), (-1, -1), "TDLVera"), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#CAD3DC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [info, Paragraph("Resumen ejecutivo", styles["TDLHeading"])]
    story.append(Paragraph(
        f"Validación técnica: <b>{_text(run.get('summary', {}).get('validation', 'NOT_EVALUABLE'))}</b>. "
        f"Hallazgos brutos: <b>{coverage.get('raw_finding_count', 'NOT_EVALUABLE')}</b>; "
        f"ocurrencias consolidadas: <b>{coverage.get('consolidated_occurrence_count', 'NOT_EVALUABLE')}</b>; "
        f"sin clasificar: <b>{coverage.get('unclassified_occurrence_count', 'NOT_EVALUABLE')}</b>; "
        f"brecha contable: <b>{coverage.get('accounting_gap', 'NOT_EVALUABLE')}</b>. "
        "No se calcula una puntuación global. Un hallazgo técnico no demuestra por sí mismo incumplimiento legal.",
        styles["TDLBody"]))
    story += [Paragraph("Metodología y límites", styles["TDLHeading"]),
              Paragraph("Auditoría local del GTFS Schedule mediante el workflow y motor identificados en la entrega. "
                        "La interpretación es una capa derivada; los JSON, manifest, seal y evidencia técnica conservan la fuente autoritativa. "
                        "Poblaciones ausentes, limitaciones y estados NOT_EVALUABLE mantienen su significado.", styles["TDLBody"])]
    story.append(Paragraph("Familias de hallazgos consolidados", styles["TDLHeading"]))
    rows = _family_rows(interpretation, findings)
    if rows:
        headers = ["Regla", "Ocurrencias", "Entidad", "Afectadas", "Patrón", "Recomendación", "Evidencia"]
        data = [[Paragraph(_text(value), styles["TDLCellHead"]) for value in headers]]
        data.extend([[Paragraph(_text(value, limit=180), styles["TDLCell"]) for value in row] for row in rows[:250]])
        table = Table(data, colWidths=[16 * mm, 21 * mm, 16 * mm, 18 * mm, 27 * mm, 42 * mm, 30 * mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#18344F")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
            ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#CAD3DC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(table)
        if len(rows) > 250:
            story.append(Paragraph(f"Se muestran 250 de {len(rows)} familias. El resultado JSON de interpretación es la fuente completa.", styles["TDLSmall"]))
    else:
        story.append(Paragraph("No hay familias consolidadas disponibles; consulte audit_interpretation_status.json.", styles["TDLBody"]))
    story += [Paragraph("Recomendaciones y alcance", styles["TDLHeading"]),
              Paragraph("Revise recomendaciones y referencias de evidencia en `AUDIT_CONSOLIDATED.json`, `findings.json` y los artefactos del motor. "
                        "Este PDF es una vista de presentación; no sustituye esos ficheros ni crea una autoridad adicional.", styles["TDLBody"])]
    gis = run.get("gis", {})
    gis_status = ", ".join(f"{name}: {result.get('status', 'NOT_EVALUABLE')}" for name, result in gis.items() if isinstance(result, dict)) if isinstance(gis, dict) else "NOT_EVALUABLE"
    if not gis_status:
        gis_status = "NOT_EVALUABLE"
    story.append(Paragraph(f"Evidencia GIS: {_text(gis_status)}. Consulte las capas GeoJSON/KML de la entrega y GIS_QGIS_GUIDE.md cuando estén disponibles.", styles["TDLBody"]))
    story.append(Paragraph("Limitaciones: interpretación técnica, alcance GTFS Schedule declarado por el motor, revisión humana de hallazgos e inferencias, y brechas/estados no evaluables preservados en la evidencia fuente.", styles["TDLBody"]))
    story.append(Paragraph(f"Referencias de reproducibilidad: audit_id={_text(audit_id)}; source_sha256={_text(identity.get('source_sha256', 'NOT_EVALUABLE'))}; audit_manifest.json; delivery_seal.json.", styles["TDLSmall"]))
    if report_model:
        audit = report_model.get("audit", {})
        summary_model = report_model.get("summary", {})
        compliance_model = report_model.get("compliance", {})
        interpretation_model = report_model.get("interpretation", {})
        scope = report_model.get("scope", {})
        matrix_rows = report_model.get("validation_matrix", [])
        sources = report_model.get("sources", [])
        not_applicable = report_model.get("not_applicable", [])
        not_evaluable = report_model.get("not_evaluable", [])
        sections = [
            ("1. Portada", "Transit Data Lab — evaluación independiente acotada por alcance y evidencia."),
            ("2. Identificación de la auditoría", f"Auditoría {audit.get('audit_id')}; proyecto {audit.get('client_project_id')}; dataset {audit.get('dataset_id')}; SHA-256 {audit.get('source_sha256')}; recibido UTC {audit.get('ingestion_timestamp_utc')}."),
            ("3. Resumen ejecutivo", f"Motor GTFS G03–G07 {summary_model.get('audit_engine_result')}; validación legacy {summary_model.get('legacy_result')}; Compliance V1 {summary_model.get('compliance_result')}; findings {summary_model.get('finding_count')}; publication readiness {summary_model.get('publication_readiness')}. Sin puntuación global."),
            ("4. Alcance", f"Protocolo: {scope.get('protocol')}. Etapas: {', '.join(scope.get('stages', []))}."),
            ("5. Jurisdicción", str(audit.get("jurisdiction", "No declarada; no se infiere."))),
            ("6. Fecha de corte", f"Inicio UTC {audit.get('cutoff_date')}; no representa vigencia jurídica."),
            ("7. Exclusiones", "; ".join(scope.get("excluded", []))),
            ("8. Metodología", "Ejecución técnica sobre copia de trabajo con identidad congelada; interpretación derivada y separada de los findings brutos."),
            ("9. Perfil del dataset", f"{audit.get('source_filename')}; {audit.get('source_size_bytes')} bytes; identidad {audit.get('dataset_id')}."),
            ("10. Validación técnica GTFS", f"Motor G03–G07: {summary_model.get('audit_engine_result')}. Validación legacy: {summary_model.get('legacy_result')} (resumen {summary_model.get('legacy_summary_result')}; coherencia interna {summary_model.get('legacy_summary_consistency')}). Consulte la matriz y los artefactos de ambos orígenes."),
            ("11. Matriz completa de validaciones", "Cada regla ejecutada aparece con aplicabilidad, evaluabilidad, resultado, conteo y referencia de evidencia."),
            ("12. Evaluación regulatoria / Compliance", f"{compliance_model.get('rule_id')}: {compliance_model.get('result')}; evaluador {compliance_model.get('evaluator_version')}; conclusión legal permitida: {compliance_model.get('legal_conclusion_allowed')}."),
            ("13. Fuentes normativas aplicables", "No se adjunta una determinación de fuentes normativas aplicables; la referencia técnica no establece aplicabilidad legal."),
            ("14. No aplicable", "; ".join(row.get("rule_id", "") for row in not_applicable) or "No hay reglas marcadas."),
            ("15. No evaluable", "; ".join(f"{row.get('rule_id')}: {row.get('result')}" for row in not_evaluable) or "No hay reglas marcadas."),
            ("16. Estado de fuentes", "; ".join(f"{row.get('identity')}: {row.get('source_status')} / {row.get('version')}" for row in sources) or "No se atribuye estado no documentado."),
            ("17. Hallazgos técnicos", f"{summary_model.get('finding_count')} findings; consulte `findings.json` para evidencia por origen."),
            ("18. Familias consolidadas", f"Familias: {len(interpretation_model.get('families', []))}; consulte AUDIT_CONSOLIDATED.json."),
            ("19. Evidencia", "La matriz enlaza los findings por índice estable dentro de findings.json."),
            ("20. Impacto", "El impacto operativo no se infiere globalmente; las estimaciones directas y sus límites están en el artefacto consolidado."),
            ("21. Interpretación", f"Estado {interpretation_model.get('status')}; brecha contable {interpretation_model.get('accounting_gap')}."),
            ("22. Recomendaciones", "Las recomendaciones técnicas requieren revisión con el titular del feed; no se genera autocorrección genérica."),
            ("23. Remediación", f"Decisión {report_model.get('remediation', {}).get('decision')}: {report_model.get('remediation', {}).get('reason', '')}"),
            ("24. GIS / revisión geográfica", f"Estados GIS: {run.get('gis', {})}; capas disponibles cuando las produjo el motor."),
            ("25. Publication readiness", str(summary_model.get("publication_readiness", "NO ES POSIBLE EMITIR CONCLUSIÓN"))),
            ("26. Limitaciones", "; ".join(report_model.get("limitations", [])) or "La evaluación es técnica e independiente."),
            ("27. Trazabilidad / reproducibilidad", "; ".join(f"{key}: {value}" for key, value in report_model.get("traceability", {}).items())),
            ("28. Disclaimer", "No es certificación oficial, validación de autoridad competente, garantía de aceptación NAP ni declaración de cumplimiento legal."),
            ("29. Anexos técnicos", "El manifest, sello, matriz JSON, runs, findings, interpretación y evidencia del motor acompañan esta vista PDF."),
        ]
        story += [PageBreak(), Paragraph("Informe cliente — contrato V1", styles["TDLTitle"])]
        for heading, body in sections:
            story.append(Paragraph(_text(heading), styles["TDLHeading"]))
            story.append(Paragraph(_text(body, limit=1600), styles["TDLBody"]))
        story.append(Paragraph("Matriz completa de validaciones", styles["TDLHeading"]))
        if matrix_rows:
            headers = ["Etapa", "Regla", "Aplicabilidad", "Evaluabilidad", "Resultado", "Severidad", "Findings", "Evidencia"]
            data = [[Paragraph(_text(value), styles["TDLCellHead"]) for value in headers]]
            for row in matrix_rows:
                values = [row.get("stage", "—"),
                          f"{row.get('rule_id', '—')} — {row.get('description', '—')} (Requisito: {row.get('requirement') or '—'})",
                          row.get("applicability") or "NO DISPONIBLE EN ARTEFACTO", row.get("evaluability", "—"),
                          row.get("result", "—"), row.get("severity") or "—", row.get("finding_count", 0),
                          f"Evidencia: {row.get('evidence_refs') or '—'}; fuente: {row.get('source_ref') or '—'}"]
                data.append([Paragraph(_text(value, limit=220), styles["TDLCell"]) for value in values])
            table = Table(data, colWidths=[15 * mm, 38 * mm, 22 * mm, 22 * mm, 22 * mm, 15 * mm, 14 * mm, 22 * mm], repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#18344F")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7F9")]),
                ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#CAD3DC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(table)
        story += [Paragraph("Fuentes y delimitación regulatoria", styles["TDLHeading"]),
                  Paragraph("La evidencia disponible no establece por sí sola jurisdicción ni vigencia legal de una fuente. No se infiere cumplimiento normativo, aceptación NAP ni certificación oficial.", styles["TDLBody"]),
                  Paragraph("La matriz completa, estados de fuente, findings, interpretación y trazabilidad están en report/client_report.json y los artefactos autoritativos incluidos en la entrega.", styles["TDLSmall"])]
    doc.build(story)
