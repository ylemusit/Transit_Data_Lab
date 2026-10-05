"""Deterministic, read-only intake checks for the Windows GTFS client."""
from __future__ import annotations

import csv
import hashlib
import zipfile
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .ingestion import IngestionError, REQUIRED, REQUIRED_COLUMNS, _decode, inspect_zip


class InputValidationError(ValueError):
    """A selected source cannot be used as an input to the existing engine."""


@dataclass(frozen=True)
class IntakeSummary:
    filename: str
    source_sha256: str
    dataset_id: str
    size_bytes: int
    intake_timestamp_utc: str
    tables: tuple[str, ...]


def validate_gtfs_zip(source: Path, *, now: datetime | None = None) -> IntakeSummary:
    """Check ZIP integrity and engine structural preconditions without extraction."""
    source = Path(source)
    if source.suffix.lower() != ".zip":
        raise InputValidationError("BLOCKED_INPUT_INVALID: selecciona un archivo con extensión .zip")
    if not source.is_file():
        raise InputValidationError("BLOCKED_INPUT_INVALID: el archivo seleccionado no existe")
    try:
        before = source.stat()
        selected, _warnings, _unsupported = inspect_zip(source)
        missing = sorted(REQUIRED - selected.keys())
        if missing:
            raise InputValidationError(
                "BLOCKED_INPUT_INVALID: faltan tablas GTFS obligatorias: "
                + ", ".join(f"{table}.txt" for table in missing)
            )
        with zipfile.ZipFile(source) as archive:
            bad_member = archive.testzip()
            if bad_member:
                raise InputValidationError(f"BLOCKED_INPUT_INVALID: el archivo ZIP está dañado ({bad_member})")
            for table in sorted(REQUIRED):
                with archive.open(selected[table]) as stream:
                    header_bytes = stream.readline(1024 * 1024)
                try:
                    header_text, _encoding = _decode(header_bytes.rstrip(b"\r\n"))
                    header = next(csv.reader([header_text]))
                except (UnicodeError, StopIteration, csv.Error) as exc:
                    raise InputValidationError(
                        f"BLOCKED_INPUT_INVALID: cabecera no legible en {table}.txt"
                    ) from exc
                if len(header) > 256 or not header or len(set(header)) != len(header):
                    raise InputValidationError(f"BLOCKED_INPUT_INVALID: cabecera inválida en {table}.txt")
                missing_columns = REQUIRED_COLUMNS[table] - set(header)
                if missing_columns:
                    raise InputValidationError(
                        f"BLOCKED_INPUT_INVALID: faltan columnas en {table}.txt: "
                        + ", ".join(sorted(missing_columns))
                    )
        digest = hashlib.sha256()
        with source.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        after = source.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise InputValidationError("BLOCKED_INPUT_INVALID: el archivo fuente cambió durante la validación")
    except InputValidationError:
        raise
    except IngestionError as exc:
        raise InputValidationError(f"BLOCKED_INPUT_INVALID: {exc}") from exc
    except (OSError, zipfile.BadZipFile, RuntimeError, EOFError, zlib.error) as exc:
        raise InputValidationError(f"BLOCKED_INPUT_INVALID: ZIP ilegible o malformado ({type(exc).__name__})") from exc

    sha = digest.hexdigest()
    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    return IntakeSummary(
        filename=source.name,
        source_sha256=sha,
        dataset_id="GTFS-" + sha[:16],
        size_bytes=after.st_size,
        intake_timestamp_utc=timestamp.isoformat().replace("+00:00", "Z"),
        tables=tuple(sorted(selected)),
    )
