# Phase 1.5 — Repository Stabilization

Fecha: 2026-09-27. Ejecución local en Transit Data Lab. No se hizo commit ni push. Compliance Phase 1 sigue congelada y no se implementó Phase 2.

## Resultado

- Git raíz: **PASS**. Repositorio inicializado en Transit Data Lab, rama `main`, sin commits ni remotos.
- Repositorios anidados: Desktop (`38e0e96`, main), Engineering (`efdfe91`, main), Artifacts (`d49ef16`, main) y restore test (`85c7005`, detached). El restore estaba limpio. Desktop tenía 3 cambios locales; Engineering 1; Artifacts 1 carpeta untracked antes de este trabajo. Se mantienen separados; el padre los ignora íntegramente. Las modificaciones autorizadas a scripts históricos quedaron solo en el working tree de Engineering y sin commit.
- `.gitignore`: creado en raíz. Excluye DuckDB/WAL, feeds GTFS raw/extracted, temporales, secretos, los cuatro repositorios anidados y `GTFS Explorer Backups`. Mantiene elegibles SQL, PowerShell, Markdown, JSON, código, manifests y reports.
- Retención: no se ignoran PDFs jurídicos. Se conservan los 12 PDF presentes (40.436.167 bytes); las 10 fuentes registradas en Compliance existen y sus hashes verificados coinciden. Permanecen elegibles para versionado por el repositorio padre.
- DuckDB y feeds: no se versionan normalmente. Los feeds existentes permanecen en disco; no se eliminaron ni movieron. No se modificaron tablas ni datos.

## Paths

Se revisaron individualmente los 23 hallazgos en `PATH_MIGRATION_FINDINGS.csv`, con clasificación añadida:

- 15 `SAFE_TO_RELATIVIZE` resueltos: PATH-001–014 y PATH-021. Los scripts Compliance resuelven el root desde `$PSScriptRoot`; el SQL fuente Compliance ya no fija el root local. Se añadió un runner GTFS que fija el directorio del laboratorio antes de ejecutar el SQL relativo. Los scripts ejecutables de evidencia de GTFS Explorer localizan sus repositorios relativos al script.
- PATH-015 queda `CURRENT_ABSOLUTE`: tres valores `source.documents.local_file` de la base existente. Se preservaron para mantener íntegra la base y sus hashes; los ficheros están presentes y verificados.
- PATH-016–020 se clasificaron `INTENTIONAL`: son referencias de procedencia en documentación/evidencia histórica. Algunas rutas ya no existen, pero describen dónde se generaron o almacenaron pruebas antiguas; no se reescribieron como si la evidencia histórica hubiera ocurrido en la nueva ruta.
- PATH-022–023 son `EXTERNAL_REFERENCE`: telemetry externa y snapshot local de Downloads, ambos existentes.
- Paths ejecutables rotos de severidad HIGH: **0**. Hallazgos CRITICAL: **0**. Quedan referencias históricas de severidad media y tres rutas absolutas en los metadatos de la base, sin impacto en los ejecutables actuales.

## Gates y hashes

- GTFS integrity: **PASS para los datos**. Siete conteos coinciden: agency 41, calendar_dates 3.875, routes 609, shapes 774.732, stop_times 354.287, stops 6.368, trips 21.015. El sentinel conserva el warning de capas futuras ausentes (`core`, `validation`, `analysis`); esto está aceptado. El runner nuevo pasó análisis sintáctico PowerShell; no se ejecutó el import porque reemplaza tablas y cambiaría la base protegida.
- Compliance Phase 1 master: **24/24 PASS**.
- 2017/1926 structural master: **21/21 PASS**; 92 provisions conservadas.
- Legal sources: **10/10 presentes; 10/10 SHA-256 PASS**.
- PowerShell: 17 scripts modificados/afectados pasaron análisis sintáctico.
- SHA-256 antes y después, idéntico:

| Base | Antes | Después |
|---|---|---|
| `gtfs_lab.duckdb` | `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc` | `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc` |
| `transit_compliance.duckdb` | `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5` | `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5` |

Salidas completas de los tres masters y la verificación de fuentes están en `reports/repository_integrity/phase_1_5/`.

## Archivos del padre

Modificados o creados: `.gitignore`, `PROJECT_CURRENT_STATE.md`, `project_baseline.json`, `reports/repository_integrity/PATH_MIGRATION_FINDINGS.csv`, y evidencias nuevas bajo `reports/repository_integrity/phase_1_5/`.

También se creó `02_Data_Engineering/GTFS_Lab/sql/01_import/run_import_consorcio_asturias.ps1`. En el repositorio hijo Engineering se corrigieron cuatro scripts de ejecución de evidencia. Los scripts de Compliance modificados son los 12 enumerados por PATH-002–013; `002_update_compliance_2026.sql` también quedó con paths relativos.

## Git status y decisión

El repositorio padre está sin commits. `git status --short` muestra únicamente contenido del padre no añadido (`.gitignore`, `02_Data_Engineering`, `03_Compliance`, `PROJECT_CURRENT_STATE.md`, `project_baseline.json` y `reports`); los repositorios producto y los backups están ignorados y conservan su propio estado. No se preparó ningún archivo con `git add`.

**READY_FOR_PHASE_2 = YES.** Los gates solicitados pasan; la advertencia de capas GTFS futuras está explícitamente aceptada. Phase 2 no se inició.

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
