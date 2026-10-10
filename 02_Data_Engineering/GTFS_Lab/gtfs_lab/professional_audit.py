"""Additive professional delivery from existing evidence and explicit reviewed decisions.

No engine execution or automatic human judgements. Historical deliveries stay immutable.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from .interpretation.cases import sha256_json, validate_cases

LAB = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
GENERATOR_VERSION = "1.1.0"
INTEGRITY_FILES = {"02_EVIDENCIAS/PACKAGE_MANIFEST.json", "02_EVIDENCIAS/PACKAGE_SEAL.json"}
TECHNICAL = {
    "PASS": "No se han detectado incumplimientos en las comprobaciones ejecutadas",
    "FAIL_TECHNICAL": "Se han detectado valores que necesitan corrección",
    "INSPECTION_ERROR": "Una parte de la inspección no pudo completarse",
    "INCOMPLETE": "La evaluación está incompleta", "NOT_EVALUABLE": "No ha sido posible evaluar el resultado técnico",
}
LABELS = {
    "CORRECT": "Corregir", "REVIEW": "Revisar con el productor", "IMPROVE": "Mejorar",
    "INFORMATIONAL": "Información", "ACCEPT_WITH_RATIONALE": "Justificación registrada",
    "PENDING_INFORMATION": "Falta información", "NOT_EVALUABLE": "No evaluable",
    "UNASSESSED": "Urgencia no determinada", "LOW": "Baja", "MEDIUM": "Media", "HIGH": "Alta", "URGENT": "Urgente",
    "NO_RESPONSE": "Sin respuesta del productor", "REPORTED_PENDING": "Actuación comunicada como pendiente",
    "REPORTED_CORRECTED": "Corrección comunicada, pendiente de verificación", "REPORTED_ACCEPTED": "Aceptación comunicada, sin borrar el resultado técnico",
    "NOT_APPLICABLE": "No aplicable", "NOT_REAUDITED": "Corrección pendiente de verificación",
    "RESOLVED": "Cierre verificado", "PERSISTENT": "Condición persistente", "REAPPEARED": "Condición reaparecida",
    "NEW": "Caso nuevo", "NOT_EVALUATED": "Sin reevaluación", "NOT_COMPARABLE": "Comparación no acreditada",
}
ENTITY = {"route": "líneas afectadas", "stop": "paradas afectadas", "trip": "viajes afectados", "frequency": "intervalos afectados", "shape": "trazados afectados"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def contained(root: Path, relative: str):
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError("artifact reference escapes delivery")
    return result


def verify_delivery(delivery: Path):
    from .delivery_integrity import verify_delivery as verify
    return verify(delivery)


def execution_view(delivery, manifest):
    """Project actual engine evidence rather than inventing a manifest status."""
    projected = copy.deepcopy(manifest)
    engine = read(delivery / "engine_run" / "engine_report.json")
    stages = engine["technical_evaluation"]["stages"]
    states = {s["status"] for s in stages}
    projected["technical_status"] = next((s for s in ("INSPECTION_ERROR", "FAIL_TECHNICAL", "NOT_EVALUABLE", "INCOMPLETE") if s in states), "PASS" if states else "NOT_EVALUABLE")
    projected["rule_matrix"] = [{"stage": stage["stage"], **rule} for stage in stages for rule in stage["rules"]]
    projected["compliance_status"] = read(delivery / "compliance.json")["result"]
    return projected


def client_projection(case):
    client = {k: copy.deepcopy(case[k]) for k in ("case_id", "title", "observation", "criterion", "action", "closure_criteria", "impact_known", "impact_potential", "limitations", "evidence")}
    client.update({"entities_text": ", ".join(f"{v} {ENTITY.get(k, k)}" for k, v in case["unique_entities"].items()) or "Entidades no cuantificadas",
                   "disposition_text": LABELS[case["disposition"]], "priority_text": LABELS[case["priority"]],
                   "producer_text": LABELS[case["producer_status"]], "reaudit_text": LABELS[case["reaudit"]["status"]]})
    return client


def build_model(manifest, interpretation, manifest_sha, revision, decisions=None, *, include_source_scope=False):
    """Decisions are a versioned input; uncovered records retain full provenance."""
    if not revision.strip():
        raise ValueError("presentation revision is required")
    if decisions is not None:
        from jsonschema import Draft202012Validator
        Draft202012Validator(read(LAB / "spec" / "reviewed_decisions_v1.schema.json")).validate(decisions)
        model = copy.deepcopy(decisions["case_contract"])
        validate_cases(model, interpretation, require_full=True)
        if model["execution_identity"]["client_audit_id"] != manifest["audit_id"] or model["execution_identity"]["manifest_sha256"] != manifest_sha:
            raise ValueError("decisions are bound to a different client execution/manifest")
        if set(decisions["closure_profiles"]) != {c["case_id"] for c in model["cases"]}:
            raise ValueError("each reviewed case requires its own closure profile")
        for case in model["cases"]:
            if case["reaudit"]["status"] == "RESOLVED":
                verification = decisions.get("closure_verifications", {}).get(case["case_id"], {})
                current_ids = {model["execution_identity"]["client_audit_id"], model["execution_identity"]["audit_execution_id"]}
                matches = any(link["relation"] == "RESOLVED" and link["execution_id"] == verification.get("execution_id")
                              and link["evidence_ref"] == verification.get("auditor_evidence_ref") for link in case["reaudit"]["links"])
                if not matches or not closure_verified(decisions["closure_profiles"][case["case_id"]], verification, current_ids):
                    raise ValueError("RESOLVED requires matching case-specific verified closure evidence from another execution")
    else:
        records = interpretation["source_findings"]
        model = {"contract": "TDL_AUDIT_CASES_V1", "version": "1.0.0",
                 "dataset_identity": copy.deepcopy(interpretation["dataset_identity"]),
                 "execution_identity": {"audit_execution_id": interpretation["execution_identity"]["audit_execution_id"],
                    "client_audit_id": manifest["audit_id"], "manifest_sha256": manifest_sha,
                    "engine_version": interpretation["execution_identity"]["engine_version"]},
                 "source_interpretation": {"contract_version": "1.0.0", "sha256": sha256_json(interpretation)},
                 "coverage": {"source_record_count": len(records), "classified_record_count": 0, "reconciled_event_count": 0,
                    "duplicate_source_reference_count": 0, "unclassified_record_count": len(records), "accounting_gap": 0,
                    "source_origins": dict(Counter(r.get("origin", r.get("stage", "UNKNOWN")) for r in records))},
                 "unclassified_source_record_ids": [r["raw_finding_id"] for r in records],
                 "technical_result": manifest.get("technical_status", "NOT_EVALUABLE"),
                 "use_readiness": {"status": "NOT_DETERMINED", "declared_use": None, "basis": "Falta definir el uso previsto y revisar su cobertura."},
                 "cases": [], "limitations": ["No se han aportado decisiones revisadas para esta fuente."]}
        # V1 dataset identity can contain more metadata; only contract fields are projected.
        model["dataset_identity"] = {k: interpretation["dataset_identity"][k] for k in ("dataset_id", "sha256")}
        validate_cases(model, interpretation, require_full=True)
    if model["dataset_identity"]["sha256"] != manifest["dataset_identity"]["source_sha256"]:
        raise ValueError("source identity mismatch")
    if model["technical_result"] != manifest.get("technical_status", "NOT_EVALUABLE"):
        raise ValueError("decisions cannot change engine technical status")
    clients = [client_projection(case) for case in model["cases"]]
    pending_ids = set(model["unclassified_source_record_ids"])
    pending = [copy.deepcopy(r) for r in interpretation["source_findings"] if r["raw_finding_id"] in pending_ids]
    steps = copy.deepcopy(decisions.get("steps", [])) if decisions else []
    if not steps:
        steps = [{"order": 1, "case_ids": [], "action": "Definir el uso previsto y revisar los resultados disponibles.",
                  "basis": "La ausencia de decisiones impide recomendar un tratamiento específico.",
                  "missing": "El responsable de los datos debe aportar destino, requisitos y contexto del servicio."}]
    case_ids = {c["case_id"] for c in model["cases"]}
    if any(set(s["case_ids"]) - case_ids for s in steps):
        raise ValueError("work sequence refers to unknown case")
    if case_ids - {cid for s in steps for cid in s["case_ids"]}:
        raise ValueError("work sequence omits reviewed cases")
    use = model["use_readiness"]
    if use["status"] in {"APTO", "APTO_CON_OBSERVACIONES"} and (not use["declared_use"] or pending or model["coverage"]["accounting_gap"]):
        raise ValueError("favorable use conclusion requires a declared destination and complete reviewed record coverage")
    use_text = "Aptitud para el destino: no evaluada; falta definir el uso previsto" if not use["declared_use"] else {
        "APTO": "Sin impedimentos identificados para el uso evaluado", "APTO_CON_OBSERVACIONES": "Sin impedimentos identificados, con observaciones",
        "REQUIERE_CORRECCION": "Requiere corrección para el uso evaluado", "NO_ES_POSIBLE_EMITIR_CONCLUSION": "No es posible concluir sobre el uso evaluado",
        "NOT_DETERMINED": "Aptitud para el uso previsto no determinada"}[use["status"]]
    basis = use["basis"]
    if include_source_scope and str(manifest.get("dataset_identity", {}).get("source_provenance", "")).upper().startswith("SYNTHETIC"):
        basis = "DEMO. Demostración con datos sintéticos; no representa un servicio real. " + basis
    result = {"contract": "TDL_PROFESSIONAL_PRESENTATION", "version": VERSION,
              "identity": {"client_audit_id": model["execution_identity"]["client_audit_id"],
                  "audit_execution_id": model["execution_identity"]["audit_execution_id"], "source_sha256": model["dataset_identity"]["sha256"], "revision": revision},
              "case_contract": model, "cases": model["cases"], "client_cases": clients,
              "coverage": model["coverage"], "pending_records": pending,
              "presentation": {"technical_text": TECHNICAL[model["technical_result"]], "use_text": use_text,
                 "basis": basis, "steps": steps, "limitations": model["limitations"]},
              "decision_provenance": {**copy.deepcopy(decisions.get("provenance", {})), "closure_profiles": copy.deepcopy(decisions.get("closure_profiles", {}))} if decisions else {},
              "matrix": manifest.get("rule_matrix", []), "compliance": manifest.get("compliance_status", "NOT_EVALUABLE")}
    validate_presentation(result, interpretation)
    return result


def validate_presentation(model, interpretation):
    from jsonschema import Draft202012Validator
    schema = read(LAB / "spec" / "professional_presentation_v1.schema.json")
    Draft202012Validator(schema).validate(model)
    validate_cases(model["case_contract"], interpretation, require_full=True)
    if model["cases"] != model["case_contract"]["cases"] or model["coverage"] != model["case_contract"]["coverage"]:
        raise ValueError("presentation projections diverge from decision contract")
    if [c["case_id"] for c in model["client_cases"]] != [c["case_id"] for c in model["cases"]]:
        raise ValueError("client case projections mismatch")
    contract = model["case_contract"]
    identity = model["identity"]
    if (identity["client_audit_id"] != contract["execution_identity"]["client_audit_id"]
            or identity["audit_execution_id"] != contract["execution_identity"]["audit_execution_id"]
            or identity["source_sha256"] != contract["dataset_identity"]["sha256"]):
        raise ValueError("presentation identity differs from authoritative contract")
    if model["client_cases"] != [client_projection(case) for case in model["cases"]]:
        raise ValueError("client presentation alters reviewed case content")
    pending_ids = set(contract["unclassified_source_record_ids"])
    if model["pending_records"] != [r for r in interpretation["source_findings"] if r["raw_finding_id"] in pending_ids]:
        raise ValueError("pending source records differ from complete authoritative coverage")
    if model["presentation"]["technical_text"] != TECHNICAL[contract["technical_result"]]:
        raise ValueError("technical presentation differs from source outcome")


def closure_verified(case, evidence, current_execution):
    """A linked run or producer statement alone never closes a reviewed case.

    The caller supplies auditor checks and correspondence, not an inferred closure.
    This predicate does not mutate RAW, decisions or the producer status.
    """
    required = case.get("closure_checks", [])
    current_ids = {current_execution} if isinstance(current_execution, str) else set(current_execution)
    return bool(required and evidence.get("execution_id") and evidence.get("execution_id") not in current_ids
                and re.fullmatch(r"[a-fA-F0-9]{64}", str(evidence.get("source_sha256", ""))) and evidence.get("correspondence_ref")
                and evidence.get("auditor_evidence_ref") and evidence.get("criteria_version") == case.get("criteria_version")
                and all(evidence.get("checks", {}).get(name) is True for name in required))


def technical_condition(kind, values):
    """Bounded checks used in closure evidence, without claiming service preservation."""
    if kind == "color":
        return all(v == "" or re.fullmatch(r"[0-9a-fA-F]{6}", v) is not None for v in values)
    if kind == "reference":
        allowed, targets, references = values
        return all((v == "" and allowed) or v in targets for v in references)
    if kind == "frequency":
        start, end, headway = values
        if headway <= 0 or end <= start:
            return False
        last = start + ((end - start - 1) // headway) * headway
        return last < end < last + headway
    if kind == "distance":
        return all(math.isfinite(v) and v >= 0 for v in values) and all(b > a for a, b in zip(values, values[1:]))
    raise ValueError("unsupported closure check")


def build_map(model, source_zip: Path, output: Path):
    """Source coordinates only. Unsupported locators stay explicitly unlocated."""
    from xml.sax.saxutils import escape
    tables = {}
    with zipfile.ZipFile(source_zip) as archive:
        for name in ("stops.txt", "shapes.txt"):
            if name in archive.namelist():
                with archive.open(name) as stream:
                    tables[name] = list(csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig", newline="")))
    points = []; folders = []; located = Counter(); bad_coordinates = 0
    def coord(row, lat_key, lon_key):
        nonlocal bad_coordinates
        try:
            lon, lat = float(row[lon_key]), float(row[lat_key])
            if not (math.isfinite(lon) and math.isfinite(lat) and -180 <= lon <= 180 and -90 <= lat <= 90):
                raise ValueError("coordinate bounds")
        except (KeyError, TypeError, ValueError):
            bad_coordinates += 1
            return None
        points.append((lon, lat)); return lon, lat
    def mark(name, description, geometry):
        return f"<Placemark><name>{escape(name)}</name><description>{escape(description)}</description>{geometry}</Placemark>"
    context = []
    for row in tables.get("stops.txt", []):
        p = coord(row, "stop_lat", "stop_lon")
        if p:
            context.append(mark(row.get("stop_name") or row["stop_id"], "Parada de contexto; sin conclusión de corrección. stop_id=" + row["stop_id"], f"<Point><coordinates>{p[0]},{p[1]},0</coordinates></Point>"))
    folders.append("<Folder><name>Paradas de contexto</name>" + "".join(context) + "</Folder>")
    shapes = {}
    for row in tables.get("shapes.txt", []):
        p = coord(row, "shape_pt_lat", "shape_pt_lon")
        if p:
            try: seq = int(row["shape_pt_sequence"])
            except (KeyError, ValueError): raise ValueError("map shape sequence not interpretable")
            shapes.setdefault(row["shape_id"], []).append((seq, p))
    context = []
    for sid, coords in sorted(shapes.items()):
        ordered = sorted(coords)
        if len({seq for seq, _ in ordered}) != len(ordered):
            raise ValueError("map shape sequence ambiguous")
        if len(ordered) < 2: continue
        line = " ".join(f"{p[0]},{p[1]},0" for _, p in ordered)
        context.append(mark("Trazado " + sid, "Trazado de contexto de la fuente, sin validación externa. shape_id=" + sid,
            '<Style><LineStyle><color>ff996633</color><width>2</width></LineStyle></Style><LineString><coordinates>' + line + '</coordinates></LineString>'))
    folders.append("<Folder><name>Red de contexto</name>" + "".join(context) + "</Folder>")
    for case, client in zip(model["cases"], model["client_cases"]):
        marks = []
        for occurrence in case["occurrences"]:
            file = occurrence["source_file"]
            match = re.search(r"data_row:(\d+)$", occurrence["normalized_locator"])
            if file not in tables or not match: continue
            idx = int(match[1]) - 1
            if not 0 <= idx < len(tables[file]): raise ValueError("map locator out of source bounds")
            row = tables[file][idx]
            p = coord(row, "stop_lat" if file == "stops.txt" else "shape_pt_lat", "stop_lon" if file == "stops.txt" else "shape_pt_lon")
            if not p: continue
            name = (row.get("stop_name") or row.get("shape_id") or "Elemento") + " | " + case["case_id"]
            desc = "\n".join([client["title"], client["observation"], "Acción: " + client["action"], "Cierre: " + client["closure_criteria"],
                              "Ver ficha " + case["case_id"] + " en Informe_auditoria.pdf y hoja Casos del libro.",
                              "Detalle técnico: " + occurrence["native_locator"] + "; " + occurrence["source_record_id"]])
            marks.append(mark(name, desc, f"<Style><IconStyle><color>ff0077dd</color><scale>0.8</scale></IconStyle></Style><Point><coordinates>{p[0]},{p[1]},0</coordinates></Point>"))
            located[case["case_id"]] += 1
        folders.append(f"<Folder><name>{escape(client['title'])}</name><description>{escape(client['action'])}</description>{''.join(marks)}</Folder>")
    identity = model["identity"]
    description = "; ".join(f"{k}={v}" for k, v in identity.items())
    description += ". Las líneas y paradas de contexto no indican ausencia de defectos. Los puntos de casos localizan registros de fuente; no acreditan impacto operativo. Casos sin localización: " + ", ".join(c["case_id"] for c in model["cases"] if not located[c["case_id"]])
    if model["pending_records"]: description += ". Hay registros pendientes de decisión; consulte Ocurrencias."
    view = ""
    if points:
        xmin, xmax = min(x for x, _ in points), max(x for x, _ in points)
        ymin, ymax = min(y for _, y in points), max(y for _, y in points)
        view = f"<LookAt><longitude>{(xmin+xmax)/2}</longitude><latitude>{(ymin+ymax)/2}</latitude><range>{max(3000, max(xmax-xmin,ymax-ymin)*111000*1.25)}</range><tilt>0</tilt></LookAt>"
    kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>' + escape(identity["client_audit_id"] + " | " + identity["revision"]) + '</name><description>' + escape(description) + '</description>' + view + ''.join(folders) + '</Document></kml>'
    ET.fromstring(kml)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive: archive.writestr("doc.kml", kml)
    return {"located_by_case": dict(located), "coordinate_count": len(points), "invalid_coordinates": bad_coordinates,
            "visual_acceptance": "PENDING_LOCAL_VIEWER", "initial_view": "Encoded from extent; viewer behavior not verified"}


def preflight(workbook_command=None):
    import importlib.metadata
    required = {"jsonschema":"4.25.1", "reportlab":"5.0.1", "pypdf":"6.20.0"}
    if not workbook_command: required["XlsxWriter"] = "3.2.9"
    versions = {}
    for name, expected in required.items():
        try: versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError("Missing professional runtime dependency: " + name) from exc
        if versions[name] != expected:
            raise ValueError("Professional runtime version mismatch: " + name)
    if workbook_command and (not Path(workbook_command[-1]).is_file() or not (shutil.which(workbook_command[0]) or Path(workbook_command[0]).is_file())):
        raise ValueError("Workbook executable/script is unavailable")
    return versions


def generate(delivery, output, revision, source_zip, decisions_path=None, workbook_command=None):
    versions = preflight(workbook_command)
    output = Path(output)
    if output.exists(): raise FileExistsError("Presentation output already exists")
    final_output = output
    output = output.with_name(output.name + ".partial")
    manifest = execution_view(delivery, verify_delivery(delivery))
    if digest(source_zip) != manifest["dataset_identity"]["source_sha256"]:
        raise ValueError("map ZIP differs from audited source")
    interpretation = read(delivery / "AUDIT_CONSOLIDATED.json")
    decisions = read(decisions_path) if decisions_path else None
    model = build_model(manifest, interpretation, digest(delivery / "audit_manifest.json"), revision, decisions, include_source_scope=True)
    # No historical delivery or existing presentation may be overwritten.
    output.mkdir(parents=True, exist_ok=False)
    results = output / "01_RESULTADOS"; evidence = output / "02_EVIDENCIAS"
    results.mkdir(); evidence.mkdir()
    shutil.copytree(delivery, output / "03_SOURCE_DELIVERY")
    write(evidence / "PRESENTATION_MODEL.json", model)
    write(evidence / "AUDIT_CASES.json", model["case_contract"])
    if decisions: write(evidence / "REVIEWED_DECISIONS.json", decisions)
    import importlib.metadata
    import sys
    write(evidence / "GENERATION_RECEIPT.json", {
        "identity": model["identity"], "generator_version": GENERATOR_VERSION,
        "python_version": sys.version.split()[0],
        "python_dependencies": versions,
        "generator_sources": {name: digest(LAB / name) for name in ("gtfs_lab/professional_audit.py", "gtfs_lab/professional_pdf.py", "gtfs_lab/professional_workbook.py", "gtfs_lab/delivery_integrity.py", "gtfs_lab/delivery_privacy.py", "gtfs_lab/interpretation/cases.py", "spec/audit_case_contract_v1.schema.json", "spec/professional_presentation_v1.schema.json", "spec/reviewed_decisions_v1.schema.json")},
        "workbook_renderer_sha256": digest(Path(workbook_command[-1])) if workbook_command else None,
        "engine_reexecuted": False, "source_zip_sha256_verified": True,
        "decision_source_sha256": digest(decisions_path) if decisions_path else None,
        "source_scope_label_applied": True,
    })
    from .professional_pdf import build_pdfs
    build_pdfs(model, results)
    gis = build_map(model, source_zip, results / "Mapa_auditoria.kmz")
    write(evidence / "GIS_CHECKS.json", gis)
    if workbook_command:
        subprocess.run([*workbook_command, str(evidence / "PRESENTATION_MODEL.json"), str(results / "Plan_de_accion_y_hallazgos.xlsx")], check=True)
    else:
        from .professional_workbook import build_workbook
        write(evidence / "WORKBOOK_CHECKS.json", build_workbook(model, results / "Plan_de_accion_y_hallazgos.xlsx"))
    (evidence / "MAP_MANUAL_PROTOCOL.md").write_text("# Aceptación visual pendiente\n\nAbrir Mapa_auditoria.kmz en visor local compatible, sin subir datos. Registrar nombre y versión. Comprobar extensión inicial y zoom de red; abrir carpetas de contexto y cada caso; seleccionar paradas y vértices; comprobar etiquetas, descripción, acción y cierre contra ficha del PDF/libro; recorrer dos trazados y verificar secuencia; comprobar casos no localizados. Registrar acciones, capturas locales, anomalías y aceptación del responsable. Los controles de coordenadas no validan el zoom del visor.\n", encoding="utf-8")
    from .delivery_privacy import inspect_delivery_content
    privacy = inspect_delivery_content(output)
    write(evidence / "DELIVERY_CONTENT_SCAN.json", privacy)
    if privacy["status"] != "PASS":
        raise ValueError("Professional delivery content inspection is incomplete or found local paths")
    finalize(output, model)
    output.rename(final_output)
    return {"status": "GENERATED_FOR_HUMAN_REVIEW", "directory": str(final_output), "identity": model["identity"], "coverage": model["coverage"], "map_visual_acceptance": gis["visual_acceptance"]}


def finalize(output, model):
    evidence = output / "02_EVIDENCIAS"
    names = [p.relative_to(output).as_posix() for p in sorted(output.rglob("*")) if p.is_file() and p.relative_to(output).as_posix() not in INTEGRITY_FILES | {"02_EVIDENCIAS/EVIDENCE_INDEX.md"}]
    lines = ["# Índice de la revisión", "", json.dumps(model["identity"], ensure_ascii=False), "", "La revisión de presentación no constituye una nueva ejecución del motor. Validación completa JSON Schema y relaciones ejecutada. Aceptación visual GIS y emisión humana pendientes.", "", *[f"- `{name}`" for name in names]]
    (evidence / "EVIDENCE_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    artifacts = {p.relative_to(output).as_posix(): {"sha256": digest(p), "size_bytes": p.stat().st_size} for p in sorted(output.rglob("*")) if p.is_file() and p.relative_to(output).as_posix() not in INTEGRITY_FILES}
    write(evidence / "PACKAGE_MANIFEST.json", {"identity": model["identity"], "generator_version": GENERATOR_VERSION, "validation": "FULL_SCHEMA_AND_RELATIONS", "artifacts": artifacts})
    write(evidence / "PACKAGE_SEAL.json", {"manifest_sha256": digest(evidence / "PACKAGE_MANIFEST.json")})
    verify_package(output)


def verify_package(output):
    evidence = output / "02_EVIDENCIAS"
    manifest = read(evidence / "PACKAGE_MANIFEST.json")
    if read(evidence / "PACKAGE_SEAL.json")["manifest_sha256"] != digest(evidence / "PACKAGE_MANIFEST.json"):
        raise ValueError("package seal mismatch")
    from .delivery_integrity import verify_inventory, inventory
    verify_inventory(output, manifest["artifacts"], INTEGRITY_FILES)
    actual = inventory(output) - INTEGRITY_FILES
    verify_delivery(output / "03_SOURCE_DELIVERY")
    source = output / "03_SOURCE_DELIVERY"
    model = read(evidence / "PRESENTATION_MODEL.json")
    interpretation = read(source / "AUDIT_CONSOLIDATED.json")
    validate_presentation(model, interpretation)
    if manifest["identity"] != model["identity"] or read(evidence / "AUDIT_CASES.json") != model["case_contract"]:
        raise ValueError("sealed package identity/case contract differs from model")
    decisions = read(evidence / "REVIEWED_DECISIONS.json") if (evidence / "REVIEWED_DECISIONS.json").exists() else None
    expected = build_model(execution_view(source, read(source / "audit_manifest.json")), interpretation,
                           digest(source / "audit_manifest.json"), model["identity"]["revision"], decisions,
                           include_source_scope=read(evidence / "GENERATION_RECEIPT.json").get("source_scope_label_applied", False))
    if model != expected:
        raise ValueError("sealed presentation differs from authoritative source and decisions")
    return len(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delivery", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--source-zip", type=Path, required=True)
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--node", help="Optional legacy Node renderer executable")
    parser.add_argument("--workbook-script", type=Path, help="Optional legacy Node renderer script")
    args = parser.parse_args()
    if bool(args.node) != bool(args.workbook_script): parser.error("--node and --workbook-script must be provided together")
    command = [args.node, str(args.workbook_script)] if args.node else None
    result = generate(args.delivery, args.output, args.revision, args.source_zip, args.decisions, command)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
