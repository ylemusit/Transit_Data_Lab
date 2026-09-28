from __future__ import annotations
import argparse, json
from pathlib import Path
from .ingestion import IngestionError
from .pipeline import record_ingestion_error, run

def main() -> int:
    parser = argparse.ArgumentParser(description="GTFS_Lab V1 technical run")
    parser.add_argument("zip", type=Path)
    parser.add_argument("--output", type=Path, default=Path("runs"))
    parser.add_argument("--route", help="route_id opcional para export GIS")
    parser.add_argument("--direction", help="direction_id opcional para export GIS")
    args = parser.parse_args()
    try:
        result = run(args.zip, args.output, args.route, args.direction)
    except IngestionError as exc:
        result = record_ingestion_error(args.zip, args.output, exc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"run_id": result["run_id"], "dataset_id": result["dataset"]["dataset_id"], "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
