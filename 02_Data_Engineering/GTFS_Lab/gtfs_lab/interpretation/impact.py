"""Evidence-bounded GTFS relationship propagation."""
from __future__ import annotations

import csv
import zipfile
from collections import defaultdict
from typing import Any

ENTITY_FILES = {"agency": "agency.txt", "route": "routes.txt", "trip": "trips.txt",
                "stop": "stops.txt", "shape": "shapes.txt", "stop_time": "stop_times.txt",
                "calendar": "calendar.txt", "calendar_date": "calendar_dates.txt",
                "frequency": "frequencies.txt"}


def load_population_and_relationships(zip_path: str) -> tuple[dict[str, int | None], dict[str, dict[str, set[str]]]]:
    populations: dict[str, int | None] = {}
    relationships: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    with zipfile.ZipFile(zip_path) as archive:
        names = {name.rsplit("/", 1)[-1]: name for name in archive.namelist() if not name.endswith("/")}
        for entity, filename in ENTITY_FILES.items():
            member = names.get(filename)
            if member is None:
                populations[entity] = None
                continue
            count = 0
            population_ids: set[str] = set()
            with archive.open(member) as raw:
                import io
                text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
                reader = csv.DictReader(text)
                for row in reader:
                    count += 1
                    key = {"route": "route_id", "trip": "trip_id", "service": "service_id",
                           "shape": "shape_id", "stop": "stop_id", "stop_time": "stop_id",
                           "calendar": "service_id", "calendar_date": "service_id",
                           "frequency": "trip_id", "agency": "agency_id"}.get(entity)
                    if key and row.get(key):
                        population_ids.add(row[key])
                        relationships[entity][row[key]].add(row[key])
                        if filename in {"calendar.txt", "calendar_dates.txt"}:
                            relationships["service"][row[key]].add(row[key])
                    if filename == "trips.txt":
                        trip = row.get("trip_id", "")
                        for field, target in (("route_id", "route"), ("service_id", "service"), ("shape_id", "shape")):
                            if trip and row.get(field):
                                relationships["trip"][trip].add(target + ":" + row[field])
                                relationships[target][row[field]].add("trip:" + trip)
                        if row.get("service_id"):
                            relationships["service"][row["service_id"]].add("trip:" + trip)
                    elif filename == "stop_times.txt":
                        trip, stop = row.get("trip_id", ""), row.get("stop_id", "")
                        if trip and stop:
                            relationships["stop"][stop].add("trip:" + trip)
                            relationships["trip"][trip].add("stop:" + stop)
                            stop_time_id = trip + ":" + str(row.get("stop_sequence", count))
                            relationships["stop_time"][stop_time_id].add("trip:" + trip)
            populations[entity] = count if entity == "stop_time" else len(population_ids)
        trip_services = relationships.get("service", {})
        if trip_services:
            populations["service"] = sum(1 for service, values in trip_services.items() if service in values)
    return populations, relationships


def propagated_counts(entity_type: str, entity_ids: set[str], relationships: dict[str, dict[str, set[str]]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    def known(kind: str, value: str) -> bool:
        return value in relationships.get(kind, {}).get(value, set())
    if entity_type == "shape":
        for shape in entity_ids:
            for item in relationships.get("shape", {}).get(shape, set()):
                if item.startswith("trip:"):
                    trip = item[5:]
                    if not known("trip", trip):
                        continue
                    result["trip"].add(trip)
                    for related in relationships.get("trip", {}).get(trip, set()):
                        kind, _, value = related.partition(":")
                        if kind in {"route", "service"} and value and known(kind, value):
                            result[kind].add(value)
    elif entity_type == "trip":
        for trip in entity_ids:
            for item in relationships.get("trip", {}).get(trip, set()):
                kind, _, value = item.partition(":")
                if kind in {"route", "service", "shape", "stop"} and value and known(kind, value):
                    result[kind].add(value)
    elif entity_type == "stop":
        for stop in entity_ids:
            for item in relationships.get("stop", {}).get(stop, set()):
                if item.startswith("trip:"):
                    trip = item[5:]
                    if not known("trip", trip):
                        continue
                    result["trip"].add(trip)
                    for related in relationships.get("trip", {}).get(trip, set()):
                        kind, _, value = related.partition(":")
                        if kind in {"route", "service", "shape"} and value and known(kind, value):
                            result[kind].add(value)
    elif entity_type in {"route", "service", "shape"}:
        relationship_type = {"route": "route", "service": "service", "shape": "shape"}[entity_type]
        for entity_id in entity_ids:
            for item in relationships.get(relationship_type, {}).get(entity_id, set()):
                if item.startswith("trip:"):
                    trip = item[5:]
                    if not known("trip", trip):
                        continue
                    result["trip"].add(trip)
                    for related in relationships.get("trip", {}).get(trip, set()):
                        kind, _, value = related.partition(":")
                        if kind in {"route", "service", "shape", "stop"} and value:
                            result[kind].add(value)
    elif entity_type == "stop_time":
        for item_id in entity_ids:
            for item in relationships.get("stop_time", {}).get(item_id, set()):
                if item.startswith("trip:") and known("trip", item[5:]):
                    result["trip"].add(item[5:])
    return result
