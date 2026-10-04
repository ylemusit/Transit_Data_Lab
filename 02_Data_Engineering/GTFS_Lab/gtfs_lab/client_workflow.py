"""Local, reproducible GTFS client audit packaging over the closed V1 engines."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import VERSION
from .audit_comparison import ComparisonError, compare_audit_directories
from .core import sha256_file
from .ingestion import IngestionError
from .interpretation.consolidation import build_result as build_interpretation
from .interpretation.reporting import write_reports as write_interpretation_reports
from .pipeline import run

WORKFLOW_VERSION = "1.0.0"
_LARGE_JSON_STREAM_THRESHOLD = 8 * 1024 * 1024
_JSON_STRING_TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"')
STATUSES = {"COMPLETED", "COMPLETED_WITH_FINDINGS", "COMPLETED_WITH_LIMITATIONS",
            "BLOCKED_INPUT_INVALID", "BLOCKED_TECHNICAL", "HUMAN_REVIEW_REQUIRED"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return sha256_file(path)


def _mapping_sha256(value: dict[str, str]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _tdl_ref() -> str:
    """Identify the executing checkout when Git metadata is available."""
    try:
        root = Path(__file__).resolve().parent
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root,
                                       text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=root,
                                        text=True, stderr=subprocess.DEVNULL).strip()
        return head + ("+WORKTREE_DIRTY" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def _redact_local_paths(value: Any) -> Any:
    """Keep local execution paths out of customer artifacts."""
    if isinstance(value, dict):
        return {key: _redact_local_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_local_paths(item) for item in value]
    if isinstance(value, str):
        return _redact_path_text(value)
    return value


def _redact_path_text(value: str) -> str:
    value = re.sub(r"(?i)\b[A-Z]:\\[^\s`\"']*", "[LOCAL_PATH_REDACTED]", value)
    return re.sub(r"(?<![\w:/])/(?:[^/\s\"'`<>]+/)*[^/\s\"'`<>]+", "[LOCAL_PATH_REDACTED]", value)


def _sanitize_large_json(path: Path) -> None:
    """Redact JSON strings line by line without materializing large artifacts."""
    temporary = path.with_name(path.name + ".redacted.tmp")
    try:
        with path.open("r", encoding="utf-8", newline="") as source, temporary.open(
                "w", encoding="utf-8", newline="") as target:
            for line in source:
                def redact(match: re.Match[str]) -> str:
                    token = match.group(0)
                    value = json.loads(token)
                    # _redact_local_paths leaves object keys unchanged.
                    if line[match.end():].lstrip().startswith(":") or not isinstance(value, str):
                        return token
                    sanitized = _redact_path_text(value)
                    return json.dumps(sanitized, ensure_ascii=False) if sanitized != value else token

                target.write(_JSON_STRING_TOKEN.sub(redact, line))
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _sanitize_delivery(directory: Path) -> set[Path]:
    streamed_json: set[Path] = set()
    for path in directory.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".csv"}:
            continue
        try:
            if path.suffix.lower() == ".json" and path.stat().st_size > _LARGE_JSON_STREAM_THRESHOLD:
                _sanitize_large_json(path)
                streamed_json.add(path.resolve())
                continue
            text = path.read_text(encoding="utf-8")
            if path.suffix.lower() == ".json":
                text = json.dumps(_redact_local_paths(json.loads(text)), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
            else:
                text = _redact_path_text(text)
            path.write_text(text, encoding="utf-8")
        except (UnicodeError, json.JSONDecodeError):
            # Non-text engine outputs are not expected to contain path strings.
            continue
    return streamed_json


def _finding_rows(run: dict[str, Any], source_sha: str) -> list[dict[str, Any]]:
    """Preserve native engine, Compliance, and legacy origins as separate rows."""
    rows: list[dict[str, Any]] = []
    engine_statuses = {
        (str(stage.get("stage", "")), str(rule.get("rule_id", ""))): rule.get("status")
        for stage in run.get("engine_report", {}).get("technical_evaluation", {}).get("stages", [])
        for rule in stage.get("rules", [])
    }
    legacy_statuses = {str(rule.get("rule_id")): rule.get("status")
                       for rule in run.get("validation", {}).get("rules", [])}

    def envelope(origin: str, finding: dict[str, Any], status: str | None,
                 eligibility: str = "HUMAN_REVIEW") -> dict[str, Any]:
        evidence = finding.get("evidence") if isinstance(finding.get("evidence"), dict) else {}
        return {"origin": origin, **finding,
                "rule_version": finding.get("rule_version", finding.get("semantic_version", finding.get("version"))),
                "authority": finding.get("authority"), "severity": finding.get("severity"),
                "requirement": finding.get("requirement"), "technical_status": status,
                "file": finding.get("source_file", finding.get("file", finding.get("table"))),
                "row_locator": finding.get("row_locator", finding.get("record_locator", finding.get("locator"))),
                "field": finding.get("field"),
                "observed_evidence": finding.get("observed_value", finding.get("observed", evidence)),
                "recommendation": finding.get("recommendation", finding.get("expected_condition")),
                "remediation_eligibility": eligibility,
                "provenance": {"origin": origin, "source_sha256": source_sha,
                               "audit_id": run.get("run_id"),
                               "native_evidence": evidence},
                "source_sha256": source_sha}

    engine = run.get("engine_report", {})
    for finding in engine.get("technical_evaluation", {}).get("findings", []):
        status = engine_statuses.get((str(finding.get("stage", "")), str(finding.get("rule_id", ""))))
        rows.append(envelope("AUDIT_ENGINE", finding, status))
    for finding in engine.get("recommendation_findings", []):
        rows.append(envelope("AUDIT_ENGINE_RECOMMENDATION", finding, finding.get("status", "INFO"), "OUT_OF_SCOPE"))
    compliance = run.get("compliance_v1", {})
    for finding in compliance.get("findings", []):
        rows.append(envelope("COMPLIANCE", {"rule_id": compliance.get("rule_id"),
                     "rule_version": compliance.get("rule_version"), "authority": "COMPLIANCE_V1",
                     "severity": "ERROR", **finding}, compliance.get("result")))
    compliance_fingerprints = {
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for item in compliance.get("findings", [])
    }
    validation = run.get("validation", {})
    for finding in validation.get("findings", []):
        if json.dumps(finding, ensure_ascii=False, sort_keys=True, separators=(",", ":")) in compliance_fingerprints:
            continue
        rows.append(envelope("LEGACY", finding, legacy_statuses.get(str(finding.get("rule_id")))))
    # Keep exact occurrences and origin; do not claim equivalence or merge semantics.
    return rows


def _client_report(manifest: dict[str, Any], run: dict[str, Any], findings: list[dict[str, Any]],
                   remediation: dict[str, Any], comparison: dict[str, Any] | None) -> str:
    identity = manifest["dataset_identity"]
    summary = run.get("summary", {})
    limitations = ["La evaluación es técnica; no acredita certificación ni cumplimiento jurídico definitivo.",
                   "NOT_EVALUABLE, NOT_APPLICABLE, errores de inspección y alcance diferido conservan sus estados.",
                   "El validador legacy, Audit Engine y Compliance se presentan como orígenes separados.",
                   "GIS se genera por el runner técnico; su presencia no es necesaria para aceptar cada finding."]
    lines = ["# Informe de auditoría GTFS para cliente", "",
             f"- Estado del workflow: `{manifest['status']}`",
             f"- Identificador de auditoría: `{manifest['audit_id']}`",
             f"- Identificador cliente/proyecto: `{manifest['client_project_id']}`",
             f"- Dataset: `{identity['dataset_id']}`",
             f"- Archivo fuente: `{identity['source_filename']}`",
             f"- SHA-256 de SOURCE: `{identity['source_sha256']}`",
             f"- Recibido UTC: `{identity['ingestion_timestamp_utc']}`", "",
             "## 1. Resumen ejecutivo", "",
             f"Resultado técnico: `{summary.get('validation', 'NOT_EVALUABLE')}`; hallazgos consolidados: {len(findings)}.",
             "No se calcula una puntuación global.", "",
             "## 2. Identidad del dataset", "",
             f"Tamaño: {identity['source_size_bytes']} bytes. Procedencia declarada: {identity['source_provenance']}.", "",
             "## 3. Alcance", "",
             "GTFS Schedule mediante GTFS Audit Engine V1, Compliance V1 y salidas legacy identificadas por separado.", "",
             "## 4. Metodología", "",
             f"Workflow `{WORKFLOW_VERSION}`; GTFS_Lab `{VERSION}`. Se conservó una copia inmutable de entrada y se verificó SHA-256 antes y después.", "",
             "## 5. Hallazgos técnicos", "",
             f"Hallazgos Audit Engine: {sum(x['origin'] == 'AUDIT_ENGINE' for x in findings)}; legacy: {sum(x['origin'] == 'LEGACY' for x in findings)}.", "",
             "## 6. Calidad de datos", "",
             f"Validación legacy: `{summary.get('validation', 'NOT_EVALUABLE')}`.", "",
             "## 7. Alineación Compliance", "",
             f"Compliance V1: `{run.get('compliance_v1', {}).get('result', 'NOT_EVALUABLE')}`; el resultado no es una conclusión jurídica.", "",
             "## 8. Evaluación de remediación", "",
             f"Decisión: `{remediation['decision']}`. {remediation['reason']}", "",
             "## 9. Before / After", "",
             (f"Comparación: `{comparison.get('status', 'UNKNOWN')}`." if comparison else "No hubo remediación derivada; no aplica comparación before/after."), "",
             "## 10. Evidencia geográfica", "",
             "Las exportaciones GIS se incluyen cuando las produjo el motor; QGIS no es requisito del workflow.", "",
             "## 11. Limitaciones conocidas", "", *[f"- {item}" for item in limitations], "",
             "## 12. Alcance diferido", "",
             "NeTEx, SIRI, GTFS-RT, certificación y resolución jurídica quedan fuera de esta auditoría GTFS V1.", "",
             "## 13. Recomendaciones", "",
             "Revisar findings y estados no evaluables con evidencia contextual del titular del feed.", "",
             "## 14. Evidencia y reproducibilidad", "",
             "El paquete incluye identidad, salidas del motor, findings por origen, manifests y SHA-256 de artefactos.", "",
             "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""]
    return "\n".join(lines)


def run_client_audit(source_zip: Path, workspace: Path, *, client_project_id: str,
                     audit_id: str, source_provenance: str = "CLIENT_PROVIDED",
                     client_metadata: dict[str, Any] | None = None,
                     audit_mode: str = "INITIAL", baseline_run: Path | None = None,
                     derived_zip: Path | None = None) -> dict[str, Any]:
    """Run a single local audit and produce a hash-verified delivery directory."""
    source_zip = source_zip.resolve()
    workspace = workspace.resolve()
    if not source_zip.is_file() or source_zip.suffix.lower() != ".zip":
        raise ValueError("BLOCKED_INPUT_INVALID: se requiere un archivo GTFS.zip existente")
    for value, label in ((client_project_id, "client_project_id"), (audit_id, "audit_id")):
        if (not isinstance(value, str) or not value.strip() or value.strip() in {".", ".."}
                or any(ord(ch) < 32 for ch in value) or any(ch in value for ch in "\\/:")):
            raise ValueError(f"BLOCKED_INPUT_INVALID: {label} debe ser un identificador local válido")
    if workspace.exists() and any(workspace.iterdir()):
        raise FileExistsError(f"el workspace ya existe y no está vacío: {workspace}")
    if source_provenance not in {"CLIENT_PROVIDED", "PUBLIC_AUTHORIZED", "SYNTHETIC", "DEVELOPMENT"}:
        raise ValueError("source_provenance debe declarar un origen permitido")
    if audit_mode not in {"INITIAL", "MAINTENANCE", "RECURRING"}:
        raise ValueError("audit_mode no pertenece al contrato V1")
    if audit_mode == "RECURRING" and baseline_run is None:
        raise ValueError("audit_mode RECURRING requiere baseline_run")
    if derived_zip is not None and baseline_run is None:
        raise ValueError("un dataset DERIVED requiere baseline_run para before/after")
    if client_metadata and any(re.search(r"secret|token|password|credential|api[_-]?key", str(key), re.I)
                               for key in client_metadata):
        raise ValueError("client_metadata no admite campos con nombres de secretos o credenciales")

    started = _utc_now()
    source_sha = _sha256(source_zip)
    source_size = source_zip.stat().st_size
    root = workspace / client_project_id / audit_id
    zones = {name: root / name.lower() for name in ("SOURCE", "WORKING", "DERIVED", "AUDIT", "DELIVERY")}
    for zone in zones.values():
        zone.mkdir(parents=True, exist_ok=False)
    frozen_source = zones["SOURCE"] / source_zip.name
    shutil.copyfile(source_zip, frozen_source)
    if _sha256(frozen_source) != source_sha or frozen_source.stat().st_size != source_size:
        raise RuntimeError("BLOCKED_TECHNICAL: SOURCE freeze no conserva hash/tamaño")

    identity = {"client_project_id": client_project_id, "audit_id": audit_id,
                "dataset_id": "GTFS-" + source_sha[:16], "source_filename": source_zip.name,
                "ingestion_timestamp_utc": started, "source_sha256": source_sha,
                "source_size_bytes": source_size, "source_provenance": source_provenance,
                "optional_client_metadata": client_metadata or {}, "audit_mode": audit_mode,
                "workflow_version": WORKFLOW_VERSION}
    _write_json(zones["AUDIT"] / "dataset_identity.json", identity)

    try:
        if derived_zip is not None:
            candidate = derived_zip.resolve()
            if not candidate.is_file() or candidate == frozen_source.resolve():
                raise ValueError("derived_zip debe apuntar a un archivo DERIVED existente y distinto de SOURCE")
            working_input = zones["DERIVED"] / candidate.name
            shutil.copyfile(candidate, working_input)
        else:
            working_input = zones["WORKING"] / source_zip.name
            shutil.copyfile(frozen_source, working_input)
        result = run(working_input, zones["AUDIT"] / "engine_runs")
        engine_run_dir = zones["AUDIT"] / "engine_runs" / result["run_id"]
        # pipeline.run already returns the full run mapping. Reloading run.json
        # duplicates potentially multi-gigabyte findings in memory on large feeds.
        run_json = result
        engine_json_path = engine_run_dir / "engine_report.json"
        engine_report = json.loads(engine_json_path.read_text(encoding="utf-8"))
        run_json["engine_report"] = engine_report
        findings = _finding_rows(run_json, result["dataset"]["source_sha256"])
        interpretation_status: dict[str, Any]
        interpretation_result = None
        try:
            interpretation_result = build_interpretation(
                dataset_identity={"dataset_id": result["dataset"]["dataset_id"],
                                  "sha256": result["dataset"]["source_sha256"]},
                audit_execution_id=str(result["run_id"]), engine_version=VERSION,
                findings=findings, zip_path=str(working_input), tdl_ref=_tdl_ref())
            write_interpretation_reports(zones["AUDIT"], interpretation_result)
            interpretation_status = {"status": "INTERPRETATION_COMPLETED",
                                     "interpretation_status": interpretation_result["interpretation_status"],
                                     "accounting_gap": interpretation_result["coverage"]["accounting_gap"]}
        except Exception as exc:
            # Preserve completed audit evidence when the derived layer fails.
            interpretation_status = {"status": "INTERPRETATION_FAILED",
                                     "error_type": type(exc).__name__, "message": str(exc)}
        _write_json(zones["AUDIT"] / "audit_interpretation_status.json", interpretation_status)

        remediation = ({"decision": "HUMAN_REVIEW", "reason": "La selección de cambios depende de evidencia y autorización humana caso por caso; no se ejecutó remediación automática genérica."}
                      if findings else {"decision": "NOT_REMEDIABLE", "reason": "No hay findings que evaluar para remediación."})
        comparison = None
        if baseline_run is not None:
            comparison = compare_audit_directories(baseline_run.resolve(), engine_run_dir)

        _write_json(zones["AUDIT"] / "findings.json", {"contract": "TDLClientFindings", "version": "1.0.0", "source_sha256": result["dataset"]["source_sha256"], "findings": findings})
        _write_json(zones["AUDIT"] / "compliance.json", run_json.get("compliance_v1", {}))
        _write_json(zones["AUDIT"] / "remediation.json", remediation)
        if comparison is not None:
            _write_json(zones["AUDIT"] / "reaudit_comparison.json", comparison)

        statuses = [result.get("summary", {}).get("validation", "NOT_EVALUABLE"), result.get("summary", {}).get("compliance_v1", "NOT_EVALUABLE")]
        has_gap = (any(value in {"NOT_EVALUABLE", "INSPECTION_ERROR", "NOT_APPLICABLE"} for value in statuses)
                   or bool(engine_report.get("known_gaps")))
        final_status = "COMPLETED_WITH_FINDINGS" if findings else "COMPLETED_WITH_LIMITATIONS" if has_gap else "COMPLETED"
        if comparison and comparison.get("comparability", {}).get("status") == "NOT_COMPARABLE":
            final_status = "HUMAN_REVIEW_REQUIRED"
        if final_status not in STATUSES:
            raise RuntimeError(f"unsupported workflow status: {final_status}")
        legacy_rule_versions = {
            str(row.get("rule_id")): str(row.get("version"))
            for row in result.get("validation", {}).get("rules", []) if row.get("rule_id") and row.get("version")}
        engine_rule_versions = {
            rule["rule_id"]: str(rule.get("semantic_version") or "UNKNOWN")
            for stage in engine_report.get("technical_evaluation", {}).get("stages", [])
            for rule in stage.get("rules", []) if rule.get("rule_id")}
        compliance_identity = run_json.get("compliance_v1", {})
        manifest: dict[str, Any] = {"contract": "TDLClientAuditManifest", "version": "1.0.0",
            "status": final_status, "audit_id": audit_id, "client_project_id": client_project_id,
            "created_at_utc": started, "completed_at_utc": _utc_now(), "audit_mode": audit_mode,
            "dataset_identity": identity, "engine_versions": {"gtfs_lab": VERSION, "client_workflow": WORKFLOW_VERSION},
            "rule_registry_identities": {
                "legacy_validator": {"identity_type": "executed_rule_version_map",
                    "rule_versions": legacy_rule_versions, "sha256": _mapping_sha256(legacy_rule_versions)},
                "audit_engine": {"identity_type": "executed_rule_version_map",
                    "rule_versions": engine_rule_versions, "sha256": _mapping_sha256(engine_rule_versions)},
                "compliance": {"rule_id": compliance_identity.get("rule_id"),
                    "rule_version": compliance_identity.get("rule_version"),
                    "evaluator_version": compliance_identity.get("evaluator_version"),
                    "evaluator_sha256": compliance_identity.get("evaluator_sha256"),
                    "reference_sha256": compliance_identity.get("reference_sha256")}},
            "compliance_version": compliance_identity.get("evaluator_version"),
            "remediation_version": "TDL_REMEDIATION_ENGINE_V1/1.0.0",
            "audit_interpretation": {"status": interpretation_status["status"],
                "contract_version": "1.0.0", "accounting_gap": interpretation_status.get("accounting_gap"),
                "raw_findings_preserved": True},
            "remediation_decision": remediation["decision"],
            "known_gaps": engine_report.get("known_gaps", []),
            "deferred_capabilities": engine_report.get("deferred_features", []),
            "delivery_artifacts": {},
            "security": {"external_upload": False, "source_immutable": True, "local_paths_in_delivery": False}}
        delivery = zones["DELIVERY"]
        shutil.copytree(engine_run_dir, delivery / "engine_run")
        (delivery / "report").mkdir()
        report_text = _client_report(manifest, run_json, findings, remediation, comparison)
        report_text = report_text.replace("## 12. Alcance diferido", (
            "## Interpretación derivada\n\n"
            f"Estado: `{interpretation_status['status']}`; contrato: `1.0.0`. "
            "El resultado de auditoría y su interpretación permanecen identificados por separado.\n\n"
            "## 12. Alcance diferido"))
        (delivery / "report" / "client_report.md").write_text(report_text, encoding="utf-8")
        for name, path in (("dataset_identity.json", zones["AUDIT"] / "dataset_identity.json"),
                           ("findings.json", zones["AUDIT"] / "findings.json"),
                           ("audit_interpretation_status.json", zones["AUDIT"] / "audit_interpretation_status.json"),
                           ("compliance.json", zones["AUDIT"] / "compliance.json"),
                           ("remediation.json", zones["AUDIT"] / "remediation.json")):
            shutil.copyfile(path, delivery / name)
        if interpretation_result is not None:
            shutil.copyfile(zones["AUDIT"] / "AUDIT_CONSOLIDATED.json", delivery / "AUDIT_CONSOLIDATED.json")
            shutil.copyfile(zones["AUDIT"] / "AUDIT_CONSOLIDATED.md", delivery / "AUDIT_CONSOLIDATED.md")
        if comparison is not None:
            shutil.copyfile(zones["AUDIT"] / "reaudit_comparison.json", delivery / "reaudit_comparison.json")
        streamed_json = _sanitize_delivery(delivery)
        unredacted_path_found = False
        for path in delivery.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".csv"}:
                continue
            if path.resolve() in streamed_json:
                # Every JSON string in this file was checked and redacted in the streaming pass.
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if _redact_path_text(text) != text:
                unredacted_path_found = True
                break
        if unredacted_path_found:
            raise RuntimeError("BLOCKED_TECHNICAL: ruta local detectada en DELIVERY")
        # Hash every client artifact; the manifest is sealed separately to avoid self-reference.
        for path in sorted(p for p in delivery.rglob("*") if p.is_file()):
            rel = path.relative_to(delivery).as_posix()
            manifest["delivery_artifacts"][rel] = {"sha256": _sha256(path), "size_bytes": path.stat().st_size}
        manifest["artifacts_sha256_verified"] = all(_sha256(delivery / name) == row["sha256"] for name, row in manifest["delivery_artifacts"].items())
        _write_json(delivery / "audit_manifest.json", manifest)
        # Include the root manifest's digest in an adjacent seal, since a file cannot hash itself.
        manifest_sha = _sha256(delivery / "audit_manifest.json")
        _write_json(delivery / "delivery_seal.json", {"audit_manifest_sha256": manifest_sha,
                    "artifacts_verified": manifest["artifacts_sha256_verified"], "sealed_at_utc": _utc_now()})
        if _sha256(frozen_source) != source_sha:
            raise RuntimeError("BLOCKED_TECHNICAL: SOURCE cambió durante la ejecución")
        return {"status": final_status, "audit_id": audit_id, "source_sha256": source_sha,
                "delivery_directory": str(delivery), "audit_manifest_sha256": manifest_sha,
                "artifact_count": len(manifest["delivery_artifacts"]), "findings_count": len(findings),
                "source_immutable": True, "artifacts_sha256_verified": manifest["artifacts_sha256_verified"]}
    except (IngestionError, zipfile.BadZipFile) as exc:
        blocked = {"status": "BLOCKED_INPUT_INVALID", "audit_id": audit_id, "source_sha256": source_sha,
                   "error_type": type(exc).__name__, "message": str(exc), "source_immutable": _sha256(frozen_source) == source_sha}
        _write_json(zones["AUDIT"] / "workflow_result.json", blocked)
        return blocked
    except ComparisonError as exc:
        blocked = {"status": "BLOCKED_TECHNICAL", "audit_id": audit_id, "source_sha256": source_sha,
                   "error_type": exc.code, "message": str(exc), "source_immutable": _sha256(frozen_source) == source_sha}
        _write_json(zones["AUDIT"] / "workflow_result.json", blocked)
        return blocked
    except Exception as exc:
        blocked = {"status": "BLOCKED_TECHNICAL", "audit_id": audit_id, "source_sha256": source_sha,
                   "error_type": type(exc).__name__, "message": str(exc), "source_immutable": _sha256(frozen_source) == source_sha}
        _write_json(zones["AUDIT"] / "workflow_result.json", blocked)
        return blocked


def main() -> int:
    parser = argparse.ArgumentParser(description="Local GTFS client audit workflow V1")
    parser.add_argument("zip", type=Path, help="GTFS ZIP input")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--client-project-id", required=True)
    parser.add_argument("--audit-id", required=True)
    parser.add_argument("--source-provenance", default="CLIENT_PROVIDED")
    parser.add_argument("--audit-mode", choices=("INITIAL", "MAINTENANCE", "RECURRING"), default="INITIAL")
    parser.add_argument("--baseline-run", type=Path)
    args = parser.parse_args()
    try:
        result = run_client_audit(args.zip, args.workspace, client_project_id=args.client_project_id,
                                  audit_id=args.audit_id, source_provenance=args.source_provenance,
                                  audit_mode=args.audit_mode, baseline_run=args.baseline_run)
    except (ValueError, OSError) as exc:
        result = {"status": "BLOCKED_INPUT_INVALID", "error": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status", "").startswith("COMPLETED") or result.get("status") == "HUMAN_REVIEW_REQUIRED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
