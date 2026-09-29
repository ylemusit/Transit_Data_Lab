"""Recover corpus provenance and structural relationships from local inputs only."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}
NAP_SNAPSHOT_OBSERVATIONS = {
    "001": ("2026-06-02", "2025-01-01", "2026-12-31"), "002": ("2026-06-02", "2025-01-01", "2026-12-31"),
    "003": ("2026-06-02", "2025-01-01", "2026-12-31"), "004": ("2026-06-02", "2025-01-01", "2026-12-31"),
    "005": ("2026-06-02", "2025-01-01", "2026-12-31"), "006": ("2026-02-04", "2024-12-31", "2025-12-30"),
    "007": ("2026-03-20", "2025-12-31", "2026-12-30"), "008": ("2026-08-31", "2024-06-01", "2026-12-31"),
    "009": ("2025-09-16", "2025-07-22", "2026-12-31"), "010": ("2026-03-09", "2025-12-31", "2049-12-30"),
    "011": ("2026-09-07", "2026-07-01", "2027-09-01"), "012": ("2025-06-30", "2024-12-31", "2049-12-31"),
    "013": ("2025-05-29", "2025-01-01", "2049-12-31"), "014": ("2026-05-27", "2026-01-01", "2049-12-31"),
    "015": ("2026-09-16", "2026-01-01", "2049-12-31"), "016": ("2026-09-22", "2026-09-21", "2027-09-21"),
    "017": ("2026-09-22", "2026-09-20", "2026-10-21"), "018": ("2026-09-22", "2026-09-01", "2027-06-30"),
    "019": ("2026-09-10", "2017-01-06", "2026-12-23"), "020": ("2025-05-30", "2023-12-31", "2026-12-30"),
}
RELATIONS = {
    "SAME_SOURCE_LINEAGE", "LIKELY_RELATED", "POSSIBLY_RELATED",
    "LIKELY_INDEPENDENT", "INDEPENDENT", "UNRESOLVED",
}
INDEPENDENCE = {"YES", "NO", "UNRESOLVED"}
FEED_FIELDS = (
    "feed_publisher_name", "feed_publisher_url", "feed_lang", "default_lang",
    "feed_start_date", "feed_end_date", "feed_version", "feed_contact_email",
    "feed_contact_url",
)
AGENCY_FIELDS = ("agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang")
TABLE_FIELDS = {
    "agency.txt": AGENCY_FIELDS,
    "routes.txt": ("route_id", "route_short_name", "route_long_name"),
    "stops.txt": ("stop_id", "stop_name"),
    "trips.txt": ("trip_id", "route_id", "service_id", "trip_headsign"),
}
NO_VALIDATOR_KEYS = {
    "finding_count", "validation_status", "audit_results", "quality_score",
    "error_count", "validator_findings", "validation_result", "findings", "results",
}


def _read_table(archive: zipfile.ZipFile, basename: str) -> list[dict[str, str]]:
    member = next((n for n in archive.namelist() if PurePosixPath(n).name.lower() == basename), None)
    if member is None:
        return []
    raw = archive.read(member)
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Keep source bytes untouched; CP1252 is only an analysis-time display decode.
        text = raw.decode("cp1252")
    return list(csv.DictReader(io.StringIO(text, newline="")))


def _unique(rows: list[dict[str, str]], field: str) -> list[str]:
    return sorted({row[field].strip() for row in rows if row.get(field, "").strip()})


def _candidate_timestamp(filename: str) -> str:
    match = re.match(r"^(\d{8})_(\d{6})_", filename)
    if not match:
        return "UNKNOWN"
    try:
        return datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").isoformat(timespec="seconds")
    except ValueError:
        return "UNKNOWN"


def _normalized(raw: str) -> dict[str, str] | None:
    if not any(marker in raw for marker in ("Ã", "Â", "â€", "ï¿½")):
        return None
    try:
        repaired = raw.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None
    if repaired == raw:
        return None
    return {"raw_value": raw, "normalized_display_value": repaired, "normalization_method": "REVERSIBLE_LATIN1_BYTES_DECODED_AS_UTF8"}


def _pretty_json(value: Any, level: int = 0) -> str:
    pad, child_pad = "  " * level, "  " * (level + 1)
    if isinstance(value, dict):
        if not value:
            return "{}"
        entries = [f"{child_pad}{json.dumps(key, ensure_ascii=False)}: {_pretty_json(child, level + 1)}" for key, child in value.items()]
        return "{\n" + ",\n".join(entries) + f"\n{pad}}}"
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(child, (dict, list)) for child in value):
            return "[" + ", ".join(json.dumps(child, ensure_ascii=False) for child in value) + "]"
        return "[\n" + ",\n".join("  " * (level + 1) + _pretty_json(child, level + 1) for child in value) + f"\n{pad}]"
    return json.dumps(value, ensure_ascii=False)


def build(corpus_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = list(csv.DictReader((corpus_root / "benchmark_manifest.csv").open(encoding="utf-8-sig", newline="")))
    datasets: list[dict[str, Any]] = []
    inputs: dict[str, dict[str, Any]] = {}
    for row in manifest:
        dataset_id = row["benchmark_id"]
        metadata_rel = f"{row['operator_path']}/00_metadata/source_metadata.json"
        metadata = json.loads((corpus_root / metadata_rel).read_text(encoding="utf-8-sig"))
        zip_source = next((s for s in metadata.get("source_files", []) if s.get("role") == "original_gtfs_zip"), {})
        zip_rel = zip_source.get("path", "")
        zip_path = corpus_root / zip_rel
        if not zip_path.is_file():
            raise FileNotFoundError(f"Dataset {dataset_id}: original GTFS ZIP unavailable")
        digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
        if zip_source.get("sha256", "").lower() != digest:
            raise ValueError(f"Dataset {dataset_id}: ZIP SHA-256 differs from metadata")
        name = PurePosixPath(zip_rel).name
        agency, routes, stops, trips = [], [], [], []
        feed: dict[str, str] = {key: "UNKNOWN" for key in FEED_FIELDS}
        with zipfile.ZipFile(zip_path) as archive:
            agency, routes, stops, trips = (_read_table(archive, table) for table in TABLE_FIELDS)
            feed_rows = _read_table(archive, "feed_info.txt")
            if feed_rows:
                feed = {key: (feed_rows[0].get(key) or "UNKNOWN").strip() for key in FEED_FIELDS}
        agency_identity = [{key: (r.get(key) or "UNKNOWN").strip() for key in AGENCY_FIELDS} for r in agency]
        timestamp = _candidate_timestamp(name)
        nap_update, nap_start, nap_end = NAP_SNAPSHOT_OBSERVATIONS[dataset_id]
        nap_snapshot_path = next((item["path"] for item in metadata.get("source_files", []) if item.get("role") == "original_nap_snapshot"), "UNKNOWN")
        sources = [
            {"type": "MANIFEST", "path": "02_Data_Engineering/GTFS_Lab/20_clientes_reales/benchmark_manifest.csv", "field": "benchmark_id"},
            {"type": "LOCAL_METADATA_FILE", "path": metadata_rel, "field": "source_files[role=original_gtfs_zip].sha256"},
            {"type": "LOCAL_METADATA_FILE", "path": metadata_rel, "field": "operator_display_name/source_platform/family"},
            {"type": "GTFS_ZIP", "path": zip_rel, "field": "agency.txt/feed_info.txt/routes.txt/stops.txt/trips.txt"},
            {"type": "FILENAME_PATTERN", "filename": name, "field": "filename_timestamp_candidate"},
        ]
        sources.extend({"type": "LOCAL_NAP_SNAPSHOT", "path": item["path"], "field": "visual_snapshot_only"} for item in metadata.get("source_files", []) if item.get("role") == "original_nap_snapshot")
        raw_operator = metadata.get("operator_display_name") or "UNKNOWN"
        raw_platform = metadata.get("source_platform") or "UNKNOWN"
        normalized_values = [value for value in (_normalized(raw_operator), _normalized(raw_platform)) if value]
        normalized_values.extend({"raw_value": row["agency_name"], "normalized_display_value": row["agency_name"], "normalization_method": "GTFS_TEXT_DECODING_UTF8_OR_CP1252_FALLBACK"} for row in agency if row.get("agency_name"))
        provenance = {
            "dataset_id": dataset_id, "zip_sha256": digest,
            "family": metadata.get("family") or row.get("family") or "UNKNOWN",
            "operator_declared": raw_operator,
            "agency_identity": agency_identity, "feed_info": feed,
            "filename_timestamp_candidate": timestamp, "timestamp_semantics": "UNKNOWN",
            "source_platform": raw_platform,
            "source_dataset_id": metadata.get("source_dataset_id") or "UNKNOWN",
            "source_url": metadata.get("source_url") or "UNKNOWN",
            "capture_date": metadata.get("capture_date") or "UNKNOWN",
            "publication_or_feed_dates": {"feed_start_date": feed["feed_start_date"], "feed_end_date": feed["feed_end_date"], "nap_last_update_metadata": metadata.get("nap_last_update") or "UNKNOWN", "nap_snapshot_displayed_service_range": {"start": nap_start, "end": nap_end}},
            "nap_snapshot_displayed_update_date": nap_update,
            "metadata_retrieved_at": "UNKNOWN",
            "evidence_sources": sources,
            "provenance_confidence": "MEDIUM" if agency_identity or feed_rows else "LOW",
            "normalization": normalized_values,
            "notes": ["Filename timestamp semantics are unknown; not treated as capture or publication date.", "NAP source dataset ID and URL are absent from local metadata.", "NAP dates are manual transcriptions from the preserved screenshot; they are not ZIP capture dates."],
            "nap_snapshot_evidence": {"type": "LOCAL_NAP_SNAPSHOT", "path": nap_snapshot_path, "fields": "displayed_updated_date_and_feed_date_range"},
        }
        datasets.append(provenance)
        inputs[dataset_id] = {
            "agency_ids": _unique(agency, "agency_id"),
            "agency_names": _unique(agency, "agency_name"),
            "route_ids": _unique(routes, "route_id"),
            "route_names": sorted({(r.get("route_id", ""), r.get("route_short_name", ""), r.get("route_long_name", "")) for r in routes}),
            "stop_ids": _unique(stops, "stop_id"),
            "stop_names": sorted({(r.get("stop_id", ""), r.get("stop_name", "")) for r in stops}),
            "trip_ids": _unique(trips, "trip_id"),
            "trip_route_ids": sorted({(r.get("trip_id", ""), r.get("route_id", "")) for r in trips}),
            "feed": feed,
        }

    manifest_pairs: list[dict[str, Any]] = []
    inventory = json.loads((Path(__file__).parent.parent / "corpus" / "inventory_v1.json").read_text(encoding="utf-8"))
    baseline_pairs = {tuple(row["dataset_ids"]) for row in inventory["structural_relationships"]}
    priority_pairs = {("016", "017"), ("016", "018"), ("016", "019"), ("017", "018"), ("017", "019"), ("018", "019")}
    for i, left in enumerate(datasets):
        for right in datasets[i + 1:]:
            a, b = left["dataset_id"], right["dataset_id"]
            x, y = inputs[a], inputs[b]
            common_agency = sorted(set(x["agency_ids"]) & set(y["agency_ids"]))
            common_routes = sorted(set(x["route_ids"]) & set(y["route_ids"]))
            common_stops = sorted(set(x["stop_ids"]) & set(y["stop_ids"]))
            common_route_names = sorted({(s, l) for _, s, l in x["route_names"] if s or l} & {(s, l) for _, s, l in y["route_names"] if s or l})
            common_stop_names = sorted({name for _, name in x["stop_names"] if name} & {name for _, name in y["stop_names"] if name})
            if not (common_agency or common_routes or common_stops or left["zip_sha256"] == right["zip_sha256"] or (a, b) in priority_pairs):
                continue
            same_agency_name = bool(set(x["agency_names"]) & set(y["agency_names"]))
            same_feed_publisher = x["feed"]["feed_publisher_name"] != "UNKNOWN" and x["feed"]["feed_publisher_name"] == y["feed"]["feed_publisher_name"]
            same_feed_version = x["feed"]["feed_version"] != "UNKNOWN" and x["feed"]["feed_version"] == y["feed"]["feed_version"]
            exact = left["zip_sha256"] == right["zip_sha256"]
            if exact:
                classification, confidence, reason = "SAME_SOURCE_LINEAGE", "HIGH", "ZIP SHA-256 is identical."
            elif common_agency or common_routes or common_stops or same_agency_name or same_feed_publisher or same_feed_version:
                classification, confidence, reason = "POSSIBLY_RELATED", "LOW", "One or more shared agency, route, stop, publisher, version, or identity signals; insufficient to establish lineage."
            else:
                classification, confidence, reason = "UNRESOLVED", "UNKNOWN", "No decisive provenance evidence; structural review is incomplete."
            if exact:
                independence = "NO"
            elif classification in {"LIKELY_RELATED", "POSSIBLY_RELATED", "UNRESOLVED"}:
                independence = "UNRESOLVED"
            else:
                independence = "UNRESOLVED"
            feed_dates_left = [x["feed"].get("feed_start_date", "UNKNOWN"), x["feed"].get("feed_end_date", "UNKNOWN")]
            feed_dates_right = [y["feed"].get("feed_start_date", "UNKNOWN"), y["feed"].get("feed_end_date", "UNKNOWN")]
            if all(v != "UNKNOWN" for v in feed_dates_left + feed_dates_right):
                temporal_relation = "FEED_DATE_RANGE_OVERLAP" if feed_dates_left[0] <= feed_dates_right[1] and feed_dates_right[0] <= feed_dates_left[1] else "FEED_DATE_RANGES_DISJOINT"
            else:
                temporal_relation = "UNKNOWN"
            manifest_pairs.append({
                "pair_id": f"{a}-{b}", "dataset_a": a, "dataset_b": b,
                "shared_agency_ids": common_agency, "shared_route_ids": common_routes,
                "shared_stop_ids": common_stops,
                "shared_agency_names": sorted(set(x["agency_names"]) & set(y["agency_names"])),
                "shared_route_short_long_names": common_route_names,
                "shared_stop_names": common_stop_names,
                "shared_trip_ids": sorted(set(x["trip_ids"]) & set(y["trip_ids"])),
                "feed_info_comparison": {
                    "publisher_a": x["feed"]["feed_publisher_name"], "publisher_b": y["feed"]["feed_publisher_name"],
                    "publisher_url_a": x["feed"]["feed_publisher_url"], "publisher_url_b": y["feed"]["feed_publisher_url"],
                    "version_a": x["feed"]["feed_version"], "version_b": y["feed"]["feed_version"],
                    "feed_dates_a": [x["feed"]["feed_start_date"], x["feed"]["feed_end_date"]],
                    "feed_dates_b": [y["feed"]["feed_start_date"], y["feed"]["feed_end_date"]],
                },
                "route_overlap_ratio": len(common_routes) / max(1, min(len(x["route_ids"]), len(y["route_ids"]))),
                "stop_overlap_ratio": len(common_stops) / max(1, min(len(x["stop_ids"]), len(y["stop_ids"]))),
                "trip_overlap_ratio": len(set(x["trip_ids"]) & set(y["trip_ids"])) / max(1, min(len(x["trip_ids"]), len(y["trip_ids"]))),
                "operator_relation": "SAME_DECLARED_NAME" if same_agency_name else "DIFFERENT_OR_UNKNOWN",
                "source_relation": "SAME_ZIP_BYTES" if exact else "NAP_IDS_URL_NOT_RECOVERED",
                "temporal_relation": temporal_relation,
                "structural_relation": "EXACT_ZIP_DUPLICATE" if exact else "SHARED_IDENTIFIERS" if (common_agency or common_routes or common_stops) else "PRIORITY_PAIR_WITH_NO_SHARED_IDENTIFIERS",
                "shared_feed_publisher": same_feed_publisher,
                "shared_feed_version": same_feed_version,
                "classification": classification, "confidence": confidence,
                "reason": reason,
                "evidence_sources": [{"type": "GTFS_ZIP_COMPARISON", "datasets": [a, b], "fields": "agency.txt/routes.txt/stops.txt/trips.txt/feed_info.txt"}],
                "independence_decision": independence,
                "can_be_opposite_split_sides": "NO" if independence == "NO" else "UNRESOLVED",
            })
    provenance = {
        "schema_version": "1.0.0", "scope": "LOCAL_METADATA_AND_INPUTS_ONLY",
        "dataset_count": len(datasets), "datasets": datasets,
        "source_lineage_candidates": [],
        "custodian_questions": [
            {"question_id": "CQ-01", "datasets_affected": [f"{i:03}" for i in range(1, 21)], "unknown": "NAP source dataset IDs and canonical resource URLs", "why_it_matters": "Cannot establish source lineage or acquisition provenance.", "evidence_found": "source_metadata.json fields are null; local NAP snapshots show no resource identifier.", "question": "What NAP resource ID and URL correspond to each benchmark dataset and which acquisition record links it to this ZIP?"},
            {"question_id": "CQ-02", "datasets_affected": sorted({x for pair in manifest_pairs if pair["shared_stop_ids"] or pair["shared_route_ids"] for x in (pair["dataset_a"], pair["dataset_b"])}), "unknown": "Origin and reuse policy for shared GTFS identifiers", "why_it_matters": "Related feeds may need to remain on one split side.", "evidence_found": "Shared route/stop IDs without shared agency IDs, names, or trips in affected pairs.", "question": "Do these shared identifiers come from a common registry/network or independent reuse, and should any affected feeds be grouped?"},
            {"question_id": "CQ-03", "datasets_affected": [f"{i:03}" for i in range(1, 21)], "unknown": "Semantic meaning of ZIP filename timestamps", "why_it_matters": "They cannot be used as capture/publication chronology without corroboration.", "evidence_found": "Filename patterns exist; metadata does not assign their meaning.", "question": "Which acquisition event, if any, does the YYYYMMDD_HHMMSS filename prefix represent?"},
        ],
    }
    relationships = {
        "schema_version": "1.0.0", "baseline_pair_count": len(baseline_pairs),
        "baseline_pairs": ["-".join(pair) for pair in sorted(baseline_pairs)],
        "priority_016_019_pair_count": 6, "pair_count": len(manifest_pairs), "pairs": manifest_pairs,
        "independence_matrix": [{"dataset_a": p["dataset_a"], "dataset_b": p["dataset_b"], "relationship": p["classification"], "confidence": p["confidence"], "can_be_opposite_split_sides": p["can_be_opposite_split_sides"]} for p in manifest_pairs],
    }
    return provenance, relationships


def validate(provenance: dict[str, Any], relationships: dict[str, Any], expected_pairs: int = 29) -> list[str]:
    errors: list[str] = []
    def walk(value: Any):
        if isinstance(value, dict):
            for key, child in value.items():
                yield key, child
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
    for key, value in list(walk(provenance)) + list(walk(relationships)):
        if key.lower() in NO_VALIDATOR_KEYS:
            errors.append(f"validator output field found: {key}")
        if isinstance(value, str) and (Path(value).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", value)):
            errors.append(f"absolute path forbidden: {value}")
    datasets = provenance.get("datasets", [])
    ids = {row.get("dataset_id") for row in datasets}
    if len(datasets) != 20 or len(ids) != 20:
        errors.append("dataset coverage must contain 20 unique datasets")
    for row in datasets:
        if not row.get("evidence_sources"):
            errors.append(f"evidence source missing: {row.get('dataset_id')}")
        if row.get("provenance_confidence") not in CONFIDENCE:
            errors.append(f"invalid confidence: {row.get('dataset_id')}")
        if row.get("capture_date") not in (None, "UNKNOWN"):
            temporal_evidence = any("capture_date" in e.get("field", "").lower() and e.get("type") in {"LOCAL_METADATA_FILE", "NAP_METADATA", "CUSTODIAN_CONFIRMATION"} for e in row.get("evidence_sources", []))
            if not temporal_evidence:
                errors.append(f"capture_date inferred from filename: {row.get('dataset_id')}")
        if any(k in row for k in NO_VALIDATOR_KEYS):
            errors.append(f"validator output field found: {row.get('dataset_id')}")
    pairs = relationships.get("pairs", [])
    if len(pairs) != expected_pairs:
        errors.append(f"relationship coverage must contain {expected_pairs} pairs (28 baseline plus priority 016-019 review)")
    seen: set[tuple[str, str]] = set()
    for pair in pairs:
        key = tuple(sorted((pair.get("dataset_a", ""), pair.get("dataset_b", ""))))
        if key in seen:
            errors.append(f"duplicate relationship: {key}")
        seen.add(key)
        if pair.get("classification") not in RELATIONS:
            errors.append(f"invalid relationship classification: {key}")
        if pair.get("confidence") not in CONFIDENCE:
            errors.append(f"invalid relationship confidence: {key}")
        if pair.get("independence_decision") not in INDEPENDENCE:
            errors.append(f"invalid independence enum: {key}")
        if pair.get("can_be_opposite_split_sides") not in INDEPENDENCE:
            errors.append(f"invalid split-side decision: {key}")
        if pair.get("independence_decision") == "YES" and not pair.get("reason", "").strip():
            errors.append(f"independent relation lacks basis: {key}")
        if pair.get("classification") in {"INDEPENDENT", "LIKELY_INDEPENDENT"} and not pair.get("reason", "").strip():
            errors.append(f"independent relation lacks basis: {key}")
        if pair.get("classification") == "UNRESOLVED" and pair.get("independence_decision") != "UNRESOLVED":
            errors.append(f"unresolved relation hidden: {key}")
    baseline_pairs = relationships.get("baseline_pairs", [])
    encoded_seen = {"-".join(key) for key in seen}
    if relationships.get("baseline_pair_count") != 28 or len(baseline_pairs) != 28 or not set(baseline_pairs).issubset(encoded_seen):
        errors.append("the 28 original structural relationship pairs are not all covered")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--relationships", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    provenance, relationships = build(args.corpus_root)
    errors = validate(provenance, relationships)
    if errors:
        raise SystemExit("\n".join(errors))
    if args.check:
        print(f"M04_PROVENANCE_GATE_PASS datasets={len(provenance['datasets'])} pairs={len(relationships['pairs'])}")
        return 0
    for path, value in ((args.provenance, provenance), (args.relationships, relationships)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_pretty_json(value) + "\n", encoding="utf-8")
    print(f"datasets={len(provenance['datasets'])} pairs={len(relationships['pairs'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
