# Windows Self-Service Client V1 — Release Candidate

**Versión:** `1.0.0-rc.1`

**Clasificación:** `RELEASE_CANDIDATE_READY_WITH_LIMITATIONS`

## Producto

Aplicación de escritorio Windows para auditar localmente un GTFS ZIP. No requiere cuenta, backend, servicio cloud ni instalación de QGIS. El EXE GUI lanza un worker aislado; DuckDB CLI y los runtimes Python/ReportLab están incluidos en el onedir.

## Build reproducible

Entorno validado: Windows 11 x64, CPython 3.12.10, PyInstaller 6.22.3, lxml 6.1.3, ReportLab 5.0.1 y DuckDB CLI 1.5.5. Las dependencias Python de build quedan fijadas en `packaging/client-build-requirements.txt`. El build script comprueba versiones, exige un worktree limpio, mantiene los binarios fuera del checkout y genera `build-metadata.json` sin rutas locales.

Desde `02_Data_Engineering/GTFS_Lab`, en PowerShell:

```powershell
./packaging/build-client-onedir.ps1 `
  -DuckDBCliPath 'C:\ruta\aprobada\duckdb.exe' `
  -OutputRoot 'C:\TDL\windows-client-build-1.0.0-rc.1'
```

`OutputRoot` debe no existir previamente. La salida incluye `dist/tdl-client/` y build metadata. No se versionan EXE, DLL, builds ni datasets.

## Instalación y ejecución

1. Distribuir el contenido de `dist/tdl-client/` dentro de un ZIP de release candidate.
2. Extraerlo localmente y ejecutar en PowerShell de usuario normal:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\Install-Client.ps1
   ```

3. Abrir **Transit Data Lab GTFS Auditor** desde el menú Inicio.
4. Para quitar esta versión, ejecutar `Uninstall-Client.ps1`; solicita confirmación literal y elimina solo su carpeta de programa versionada y acceso directo. No borra outputs de auditoría.

No se requieren privilegios de administrador, Python, VS Code ni DuckDB instalados en el equipo usuario.

## Verificación W08

- Build onedir desde entorno Python aislado con versiones fijadas: `PASS`.
- Worker empaquetado con PATH reducido a Windows System32, sin checkout, Python ni instalación de DuckDB: éxito E2E con ruta Unicode; PDF, GeoJSON/KML, guide QGIS, manifest, seal y SHA-256 verificados: `PASS`.
- Worker empaquetado con ZIP inválido: `BLOCKED_INPUT_INVALID`, exit code 2: `PASS`.
- Suite client en el build onedir final: `25/25 PASS`, 0 skips.
- Instalación/desinstalación por usuario en carpeta temporal: `PASS`; no requiere admin y elimina solo artefactos del test.
- `py_compile` y `git diff --check`: `PASS`.
- Inspección PDF sintética: 1 y 5 páginas renderizadas e inspeccionadas; acentos y saltos de tabla legibles.

## Validación limpia

`CLEAN_MACHINE_VALIDATION = PARTIAL / BLOCKED_BY_ENVIRONMENT`. No había VM Windows externa, Windows Sandbox ni segundo equipo genuinamente limpio disponible. El sustituto aisló el worker empaquetado con PATH restringido y cwd fuera del checkout. La instalación se comprobó en el host de desarrollo, no en una máquina limpia. La aceptación visual/manual de la GUI RC y su cancelación/reinicio desde EXE requiere la revisión humana de este release candidate; no se infiere del test del worker.

## Límites y release authority

- QGIS es externo; solo se probaron las capas GeoJSON/KML ya producidas y la guía de acceso. GeoPackage no se genera.
- `MINIMUM_HARDWARE = NOT_YET_ESTABLISHED`; `RECOMMENDED_HARDWARE = NOT_YET_ESTABLISHED`; feeds extremos no certificados; dataset 019 permanece diferido.
- `CODE_SIGNING = NOT_USED`; hay un certificado local con cadena confiable y clave disponible, pero su identidad e idoneidad para este producto no se han validado. No se firmó el RC. `SMARTSCREEN_REPUTATION = NOT_ESTABLISHED`.
- No se accedió a HOLDOUT, no hay lógica específica de operador y no cambiaron semánticas del motor/compliance/interpretación.
- El PDF es presentación; JSON, findings, manifest y seal conservan la autoridad técnica.
- Esta es una release candidate sin publicar. La PR queda para revisión humana; no se fusiona ni se publica una release pública.

## Rollback / rebuild

Cada versión se instala en un directorio separado por versión. Para volver atrás, desinstale únicamente la versión RC desde el script incluido y vuelva a instalar la versión previa. Para reconstruir, use el commit versionado y las versiones de `client-build-requirements.txt`, además de DuckDB CLI 1.5.5; conserve `build-metadata.json` con la salida local.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
