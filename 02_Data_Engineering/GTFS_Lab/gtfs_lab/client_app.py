"""Minimal Windows application shell for the local GTFS client workflow."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tkinter as tk
import uuid
import ctypes
import threading
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Callable
from .client_intake import InputValidationError, IntakeSummary, validate_gtfs_zip
from .client_version import CLIENT_VERSION


LAB_ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Transit Data Lab — Auditor GTFS V1"
ERROR_ALREADY_EXISTS = 183


def classify_worker_exit(cancel_requested: bool, return_code: int) -> str:
    """Classify completion by recorded user intent before the worker exit code."""
    if cancel_requested:
        return "CANCELLED"
    return "SUCCEEDED" if return_code == 0 else "FAILED"


def classify_execution_result(cancel_requested: bool, return_code: int,
                              result: dict[str, object] | None) -> str:
    """Keep user cancellation and workflow outcomes distinct from app failures."""
    if cancel_requested:
        return "CANCELLED"
    status = result.get("status") if result else None
    if status == "BLOCKED_INPUT_INVALID":
        return "BLOCKED_INPUT_INVALID"
    if status == "BLOCKED_TECHNICAL":
        return "AUDIT_FAILED"
    if return_code == 0 and isinstance(status, str) and status.startswith("COMPLETED"):
        return "SUCCEEDED"
    if return_code == 0 and status == "HUMAN_REVIEW_REQUIRED":
        return "HUMAN_REVIEW_REQUIRED"
    return "APPLICATION_FAILED"


def result_summary_text(manifest: dict[str, object], interpretation: dict[str, object]) -> str:
    """Build a user-readable summary from the authoritative delivery artifacts."""
    coverage = interpretation.get("coverage", {})
    if not isinstance(coverage, dict):
        coverage = {}
    identity = manifest.get("dataset_identity", {})
    if not isinstance(identity, dict):
        identity = {}
    return (
        f"Dataset: {identity.get('dataset_id', '—')} · Archivo: {identity.get('source_filename', '—')}\n"
        f"SHA-256: {identity.get('source_sha256', '—')}\n"
        f"Versión cliente: {manifest.get('engine_versions', {}).get('client_application', '—')} · "
        f"Estado: {manifest.get('status', '—')} · Interpretación: {interpretation.get('interpretation_status', '—')}\n"
        f"Hallazgos brutos: {coverage.get('raw_finding_count', '—')} · Consolidados: {coverage.get('consolidated_occurrence_count', '—')} · "
        f"Sin clasificar: {coverage.get('unclassified_occurrence_count', '—')} · Brecha contable: {coverage.get('accounting_gap', '—')}\n"
        "Los hallazgos son evidencia técnica; no constituyen por sí solos una conclusión de incumplimiento legal."
    )


def family_row_values(family: dict[str, object]) -> tuple[object, ...]:
    entities = family.get("affected_entities", [])
    entity_count = (len(entities) if isinstance(entities, list) else family.get("affected_entity_count", "—"))
    if not entities:
        entity_count = family.get("affected_entity_count", entity_count)
    impact = family.get("operational_impact", "—")
    if isinstance(impact, dict):
        direct = impact.get("direct_affected", {})
        impact = f"{direct.get('entity_type', '—')}: {direct.get('entity_count', '—')} directas"
    patterns = family.get("patterns", [])
    pattern = patterns[0].get("classification", "—") if isinstance(patterns, list) and patterns and isinstance(patterns[0], dict) else "—"
    return (family.get("rule_id", family.get("family_id", "—")),
            family.get("occurrence_count", family.get("raw_occurrence_count", "—")), entity_count,
            pattern, impact)


def family_detail_payload(family: dict[str, object], source_findings: object) -> dict[str, object]:
    """Join read-only source finding detail to its consolidated family view."""
    if not isinstance(source_findings, list):
        source_findings = []
    related = [
        finding for finding in source_findings
        if isinstance(finding, dict)
        and finding.get("rule_id") == family.get("rule_id")
        and finding.get("stage") == family.get("stage")
        and finding.get("source_file") == family.get("source_file")
    ]
    return {"family": family, "source_findings": related}


class WindowsInstanceLock:
    """Keep one client process active per Windows user session."""

    def __init__(self) -> None:
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._kernel32.CreateMutexW.restype = ctypes.c_void_p
        self._kernel32.CreateMutexW.argtypes = (ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p)
        self._kernel32.ReleaseMutex.argtypes = (ctypes.c_void_p,)
        self._kernel32.CloseHandle.argtypes = (ctypes.c_void_p,)
        self._handle = self._kernel32.CreateMutexW(None, True, "Local\\TransitDataLab.WindowsClientV1")
        if not self._handle:
            raise ctypes.WinError(ctypes.get_last_error())
        self.acquired = ctypes.get_last_error() != ERROR_ALREADY_EXISTS
        if not self.acquired:
            self._kernel32.CloseHandle(self._handle)
            self._handle = None

    def release(self) -> None:
        if self._handle:
            self._kernel32.ReleaseMutex(self._handle)
            self._kernel32.CloseHandle(self._handle)
            self._handle = None


def worker_cwd() -> Path:
    """Use a stable directory available in both source and onedir layouts."""
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else LAB_ROOT


def worker_command(source: Path, workspace: Path, audit_id: str) -> list[str]:
    """Build a fixed-argument worker command for source or future onedir mode."""
    if getattr(sys, "frozen", False):
        worker = Path(sys.executable).with_name("tdl-worker.exe")
        if not worker.is_file():
            raise FileNotFoundError("No se encuentra el componente de auditoría de esta instalación.")
        command = [str(worker)]
    else:
        command = [sys.executable, "-m", "gtfs_lab.client_workflow"]

    return command + [
        str(source),
        "--workspace", str(workspace),
        "--client-project-id", "tdl-local",
        "--audit-id", audit_id,
        "--source-provenance", "CLIENT_PROVIDED",
        "--audit-mode", "INITIAL",
    ]


class ClientApp:
    def __init__(self, root: tk.Tk, on_exit: Callable[[], None] | None = None) -> None:
        self.root = root
        self._on_exit = on_exit
        self.root.title(APP_NAME)
        self.root.minsize(620, 390)
        self.root.geometry("720x440")

        self.source = tk.StringVar()
        self.destination = tk.StringVar()
        self.status = tk.StringVar(value="Selecciona un archivo GTFS ZIP para empezar.")
        self._process: subprocess.Popen[bytes] | None = None
        self._workspace: Path | None = None
        self._audit_id: str | None = None
        self._stdout_path: Path | None = None
        self._stderr_path: Path | None = None
        self._technical_log_path: Path | None = None
        self._stage_path: Path | None = None
        self._stage_offset = 0
        self._active_stage: str | None = None
        self._cancel_requested = False
        self._cancel_requested_at: str | None = None
        self._termination_thread: threading.Thread | None = None
        self._termination_result: dict[str, object] | None = None
        self._state = "IDLE"
        self._intake: IntakeSummary | None = None

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Auditor GTFS", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text=f"Versión {CLIENT_VERSION}. Analiza un archivo GTFS Schedule y guarda una entrega verificable en tu equipo.",
            wraplength=660,
        ).pack(anchor="w", pady=(4, 20))

        self._path_row(frame, "Archivo GTFS ZIP", self.source, self._choose_source, "Examinar…")
        self.intake_summary = tk.StringVar(value="Selecciona un GTFS ZIP para validar tablas e identidad antes de auditar.")
        ttk.Label(frame, textvariable=self.intake_summary, wraplength=660, justify="left").pack(anchor="w", pady=(4, 6))
        self._path_row(frame, "Guardar en", self.destination, self._choose_destination, "Elegir carpeta…")

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(18, 8))
        self.run_button = ttk.Button(controls, text="Iniciar auditoría", command=self._start)
        self.run_button.pack(side="left")
        self.run_button.configure(state="disabled")
        self.cancel_button = ttk.Button(controls, text="Cancelar", command=self._cancel, state="disabled")
        self.cancel_button.pack(side="left", padx=(8, 0))
        self.results_button = ttk.Button(controls, text="Ver resultados", command=self._show_results, state="disabled")
        self.results_button.pack(side="left", padx=(8, 0))
        self.gis_button = ttk.Button(controls, text="Abrir GIS", command=self._open_gis, state="disabled")
        self.gis_button.pack(side="right", padx=(8, 0))
        self.open_button = ttk.Button(controls, text="Abrir entrega", command=self._open_delivery, state="disabled")
        self.open_button.pack(side="right")

        ttk.Separator(frame).pack(fill="x", pady=12)
        ttk.Label(frame, textvariable=self.status, wraplength=660).pack(anchor="w")
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=(12, 0))
        ttk.Label(
            frame,
            text="La ejecución es local y serial. El archivo de origen se conserva sin modificar.",
            foreground="#555555",
        ).pack(anchor="w", pady=(18, 0))

    @staticmethod
    def _path_row(parent: ttk.Frame, label: str, variable: tk.StringVar,
                  command: object, button_label: str) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=6)
        ttk.Label(row, text=label, width=16).pack(side="left", anchor="w")
        ttk.Entry(row, textvariable=variable, state="readonly").pack(side="left", fill="x", expand=True)
        ttk.Button(row, text=button_label, command=command).pack(side="left", padx=(8, 0))

    def _choose_source(self) -> None:
        selected = filedialog.askopenfilename(
            title="Selecciona el archivo GTFS ZIP",
            filetypes=(("Archivo ZIP", "*.zip"), ("Todos los archivos", "*.*")),
        )
        if selected:
            self._prepare_new_run()
            self.source.set(selected)
            self._intake = None
            try:
                self._intake = validate_gtfs_zip(Path(selected))
            except InputValidationError as exc:
                self.intake_summary.set(str(exc))
                self.status.set("La entrada no supera la validación; no se ha iniciado la auditoría.")
                self._state = "IDLE"
                self.run_button.configure(state="disabled")
                return
            self._show_intake(self._intake)
            self._refresh_ready_state()
            self.status.set("Entrada validada. Elige dónde guardar la entrega.")

    def _show_intake(self, intake: IntakeSummary, audit_id: str | None = None) -> None:
        tables = ", ".join(f"{table}.txt" for table in intake.tables)
        self.intake_summary.set(
            f"Validación GTFS: correcta · Archivo: {intake.filename} · "
            f"Identidad: {intake.dataset_id} · SHA-256: {intake.source_sha256} · "
            f"Tamaño: {intake.size_bytes:,} bytes · Tablas: {tables} · "
            f"Recepción UTC: {intake.intake_timestamp_utc}"
            + (f" · Auditoría: {audit_id}" if audit_id else "")
        )

    def _choose_destination(self) -> None:
        selected = filedialog.askdirectory(title="Elige la carpeta donde guardar la entrega")
        if selected:
            self._prepare_new_run()
            self.destination.set(selected)
            self._refresh_ready_state()
            self.status.set("Listo para iniciar la auditoría." if self._intake else "Valida primero un archivo GTFS ZIP.")

    def _prepare_new_run(self) -> None:
        """Detach the GUI from the previous run before accepting new inputs."""
        if self._state in {"RUNNING", "CANCELLING"}:
            return

        self._state = "IDLE"
        self._workspace = None
        self._audit_id = None
        self._stdout_path = None
        self._stderr_path = None
        self._technical_log_path = None
        self._stage_path = None
        self._stage_offset = 0
        self._active_stage = None
        if self._intake is not None:
            self._show_intake(self._intake)
        self.open_button.configure(state="disabled")
        self.results_button.configure(state="disabled")
        self.gis_button.configure(state="disabled")
        self.run_button.configure(state="disabled")

    def _refresh_ready_state(self) -> None:
        if self._state in {
            "SUCCEEDED", "CANCELLED", "BLOCKED_INPUT_INVALID", "AUDIT_FAILED",
            "APPLICATION_FAILED", "HUMAN_REVIEW_REQUIRED",
        }:
            self._prepare_new_run()
        ready = self._state in {"IDLE", "READY"} and self._intake is not None and Path(self.destination.get()).is_dir()
        self.run_button.configure(state="normal" if ready else "disabled")
        if ready:
            self._state = "READY"

    def _start(self) -> None:
        source = Path(self.source.get())
        parent = Path(self.destination.get())
        try:
            current_intake = validate_gtfs_zip(source)
        except InputValidationError as exc:
            self._prepare_new_run()
            self._intake = None
            self.intake_summary.set(str(exc))
            self._state = "IDLE"
            messagebox.showerror("Entrada GTFS no válida", str(exc), parent=self.root)
            return
        self._intake = current_intake
        if not parent.is_dir():
            messagebox.showerror("Carpeta no válida", "Selecciona una carpeta de destino existente.", parent=self.root)
            return
        self._state = "READY"

        audit_id = "audit-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
        self._show_intake(current_intake, audit_id)
        workspace = parent / f"TDL-Auditoria-{audit_id.removeprefix('audit-')}"
        if workspace.exists():
            messagebox.showerror("Destino ocupado", "La carpeta de esta ejecución ya existe. Vuelve a intentarlo.", parent=self.root)
            return
        stdout_path = parent / f".{workspace.name}.stdout.log"
        stderr_path = parent / f".{workspace.name}.stderr.log"
        self._technical_log_path = parent / f".{workspace.name}.technical.jsonl"
        self._cancel_requested = False
        self._cancel_requested_at = None
        self._termination_thread = None
        self._termination_result = None
        self._stage_path = parent / f".{workspace.name}.stages.jsonl"
        self._stage_offset = 0
        self._active_stage = None
        try:
            command = worker_command(source, workspace, audit_id)
            worker_env = os.environ.copy()
            worker_env["TDL_RESOURCE_STAGE_FILE"] = str(self._stage_path)
            with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
                self._process = subprocess.Popen(
                    command, cwd=worker_cwd(), stdin=subprocess.DEVNULL,
                    stdout=stdout, stderr=stderr,
                    env=worker_env,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
        except (OSError, ValueError) as exc:
            self._process = None
            messagebox.showerror("No se pudo iniciar", str(exc), parent=self.root)
            return

        self._workspace = workspace
        self._audit_id = audit_id
        self._stdout_path = stdout_path
        self._stderr_path = stderr_path
        self._state = "RUNNING"
        safe_command = [
            "tdl-worker.exe" if getattr(sys, "frozen", False) else f"{Path(sys.executable).name} -m gtfs_lab.client_workflow",
            "<selected_gtfs_zip>", "--workspace", "<run_workspace>",
            "--client-project-id", "tdl-local", "--audit-id", audit_id,
            "--source-provenance", "CLIENT_PROVIDED", "--audit-mode", "INITIAL",
        ]
        self._log_event("worker_started", pid=self._process.pid, audit_id=audit_id,
                        worker_command=safe_command, intake={
                            "filename": current_intake.filename,
                            "source_sha256": current_intake.source_sha256,
                            "dataset_id": current_intake.dataset_id,
                            "size_bytes": current_intake.size_bytes,
                            "intake_timestamp_utc": current_intake.intake_timestamp_utc,
                            "tables": list(current_intake.tables),
                        })
        self.open_button.configure(state="disabled")
        self.run_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.status.set("Auditoría en curso. Puedes seguir usando esta ventana.")
        self.progress.start(12)
        self.root.after(250, self._poll)

    def _poll(self) -> None:
        if self._process is None:
            return
        self._refresh_execution_stage()
        return_code = self._process.poll()
        if return_code is None:
            self.root.after(250, self._poll)
            return

        self.progress.stop()
        self.run_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self._process = None
        result = self._read_result()
        classification = classify_execution_result(self._cancel_requested, return_code, result)
        if classification == "CANCELLED":
            self._state = "CANCELLED"
            self.open_button.configure(state="disabled")
            self.status.set("Auditoría cancelada por el usuario.")
        elif classification == "SUCCEEDED":
            self._state = "SUCCEEDED"
            self.status.set(
                f"Auditoría completada. Hallazgos: {result.get('findings_count', '—')}. "
                f"Archivos de entrega: {result.get('artifact_count', '—')}."
            )
            self.open_button.configure(state="normal")
            self.results_button.configure(state="normal")
            self._refresh_gis_button()
        elif classification == "HUMAN_REVIEW_REQUIRED":
            self._state = "HUMAN_REVIEW_REQUIRED"
            self.status.set("Ejecución completada; el resultado requiere revisión humana antes de su uso.")
            self.open_button.configure(state="normal")
            self.results_button.configure(state="normal")
            self._refresh_gis_button()
        elif classification == "BLOCKED_INPUT_INVALID":
            self._state = "BLOCKED_INPUT_INVALID"
            self.status.set("Entrada inválida. Revisa el archivo GTFS seleccionado; no hay una entrega completa.")
        elif classification == "AUDIT_FAILED":
            self._state = "AUDIT_FAILED"
            self.status.set("La auditoría encontró un fallo técnico. Los archivos parciales se conservan para revisión.")
        else:
            self._state = "APPLICATION_FAILED"
            detail = result.get("status", "") if result else ""
            self.status.set(f"La aplicación no pudo completar la ejecución ({detail or 'fallo técnico de aplicación'}). No se han borrado sus archivos.")
            messagebox.showwarning(
                "Auditoría no completada",
                "Se conservaron los archivos creados para facilitar la revisión. "
                f"Registro técnico: {self._stderr_path}",
                parent=self.root,
            )
        self._log_event(
            "worker_finished",
            worker_return_code=return_code,
            gui_classification=self._state,
            result_status=result.get("status") if result else None,
            termination=self._termination_result,
            important_stderr=self._stderr_excerpt(),
        )

    def _show_results(self) -> None:
        """Present a read-only view of the sealed workflow artifacts."""
        if self._workspace is None or self._audit_id is None:
            return
        delivery = self._workspace / "tdl-local" / self._audit_id / "delivery"
        try:
            manifest = json.loads((delivery / "audit_manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Resultados no disponibles", f"No se pudo leer el manifest de entrega: {exc}", parent=self.root)
            return
        try:
            interpretation = json.loads((delivery / "AUDIT_CONSOLIDATED.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            audit_interpretation = manifest.get("audit_interpretation", {})
            status = audit_interpretation.get("status", "NOT_EVALUABLE") if isinstance(audit_interpretation, dict) else "NOT_EVALUABLE"
            interpretation = {"interpretation_status": status, "finding_families": [], "source_findings": [], "coverage": {}}
        try:
            pdf_status = json.loads((delivery / "report" / "pdf_generation_status.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pdf_status = {"status": "NOT_EVALUABLE"}
        window = tk.Toplevel(self.root)
        window.title("Resultados de auditoría GTFS")
        window.geometry("860x600")
        window.transient(self.root)
        body = ttk.Frame(window, padding=16)
        body.pack(fill="both", expand=True)
        summary = result_summary_text(manifest, interpretation) + f"\nInforme PDF: {pdf_status.get('status', 'NOT_EVALUABLE')}"
        ttk.Label(body, text=summary, wraplength=820, justify="left").pack(fill="x", pady=(0, 12))
        columns = ("rule", "occurrences", "entities", "pattern", "impact")
        tree = ttk.Treeview(body, columns=columns, show="headings", height=12)
        for col, label, width in zip(columns, ("Regla", "Ocurrencias", "Entidades", "Patrón", "Impacto directo"), (130, 90, 90, 230, 250)):
            tree.heading(col, text=label)
            tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True)
        details = tk.Text(body, height=8, wrap="word", state="disabled")
        details.pack(fill="x", pady=(10, 0))
        families = interpretation.get("finding_families", [])
        for index, family in enumerate(families):
            tree.insert("", "end", iid=str(index), values=family_row_values(family))
        def show_family(_event: object = None) -> None:
            selected = tree.selection()
            if not selected:
                return
            family = families[int(selected[0])]
            content = json.dumps(
                family_detail_payload(family, interpretation.get("source_findings")),
                ensure_ascii=False, indent=2,
            )
            details.configure(state="normal")
            details.delete("1.0", "end")
            details.insert("1.0", content)
            details.configure(state="disabled")
        tree.bind("<<TreeviewSelect>>", show_family)
        actions = ttk.Frame(body)
        actions.pack(fill="x", pady=(8, 0))
        pdf_button = ttk.Button(actions, text="Abrir informe PDF", command=self._open_pdf,
                                state="normal" if pdf_status.get("status") == "GENERATED" else "disabled")
        pdf_button.pack(side="left")
        ttk.Button(actions, text="Abrir entrega completa", command=self._open_delivery).pack(side="right")

    def _refresh_execution_stage(self) -> None:
        """Read worker stage markers without inventing percentage completion."""
        if self._stage_path is None:
            return
        labels = {
            "INTAKE": "Validación y preparación de entrada",
            "AUDIT": "Auditoría GTFS",
            "INTERPRETATION": "Interpretación y consolidación",
            "REPLAY": "Comprobación de reproducibilidad",
            "REPORT_GENERATION": "Preparación de informes y entrega",
            "ZIP_EXTRACTION": "Lectura del archivo ZIP",
            "INGESTION": "Lectura de tablas GTFS",
        }
        try:
            with self._stage_path.open("r", encoding="utf-8") as stream:
                stream.seek(self._stage_offset)
                lines = stream.readlines()
                self._stage_offset = stream.tell()
        except (FileNotFoundError, OSError):
            return
        for line in lines:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            stage = str(event.get("stage", ""))
            state = event.get("state")
            if state == "START":
                self._active_stage = stage
            elif state == "END" and self._active_stage == stage:
                self._active_stage = None
        if self._active_stage:
            self.status.set(f"Etapa en curso: {labels.get(self._active_stage, self._active_stage)}. Puedes cancelar la auditoría.")

    def _log_event(self, event: str, **details: object) -> None:
        if self._technical_log_path is None:
            return
        record = {"timestamp": datetime.now().astimezone().isoformat(), "event": event, **details}
        try:
            with self._technical_log_path.open("a", encoding="utf-8", newline="\n") as log:
                log.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            # Diagnostic logging must not break the GUI lifecycle.
            pass

    def _stderr_excerpt(self) -> str:
        """Retain only the final diagnostic bytes in the private technical log."""
        if self._stderr_path is None:
            return ""
        try:
            with self._stderr_path.open("rb") as stream:
                stream.seek(max(0, self._stderr_path.stat().st_size - 4096))
                return stream.read().decode("utf-8", errors="replace")[-2000:]
        except OSError:
            return "[stderr unavailable]"
    def _read_result(self) -> dict[str, object] | None:
        if self._stdout_path is None:
            return None
        try:
            value = json.loads(self._stdout_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _cancel(self) -> None:
        process = self._process
        if process is None or self._state != "RUNNING":
            return
        if not messagebox.askyesno(
            "Cancelar auditoría", "¿Quieres detener la auditoría? Los archivos ya creados se conservarán.", parent=self.root
        ):
            return
        # Recheck after the modal dialog: the worker may have exited while it was open.
        if process.poll() is not None:
            self.root.after(0, self._poll)
            return
        self._cancel_requested = True
        self._cancel_requested_at = datetime.now().astimezone().isoformat()
        self._state = "CANCELLING"
        self.cancel_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.status.set("Cancelación solicitada. Se está deteniendo la auditoría…")
        self._log_event("cancel_requested", cancel_requested_at=self._cancel_requested_at, worker_pid=process.pid)
        self._termination_thread = threading.Thread(
            target=self._terminate_process_tree, args=(process,), name="tdl-worker-terminator", daemon=True
        )
        self._termination_thread.start()

    def _terminate_process_tree(self, process: subprocess.Popen[bytes]) -> None:
        result: dict[str, object] = {"attempted": True, "worker_pid": process.pid}
        self._log_event("termination_attempt", worker_pid=process.pid)
        try:
            if os.name == "nt":
                completed = subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), timeout=15,
                )
                result["tree_termination_return_code"] = completed.returncode
                result["descendant_termination_attempted"] = True
            else:
                process.terminate()
                result["tree_termination_return_code"] = 0
                result["descendant_termination_attempted"] = False
        except (OSError, subprocess.TimeoutExpired) as exc:
            result["termination_error"] = type(exc).__name__
            try:
                process.terminate()
                result["fallback_terminate"] = "sent"
            except OSError as fallback_exc:
                # A process that exited during the race needs no further termination.
                result["fallback_terminate"] = type(fallback_exc).__name__
        finally:
            self._termination_result = result
            self._log_event("termination_attempt_finished", **result)

    def _open_delivery(self) -> None:
        if self._workspace is None:
            return
        if self._audit_id is None:
            return
        delivery = self._workspace / "tdl-local" / self._audit_id / "delivery"
        if not delivery.is_dir():
            messagebox.showinfo("Entrega no disponible", "No se ha encontrado una entrega completa.", parent=self.root)
            return
        try:
            os.startfile(str(delivery))
        except OSError as exc:
            messagebox.showerror("No se pudo abrir la carpeta", str(exc), parent=self.root)

    def _refresh_gis_button(self) -> None:
        if self._workspace is None or self._audit_id is None:
            return
        exports = self._workspace / "tdl-local" / self._audit_id / "delivery" / "engine_run" / "exports"
        has_layers = exports.is_dir() and any(exports.rglob("*.geojson")) or exports.is_dir() and any(exports.rglob("*.kml"))
        self.gis_button.configure(state="normal" if has_layers else "disabled")

    def _open_gis(self) -> None:
        if self._workspace is None or self._audit_id is None:
            return
        exports = self._workspace / "tdl-local" / self._audit_id / "delivery" / "engine_run" / "exports"
        if not exports.is_dir():
            messagebox.showinfo("GIS no disponible", "Esta auditoría no produjo una carpeta de exportación GIS.", parent=self.root)
            return
        try:
            os.startfile(str(exports))
        except OSError as exc:
            messagebox.showerror("No se pudo abrir la carpeta GIS", str(exc), parent=self.root)

    def _open_pdf(self) -> None:
        if self._workspace is None or self._audit_id is None:
            return
        pdf_path = self._workspace / "tdl-local" / self._audit_id / "delivery" / "report" / "client_report.pdf"
        if not pdf_path.is_file():
            messagebox.showinfo("Informe PDF no disponible", "El informe PDF no se generó; la auditoría y sus evidencias permanecen disponibles.", parent=self.root)
            return
        try:
            os.startfile(str(pdf_path))
        except OSError as exc:
            messagebox.showerror("No se pudo abrir el informe PDF", str(exc), parent=self.root)

    def _close(self) -> None:
        if self._process is not None:
            messagebox.showinfo("Auditoría en curso", "Cancela o espera a que termine la auditoría antes de cerrar.", parent=self.root)
            return
        self.root.destroy()
        if self._on_exit is not None:
            self._on_exit()


def main() -> None:
    root = tk.Tk()
    if os.name == "nt":
        try:
            instance_lock = WindowsInstanceLock()
        except OSError as exc:
            messagebox.showerror("No se pudo iniciar", f"No se pudo comprobar si ya hay otra instancia.\n{exc}", parent=root)
            root.destroy()
            return
        if not instance_lock.acquired:
            messagebox.showinfo("Auditor GTFS abierto", "Ya hay otra ventana del auditor en ejecución.", parent=root)
            root.destroy()
            return
        on_exit = instance_lock.release
    else:
        on_exit = None
    ClientApp(root, on_exit=on_exit)
    root.mainloop()


if __name__ == "__main__":
    main()
