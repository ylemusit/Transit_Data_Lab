# Repository Integrity Report

Fecha: 2026-09-27. Recomendación: **NO iniciar Phase 2 todavía**.

No se detectó pérdida del baseline GTFS ni alteración estructural de Compliance Phase 1. La pausa se recomienda por gobierno e integridad operativa del repositorio padre, no por corrupción de datos.

## Alcance y método

- Inspección de filesystem, scripts/documentos relevantes y catálogos DuckDB.
- DuckDB 1.5.5 abierto con `-readonly`.
- Ejecución de los masters existentes de Compliance y del nuevo sentinel GTFS.
- Inspección Git read-only de los cuatro repositorios anidados detectados.
- Hashes SHA-256 antes/después de las bases.
- Sin commit, push, modificación de bases, feeds, corpus, exports o ficheros preexistentes.

Limitación: varios directorios de runtime bajo GTFS Explorer Artifacts devolvieron acceso denegado. El inventario global visible por `rg` fue de 280.528 ficheros, pero esa cifra incluye repositorios, backups y artefactos y no debe interpretarse como censo completo verificable.

## Estructura real

La jerarquía de seis áreas coincide nominalmente con la arquitectura objetivo. Solo GTFS_Lab, Compliance y Products contienen trabajo material; Research & Standards, los otros labs, Interoperability y Audits son esqueletos vacíos. El trabajo de auditoría de 20 operadores permanece bajo GTFS_Lab.

## Diferencias relevantes frente al contexto recibido

1. GTFS_Lab no contiene la estructura `core -> validation -> analysis -> GIS`: únicamente `raw` y `main.stops` están persistidos.
2. Los directorios SQL reales son `02_exploration`, `03_validation` y `04_analysis`; no existen las ramas históricas `02_core`, `05_gis` o `06_reports`.
3. El README principal de GTFS_Lab existe pero está vacío.
4. Los KML existen, pero no sus SQL/scripts de generación.
5. Compliance coincide con el catálogo esperado y Phase 1 permanece congelada.
6. La raíz Transit Data Lab no es Git; Products conserva repositorios Git separados.

## Git

| Repositorio | HEAD | Estado |
|---|---|---|
| GTFS Explorer Desktop | `38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd` | `main`, 20 entradas: 17 modificadas y 3 nuevas. |
| GTFS Explorer Engineering | `efdfe91c2c888bf7e3de6c72a29e4e2ee8f0abbf` | `main`, 1 modificado. |
| GTFS Explorer Artifacts | `d49ef160b1e1685c143389f86ecf9643af1f4f03` | `main`, 4 nuevos. |
| restore test v0.2.2 | `85c700587ffec06d73d84825e1951fb73259b62c` | detached, limpio. |

Estos cambios se preservaron. Como la raíz no es Git, no existe una clasificación tracked/untracked/ignored para GTFS_Lab o Compliance. Tampoco hay política `.gitignore` de raíz; el ignore de `20_clientes_reales` solo cubre temporales/cachés.

## Paths y migración

- Los scripts de Compliance usan la ruta absoluta actual; no están rotos aquí, pero son no portables.
- Tres filas `source.documents.local_file` usan rutas absolutas actuales.
- El import GTFS usa rutas relativas válidas solo si DuckDB se ejecuta desde GTFS_Lab.
- Documentación current de Engineering y scripts de evidencia siguen apuntando a los antiguos roots `.../Proyectos/GTFS Explorer Desktop|Engineering|Artifacts`, que ya no existen tras la migración.
- `AGENTS.md` de Desktop apunta a la telemetría de Codex y esa ruta sí existe.
- La referencia a `Downloads/ctm-mallorca-es.zip` también existe actualmente.

El detalle accionable está en `PATH_MIGRATION_FINDINGS.csv`.

## Duplicación y material posiblemente abandonado

- `main.stops` es una copia exacta por conjuntos de `raw.stops`.
- Dos exports Bizkaibus de 18.390.746 bytes son idénticos entre `run_001` y `run_002_rc002`; sus manifests también son idénticos. Pueden ser evidencia histórica intencionada, por lo que no se recomienda borrar sin decisión de retención.
- Se observan ocho bases `data.duckdb` y ocho backups `*.editor-pre-migration.bak` dentro de resultados de operadores. Son artefactos diferenciados por run, no duplicados confirmados por hash en esta auditoría.
- Products contiene repositorios, backups y runtime packaging bajo el mismo árbol; requiere política de retención, no limpieza automática.

## Severidad

### CRITICAL

Ninguno.

### HIGH

- `RI-H01`: la raíz no es un repositorio Git. No puede demostrarse integridad tracked/untracked/ignored ni protegerse Phase 2 con un baseline del proyecto padre.

### MEDIUM

- `RI-M01`: capas GTFS core, validation y analysis ausentes respecto a la arquitectura descrita.
- `RI-M02`: scripts/rutas de reproducción GIS no encontrados.
- `RI-M03`: documentación operativa GTFS vacía y ausencia de documentación raíz previa a esta auditoría.
- `RI-M04`: rutas pre-migración rotas en documentación current y scripts de evidencia de GTFS Explorer.
- `RI-M05`: no existe política de ignore/retención para los 1,37 GB de Data Engineering ni para bases, feeds, exports y corpus Compliance.
- `RI-M06`: tres repositorios de producto contienen cambios locales no cerrados. No se evalúa su corrección, solo su estado.

### LOW

- `RI-L01`: rutas absolutas actuales en scripts y tres registros Compliance reducen portabilidad.
- `RI-L02`: `main.stops` duplica `raw.stops` sin documentación.
- `RI-L03`: export y manifest Bizkaibus repetidos byte a byte entre dos runs.
- `RI-L04`: cobertura incompleta de directorios runtime de Artifacts por acceso denegado.

### INFO

- `RI-I01`: GTFS-RT, NeTEx, SIRI, Interoperability y Audits están planificados pero vacíos.
- `RI-I02`: Annex 1.3 B-I/D-I sigue visible sin modificación.
- `RI-I03`: Compliance Phase 1 y el baseline raw GTFS pasan los controles ejecutados.

## Condiciones recomendadas antes de Phase 2

1. Decidir y documentar si Transit Data Lab será un único repositorio Git, un superproyecto con repos anidados o un workspace gobernado por manifest.
2. Definir qué bases, feeds, corpus, exports, backups y reports se versionan, ignoran o almacenan externamente.
3. Corregir o congelar explícitamente las referencias pre-migración de Products.
4. Decidir si Phase 2 puede comenzar con GTFS_Lab todavía limitado a raw o si core/validation/analysis son precondición.
5. Capturar un baseline Git limpio o una excepción documentada para los cambios locales de Products.

No se inició Phase 2.

---

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

