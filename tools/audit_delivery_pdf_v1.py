"""Spanish audience-specific views of the same frozen report model."""
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

NAVY = colors.HexColor("#163247")
TEAL = colors.HexColor("#007E87")
PALE = colors.HexColor("#EDF4F6")
STATUS = {"PASS": "Sin incidencias", "FAIL_TECHNICAL": "Incidencias técnicas",
          "NOT_EVALUABLE": "No evaluable", "NOT_APPLICABLE": "No aplicable"}
UNITS = {"SUPPLIED_FIELD_VALUE": "valores informados", "EXACT_TIMES_1_INTERVAL": "intervalos",
         "SHAPE_TRANSITION": "transiciones del trazado", "XML_FILE": "ficheros"}
TITLES = {"PAL-G03-COLOR": "Colores de las líneas", "PAL-G04-PARENT": "Relación entre paradas y estaciones",
          "PAL-G04-SHAPE": "Asignación de trazados a viajes", "PAL-G06-FREQUENCY": "Coherencia de los intervalos de salida",
          "PAL-G07-DUP": "Puntos consecutivos repetidos en el trazado", "PAL-G07-EQUAL": "Distancias iguales entre puntos diferentes",
          "NETEX-SYNTHETIC-MALFORMED-REFERENCE": "Fichero que no puede interpretarse"}
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle("TDLBody", fontName="Helvetica", fontSize=10, leading=14, textColor=NAVY, spaceAfter=8))
STYLES.add(ParagraphStyle("TDLSmall", parent=STYLES["TDLBody"], fontSize=8, leading=11, spaceAfter=5))
STYLES.add(ParagraphStyle("TDLTitle", parent=STYLES["TDLBody"], fontSize=24, leading=28, spaceAfter=18))
STYLES.add(ParagraphStyle("TDLHeading", parent=STYLES["TDLBody"], fontSize=15, leading=19, textColor=TEAL, spaceBefore=10, spaceAfter=10))


def p(text, style="TDLBody"):
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), STYLES[style])


def heading(text): return p(text, "TDLHeading")
def number(value): return f"{value:,}".replace(",", ".")


def exposure(case):
    e = case["exposure"]
    return f"{number(e['affected_count'])} de {number(e['eligible_count'])} {UNITS[e['unit']]}"


def table(rows, widths, small=True):
    style = "TDLSmall" if small else "TDLBody"
    data = [[p(v, style) for v in row] for row in rows]
    result = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PALE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), .4, colors.HexColor("#D1DFE5"))]))
    return result


def counts(model):
    c = model["conclusion"]["unique_control_counts"]
    return " | ".join(f"{c.get(key, 0)} {label.lower()}" for key, label in STATUS.items())


def cover(model, audience):
    synthetic = model["format"] == "NETEX"
    return [p("TRANSIT DATA LAB", "TDLHeading"), p("Informe para " + audience, "TDLTitle"),
            p(model["label"], "TDLHeading"), p("Referencia sintética interna" if synthetic else "Revisión de una ejecución existente"),
            p("Edición de entrega: 8 de octubre de 2026. No se ha ejecutado de nuevo el motor."),
            p(model["scope_note"]), heading("Conclusión"),
            p("El fichero de ejemplo no puede interpretarse. La validación del esquema quedó sin evaluar." if synthetic else
              "Se documentan incidencias en la información del servicio y partes que todavía no se han podido comprobar."),
            p(f"{len(model['controls'])} controles distintos: {counts(model)}."),
            p(f"{len(model['cases'])} grupo(s) de hallazgos. Un mismo control puede originar varios grupos y un grupo puede aparecer en dos capas de validación."),
            heading("Decisión pendiente"),
            p("Definir dónde se utilizará el fichero y qué condiciones exige ese destinatario. Encargar al equipo productor una propuesta de corrección y comprobarla con una nueva revisión."),
            p("La prioridad y el bloqueo para el destinatario no están determinados. Los recuentos no demuestran costes, viajeros afectados ni perjuicios reales."),
            p("Entrega privada pendiente de revisión humana y de prueba de comprensión con sus destinatarios.", "TDLSmall")]


def management(model):
    story = cover(model, "dirección") + [PageBreak(), heading("Qué necesita atención")]
    rows = [["Asunto", "Exposición documentada", "Siguiente paso"]]
    for case in model["cases"]:
        rows.append([TITLES[case["case_id"]], exposure(case),
                     "Corregir y comprobar" if case["disposition"] == "CORRECT" else "Revisar antes de decidir"])
    story += [table(rows, [67*mm, 57*mm, 46*mm]), Spacer(1, 8*mm),
              p("Las unidades son distintas entre asuntos; no deben sumarse como si fueran viajes o personas. Los valores informados excluyen los campos vacíos cuando corresponda."),
              heading("Qué puede significar para la empresa"),
              p("Conviene contrastar los datos con la información que desea publicar la empresa y probarlos en el sistema que los recibirá. Todavía no se ha demostrado una consecuencia operativa ni se conoce la causa de cada incidencia."),
              heading("Qué falta comprobar")]
    if model["format"] == "GTFS_SCHEDULE":
        story += [p("Quedan partes de las condiciones de presencia de campos y del orden temporal sin evaluar. La conformidad legal, la aceptación del destinatario y la correspondencia con el servicio real requieren comprobaciones específicas."),
                  PageBreak()]
    else:
        story += [p("Este ejemplo no representa a una empresa de transporte. No demuestra conformidad con un esquema o perfil NeTEx ni capacidad sobre una publicación completa.")]
    story += [heading("Plan de decisión y corrección"),
        table([["Paso", "Responsabilidad propuesta", "Evidencia para avanzar"],
               ["1. Acordar el uso y la fecha", "Dirección y destinatario", "Destino, condiciones de aceptación y fecha acordada."],
               ["2. Revisar y corregir", "Equipo productor", "Nueva versión del fichero y respuesta por asunto."],
               ["3. Volver a comprobar", "Responsable de auditoría", "Nueva ejecución, comparación y pruebas de cierre."],
               ["4. Aceptar la entrega", "Dirección y destinatario", "Decisión sobre resultados y límites restantes."]], [46*mm, 54*mm, 70*mm]),
        Spacer(1, 7*mm), p("Estas responsabilidades son propuestas. No hay personas asignadas ni fechas comprometidas."),
        p("Una corrección comunicada por el productor sigue pendiente de verificación hasta que exista una nueva ejecución enlazada. Actualmente no hay respuesta del productor ni nueva auditoría de cierre."),
        heading("Cómo consultar el detalle"), p("Abra INDEX.html en la carpeta principal. Desde allí puede acceder al informe técnico, al modelo común y a los anexos de evidencia."),
        p("Referencia: " + model["identity"]["reference_id"], "TDLSmall")]
    return story


def technical(model, package):
    story = cover(model, "el equipo técnico") + [heading("Identidad y alcance"),
        p("Fuente: " + model["engagement"]["source"]["identity"], "TDLSmall"),
        p("SHA-256 de fuente: " + model["identity"]["source_sha256"], "TDLSmall"),
        p("Referencia técnica: " + model["engagement"]["reference"]["specification"] + " / " + model["engagement"]["reference"]["version"], "TDLSmall"),
        p("El informe proyecta evidencia existente. El expediente normativo es contexto; no equivale a cumplimiento legal. GTFS-RT y otros formatos están fuera del alcance.", "TDLSmall"), PageBreak()]
    controls = model["controls"]
    for offset in range(0, len(controls), 16):
        story += [heading("Matriz de controles" + (f" ({offset+1}-{min(offset+16,len(controls))})" if len(controls)>16 else ""))]
        rows = [["Control", "Resultado", "Grupos enlazados"]]
        for control in controls[offset:offset+16]:
            rows.append([control["rule_id"], STATUS[control["status"]], ", ".join(control.get("case_ids", [])) or "Sin grupo"])
        story += [table(rows, [76*mm, 44*mm, 50*mm]),
                  p("Cada fila cuenta un control único. Las capas, versiones y correspondencias completas están en el modelo común y el índice de evidencia.", "TDLSmall"), PageBreak()]
    story += [heading("Cobertura y partes no evaluables")]
    if model["format"] == "GTFS_SCHEDULE":
        story += [p("Presencia condicional de campos: 15.395 anotaciones de evaluación parcial; no son 15.395 defectos nuevos del operador. Se desglosan en 15.381 condiciones desconocidas, 12 condiciones sin resolver y 2 decisiones sobre extensiones pendientes."),
            p("El origen contiene 95 decisiones y 14.713 comprobaciones condicionales resueltas. El muestreo está truncado; esta entrega no acredita que todas las condiciones estén evaluadas."),
            p("Orden temporal de viajes: un elemento de revisión pendiente, no un viaje afectado demostrado. No existe aquí una comprobación implementada y completa del orden entre paradas."),
            p("Alternativas propuestas: resolver condiciones y política de extensiones en una versión nueva; diseñar comprobaciones temporales con horas extendidas, cambio de día y semántica de frecuencias. Contrastar con una referencia independiente del servicio. Estas alternativas no se han ejecutado."),
            heading("Conciliación de evidencias"),
            p("3.553 registros de origen = 3.541 eventos conciliados + 12 referencias duplicadas. Brecha de contabilización: cero. Los 12 enlaces de trazado aparecen en dos capas; no son 24 viajes diferentes."),
            p("Detalle: 02_MODELO/COVERAGE_EXPLANATION.json; 02_MODELO/CONTROL_CROSSWALK.json; 02_MODELO/PRESENTATION_MODEL.json.", "TDLSmall")]
    else:
        story += [p("XML mal formado: no se pudo efectuar una validación XSD concluyente. La referencia histórica contiene un fallo técnico XML y un estado XSD no evaluable."),
                  p("Solo se incluyen NETEX-XML-001 y NETEX-XSD-001. Perfil, identidad, referencias, calendarios y calidad del servicio no están cubiertos por este ejemplo. No existe una nueva ejecución en esta entrega."),
                  p("Alternativa propuesta: corregir el XML, identificar la nueva fuente y comprobar por separado XML, versión de esquema y perfil. No ejecutada."),
                  p("Evidencia: 02_EVIDENCIAS/NETEX_HISTORICAL_E2E.json; registro de reglas: 02_EVIDENCIAS/NETEX_RULE_REGISTRY.json.", "TDLSmall")]
    story += [PageBreak()]
    for index, case in enumerate(model["cases"]):
        story += [heading(TITLES[case["case_id"]]), p(case["case_id"] + " | " + ", ".join(case["rule_ids"]), "TDLSmall"),
            heading("Hecho y criterio"), p(case["condition"]), p(case["criterion"]["text"]),
            p("Estado: incidencia documentada. Tratamiento: " + ("corregir" if case["disposition"] == "CORRECT" else "revisar antes de decidir") + ".", "TDLSmall"),
            heading("Exposición y evidencia"), p(exposure(case) + ". Población: " + case["exposure"]["field"] + "."),
            p("Las cifras no son severidad ni impacto en viajeros. Fuente vinculada por SHA-256. Localizadores completos en la referencia siguiente.", "TDLSmall")]
        for evidence in case["evidence"]:
            story += [p(evidence["source_ref"], "TDLSmall")]
        story += [heading("Causa e impacto"), p("Causa desconocida. Impacto real no verificado."),
                  p(case["observed_impact"]["text"], "TDLSmall"),
                  p("Impacto potencial, sin confirmación: " + case["potential_impact"]["text"], "TDLSmall"),
                  heading("Acción y prueba de cierre"), p(case["action"]), p(case["closure"], "TDLSmall")]
        for limit in case["criterion"].get("source_metadata_limitations", []):
            story += [p("Límite del criterio: " + limit, "TDLSmall")]
        story += [p("Prioridad no determinada; bloqueo para destino desconocido. Sin respuesta del productor y sin reauditoría de cierre.", "TDLSmall"), PageBreak()]
    story += [heading("Seguimiento y reproducción de la entrega"),
        p("La respuesta del productor no cierra un caso. Para resolverlo: nueva fuente identificada, nueva ejecución comparable, prueba de cierre enlazada y revisión de las limitaciones restantes."),
        p("INDEX.html conduce a ambos informes y a los anexos. REPORT_MODEL.json es el modelo común; VIEW_CONSISTENCY.json identifica las dos proyecciones; REFERENCE_INDEX.json enlaza la evidencia local."),
        p("DELIVERY_MANIFEST.json enumera los archivos y sus huellas; DELIVERY_SEAL.json identifica el manifiesto. Las huellas detectan alteraciones frente a este manifiesto; no son una firma autenticada del auditor."),
        p("Los metadatos históricos conservan sus rutas de origen como procedencia. Las referencias activas de esta entrega son relativas a su carpeta."),
        p("El proyecto cartográfico requiere un visor compatible. Las fuentes legales externas son contexto y se incluyen sus capturas existentes. No se ha vuelto a comprobar su vigencia en esta entrega." if model["format"] == "GTFS_SCHEDULE" else
          "El registro incluido distingue XML, esquema y perfil. Esta referencia no acredita aceptación de un destinatario ni conformidad de perfil."),
        p("Modelo semántico SHA-256: " + model["semantic_sha256"], "TDLSmall"),
        p("Referencia: " + model["identity"]["reference_id"], "TDLSmall")]
    return story


def build_reports(model, package):
    views = []
    for audience, path, factory in [("DIRECCION", "01_DIRECCION/Informe_direccion.pdf", management),
                                    ("TECNICO", "02_TECNICO/Informe_tecnico.pdf", lambda m: technical(m, package))]:
        output = Path(package) / path; output.parent.mkdir(parents=True, exist_ok=True)
        def decoration(canvas, document):
            canvas.saveState(); canvas.setFillColor(NAVY); canvas.setFont("Helvetica", 8)
            canvas.drawString(20*mm, 284*mm, "TRANSIT DATA LAB | " + audience)
            canvas.setStrokeColor(TEAL); canvas.line(20*mm, 279*mm, 190*mm, 279*mm)
            canvas.drawString(20*mm, 13*mm, "Entrega privada | Revisión humana pendiente")
            canvas.drawRightString(190*mm, 13*mm, str(document.page))
            canvas.restoreState()
        doc = SimpleDocTemplate(str(output), pagesize=(210*mm, 297*mm), leftMargin=20*mm, rightMargin=20*mm,
            topMargin=25*mm, bottomMargin=23*mm, title="Transit Data Lab - " + audience + " - " + model["label"],
            author="Transit Data Lab", subject="TDL semantic SHA-256 " + model["semantic_sha256"])
        doc.build(factory(model), onFirstPage=decoration, onLaterPages=decoration)
        views.append({"audience": audience, "path": path, "semantic_sha256": model["semantic_sha256"],
                      "case_ids": [c["case_id"] for c in model["cases"]],
                      "unique_control_counts": model["conclusion"]["unique_control_counts"]})
    return views
