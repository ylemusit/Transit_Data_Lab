# Windows Self-Service Client V1 — W08 Packaging / Release

**Estado:** `PASS_WITH_LIMITATIONS` (2026-10-05).

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

W08 queda cerrado como `PASS_WITH_LIMITATIONS`. La build limpia y regresiones pasan; clean-machine sigue parcial/bloqueado por entorno y la GUI RC queda pendiente de aceptación visual/manual humana.

## NEXT PHASE

W08 completado. Publicar branch y preparar PR para revisión humana sin merge ni publicación de release.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
