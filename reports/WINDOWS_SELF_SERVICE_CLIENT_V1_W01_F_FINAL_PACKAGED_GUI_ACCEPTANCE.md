# W01-F — Aceptación final de GUI empaquetada

**Fecha:** 2026-10-05
**Clasificación final:** `W01F_PASS_READY_FOR_W01_CLOSURE`
**Resultado de fase:** aceptación humana PASS; `W01_APPLICATION_SHELL = CLOSED_WITH_NONBLOCKING_LIMITATIONS`.

El registro inicial de esta aceptación y su continuación automatizada se conservan debajo como historial. La decisión manual final posterior, declarada por Yeison, es la autoridad vigente y actualiza los pasos inicialmente no ejecutados.

## Alcance y limitación de ejecución

Se lanzó `tdl-client.exe` del paquete onedir existente desde un directorio temporal local, con ese directorio como `WorkingDirectory`, fuera del repositorio. La ventana real apareció con título `Transit Data Lab — Auditor GTFS`; el proceso respondió durante la comprobación. Se generó una entrada GTFS sintética local para la aceptación (SHA-256 `F93ACEAC984D6BD7248884608C4193E8C64D1C0870856C2EDFA8CCE0D92F94AE`).

El conector de escritorio disponible en esta sesión solo expone control de navegador y no ofrece APIs para inspeccionar, capturar o manejar ventanas nativas. Por ello no se pulsaron botones ni se condujeron los diálogos Windows. No se atribuye aceptación GUI a los E2E previos basados en harness.

La ventana compilada se dejó abierta para que Yeison pueda continuar la aceptación manual. El único proceso `tdl-client` visible al cierre del registro es esa instancia intencionadamente abierta; no se inició worker durante esta aceptación. Esto no es un resultado de limpieza tras salida normal.

## Matriz observada

| Comprobación | Resultado en GUI compilada | Nota |
|---|---|---|
| Inicio GUI compilada | PASS | Ventana visible/responding; binario onedir `dist-w01p`.
| Diálogo real ZIP (cancelar y volver a seleccionar) | NO EJECUTADO | Requiere control de ventana nativa.
| Diálogo real de carpeta (cancelar y volver a seleccionar) | NO EJECUTADO | Requiere control de ventana nativa.
| E2E éxito compilado | NO EJECUTADO | No se seleccionó origen ni destino mediante GUI.
| Cancelación E2E compilada | NO EJECUTADO | No se inició auditoría desde la GUI.
| Fallo E2E compilado | NO EJECUTADO | No se introdujo caso inválido desde la GUI.
| Abrir entrega con botón real | NO EJECUTADO | No se completó auditoría compilada.
| Repetición tras cancelar | NO EJECUTADO | Depende de cancelación compilada.
| Segunda instancia real | NO EJECUTADO | No se abrió ni observó un segundo ejecutable.
| Cierre normal y reinicio | NO EJECUTADO | La ventana queda abierta para revisión humana.
| Independencia de PATH restringido | NO EJECUTADO en esta sesión | W01-P ya registró ejecución empaquetada con PATH limitado desde `%TEMP%`.
| Limpieza tras éxito/cancelación/fallo/salida | NO EVALUABLE | No se ejecutaron esos ciclos desde el GUI compilado.

## Evidencia previa reutilizada de W01-P

- `PACKAGED_ONEDIR = PASS`; `DUCKDB_BUNDLED = YES` (DuckDB CLI 1.5.5).
- Worker empaquetado: auditoría sintética, 30 artefactos con hashes/manifiesto/sello, éxito/fallo/cancelación, post-cancel rerun y 0 descendientes huérfanos: PASS dentro del harness de integración.
- GUI compilada: inicio y respuesta ya verificados. El E2E de shell y el worker empaquetado usó harness; no sustituye la matriz de aceptación de GUI real.
- `CLEAN_MACHINE_VALIDATION = PENDING`.
- `ENGINE_SEMANTICS_CHANGED = NO`; `HOLDOUT_ACCESSED = NO`.

## Verificaciones de esta fase

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 12 tests; 11 PASS, 1 FAIL. Falló `WindowsInstanceLockTests.test_rejects_duplicate_and_allows_restart_after_release` porque la instancia real lanzada para esta aceptación ya poseía el mutex y el test esperaba adquirirlo como primera instancia. No es evidencia de defecto del mutex ni sustituye la prueba con dos ejecutables; la prueba queda pendiente de repetición tras cerrar la GUI normalmente.
- `git diff --check`: PASS (solo avisos de normalización CRLF; sin errores de whitespace).
- No se modificó código en W01-F. Esta fase fue exclusivamente de aceptación y registro.
- El estado Git conserva cambios W01 preexistentes; no se preparó, confirmó ni publicó ningún cambio.

## Resumen requerido

```ini
COMPILED_GUI_START = PASS
REAL_DIALOG_INTERACTION = NO_EJECUTADO
COMPILED_GUI_SUCCESS_E2E = NO_EJECUTADO
COMPILED_GUI_CANCEL_E2E = NO_EJECUTADO
COMPILED_GUI_FAILURE = NO_EJECUTADO
OPEN_DELIVERY = NO_EJECUTADO
SINGLE_INSTANCE_REAL_EXE = NO_EJECUTADO
POST_CANCEL_RERUN = NO_EJECUTADO
ORPHAN_PROCESSES = 1 tdl-client intencionadamente abierto; 0 workers iniciados
PACKAGED_ONEDIR = PASS (evidencia W01-P)
DUCKDB_BUNDLED = YES, DuckDB CLI 1.5.5 (evidencia W01-P)
CLEAN_MACHINE_VALIDATION = PENDING
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
TESTS = 12: 11 PASS, 1 FAIL (contención del mutex por GUI abierta)
git diff --check = PASS (avisos CRLF)
git status = cambios W01 preexistentes; sin cambios preparados
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Aceptación humana final — 2026-10-05

Resultados manuales comunicados y aceptados por Yeison:

```ini
W01-F = W01F_PASS_READY_FOR_W01_CLOSURE
COMPILED_GUI_START = PASS
REAL_DIALOG_INTERACTION = PASS
COMPILED_GUI_SUCCESS_E2E = PASS
OPEN_DELIVERY = PASS
COMPILED_GUI_CANCEL_E2E = PASS
CANCELLED_BEFORE_NORMAL_SUCCESS = YES
FILES_STOPPED_AFTER_CANCEL = YES
POST_CANCEL_RERUN = PASS
SINGLE_INSTANCE_REAL_EXE = PASS
SECOND_INSTANCE_REJECTED = PASS
FIRST_INSTANCE_STILL_USABLE = PASS
NORMAL_EXIT = PASS
RESTART_AFTER_EXIT = PASS
ORPHAN_PROCESSES_FINAL = 0
AUTOMATED_TESTS = 7/7 PASS
MUTEX_TEST_AFTER_GUI_CLOSED = PASS
PY_COMPILE = PASS
GIT_DIFF_CHECK = PASS
PACKAGED_ONEDIR = PASS
DUCKDB_BUNDLED = YES
CLEAN_MACHINE_VALIDATION = PENDING
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
```

`CLEAN_MACHINE_VALIDATION = PENDING` corresponde a una fase posterior de packaging/release. Siguen como limitaciones: soporte extremo de feeds sin certificar; hardware mínimo/recomendado no establecido; instalador de producción no declarado listo; QGIS como workbench externo de evidencia; presentación PDF/informes en W06; e ingeniería de releases fuera de W01. `W02 = NEXT / NOT_STARTED`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Continuación de aceptación — 2026-10-05

La comprobación del entorno de automatización confirmó que esta sesión no expone ventanas nativas: `cua.getState()` devolvió `apps = []` y `cua.listWindows` no está disponible. No se inició ni manipuló otra GUI. En consecuencia, los pasos manuales de F02, F04, F05 y F06 siguen sin evidencia directa del EXE. La clasificación continúa siendo `W01F_BLOCKED_GUI`; el E2E con callbacks/harness tampoco demuestra la interacción real de Cancelar.

Sí se completó la repetición automatizada solicitada con la GUI cerrada. La consulta de procesos `tdl-client`, `tdl-worker` y `duckdb` no encontró procesos activos antes de ejecutarla. Desde `02_Data_Engineering/GTFS_Lab`, con el intérprete del entorno Python local:

- `python -m unittest -v tests.test_client_app tests.test_client_packaging`: 7/7 PASS, incluidos el mutex (rechazo de duplicado y adquisición tras liberar), worker empaquetado exitoso con rutas Unicode y entrega verificada, y fallo genuino del worker.
- `python -m py_compile` sobre `client_app.py`, `client_worker.py`, `test_client_app.py` y `test_client_packaging.py`: PASS.
- `git diff --check`: PASS; Git mostró avisos informativos de normalización CRLF en tres archivos, sin errores de whitespace.
- La consulta final tampoco encontró procesos `tdl-client`, `tdl-worker` ni `duckdb`.

La evidencia W00 ya existente muestra que el fixture sintético S16 completó la auditoría del motor. Su ZIP reproducible mide 167.370 bytes, contiene 16.000 filas de `stop_times.txt` y tiene SHA-256 `32a040c26df65d1f7f12771e8ed3e35c3a6137ecedac4dc72f765fe83e8d1c2f`. Esa evidencia no registra un tiempo de ejecución que pruebe que S16 dure lo suficiente para pulsar Cancelar, y no demuestra F01/F02 en la GUI; no se afirma que se haya creado ni ejecutado ese fixture desde el EXE.

```ini
W01F_CLASSIFICATION = W01F_BLOCKED_GUI
COMPILED_GUI_START = PASS (evidencia previa; sin nueva interacción)
REAL_DIALOG_INTERACTION = NO EJECUTADO
COMPILED_GUI_SUCCESS_E2E = NO EJECUTADO
OPEN_DELIVERY = NO EJECUTADO
CANCELLATION_FIXTURE_SCALE = S16 candidate from existing W00 synthetic benchmark; runtime sufficiency not established
RESOURCE_PREFLIGHT = NO NUEVO PREFLIGHT; prior W00 synthetic S16 pipeline PASS
COMPILED_GUI_CANCEL_E2E = NO EJECUTADO
CANCELLED_BEFORE_NORMAL_SUCCESS = NO EVALUABLE
CANCEL_MESSAGE = NO EVALUADO EN EXE
GENERIC_ERROR_AFTER_CANCEL = NO EVALUADO EN EXE
ORPHAN_WORKERS_AFTER_CANCEL = NO EVALUABLE; no GUI worker started in this continuation
POST_CANCEL_RERUN = NO EJECUTADO EN EXE
SINGLE_INSTANCE_REAL_EXE = NO EJECUTADO
SECOND_INSTANCE_REJECTED = NO EJECUTADO EN EXE
FIRST_INSTANCE_STILL_USABLE = NO EJECUTADO
NORMAL_EXIT = NO EJECUTADO EN EXE
RESTART_AFTER_EXIT = NO EJECUTADO EN EXE
ORPHAN_PROCESSES_FINAL = 0 observed for tdl-client, tdl-worker, duckdb
MUTEX_TEST_AFTER_GUI_CLOSED = PASS
PACKAGED_ONEDIR = PASS (evidencia W01-P)
DUCKDB_BUNDLED = YES (evidencia W01-P)
CLEAN_MACHINE_VALIDATION = PENDING
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
TESTS = 7/7 PASS after GUI-closed mutex rerun
py_compile = PASS
git diff --check = PASS (avisos CRLF informativos)
git status = cambios W01 locales preexistentes y este informe actualizado; sin staging/commit
STOP = W01F_READY_FOR_HUMAN_REVIEW NOT REACHED
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
