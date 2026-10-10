"""PDF views of the common professional presentation model."""
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle


def build_pdfs(model, output: Path):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TextTDL", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=7))
    styles.add(ParagraphStyle(name="SmallTDL", fontName="Helvetica", fontSize=8, leading=11, spaceAfter=5))
    def p(text, style="TextTDL"):
        return Paragraph(escape(str(text)), styles[style])
    identity = model["identity"]; cov = model["coverage"]; view = model["presentation"]
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Helvetica", 7)
        canvas.drawString(18*mm, 10*mm, identity["client_audit_id"] + " | " + identity["revision"] + " | Revisión humana de emisión pendiente")
        canvas.drawRightString(192*mm, 10*mm, str(doc.page)); canvas.restoreState()
    def render(name, story):
        doc = SimpleDocTemplate(str(output / name), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                                topMargin=18*mm, bottomMargin=22*mm, title="Auditoría GTFS " + identity["revision"], author="Transit Data Lab")
        doc.build(story, onFirstPage=footer, onLaterPages=footer)
    def section(label, text): return [p(label, "Heading2"), p(text)]
    title = [p("Informe de auditoría GTFS", "Title"), p("Ejecución fuente: " + identity["client_audit_id"] + ". Revisión: " + identity["revision"], "SmallTDL")]
    summary = [p("Conclusión y alcance", "Heading1"), p(view["technical_text"] + "."), p(view["use_text"] + "."), p(view["basis"]),
               p(f"Se conservan {cov['source_record_count']} registros de evidencia. {cov['reconciled_event_count']} eventos reconciliados, {cov['duplicate_source_reference_count']} referencias duplicadas. {cov['unclassified_record_count']} registros pendientes de decisión."),
               p("Motivos", "Heading2")]
    summary += [p(c["title"]) for c in model["client_cases"]]
    if model["pending_records"]: summary += [p("Hay resultados sin decisión revisada. Su detalle completo se conserva en el libro y en la evidencia.")]
    if not model["cases"] and not model["pending_records"]: summary += [p("No hay hallazgos en la evidencia aportada. Esto no acredita cobertura suficiente para un uso no definido.")]
    summary += [p("Siguiente paso", "Heading2"), p(view["steps"][0]["action"]), p("Límites", "Heading2"),
                p("No se ha verificado una corrección del productor. El análisis regulatorio incluido es técnico y no acredita cumplimiento jurídico integral. La emisión y la aceptación visual del mapa están pendientes.")]
    story = title + summary + [PageBreak(), p("Secuencia de actuación", "Heading1"),
        p("El orden propuesto responde a dependencias de trabajo. La urgencia y cualquier impedimento para el destino requieren conocer el uso, la fecha prevista y los requisitos del consumidor. El responsable del servicio y el destinatario pueden aportar estos datos.")]
    for step in view["steps"]:
        story += section(f"{step['order']}. {step['action']}", "Fundamento: " + step["basis"])
        story += [p("Casos: " + (", ".join(step["case_ids"]) or "Alcance general"), "SmallTDL"), p("Información necesaria: " + step["missing"])]
    for case, client in zip(model["cases"], model["client_cases"]):
        story += [PageBreak(), p(client["title"], "Heading1"), p("Ficha " + client["case_id"], "SmallTDL"),
                  p(client["disposition_text"] + ". " + client["priority_text"] + "."),
                  p(client["producer_text"] + ". " + client["reaudit_text"] + "."),
                  p(f"{case['reconciled_event_count']} eventos; {case['occurrence_count']} registros de procedencia. " + client["entities_text"] + ".")]
        for label, key in (("Qué se ha observado", "observation"), ("Criterio aplicado", "criterion"), ("Acción propuesta", "action"),
                           ("Qué permite cerrar el caso", "closure_criteria"), ("Impacto demostrado", "impact_known"), ("Consecuencia posible", "impact_potential")):
            story += section(label, client[key])
        story += [p("Evidencia y límites", "Heading2")]
        story += [p(text, "SmallTDL") for text in client["evidence"] + client["limitations"]]
        story += [p("Referencias originales y códigos fuente: hoja Ocurrencias y AUDIT_CASES.json. La comunicación de una corrección no equivale a cierre verificado.", "SmallTDL")]
    story += [PageBreak(), p("Trazabilidad y limitaciones", "Heading1")]
    for key, label in (("client_audit_id", "Ejecución cliente"), ("audit_execution_id", "Ejecución del motor"), ("revision", "Revisión de presentación"), ("source_sha256", "SHA-256 de la fuente")):
        story += section(label, identity[key])
    story += [p(f"Control de conservación: {cov['accounting_gap']} registros sin reconciliar fuera de la cobertura declarada.")]
    story += [p(text) for text in view["limitations"]]
    story += [p("La evidencia histórica se conserva. Esta revisión utiliza la ejecución fuente indicada arriba; no realiza una nueva auditoría del motor ni sustituye entregas anteriores."),
              p("La integridad de toda esta revisión, incluidos los archivos añadidos después de la ejecución, se comprueba mediante PACKAGE_MANIFEST.json y PACKAGE_SEAL.json. Consulte EVIDENCE_INDEX.md y 03_SOURCE_DELIVERY."),
              p("Detalle técnico", "Heading2"), p("Resultado original: " + model["case_contract"]["technical_result"] + ". Estado original de destino: " + model["case_contract"]["use_readiness"]["status"] + ".", "SmallTDL")]
    render("Informe_auditoria.pdf", story)
    readme = [p("Expediente de auditoría GTFS", "Title"), p("Ejecución fuente: " + identity["client_audit_id"] + ". Revisión: " + identity["revision"]),
              p(view["technical_text"] + ". " + view["use_text"] + "."),
              p("Leer primero Informe_auditoria.pdf. Usar Plan_de_accion_y_hallazgos.xlsx para buscar los casos, localizar sus registros y preparar el seguimiento. Abrir Mapa_auditoria.kmz en un visor local compatible."),
              p("Los casos sin localización comprobable figuran en el libro y el informe. Los elementos de contexto del mapa no significan que no existan defectos."),
              p("02_EVIDENCIAS contiene decisiones, modelo, índice, controles GIS y manifiesto de integridad. 03_SOURCE_DELIVERY conserva la entrega de la ejecución fuente."),
              p("La revisión no acredita correcciones del productor, aceptación del cliente ni cumplimiento jurídico. Aceptación visual del mapa y revisión humana de emisión pendientes."),
              p("Run de motor: " + identity["audit_execution_id"], "SmallTDL"), p("Fuente SHA-256: " + identity["source_sha256"], "SmallTDL")]
    render("LEEME.pdf", readme)
