from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import zipfile
from . import VERSION
from .core import DatasetIdentity, RunContext, new_run_id, sha256_file

KNOWN = ["agency", "stops", "routes", "trips", "stop_times", "calendar", "calendar_dates", "shapes", "frequencies", "transfers", "feed_info", "levels", "translations", "pathways", "attributions", "fare_attributes", "fare_rules", "fare_media", "fare_products", "fare_leg_rules", "fare_leg_join_rules", "fare_transfer_rules", "timeframes", "networks", "route_networks", "areas", "stop_areas", "locations", "location_groups", "booking_rules", "fare_parkings"]
REQUIRED = {"agency", "stops", "routes", "trips", "stop_times"}
REQUIRED_COLUMNS = {
    "agency": {"agency_name", "agency_url", "agency_timezone"},
    "stops": {"stop_id", "stop_lat", "stop_lon"},
    "routes": {"route_id", "route_type"},
    "trips": {"route_id", "service_id", "trip_id"},
    "stop_times": {"trip_id", "stop_sequence"},
}
MAX_MEMBER = 512 * 1024 * 1024
MAX_TOTAL = 2 * 1024 * 1024 * 1024

class IngestionError(Exception):
    code = "INGESTION_ERROR"

def _safe_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    p = PurePosixPath(normalized)
    return not p.is_absolute() and not any(part in ("..", "") for part in p.parts) and not (len(normalized) > 1 and normalized[1] == ":")

def _decode(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            return payload.decode(encoding, errors="strict"), encoding
        except UnicodeDecodeError:
            pass
    try:
        return payload.decode("cp1252", errors="strict"), "cp1252"
    except UnicodeDecodeError as exc:
        raise IngestionError(f"Codificación no soportada: {exc}") from exc

def inspect_zip(zip_path: Path) -> tuple[dict[str, zipfile.ZipInfo], list[str], list[str]]:
    try:
        zf = zipfile.ZipFile(zip_path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise IngestionError(f"ZIP ilegible o malformado: {exc}") from exc
    with zf:
        selected: dict[str, zipfile.ZipInfo] = {}
        not_supported: list[str] = []
        seen_names: set[str] = set()
        warnings: list[str] = []
        total = 0
        for info in zf.infolist():
            if not _safe_member(info.filename):
                raise IngestionError(f"Ruta ZIP insegura: {info.filename!r}")
            folded = info.filename.casefold()
            if folded in seen_names:
                raise IngestionError(f"Nombre duplicado en ZIP: {info.filename!r}")
            seen_names.add(folded)
            total += info.file_size
            if info.file_size > MAX_MEMBER or total > MAX_TOTAL:
                raise IngestionError("Límite de tamaño ZIP excedido")
            if info.is_dir() or not info.filename.lower().endswith(".txt"):
                continue
            basename = PurePosixPath(info.filename).name.lower()
            table = basename[:-4]
            if table not in KNOWN:
                warnings.append(f"Tabla no soportada ignorada: {info.filename}")
                not_supported.append(info.filename)
                continue
            if "/" in info.filename.replace("\\", "/"):
                warnings.append(f"Tabla fuera de la raíz GTFS ignorada: {info.filename}")
                not_supported.append(info.filename)
                continue
            if table in selected:
                raise IngestionError(f"Archivo de tabla duplicado: {basename}")
            selected[table] = info
        return selected, warnings, not_supported

def _validate_member(zf: zipfile.ZipFile, info: zipfile.ZipInfo, table: str) -> tuple[bytes, list[str], str, int, list[str]]:
    try:
        raw = zf.read(info)
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise IngestionError(f"No se pudo descomprimir {info.filename}: {exc}") from exc
    text, encoding = _decode(raw)
    if encoding == "cp1252":
        warning = [f"{info.filename}: se aplicó fallback cp1252"]
    else:
        warning = []
    stream = io.StringIO(text, newline="")
    try:
        reader = csv.reader(stream, strict=True)
        header = next(reader, None)
        if not header or any(not h.strip() for h in header) or len(set(header)) != len(header):
            raise IngestionError(f"Cabecera vacía, duplicada o ausente: {info.filename}")
        missing = REQUIRED_COLUMNS.get(table, set()) - set(header)
        if missing:
            raise IngestionError(f"Faltan columnas requeridas en {info.filename}: {', '.join(sorted(missing))}")
        rows = 0
        for line_no, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise IngestionError(f"CSV malformado en {info.filename}, registro {line_no}: {len(row)} campos; cabecera {len(header)}")
            rows += 1
    except (csv.Error, StopIteration) as exc:
        if isinstance(exc, IngestionError):
            raise
        raise IngestionError(f"CSV malformado en {info.filename}: {exc}") from exc
    return raw, header, encoding, rows, warning

def load_dataset(zip_path: Path, output_dir: Path) -> RunContext:
    zip_path = zip_path.resolve()
    if not zip_path.is_file():
        raise IngestionError(f"No existe el ZIP: {zip_path}")
    selected, warnings, not_supported = inspect_zip(zip_path)
    run_id = new_run_id()
    work_dir = output_dir.resolve() / run_id
    tables_dir = work_dir / "input"
    tables_dir.mkdir(parents=True, exist_ok=False)
    table_paths: dict[str, Path] = {}
    files_meta: dict[str, dict] = {}
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for table, info in selected.items():
                raw, header, encoding, rows, member_warnings = _validate_member(zf, info, table)
                dest = tables_dir / f"{table}.txt"
                dest.write_bytes(raw)
                table_paths[table] = dest
                files_meta[f"{table}.txt"] = {"status": "PRESENT", "rows": rows, "headers": header, "encoding": encoding, "uncompressed_bytes": len(raw)}
                warnings.extend(member_warnings)
    except Exception:
        raise
    for table in KNOWN:
        files_meta.setdefault(f"{table}.txt", {"status": "ABSENT", "rows": 0, "headers": [], "encoding": None, "uncompressed_bytes": 0})
    inventory = {table: ("PRESENT" if table in selected else "ABSENT" if table in REQUIRED else "OPTIONAL") for table in KNOWN}
    inventory.update({f"NOT_SUPPORTED:{name}": "NOT_SUPPORTED" for name in not_supported})
    for table in REQUIRED:
        if table not in selected:
            warnings.append(f"Falta tabla obligatoria: {table}.txt")
    digest = sha256_file(zip_path)
    identity = DatasetIdentity(dataset_id="GTFS-" + digest[:16], source_filename=zip_path.name, source_sha256=digest, ingestion_timestamp_utc=datetime.now(timezone.utc).isoformat(), parser_version="gtfs-lab-csv/1", gtfs_lab_version=VERSION, files=files_meta)
    return RunContext(run_id, identity, zip_path, work_dir, table_paths, inventory, warnings)
