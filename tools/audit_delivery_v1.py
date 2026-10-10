"""Dual-audience reports and portable private delivery for GTFS/NeTEx (07/08).

Builds views of existing evidence. Auditors, frozen inputs and source packages
are never modified. The common model and PDFs have the same semantic digest.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
from urllib.parse import unquote, urlsplit
import zipfile

from tools.audit_assessment_v1 import conclusion, validate_finding
from tools.audit_foundation_v1 import engagement_gate

ROOT = Path(__file__).resolve().parents[1]
INTEGRITY_NAMES = {"DELIVERY_MANIFEST.json", "DELIVERY_SEAL.json"}
STATUS_ES = {"PASS": "Sin incidencias en el control", "FAIL_TECHNICAL": "Incidencias técnicas",
             "NOT_EVALUABLE": "No evaluable", "NOT_APPLICABLE": "No aplicable",
             "INSPECTION_ERROR": "Error de inspección", "HUMAN_REVIEW_REQUIRED": "Revisión humana"}
UNIT_ES = {"SUPPLIED_FIELD_VALUE": "valores informados", "EXACT_TIMES_1_INTERVAL": "intervalos",
           "SHAPE_TRANSITION": "transiciones del trazado", "XML_FILE": "ficheros"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()


def semantic_digest(model):
    value = {k: v for k, v in model.items() if k != "semantic_sha256"}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def contained(root, name):
    rel = PurePosixPath(name)
    if not name or "\\" in name or ":" in name or rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Unsafe delivery path: " + name)
    path = Path(root) / rel
    if not path.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError("Delivery reference escapes package")
    return path


def files(root):
    """Bounded named root walk; reject reparse points before descending."""
    root = Path(root)
    if root.is_symlink() or getattr(root.stat(), 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400):
        raise ValueError("Reparse source root")
    stack = [root]
    while stack:
        current = stack.pop()
        with os.scandir(current) as entries:
            for entry in entries:
                info = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400):
                    raise ValueError("Reparse point in delivery tree")
                path = Path(entry.path)
                if entry.is_dir(follow_symlinks=False): stack.append(path)
                elif entry.is_file(follow_symlinks=False): yield path


def copy_file(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise ValueError("Output collision: " + str(destination))
    shutil.copy2(source, destination)


def copy_tree(source, destination):
    for path in files(source): copy_file(path, destination / path.relative_to(source))


def verify_original(root, manifest_name, seal_name):
    manifest = contained(root, manifest_name); seal = read(contained(root, seal_name))
    if digest(manifest) != seal["manifest_sha256"]: raise ValueError("Original seal mismatch")
    artifacts = read(manifest)["artifacts"]
    actual = {p.relative_to(root).as_posix() for p in files(root)} - {manifest_name, seal_name}
    if actual != set(artifacts): raise ValueError("Original inventory mismatch")
    for name, expected in artifacts.items():
        path = contained(root, name)
        if digest(path) != expected["sha256"] or path.stat().st_size != expected["size_bytes"]:
            raise ValueError("Original artifact mismatch: " + name)
    return {"files": len(artifacts), "manifest_sha256": digest(manifest)}


def archive_original(root, destination):
    """Byte-preserving named entries, including original manifests and seals."""
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files(root)): archive.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(destination) as archive:
        for name in archive.namelist():
            if hashlib.sha256(archive.read(name)).hexdigest() != digest(contained(root, name)):
                raise ValueError("Archive preservation mismatch")


def validate_model(model):
    if model["contract"] != "TDL_DUAL_AUDIENCE_MODEL/1" or model["format"] not in {"GTFS_SCHEDULE", "NETEX"}:
        raise ValueError("Unsupported report model")
    if model["semantic_sha256"] != semantic_digest(model): raise ValueError("Semantic model changed")
    engagement = model["engagement"]
    if (engagement["format"] != model["format"] or not engagement["source"].get("identity")
            or not engagement["reference"].get("specification") or not engagement["reference"].get("version")
            or "TECHNICAL_RESULTS" not in model["engagement_gate"]["eligible_categories"]):
        raise ValueError("Technical scope is not bound")
    if model["identity"]["source_sha256"] != model["engagement"]["source"]["sha256"]:
        raise ValueError("Engagement source differs from report identity")
    controls = model["controls"]; ids = {c["rule_id"] for c in controls}
    if len(ids) != len(controls) or ids != set(model["engagement"]["included_controls"]):
        raise ValueError("Report controls differ from the defined scope")
    if dict(Counter(c["status"] for c in controls)) != model["conclusion"]["unique_control_counts"]:
        raise ValueError("Report status counts differ")
    case_ids = {c["case_id"] for c in model["cases"]}
    if len(case_ids) != len(model["cases"]): raise ValueError("Duplicate report case")
    for case in model["cases"]:
        validate_finding(case)
        if case["format"] != model["format"] or not set(case["rule_ids"]) <= ids:
            raise ValueError("Case points outside report scope")
    for control in controls:
        if not set(control.get("case_ids", [])) <= case_ids: raise ValueError("Control has an orphan case")
        expected = {c["case_id"] for c in model["cases"] if control["rule_id"] in c["rule_ids"]}
        if set(control.get("case_ids", [])) != expected: raise ValueError("Inconsistent case/control relationship")
    if model["release_state"] != "PRIVATE_REVIEW_REQUIRED": raise ValueError("Unsupported release claim")


def model_gtfs(r3, assessment, foundation, source):
    raw = read(r3 / "02_EVIDENCIAS/PRESENTATION_MODEL.json")
    receipt = read(assessment / "GENERATION_RECEIPT.json")
    if receipt["inputs"]["model"]["sha256"] != digest(r3 / "02_EVIDENCIAS/PRESENTATION_MODEL.json"):
        raise ValueError("Assessment refers to another model")
    for name, expected in receipt["outputs"].items():
        if digest(contained(assessment, name)) != expected: raise ValueError("Assessment output changed")
    if digest(source) != raw["identity"]["source_sha256"]: raise ValueError("GTFS source identity differs")
    crosswalk = read(foundation / "CONTROL_CROSSWALK.json")
    if receipt["inputs"]["crosswalk"]["sha256"] != digest(foundation / "CONTROL_CROSSWALK.json"):
        raise ValueError("Assessment and crosswalk differ")
    cases = read(assessment / "ASSESSED_FINDINGS.json")
    for case in cases:
        original = next(c for c in raw["cases"] if c["case_id"] == case["case_id"])
        case["title"] = original["title"]
        case["rule_ids"] = sorted({o["rule_id"] for o in original["occurrences"]})
        for evidence in case["evidence"]:
            evidence["historical_source_ref"] = evidence["source_ref"]
            evidence["source_ref"] = "02_MODELO/" + evidence["source_ref"]
    return finish_model({"contract": "TDL_DUAL_AUDIENCE_MODEL/1", "format": "GTFS_SCHEDULE", "label": "Palma - información del servicio",
        "identity": {**raw["identity"], "reference_id": raw["identity"]["client_audit_id"]},
        "engagement": read(ROOT / "reports/audit_foundation_v1/engagement_gtfs_palma.json"),
        "cases": cases, "controls": crosswalk["controls"], "coverage": read(assessment / "COVERAGE_EXPLANATION.json"),
        "conclusion": read(assessment / "TECHNICAL_CONCLUSION.json"), "reconciliation": raw["coverage"],
        "scope_note": "Vista de la ejecución existente, limitada al fichero identificado y a los criterios implantados.",
        "release_state": "PRIVATE_REVIEW_REQUIRED", "source_kind": "EXISTING_GTFS_AUDIT",
        "references": {"original_model": "02_MODELO/PRESENTATION_MODEL.json", "assessed_cases": "02_MODELO/ASSESSED_FINDINGS.json",
            "coverage": "02_MODELO/COVERAGE_EXPLANATION.json", "crosswalk": "02_MODELO/CONTROL_CROSSWALK.json",
            "source_input": "03_SOURCE_DELIVERY/source/00001.zip", "regulatory": "02_EVIDENCIAS/REGULATORY_REVIEW.json"}})


def model_netex():
    case = read(ROOT / "reports/audit_assessment_v1/NETEX_REFERENCE_FINDING.json")
    evidence_path = ROOT / case["evidence"][0]["source_ref"]
    fixture = ROOT / case["evidence"][0]["fixture"]
    if digest(fixture) != case["exposure"]["source_sha256"] or digest(evidence_path) != case["evidence"][0]["source_sha256"]:
        raise ValueError("NeTEx historical reference changed")
    record = next(r for r in read(evidence_path)["cases"] if r["source_file"] == fixture.name)
    if record["well_formedness"] != "NOT_WELL_FORMED" or record["xsd_validation"] != "XSD_NOT_EVALUABLE":
        raise ValueError("Review changed NeTEx reference result")
    engagement = deepcopy(read(ROOT / "reports/audit_foundation_v1/engagement_netex_synthetic.json"))
    engagement["engagement_id"] = "TDL-ENG-NETEX-MALFORMED-REFERENCE-20261008"
    engagement["source"] = {"identity": "malformed.xml", "sha256": digest(fixture), "producer_revision": None}
    engagement["included_controls"] = ["NETEX-XML-001", "NETEX-XSD-001"]
    case["title"] = "Fichero que no puede interpretarse correctamente"; case["rule_ids"] = ["NETEX-XML-001"]
    case["disposition"] = "CORRECT"
    case["exposure"]["field"] = "documento XML"
    case["evidence"][0]["source_ref"] = "02_EVIDENCIAS/NETEX_HISTORICAL_E2E.json"
    case["evidence"][0]["fixture"] = "03_SOURCE_DELIVERY/malformed.xml"
    case["criterion"]["reference"] = "02_EVIDENCIAS/NETEX_RULE_REGISTRY.json:NETEX-XML-001"
    controls = [{"rule_id": "NETEX-XML-001", "status": "FAIL_TECHNICAL", "layer": "NETEX_XML", "case_ids": [case["case_id"]]},
                {"rule_id": "NETEX-XSD-001", "status": "NOT_EVALUABLE", "layer": "NETEX_XSD", "case_ids": []}]
    context = {"consequence_kind": "NOT_VERIFIED"}
    return finish_model({"contract": "TDL_DUAL_AUDIENCE_MODEL/1", "format": "NETEX", "label": "NeTEx - referencia sintética",
        "identity": {"reference_id": "NETEX-SYNTHETIC-20261002:malformed.xml", "source_sha256": digest(fixture), "audit_execution_id": None},
        "engagement": engagement, "cases": [case], "controls": controls,
        "coverage": {"non_evaluable_controls": [{"rule_id": "NETEX-XSD-001", "status": "NOT_EVALUABLE",
            "reason": "El XML no se pudo interpretar; la validación contra el esquema no se ejecutó sobre un documento interpretable.",
            "scope_not_covered": "Conformidad XSD, perfil, referencias y calidad del servicio.",
            "alternative": "Corregir el XML, identificar la nueva fuente y evaluar XML, esquema y perfil por separado.",
            "alternative_status": "PROPOSED_NOT_EXECUTED"}]},
        "conclusion": conclusion(controls, context), "reconciliation": {"source_record_count": None, "reconciled_event_count": None,
            "basis": "Evidencia histórica agregada y un caso de referencia; no se inventa un archivo de hallazgos completo."},
        "scope_note": "Ejemplo interno sobre un fichero sintético y evidencia histórica; no es una auditoría de operador ni una ejecución nueva.",
        "release_state": "PRIVATE_REVIEW_REQUIRED", "source_kind": "HISTORICAL_SYNTHETIC_NETEX_REFERENCE",
        "references": {"historical_evidence": "02_EVIDENCIAS/NETEX_HISTORICAL_E2E.json", "registry": "02_EVIDENCIAS/NETEX_RULE_REGISTRY.json",
                       "source_input": "03_SOURCE_DELIVERY/malformed.xml"}})


def finish_model(model):
    model["engagement_gate"] = engagement_gate(model["engagement"])
    model["semantic_sha256"] = semantic_digest(model)
    validate_model(model)
    return model


def json_pointer(path, pointer):
    value = read(path)
    for token in pointer.strip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"}: self.links.append(value)


def reference_index(package, model):
    refs = [{"path": name, "role": role} for role, name in model["references"].items()]
    for name in ("01_DIRECCION/Informe_direccion.pdf", "02_TECNICO/Informe_tecnico.pdf", "02_MODELO/REPORT_MODEL.json"):
        refs.append({"path": name, "role": "CURRENT_DELIVERY"})
    if model["format"] == "GTFS_SCHEDULE":
        for row in read(package / "02_EVIDENCIAS/VALIDATIONS.json"):
            path = row["source"].split("#", 1)[0]
            refs.append({"path": path, "role": "R4_SOURCE_RESOLVED", "rule_id": row["rule_id"]})
        for row in read(package / "02_MODELO/CONTROL_CROSSWALK.json")["controls"]:
            for index in row["source_matrix_indexes"]:
                refs.append({"path": "03_SOURCE_DELIVERY/report/client_report.json", "pointer": f"/validation_matrix/{index}",
                             "role": "SOURCE_MATRIX_ROW", "rule_id": row["rule_id"]})
        for index, case in enumerate(model["cases"]):
            refs.append({"path": "02_MODELO/PRESENTATION_MODEL.json", "pointer": f"/cases/{index}/occurrences", "role": "CASE_OCCURRENCES", "case_id": case["case_id"]})
        for p in files(package / "02_EVIDENCIAS/legal_sources"):
            refs.append({"path": p.relative_to(package).as_posix(), "role": "CAPTURED_LEGAL_SOURCE"})
    for ref in refs:
        path = contained(package, ref["path"])
        if not path.is_file(): raise ValueError("Missing active reference: " + ref["path"])
        if "pointer" in ref: json_pointer(path, ref["pointer"])
        ref["sha256"] = digest(path)
    return {"contract": "TDL_PORTABLE_REFERENCE_INDEX/1", "active_references": refs,
            "historical_metadata_policy": "Absolute paths and archived selectors remain historical provenance, not runtime dependencies.",
            "external_urls_policy": "Online links in original normative material are contextual; captured sources are included."}


def index_html(package, model):
    items = [("01_DIRECCION/Informe_direccion.pdf", "Informe para dirección", "Decisiones, exposición y siguiente paso."),
             ("02_TECNICO/Informe_tecnico.pdf", "Informe para el equipo técnico", "Criterios, controles, casos y pruebas de cierre."),
             ("02_MODELO/REPORT_MODEL.json", "Resultados comunes", "Misma identidad y mismos estados para ambas vistas.")]
    if model["format"] == "GTFS_SCHEDULE":
        items += [("01_RESULTADOS/Plan_de_accion_y_hallazgos_R3_preservado.xlsx", "Libro de detalle original", "Documento R3 preservado; nuevas valoraciones en el informe técnico."),
                  ("01_RESULTADOS/Informe_comercial_transporte.pdf", "Atlas y contexto normativo", "Expediente R4 original, como anexo de consulta."),
                  ("01_RESULTADOS/gis/Auditoria_Palma_R4.qgz", "Proyecto cartográfico", "Requiere un visor compatible; capas incluidas."),
                  ("01_RESULTADOS/Mapa_auditoria.kmz", "Mapa de hallazgos", "Archivo original para un visor compatible."),
                  ("ARCHIVOS_ORIGINALES/R3.zip", "Paquete R3 original", "Archivo completo con sus manifiestos y sellos."),
                  ("ARCHIVOS_ORIGINALES/R4.zip", "Paquete R4 original", "Archivo completo con sus manifiestos y sellos.")]
    items += [("REFERENCE_INDEX.json", "Índice de evidencia", "Referencias relativas verificadas."),
              ("GENERATION_RECEIPT.json", "Identidad de esta entrega", "Origen, versiones y huellas de generación.")]
    cards = "".join(f'<a class="card" href="{escape(path)}"><strong>{escape(title)}</strong><span>{escape(body)}</span></a>' for path, title, body in items)
    html = f'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Transit Data Lab - {escape(model['label'])}</title><style>
body{{margin:0;background:#f1f5f7;color:#163247;font:16px/1.55 Arial,sans-serif}}main{{max-width:1000px;margin:auto;padding:40px 24px}}
.brand{{color:#007e87;font-weight:bold;letter-spacing:.08em}}h1{{font-size:36px;line-height:1.2}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:30px 0}}
.card{{display:block;padding:24px;background:white;border:1px solid #d2dfe4;border-radius:12px;color:inherit;text-decoration:none}}.card strong{{font-size:20px;display:block;margin-bottom:8px}}.card span{{color:#405765}}a:focus-visible{{outline:3px solid #007e87;outline-offset:4px}}.notice{{padding:18px;border-left:5px solid #007e87;background:white}}footer{{font-size:14px;color:#405765}}</style>
<main><div class="brand">TRANSIT DATA LAB</div><h1>{escape(model['label'])}</h1><p>{escape(model['scope_note'])}</p>
<div class="notice">Entrega privada para revisión. La comprensión con clientes, la emisión humana y la aceptación del destinatario siguen pendientes.</div>
<div class="grid">{cards}</div><footer>Los recuentos describen datos y comprobaciones, no viajeros afectados o costes. Las referencias funcionan dentro de esta carpeta; el proyecto cartográfico necesita su aplicación correspondiente.</footer></main></html>'''
    (package / "INDEX.html").write_text(html, encoding="utf-8")


def seal(package):
    artifacts = {p.relative_to(package).as_posix(): {"sha256": digest(p), "size_bytes": p.stat().st_size}
                 for p in sorted(files(package)) if p.relative_to(package).as_posix() not in INTEGRITY_NAMES}
    write(package / "DELIVERY_MANIFEST.json", {"contract": "TDL_PORTABLE_DELIVERY_MANIFEST/1", "artifacts": artifacts})
    write(package / "DELIVERY_SEAL.json", {"manifest_sha256": digest(package / "DELIVERY_MANIFEST.json")})


def verify_delivery(package):
    from tools.audit_delivery_verify_v1 import verify
    standalone_result = verify(package)
    package = Path(package)
    manifest = read(package / "DELIVERY_MANIFEST.json")
    if digest(package / "DELIVERY_MANIFEST.json") != read(package / "DELIVERY_SEAL.json")["manifest_sha256"]:
        raise ValueError("Delivery seal mismatch")
    actual = {p.relative_to(package).as_posix() for p in files(package)} - INTEGRITY_NAMES
    if actual != set(manifest["artifacts"]): raise ValueError("Delivery inventory differs")
    for name, expected in manifest["artifacts"].items():
        path = contained(package, name)
        if digest(path) != expected["sha256"] or path.stat().st_size != expected["size_bytes"]: raise ValueError("Delivery artifact changed: " + name)
    model = read(package / "02_MODELO/REPORT_MODEL.json"); validate_model(model)
    ref_count = 0
    for ref in read(package / "REFERENCE_INDEX.json")["active_references"]:
        path = contained(package, ref["path"])
        if digest(path) != ref["sha256"]: raise ValueError("Reference hash differs")
        if "pointer" in ref:
            row = json_pointer(path, ref["pointer"])
            if "rule_id" in ref and row["rule_id"] != ref["rule_id"]: raise ValueError("Reference points to another control")
        ref_count += 1
    parser = Links(); parser.feed((package / "INDEX.html").read_text(encoding="utf-8"))
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: raise ValueError("Unexpected online index dependency")
        if not contained(package, unquote(url.path)).is_file(): raise ValueError("Broken index link")
    views = read(package / "VIEW_CONSISTENCY.json")
    if any(view["semantic_sha256"] != model["semantic_sha256"] for view in views["views"]): raise ValueError("Views use different semantic models")
    return {"result": "PASS", "standalone": standalone_result["standalone"], "files": len(actual), "active_references": ref_count, "index_links": len(parser.links),
            "format": model["format"], "semantic_sha256": model["semantic_sha256"]}


def generate(format, output, r3=None, r4=None, assessment=None, foundation=None, source=None):
    from tools.audit_delivery_pdf_v1 import build_reports
    output = Path(output)
    for root in (r3, r4, assessment, foundation):
        if root and (Path(root).resolve() == output.resolve() or Path(root).resolve() in output.resolve().parents):
            raise ValueError("Output must not be inside input evidence")
    preservation = {}
    if format == "GTFS_SCHEDULE":
        if any(v is None for v in (r3, r4, assessment, foundation, source)): raise ValueError("GTFS delivery inputs are required")
        preservation["R3"] = verify_original(r3, "02_EVIDENCIAS/PACKAGE_MANIFEST.json", "02_EVIDENCIAS/PACKAGE_SEAL.json")
        preservation["R4"] = verify_original(r4, "02_EVIDENCIAS/SUPPLEMENT_MANIFEST.json", "02_EVIDENCIAS/SUPPLEMENT_SEAL.json")
        model = model_gtfs(r3, assessment, foundation, source)
    elif format == "NETEX": model = model_netex()
    else: raise ValueError("Unsupported delivery format")
    output.mkdir(parents=True, exist_ok=False)
    if format == "GTFS_SCHEDULE":
        copy_tree(r3 / "03_SOURCE_DELIVERY", output / "03_SOURCE_DELIVERY")
        copy_file(source, output / "03_SOURCE_DELIVERY/source/00001.zip")
        copy_tree(r4 / "01_RESULTADOS", output / "01_RESULTADOS")
        for path in files(r4 / "02_EVIDENCIAS"):
            if path.name not in {"SUPPLEMENT_MANIFEST.json", "SUPPLEMENT_SEAL.json"}:
                copy_file(path, output / "02_EVIDENCIAS" / path.relative_to(r4 / "02_EVIDENCIAS"))
        copy_file(r3 / "01_RESULTADOS/Mapa_auditoria.kmz", output / "01_RESULTADOS/Mapa_auditoria.kmz")
        copy_file(r3 / "02_EVIDENCIAS/PRESENTATION_MODEL.json", output / "02_MODELO/PRESENTATION_MODEL.json")
        for name in ("ASSESSED_FINDINGS.json", "COVERAGE_EXPLANATION.json", "TECHNICAL_CONCLUSION.json", "SOURCE_POPULATIONS.json"):
            copy_file(assessment / name, output / "02_MODELO" / name)
        copy_file(foundation / "CONTROL_CROSSWALK.json", output / "02_MODELO/CONTROL_CROSSWALK.json")
        (output / "ARCHIVOS_ORIGINALES").mkdir()
        archive_original(r3, output / "ARCHIVOS_ORIGINALES/R3.zip")
        archive_original(r4, output / "ARCHIVOS_ORIGINALES/R4.zip")
    else:
        copy_file(ROOT / "02_Data_Engineering/NeTEx_Lab/tests/fixtures/malformed.xml", output / "03_SOURCE_DELIVERY/malformed.xml")
        copy_file(ROOT / "02_Data_Engineering/NeTEx_Lab/reports/evidence/e2e_synthetic_20261002.json", output / "02_EVIDENCIAS/NETEX_HISTORICAL_E2E.json")
        copy_file(ROOT / "02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json", output / "02_EVIDENCIAS/NETEX_RULE_REGISTRY.json")
    write(output / "02_MODELO/REPORT_MODEL.json", model)
    copy_file(ROOT / "tools/audit_delivery_verify_v1.py", output / "VERIFICAR.py")
    views = build_reports(model, output)
    write(output / "VIEW_CONSISTENCY.json", {"contract": "TDL_DUAL_VIEW_CONSISTENCY/1", "views": views})
    write(output / "REFERENCE_INDEX.json", reference_index(output, model))
    write(output / "GENERATION_RECEIPT.json", {"contract": "TDL_DUAL_DELIVERY_RECEIPT/1", "format": format,
        "source_sha256": model["identity"]["source_sha256"], "semantic_sha256": model["semantic_sha256"],
        "generator_sha256": digest(Path(__file__)), "pdf_generator_sha256": digest(ROOT / "tools/audit_delivery_pdf_v1.py"),
        "original_package_verification": preservation, "source_identity": model["identity"],
        "new_engine_execution": False, "human_emission_review": "PENDING", "customer_comprehension": "NOT_TESTED"})
    index_html(output, model)
    seal(output)
    return verify_delivery(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["GTFS_SCHEDULE", "NETEX"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    for name in ("r3", "r4", "assessment", "foundation", "source"): parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    result = verify_delivery(args.output) if args.verify else generate(args.format, args.output, args.r3, args.r4, args.assessment, args.foundation, args.source)
    print(json.dumps(result, ensure_ascii=False))
