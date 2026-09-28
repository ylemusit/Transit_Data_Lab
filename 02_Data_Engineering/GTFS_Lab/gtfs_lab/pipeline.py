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
from .ingestion import IngestionError, load_dataset
from .validation import validate

def run(zip_path: Path, output_root: Path, route_id: str | None = None, direction_id: str | None = None) -> dict:
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
        validation = validate(ctx)
        validation = _attach_compliance_result(validation, compliance)
        required = ("agency", "stops", "routes", "trips", "stop_times")
        file_integrity = "PASS" if all(ctx.inventory[t] == "PRESENT" for t in required) else "FAIL"
        schema_integrity = "NOT_EVALUABLE" if file_integrity != "PASS" else "PASS" if all(ctx.dataset.files.get(t + ".txt", {}).get("headers") for t in required) else "FAIL"
        referential_integrity = "NOT_EVALUABLE" if file_integrity != "PASS" else "INSPECTION_ERROR" if any(r["scope"] == "COMPLIANCE_V1" and r["status"] == "INSPECTION_ERROR" for r in validation["rules"]) else "FAIL_TECHNICAL" if any(r["status"] == "FAIL_TECHNICAL" and r["scope"] == "REFERENTIAL" for r in validation["rules"]) else "NOT_EVALUABLE" if any(r["scope"] == "COMPLIANCE_V1" and r["status"] == "NOT_EVALUABLE" for r in validation["rules"]) else "PASS"
        integrity = {"file_integrity": file_integrity, "schema_integrity": schema_integrity, "referential_integrity": referential_integrity, "table_rows": {k: v["rows"] for k, v in ctx.dataset.files.items() if v["status"] == "PRESENT"}}
        analysis_result = analyze(ctx)
        gis_dir = ctx.work_dir / "exports"
        gis_result = {"stops": export_stops(ctx, gis_dir), "routes": export_route(ctx, gis_dir / "routes", route_id, direction_id)}
        db_result = build_duckdb(ctx)
        result.update({"integrity": integrity, "validation": validation, "analysis": analysis_result, "gis": gis_result, "database": db_result, "compliance_v1": compliance, "ended_at_utc": datetime.now(timezone.utc).isoformat(), "errors": []})
        integrity_status = next((integrity[k] for k in ("file_integrity", "schema_integrity", "referential_integrity") if integrity[k] != "PASS"), "PASS")
        result["summary"] = {"ingestion": "PASS", "integrity": integrity_status, "validation": validation["status"], "findings": validation["finding_count"], "analysis": "PASS", "gis": "PASS" if gis_result["stops"]["status"] == "PASS" or gis_result["routes"]["status"] == "PASS" else "NOT_EVALUABLE", "database": db_result["status"], "compliance_v1": compliance["result"]}
        write_json(ctx.work_dir / "run.json", result)
        write_json(ctx.work_dir / "analysis.json", analysis_result)
        write_json(ctx.work_dir / "validation.json", validation)
        report = render_report(result)
        (ctx.work_dir / "report.md").write_text(report, encoding="utf-8")
        persist_audit(ctx, result)
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
    result = {"run_id": run_id, "dataset": {"dataset_id": "GTFS-" + digest[:16] if digest else None, "source_filename": zip_path.name, "source_sha256": digest}, "gtfs_lab_version": VERSION, "parser_version": "gtfs-lab-csv/1", "validator_version": "1.0.0", "started_at_utc": started, "ended_at_utc": datetime.now(timezone.utc).isoformat(), "ingestion": {"status": "INGESTION_ERROR"}, "integrity": {"status": "SKIPPED_BY_DEPENDENCY"}, "validation": {"status": "SKIPPED_BY_DEPENDENCY", "findings": []}, "analysis": {"status": "SKIPPED_BY_DEPENDENCY"}, "gis": {"status": "SKIPPED_BY_DEPENDENCY"}, "compliance_v1": {"status": "SKIPPED_BY_DEPENDENCY"}, "errors": [{"type": "INGESTION_ERROR", "message": str(error)}], "summary": {"ingestion": "INGESTION_ERROR", "integrity": "SKIPPED_BY_DEPENDENCY", "validation": "SKIPPED_BY_DEPENDENCY", "analysis": "SKIPPED_BY_DEPENDENCY", "gis": "SKIPPED_BY_DEPENDENCY", "compliance_v1": "SKIPPED_BY_DEPENDENCY"}}
    write_json(work_dir / "run.json", result)
    (work_dir / "report.md").write_text("# Informe técnico GTFS_Lab — error de ingestión\n\n" + f"- Run: `{run_id}`\n- Fuente: `{zip_path.name}`\n- SHA-256: `{digest or 'NO_DISPONIBLE'}`\n- Estado: `INGESTION_ERROR`\n- Error: {error}\n\nValidación, análisis, GIS y Compliance se marcaron `SKIPPED_BY_DEPENDENCY`; no se generaron findings GTFS.\n\nYeison Arbey Carrillo Lemus. Todos los derechos reservados.\n", encoding="utf-8")
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
    lines += ["", "## Análisis", "", "```json", json.dumps(run_result["analysis"]["counts"], ensure_ascii=False, indent=2), "```", f"- Rutas: {len(run_result['analysis']['routes'])}; paradas compartidas: {len(run_result['analysis']['shared_stops'])}", f"- Calendario: {service_summary['status']}; servicios con fechas: {len(service_summary.get('active_dates_by_service_id', {}))}; pares servicio-fecha: {active_dates}", "", "## GIS y DuckDB", "", f"- GeoJSON/KML paradas: {run_result['gis']['stops']['status']} ({run_result['gis']['stops'].get('features', 0)} entidades)", f"- GIS rutas/formas: {run_result['gis']['routes']['status']} ({len(run_result['gis']['routes'].get('artifacts', []))} archivos)", f"- Base DuckDB aislada: {run_result['database']['status']}", "", "## Compliance V1", "", f"- Regla: `{run_result['compliance_v1']['rule_id']}` → `{run_result['compliance_v1']['result']}` ({run_result['compliance_v1'].get('reason', '')})", f"- Evaluador: `{run_result['compliance_v1'].get('evaluator_version')}` / `{run_result['compliance_v1'].get('evaluator_sha256')}`.", f"- Procedencia: {run_result['compliance_v1']['provenance']}.", "", "## Límites", "", "- Resultado exclusivamente técnico; no concluye cumplimiento jurídico ni incumplimiento de operador.", "- SIRI y GTFS-RT no se procesan; tablas GTFS adicionales solo se inventariarían si están en el catálogo soportado.", "- Revisión de falsos positivos debe conservar specification, interpretation, implementation, input/hash, versión/parser, validador y serialización antes de atribuirlos al operador.", "", "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""]
    return "\n".join(lines)
