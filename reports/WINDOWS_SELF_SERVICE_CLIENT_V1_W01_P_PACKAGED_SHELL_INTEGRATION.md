# Windows Self-Service Client V1 — W01-P Packaged Shell Integration

**Resultado técnico:** `W01P_PASS_WITH_NONBLOCKING_LIMITATIONS`. La aceptación humana posterior de W01-F, del 2026-10-05, cerró las comprobaciones de GUI compilada que estaban pendientes en esta matriz. El cierre global y la decisión se documentan al final de este informe y en el registro [W01-F](WINDOWS_SELF_SERVICE_CLIENT_V1_W01_F_FINAL_PACKAGED_GUI_ACCEPTANCE.md).

## Alcance y resultado

Se creó una build reproducible PyInstaller onedir con `tdl-client.exe` y `tdl-worker.exe` separados. La GUI continúa lanzando el workflow como subproceso. El runtime incluye Python 3.12.10, Tk/Tcl, los módulos `gtfs_lab`, las siete especificaciones GTFS, lxml 6.1.3 con sus DLL, DuckDB CLI 1.5.5 y los recursos con hash fijado de Compliance V1. Los binarios de `dist-w01p/` y `build-w01p/` son locales e ignorados por Git.

El worker empaquetado completó auditorías en `cwd` ajeno al repositorio, con `PATH` limitado a `System32` y sin `PYTHONPATH`/`PYTHONHOME`. Una entrada y una carpeta con espacios y tildes llegaron al worker; la SOURCE conservó su SHA-256 y la entrega produjo 30 artefactos, manifest y seal verificados. Esta prueba encontró y corrigió la codificación del JSON de salida: el worker empaquetado fuerza UTF-8, que es lo que consume la GUI.

La GUI compilada se inició con PATH limitado; el proceso mantuvo `Responding = true` y título `Transit Data Lab — Auditor GTFS`. Para la integración de flujo se ejecutó el `ClientApp` Tk actual en un harness que simula el estado congelado y lanza el `tdl-worker.exe` empaquetado. Resultado: éxito, fallo real de ZIP clasificado `FAILED`, cancelación `CANCELLING` → `CANCELLED`, worker terminado, sin aviso genérico, entrega deshabilitada, log técnico con comando seguro/cancelación/clasificación/`stderr`, apertura de la carpeta correcta y ejecución posterior exitosa. La ventana procesó 24–87 pulsos Tk durante los escenarios.

**Límite de evidencia:** el E2E ejercitó el shell Tk desde el harness Python, no manejó los botones de la GUI compilada. El ejecutable GUI se probó de inicio/respuesta por separado. Los diálogos nativos no se condujeron con este entorno; las selecciones del harness se simularon. La prueba de mutex cubrió el bloqueo de duplicados y la adquisición tras liberar, pero no la secuencia manual con dos ejecutables y su cuadro informativo. Por tanto, la interoperabilidad del paquete está demostrada, con esos dos pasos de interfaz pendientes de validación humana.

## Evidencia del runtime

- PyInstaller `6.22.3`; Python de build/runtime `3.12.10`; destino Windows 11 x64; salida onedir.
- DuckDB: `v1.5.5 (Variegata) d8cdaa33fd`, `_internal/duckdb.exe`, SHA-256 `fde737c7749075f6b54e14772a4e6b33a5fa0201075d03640aca358074ea4554`.
- Evaluador Compliance V1 incluido con SHA-256 fijado `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; referencia GTFS incluida con SHA-256 `1ff40b8001b180bd023dd6f1899907aecbcb4600c8dbcb6fc6c841a50839b147`; el cargador resuelve ambos desde `_MEIPASS/runtime_assets` cuando está congelado.
- `DEVELOPER_ABSOLUTE_PATH_DEPENDENCY = NO` para ejecución empaquetada: worker probado desde `%TEMP%`, PATH de sistema y sin Python/DuckDB del desarrollador. Las rutas de entrada/salida del usuario siguen siendo las que selecciona el usuario.
- Auditoría sintética: SHA-256 del ZIP antes/después `db0303034934ed94e558ea79de8670cd0066f99b11ecf284ad9cb849cb066aad`; 30/30 artefactos concordaron con el manifest y el seal validó el manifest.
- `ORPHAN_PROCESSES = 0` tras el E2E empaquetado: no quedaron procesos `tdl-worker.exe` ni `duckdb.exe` del paquete.
- `CLEAN_MACHINE_VALIDATION = PENDING`; el equipo de desarrollo no equivale a una máquina limpia.
- `ENGINE_SEMANTICS_CHANGED = NO`; el cambio en `compliance_adapter.py` solo resuelve recursos congelados. `HOLDOUT_ACCESSED = NO`.

## Matriz de ejecución

| Escenario | Resultado | Evidencia y límite |
|---|---|---|
| START | PASS | `tdl-client.exe` con PATH reducido; ventana identificada y respondiendo. |
| SECOND INSTANCE | FAIL / pendiente | Prueba del mutex y reinicio del lock PASS; falta ejecutar y verificar dos GUIs empaquetadas juntas. |
| SELECT ZIP | PASS (harness) | Callback con ZIP sintético; selección nativa simulada. |
| SELECT OUTPUT | PASS (harness) | Callback con destino Unicode; diálogo nativo simulado. |
| SUCCESSFUL AUDIT | PASS (integración) | GUI Tk del harness + worker empaquetado; salida y hashes verificados. |
| FAILED AUDIT | PASS (integración) | ZIP inválido terminó como `FAILED`, no `CANCELLED`. |
| CANCEL AUDIT | PASS (integración) | `CANCELLING` → `CANCELLED`; worker terminó; entrega deshabilitada y log registrado. |
| OPEN DELIVERY | PASS (integración) | Se abrió el directorio `delivery` esperado mediante el callback. |
| RE-RUN AFTER CANCEL | PASS (integración) | Auditoría posterior completada correctamente. |
| RE-RUN AFTER SUCCESS | PASS (integración) | Se completó más de una auditoría en la misma instancia del shell. |
| EXIT / RESTART | FAIL / pendiente | El lock se libera y readquiere en la prueba unitaria; no se condujo el cierre normal de la GUI compilada. |
| REAL DIALOG INTERACTION | NOT_YET_TESTED | Sin automatización de diálogos nativos disponible en esta sesión. |

La matriz recoge comprobaciones asistidas y sus límites; `SELECT ZIP`, `SELECT OUTPUT`, los casos funcionales y `OPEN DELIVERY` no son una sesión manual con diálogos nativos.

## Resumen W01-P

```ini
PYINSTALLER_ONEDIR_GUI = PASS
GUI_LAUNCH = PASS
WORKER_LAUNCH = PASS
DUCKDB_BUNDLED = YES
PACKAGED_GUI_E2E = PASS_WITH_HARNESS_LIMITATION
PACKAGED_CANCELLATION = PASS_WITH_HARNESS_LIMITATION
PACKAGED_FAILURE = PASS_WITH_HARNESS_LIMITATION
SINGLE_INSTANCE = FAIL (full executable double launch pending; mutex test PASS)
REAL_DIALOG_INTERACTION = NOT_YET_TESTED
OPEN_DELIVERY = PASS_WITH_HARNESS_LIMITATION
POST_CANCEL_RERUN = PASS_WITH_HARNESS_LIMITATION
ORPHAN_PROCESSES = 0
DEVELOPER_ABSOLUTE_PATH_DEPENDENCY = NO
CLEAN_MACHINE_VALIDATION = PENDING
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
TESTS = 7 PASS (5 client app, 2 packaged worker)
py_compile = PASS
git diff --check = PASS
git status = W01-C retained plus scoped W01-P changes; no binaries tracked
```

**Reproducción:** desde `02_Data_Engineering/GTFS_Lab`, instalar PyInstaller 6.x y lxml 6.1.x en el entorno de build, asegurarse de que DuckDB CLI 1.5.5 está disponible en PATH o indicar `TDL_DUCKDB_CLI`, y ejecutar:

```powershell
python -m PyInstaller --noconfirm --distpath dist-w01p --workpath build-w01p packaging\tdl_client_onedir.spec
python -m unittest discover -s tests -p test_client_app.py
python -m unittest discover -s tests -p test_client_packaging.py
```

Los datos de ejecución y la evidencia JSON del harness quedan en directorios temporales locales; no se versionan. Esta entrega no crea instalador, no se valida en máquina limpia, no se fusiona y no inicia W02.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Resultado de aceptación humana final — 2026-10-05

Las comprobaciones manuales posteriores confirmaron inicio, interacción con diálogos reales, E2E de éxito y cancelación desde el EXE, apertura de entrega, cancelación antes de éxito normal, parada de ficheros, repetición posterior, rechazo de una segunda instancia manteniendo usable la primera, salida y reinicio. `ORPHAN_PROCESSES_FINAL = 0`. Por tanto, los pendientes de interacción GUI consignados en la matriz anterior quedan resueltos por esta evidencia humana; se conservan allí como histórico de la ejecución W01-P.

`CLEAN_MACHINE_VALIDATION = PENDING` sigue siendo una validación posterior de packaging/release. No implica fallo de la aceptación actual en la máquina de desarrollo.

```ini
W01P_CLASSIFICATION = CLOSED_WITH_NONBLOCKING_LIMITATIONS
W01_ACCEPTANCE = PASS
AUTOMATED_TESTS = 7/7 PASS
PY_COMPILE = PASS
GIT_DIFF_CHECK = PASS
PACKAGED_ONEDIR = PASS
DUCKDB_BUNDLED = YES
CLEAN_MACHINE_VALIDATION = PENDING
W02 = NEXT / NOT_STARTED
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
