# Transit Data Lab — Current State

Auditado el 27 de septiembre de 2026 mediante consultas DuckDB read-only, inspección del filesystem y lectura de los repositorios Git anidados. Este documento describe únicamente hechos observados. No certifica interpretación jurídica ni fidelidad textual del corpus.

## Project purpose

Transit Data Lab es el contenedor padre para investigación de estándares, ingeniería de datos, Compliance, interoperabilidad, auditorías y productos de transporte público. La separación observada y asumida como contrato es:

- `GTFS Explorer`: producto.
- `GTFS_Lab`: laboratorio de datos y validación.
- `03_Compliance`: corpus, requisitos, mappings y auditoría jurídica, con base independiente.
- `04_Interoperability`: mappings entre estándares, no conversiones 1:1.

## Repository architecture

La raíz contiene los seis directorios conceptuales esperados. Estado físico:

| Área | Estado observado |
|---|---|
| `01_Research_Standards` | Solo estructura de directorios; 0 archivos. |
| `02_Data_Engineering` | 450 archivos, 1.374.559.240 bytes tras añadir el test autorizado. GTFS_Lab contiene el trabajo real; GTFS-RT, NeTEx y SIRI están vacíos. |
| `03_Compliance` | 54 archivos, 45.661.166 bytes. Base, corpus, SQL y tests presentes. |
| `04_Interoperability` | Solo estructura de directorios; 0 archivos. |
| `05_Audits` | Solo estructura de directorios; 0 archivos. |
| `06_Products` | Contiene GTFS Explorer Desktop, Engineering, Artifacts y Backups como repositorios/colecciones separados. |

La raíz de Transit Data Lab tiene un repositorio Git padre sin commits. Cuatro repositorios anidados de GTFS Explorer se mantienen aislados e ignorados por el índice padre mediante `.gitignore`.

## GTFS Lab

**IMPLEMENTED:** raw, DuckDB, feed import, integrity baseline verified/frozen y GIS outputs existentes (tres KML conservados; no existe pipeline GIS reproducible).

**PLANNED / NOT IMPLEMENTED:** `core`, `validation`, `analysis` y pipeline GIS reproducible. Su ausencia es una advertencia aceptada y no bloquea Compliance Phase 2.

### Database

- Ruta: `02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb`.
- SHA-256 auditado: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Abre con DuckDB CLI 1.5.5 en modo read-only.
- Esquema de usuario persistido: `raw`.
- Relaciones: siete tablas `raw.*` y una tabla adicional `main.stops`.
- `main.stops` tiene 6.368 filas y es equivalente por conjuntos a `raw.stops`; su propósito no está documentado.

No existen los esquemas `core`, `validation` ni `analysis`, ni vistas persistidas.

### Import pipeline

El feed fuente y la extracción están presentes:

- ZIP: `feeds/raw/20260924_020003_Consorcio_Asturias.zip`.
- SHA-256: `f3093ab85d728ee824ba45cd3f247d1d9ea68a4685aaf25b27a8de98ea50b549`.
- Siete entradas ZIP; las siete existen extraídas y cada hash coincide.
- No existe `calendar.txt`; sí `calendar_dates.txt`.
- El SQL existente importa mediante `read_csv(..., all_varchar = true)` y usa rutas relativas a `GTFS_Lab`.

### Raw layer

Conteos observados y coincidentes con el baseline:

| Tabla | Filas |
|---|---:|
| `raw.agency` | 41 |
| `raw.calendar_dates` | 3.875 |
| `raw.routes` | 609 |
| `raw.shapes` | 774.732 |
| `raw.stop_times` | 354.287 |
| `raw.stops` | 6.368 |
| `raw.trips` | 21.015 |

Todas las columnas raw, incluidas `arrival_time` y `departure_time`, permanecen como `VARCHAR`.

### Core layer

`NOT_FOUND`. No existe esquema `core`, SQL de construcción ni objetos tipados persistidos.

### Validation

`NOT_FOUND` como motor del GTFS_Lab. El directorio `sql/03_validation` está vacío y `validation.results` no existe. Las familias indicadas —required files/fields, claves duplicadas, FK, coordenadas, secuencias, semántica temporal, monotonicidad, geometría, huérfanos, no usados, rutas sin viajes, proximidad a shape y URLs— no están implementadas en el laboratorio.

El nuevo `sql/07_tests/test_gtfs_lab_integrity.sql` es únicamente un sentinel read-only de integridad del baseline; no sustituye un validador GTFS.

### Analysis

`NOT_FOUND`. `sql/04_analysis` está vacío y no existe esquema `analysis`.

### GIS

No se localizaron SQL ni scripts GIS. Sí existen tres exportaciones KML para `route_id = 440`:

- `route_440.kml`: 2 LineString, 814 coordenadas.
- `route_440_dir0.kml`: 1 LineString, 377 coordenadas.
- `route_440_dir1.kml`: 1 LineString, 437 coordenadas.

Los bounds observados son longitud -5,67 a -5,63 y latitud 43,36 a 43,39, coherentes con Asturias y con el orden KML longitud/latitud. No se regeneraron.

### Known baselines

- Duplicados de claves estructurales examinadas: 0.
- Referencias huérfanas examinadas: 0.
- Coordenadas fuera de rango o no numéricas: 0.
- Secuencias inválidas/no crecientes: 0.
- Filas con llegada o salida a partir de 24:00:00: 201.
- Hora máxima observada: 24.
- Ruta 440: 1 ruta, 2 viajes, 2 shapes y 814 puntos.

### Known limitations

- `README.md` del GTFS_Lab está vacío.
- No hay scripts reproducibles para las exportaciones KML existentes.
- El SQL de importación conserva rutas relativas al GTFS_Lab y se ejecuta mediante `run_import_consorcio_asturias.ps1`, que fija el directorio del proyecto.
- La tabla `main.stops` duplica por contenido a `raw.stops` sin documentación.

## GTFS-RT Lab

Directorio presente y vacío. `PLANNED`.

## NeTEx Lab

Directorio presente y vacío. `PLANNED`.

## SIRI Lab

Directorio presente y vacío. `PLANNED`.

## Compliance

Phase 1 legal corpus = FROZEN. Phase 2 requirements engine = FROZEN.
Alcance: EU-REG-2017-1926, versión consolidada 2024-03-04. Promoción autorizada: 2026-09-27T01:18:24.849175+00:00.

### Database

- Ruta: `03_Compliance/databases/transit_compliance.duckdb`.
- Compliance DB SHA-256: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.
- Baseline histórico Phase 1 preservado: `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`.
- Acceso read-only; ninguna escritura en DuckDB durante la promoción.
- Esquemas: `source`, `compliance`, `mapping`, `audit`, `analysis`.

### Estado congelado

| Elemento | Estado |
|---|---|
| provisions | 92 |
| source facts | 36 |
| requirements | 48 aprobados/materializados (48/48) |
| deadlines | 10 registros; 10 fechas explícitas |
| dependencias externas | 7 PARTIAL |
| functional time requirements | 5 |
| Gate 1 | CLOSED |
| Gate 2 | CLOSED |
| materialization | PASS |
| freeze review | PASS; 0 bloqueos |
| mapping.format_coverage | 0; pendiente |
| audit.rules | 0; pendiente |

### Legal corpus y tests

10 documentos con URL oficial, fichero local y SHA-256 válido; 6 relaciones.
Los 92 provisions y las fuentes de Phase 1 permanecen sin cambios.
Validación final read-only: invariantes Phase 1 22/22 PASS; estructura 22/22 PASS;
anexos 7 suites, 63/63 PASS; hashes jurídicos 10/10 PASS; gate posterior 387/387 PASS.
Los tests de estado histórico y su evidencia permanecen intactos.

### Límites y exclusiones

- Annex 1.3 B-I y Annex 1.3 D-I: anomalías conocidas conservadas.
- Siete dependencias externas permanecen PARTIAL; interpretación pendiente.
- Tres valores `source.documents.local_file` son absolutos y no portables.
- textual_fidelity_certified = false; fidelidad textual NO certificada.
- legal_compliance_assessed = false; cumplimiento jurídico NO evaluado.
- format_mapping_completed = false; mapping NO completado.
- audit_rules_created = false; reglas de auditoría NO creadas.
- phase_3_started = false; Phase 3 NOT STARTED.
- Replay controlado con decisiones humanas; Gate 1/2 no tienen generador independiente.

Registros formales: `03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.md`
y `PHASE_2_FORMAL_FREEZE.json`. El FAIL anterior se conserva como
PRECONDITION_INPUT_ERROR / INCORRECT_EXPECTED_GTFS_SHA_IN_INSTRUCTION.

## Interoperability

Los directorios `GTFS_to_NeTEx`, `GTFS-RT_to_SIRI` y `Mapping` existen y están vacíos. No se observó implementación. Las futuras clasificaciones deben distinguir `AVAILABLE`, `MAPPABLE`, `PARTIAL`, `MISSING`, `UNKNOWN` y `NOT_APPLICABLE`, sin inventar información.

## Audits

Los directorios padre existen y están vacíos. El trabajo de 20 operadores está actualmente dentro de `02_Data_Engineering/GTFS_Lab/20_clientes_reales`, no en `05_Audits`.

## Products

`06_Products/GTFS Explorer` contiene cuatro repositorios Git detectados. Desktop, Engineering y Artifacts tienen cambios locales; la copia restore está limpia y detached. No se modificó ninguno.

## Git / repository health

- La raíz es Git. `.gitignore` excluye bases DuckDB, feeds raw/extracted, temporales y repositorios producto anidados; documentos, código, SQL, reports, manifests y PDFs jurídicos siguen siendo elegibles para versionado.
- El `.gitignore` raíz aplica a GTFS_Lab y Compliance; no se añadieron reglas que oculten SQL, PowerShell, Markdown, JSON, manifests, reports pequeños o PDFs jurídicos.
- El único `.gitignore` observado fuera de Products está en `20_clientes_reales` y solo cubre cachés y temporales.
- Las referencias históricas de procedencia en documentación y evidencia conservan las rutas originales intencionadamente. Los scripts ejecutables de evidencia afectados resuelven Desktop y Engineering desde `$PSScriptRoot`.
- Algunos subdirectorios temporales de Artifacts devuelven acceso denegado; no se alteraron permisos.

## Known technical debt

- El repositorio padre no tiene commits ni remote; sus cuatro repositorios producto se gestionan de forma independiente.
- Faltan las capas GTFS core, validation y analysis descritas conceptualmente.
- Falta documentación operativa del GTFS_Lab.
- Faltan fuentes reproducibles del GIS/KML.
- Existen rutas absolutas y referencias pre-migración no portables.
- `06_Products` mezcla repositorios, backups y gran volumen de artefactos bajo el mismo árbol padre.

## Open anomalies

- Annex 1.3 B-I/D-I: visible, no corregida.
- `main.stops`: duplicado exacto de `raw.stops`, propósito desconocido.
- Dos ZIP de exportación Bizkaibus y sus manifests son duplicados byte a byte entre `run_001` y `run_002_rc002`; pueden ser evidencia intencionada.
- GTFS Explorer Desktop tiene 20 entradas de estado; Engineering 1; Artifacts 4.

## Current frozen baselines

- GTFS raw: los siete conteos indicados en este documento.
- Compliance Phase 1: FROZEN; baseline histórico preservado, 10 fuentes con hash válido, 6 relaciones y 92 provisions.
- Compliance Phase 2: FROZEN; 48 requisitos, 36 source facts, 10 deadlines y 7 dependencias PARTIAL.
- Estas bases permanecieron byte a byte sin cambios durante la auditoría.

## Next planned phase

READY_FOR_PHASE_3_PLANNING = YES. Phase 3 NOT STARTED.
Phase 2 está formalmente congelada. Solo se habilita planificación futura;
no se crean mappings, reglas ni decisiones jurídicas en esta promoción.

---

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Repository governance

- Repositorio Git raíz creado en Transit Data Lab, sin commit ni remote.
- Los repositorios Git anidados Desktop, Engineering, Artifacts y restore test se conservan independientes. El `.gitignore` del padre los excluye para evitar absorber su contenido o registrar gitlinks accidentalmente.
- DuckDB (`*.duckdb`, WAL) y feeds raw/extracted quedan locales y fuera del control normal de versiones; SQL de importación, scripts, tests y baselines sí se conservan.
- Los 12 PDF jurídicos (40.436.167 bytes) se conservan en el corpus con sus SHA-256 y no se ignoran. Su retención es necesaria para reproducir y verificar las fuentes; se versionarán en el repositorio padre.
- Los valores `source.documents.local_file` absolutos de la base existente permanecen intactos para proteger su hash. El SQL fuente y los scripts ya usan rutas portables.

