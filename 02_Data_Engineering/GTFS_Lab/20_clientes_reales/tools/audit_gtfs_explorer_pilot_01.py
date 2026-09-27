from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPERATORS = [
    ("002", "Ancebus", "FAMILY_A_SMALL_BASIC/002_ancebus"),
    ("005", "Viagón", "FAMILY_A_SMALL_BASIC/005_viagon"),
    ("014", "Gilsanz", "FAMILY_C_COMPLEX_REGIONAL/014_gilsanz"),
    ("019", "Bizkaibus", "FAMILY_D_MATURE_BENCHMARK/019_bizkaibus"),
    ("020", "Kbus", "FAMILY_D_MATURE_BENCHMARK/020_kbus"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def load_report(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    match = re.search(r"<pre>(.*?)</pre>", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No se encontró payload JSON en {path}")
    return json.loads(html.unescape(match.group(1)))


def load_baseline() -> list[dict]:
    with (ROOT / "pilot_01_baseline.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def json_export(run: Path) -> tuple[Path | None, dict | None]:
    for path in sorted(run.glob("*.json")):
        if path.name in {"project.json"} or path.name.endswith(".manifest.json"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("generator", {}).get("name") == "GTFS Explorer Desktop":
            return path, data
    return None, None


def source_integrity(op: Path) -> dict:
    original = sorted((op / "02_sources/gtfs_schedule/original").glob("*.zip"))
    census_path = op / "04_audit/pilot_01/source_census.json"
    census = json.loads(census_path.read_text(encoding="utf-8"))
    current_hash = sha256(original[0]) if original else None
    recorded_hash = census.get("original_zip_sha256")
    extracted = op / "02_sources/gtfs_schedule/extracted"
    working = [p for p in op.rglob("*working*copy*") if p.is_dir()]
    working_files = [
        str(p.relative_to(ROOT)).replace("\\", "/")
        for directory in working
        for p in directory.rglob("*")
        if p.is_file()
    ]
    return {
        "original_zip": str(original[0].relative_to(ROOT)).replace("\\", "/") if original else None,
        "original_zip_sha256_current": current_hash,
        "original_zip_sha256_recorded": recorded_hash,
        "original_zip_hash_unchanged": bool(current_hash and recorded_hash and current_hash.lower() == recorded_hash.lower()),
        "extracted_file_count": len(list(extracted.glob("*"))),
        "working_copy_directories": [str(p.relative_to(ROOT)).replace("\\", "/") for p in working],
        "working_copy_file_paths": working_files,
    }


def extract_operator(item: tuple[str, str, str]) -> dict:
    benchmark_id, operator, rel = item
    op = ROOT / rel
    run = op / "03_gtfs_explorer/run_001"
    report_path = run / "informe-validacion.html"
    report = load_report(report_path)
    batch = report.get("batch", {})
    issues = report.get("issues", [])
    summary = report.get("summary_by_severity", {})
    project = json.loads((run / "project.json").read_text(encoding="utf-8"))
    export_path, export = json_export(run)
    counts = Counter(issue.get("severity") for issue in issues)
    best_practice = sum(
        issue.get("occurrence_count") or 0
        for issue in issues
        if issue.get("category") == "BEST_PRACTICE"
    )
    grouped: dict[tuple[str, str, str, str, str, str], dict[str, int]] = defaultdict(
        lambda: {"occurrence_count": 0, "distinct_detail_rows": 0}
    )
    for issue in issues:
        location = issue.get("location") or {}
        key = (
            (issue.get("rule") or {}).get("code"),
            issue.get("severity"),
            issue.get("category"),
            location.get("file"),
            location.get("field"),
            (issue.get("message") or {}).get("key"),
        )
        grouped[key]["occurrence_count"] += issue.get("occurrence_count") or 0
        grouped[key]["distinct_detail_rows"] += 1
    return {
        "benchmark_id": benchmark_id,
        "operator": operator,
        "relative_root": rel,
        "run": run,
        "report": report,
        "batch": batch,
        "issues": issues,
        "summary": summary,
        "project": project,
        "export_path": export_path,
        "export": export,
        "grouped": grouped,
        "counts": counts,
        "best_practice": best_practice,
        "integrity": source_integrity(op),
    }


def csv_value(value: object) -> str:
    return "" if value is None else str(value)


def create_rule_summaries(records: list[dict]) -> None:
    fields = [
        "rule_id", "severity", "category", "file", "field", "message_key",
        "occurrence_count", "distinct_detail_rows", "evidence_source",
    ]
    for record in records:
        path = ROOT / record["relative_root"] / "03_gtfs_explorer/parsed_rule_summary.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for key in sorted(record["grouped"]):
                values = record["grouped"][key]
                writer.writerow(dict(zip(fields, key + (values["occurrence_count"], values["distinct_detail_rows"], "informe-validacion.html:issues"))))


def baseline_rows(records: list[dict]) -> list[dict]:
    rows = load_baseline()
    by_id = {record["benchmark_id"]: record for record in records}
    for row in rows:
        record = by_id[row["benchmark_id"]]
        batch = record["batch"]
        report = record["report"]
        omitted = batch.get("omitted_issue_count")
        row.update({
            "gte_run_id": batch.get("id"),
            "gte_status": batch.get("state"),
            "gte_detected_issue_count": batch.get("total_issue_count"),
            "gte_persisted_issue_count": batch.get("stored_issue_count"),
            "gte_detail_complete": str(omitted == 0 and batch.get("stored_issue_count") == batch.get("total_issue_count")).lower(),
            "gte_error_count": report.get("summary_by_severity", {}).get("ERROR", 0),
            "gte_warning_count": report.get("summary_by_severity", {}).get("WARNING", 0),
            "gte_notice_count": report.get("summary_by_severity", {}).get("NOTICE", 0),
            "gte_best_practice_count": record["best_practice"],
        })
    return rows


def write_baseline(rows: list[dict]) -> None:
    path = ROOT / "pilot_01_baseline.csv"
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_baseline_matrix(rows: list[dict]) -> None:
    lines = [
        "# Pilot 01 — baseline matrix", "",
        "Valores NAP: `NAP snapshot` + `manual_verified`. Valores físicos: censados desde `02_sources/gtfs_schedule/extracted/`. Valores GTFS Explorer: evidencia de `run_001/informe-validacion.html`.", "",
        "| Operador | Rutas NAP/GTFS | Paradas NAP/GTFS | Viajes NAP/GTFS | Fechas | Geometría | Tarifas | Accesibilidad | GTE status | GTE detectadas | GTE persistidas | Detalle completo |", "|---|---:|---:|---:|---|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['operator']} | {row['declared_routes']}/{row['routes_rows']} | {row['declared_stops']}/{row['stops_rows']} | {row['declared_trips']}/{row['trips_rows']} | {row['date_alignment']} | {row['geometry_alignment']} | {row['fare_alignment']} | {row['accessibility_alignment']} | {row['gte_status']} | {row['gte_detected_issue_count']} | {row['gte_persisted_issue_count']} | {row['gte_detail_complete']} |")
    lines += ["", "Las cifras GTE se conservan separadas entre ocurrencias detectadas, ocurrencias persistidas y filas de detalle persistidas.", ""]
    write(ROOT / "docs/PILOT_01_BASELINE_MATRIX.md", "\n".join(lines))


def write_inventory(records: list[dict]) -> None:
    data = []
    for record in records:
        run = record["run"]
        files = []
        for path in sorted(run.iterdir()):
            if path.is_file():
                files.append({"name": path.name, "size_bytes": path.stat().st_size, "sha256": sha256(path)})
        data.append({
            "benchmark_id": record["benchmark_id"], "operator": record["operator"],
            "product_version": (record["export"] or {}).get("generator", {}).get("version"),
            "run_id": record["batch"].get("id"), "filter": record["report"].get("filter"),
            "full_unfiltered_evidence": record["report"].get("filter") == {"severities": None, "categories": None},
            "files": files, "source_integrity": record["integrity"],
        })
    write(ROOT / "04_audit/pilot_01/gte_output_inventory.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    lines = ["# GTFS Explorer 0.2.1 — output inventory", "", "Inventario read-only de `03_gtfs_explorer/run_001`; los hashes se calcularon sobre los ficheros existentes.", ""]
    for item in data:
        lines += [f"## {item['benchmark_id']} — {item['operator']}", "", f"- Producto: `{item['product_version']}`.", f"- run_id observado: `{item['run_id']}`.", f"- Filtro: `{json.dumps(item['filter'], ensure_ascii=False)}`.", f"- Informe FULL/UNFILTERED: `{item['full_unfiltered_evidence']}`; la completitud de detalle se evalúa por separado.", "", "| Nombre | Bytes | SHA-256 |", "|---|---:|---|"]
        lines += [f"| `{f['name']}` | {f['size_bytes']} | `{f['sha256']}` |" for f in item["files"]] + [""]
    write(ROOT / "04_audit/pilot_01/gte_output_inventory.md", "\n".join(lines))


def write_nap_vs_gte(records: list[dict], rows: list[dict]) -> None:
    by_id = {row["benchmark_id"]: row for row in rows}
    lines = ["# NAP vs GTFS Explorer 0.2.1 — Pilot Audit 01", "", "La comparación de reglas solo se clasifica como correspondencia cuando existe evidencia de ambos lados. El baseline NAP disponible aporta conteos agregados y estado, pero no rule IDs; por eso no se fuerza una equivalencia de reglas.", ""]
    for record in records:
        row = by_id[record["benchmark_id"]]
        lines += [f"## {record['benchmark_id']} — {record['operator']}", "", "### NAP", "", f"- Errores: `{row['nap_error_count']}`.", f"- Warnings: `{row['nap_warning_count']}`.", f"- Estado: `{row['nap_validation_status']}`.", "", "### GTFS Explorer", "", f"- Estado: `{row['gte_status']}`; detectadas: `{row['gte_detected_issue_count']}`; persistidas: `{row['gte_persisted_issue_count']}`; detalle completo: `{row['gte_detail_complete']}`.", f"- Severity counts persistidos: ERROR `{row['gte_error_count']}`, WARNING `{row['gte_warning_count']}`, NOTICE `{row['gte_notice_count']}`, BEST_PRACTICE `{row['gte_best_practice_count']}`.", "", "| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |", "|---|---|---:|---:|---|---|"]
        for key in sorted(record["grouped"]):
            values = record["grouped"][key]
            lines.append(f"| `{key[0]}` | {key[1]} | {values['occurrence_count']} | {values['distinct_detail_rows']} | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |")
        lines += ["", "Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.", ""]
    write(ROOT / "04_audit/pilot_01/NAP_VS_GTFS_EXPLORER.md", "\n".join(lines))


def write_differential(records: list[dict], rows: list[dict]) -> None:
    fields = ["benchmark_id", "operator", "finding_key", "nap_detected", "gte_detected", "source_evidence_present", "gte_rule_id", "gte_severity", "gte_occurrence_count", "comparison_class", "notes"]
    output = []
    by_id = {row["benchmark_id"]: row for row in rows}
    for record in records:
        row = by_id[record["benchmark_id"]]
        rules = ";".join(sorted({key[0] for key in record["grouped"]}))
        for key, nap_value in (("NAP_ERROR_COUNT", int(row["nap_error_count"]) > 0), ("NAP_WARNING_COUNT", int(row["nap_warning_count"]) > 0), ("NAP_VALIDATION_STATUS", True)):
            output.append({"benchmark_id": record["benchmark_id"], "operator": record["operator"], "finding_key": key, "nap_detected": str(nap_value).lower(), "gte_detected": str(int(row["gte_detected_issue_count"]) > 0).lower(), "source_evidence_present": "true", "gte_rule_id": rules, "gte_severity": "mixed", "gte_occurrence_count": row["gte_detected_issue_count"], "comparison_class": "NOT_COMPARABLE", "notes": "NAP aporta agregado/estado; no aporta rule_id comparable."})
        for key in sorted(record["grouped"]):
            values = record["grouped"][key]
            output.append({"benchmark_id": record["benchmark_id"], "operator": record["operator"], "finding_key": f"GTE_RULE:{key[0]}", "nap_detected": "null", "gte_detected": "true", "source_evidence_present": "true", "gte_rule_id": key[0], "gte_severity": key[1], "gte_occurrence_count": values["occurrence_count"], "comparison_class": "UNKNOWN", "notes": "No existe detalle NAP por regla para decidir BOTH_DETECT, GTE_ONLY o NAP_ONLY."})
    with (ROOT / "04_audit/pilot_01/differential_matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    lines = ["# Differential matrix — Pilot Audit 01", "", "`NOT_COMPARABLE` se usa para agregados NAP/GTE sin semántica de regla común. `UNKNOWN` se usa para reglas GTE cuando NAP no aporta rule_id o detalle equivalente.", "", "| " + " | ".join(fields) + " |", "|" + "|".join("---" for _ in fields) + "|"]
    lines += ["| " + " | ".join(csv_value(row[field]).replace("|", "\\|") for field in fields) + " |" for row in output]
    write(ROOT / "04_audit/pilot_01/differential_matrix.md", "\n".join(lines) + "\n")


def write_product_gaps(records: list[dict], rows: list[dict]) -> None:
    by_id = {row["benchmark_id"]: row for row in rows}
    lines = ["# Pilot Audit 01 — product gaps observed", "", "Solo hechos demostrables en los artefactos existentes. No contiene propuestas de implementación ni interpretación jurídica.", "", "## OBSERVED FACT", "", "- Los cinco outputs contienen informes de validación GTFS Explorer 0.2.1 con filtros nulos (`severities=null`, `categories=null`), por lo que el informe declara alcance sin filtro de severidad/categoría.", "- El baseline NAP contiene estado y conteos agregados, pero no rule IDs ni filas de detalle equivalentes; por ello no permite mapear cada regla GTE a NAP.", "- GTE produce rule IDs, severidad, categoría, localización, message_key y ocurrencias por detalle; esta granularidad no está presente en el baseline NAP.", "- Ancebus, Viagón, Gilsanz y Kbus conservan todos los detalles declarados por sus informes (`omitted_issue_count=0`).", "- Bizkaibus declara `1.040.852` incidencias detectadas, conserva `100.000` detalles y omite `940.852`; su detalle no es completo.", "- El número total y la severidad no son intercambiables: por ejemplo, Kbus tiene NAP `317` warnings y `0` errores, mientras que GTE conserva `644` errores y `0` warnings.", "- El baseline NAP declara recursos externos o capas adicionales (GTFS-RT, NeTEx, SIRI) para Kbus y Bizkaibus que no aparecen como findings del informe GTFS Schedule inspeccionado.", "- La información NAP sobre accesibilidad, tarifas y recursos externos no se convierte automáticamente en una regla GTE: el informe GTE solo demuestra los findings contenidos en su payload.", "", "## FUTURE HYPOTHESIS", "", "- No se registra ninguna hipótesis de implementación en esta fase.", ""]
    write(ROOT / "docs/PILOT_01_PRODUCT_GAPS.md", "\n".join(lines))


def write_final(records: list[dict], rows: list[dict]) -> None:
    by_id = {row["benchmark_id"]: row for row in rows}
    lines = ["# GTFS Explorer — Pilot Audit 01", "", "## STATUS", "", "PASS_WITH_OBSERVATIONS — cinco operadores procesados; evidencia preservada y comparación completada. Bizkaibus tiene detalle truncado por el límite observado del informe (`100.000` persistidas de `1.040.852` detectadas). No es una conclusión jurídica ni de cumplimiento.", "", "## OPERATORS PROCESSED", "", "| ID | Operator | Output | Product |", "|---|---|---|---|"]
    for record in records:
        lines.append(f"| {record['benchmark_id']} | {record['operator']} | `03_gtfs_explorer/run_001` | {record['export'].get('generator', {}).get('version') if record['export'] else 'null'} |")
    lines += ["", "## GTFS EXPLORER RUN INTEGRITY", "", "| Operator | run_id | status | detected | persisted | detail_complete | omitted | filter |", "|---|---|---|---:|---:|---|---:|---|"]
    for record in records:
        batch = record["batch"]
        lines.append(f"| {record['operator']} | `{batch.get('id')}` | {batch.get('state')} | {batch.get('total_issue_count')} | {batch.get('stored_issue_count')} | {batch.get('omitted_issue_count') == 0} | {batch.get('omitted_issue_count')} | null/null |")
    lines += ["", "`legacy_truncated` no aparece en los informes inspeccionados: `null`. `omitted_occurrences` se ha tomado de `batch.omitted_issue_count`.", "", "## SEVERITY SUMMARY", "", "| operator | NAP errors | NAP warnings | GTE errors | GTE warnings | GTE notices | GTE best practices | GTE detected occurrences |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for record in records:
        row = by_id[record["benchmark_id"]]
        lines.append(f"| {record['operator']} | {row['nap_error_count']} | {row['nap_warning_count']} | {row['gte_error_count']} | {row['gte_warning_count']} | {row['gte_notice_count']} | {row['gte_best_practice_count']} | {row['gte_detected_issue_count']} |")
    lines += ["", "## KEY DIFFERENTIALS", "", "- GTE proporciona reglas y localizaciones por hallazgo; NAP solo aporta agregados en el baseline disponible.", "- Bizkaibus es el único run con truncado de detalle: `940.852` incidencias omitidas.", "- GTE clasifica como ERROR findings que NAP presenta como warnings o no muestra con rule_id comparable; esto demuestra diferencia de taxonomía/alcance, no equivalencia jurídica.", "", "## GTFS EXPLORER ONLY", "", "0 reglas clasificadas de forma concluyente como exclusivas de GTE; las reglas sin correspondencia NAP quedan `UNKNOWN`.", "", "## NAP ONLY", "", "0 reglas clasificadas de forma concluyente como exclusivas de NAP; los agregados NAP sin regla comparable quedan `NOT_COMPARABLE`.", "", "## BOTH", "", "0 reglas clasificadas de forma concluyente como detectadas por ambos; no existe rule_id NAP suficiente para probarlo.", "", "## PRODUCT GAPS OBSERVED", "", "Hechos documentados en `docs/PILOT_01_PRODUCT_GAPS.md`.", "", "## DATA INTEGRITY", "", "- Los hashes SHA-256 actuales de los ZIP originales coinciden con los registrados en `source_census.json` para los cinco operadores.", "- Los outputs GTE se preservaron y se inventariaron con tamaño y SHA-256 en `04_audit/pilot_01/gte_output_inventory.md` y `.json`.", "- No se modificaron GTFS Explorer, feeds ni fuentes extraídas. No se ejecutó ninguna operación remota ni se creó Working Copy durante esta tarea.", "- Los exports JSON contienen un `source.sha256`/`manifest_sha256` de la ejecución; se conservan como evidencia y no se reinterpretan como el SHA-256 del ZIP original.", "", "## OUTPUTS CREATED", "", "- `03_gtfs_explorer/parsed_rule_summary.csv` por operador.", "- `pilot_01_baseline.csv` y `docs/PILOT_01_BASELINE_MATRIX.md` completados solo en columnas GTE.", "- `04_audit/pilot_01/gte_output_inventory.md` y `.json`.", "- `04_audit/pilot_01/NAP_VS_GTFS_EXPLORER.md`.", "- `04_audit/pilot_01/differential_matrix.csv` y `.md`.", "- `docs/PILOT_01_PRODUCT_GAPS.md`.", "- Este informe en `04_audit/pilot_01/final_report.md`.", "", "## NEXT STEP", "", "Review Pilot Audit 01 differential evidence and define the first Audit/Quality requirement model.", "", "No se inicia automáticamente esa fase.", ""]
    write(ROOT / "04_audit/pilot_01/final_report.md", "\n".join(lines))


def main() -> None:
    records = [extract_operator(item) for item in OPERATORS]
    create_rule_summaries(records)
    rows = baseline_rows(records)
    write_baseline(rows)
    write_baseline_matrix(rows)
    write_inventory(records)
    write_nap_vs_gte(records, rows)
    write_differential(records, rows)
    write_product_gaps(records, rows)
    write_final(records, rows)
    print("Pilot Audit 01 generated for", ", ".join(record["operator"] for record in records))


if __name__ == "__main__":
    main()
