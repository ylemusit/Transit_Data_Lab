"""Run the CS Autobuses synthetic factory ZIP through the TDL client workflow."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

from gtfs_lab.client_workflow import run_client_audit


TOOL_VERSION = "1.7.0"
CLIENT_ID = "CS-AUTOBUSES-DEMO"
AUDIT_ID = "E2E-CS-AUTOBUSES-FACTORY-V1"
EXPECTED_FILE_COUNT = 32
REQUIRED_FILES = {"agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt"}
TEXT_ARTIFACT_SUFFIXES = {".csv", ".geojson", ".html", ".json", ".kml", ".md", ".txt", ".xml", ".yaml", ".yml"}
LOCAL_PATH_PATTERN = re.compile(r"(?i)(?<![A-Z0-9])(?:[A-Z]:[\\/]|\\\\[^\\/\s]+[\\/][^\\/\s]+[\\/])")
KNOWN_ENUM_VALUES = {
    ("is_bidirectional", "1"): ("pathways.txt", "GTFS documenta 1 como bidireccional"),
    ("location_type", "1"): ("stops.txt", "GTFS documenta 1 como estación"),
    ("table_name", "agency"): ("translations.txt", "GTFS incluye agency entre los valores permitidos"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def generation_step_record(python_executable: str, generator: Path, flag: str, return_code: int, stdout: str) -> dict[str, Any]:
    stdout_bytes = stdout.encode("utf-8", errors="replace")
    return {
        "command": [Path(python_executable).name, generator.name, flag],
        "return_code": return_code,
        "stdout_sha256": hashlib.sha256(stdout_bytes).hexdigest(),
        "stdout_line_count": len(stdout.splitlines()),
    }


def workflow_delivery_relative_path(delivery_directory: str | None, evidence_root: Path) -> str | None:
    if not delivery_directory:
        return None
    evidence_root = evidence_root.resolve()
    delivery_path = Path(delivery_directory).resolve()
    if not delivery_path.is_relative_to(evidence_root):
        raise RuntimeError("La entrega del workflow quedó fuera de la carpeta de evidencia E2E.")
    return delivery_path.relative_to(evidence_root).as_posix()


def _extract_pdf_text(path: Path) -> str | None:
    from gtfs_lab.delivery_privacy import extract_pdf_text
    return extract_pdf_text(path)


def inspect_delivery_content(delivery_path: Path) -> dict[str, Any]:
    """Scan client-delivery text independently and report any unscanned PDF/binary files."""
    from gtfs_lab.delivery_privacy import inspect_delivery_content as inspect
    return inspect(delivery_path, pdf_extractor=_extract_pdf_text)


def inspect_factory_zip(path: Path) -> dict[str, Any]:
    """Check the known CS Autobuses demo package before giving it to the auditor."""
    if not path.is_file() or path.suffix.lower() != ".zip":
        raise ValueError("La entrada debe ser un ZIP existente.")
    if not zipfile.is_zipfile(path):
        raise ValueError("La entrada no es un ZIP válido.")

    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        files = [entry for entry in entries if not entry.is_dir()]
        names = [entry.filename for entry in files]
        if len(names) != len(set(names)):
            raise ValueError("El ZIP contiene nombres de archivo duplicados.")
        if any("/" in name or "\\" in name or name in {"", ".", ".."} for name in names):
            raise ValueError("Los archivos GTFS deben estar en la raíz del ZIP.")
        if any(entry.flag_bits & 0x1 for entry in files):
            raise ValueError("El ZIP cifrado no se admite en este E2E.")
        if len(files) != EXPECTED_FILE_COUNT:
            raise ValueError(f"Se esperaban {EXPECTED_FILE_COUNT} archivos; encontrados {len(files)}.")
        if not REQUIRED_FILES.issubset(set(names)) or "locations.geojson" not in names:
            raise ValueError("Faltan archivos esperados de la demostración CS Autobuses.")
        total_size = sum(entry.file_size for entry in files)
        if total_size > 100 * 1024 * 1024:
            raise ValueError("El ZIP supera el límite de 100 MiB de este E2E sintético.")
        bad_member = archive.testzip()
        if bad_member is not None:
            raise ValueError(f"CRC inválido en la entrada {bad_member!r}.")
        member_content_sha256 = {
            entry.filename: hashlib.sha256(archive.read(entry)).hexdigest()
            for entry in files
        }

    content_manifest = [
        {"name": name, "sha256": digest}
        for name, digest in sorted(member_content_sha256.items())
    ]
    content_manifest_sha256 = hashlib.sha256(
        json.dumps(content_manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return {
        "entry_count": len(files),
        "entries_at_zip_root": True,
        "duplicate_names": False,
        "crc_check": "PASS",
        "uncompressed_size_bytes": total_size,
        "member_content_sha256": member_content_sha256,
        "content_manifest_sha256": content_manifest_sha256,
    }


def runtime_audit_quality_root() -> Path:
    project_root = Path(__file__).resolve().parents[3]
    config_path = project_root / "config" / "tdl_paths.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    runtime_root = Path(config["TDL_RUNTIME_ROOT"]).resolve()
    return runtime_root / "AuditQuality" / "FactoryE2E"


def _reject_reparse(path: Path) -> None:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    if attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
        raise ValueError(f"No se admiten enlaces ni reparse points en las entradas de fábrica: {path.name}")


def reproduce_factory(factory_root: Path, working_root: Path) -> tuple[Path, dict[str, str], list[dict[str, Any]]]:
    """Copy only the generator and its direct origin files, then generate a fresh ZIP."""
    _reject_reparse(factory_root)
    factory_root = factory_root.resolve(strict=True)
    source_generator = factory_root / "generar_cs_autobuses.py"
    source_origins = factory_root / "origenes"
    _reject_reparse(source_generator)
    _reject_reparse(source_origins)
    if not stat.S_ISREG(source_generator.lstat().st_mode) or not stat.S_ISDIR(source_origins.lstat().st_mode):
        raise ValueError("Frabica_GTFS debe contener el generador y la carpeta origenes esperados.")

    origin_files = sorted(source_origins.iterdir(), key=lambda path: path.name.casefold())
    if not origin_files:
        raise ValueError("La carpeta origenes está vacía.")
    for path in origin_files:
        _reject_reparse(path)
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError(f"Solo se admiten archivos de origen directos: {path.name}")

    working_root.mkdir(parents=True, exist_ok=False)
    working_origins = working_root / "origenes"
    working_origins.mkdir()
    working_generator = working_root / source_generator.name
    source_files = [("generator/" + source_generator.name, source_generator)] + [
        ("origenes/" + path.name, path) for path in origin_files
    ]
    source_hashes = {name: sha256(path) for name, path in source_files}
    shutil.copyfile(source_generator, working_generator)
    for path in origin_files:
        shutil.copyfile(path, working_origins / path.name)

    steps = []
    for flag in ("--generar-gtfs", "--empaquetar-gtfs"):
        command = [sys.executable, str(working_generator), flag]
        completed = subprocess.run(command, cwd=working_root, capture_output=True, text=True, check=True)
        steps.append(generation_step_record(command[0], working_generator, flag, completed.returncode, completed.stdout))

    unchanged = all(sha256(path) == source_hashes[name] for name, path in source_files)
    if not unchanged:
        raise RuntimeError("Las fuentes originales de Frabica_GTFS cambiaron durante la reproducción.")
    generated_zip = working_root / "entregas" / "CS_Autobuses_GTFS_32_archivos_DEMOSTRACION.zip"
    if not generated_zip.is_file():
        raise RuntimeError("El generador no produjo el ZIP de demostración esperado.")
    return generated_zip, source_hashes, steps


def run(factory_root: Path, output: Path, *, professional: bool = False) -> dict[str, Any]:
    _reject_reparse(factory_root)
    factory_root = factory_root.resolve(strict=True)
    output = output.resolve()
    allowed_root = runtime_audit_quality_root().resolve()
    if not output.is_relative_to(allowed_root) or output == allowed_root:
        raise ValueError(f"La evidencia debe quedar bajo {allowed_root}.")
    if output.exists():
        raise FileExistsError(f"La carpeta de evidencia ya existe: {output}")

    output.mkdir(parents=True, exist_ok=False)
    source_zip, factory_source_hashes, generation_steps = reproduce_factory(
        factory_root, output / "factory_reproduction"
    )
    package_inventory = inspect_factory_zip(source_zip)
    source_sha = sha256(source_zip)
    workspace = output / "workflow"
    result = run_client_audit(
        source_zip,
        workspace,
        client_project_id=CLIENT_ID,
        audit_id=AUDIT_ID,
        source_provenance="SYNTHETIC",
        client_metadata={"company_name": "CS Autobuses", "scenario": "FACTORY_DEMONSTRATION"},
        audit_mode="INITIAL",
    )

    checks: dict[str, bool] = {
        "factory_zip_inventory": package_inventory["entry_count"] == EXPECTED_FILE_COUNT,
        "factory_source_unchanged": all(
            sha256(
                factory_root / Path(name).name
                if name.startswith("generator/")
                else factory_root / "origenes" / Path(name).name
            ) == expected
            for name, expected in factory_source_hashes.items()
        ),
        "generated_zip_unchanged": sha256(source_zip) == source_sha,
        "audit_used_generated_zip": result.get("source_sha256") == source_sha,
        "workflow_completed": str(result.get("status", "")).startswith("COMPLETED"),
        "source_immutable": result.get("source_immutable") is True,
        "delivery_hashes_verified": result.get("artifacts_sha256_verified") is True,
    }
    delivery_relative_path = workflow_delivery_relative_path(result.get("delivery_directory"), output)
    delivery_path = output / delivery_relative_path if delivery_relative_path is not None else None
    checks["workflow_delivery_within_evidence_root"] = delivery_relative_path is not None
    manifest_sha = None
    pdf_status = None
    delivery_content_scan: dict[str, Any] = {
        "status": "NOT_RUN", "text_files_scanned": 0, "pdf_files": 0,
        "pdf_text_scan": "NOT_RUN", "opaque_files_not_text_scanned": 0, "path_matches": [],
    }
    known_validator_discrepancies: list[dict[str, str]] = []
    if delivery_path is not None and delivery_path.is_dir():
        manifest_path = delivery_path / "audit_manifest.json"
        seal_path = delivery_path / "delivery_seal.json"
        required_artifacts = [
            manifest_path,
            seal_path,
            delivery_path / "report" / "client_report.json",
            delivery_path / "report" / "client_report.md",
            delivery_path / "report" / "client_report.pdf",
            delivery_path / "AUDIT_CONSOLIDATED.json",
            delivery_path / "findings.json",
        ]
        checks["client_audit_artifacts_present"] = all(path.is_file() for path in required_artifacts)
        delivery_content_scan = inspect_delivery_content(delivery_path)
        checks["text_artifact_paths_absent"] = not delivery_content_scan["path_matches"]
        if manifest_path.is_file() and seal_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            seal = json.loads(seal_path.read_text(encoding="utf-8"))
            manifest_sha = sha256(manifest_path)
            checks["manifest_matches_source"] = manifest.get("dataset_identity", {}).get("source_sha256") == source_sha
            checks["delivery_seal_valid"] = seal.get("audit_manifest_sha256") == manifest_sha
            from gtfs_lab.delivery_integrity import verify_delivery
            try:
                verify_delivery(delivery_path)
                checks["delivery_inventory_valid"] = True
            except (ValueError, OSError, KeyError):
                checks["delivery_inventory_valid"] = False
            checks["manifest_declares_no_external_upload"] = manifest.get("security", {}).get("external_upload") is False
            checks["manifest_declares_no_local_paths"] = manifest.get("security", {}).get("local_paths_in_delivery") is False
            checks["manifest_sha256_verified"] = result.get("audit_manifest_sha256") == manifest_sha
        pdf_status_path = delivery_path / "report" / "pdf_generation_status.json"
        if pdf_status_path.is_file():
            pdf_status = json.loads(pdf_status_path.read_text(encoding="utf-8")).get("status")
        checks["pdf_generated"] = pdf_status == "GENERATED"
        findings_path = delivery_path / "findings.json"
        if findings_path.is_file():
            finding_rows = json.loads(findings_path.read_text(encoding="utf-8")).get("findings", [])
            for finding in finding_rows:
                rule_id = str(finding.get("rule_id", ""))
                field = str(finding.get("field", ""))
                observed = str(finding.get("observed", ""))
                known = KNOWN_ENUM_VALUES.get((field, observed))
                if rule_id == "GTFS-G03-FIELD-TYPE" and known:
                    filename, basis = known
                    known_validator_discrepancies.append({
                        "rule_id": rule_id,
                        "file": filename,
                        "field": field,
                        "observed": observed,
                        "assessment": "REVIEW_REQUIRED; este valor está permitido por la referencia GTFS consultada, por lo que el hallazgo de tipo no se debe entregar como defecto confirmado.",
                        "basis": basis,
                    })
    else:
        checks["client_audit_artifacts_present"] = False
        checks["text_artifact_paths_absent"] = False
        checks["delivery_seal_valid"] = False
        checks["delivery_inventory_valid"] = False
        checks["manifest_declares_no_external_upload"] = False
        checks["manifest_declares_no_local_paths"] = False
        checks["manifest_sha256_verified"] = False
        checks["pdf_generated"] = False

    checks["delivery_content_scan_complete"] = delivery_content_scan["status"] == "PASS"
    checks["no_known_validator_discrepancies"] = not known_validator_discrepancies
    presentation_status = "NOT_RUN"
    presentation_path = None
    if professional and checks["delivery_inventory_valid"]:
        from gtfs_lab.professional_audit import generate, verify_package
        generated = generate(delivery_path, output / "professional", "CS-AUTOBUSES-DEMO-R1", source_zip)
        presentation_status = generated["status"]
        presentation_path = "professional"
        checks["professional_package_verified"] = verify_package(output / "professional") > 0
    elif professional:
        checks["professional_package_verified"] = False
    use_readiness_reasons = ["El conjunto de entrada y la entidad son sintéticos; no representan un operador ni un servicio real."]
    if known_validator_discrepancies:
        use_readiness_reasons.append(
            f"{len(known_validator_discrepancies)} hallazgos GTFS-G03-FIELD-TYPE usan valores enumerados permitidos y requieren revisión antes de cualquier entrega."
        )
    use_readiness_reasons.append("La emisión requiere revisión humana del caso, alcance y destinatario.")
    if delivery_content_scan["status"] == "PARTIAL_UNSCANNED_CONTENT":
        use_readiness_reasons.append(
            "La inspección independiente de rutas locales cubre texto, pero el runtime actual no permite extraer texto del PDF y quedan ficheros opacos sin revisar."
        )
    if delivery_content_scan["status"] == "FAIL_PATH_FOUND":
        use_readiness_reasons.append("La inspección independiente detectó rutas locales en artefactos de la entrega.")
    if presentation_status == "NOT_RUN":
        use_readiness_reasons.append("La presentación profesional completa no se ha generado en esta pasada.")

    receipt = {
        "contract": "TDL_CS_AUTOBUSES_FACTORY_CLIENT_E2E",
        "version": TOOL_VERSION,
        "e2e_runner_sha256": sha256(Path(__file__)),
        "scenario": "SYNTHETIC_DEMONSTRATION",
        "company_name": "CS Autobuses",
        "source_provenance": "SYNTHETIC",
        "factory_source_id": factory_root.name,
        "factory_source_files_sha256": factory_source_hashes,
        "generation_steps": generation_steps,
        "source_sha256": source_sha,
        "factory_zip_inventory": package_inventory,
        "workflow": {
            "status": result.get("status"),
            "audit_id": result.get("audit_id"),
            "source_sha256": result.get("source_sha256"),
            "source_immutable": result.get("source_immutable"),
            "artifacts_sha256_verified": result.get("artifacts_sha256_verified"),
            "artifact_count": result.get("artifact_count"),
            "findings_count": result.get("findings_count"),
            "audit_manifest_sha256": result.get("audit_manifest_sha256"),
            "delivery_relative_path": delivery_relative_path,
        },
        "delivery_manifest_sha256": manifest_sha,
        "pdf_status": pdf_status,
        "professional_presentation_status": presentation_status,
        "professional_presentation_relative_path": presentation_path,
        "demo_use_readiness": "INTERNAL_DEMO_READY_WITH_LIMITATIONS" if professional and all(checks.values()) else "INCOMPLETE",
        "publication_readiness": "NOT_EVALUATED; aceptación NAP separada de la auditoría previa a publicación",
        "known_validator_discrepancies": known_validator_discrepancies,
        "delivery_content_scan": delivery_content_scan,
        "client_use_readiness": {"status": "BLOCKED_FOR_CLIENT_ISSUANCE", "reasons": use_readiness_reasons},
        "checks": checks,
        "e2e_status": "PASS" if all(checks.values()) else "FAIL",
        "scope_limit": "La salida demuestra el recorrido interno sintético; no acredita fuentes reales, cobertura universal, conformidad jurídica, aceptación NAP ni autorización de emisión a un cliente.",
    }
    write_json(output / "E2E_RECEIPT.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--factory-root", type=Path, required=True, help="raíz de Frabica_GTFS con el generador y origenes/")
    parser.add_argument("--output", type=Path, required=True, help="directorio nuevo bajo 04_Runtime/AuditQuality/FactoryE2E")
    parser.add_argument("--professional", action="store_true", help="generar y verificar también dos PDF, libro y KMZ")
    args = parser.parse_args()
    try:
        receipt = run(args.factory_root, args.output, professional=args.professional)
    except Exception as exc:
        print(json.dumps({"e2e_status": "FAIL", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"e2e_status": receipt["e2e_status"], "receipt": str(args.output.resolve() / "E2E_RECEIPT.json"),
                      "audit_status": receipt["workflow"].get("status"), "checks": receipt["checks"]}, ensure_ascii=False))
    return 0 if receipt["e2e_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
