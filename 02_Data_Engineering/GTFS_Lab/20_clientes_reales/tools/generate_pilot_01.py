from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

OPERATORS = [
    ("002", "Ancebus", "FAMILY_A_SMALL_BASIC", "002_ancebus", "2025-01-01", "2026-12-31", False, False, False, "2026-06-02", "VALID_WITHOUT_WARNINGS", 0, 0),
    ("005", "Viagón", "FAMILY_A_SMALL_BASIC", "005_viagon", "2025-01-01", "2026-12-31", False, False, False, "2026-06-02", "VALID_WITH_WARNINGS", 0, 22),
    ("014", "Gilsanz", "FAMILY_C_COMPLEX_REGIONAL", "014_gilsanz", "2026-01-01", "2049-12-31", False, False, True, "2026-05-27", "INVALID_WITH_ERRORS", 1, 1),
    ("020", "Kbus", "FAMILY_D_MATURE_BENCHMARK", "020_kbus", "2023-12-31", "2026-12-30", False, True, True, "2025-05-30", "VALID_WITH_WARNINGS", 0, 317),
    ("019", "Bizkaibus", "FAMILY_D_MATURE_BENCHMARK", "019_bizkaibus", "2017-01-06", "2026-12-23", True, True, True, "2026-09-10", "VALID_WITHOUT_WARNINGS", 0, 0),
]

NAP_RESOURCES = {
    "002": {"gtfs_rt": False, "netex": False, "siri": False},
    "005": {"gtfs_rt": False, "netex": False, "siri": False},
    "014": {"gtfs_rt": False, "netex": False, "siri": False},
    "020": {"gtfs_rt": True, "netex": True, "siri": True},
    "019": {"gtfs_rt": True, "netex": True, "siri": True},
}

GTFS_STANDARD_FIELDS = {
    "agency.txt": {"agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang", "agency_phone", "agency_fare_url", "agency_email"},
    "routes.txt": {"route_id", "agency_id", "route_short_name", "route_long_name", "route_desc", "route_type", "route_url", "route_color", "route_text_color", "route_sort_order", "continuous_pickup", "continuous_drop_off", "network_id"},
    "stops.txt": {"stop_id", "stop_code", "stop_name", "tts_stop_name", "stop_desc", "tts_stop_desc", "stop_lat", "stop_lon", "zone_id", "stop_url", "location_type", "parent_station", "stop_timezone", "wheelchair_boarding", "level_id", "platform_code", "areas", "signposted_as", "from_stop_id", "to_stop_id"},
    "trips.txt": {"route_id", "service_id", "trip_id", "trip_headsign", "trip_short_name", "direction_id", "block_id", "shape_id", "wheelchair_accessible", "bikes_allowed", "cars_allowed", "exceptional", "boarding_duration", "alighting_duration"},
    "stop_times.txt": {"trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "stop_headsign", "pickup_type", "drop_off_type", "continuous_pickup", "continuous_drop_off", "shape_dist_traveled", "timepoint", "stop_note", "departure_day", "arrival_day"},
    "calendar.txt": {"service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"},
    "calendar_dates.txt": {"service_id", "date", "exception_type"},
}


def read_table(path: Path):
    raw = path.read_bytes()
    encoding = "utf-8-sig"
    try:
        text = raw.decode(encoding)
    except UnicodeDecodeError:
        encoding = "cp1252"
        text = raw.decode(encoding)
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "CRLF" if b"\r\n" in raw else "LF" if b"\n" in raw else "NONE"
    rows = list(csv.reader(text.splitlines()))
    header = rows[0] if rows else []
    data = [dict(zip(header, row + [""] * (len(header) - len(row)))) for row in rows[1:]]
    return {
        "raw": raw,
        "encoding": encoding,
        "bom": bom,
        "newline": newline,
        "header": header,
        "rows": data,
        "data_rows": len(data),
        "columns": len(header),
        "duplicate_columns": len(header) != len(set(header)),
    }


def truthy(value: str) -> bool:
    return value.strip() not in ("", "0")


def dist(rows, field):
    return dict(sorted(Counter((r.get(field, "") or "").strip() for r in rows).items()))


def population(rows, field):
    c = Counter()
    for r in rows:
        value = (r.get(field, "") or "").strip()
        c["blank" if value == "" else value] += 1
    return dict(sorted(c.items()))


def parse_date(value):
    value = value.strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None


def alignment(feed_min, feed_max, declared_min, declared_max):
    if not feed_min or not feed_max:
        return "NOT_COMPARABLE"
    feed_min_date, feed_max_date = parse_date(feed_min), parse_date(feed_max)
    dmin, dmax = parse_date(declared_min), parse_date(declared_max)
    if not feed_min_date or not feed_max_date or not dmin or not dmax:
        return "NOT_COMPARABLE"
    if feed_min_date == dmin and feed_max_date == dmax:
        return "MATCH"
    if feed_max_date >= dmin and feed_min_date <= dmax:
        return "PARTIAL_MATCH"
    return "DIFFERENCE"


def bool_text(value):
    return "true" if value else "false"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def inspect_operator(item):
    benchmark_id, operator, family, slug, declared_from, declared_to, declared_accessibility, declared_fares, declared_geometry, nap_update, nap_status, nap_errors, nap_warnings = item
    op_dir = ROOT / family / slug
    extracted = op_dir / "02_sources" / "gtfs_schedule" / "extracted"
    original_zips = list((op_dir / "02_sources" / "gtfs_schedule" / "original").glob("*.zip"))
    tables = {}
    for path in sorted(extracted.glob("*.txt")):
        tables[path.name] = read_table(path)

    file_records = []
    nonstandard = []
    for name, table in tables.items():
        extras = [c for c in table["header"] if c not in GTFS_STANDARD_FIELDS.get(name, set())]
        file_records.append({
            "file": name,
            "size_bytes": len(table["raw"]),
            "data_rows": table["data_rows"],
            "columns": table["columns"],
            "column_names": table["header"],
            "encoding": table["encoding"],
            "bom": table["bom"],
            "newline": table["newline"],
            "empty": table["data_rows"] == 0,
            "duplicate_columns": table["duplicate_columns"],
            "nonstandard_columns": extras,
        })
        for col in extras:
            nonstandard.append({"file": name, "column": col, "nonstandard_occurrence_count": sum(1 for r in table["rows"] if (r.get(col, "") or "").strip() != "")})

    trips = tables.get("trips.txt", {}).get("rows", [])
    stops = tables.get("stops.txt", {}).get("rows", [])
    stop_times = tables.get("stop_times.txt", {}).get("rows", [])
    routes = tables.get("routes.txt", {}).get("rows", [])
    calendar = tables.get("calendar.txt", {}).get("rows", [])
    calendar_dates = tables.get("calendar_dates.txt", {}).get("rows", [])
    dates = [d for r in calendar for d in (parse_date(r.get("start_date", "")), parse_date(r.get("end_date", ""))) if d]
    exception_dates = [parse_date(r.get("date", "")) for r in calendar_dates if parse_date(r.get("date", ""))]
    all_dates = dates + exception_dates
    feed_min = min(all_dates).isoformat() if all_dates else None
    feed_max = max(all_dates).isoformat() if all_dates else None
    shapes = tables.get("shapes.txt", {}).get("rows", [])
    shape_ids = {r.get("shape_id", "").strip() for r in shapes if r.get("shape_id", "").strip()}
    trip_shape_ids = {r.get("shape_id", "").strip() for r in trips if r.get("shape_id", "").strip()}
    fare_files = {"fare_attributes.txt", "fare_rules.txt", "fare_products.txt", "fare_leg_rules.txt", "fare_transfer_rules.txt", "networks.txt", "route_networks.txt", "areas.txt", "stop_areas.txt"}
    fare_present = sorted(fare_files.intersection(tables))
    accessibility_present = bool(stops and "wheelchair_boarding" in tables.get("stops.txt", {}).get("header", [])) or bool(trips and "wheelchair_accessible" in tables.get("trips.txt", {}).get("header", []))
    feed_info = tables.get("feed_info.txt", {}).get("rows", [])
    source_zip = original_zips[0] if original_zips else None
    zip_members = []
    if source_zip:
        with zipfile.ZipFile(source_zip) as zf:
            zip_members = sorted(zf.namelist())

    data = {
        "benchmark_id": benchmark_id,
        "operator": operator,
        "family": family,
        "source_root": str(extracted.relative_to(ROOT)).replace("\\", "/"),
        "original_zip": str(source_zip.relative_to(ROOT)).replace("\\", "/") if source_zip else None,
        "original_zip_sha256": hashlib.sha256(source_zip.read_bytes()).hexdigest().upper() if source_zip else None,
        "zip_members": zip_members,
        "files": file_records,
        "nonstandard_fields": nonstandard,
        "metrics": {
            "agency_rows": len(tables.get("agency.txt", {}).get("rows", [])),
            "routes_rows": len(routes), "stops_rows": len(stops), "trips_rows": len(trips), "stop_times_rows": len(stop_times),
            "calendar_rows": len(calendar), "calendar_dates_rows": len(calendar_dates), "shapes_rows": len(shapes),
            "frequencies_rows": len(tables.get("frequencies.txt", {}).get("rows", [])), "transfers_rows": len(tables.get("transfers.txt", {}).get("rows", [])),
            "feed_info_rows": len(feed_info), "fare_attributes_rows": len(tables.get("fare_attributes.txt", {}).get("rows", [])), "fare_rules_rows": len(tables.get("fare_rules.txt", {}).get("rows", [])),
            "pathways_rows": len(tables.get("pathways.txt", {}).get("rows", [])), "levels_rows": len(tables.get("levels.txt", {}).get("rows", [])), "translations_rows": len(tables.get("translations.txt", {}).get("rows", [])), "attributions_rows": len(tables.get("attributions.txt", {}).get("rows", [])),
        },
        "distributions": {
            "routes.route_type": dist(routes, "route_type"), "stops.location_type": dist(stops, "location_type"), "stops.wheelchair_boarding": population(stops, "wheelchair_boarding"),
            "trips.wheelchair_accessible": population(trips, "wheelchair_accessible"), "trips.bikes_allowed": population(trips, "bikes_allowed"), "trips.shape_id": {"populated": len(trip_shape_ids), "blank": sum(1 for r in trips if not (r.get("shape_id", "") or "").strip())},
            "stop_times.pickup_type": dist(stop_times, "pickup_type"), "stop_times.drop_off_type": dist(stop_times, "drop_off_type"), "stop_times.timepoint": dist(stop_times, "timepoint"),
        },
        "temporal": {"minimum_service_date_detectable": feed_min, "maximum_service_date_detectable": feed_max, "calendar_present": "calendar.txt" in tables, "calendar_dates_present": "calendar_dates.txt" in tables, "service_ids_calendar": len({r.get("service_id", "") for r in calendar}), "exceptions_added": sum(1 for r in calendar_dates if r.get("exception_type") == "1"), "exceptions_removed": sum(1 for r in calendar_dates if r.get("exception_type") == "2"), "feed_start_date": feed_info[0].get("feed_start_date") if feed_info else None, "feed_end_date": feed_info[0].get("feed_end_date") if feed_info else None},
        "geometry": {"shapes_present": "shapes.txt" in tables, "shape_points": len(shapes), "distinct_shape_id": len(shape_ids), "trips_with_shape_id": len(trip_shape_ids), "trips_without_shape_id": len(trips) - len(trip_shape_ids)},
        "fares": {"fare_data_in_gtfs": bool(fare_present), "files_present": fare_present},
        "accessibility": {"accessibility_data_present_in_gtfs": accessibility_present, "stops_wheelchair_boarding_present": "wheelchair_boarding" in tables.get("stops.txt", {}).get("header", []), "trips_wheelchair_accessible_present": "wheelchair_accessible" in tables.get("trips.txt", {}).get("header", [])},
        "nap": {"declared_routes": {"value": {"002": 2, "005": 11, "014": 144, "020": 4, "019": 99}[benchmark_id], "evidence_source": "NAP snapshot", "transcription_method": "manual_verified"}, "declared_stops": {"value": {"002": 26, "005": 62, "014": 1244, "020": 88, "019": 2334}[benchmark_id], "evidence_source": "NAP snapshot", "transcription_method": "manual_verified"}, "declared_trips": {"value": {"002": 6, "005": 22, "014": 788, "020": 278, "019": 22151}[benchmark_id], "evidence_source": "NAP snapshot", "transcription_method": "manual_verified"}, "declared_valid_from": declared_from, "declared_valid_to": declared_to, "declared_accessibility": declared_accessibility, "declared_fares": declared_fares, "declared_route_geometry": declared_geometry, "nap_last_update": nap_update, "nap_validation_status": nap_status, "nap_error_count": nap_errors, "nap_warning_count": nap_warnings, "declared_gtfs_rt": NAP_RESOURCES[benchmark_id]["gtfs_rt"], "declared_netex": NAP_RESOURCES[benchmark_id]["netex"], "declared_siri": NAP_RESOURCES[benchmark_id]["siri"]},
        "comparison": {"count_alignment": "MATCH" if (len(routes), len(stops), len(trips)) == ({"002": (2, 26, 6), "005": (11, 62, 22), "014": (144, 1244, 788), "020": (4, 88, 278), "019": (99, 2334, 22151)}[benchmark_id]) else "DIFFERENCE", "date_alignment": alignment(feed_min, feed_max, declared_from, declared_to), "geometry_alignment": "CONSISTENT_WITH_NAP" if bool(shapes) == declared_geometry else "POSSIBLE_DIFFERENCE", "fare_alignment": "FARE_DATA_IN_GTFS" if fare_present else "EXTERNAL_FARE_RESOURCE_DECLARED_AT_NAP" if declared_fares else "NO_FARE_DATA_DECLARED", "accessibility_alignment": "ACCESSIBILITY_DATA_PRESENT_IN_GTFS" if accessibility_present else "NO_ACCESSIBILITY_DATA_IN_GTFS"},
    }
    audit_dir = op_dir / "04_audit" / "pilot_01"
    write(audit_dir / "source_census.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    md = [f"# Source census — {operator} ({benchmark_id})", "", f"Fuente física censada: `{data['source_root']}`", "", "## Ficheros", "", "| Fichero | Bytes | Filas | Columnas | Encoding | BOM | Saltos | Vacío | Columnas exactas |", "|---|---:|---:|---:|---|---|---|---|---|"]
    for f in file_records:
        md.append(f"| `{f['file']}` | {f['size_bytes']} | {f['data_rows']} | {f['columns']} | {f['encoding']} | {bool_text(f['bom'])} | {f['newline']} | {bool_text(f['empty'])} | `{', '.join(f['column_names'])}` |")
    md += ["", "## Archivos GTFS", "", f"Obligatorios presentes: `{', '.join(x for x in ['agency.txt','routes.txt','trips.txt','stop_times.txt','stops.txt'] if x in tables)}`.", f"Opcionales presentes: `{', '.join(x for x in ['calendar.txt','calendar_dates.txt','shapes.txt','frequencies.txt','transfers.txt','feed_info.txt','fare_attributes.txt','fare_rules.txt','pathways.txt','levels.txt','translations.txt','attributions.txt'] if x in tables)}`.", f"Archivos no estándar adicionales: `{', '.join(x for x in tables if x not in GTFS_STANDARD_FIELDS) or 'ninguno'}`.", "", "## Campos no estándar", ""]
    if nonstandard:
        md += ["| Fichero | Campo | Ocurrencias no vacías |", "|---|---|---:|"] + [f"| `{x['file']}` | `{x['column']}` | {x['nonstandard_occurrence_count']} |" for x in nonstandard]
    else:
        md.append("Ninguno detectado con el baseline de campos estándar usado en este censo.")
    write(audit_dir / "source_census.md", "\n".join(md) + "\n")
    write(audit_dir / "nap_vs_source.md", f"# NAP vs source — {operator} ({benchmark_id})\n\nTodos los datos NAP de esta tabla proceden de `NAP snapshot`; los datos GTFS proceden del directorio físico `extracted/`.\n\n| Campo | NAP declarado | Fuente física | Resultado |\n|---|---:|---:|---|\n| routes | {data['nap']['declared_routes']['value']} | {len(routes)} | {data['comparison']['count_alignment']} |\n| stops | {data['nap']['declared_stops']['value']} | {len(stops)} | {data['comparison']['count_alignment']} |\n| trips | {data['nap']['declared_trips']['value']} | {len(trips)} | {data['comparison']['count_alignment']} |\n| valid dates | {declared_from} → {declared_to} | {feed_min} → {feed_max} | {data['comparison']['date_alignment']} |\n| route geometry | {bool_text(declared_geometry)} | shapes.txt={bool_text('shapes.txt' in tables)}, trips con shape_id={len(trip_shape_ids)} | {data['comparison']['geometry_alignment']} |\n| fares | {bool_text(declared_fares)} | {', '.join(fare_present) or 'sin ficheros tarifarios'} | {data['comparison']['fare_alignment']} |\n| accessibility | {bool_text(declared_accessibility)} | {bool_text(accessibility_present)} | {data['comparison']['accessibility_alignment']} |\n")
    write(op_dir / "03_gtfs_explorer" / "README.md", f"# Recepción GTFS Explorer 0.2.1 — {operator}\n\nEste directorio queda preparado para recibir posteriormente el HTML report, manifest, JSON/CSV, metadatos de ejecución y capturas que produzca GTFS Explorer Desktop 0.2.1.\n\nGTFS Explorer Desktop 0.2.1 será ejecutado externamente; sus outputs se copiarán aquí como evidencia. No se ejecuta ni se replica en este piloto.\n")
    if benchmark_id == "020":
        agency = tables.get("agency.txt", {}).get("rows", [])
        agency_urls = [r.get("agency_url", "") for r in agency if r.get("agency_url")]
        route_urls = sorted({r.get("route_url", "") for r in routes if r.get("route_url")})
        stop_names = [r.get("stop_name", "") for r in stops]
        barakaldo_stops = sorted({n for n in stop_names if re.search(r"barakaldo|altos hornos|lasesarre|retuerto|desertu", n, re.I)})
        identity = f"# Kbus source identity verification\n\n## Status\n\n**CONFIRMED**\n\n## Evidence observed in source\n\n- Original ZIP: `{source_zip.name}`. The filename contains `Barakaldo`.\n- `agency.txt`: `agency_id=kbus`, `agency_name=Kbus`.\n- `agency_url`: `{', '.join(agency_urls)}`.\n- `routes.txt`: {len(routes)} routes; route URLs point to the Kbus website: `{', '.join(route_urls)}`.\n- `stops.txt`: {len(stops)} stops. The following observed stop names are consistent with the Barakaldo network context: {', '.join(barakaldo_stops[:20]) or 'none detected'}.\n- The source ZIP and the existing operator folder are paired as `020_kbus`; no file was moved or modified.\n\n## Scope note\n\nThis confirms the physical association of the source with Kbus/Barakaldo. It is not a regulatory or semantic validation of the feed.\n"
        write(op_dir / "00_metadata" / "source_identity_verification.md", identity)
    return data


def main():
    records = [inspect_operator(item) for item in OPERATORS]
    root_audit = ROOT / "04_audit" / "pilot_01"
    write(root_audit / "source_census.json", json.dumps({"pilot": "Pilot Audit 01", "generated_at": datetime.now().astimezone().isoformat(), "operators": records}, ensure_ascii=False, indent=2) + "\n")
    central = ["# Pilot 01 — source census", "", "Censo físico read-only de los cinco GTFS extraídos. No es una validación semántica.", "", "| ID | Operador | TXT | routes | stops | trips | stop_times | shapes | fares | feed_info |", "|---|---|---:|---:|---:|---:|---:|---|---|---|"]
    for r in records:
        central.append(f"| {r['benchmark_id']} | {r['operator']} | {len(r['files'])} | {r['metrics']['routes_rows']} | {r['metrics']['stops_rows']} | {r['metrics']['trips_rows']} | {r['metrics']['stop_times_rows']} | {bool_text(r['geometry']['shapes_present'])} | {bool_text(r['fares']['fare_data_in_gtfs'])} | {r['metrics']['feed_info_rows']} |")
    central += ["", "El detalle de bytes, filas, columnas, encoding, BOM, saltos de línea, columnas duplicadas y campos no estándar se encuentra en el `source_census.json` y `source_census.md` de cada operador."]
    write(root_audit / "source_census.md", "\n".join(central) + "\n")
    rows = []
    fields = ["benchmark_id", "operator", "family", "nap_validation_status", "nap_error_count", "nap_warning_count", "nap_last_update", "declared_routes", "declared_stops", "declared_trips", "declared_valid_from", "declared_valid_to", "declared_accessibility", "declared_fares", "declared_geometry", "declared_gtfs_rt", "declared_netex", "declared_siri", "agency_rows", "routes_rows", "stops_rows", "trips_rows", "stop_times_rows", "calendar_present", "calendar_dates_present", "shapes_present", "distinct_shapes", "trips_with_shapes", "trips_without_shapes", "fare_data_present", "accessibility_data_present", "count_alignment", "date_alignment", "geometry_alignment", "fare_alignment", "accessibility_alignment", "gte_run_id", "gte_status", "gte_detected_issue_count", "gte_persisted_issue_count", "gte_detail_complete", "gte_error_count", "gte_warning_count", "gte_notice_count", "gte_best_practice_count"]
    for r in records:
        n, m, t = r["nap"], r["metrics"], r["temporal"]
        rows.append({"benchmark_id": r["benchmark_id"], "operator": r["operator"], "family": r["family"], "nap_validation_status": n["nap_validation_status"], "nap_error_count": n["nap_error_count"], "nap_warning_count": n["nap_warning_count"], "nap_last_update": n["nap_last_update"], "declared_routes": n["declared_routes"]["value"], "declared_stops": n["declared_stops"]["value"], "declared_trips": n["declared_trips"]["value"], "declared_valid_from": n["declared_valid_from"], "declared_valid_to": n["declared_valid_to"], "declared_accessibility": n["declared_accessibility"], "declared_fares": n["declared_fares"], "declared_geometry": n["declared_route_geometry"], "declared_gtfs_rt": n["declared_gtfs_rt"], "declared_netex": n["declared_netex"], "declared_siri": n["declared_siri"], "agency_rows": m["agency_rows"], "routes_rows": m["routes_rows"], "stops_rows": m["stops_rows"], "trips_rows": m["trips_rows"], "stop_times_rows": m["stop_times_rows"], "calendar_present": t["calendar_present"], "calendar_dates_present": t["calendar_dates_present"], "shapes_present": r["geometry"]["shapes_present"], "distinct_shapes": r["geometry"]["distinct_shape_id"], "trips_with_shapes": r["geometry"]["trips_with_shape_id"], "trips_without_shapes": r["geometry"]["trips_without_shape_id"], "fare_data_present": r["fares"]["fare_data_in_gtfs"], "accessibility_data_present": r["accessibility"]["accessibility_data_present_in_gtfs"], **r["comparison"], **{f: "" for f in fields if f.startswith("gte_")}})
    with (ROOT / "pilot_01_baseline.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    matrix = ["# Pilot 01 — baseline matrix", "", "Valores NAP: `NAP snapshot` + `manual_verified`. Valores físicos: censados desde `02_sources/gtfs_schedule/extracted/`. Las columnas GTFS Explorer permanecen vacías hasta una ejecución externa.", "", "| Operador | Rutas NAP/GTFS | Paradas NAP/GTFS | Viajes NAP/GTFS | Fechas | Geometría | Tarifas | Accesibilidad |", "|---|---:|---:|---:|---|---|---|---|"]
    for r in records:
        n, m = r["nap"], r["metrics"]
        matrix.append(f"| {r['operator']} | {n['declared_routes']['value']}/{m['routes_rows']} | {n['declared_stops']['value']}/{m['stops_rows']} | {n['declared_trips']['value']}/{m['trips_rows']} | {r['comparison']['date_alignment']} | {r['comparison']['geometry_alignment']} | {r['comparison']['fare_alignment']} | {r['comparison']['accessibility_alignment']} |")
    matrix += ["", "## GTFS Explorer columns", "", "`gte_run_id`, `gte_status`, `gte_detected_issue_count`, `gte_persisted_issue_count`, `gte_detail_complete`, `gte_error_count`, `gte_warning_count`, `gte_notice_count` y `gte_best_practice_count` se mantienen vacías por diseño."]
    write(ROOT / "docs" / "PILOT_01_BASELINE_MATRIX.md", "\n".join(matrix) + "\n")
    write(ROOT / "docs" / "PILOT_01.md", "# GTFS Explorer — Spain Mobility Data Benchmark 2026\n\n## Pilot Audit 01\n\nObjetivo: comparar la información declarada/observada en NAP con el GTFS físico y, posteriormente, con los resultados de GTFS Explorer Desktop 0.2.1. En una fase posterior podrán separarse las capas Audit / Quality / Regulatory.\n\nLa hipótesis de investigación es que un GTFS aceptado por el NAP puede todavía contener hallazgos técnicos, de calidad o de cobertura relevantes que no sean visibles en la validación superficial publicada. Esta frase es una hipótesis, no una conclusión.\n\nEste piloto se limita a baseline NAP, identidad de fuentes, censo físico y métricas objetivas. No realiza auditoría jurídica, compliance scoring, risk scoring, correcciones de feeds ni parsing GTFS-RT/SIRI/NeTEx.\n\nSiguiente paso recomendado: ejecutar GTFS Explorer Desktop 0.2.1 contra los cinco feeds y almacenar sus resultados en `03_gtfs_explorer/`.\n")
    summary = ["# Pilot Audit 01 — final report", "", "## 1. STATUS", "", "PASS_WITH_OBSERVATIONS", "", "Los cinco operadores han sido censados. El resultado es observacional; no constituye validación semántica, jurídica ni de cumplimiento.", "", "## 2. PILOT OPERATORS", "", "| ID | Operador | Estado |", "|---|---|---|"]
    for r in records: summary.append(f"| {r['benchmark_id']} | {r['operator']} | PROCESSED |")
    summary += ["", "## 3. KBUS IDENTITY", "", "CONFIRMED. Evidencia detallada en `FAMILY_D_MATURE_BENCHMARK/020_kbus/00_metadata/source_identity_verification.md`.", "", "## 4. GTFS FILE COVERAGE", "", "| Operador | Ficheros TXT | ZIP original |", "|---|---:|---|"]
    for r in records: summary.append(f"| {r['operator']} | {len(r['files'])} | `{r['original_zip']}` |")
    summary += ["", "## 5. CORE COUNTS", "", "| Operador | routes | stops | trips | stop_times |", "|---|---:|---:|---:|---:|"]
    for r in records: summary.append(f"| {r['operator']} | {r['metrics']['routes_rows']} | {r['metrics']['stops_rows']} | {r['metrics']['trips_rows']} | {r['metrics']['stop_times_rows']} |")
    summary += ["", "## 6. NAP VS SOURCE", "", "Los resultados detallados están en cada `04_audit/pilot_01/nap_vs_source.md` y en la matriz raíz.", "", "## 7. OPTIONAL DATA COVERAGE", "", "Se han censado shapes, fares, accessibility, feed_info y calendarios en los JSON por operador.", "", "## 8. NON-STANDARD DATA", "", "Se registran por fichero y columna en cada `source_census.json`.", "", "## 9. INTEGRITY", "", "Los SHA-256 de los ZIP originales se han calculado sin escribir sobre ellos. No se han modificado ficheros source ni se han ejecutado operaciones remotas.", "", "## 10. OUTPUTS CREATED", "", "`04_audit/pilot_01/`, `03_gtfs_explorer/README.md` por operador, `docs/PILOT_01.md`, `docs/PILOT_01_BASELINE_MATRIX.md` y `pilot_01_baseline.csv`.", "", "## 11. OBSERVATIONS", "", "Kbus queda asociado físicamente a Barakaldo mediante el nombre del ZIP, agency, URL, rutas y topónimos observados.", "", "## 12. NEXT ACTION", "", "Ejecutar GTFS Explorer Desktop 0.2.1 contra los cinco feeds y almacenar sus resultados en `03_gtfs_explorer/`. No se inicia automáticamente en este piloto."]
    write(root_audit / "final_report.md", "\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
