from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import hashlib
import json
import uuid

@dataclass
class DatasetIdentity:
    dataset_id: str
    source_filename: str
    source_sha256: str
    ingestion_timestamp_utc: str
    parser_version: str
    gtfs_lab_version: str
    files: dict[str, dict[str, Any]] = field(default_factory=dict)

@dataclass
class RunContext:
    run_id: str
    dataset: DatasetIdentity
    source_zip: Path
    work_dir: Path
    tables: dict[str, Path]
    inventory: dict[str, str]
    warnings: list[str] = field(default_factory=list)

@dataclass
class RuleResult:
    rule_id: str
    version: str
    scope: str
    severity: str
    description: str
    source_reference: str
    status: str
    checked_rows: int = 0
    finding_count: int = 0
    findings: list[dict[str, Any]] = field(default_factory=list)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def new_run_id() -> str:
    return "GTFSRUN-" + uuid.uuid4().hex[:16]

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def result_dict(result: RuleResult) -> dict[str, Any]:
    return asdict(result)
