# Windows Self-Service Client V1 — W08 Packaging / Release

**Estado de packaging:** `PASS_WITH_LIMITATIONS`. **Estado vigente (2026-10-05):** `W08_HUMAN_ACCEPTANCE = PASS`; `FINAL_ACCEPTANCE = PASS_WITH_LIMITATIONS`; `APPLICATION_DEFECT_001 = CLOSED_FIXED_AND_VERIFIED`. Los estados de aceptación bloqueada/en curso que aparecen en entradas previas son históricos y quedaron supersedidos por esta consolidación final.

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
- La aceptación visual/manual de la GUI RC está completada según la consolidación final al final de este informe.
- No se usó certificado de firma; SmartScreen no se ha establecido.

## DECISION

La evaluación técnica de packaging conserva `PASS_WITH_LIMITATIONS`: la build limpia y las regresiones pasan; clean-machine sigue parcial/bloqueado por entorno. En la evaluación humana inicial se reprodujo un defecto funcional; su retest posterior y cierre constan al final de este informe.

## NEXT PHASE

### APPLICATION_DEFECT_001 — TERMINAL_STATE_DOES_NOT_REARM_NEW_RUN

- `ROOT_CAUSE`: `_refresh_ready_state()` solo consideraba `IDLE` y `READY`; tras una ejecución el estado terminal impedía volver a preparar una auditoría.
- `FIX`: transición explícita de preparación de run que desconecta referencias anteriores, desactiva acciones de resultados/entrega/GIS y conserva sus ficheros. El `audit_id` se genera al pulsar Start.
- `AUTOMATED_REGRESSION`: cliente empaquetado 26/26 PASS; GUI/worker del onedir completa éxito → nueva entrada/destino → éxito, cancelación y rerun; GTFS_Lab 303 PASS / 3 SKIP, excluida la prueba histórica que lee evidencia HOLDOUT; `py_compile` y `git diff --check` PASS.
- `NEW_RC_BUILD`: `1.0.0-rc.1`, onedir, source commit `a3a1ddef92df6e252d995405d62250ea0583a433`; metadata externa `C:\TDL\windows-client-v1-w08-terminal-rearm-rc1\build-metadata.json`, SHA-256 `D207EEB67503029B9048A7321C759B7C5AFEE683A4EE71E42A593037C497DCA6`.
- `INSTALLED_EXE_SHA256`: `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266` (igual al EXE construido).
- Estado en el momento de redactar este bloque: `W08_HUMAN_ACCEPTANCE = BLOCKED_PENDING_DEFECT_RETEST`; supersedido por el retest manual al final del informe.
- HOLDOUT no se accedió. PR #51 sigue sin merge; no se publicó release.

Nota histórica al cierre anterior: se solicitó repetir únicamente la secuencia humana afectada documentada en `C:\TDL\W08_RC_HUMAN_ACCEPTANCE\06_notes\W08_RC_HUMAN_ACCEPTANCE_LOG.md`. El retest se completó; resultado actualizado al final de este informe.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## W08 HUMAN ACCEPTANCE — RETEST DEL DEFECT (2026-10-05)

**Resultado humano recibido:** `APPLICATION_DEFECT_001 = CLOSED_FIXED_AND_VERIFIED`; `W08_HUMAN_ACCEPTANCE = IN_PROGRESS`.

Retest manual del EXE RC:

- `NORMAL_SUCCESS = PASS`; `SUCCESS_TO_NEW_RUN_READY = PASS`; `S32_INTAKE = PASS`.
- Nuevo destino: `C:\TDL\W08_RC_HUMAN_ACCEPTANCE\03_cancel`.
- `START_BUTTON_REENABLED = PASS`; `STALE_RESULTS_ACTIONS_RESET = PASS`.
- `CANCEL_REAL_EXE = PASS`; `CANCEL_FINAL_STATE = CANCELLED`; `SUCCESSFUL_DELIVERY_AFTER_CANCEL_EXPOSED = NO`.
- `POST_CANCEL_RERUN = PASS`; salida `C:\TDL\W08_RC_HUMAN_ACCEPTANCE\04_post_cancel`; `POST_CANCEL_FINAL_STATE = SUCCEEDED`; `POST_CANCEL_FINDINGS = 0`; `POST_CANCEL_DELIVERY_ARTIFACTS = 33`.

En el momento de este retest la aceptación global seguía en curso. La aceptación final y el estado de todos los checks se consolidan en la siguiente sección.

## FINAL HUMAN ACCEPTANCE CONSOLIDATION (2026-10-05)

```ini
W02 = PASS_WITH_LIMITATIONS
W03 = PASS_WITH_LIMITATIONS
W04 = PASS_WITH_LIMITATIONS
W05 = PASS_WITH_LIMITATIONS
W06 = PASS_WITH_LIMITATIONS
W07 = PASS_WITH_LIMITATIONS
W08 = PASS_WITH_LIMITATIONS
W08_HUMAN_ACCEPTANCE = PASS
FINAL_ACCEPTANCE = PASS_WITH_LIMITATIONS
APPLICATION_DEFECT_001 = CLOSED_FIXED_AND_VERIFIED
RC_SOURCE_COMMIT = a3a1ddef92df6e252d995405d62250ea0583a433
RC_EXE_SHA256 = 3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266
CLEAN_MACHINE_VALIDATION = PARTIAL / BLOCKED_BY_ENVIRONMENT
CODE_SIGNING = NOT_USED
SMARTSCREEN_REPUTATION = NOT_ESTABLISHED
MINIMUM_HARDWARE = NOT_YET_ESTABLISHED
RECOMMENDED_HARDWARE = NOT_YET_ESTABLISHED
EXTREME_FEED_SUPPORT = NOT_CERTIFIED
DATASET_019 = DEFERRED
HOLDOUT_ACCESSED = NO
OPERATOR_SPECIFIC_CODE = NO
RELEASE_PUBLISHED = NO
```

### Manual acceptance flow — PASS

- Instalación del RC y lanzamiento desde el menú Inicio.
- Intake GTFS válido, identidad del dataset y auditoría normal completada.
- UX de resultados y apertura/inspección visual del PDF.
- Exportación GIS; GeoJSON abierto en QGIS y KML abierto en Google Earth.
- Segunda auditoría secuencial tras un éxito anterior.
- Cancelación del EXE real y rerun posterior completado.
- ZIP malformado bloqueado durante intake.
- Segunda instancia rechazada; cierre y reinicio de la aplicación.
- Desinstalación y comprobación de que las salidas de auditoría se conservaron.

### Final verification

- `AUTOMATED_TESTS`: suite cliente 26/26 PASS.
- `PACKAGED_TESTS`: 2/2 PASS contra `C:\TDL\windows-client-v1-w08-terminal-rearm-rc1\dist\tdl-client\tdl-worker.exe`.
- `GTFS_LAB_REGRESSION`: 306 tests, 1 SKIP, 0 failures. Se excluyó `test_m05c_historical_proof.py`, el módulo que lee evidencia histórica HOLDOUT; no se accedió a esa evidencia.
- `PY_COMPILE`: `python -m compileall -q gtfs_lab tests` PASS.
- `GIT_DIFF_CHECK`: `git diff --check` PASS.
- El RC instalado corresponde al source commit `a3a1ddef92df6e252d995405d62250ea0583a433`; el EXE instalado y el binario reconstruido coinciden en SHA-256 `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266`.

HOLDOUT no se accedió y no se ejecutaron pruebas que lean su evidencia. No se añadió lógica específica de operador. PR #51 sigue abierta para decisión humana; no se fusionó y no se publicó release.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
