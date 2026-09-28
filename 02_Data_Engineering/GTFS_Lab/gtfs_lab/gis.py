from __future__ import annotations
import json
from pathlib import Path
from .core import RunContext, write_json
from .validation import _rows

def export_stops(ctx: RunContext, output: Path) -> dict:
    features = []
    if "stops" not in ctx.tables: return {"status": "NOT_EVALUABLE", "artifacts": []}
    for no, row in _rows(ctx.tables["stops"]):
        try: lat, lon = float(row["stop_lat"]), float(row["stop_lon"])
        except (KeyError, ValueError): continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180): continue
        features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]}, "properties": {k: v for k, v in row.items()}})
    path = output / "stops.geojson"
    write_json(path, {"type": "FeatureCollection", "features": features})
    kml = output / "stops.kml"
    with kml.open("w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>GTFS stops</name>')
        for feature in features:
            p = feature["properties"]; name = _xml(p.get("stop_name") or p.get("stop_id", "")); lon, lat = feature["geometry"]["coordinates"]
            f.write(f'<Placemark><name>{name}</name><Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>')
        f.write('</Document></kml>\n')
    return {"status": "PASS", "artifacts": [str(path), str(kml)], "features": len(features)}

def export_route(ctx: RunContext, output: Path, route_id: str | None = None, direction_id: str | None = None) -> dict:
    if not all(t in ctx.tables for t in ("routes", "trips", "shapes")):
        return {"status": "NOT_EVALUABLE", "artifacts": []}
    wanted: dict[str, set[str]] = {}
    for _, row in _rows(ctx.tables["trips"]):
        if (not route_id or row.get("route_id") == route_id) and (direction_id is None or row.get("direction_id") == direction_id):
            if row.get("shape_id"): wanted.setdefault((row.get("route_id", ""), row.get("direction_id", "")), set()).add(row["shape_id"])
    points = {k: [] for shapes in wanted.values() for k in shapes}
    for _, row in _rows(ctx.tables["shapes"]):
        sid = row.get("shape_id", "")
        if sid not in points: continue
        try: lat, lon, seq = float(row["shape_pt_lat"]), float(row["shape_pt_lon"]), int(row["shape_pt_sequence"])
        except (KeyError, ValueError): continue
        if -90 <= lat <= 90 and -180 <= lon <= 180: points[sid].append((seq, lon, lat))
    output.mkdir(parents=True, exist_ok=True); artifacts = []
    geojson_features = []
    for (rid, direction), shape_ids in sorted(wanted.items()):
        for sid in sorted(shape_ids):
            coords = sorted(points.get(sid, []))
            if not coords: continue
            suffix = f"_dir_{_slug(direction)}" if direction != "" else ""
            path = output / f"route_{_slug(rid)}{suffix}_shape_{_slug(sid)}.kml"
            with path.open("w", encoding="utf-8", newline="\n") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
                f.write(f'<name>Route { _xml(rid) } shape { _xml(sid) }</name><Placemark><LineString><tessellate>1</tessellate><coordinates>')
                f.write(" ".join(f"{lon},{lat},0" for _, lon, lat in coords)); f.write('</coordinates></LineString></Placemark></Document></kml>\n')
            artifacts.append(str(path))
            geojson_features.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[lon, lat] for _, lon, lat in coords]}, "properties": {"route_id": rid, "direction_id": direction, "shape_id": sid}})
    if geojson_features:
        path = output / (f"route_{_slug(route_id)}_dir_{_slug(direction_id)}.geojson" if route_id and direction_id is not None else f"routes{('_' + _slug(route_id)) if route_id else ''}.geojson")
        write_json(path, {"type": "FeatureCollection", "features": geojson_features}); artifacts.append(str(path))
    return {"status": "PASS" if artifacts else "NOT_EVALUABLE", "artifacts": artifacts, "route_id": route_id, "direction_id": direction_id}

def _xml(value: str) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def _slug(value: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(value))[:80] or "unknown"
