from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator
from .core import RunContext, RuleResult

RULES = {
    "GTFS-STRUCT-REQUIRED": ("STRUCTURAL", "ERROR", "GTFS Schedule Reference; required tables"),
    "GTFS-STRUCT-SERVICE-CALENDAR": ("STRUCTURAL", "ERROR", "GTFS Schedule Reference; calendar.txt or calendar_dates.txt"),
    "GTFS-REF-TRIP-ROUTE": ("REFERENTIAL", "ERROR", "GTFS Schedule Reference; trips.route_id"),
    "GTFS-REF-SERVICE": ("REFERENTIAL", "ERROR", "GTFS Schedule Reference; trips.service_id"),
    "GTFS-REF-SHAPE": ("REFERENTIAL", "ERROR", "GTFS Schedule Reference; trips.shape_id (when supplied)"),
    "GTFS-UNIQUE-PRIMARY-ID": ("STRUCTURAL", "ERROR", "GTFS Schedule Reference primary IDs"),
    "GTFS-COORDINATE-RANGE": ("DATA_CONSISTENCY", "ERROR", "GTFS Schedule Reference latitude/longitude ranges"),
}

def _rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        for record_no, row in enumerate(reader, 2):
            yield record_no, row

def _finding(ctx: RunContext, rule: str, table: str, record: int | str, field: str | None, observed, expected: str, message: str) -> dict:
    return {"dataset_id": ctx.dataset.dataset_id, "rule_id": rule, "table": table, "row_locator": f"record:{record}", "field": field, "observed_value": observed, "expected_condition": expected, "technical_message": message, "evidence": {"source_sha256": ctx.dataset.source_sha256, "parser_version": ctx.dataset.parser_version}}

def _validate(ctx: RunContext) -> dict:
    findings: list[dict] = []
    checked: dict[str, int] = {}
    failed: set[str] = set()
    missing = [t for t, status in ctx.inventory.items() if t in {"agency", "stops", "routes", "trips", "stop_times"} and status != "PRESENT"]
    if missing:
        failed.add("GTFS-STRUCT-REQUIRED")
        for table in missing:
            findings.append(_finding(ctx, "GTFS-STRUCT-REQUIRED", table + ".txt", "file", None, "ABSENT", "file present", f"Falta tabla GTFS obligatoria {table}.txt"))
    if not any(table in ctx.tables for table in ("calendar", "calendar_dates")):
        failed.add("GTFS-STRUCT-SERVICE-CALENDAR")
        findings.append(_finding(ctx, "GTFS-STRUCT-SERVICE-CALENDAR", "calendar.txt/calendar_dates.txt", "file", None, "ABSENT", "at least one calendar table present", "No existe tabla de calendario para interpretar service_id"))
    # A failed ingest never reaches this engine. Do not turn absent optional parents into false orphans.
    ids: dict[str, set[str]] = {}
    for table, column in (("routes", "route_id"), ("trips", "trip_id"), ("stops", "stop_id"), ("agency", "agency_id")):
        path = ctx.tables.get(table)
        if not path: continue
        known: set[str] = set(); seen: set[str] = set(); checked[table] = 0
        for no, row in _rows(path):
            checked[table] += 1; value = row.get(column, "")
            if value and value in seen:
                failed.add("GTFS-UNIQUE-PRIMARY-ID")
                findings.append(_finding(ctx, "GTFS-UNIQUE-PRIMARY-ID", table + ".txt", no, column, value, "unique primary identifier", f"Identificador duplicado en {table}"))
            seen.add(value)
            if value: known.add(value)
        ids[table] = known
    services: set[str] = set()
    service_calendar_available = any(table in ctx.tables for table in ("calendar", "calendar_dates"))
    for table in ("calendar", "calendar_dates"):
        if table in ctx.tables:
            for _, row in _rows(ctx.tables[table]):
                if row.get("service_id"): services.add(row["service_id"])
    trips_path = ctx.tables.get("trips")
    if trips_path:
        checked["trips_references"] = 0
        for no, row in _rows(trips_path):
            checked["trips_references"] += 1
            for rule, field, target, label in (("GTFS-REF-TRIP-ROUTE", "route_id", ids.get("routes"), "route_id debe existir en routes.txt"), ("GTFS-REF-SERVICE", "service_id", services if service_calendar_available else None, "service_id debe existir en calendar.txt o calendar_dates.txt"), ("GTFS-REF-SHAPE", "shape_id", None, "shape_id debe existir en shapes.txt cuando se proporciona")):
                value = row.get(field, "")
                if rule == "GTFS-REF-SHAPE":
                    if value and "shapes" in ctx.tables:
                        if "shapes_ids" not in ids:
                            ids["shapes_ids"] = {r.get("shape_id", "") for _, r in _rows(ctx.tables["shapes"]) if r.get("shape_id")}
                        target = ids["shapes_ids"]
                    else: continue
                if target is None: continue
                if value not in target:
                    failed.add(rule); findings.append(_finding(ctx, rule, "trips.txt", no, field, value, label, "Referencia técnica sin registro padre"))
    for table, lat_col, lon_col in (("stops", "stop_lat", "stop_lon"), ("shapes", "shape_pt_lat", "shape_pt_lon")):
        if table not in ctx.tables: continue
        checked[table + "_coordinates"] = 0
        for no, row in _rows(ctx.tables[table]):
            checked[table + "_coordinates"] += 1
            try: lat, lon = float(row[lat_col]), float(row[lon_col])
            except (KeyError, TypeError, ValueError): lat, lon = float("nan"), float("nan")
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                failed.add("GTFS-COORDINATE-RANGE"); findings.append(_finding(ctx, "GTFS-COORDINATE-RANGE", table + ".txt", no, lat_col + "/" + lon_col, [row.get(lat_col), row.get(lon_col)], "latitude in [-90,90], longitude in [-180,180]", "Coordenadas ausentes, no numéricas o fuera de rango"))
    results = []
    for rule, (scope, severity, source) in RULES.items():
        fs = [x for x in findings if x["rule_id"] == rule]
        if rule == "GTFS-STRUCT-REQUIRED" and not missing: status = "PASS"
        elif rule in failed: status = "FAIL_TECHNICAL"
        elif rule in {"GTFS-REF-TRIP-ROUTE", "GTFS-REF-SHAPE"} and not trips_path: status = "NOT_EVALUABLE"
        elif rule == "GTFS-REF-SERVICE" and (not trips_path or not service_calendar_available): status = "NOT_EVALUABLE"
        elif rule == "GTFS-COORDINATE-RANGE" and not ("stops" in ctx.tables or "shapes" in ctx.tables): status = "NOT_EVALUABLE"
        else: status = "PASS"
        results.append({"rule_id": rule, "version": "1.0.0", "scope": scope, "severity": severity, "description": rule.replace("-", " "), "source_reference": source, "status": status, "checked_rows": checked.get("trips_references", 0) if rule.startswith("GTFS-REF") else checked.get("stops_coordinates", 0) + checked.get("shapes_coordinates", 0) if rule == "GTFS-COORDINATE-RANGE" else 0, "finding_count": len(fs), "findings": fs})
    return {"status": "FAIL_TECHNICAL" if findings else "PASS", "findings": findings, "rules": results, "checked_rows": checked, "finding_count": len(findings)}

def validate(ctx: RunContext) -> dict:
    try:
        return _validate(ctx)
    except Exception as exc:
        return {"status": "INSPECTION_ERROR", "findings": [], "rules": [{"rule_id": "GTFS-ENGINE-INSPECTION", "version": "1.0.0", "scope": "ENGINE", "severity": "ERROR", "description": "La inspección técnica no pudo completarse", "source_reference": "GTFS_Lab V1 run contract", "status": "INSPECTION_ERROR", "checked_rows": 0, "finding_count": 0, "findings": []}], "checked_rows": {}, "finding_count": 0, "errors": [f"{type(exc).__name__}: {exc}"]}
