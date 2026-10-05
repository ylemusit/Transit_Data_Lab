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


LAB_ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Transit Data Lab — Auditor GTFS"
ERROR_ALREADY_EXISTS = 183


def classify_worker_exit(cancel_requested: bool, return_code: int) -> str:
    """Classify completion by recorded user intent before the worker exit code."""
    if cancel_requested:
        return "CANCELLED"
    return "SUCCEEDED" if return_code == 0 else "FAILED"


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
        self._cancel_requested = False
        self._cancel_requested_at: str | None = None
        self._termination_thread: threading.Thread | None = None
        self._termination_result: dict[str, object] | None = None
        self._state = "IDLE"

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Auditor GTFS", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="Analiza un archivo GTFS Schedule y guarda una entrega verificable en tu equipo.",
            wraplength=660,
        ).pack(anchor="w", pady=(4, 20))

        self._path_row(frame, "Archivo GTFS ZIP", self.source, self._choose_source, "Examinar…")
        self._path_row(frame, "Guardar en", self.destination, self._choose_destination, "Elegir carpeta…")

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(18, 8))
        self.run_button = ttk.Button(controls, text="Iniciar auditoría", command=self._start)
        self.run_button.pack(side="left")
        self.cancel_button = ttk.Button(controls, text="Cancelar", command=self._cancel, state="disabled")
        self.cancel_button.pack(side="left", padx=(8, 0))
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
            self.source.set(selected)
            self._refresh_ready_state()
            self.status.set("Archivo seleccionado. Elige dónde guardar la entrega.")

    def _choose_destination(self) -> None:
        selected = filedialog.askdirectory(title="Elige la carpeta donde guardar la entrega")
        if selected:
            self.destination.set(selected)
            self._refresh_ready_state()
            self.status.set("Listo para iniciar la auditoría.")

    def _refresh_ready_state(self) -> None:
        if self._state in {"IDLE", "READY"} and self.source.get() and self.destination.get():
            self._state = "READY"

    def _start(self) -> None:
        source = Path(self.source.get())
        parent = Path(self.destination.get())
        if not source.is_file() or source.suffix.lower() != ".zip":
            messagebox.showerror("Archivo no válido", "Selecciona un archivo ZIP existente.", parent=self.root)
            return
        if not parent.is_dir():
            messagebox.showerror("Carpeta no válida", "Selecciona una carpeta de destino existente.", parent=self.root)
            return
        self._state = "READY"

        audit_id = "audit-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
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
        try:
            command = worker_command(source, workspace, audit_id)
            with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
                self._process = subprocess.Popen(
                    command, cwd=worker_cwd(), stdin=subprocess.DEVNULL,
                    stdout=stdout, stderr=stderr,
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
                        worker_command=safe_command)
        self.open_button.configure(state="disabled")
        self.run_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.status.set("Auditoría en curso. Puedes seguir usando esta ventana.")
        self.progress.start(12)
        self.root.after(250, self._poll)

    def _poll(self) -> None:
        if self._process is None:
            return
        return_code = self._process.poll()
        if return_code is None:
            self.root.after(250, self._poll)
            return

        self.progress.stop()
        self.run_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self._process = None
        result = self._read_result()
        classification = classify_worker_exit(self._cancel_requested, return_code)
        if classification == "CANCELLED":
            self._state = "CANCELLED"
            self.open_button.configure(state="disabled")
            self.status.set("Auditoría cancelada por el usuario.")
        elif return_code == 0 and result and str(result.get("status", "")).startswith("COMPLETED"):
            self._state = "SUCCEEDED"
            self.status.set(
                f"Auditoría completada. Hallazgos: {result.get('findings_count', '—')}. "
                f"Archivos de entrega: {result.get('artifact_count', '—')}."
            )
            self.open_button.configure(state="normal")
        elif return_code == 0 and result and result.get("status") == "HUMAN_REVIEW_REQUIRED":
            self._state = "SUCCEEDED"
            self.status.set("Ejecución completada; el resultado requiere revisión humana antes de su uso.")
            self.open_button.configure(state="normal")
        else:
            self._state = "FAILED"
            detail = result.get("status", "") if result else ""
            self.status.set(f"La auditoría no se completó ({detail or 'error técnico'}). No se han borrado sus archivos.")
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
