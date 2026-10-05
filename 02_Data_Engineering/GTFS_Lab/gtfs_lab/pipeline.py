from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import json
from . import VERSION
from .analysis import analyze
from .audit_persistence import persist_audit
from .compliance_adapter import inspect_fixed_stop_references
from .core import new_run_id, sha256_file, write_json
from .database import build_duckdb
from .gis import export_route, export_stops
from .g03_structure import inspect_g03_archive
from .g04_identity import evaluate_g04
from .g05_temporal import evaluate_g05
from .g06_operations import evaluate_g06
from .g07_spatial import evaluate_g07
from .g08_quality import evaluate_g08_run
from .g09_reporting import build_engine_report, render_engine_report
from .ingestion import IngestionError, load_dataset
from .validation import validate
from .resource_stages import mark as _mark_stage

def run(zip_path: Path, output_root: Path, route_id: str | None = None, direction_id: str | None = None) -> dict:
    _mark_stage("AUDIT", "START")
    g03_result = inspect_g03_archive(zip_path)
    ctx = load_dataset(zip_path, output_root)
    try:
        result = {
            "run_id": ctx.run_id,
            "dataset": ctx.dataset.__dict__,
            "gtfs_lab_version": VERSION,
            "validator_version": "1.0.0",
            "ingestion": {"status": "PASS", "warnings": ctx.warnings},
            "started_at_utc": datetime.now(timezone.utc).isoformat(),
            "inventory": ctx.inventory,
            "warnings": ctx.warnings,
        }
        compliance = inspect_fixed_stop_references(ctx)
        compliance["run_id"] = ctx.run_id
        g03_catalog = g03_result["file_catalog"]
        validation = validate(ctx)
        validation = _attach_compliance_result(validation, compliance)
        g04_result = evaluate_g04(ctx, g03_result, validation)
        g05_result = evaluate_g05(ctx, g03_result, g04_result)
        g06_result = evaluate_g06(ctx, g03_result, g04_result, g05_result)
        g07_result = evaluate_g07(ctx, g03_result, g04_result)
        g08_result = evaluate_g08_run(ctx, g03_result)
        required = ("agency", "stops", "routes", "trips", "stop_times")
        file_integrity = "PASS" if all(ctx.inventory[t] == "PRESENT" for t in required) else "FAIL"
        schema_integrity = "NOT_EVALUABLE" if file_integrity != "PASS" else "PASS" if all(ctx.dataset.files.get(t + ".txt", {}).get("headers") for t in required) else "FAIL"
        referential_integrity = "NOT_EVALUABLE" if file_integrity != "PASS" else "INSPECTION_ERROR" if any(r["scope"] == "COMPLIANCE_V1" and r["status"] == "INSPECTION_ERROR" for r in validation["rules"]) else "FAIL_TECHNICAL" if any(r["status"] == "FAIL_TECHNICAL" and r["scope"] == "REFERENTIAL" for r in validation["rules"]) else "NOT_EVALUABLE" if any(r["scope"] == "COMPLIANCE_V1" and r["status"] == "NOT_EVALUABLE" for r in validation["rules"]) else "PASS"
        integrity = {"file_integrity": file_integrity, "schema_integrity": schema_integrity, "referential_integrity": referential_integrity, "table_rows": {k: v["rows"] for k, v in ctx.dataset.files.items() if v["status"] == "PRESENT"}}
        analysis_result = analyze(ctx)
        gis_dir = ctx.work_dir / "exports"
        gis_result = {"stops": export_stops(ctx, gis_dir), "routes": export_route(ctx, gis_dir / "routes", route_id, direction_id)}
        db_result = build_duckdb(ctx)
        result.update({"integrity": integrity, "validation": validation, "g03_file_catalog": g03_catalog, "g03": g03_result, "g04": g04_result, "g05": g05_result, "g06": g06_result, "g07": g07_result, "g08": g08_result, "analysis": analysis_result, "gis": gis_result, "database": db_result, "compliance_v1": compliance, "ended_at_utc": datetime.now(timezone.utc).isoformat(), "errors": []})
        integrity_status = next((integrity[k] for k in ("file_integrity", "schema_integrity", "referential_integrity") if integrity[k] != "PASS"), "PASS")
        result["summary"] = {"ingestion": "PASS", "integrity": integrity_status, "validation": validation["status"], "findings": validation["finding_count"], "g03_file_catalog": g03_catalog["status"], "g03": g03_result["status"], "g04": g04_result["status"], "g05": g05_result["status"], "g06": g06_result["status"], "g07": g07_result["status"], "analysis": "PASS", "gis": "PASS" if gis_result["stops"]["status"] == "PASS" or gis_result["routes"]["status"] == "PASS" else "NOT_EVALUABLE", "database": db_result["status"], "compliance_v1": compliance["result"]}
        _mark_stage("AUDIT", "END")
        _mark_stage("REPORT_GENERATION", "START")
        _mark_stage("REPORT_INPUT_PREPARATION", "START", lambda: {
            "validation_findings": validation.get("finding_count", len(validation.get("findings", []))),
            "g03_findings": len(g03_result.get("findings", [])),
            "g04_findings": len(g04_result.get("findings", [])),
            "g05_findings": len(g05_result.get("findings", [])),
            "g06_findings": len(g06_result.get("findings", [])),
            "g07_findings": len(g07_result.get("findings", [])),
            "g08_findings": len(g08_result.get("findings", [])),
            "run_top_level_keys": len(result),
        })
        _mark_stage("REPORT_INPUT_PREPARATION", "END")
        _mark_stage("JSON_SERIALIZATION_AND_FILE_WRITE", "START")
        write_json(ctx.work_dir / "run.json", result)
        write_json(ctx.work_dir / "analysis.json", analysis_result)
        write_json(ctx.work_dir / "validation.json", validation)
        write_json(ctx.work_dir / "g04.json", g04_result)
        write_json(ctx.work_dir / "g05.json", g05_result)
        write_json(ctx.work_dir / "g06.json", g06_result)
        write_json(ctx.work_dir / "g07.json", g07_result)
        write_json(ctx.work_dir / "g08.json", g08_result)
        _mark_stage("JSON_SERIALIZATION_AND_FILE_WRITE", "END")
        _mark_stage("MARKDOWN_MODEL_BUILD", "START")
        report = render_report(result)
        _mark_stage("MARKDOWN_MODEL_BUILD", "END", lambda: {"report_characters": len(report)})
        _mark_stage("MARKDOWN_FILE_WRITE", "START")
        (ctx.work_dir / "report.md").write_text(report, encoding="utf-8")
        _mark_stage("MARKDOWN_FILE_WRITE", "END")
        _mark_stage("ENGINE_JSON_MODEL_BUILD", "START")
        engine_report = build_engine_report(result)
        _mark_stage("ENGINE_JSON_MODEL_BUILD", "END", lambda: {
            "finding_rows": len(engine_report.get("technical_evaluation", {}).get("findings", [])),
            "recommendation_findings": len(engine_report.get("recommendation_findings", [])),
            "top_level_keys": len(engine_report),
        })
        _mark_stage("ENGINE_JSON_SERIALIZATION_AND_FILE_WRITE", "START")
        write_json(ctx.work_dir / "engine_report.json", engine_report)
        _mark_stage("ENGINE_JSON_SERIALIZATION_AND_FILE_WRITE", "END")
        _mark_stage("ENGINE_MARKDOWN_MODEL_BUILD", "START")
        engine_markdown = render_engine_report(engine_report)
        _mark_stage("ENGINE_MARKDOWN_MODEL_BUILD", "END", lambda: {"report_characters": len(engine_markdown)})
        _mark_stage("ENGINE_MARKDOWN_FILE_WRITE", "START")
        (ctx.work_dir / "engine_report.md").write_text(engine_markdown, encoding="utf-8")
        _mark_stage("ENGINE_MARKDOWN_FILE_WRITE", "END")
        _mark_stage("EVIDENCE_REFERENCE_AND_PERSISTENCE_BUILD", "START")
        persistence = persist_audit(ctx, result)
        if persistence.get("manifest_status") != "ACCEPTED":
            raise RuntimeError(
                f"Trust audit persistence was not accepted: {persistence}"
            )
        _mark_stage("EVIDENCE_REFERENCE_AND_PERSISTENCE_BUILD", "END", lambda: {
            "manifest_status": persistence.get("manifest_status")
        })
        _mark_stage("REPORT_GENERATION", "END")
        return result
    except Exception:
        # Do not erase partial evidence; mark run error with context for diagnosis.
        raise

def record_ingestion_error(zip_path: Path, output_root: Path, error: Exception) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    digest = sha256_file(zip_path) if zip_path.is_file() else None
    run_id = new_run_id()
    work_dir = output_root.resolve() / run_id
    work_dir.mkdir(parents=True, exist_ok=False)
    g03_result = inspect_g03_archive(zip_path) if zip_path.is_file() else {"status": "INSPECTION_ERROR"}
    result = {"run_id": run_id, "dataset": {"dataset_id": "GTFS-" + digest[:16] if digest else None, "source_filename": zip_path.name, "source_sha256": digest}, "gtfs_lab_version": VERSION, "parser_version": "gtfs-lab-csv/1", "validator_version": "1.0.0", "started_at_utc": started, "ended_at_utc": datetime.now(timezone.utc).isoformat(), "ingestion": {"status": "INGESTION_ERROR"}, "integrity": {"status": "SKIPPED_BY_DEPENDENCY"}, "validation": {"status": "SKIPPED_BY_DEPENDENCY", "findings": []}, "g03": g03_result, "g03_file_catalog": g03_result.get("file_catalog", {"status": "INSPECTION_ERROR"}), "g04": {"status": "SKIPPED_BY_DEPENDENCY"}, "g05": {"status": "SKIPPED_BY_DEPENDENCY"}, "g06": {"status": "SKIPPED_BY_DEPENDENCY"}, "g07": {"status": "SKIPPED_BY_DEPENDENCY"}, "g08": {"status": "SKIPPED_BY_DEPENDENCY"}, "analysis": {"status": "SKIPPED_BY_DEPENDENCY"}, "gis": {"status": "SKIPPED_BY_DEPENDENCY"}, "compliance_v1": {"status": "SKIPPED_BY_DEPENDENCY"}, "errors": [{"type": "INGESTION_ERROR", "message": str(error)}], "summary": {"ingestion": "INGESTION_ERROR", "integrity": "SKIPPED_BY_DEPENDENCY", "validation": "SKIPPED_BY_DEPENDENCY", "g03": g03_result.get("status", "INSPECTION_ERROR"), "g04": "SKIPPED_BY_DEPENDENCY", "g05": "SKIPPED_BY_DEPENDENCY", "g06": "SKIPPED_BY_DEPENDENCY", "g07": "SKIPPED_BY_DEPENDENCY", "g08": "SKIPPED_BY_DEPENDENCY", "analysis": "SKIPPED_BY_DEPENDENCY", "gis": "SKIPPED_BY_DEPENDENCY", "compliance_v1": "SKIPPED_BY_DEPENDENCY"}}
    write_json(work_dir / "run.json", result)
    g03_status = g03_result.get("status", "INSPECTION_ERROR")
    (work_dir / "report.md").write_text("# Informe técnico GTFS_Lab — error de ingestión\n\n" + f"- Run: `{run_id}`\n- Fuente: `{zip_path.name}`\n- SHA-256: `{digest or 'NO_DISPONIBLE'}`\n- Estado: `INGESTION_ERROR`\n- Error: {error}\n- G03 estructural: `{g03_status}` (resultado independiente; findings legacy no evaluados).\n\nValidación, análisis, GIS y Compliance se marcaron `SKIPPED_BY_DEPENDENCY`; no se generaron findings legacy.\n\nYeison Arbey Carrillo Lemus. Todos los derechos reservados.\n", encoding="utf-8")
    return result

def _attach_compliance_result(validation: dict, compliance: dict) -> dict:
    validation["local_status"] = validation["status"]
    validation["compliance_v1_status"] = compliance["result"]
    validation["rules"].append({"rule_id": compliance["rule_id"], "version": compliance["rule_version"], "scope": "COMPLIANCE_V1", "severity": "ERROR", "description": "Fixed-stop stop_times references to trips and stops", "source_reference": f"gtfs_reference.md sha256={compliance.get('reference_sha256')}", "status": compliance["result"], "checked_rows": 0, "finding_count": len(compliance["findings"]), "findings": compliance["findings"], "evaluator_sha256": compliance.get("evaluator_sha256")})
    validation["findings"].extend(compliance["findings"])
    validation["finding_count"] = len(validation["findings"])
    local_status = validation["local_status"]
    comp_status = compliance["result"]
    if local_status == "FAIL_TECHNICAL" or comp_status == "FAIL_TECHNICAL":
        validation["status"] = "FAIL_TECHNICAL"
    elif local_status == "INSPECTION_ERROR" or comp_status == "INSPECTION_ERROR":
        validation["status"] = "INSPECTION_ERROR"
    elif local_status == "NOT_EVALUABLE" or comp_status == "NOT_EVALUABLE":
        validation["status"] = "NOT_EVALUABLE"
    else:
        validation["status"] = "PASS"
    return validation

def render_report(run_result: dict) -> str:
    d = run_result["dataset"]
    lines = ["# Informe técnico GTFS_Lab", "", f"- Run: `{run_result['run_id']}`", f"- Dataset: `{d['dataset_id']}`", f"- Fuente: `{d['source_filename']}`", f"- SHA-256: `{d['source_sha256']}`", f"- Ingesta UTC: `{d['ingestion_timestamp_utc']}`", f"- GTFS_Lab: `{run_result['gtfs_lab_version']}`; parser: `{d['parser_version']}`; reglas: `{run_result['validator_version']}`", "", "## Tablas y filas", "", "| Tabla | Estado | Filas |", "|---|---:|---:|"]
    for table, status in run_result["inventory"].items():
        label = table.removeprefix("NOT_SUPPORTED:") if table.startswith("NOT_SUPPORTED:") else table + ".txt"
        count = d["files"].get(table + ".txt", {}).get("rows", 0)
        lines.append(f"| {label} | {status} | {count} |")
    catalog = run_result["g03_file_catalog"]
    lines += ["", "## G03 — Catálogo de archivos", "", f"- Detección: `{catalog['status']}`; miembros examinados: {catalog['checked_members']}; cobertura del catálogo oficial: `{catalog['official_catalog_coverage']}`.", "", "| Miembro | Clasificación |", "|---|---|"]
    for member in catalog["members"]:
        lines.append(f"| `{member['path']}` | `{member['classification']}` |")
    lines.append(f"- Límite: {catalog['limitation']}")
    if "g03" in run_result:
        lines += ["", "## G03 — Estructura y contrato", "", f"- Estado: `{run_result['g03']['status']}`; el resultado G03 permanece separado de los findings legacy."]
        for rule in run_result["g03"].get("rules", []):
            lines.append(f"- `{rule['rule_id']}`: `{rule['status']}`; findings: {len(rule['findings'])}; evaluador ejecutado: `{rule['evaluator_executed']}`.")
        if "header_schema" in run_result["g03"]:
            lines.append(f"- Gap de metadatos: {', '.join(run_result['g03']['header_schema'].get('missing_metadata', []))}")
    if "g04" in run_result:
        lines += ["", "## G04 — Identidad e integridad referencial", "", f"- Estado independiente: `{run_result['g04']['status']}`; hallazgos: {len(run_result['g04'].get('findings', []))}."]
        for rule in run_result["g04"].get("rules", []):
            lines.append(f"- `{rule['rule_id']}`: `{rule['status']}`; no evaluables: {rule.get('coverage', {}).get('not_evaluable', 'N/D')}.")
        lines += ["", "Solapamiento con legacy (comparación técnica; no implica equivalencia):", "", "| Regla legacy | Hallazgos legacy | Hallazgos G04 | Pares coincidentes |", "|---|---:|---:|---:|"]
        for comparison in run_result["g04"].get("legacy_comparison", []):
            lines.append(f"| `{comparison['legacy_rule_id']}` | {comparison['legacy_findings']} | {comparison['g04_findings']} | {comparison['matching_finding_pairs']} |")
    for phase in ("g05", "g06", "g07"):
        if phase in run_result:
            title = phase.upper()
            lines += ["", f"## {title} — auditoría especializada", "", f"- Estado: `{run_result[phase]['status']}`; hallazgos: {len(run_result[phase].get('findings', []))}."]
            for rule in run_result[phase].get("rules", []):
                detail = f"; recomendación cumplida: `{rule['recommendation_met']}`" if phase == "g08" else f"; no evaluables: {rule.get('coverage', {}).get('not_evaluable', 'N/D')}"
                lines.append(f"- `{rule['rule_id']}`: `{rule['status']}`{detail}.")
    lines += ["", "## Integridad", "", f"- Archivos: {run_result['integrity']['file_integrity']}", f"- Esquema: {run_result['integrity']['schema_integrity']}", f"- Referencial: {run_result['integrity']['referential_integrity']}", "", "## Validación", "", f"Estado: **{run_result['validation']['status']}**; hallazgos técnicos: {run_result['validation']['finding_count']}", "", "| Regla | Estado | Hallazgos |", "|---|---|---:|"]
    for r in run_result["validation"]["rules"]: lines.append(f"| {r['rule_id']} | {r['status']} | {r['finding_count']} |")
    lines += ["", "Hallazgos:"]
    if run_result["validation"]["findings"]:
        for f in run_result["validation"]["findings"]:
            lines.append(f"- `{f['rule_id']}` {f['table']} {f['row_locator']} / {f['field']}: observado `{f['observed_value']}`; esperado {f['expected_condition']}. {f['technical_message']}")
    else:
        lines.append("- Ninguno.")
    service_summary = run_result["analysis"]["service_calendar_summary"]
    active_dates = sum(len(values) for values in service_summary.get("active_dates_by_service_id", {}).values())
    lines += ["", "## Análisis", "", "```json", json.dumps(run_result["analysis"]["counts"], ensure_ascii=False, indent=2), "```", f"- Rutas: {len(run_result['analysis']['routes'])}; paradas compartidas: {len(run_result['analysis']['shared_stops'])}", f"- Calendario: {service_summary['status']}; servicios con fechas: {len(service_summary.get('active_dates_by_service_id', {}))}; pares servicio-fecha: {active_dates}", "", "## GIS y DuckDB", "", f"- GeoJSON/KML paradas: {run_result['gis']['stops']['status']} ({run_result['gis']['stops'].get('features', 0)} entidades)", f"- GIS rutas/formas: {run_result['gis']['routes']['status']} ({len(run_result['gis']['routes'].get('artifacts', []))} archivos)", f"- Base DuckDB aislada: {run_result['database']['status']}", "", "## Compliance V1", "", f"- Regla: `{run_result['compliance_v1']['rule_id']}` → `{run_result['compliance_v1']['result']}` ({run_result['compliance_v1'].get('reason', '')})", f"- Evaluador: `{run_result['compliance_v1'].get('evaluator_version')}` / `{run_result['compliance_v1'].get('evaluator_sha256')}`.", f"- Procedencia: {run_result['compliance_v1']['provenance']}.", "", "## Límites", "", "- Resultado exclusivamente técnico; no concluye cumplimiento jurídico ni incumplimiento de operador.", "- SIRI y GTFS-RT no se procesan; las tablas adicionales detectadas permanecen no inspeccionadas salvo el subconjunto declarado y no elevan cobertura por sí solas.", "- Revisión de falsos positivos debe conservar specification, interpretation, implementation, input/hash, versión/parser, validador y serialización antes de atribuirlos al operador.", "", "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""]
    return "\n".join(lines)
