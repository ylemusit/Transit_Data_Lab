"""Build a metadata and input-structure inventory for the real GTFS corpus.

This tool reads GTFS tables from source ZIPs. It does not run audit rules or
consume findings, validator statuses, or previous run outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


TABLE_KEYS = {
    "agency.txt": ("agency_id", "agency_ids"),
    "routes.txt": ("route_id", "route_ids"),
    "stops.txt": ("stop_id", "stop_ids"),
}
COUNT_TABLES = {
    "routes.txt": "route_count",
    "stops.txt": "stop_count",
    "trips.txt": "trip_count",
}


def _table_rows(archive: zipfile.ZipFile, member: str) -> list[dict[str, str]]:
    with archive.open(member) as stream:
        text = io.TextIOWrapper(stream, encoding="utf-8-sig", errors="replace", newline="")
        return list(csv.DictReader(text))


def _zip_inventory(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    tables: dict[str, list[str]] = {}
    counts: dict[str, int] = {}
    with zipfile.ZipFile(path) as archive:
        members = sorted(info.filename for info in archive.infolist() if not info.is_dir())
        basenames = [PurePosixPath(name).name.lower() for name in members]
        for table, (column, key) in TABLE_KEYS.items():
            member = next((name for name in members if PurePosixPath(name).name.lower() == table), None)
            rows = _table_rows(archive, member) if member else []
            tables[key] = sorted({row[column] for row in rows if row.get(column)})
            if table in COUNT_TABLES and member:
                counts[COUNT_TABLES[table]] = len(rows)
        for table, key in COUNT_TABLES.items():
            if key in counts:
                continue
            member = next((name for name in members if PurePosixPath(name).name.lower() == table), None)
            if member:
                counts[key] = len(_table_rows(archive, member))

    return {
        "zip_sha256": digest.hexdigest(),
        "size_bytes": path.stat().st_size,
        "file_count": len(members),
        "tables_present": sorted({PurePosixPath(name).name for name in members if PurePosixPath(name).suffix.lower() == ".txt"}),
        "counts": counts,
        "calendar_model": {
            "calendar_txt": "calendar.txt" in basenames,
            "calendar_dates_txt": "calendar_dates.txt" in basenames,
        },
        "shape_presence": "shapes.txt" in basenames,
        "_identifiers": tables,
    }


def build_inventory(corpus_root: Path) -> dict[str, Any]:
    manifest_path = corpus_root / "benchmark_manifest.csv"
    with manifest_path.open(encoding="utf-8-sig", newline="") as stream:
        manifest = list(csv.DictReader(stream))

    datasets: list[dict[str, Any]] = []
    for row in manifest:
        operator_dir = corpus_root / row["operator_path"]
        metadata_path = operator_dir / "00_metadata" / "source_metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        source = next(
            (item for item in metadata.get("source_files", []) if item.get("role") == "original_gtfs_zip"),
            None,
        )
        relative_zip = source.get("path") if source else None
        zip_path = corpus_root / relative_zip if relative_zip else None
        expected_hash = source.get("sha256") if source else None
        if zip_path is None or not zip_path.is_file():
            raise FileNotFoundError(f"Source ZIP unavailable for dataset {row['benchmark_id']}")

        measured = _zip_inventory(zip_path)
        actual_hash = measured.pop("zip_sha256")
        identifiers = measured.pop("_identifiers")
        datasets.append(
            {
                "dataset_id": row["benchmark_id"],
                "family": row.get("family") or "UNKNOWN",
                "operator_if_known": metadata.get("operator_display_name") or "UNKNOWN",
                "geography_if_known": metadata.get("country") or "UNKNOWN",
                "source_platform": metadata.get("source_platform") or "UNKNOWN",
                "source_dataset_id": metadata.get("source_dataset_id") or "UNKNOWN",
                "source_url": metadata.get("source_url") or "UNKNOWN",
                "capture_date": metadata.get("capture_date") or "UNKNOWN",
                "zip_relative_path": relative_zip,
                "zip_sha256": actual_hash,
                "declared_sha256": expected_hash or "UNKNOWN",
                "sha_matches_metadata": bool(expected_hash and actual_hash.lower() == expected_hash.lower()),
                **measured,
                "_identifiers": identifiers,
            }
        )

    relationships = []
    for index, left in enumerate(datasets):
        for right in datasets[index + 1 :]:
            shared = {
                table: len(set(left["_identifiers"][key]) & set(right["_identifiers"][key]))
                for table, key in (("agency.txt", "agency_ids"), ("routes.txt", "route_ids"), ("stops.txt", "stop_ids"))
            }
            exact_duplicate = left["zip_sha256"] == right["zip_sha256"]
            if exact_duplicate or any(shared.values()):
                relationships.append(
                    {
                        "dataset_ids": [left["dataset_id"], right["dataset_id"]],
                        "exact_zip_duplicate": exact_duplicate,
                        "shared_identifier_counts": shared,
                    }
                )

    for dataset in datasets:
        dataset.pop("_identifiers")
    families = sorted({dataset["family"] for dataset in datasets})
    return {
        "inventory_version": "1.0.0",
        "source_manifest": "02_Data_Engineering/GTFS_Lab/20_clientes_reales/benchmark_manifest.csv",
        "inspection_scope": "METADATA_AND_INPUT_STRUCTURE",
        "evaluation_outputs_used": False,
        "validator_findings_used": False,
        "dataset_count": len(datasets),
        "family_counts": {family: sum(item["family"] == family for item in datasets) for family in families},
        "all_declared_zip_hashes_match": all(item["sha_matches_metadata"] for item in datasets),
        "datasets": datasets,
        "structural_relationships": relationships,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-root", type=Path, required=True, help="Directory containing benchmark_manifest.csv")
    parser.add_argument("--output", type=Path, required=True, help="Output inventory JSON path")
    args = parser.parse_args()
    inventory = build_inventory(args.corpus_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"datasets={inventory['dataset_count']} hash_matches={sum(row['sha_matches_metadata'] for row in inventory['datasets'])}")
    print(f"structural_relationships={len(inventory['structural_relationships'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
