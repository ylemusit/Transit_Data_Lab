# Windows Self-Service Client V1 — W08 Packaging / Release

**Estado:** `IN_PROGRESS` (2026-10-05).

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
- Falta repetir build/test con el commit limpio final y cerrar verificación de paquetes/fontes.

## EVIDENCE

El build de ensayo tiene metadata externa al repo en `C:\TDL\windows-client-v1-w08-build-rc1\build-metadata.json`. No es el artefacto final porque se generó durante cambios W08 sin commit. La campaña conserva esa evidencia local para diagnosticar y repetirá desde el commit limpio.

## LIMITATIONS

- No hay VM Windows externa ni Windows Sandbox disponible; clean-machine quedará parcial aunque el worker onedir pase con PATH/cwd aislados.
- La GUI RC no tiene aceptación visual/manual final en esta sesión.
- No se usó certificado de firma; SmartScreen no se ha establecido.

## DECISION

W08 sigue abierto hasta el build y regresión final desde worktree limpio, más clasificación honesta de entorno limpio y firma.

## NEXT PHASE

Completar W08, actualizar `PROJECT_STATUS.md`/`PROJECT_STATUS_TREE.md`, publicar branch y preparar PR de revisión humana sin merge.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
