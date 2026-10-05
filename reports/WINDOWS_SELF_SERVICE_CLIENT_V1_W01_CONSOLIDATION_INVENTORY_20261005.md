# W01 — inventario de consolidación — 2026-10-05

Base del worktree: `6271a75399732dfafcaef06ec5fd63ff5835a86b` (`origin/main`). Rama: `feat/windows-client-v1-w01`. Se revisaron 14 rutas de implementación/estado/informes W01 preexistentes y se añade esta ruta como evidencia de inventario (15 rutas seleccionadas en total); los resultados `build-w01p/` y `dist-w01p/` son directorios locales ignorados, no aparecen como cambios Git y no se publican.

| Ruta | Clasificación | Motivo |
|---|---|---|
| `.gitignore` | `MUST_COMMIT` | Excluye únicamente outputs reproducibles locales de W01-P. |
| `02_Data_Engineering/GTFS_Lab/gtfs_lab/compliance_adapter.py` | `MUST_COMMIT` | Resuelve recursos de Compliance desde el runtime PyInstaller; no cambia semántica del motor. |
| `02_Data_Engineering/GTFS_Lab/gtfs_lab/client_app.py` | `MUST_COMMIT` | GUI, coordinación de worker, cancelación, mutex y logging local. |
| `02_Data_Engineering/GTFS_Lab/gtfs_lab/client_worker.py` | `MUST_COMMIT` | Entrada ejecutable del worker separado. |
| `02_Data_Engineering/GTFS_Lab/packaging/runtime_path_hook.py` | `MUST_COMMIT` | Hook reproducible para resolución de recursos empaquetados. |
| `02_Data_Engineering/GTFS_Lab/packaging/tdl_client_onedir.spec` | `MUST_COMMIT` | Configuración reproducible PyInstaller onedir GUI + worker y DuckDB. |
| `02_Data_Engineering/GTFS_Lab/tests/test_client_app.py` | `MUST_COMMIT` | Regresión del shell y mutex. |
| `02_Data_Engineering/GTFS_Lab/tests/test_client_packaging.py` | `MUST_COMMIT` | Regresión del worker empaquetado. |
| `02_Data_Engineering/GTFS_Lab/tools/client_packaged_gui_e2e.py` | `MUST_COMMIT` | Harness reproducible de integración del shell empaquetado. |
| `PROJECT_STATUS.md` | `MUST_COMMIT` | Estado vigente y límites de fase. |
| `PROJECT_STATUS_TREE.md` | `MUST_COMMIT` | Mapa de estado sincronizado. |
| `reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_APPLICATION_SHELL.md` | `MUST_COMMIT` | Alcance, arquitectura, resultado y cierre W01. |
| `reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_P_PACKAGED_SHELL_INTEGRATION.md` | `MUST_COMMIT` | Evidencia de integración onedir y aceptación final. |
| `reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_F_FINAL_PACKAGED_GUI_ACCEPTANCE.md` | `MUST_COMMIT` | Registro histórico y decisión humana final. |
| `reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_CONSOLIDATION_INVENTORY_20261005.md` | `MUST_COMMIT` | Clasificación y política de publicación de este inventario. |

`SHOULD_COMMIT = none`; `LOCAL_EVIDENCE_PRESERVE = none inside this worktree`; `REPRODUCIBLE_DO_NOT_COMMIT = build-w01p/ and dist-w01p/ (ignored local outputs)`; `SAFE_TO_REMOVE_LATER = none`; `UNRELATED_DO_NOT_TOUCH = none identified`; `NEEDS_HUMAN_DECISION = none`.

Los logs y fixtures de aceptación manual se indicaron como evidencia local fuera del repositorio y no se copiaron aquí. No se encontraron datos privados de operador/cliente ni datos HOLDOUT entre las rutas clasificadas. Los cambios de estado de la aceptación provienen del resultado humano explícito comunicado para W01-F. Este inventario no declara validación en máquina limpia ni preparación de instalador de producción.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
