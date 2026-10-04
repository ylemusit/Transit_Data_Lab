"""Generic interpreter for GTFS-G07-DISTANCE-PROGRESSION findings."""
from __future__ import annotations

import csv
import io
import math
import zipfile
from bisect import bisect_left
from collections import defaultdict
from typing import Any

RULE_ID = "GTFS-G07-DISTANCE-PROGRESSION"
EARTH_RADIUS_M = 6_371_008.8


def _shape_rows(zip_path: str) -> dict[str, list[tuple[int, int, float, float, str]]]:
    result: dict[str, list[tuple[int, int, float, float, str]]] = defaultdict(list)
    with zipfile.ZipFile(zip_path) as archive:
        member = next((name for name in archive.namelist() if name.rsplit("/", 1)[-1] == "shapes.txt"), None)
        if member is None:
            return result
        with archive.open(member) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            for row_number, row in enumerate(reader, 1):
                try:
                    result[row["shape_id"]].append((row_number, int(row["shape_pt_sequence"]),
                        float(row["shape_pt_lat"]), float(row["shape_pt_lon"]), row.get("shape_dist_traveled", "")))
                except (KeyError, TypeError, ValueError):
                    continue
    for values in result.values():
        values.sort(key=lambda item: item[1])
    return result


def _distance_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(min(1.0, math.sqrt(h)))


def classify_findings(findings: list[dict[str, Any]], zip_path: str | None) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rows = _shape_rows(zip_path) if zip_path else {}
    row_positions = {(shape, row[0]): index for shape, values in rows.items() for index, row in enumerate(values)}
    sequence_values = {shape: [row[1] for row in values] for shape, values in rows.items()}
    classified: dict[str, list[dict[str, Any]]] = defaultdict(list)
    equal_move_buckets = {"0": 0, "0-0.25m": 0, "0.25-0.50m": 0, "0.50-0.75m": 0, "0.75-1m": 0, ">1m": 0}
    precision_values: set[str] = {"FRACTIONAL" if "." in row[4] else "INTEGER_ONLY"
                                  for values in rows.values() for row in values if row[4]}
    transition_count = increase_count = equal_count = decrease_count = 0
    for shape_rows in rows.values():
        ordered = sorted(shape_rows, key=lambda item: item[1])
        for previous_row, current_row in zip(ordered, ordered[1:]):
            try:
                previous_distance, current_distance = float(previous_row[4]), float(current_row[4])
            except (TypeError, ValueError):
                continue
            transition_count += 1
            if current_distance > previous_distance:
                increase_count += 1
            elif current_distance < previous_distance:
                decrease_count += 1
            else:
                equal_count += 1
                movement = _distance_m(previous_row[2:4], current_row[2:4])
                bucket = ("0" if movement == 0 else "0-0.25m" if movement <= .25 else
                          "0.25-0.50m" if movement <= .50 else "0.50-0.75m" if movement <= .75 else
                          "0.75-1m" if movement <= 1 else ">1m")
                equal_move_buckets[bucket] += 1
    for finding in findings:
        if finding.get("rule_id") != RULE_ID:
            continue
        observed = finding.get("observed") if isinstance(finding.get("observed"), dict) else {}
        shape = str(observed.get("shape_id", finding.get("shape_id", "")))
        current = observed.get("current")
        previous = observed.get("previous")
        coords_changed = None
        movement = None
        exact = False
        row_locator = str(finding.get("record_locator", ""))
        try:
            row_number = int(row_locator.rsplit(":", 1)[-1])
        except ValueError:
            row_number = -1
        shape_rows = rows.get(shape, [])
        current_position = row_positions.get((shape, row_number))
        current_row = shape_rows[current_position] if current_position is not None else None
        if current_row:
            try:
                sequence_position = bisect_left(sequence_values.get(shape, []), current_row[1])
                if sequence_position and sequence_values[shape][sequence_position - 1] < current_row[1]:
                    previous_row = shape_rows[sequence_position - 1]
                    coords_changed = (current_row[2:4] != previous_row[2:4])
                    movement = _distance_m(previous_row[2:4], current_row[2:4])
                    exact = not coords_changed and str(previous_row[4]) == str(current_row[4])
            except (TypeError, ValueError):
                pass
        if isinstance(current, (int, float)) and isinstance(previous, (int, float)) and current < previous:
            pattern = "DISTANCE_DECREASE"
        elif current == previous and coords_changed is False and exact:
            pattern = "EXACT_DUPLICATE_GEOMETRY"
        elif current == previous and coords_changed is True and movement is not None:
            pattern = "QUANTIZATION_COMPATIBLE"
        else:
            pattern = "UNKNOWN_PATTERN"
        classified[pattern].append(finding)
    precision = "UNKNOWN" if not precision_values else next(iter(precision_values)) if len(precision_values) == 1 else "MIXED"
    metrics = {"transition_count": transition_count, "increase_count": increase_count,
               "equal_count": equal_count, "decrease_count": decrease_count,
               "equal_coordinate_movement_buckets_m": equal_move_buckets,
               "distance_precision": precision}
    return classified, metrics
