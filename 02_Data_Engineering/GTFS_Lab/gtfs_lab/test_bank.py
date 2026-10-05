"""Controlled local intake and procedural acceptance over Client Workflow V1.

Case records are authoritative. JSON/CSV/JSONL registers are rebuildable views.
No engine contracts, source bytes or historical cases are modified.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import shutil
import stat
import subprocess
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .client_workflow import _redact_local_paths, _redact_path_text, run_client_audit
from .core import sha256_file
from .interpretation.consolidation import semantic_fingerprint
from .resource_stages import mark as _mark_stage

BANK_VERSION = "1.0.0"
DEFAULT_TEST_BANK_ROOT = Path("C:/TDL/BANK")


def _tdl_revision() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=Path(__file__).parent,
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"
CATEGORIES = set("INPUT FILESYSTEM WINDOWS ZIP CSV ENCODING DUCKDB GTFS_ENGINE COMPLIANCE REPORTING DELIVERY REPLAY PERFORMANCE UX UNKNOWN".split())
FAILURE_STATUSES = {"OPEN", "UNDER_INVESTIGATION", "RESOLVED", "ACCEPTED_LIMITATION", "NOT_REPRODUCIBLE"}
GATES = ("SOURCE_CAPTURED", "SOURCE_HASHED", "SOURCE_IMMUTABLE", "PREFLIGHT_COMPLETED",
         "AUDIT_COMPLETED", "FINDINGS_GENERATED", "INTERPRETATION_COMPLETED", "REPORT_GENERATED", "DELIVERY_GENERATED",
         "REPLAY_COMPLETED", "INTERPRETATION_REPLAY", "EVIDENCE_COMPLETE", "NO_UNRESOLVED_PIPELINE_FAILURE")


class PipelineFailure(ValueError):
    def __init__(self, message: str, category: str):
        super().__init__(message)
        self.category = category


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def _write(path: Path, value: Any) -> None:
    _atomic(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


@contextmanager
def _locked(bank: Path):
    if len(str(bank)) > 64:
        raise ValueError("El banco requiere una ruta corta (máximo 64 caracteres); por ejemplo C:/TDL/BANK")
    for name in ("ACTIVE", "OK", "NOT_OK", "REGISTRY"):
        (bank / name).mkdir(parents=True, exist_ok=True)
    lock = bank / "REGISTRY" / "bank.lock"
    # Exclusive creation serializes writers, including ID reservation and exports.
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"pid": os.getpid(), "started_at": _now()}))
    try:
        yield
    finally:
        lock.unlink()


def _rebuild(bank: Path) -> list[dict[str, Any]]:
    records = []
    for zone in ("ACTIVE", "OK", "NOT_OK"):
        for case in sorted((bank / zone).iterdir()):
            if not case.is_dir():
                continue
            record = _read(case / "case.json")
            record["case_path"] = case.relative_to(bank).as_posix()
            # An interrupted finalization must never appear accepted in ACTIVE.
            if zone == "ACTIVE":
                record["result"] = "ACTIVE"
                record["case_result"] = "ACTIVE"
            elif record["result"] != zone or case.name != f"{record['case_id']}_{zone}":
                raise ValueError("Clasificación/carpeta incoherente; revisar el expediente")
            records.append(record)
    records.sort(key=lambda row: row["case_id"])
    if len({row["case_id"] for row in records}) != len(records):
        raise ValueError("Case ID duplicado; registro no exportado")
    _write(bank / "REGISTRY" / "TEST_BANK_REGISTER.json", {"version": BANK_VERSION, "cases": records})
    columns = ("case_id", "dataset_title", "format", "source_sha256", "dataset_sha256", "original_filename",
               "tdl_version", "tdl_commit", "case_result", "audit_result", "replay_result", "finding_count",
               "started_at", "finished_at", "result", "audit_status", "replay", "findings",
               "pipeline_failures", "historical_pipeline_failures", "known_friction",
               "code_changes_required", "operator_specific_code", "case_path")
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for row in records:
        # Spreadsheet formula neutralization; JSON retains exact original strings.
        writer.writerow({key: "'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value
                         for key, value in row.items()})
    _atomic(bank / "REGISTRY" / "TEST_BANK_REGISTER.csv", output.getvalue())
    failures = [event for row in records for event in row.get("failures", [])]
    _atomic(bank / "REGISTRY" / "FAILURE_REGISTER.jsonl", "".join(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n" for event in failures))
    return records


def rebuild_register(bank: Path) -> list[dict[str, Any]]:
    bank = bank.resolve()
    with _locked(bank):
        return _rebuild(bank)


def _capture(source: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    before = source.stat()
    digest = sha256_file(source)
    after = source.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("La fuente cambió durante la captura")
    return {"contract": "TDLOriginalIdentity", "version": BANK_VERSION,
            "original_filename": source.name, "original_extension": source.suffix,
            "original_path": str(source), "original_size": after.st_size,
            "sha256": digest, "captured_at": _now(),
            "ORIGINAL_METADATA": metadata,
            "FILESYSTEM_METADATA": {
                "modified_time_observed_utc": datetime.fromtimestamp(after.st_mtime, timezone.utc).isoformat(),
                "created_time_observed_utc": datetime.fromtimestamp(after.st_birthtime, timezone.utc).isoformat() if hasattr(after, "st_birthtime") else None,
                "reliability": "OBSERVED_ONLY; NOT_PUBLISHER_TIMESTAMPS",
                "source_role": "RECEIVED_LOCAL_FILE; MAY_BE_A_PREVIOUS_CAPTURE"}}


def _preflight(path: Path) -> dict[str, Any]:
    # No extraction. Detailed GTFS structure/encoding remains owned by the engine.
    with zipfile.ZipFile(path) as archive:
        if not archive.infolist():
            raise ValueError("ZIP vacío")
        for member in archive.infolist():
            name = member.filename.replace("\\", "/")
            if name.startswith("/") or ".." in name.split("/") or ":" in name or member.flag_bits & 1:
                raise ValueError("Miembro ZIP inseguro o cifrado")
        bad = archive.testzip()
        if bad:
            raise ValueError(f"CRC inválido: {bad}")
        return {"status": "PASS", "members": len(archive.infolist()), "crc": "PASS",
                "scope": "ZIP_STRUCTURE_CRC_PATHS; GTFS_SEMANTICS_OWNED_BY_ENGINE"}


def _verify_workflow(delivery: Path, digest: str) -> tuple[dict[str, Any], Path]:
    manifest_path = delivery / "audit_manifest.json"
    manifest = _read(manifest_path)
    seal = _read(delivery / "delivery_seal.json")
    if seal.get("audit_manifest_sha256") != sha256_file(manifest_path):
        raise ValueError("Seal de entrega incorrecto")
    if seal.get("artifacts_verified") is not True or manifest.get("artifacts_sha256_verified") is not True:
        raise ValueError("Entrega no verificada por el workflow")
    if not manifest.get("status", "").startswith("COMPLETED"):
        raise ValueError("Workflow incompleto")
    interpretation_status = _read(delivery / "audit_interpretation_status.json")
    if interpretation_status.get("status") != "INTERPRETATION_COMPLETED":
        raise ValueError("Interpretación ausente o fallida")
    if not (delivery / "AUDIT_CONSOLIDATED.json").is_file() or not (delivery / "AUDIT_CONSOLIDATED.md").is_file():
        raise ValueError("Faltan informes de interpretación")
    if manifest["dataset_identity"]["source_sha256"] != digest:
        raise ValueError("Identidad de fuente incorrecta")
    artifacts = manifest["delivery_artifacts"]
    if not artifacts:
        raise ValueError("Entrega vacía")
    for name, expected in artifacts.items():
        target = (delivery / name).resolve()
        if not target.is_relative_to(delivery.resolve()):
            raise ValueError("Artefacto fuera de DELIVERY")
        if target.stat().st_size != expected["size_bytes"] or sha256_file(target) != expected["sha256"]:
            raise ValueError("Artefacto de entrega alterado")
    run_data = _read(delivery / "engine_run" / "run.json")
    if run_data.get("database", {}).get("status") != "PASS":
        raise PipelineFailure("Fallo de DuckDB sin resolver", "DUCKDB")
    if run_data.get("errors"):
        raise PipelineFailure("Fallo de pipeline sin resolver", "GTFS_ENGINE")
    engine_dir = delivery.parent / "audit" / "engine_runs" / run_data["run_id"]
    if not (engine_dir / "engine_report.json").is_file():
        raise ValueError("Falta evidencia interna del motor")
    return manifest, engine_dir


def _failure(case_id: str, index: int, phase: str, category: str, observed: str,
             *, status: str = "OPEN", historical: bool = False, **details: Any) -> dict[str, Any]:
    if category not in CATEGORIES or status not in FAILURE_STATUSES:
        raise ValueError("Categoría/estado de incidencia desconocido")
    allowed = {"root_cause", "root_cause_status", "resolution", "general_fix_required",
               "operator_specific", "resolved_in_version", "evidence_reference", "exception_type",
               "failure_type", "first_seen", "last_seen", "first_seen_case", "last_seen_case",
               "discovered_during_real_data_pilot"}
    if set(details) - allowed:
        raise ValueError("Campos de incidencia desconocidos")
    return {"failure_id": f"FAIL-{case_id}-{index:03d}", "case_id": case_id,
            "phase": phase, "category": category, "observed": observed, "status": status,
            "historical": historical, "recorded_at": _now(), "root_cause": None,
            "root_cause_status": "UNCONFIRMED", "resolution": None,
            "general_fix_required": "UNKNOWN", "operator_specific": False,
            "resolved_in_version": None, "first_seen": case_id, "last_seen": case_id,
            "first_seen_case": details.get("first_seen", case_id),
            "last_seen_case": details.get("last_seen", case_id),
            "TDL_version": BANK_VERSION, "tdl_commit": _tdl_revision(), **details}


def _delivery(case: Path, identity: dict[str, Any], workflow: Path, case_id: str) -> None:
    delivery = case / "DELIVERY"
    shutil.copytree(workflow, delivery / "workflow")
    metadata = identity["ORIGINAL_METADATA"]
    public = {"TDL_CASE_REFERENCE": case_id, "audit_reference": f"TDL-{case_id}", "original_filename": identity["original_filename"],
              "source_sha256": identity["sha256"], "source_size_bytes": identity["original_size"],
              "dataset_title": metadata.get("dataset_title"), "publisher": metadata.get("publisher"),
              "operator": metadata.get("operator"), "source_url": metadata.get("source_url"),
              "retrieved_time": metadata.get("retrieved_time"), "license_status": metadata.get("license_status")}
    _write(delivery / "original_identity.json", _redact_local_paths(public))
    title = _redact_path_text(str(metadata.get("dataset_title") or "Dataset")).replace("\n", " ").replace("\r", " ")
    safe_title = re.sub(r"[^\w-]+", "_", title, flags=re.UNICODE).strip("_")[:60] or "Dataset"
    report = (workflow / "report" / "client_report.md").read_text(encoding="utf-8")
    header = f"# {title}\n\nReferencia de auditoría: TDL-{case_id}\n\nArchivo original: {identity['original_filename']}\n\n"
    (delivery / f"{safe_title}_Auditoria_TDL.md").write_text(header + report, encoding="utf-8")
    artifacts = {p.relative_to(delivery).as_posix(): {"sha256": sha256_file(p), "size_bytes": p.stat().st_size}
                 for p in sorted(delivery.rglob("*")) if p.is_file()}
    _write(delivery / "bank_delivery_manifest.json", {"case_id": case_id, "artifacts": artifacts})
    _write(delivery / "bank_delivery_seal.json", {"manifest_sha256": sha256_file(delivery / "bank_delivery_manifest.json")})


def run_case(source: Path, bank: Path, *, metadata: dict[str, Any] | None = None,
             provenance: str = "CLIENT_PROVIDED", historical_failures: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source, bank = source.resolve(), bank.resolve()
    metadata = dict(metadata or {})
    allowed_metadata = {"dataset_title", "publisher", "operator", "source_url", "retrieved_time",
                        "license_status", "known_friction", "prior_case_id", "metadata_evidence"}
    if set(metadata) - allowed_metadata or any(value is not None and not isinstance(value, str) for value in metadata.values()):
        raise ValueError("Los metadatos deben usar los campos de texto admitidos en el contrato")
    if not source.is_file() or source.suffix.lower() != ".zip":
        raise ValueError("Se requiere un ZIP existente")
    if source.is_relative_to(bank):
        raise ValueError("La entrada debe estar fuera del banco; no modificar expedientes previos")
    if provenance not in {"CLIENT_PROVIDED", "PUBLIC_AUTHORIZED", "SYNTHETIC", "DEVELOPMENT"}:
        raise ValueError("Procedencia desconocida")
    # Capture original identity before normalization and ID allocation.
    identity = _capture(source, metadata)
    json.dumps(identity)  # Reject non-serializable metadata before reserving a case.
    for event in historical_failures or []:
        _failure("00000", 1, **event)
    with _locked(bank):
        reservations = bank / "REGISTRY" / "RESERVATIONS"
        reservations.mkdir(exist_ok=True)
        used = [int(p.name) for p in reservations.iterdir() if re.fullmatch(r"\d{5}", p.name)]
        used += [int(row["case_id"]) for row in _rebuild(bank)]
        number = max(used, default=0) + 1
        if number > 99999:
            raise ValueError("Espacio de IDs agotado; no se reutilizan códigos")
        case_id = f"{number:05d}"
        (reservations / case_id).mkdir()
        case = bank / "ACTIVE" / case_id
        case.mkdir()
        for zone in ("SOURCE", "WORKING", "AUDIT", "DELIVERY", "EVIDENCE"):
            (case / zone).mkdir()
        identity["case_id"] = case_id
        _write(case / "EVIDENCE" / "original_identity.json", identity)
        record = {"version": BANK_VERSION, "case_id": case_id, "dataset_title": metadata.get("dataset_title"),
                  "format": "GTFS", "original_filename": source.name, "source_sha256": identity["sha256"],
                  "dataset_sha256": identity["sha256"], "original_metadata": metadata,
                  "tdl_version": BANK_VERSION, "tdl_commit": _tdl_revision(),
                  "controlled_short_workspace": True,
                  "started_at": _now(), "finished_at": None, "result": "ACTIVE", "replay": "NOT_RUN",
                  "case_result": "ACTIVE", "audit_result": "NOT_RUN", "replay_result": "NOT_RUN", "finding_count": None,
                  "audit_status": "NOT_RUN", "findings": None, "pipeline_failures": 0,
                  "historical_pipeline_failures": len(historical_failures or []),
                  "known_friction": metadata.get("known_friction"), "code_changes_required": "NO",
                  "operator_specific_code": "NO", "gates": {key: False for key in GATES},
                  "failures": [_failure(case_id, i, historical=True, **event) for i, event in enumerate(historical_failures or [], 1)]}
        gates = record["gates"]
        gates.update(SOURCE_CAPTURED=True, SOURCE_HASHED=True)
        _write(case / "case.json", record)
        _rebuild(bank)
        phase, category = "SOURCE_FREEZE", "FILESYSTEM"
        frozen = case / "SOURCE" / f"{case_id}.zip"
        try:
            shutil.copyfile(source, frozen)
            if sha256_file(frozen) != identity["sha256"]:
                raise ValueError("SOURCE no conserva los bytes capturados")
            frozen.chmod(stat.S_IREAD)
            phase, category = "PREFLIGHT", "ZIP"
            _write(case / "EVIDENCE" / "preflight.json", _preflight(frozen))
            gates["PREFLIGHT_COMPLETED"] = True
            outcomes, engine_dirs = [], []
            for attempt in ("a", "b"):
                phase, category = f"AUDIT_{attempt.upper()}", "GTFS_ENGINE"
                result = run_client_audit(frozen, case / "WORKING" / attempt,
                                          client_project_id="T", audit_id=case_id,
                                          source_provenance=provenance)
                _write(case / "AUDIT" / f"{attempt}_result.json", result)
                if not result.get("status", "").startswith("COMPLETED"):
                    raise ValueError(f"Workflow bloqueado: {result}")
                workflow = Path(result["delivery_directory"])
                phase, category = "VERIFY_WORKFLOW", "DELIVERY"
                manifest, engine_dir = _verify_workflow(workflow, identity["sha256"])
                engine_dirs.append(engine_dir)
                outcomes.append(result)
                if attempt == "a":
                    gates["AUDIT_COMPLETED"] = True
                    gates["FINDINGS_GENERATED"] = (workflow / "findings.json").is_file()
                    gates["INTERPRETATION_COMPLETED"] = (workflow / "audit_interpretation_status.json").is_file()
                    gates["REPORT_GENERATED"] = (workflow / "report" / "client_report.md").is_file()
                    record.update(audit_status=manifest["status"], findings=result["findings_count"])
                    initial_workflow = workflow
            phase, category = "REPLAY", "REPLAY"
            _mark_stage("REPLAY", "START")
            hashes = [sha256_file(path / "engine_report.json") for path in engine_dirs]
            interpretation_paths = [Path(outcome["delivery_directory"]) / "AUDIT_CONSOLIDATED.json" for outcome in outcomes]
            interpretation_results = [_read(path) for path in interpretation_paths]
            interpretation_fingerprints = [semantic_fingerprint(item) for item in interpretation_results]
            replay_pass = (hashes[0] == hashes[1] and outcomes[0]["findings_count"] == outcomes[1]["findings_count"]
                           and interpretation_fingerprints[0] == interpretation_fingerprints[1])
            _write(case / "EVIDENCE" / "replay.json", {"status": "PASS" if replay_pass else "FAIL",
                   "source_sha256": identity["sha256"], "engine_report_sha256": hashes,
                   "interpretation_semantic_fingerprint": interpretation_fingerprints,
                   "scope": "SAME_SOURCE_ENGINE_REPORT_BYTES_FINDINGS_COUNT_AND_INTERPRETATION_SEMANTICS; EXECUTION_PROVENANCE_IDS_EXCLUDED"})
            record["replay"] = "PASS" if replay_pass else "FAIL"
            if not replay_pass:
                raise ValueError("Replay no reproducible")
            gates["REPLAY_COMPLETED"] = True
            gates["INTERPRETATION_REPLAY"] = interpretation_fingerprints[0] == interpretation_fingerprints[1]
            record["replay"] = "PASS"
            _mark_stage("REPLAY", "END")
            phase, category = "DELIVERY", "DELIVERY"
            _delivery(case, identity, initial_workflow, case_id)
            gates["DELIVERY_GENERATED"] = True
            phase, category = "SOURCE_VERIFY", "FILESYSTEM"
            gates["SOURCE_IMMUTABLE"] = sha256_file(frozen) == sha256_file(source) == identity["sha256"]
            if not gates["SOURCE_IMMUTABLE"]:
                raise ValueError("Fuente original/congelada alterada")
            gates["EVIDENCE_COMPLETE"] = True
            gates["NO_UNRESOLVED_PIPELINE_FAILURE"] = not any(event["status"] in {"OPEN", "UNDER_INVESTIGATION"} for event in record["failures"])
        except Exception as exc:
            if isinstance(exc, PipelineFailure):
                category = exc.category
            record["pipeline_failures"] += 1
            record["code_changes_required"] = "NO" if category == "ZIP" else "UNKNOWN"
            record["failures"].append(_failure(case_id, len(record["failures"]) + 1, phase, category, str(exc), exception_type=type(exc).__name__))
            try:
                gates["SOURCE_IMMUTABLE"] = frozen.is_file() and sha256_file(frozen) == sha256_file(source) == identity["sha256"]
            except OSError:
                gates["SOURCE_IMMUTABLE"] = False
        record["finished_at"] = _now()
        record["result"] = "OK" if all(gates.values()) else "NOT_OK"
        record.update(case_result=record["result"], audit_result=record["audit_status"],
                      replay_result=record["replay"], finding_count=record["findings"])
        destination = bank / record["result"] / f"{case_id}_{record['result']}"
        record["case_path"] = destination.relative_to(bank).as_posix()
        _mark_stage("CLEANUP", "START")
        _write(case / "case.json", record)
        # Paths in runner results remain observed historical paths. Resolve current
        # files relative to case_path; never rewrite the sealed workflow manifests.
        case.rename(destination)
        _rebuild(bank)
        _mark_stage("CLEANUP", "END")
        return record


def main() -> int:
    parser = argparse.ArgumentParser(description="TDL Real Dataset Test Bank V1")
    parser.add_argument("source", type=Path, nargs="?")
    parser.add_argument("--bank", type=Path, default=DEFAULT_TEST_BANK_ROOT)
    parser.add_argument("--metadata", type=Path, help="JSON local de metadatos originales")
    parser.add_argument("--historical-failures", type=Path, help="JSON local de incidencias históricas")
    parser.add_argument("--provenance", default="CLIENT_PROVIDED")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    try:
        if args.rebuild:
            rows = rebuild_register(args.bank)
            result = {"status": "REGISTRY_REBUILT", "cases": len(rows)}
        elif args.source:
            result = run_case(args.source, args.bank, metadata=_read(args.metadata) if args.metadata else None,
                              provenance=args.provenance,
                              historical_failures=_read(args.historical_failures) if args.historical_failures else None)
        else:
            parser.error("source es obligatorio salvo --rebuild")
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result.get("result") == "OK" or args.rebuild else 2
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
