from __future__ import annotations
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from .core import RunContext
from .validation import _rows

def analyze(ctx: RunContext) -> dict:
    names = {"agency": "agency", "routes": "route_id", "trips": "trip_id", "stops": "stop_id", "stop_times": "stop_time", "shapes": "shape_id", "calendar": "service_id", "calendar_dates": "service_id"}
    counts = {table: ctx.dataset.files.get(table + ".txt", {}).get("rows", 0) for table in names}
    route_ids: dict[str, set[str]] = defaultdict(set); route_counts: dict[str, int] = defaultdict(int); service_counts: dict[str, int] = defaultdict(int)
    route_names = {}
    if "routes" in ctx.tables:
        route_names = {r.get("route_id", ""): r.get("route_short_name") or r.get("route_long_name") or r.get("route_id") for _, r in _rows(ctx.tables["routes"])}
    trip_routes = {}
    if "trips" in ctx.tables:
        for _, row in _rows(ctx.tables["trips"]):
            trip_routes[row.get("trip_id", "")] = row.get("route_id", "")
            service_counts[row.get("service_id", "")] += 1
    if "stop_times" in ctx.tables:
        for _, row in _rows(ctx.tables["stop_times"]):
            route = trip_routes.get(row.get("trip_id", ""), "")
            stop = row.get("stop_id", "")
            if route and stop:
                route_ids[route].add(stop); route_counts[route] += 1
    route_stop_matrix = [{"route_id": route, "route_name": route_names.get(route, route), "unique_stops": len(stops), "stop_time_rows": route_counts.get(route, 0), "stop_ids": sorted(stops)} for route, stops in sorted(route_ids.items())]
    shared = defaultdict(list)
    for row in route_stop_matrix:
        for stop in row["stop_ids"]: shared[stop].append(row["route_id"])
    shared_stops = [{"stop_id": stop, "route_ids": routes} for stop, routes in sorted(shared.items()) if len(routes) > 1]
    return {"dataset_id": ctx.dataset.dataset_id, "counts": counts, "agencies": _id_list(ctx, "agency", "agency_id"), "routes": [{"route_id": r, "name": n} for r, n in sorted(route_names.items())], "services": {"trip_count_by_service_id": dict(sorted(service_counts.items()))}, "service_calendar_summary": _service_calendar(ctx), "shapes": _id_list(ctx, "shapes", "shape_id", cap=5000), "route_stop_matrix": route_stop_matrix, "shared_stops": shared_stops, "limitations": ["Fechas calculadas solo con los archivos de calendario presentes; date span se devuelve como fechas ISO.", "Route-stop matrix se basa en stop_times.stop_id y excluye entidades flex fuera de ese campo."]}

def _service_calendar(ctx: RunContext) -> dict:
    dates: dict[str, set[str]] = defaultdict(set)
    malformed_rows = 0
    if "calendar" not in ctx.tables and "calendar_dates" not in ctx.tables:
        return {"status": "NOT_EVALUABLE", "active_dates_by_service_id": {}, "malformed_rows": 0}
    if "calendar" in ctx.tables:
        weekdays = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        for _, row in _rows(ctx.tables["calendar"]):
            try:
                current = datetime.strptime(row["start_date"], "%Y%m%d").date()
                end = datetime.strptime(row["end_date"], "%Y%m%d").date()
                if end < current: raise ValueError("end_date before start_date")
                if (end - current).days > 18_262: raise ValueError("calendar span exceeds 50 years")
                service = row["service_id"]
                while current <= end:
                    if row.get(weekdays[current.weekday()]) == "1": dates[service].add(current.isoformat())
                    current += timedelta(days=1)
            except (KeyError, ValueError, OverflowError):
                malformed_rows += 1
    if "calendar_dates" in ctx.tables:
        for _, row in _rows(ctx.tables["calendar_dates"]):
            try:
                date = datetime.strptime(row["date"], "%Y%m%d").date().isoformat()
                service, exception = row["service_id"], row["exception_type"]
                if exception == "1": dates[service].add(date)
                elif exception == "2": dates[service].discard(date)
                else: malformed_rows += 1
            except (KeyError, ValueError):
                malformed_rows += 1
    return {"status": "PASS" if malformed_rows == 0 else "PARTIAL", "active_dates_by_service_id": {service: sorted(values) for service, values in sorted(dates.items())}, "malformed_rows": malformed_rows}

def _id_list(ctx: RunContext, table: str, field: str, cap: int | None = None) -> list[str]:
    if table not in ctx.tables: return []
    vals = set()
    for _, row in _rows(ctx.tables[table]):
        if row.get(field): vals.add(row[field])
    result = sorted(vals)
    return result[:cap] if cap else result
