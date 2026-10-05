# Windows Self-Service Client V1 — W08 Packaging / Release

**Estado:** `PASS_WITH_LIMITATIONS / W08_HUMAN_ACCEPTANCE = BLOCKED_PENDING_DEFECT_RETEST` (2026-10-05).

## SCOPE

Fijar versión del producto, build onedir Windows reproducible, mecanismo de instalación por usuario y protocolo de validación/rollback.

## IMPLEMENTATION

- Versión de producto `1.0.0-rc.1`, separada de la versión GTFS_Lab y visible en GUI/manifest/PDF.
- Lock de build para CPython 3.12.10, PyInstaller, lxml, ReportLab y dependencias transitivas; DuckDB CLI se comprueba en 1.5.5.
- `build-client-onedir.ps1` exige checkout limpio, genera onedir en output externo nuevo y registra `build-metadata.json` sin rutas locales.
- Scripts de instalación/desinstalación por usuario actual con carpeta versionada y confirmación antes de eliminar solo esa versión.
- Docs de release candidata recogen reconstrucción, instalación, rollback, hardware, firma y límites de clean-machine.

## TESTS

- El build onedir de ensayo produjo GUI y worker desde entorno Python aislado.
- La suite empaquetada de worker pasó 2/2 en PATH reducido; la suite client completa dio 25/25 PASS, incluidos esos casos.
- Instalación y desinstalación de ensayo pasaron en una ruta temporal; el test no requiere admin.
- Build final limpio y suite completa: `311 tests OK (3 skipped)`; suite client contra el worker del paquete final: `25/25 PASS`, sin skips.
- `py_compile` y `git diff --check`: `PASS`.
- Verificación final de instalación/desinstalación por usuario en ruta temporal: `PASS`; el acceso directo y la carpeta de prueba se retiraron.

## EVIDENCE

El build final externo al repo se generó desde el commit limpio `d050f536c29fb58106d6924055015e75ab621eb7`. Metadata en `C:\TDL\windows-client-v1-w08-build-final-rc1\build-metadata.json`; SHA-256 `441259F22C34F82674C833E2D98032A13C932971D425E91B99FEF806D43BE805`. Versiones observadas: Python 3.12.10, PyInstaller 6.22.3, ReportLab 5.0.1 y DuckDB CLI 1.5.5. Los binarios quedan en esa ruta local externa; no se añaden al repositorio.

## LIMITATIONS

- No hay VM Windows externa ni Windows Sandbox disponible; clean-machine quedará parcial aunque el worker onedir pase con PATH/cwd aislados.
- La GUI RC no tiene aceptación visual/manual final en esta sesión.
- No se usó certificado de firma; SmartScreen no se ha establecido.

## DECISION

La evaluación técnica de packaging conserva `PASS_WITH_LIMITATIONS`: la build limpia y las regresiones pasan; clean-machine sigue parcial/bloqueado por entorno. La aceptación humana que estaba pendiente reprodujo ahora un defecto funcional y permanece bloqueada hasta el retest del RC corregido.

## NEXT PHASE

### APPLICATION_DEFECT_001 — TERMINAL_STATE_DOES_NOT_REARM_NEW_RUN

- `ROOT_CAUSE`: `_refresh_ready_state()` solo consideraba `IDLE` y `READY`; tras una ejecución el estado terminal impedía volver a preparar una auditoría.
- `FIX`: transición explícita de preparación de run que desconecta referencias anteriores, desactiva acciones de resultados/entrega/GIS y conserva sus ficheros. El `audit_id` se genera al pulsar Start.
- `AUTOMATED_REGRESSION`: cliente empaquetado 26/26 PASS; GUI/worker del onedir completa éxito → nueva entrada/destino → éxito, cancelación y rerun; GTFS_Lab 303 PASS / 3 SKIP, excluida la prueba histórica que lee evidencia HOLDOUT; `py_compile` y `git diff --check` PASS.
- `NEW_RC_BUILD`: `1.0.0-rc.1`, onedir, source commit `a3a1ddef92df6e252d995405d62250ea0583a433`; metadata externa `C:\TDL\windows-client-v1-w08-terminal-rearm-rc1\build-metadata.json`, SHA-256 `D207EEB67503029B9048A7321C759B7C5AFEE683A4EE71E42A593037C497DCA6`.
- `INSTALLED_EXE_SHA256`: `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266` (igual al EXE construido).
- `W08_HUMAN_ACCEPTANCE`: `BLOCKED_PENDING_DEFECT_RETEST`.
- HOLDOUT no se accedió. PR #51 sigue sin merge; no se publicó release.

Siguiente paso: repetir únicamente la secuencia humana afectada documentada en `C:\TDL\W08_RC_HUMAN_ACCEPTANCE\06_notes\W08_RC_HUMAN_ACCEPTANCE_LOG.md`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
