# Evidence index

Fecha de revisión: 2026-09-27. 28 evidencias, con 76 rutas exactas únicas. Todas las rutas son relativas a la raíz Transit Data Lab; los enlaces parten de este documento. Los conjuntos de pruebas se agrupan bajo un Evidence ID sin ocultar sus rutas individuales. SHA-256 calculados sobre los archivos actuales durante esta revisión. No se copian artefactos técnicos a Business.

## Verificación observada en esta fase

- Bases GTFS/Compliance: SHA-256 coincide con baselines activos, sin mutación.
- ZIP Asturias: 7/7 entradas coinciden con los TXT en `02_Data_Engineering/GTFS_Lab/feeds/extracted/20260924_020003_Consorcio_Asturias/` (agency.txt, calendar_dates.txt, routes.txt, shapes.txt, stops.txt, stop_times.txt, trips.txt).
- Sentinel GTFS ejecutado con DuckDB `-no-init -batch -bail -readonly -json`: exit 0; 46 checks, 42 PASS y cuatro FAIL (analysis, core, validation y validation.results ausentes). El resultado global conserva WARNING. No se ha ejecutado importación.
- Compliance: consultas read-only de catálogo y conteos confirman 48 requirements, 36 facts, 10 deadlines; mapping.format_coverage, mapping.format_equivalences, audit.rules, audit.runs y audit.results tienen cero filas.
- Diez fuentes de EVD-012 recomprobadas por SHA-256: 10/10 coincidencias. No se revisa su interpretación jurídica ni vigencia por Internet.
- EVD-015: lectura completa de resultados JSON (múltiples arrays de DuckDB), clasificación por filas con `test`/`status`, diez exit codes guardados iguales a 0 y diez hashes SQL coincidentes. Invariantes 22/22, estructura 22/22, anexos 63/63, gate posterior 387/387 PASS. Son resultados persistidos de la congelación; no nuevos resultados de rerun en esta fase.
- Dos manifiestos Kbus recomprobados: hash HTML `d67c57a206e0d052bdbd78cdd3bde1a1eacd41681f3547bb6341253ef46e7d5f`; hash JSON `8de77f94cac49559d070dd06211afc7ce75a63adf69a9aa6de2d19d1a9608048`, ambos coincidentes.
- Los scripts de importación, piloto, materialización y congelación no se ejecutaron. No se hicieron pruebas de escritura ni correcciones técnicas.

Los controles de esta fase devuelven resultados en memoria/terminal; este índice registra método, resultados y hashes. La evidencia técnica histórica continúa en sus ubicaciones originales. El registro no convierte una verificación Business en una nueva congelación técnica.

## Índice

<a id="tdl-evd-001"></a>

### TDL-EVD-001 — Baseline del contenedor

- **Evidence ID:** TDL-EVD-001.
- **Tipo de artefacto:** Baseline JSON / estado técnico.
- **Componente:** Transversal.
- **Capability IDs relacionados:** TDL-CAP-001, TDL-CAP-002, TDL-CAP-005, TDL-CAP-006, TDL-CAP-007, TDL-CAP-008.
- **Qué acredita:** Conteos y separación de componentes; identifica baselines activos.
- **Limitaciones conocidas:** Documento no equivale a ejecución; los conteos físicos de archivos son anteriores y no se usan como inventario actual.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [project_baseline.json](../../project_baseline.json) | `541b19b2d4b47d9639a346df9531ec163e92c96f2a5f56d7413a07620ffb0da3` |
| [PROJECT_CURRENT_STATE.md](../../PROJECT_CURRENT_STATE.md) | `1926a19ab7a779fcb4bdb256499a2e703696f92460c458b4f757bc9668141871` |

<a id="tdl-evd-002"></a>

### TDL-EVD-002 — Base raw GTFS

- **Evidence ID:** TDL-EVD-002.
- **Tipo de artefacto:** DuckDB.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-001, TDL-CAP-002, TDL-CAP-003, TDL-CAP-004.
- **Qué acredita:** Siete tablas raw consultables y main.stops; hash vigente coincide.
- **Limitaciones conocidas:** Un único feed; raw VARCHAR; sin core/analysis/validation.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb](../../02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb) | `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc` |

<a id="tdl-evd-003"></a>

### TDL-EVD-003 — Fuente Asturias

- **Evidence ID:** TDL-EVD-003.
- **Tipo de artefacto:** ZIP GTFS.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-001, TDL-CAP-002.
- **Qué acredita:** Fuente conservada; siete entradas iguales por SHA-256 a su extracción.
- **Limitaciones conocidas:** No acredita calidad de otros feeds ni derechos de explotación.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/feeds/raw/20260924_020003_Consorcio_Asturias.zip](../../02_Data_Engineering/GTFS_Lab/feeds/raw/20260924_020003_Consorcio_Asturias.zip) | `f3093ab85d728ee824ba45cd3f247d1d9ea68a4685aaf25b27a8de98ea50b549` |

<a id="tdl-evd-004"></a>

### TDL-EVD-004 — Importación SQL

- **Evidence ID:** TDL-EVD-004.
- **Tipo de artefacto:** SQL.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-001.
- **Qué acredita:** Transacción e importación de siete TXT con all_varchar=true.
- **Limitaciones conocidas:** CREATE OR REPLACE; no ejecutado en esta fase; no prueba extracción automatizada.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/sql/01_import/20260924_020003_import_consorcio_asturias.sql](../../02_Data_Engineering/GTFS_Lab/sql/01_import/20260924_020003_import_consorcio_asturias.sql) | `91cc3dfe7145426db892cccb115abcb0622f5f5b318cc62b015ddef0fc938c62` |

<a id="tdl-evd-005"></a>

### TDL-EVD-005 — Runner de importación

- **Evidence ID:** TDL-EVD-005.
- **Tipo de artefacto:** PowerShell.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-001.
- **Qué acredita:** Resuelve directorio y propaga fallo de DuckDB.
- **Limitaciones conocidas:** Sintaxis validada históricamente; replay de importación no observado.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/sql/01_import/run_import_consorcio_asturias.ps1](../../02_Data_Engineering/GTFS_Lab/sql/01_import/run_import_consorcio_asturias.ps1) | `894240131b36a056c7b656d1570c22058e591386d8d50f35709359aa0ad3ba50` |

<a id="tdl-evd-006"></a>

### TDL-EVD-006 — Sentinel GTFS

- **Evidence ID:** TDL-EVD-006.
- **Tipo de artefacto:** SQL read-only.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-003, TDL-CAP-004, TDL-CAP-006, TDL-CAP-007, TDL-CAP-008.
- **Qué acredita:** Controles de conteos, relaciones, claves, referencias, secuencias y conservación temporal.
- **Limitaciones conocidas:** Baseline específico; cuatro FAIL de capas ausentes; no validador general.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/sql/07_tests/test_gtfs_lab_integrity.sql](../../02_Data_Engineering/GTFS_Lab/sql/07_tests/test_gtfs_lab_integrity.sql) | `8faee3ad03c65d6858104e2e1da20da5dce3b1e780de568f6efa44f86447def0` |

<a id="tdl-evd-007"></a>

### TDL-EVD-007 — Resultados GTFS conservados

- **Evidence ID:** TDL-EVD-007.
- **Tipo de artefacto:** Salida de pruebas.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-003, TDL-CAP-004.
- **Qué acredita:** Ejecución histórica del sentinel; 201 filas >=24h y ruta 440.
- **Limitaciones conocidas:** No hay exit_code separado; no se usa como único respaldo de PASS.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [reports/repository_integrity/phase_1_5/gtfs_integrity.txt](../../reports/repository_integrity/phase_1_5/gtfs_integrity.txt) | `1abce89bed94996a01c788ffefb616c3fbd89b1c7d276ef5e3fab1771df656d8` |

<a id="tdl-evd-008"></a>

### TDL-EVD-008 — Informe de integridad GTFS

- **Evidence ID:** TDL-EVD-008.
- **Tipo de artefacto:** Informes.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-001, TDL-CAP-002, TDL-CAP-003, TDL-CAP-004, TDL-CAP-005, TDL-CAP-006, TDL-CAP-007, TDL-CAP-008.
- **Qué acredita:** Baseline WARNING, capas ausentes y runner no replayado.
- **Limitaciones conocidas:** Auditorías históricas; no permiten inferir capacidad completa.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [reports/repository_integrity/GTFS_INTEGRITY_REPORT.md](../../reports/repository_integrity/GTFS_INTEGRITY_REPORT.md) | `cecedd15aacecf0ea946bf37f6d109bf277594a5ad7faeaceb660d204fa07b6a` |
| [reports/repository_integrity/PHASE_1_5_STABILIZATION_REPORT.md](../../reports/repository_integrity/PHASE_1_5_STABILIZATION_REPORT.md) | `52b159cbc374f3e3f72e3f8f0906b48b85a7230d69b50aa885e2584d701159eb` |

<a id="tdl-evd-009"></a>

### TDL-EVD-009 — Exports GIS

- **Evidence ID:** TDL-EVD-009.
- **Tipo de artefacto:** KML.
- **Componente:** GTFS_Lab.
- **Capability IDs relacionados:** TDL-CAP-005.
- **Qué acredita:** Tres geometrías almacenadas de ruta 440, 814 puntos entre los dos sentidos.
- **Limitaciones conocidas:** Sin SQL/script de regeneración ni pipeline GIS observado.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/exports/route_440.kml](../../02_Data_Engineering/GTFS_Lab/exports/route_440.kml) | `ec4910135abcb79b2f80e9fe77e3d8fa3afec0488207abee16d654ad75a9b2d6` |
| [02_Data_Engineering/GTFS_Lab/exports/route_440_dir0.kml](../../02_Data_Engineering/GTFS_Lab/exports/route_440_dir0.kml) | `fdd2d0c5398db95f39aa53a742e5338a369ec387a320e53e17ffa3794a2c1e65` |
| [02_Data_Engineering/GTFS_Lab/exports/route_440_dir1.kml](../../02_Data_Engineering/GTFS_Lab/exports/route_440_dir1.kml) | `d8078684945cab253a3f65d0b7c5268477b9db2cb8087224c4629f2b4c5c92ad` |

<a id="tdl-evd-010"></a>

### TDL-EVD-010 — Base Compliance

- **Evidence ID:** TDL-EVD-010.
- **Tipo de artefacto:** DuckDB.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-009, TDL-CAP-010, TDL-CAP-012, TDL-CAP-014, TDL-CAP-015.
- **Qué acredita:** Infraestructura persistida, 48 requirements, 36 facts y 10 deadlines.
- **Limitaciones conocidas:** mapping y audit vacíos; no evaluación de cumplimiento.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/databases/transit_compliance.duckdb](../../03_Compliance/databases/transit_compliance.duckdb) | `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3` |

<a id="tdl-evd-011"></a>

### TDL-EVD-011 — Congelación formal

- **Evidence ID:** TDL-EVD-011.
- **Tipo de artefacto:** Baseline congelada.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-009, TDL-CAP-010, TDL-CAP-011, TDL-CAP-012, TDL-CAP-014, TDL-CAP-015.
- **Qué acredita:** Phase 2 FROZEN, fuente 2024-03-04, hash activo y límites expresos.
- **Limitaciones conocidas:** Phase 1 hash es histórico; no es el hash exigible a la base acumulativa actual.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json](../../03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.json) | `117837aacfba3f136f5c0cd171d7e1dd00c34e3cdf531eee43e0b202cdf80a05` |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.md](../../03_Compliance/reports/phase_2/freeze/PHASE_2_FORMAL_FREEZE.md) | `d15a91ba1099305e67a8479ec7ef87b23d541775ce2e6ccc7120758dadb5b7b3` |

<a id="tdl-evd-012"></a>

### TDL-EVD-012 — Hash de fuentes

- **Evidence ID:** TDL-EVD-012.
- **Tipo de artefacto:** Manifiesto de fuentes.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-009.
- **Qué acredita:** Diez documentos locales con SHA-256 esperado y actual; se recomprobaron 10/10.
- **Limitaciones conocidas:** Integridad binaria no acredita fidelidad del texto normalizado ni vigencia jurídica.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/LEGAL_SOURCE_HASH_CHECKS.csv](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/LEGAL_SOURCE_HASH_CHECKS.csv) | `324b1801107dd5313f8b66ce83305f368f2048d3d3ab0c0fb0ee7c2732273908` |

<a id="tdl-evd-013"></a>

### TDL-EVD-013 — Universo materializado

- **Evidence ID:** TDL-EVD-013.
- **Tipo de artefacto:** Snapshots CSV.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-010.
- **Qué acredita:** Contenido congelado de 48 requisitos, 36 facts y 10 deadlines.
- **Limitaciones conocidas:** Siete dependencias PARTIAL y dos anomalías preservadas.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_REQUIREMENTS.csv](../../03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_REQUIREMENTS.csv) | `f46f98339ebe4c6194be23b5a9800346df659c6a9df68c0a101a0b07e46fee72` |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_SOURCE_FACTS.csv](../../03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_SOURCE_FACTS.csv) | `5f82d4153adf5b1139d4e9abc182904cfd3e7775027d2b837878d6dc6a204907` |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_DEADLINES.csv](../../03_Compliance/reports/phase_2/freeze/PHASE_2_FINAL_DEADLINES.csv) | `fd90dd1fbcdc6b80b086c58e4a4b630176ac9c308f936ea0c8a9da26284fc11b` |

<a id="tdl-evd-014"></a>

### TDL-EVD-014 — Materialización

- **Evidence ID:** TDL-EVD-014.
- **Tipo de artefacto:** Informe / Python.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-010, TDL-CAP-013.
- **Qué acredita:** Delta histórico 3→48 requisitos, 1→10 deadlines, guardas y transacción.
- **Limitaciones conocidas:** No ejecutar en la base activa; exige estado histórico e inputs aprobados.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/materialization/PHASE_2_REQUIREMENTS_MATERIALIZATION.md](../../03_Compliance/reports/phase_2/materialization/PHASE_2_REQUIREMENTS_MATERIALIZATION.md) | `54c5a374ba735490b8adabbb71e3aef7812e0ff21b40ad987a3fe2909605f016` |
| [03_Compliance/reports/phase_2/materialization/materialize_requirements.py](../../03_Compliance/reports/phase_2/materialization/materialize_requirements.py) | `418b49b3123a071138687416f87ae7b149d45abc59c0d6294e7c1694e929ff06` |

<a id="tdl-evd-015"></a>

### TDL-EVD-015 — Gates finales

- **Evidence ID:** TDL-EVD-015.
- **Tipo de artefacto:** Resultados completos / exit codes / SQL.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-009, TDL-CAP-010, TDL-CAP-012.
- **Qué acredita:** 22+22+63+387 comprobaciones PASS; diez exit codes 0 y diez hashes SQL coincidentes.
- **Limitaciones conocidas:** Resultados del baseline activo persistidos; no rerun de todos los gates en esta fase.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/FINAL_TEST_RESULTS.csv](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/FINAL_TEST_RESULTS.csv) | `65e878da5a99b0d325a0b66fb71f054956419863101960707c4ce9c041a281f7` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_1_invariants.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_1_invariants.json) | `28a8671fae7d5ee04160c935e34895c635e719c9d8f5bf6f43c3d6d6c1b835c6` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_1_invariants.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_1_invariants.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/phase_1/test_phase_1_invariants.sql](../../03_Compliance/sql/07_tests/phase_1/test_phase_1_invariants.sql) | `b2a89c0d14842bc2ff5f7d5b561b60a7d3d76269004c1b71e10ffc5e7300332a` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_master_structure.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_master_structure.json) | `bc796cce428bf722e6670a1528f7d4d7cf767b852e1f967cb5903925e6acfab7` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_master_structure.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_master_structure.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_master_structure.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_master_structure.sql) | `db2b5366319769e3a739e7629d8e04f7f79afd0528d02374a1e9933f455e194b` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_1.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_1.json) | `0e2cce8c5060c202ced50976d4d45103a987df00e2e4e411b2ed8a25d76170e3` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_1.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_1.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_1.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_1.sql) | `93f4715baefbe8c9cdc158a01bcbdd20fe93bbcb3f0512741126d0d11244b5d0` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_2.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_2.json) | `b9d2731721fa01cf08c82d1c06d1e9d211806c91e341af74b579b934240fed89` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_2.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_2.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_2.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_2.sql) | `f2265f6bbc4fb2df1e829eaa98464197a1a2130fa95b213aa2441c983d437d69` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_3.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_3.json) | `6976688459780905208ab896ed8cc4a90ff4f485169e1c34571aea3dc4929370` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_3.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_3.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_3.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_3.sql) | `196a32123a84ef5d79fd366c68b5c1e5f14ba60b90f26a9cc3ef1c437844af1c` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_4.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_4.json) | `e50b4bd78a26f35b181e97b9a05cf5256c7d7105a3d8890b005b19b88a073ba4` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_4.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_1_4.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_4.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_1_4.sql) | `6d89324b08f93db8c8881f82711216ca80a96d7d627d091501fade308b9daf39` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_1.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_1.json) | `c06e25122855e077b4396ba6686e504c82b7af3e493508ceacf8c00545c50049` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_1.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_1.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_1.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_1.sql) | `da3f0f3f110e9d55b3c3cc159c5558ec579c556e3230d64fdd5421e1ebc0c5b6` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_2.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_2.json) | `5562a146a804e38e740d1ff59c35d135ced94caa836ac4efec65bf8d634fce8c` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_2.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_2.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_2.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_2.sql) | `b3656f2539549c5bd178ed8e58b35a01d6ed275469072db52309789191187a6a` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_3.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_3.json) | `39d608920a18a280a46fbff0b1ad36099cbee7fe19da8702ce90e969fd4d8f60` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_3.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_eu_2017_1926_annex_2_3.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_3.sql](../../03_Compliance/sql/07_tests/source/test_eu_2017_1926_annex_2_3.sql) | `778afdf1ec09cbfb5f4ad99eebef2f451dc67b2d5f9cdee9e60f5c530ac779da` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_2_post_materialization_gate.json](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_2_post_materialization_gate.json) | `a556697bf92c4e8f4462c1bf8be7b4a1a54bb8fe22749e8484bc627bd19c80a6` |
| [03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_2_post_materialization_gate.exit_code.txt](../../03_Compliance/reports/phase_2/freeze/promotion_resume/run_001/test_phase_2_post_materialization_gate.exit_code.txt) | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| [03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql](../../03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql) | `974a972340fe8949d69f90f01bb7835265671d4e3ce8fb69c80daf8cb7d3cba8` |

<a id="tdl-evd-016"></a>

### TDL-EVD-016 — Matriz de reproducibilidad

- **Evidence ID:** TDL-EVD-016.
- **Tipo de artefacto:** Matriz CSV.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-011, TDL-CAP-013.
- **Qué acredita:** Distingue replay controlado, revisión humana, scripts y estado histórico.
- **Limitaciones conocidas:** execution_performed=NO en revisión; no replay integral independiente.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/freeze/PHASE_2_REPRODUCIBILITY_MATRIX.csv](../../03_Compliance/reports/phase_2/freeze/PHASE_2_REPRODUCIBILITY_MATRIX.csv) | `05f1c26b7fe2d408fb482a146c5e62d943fa1915c00a7bfe8cae08f358955e61` |

<a id="tdl-evd-017"></a>

### TDL-EVD-017 — Política histórica de tests

- **Evidence ID:** TDL-EVD-017.
- **Tipo de artefacto:** Política técnica.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-009, TDL-CAP-012, TDL-CAP-013.
- **Qué acredita:** Distingue invariantes de condiciones mutables de Phase 1/pre-materialización.
- **Limitaciones conocidas:** No interpretar EXPECTED_HISTORICAL_STATE_MISMATCH como fallo del baseline activo.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/TEST_BASELINE_POLICY.md](../../03_Compliance/TEST_BASELINE_POLICY.md) | `fd26a072aa184187bdbfa27b5a3b0157298e595f7ec525efa8d2a2a15f323db5` |

<a id="tdl-evd-018"></a>

### TDL-EVD-018 — Gate 1 humano

- **Evidence ID:** TDL-EVD-018.
- **Tipo de artefacto:** Decisiones / conciliación.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-010, TDL-CAP-011, TDL-CAP-013.
- **Qué acredita:** Revisión documentada de candidatos y soporte de fuente.
- **Limitaciones conocidas:** Decisiones humanas, no extracción jurídica autónoma.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/review/gate_1/HUMAN_DECISION_MATRIX_V1.csv](../../03_Compliance/reports/phase_2/review/gate_1/HUMAN_DECISION_MATRIX_V1.csv) | `59fb133a0c2803feb9c7832c97f8f15985eedc7e57b74f6712b38a52272a54c9` |
| [03_Compliance/reports/phase_2/review/gate_1/GATE_1_RECONCILIATION.md](../../03_Compliance/reports/phase_2/review/gate_1/GATE_1_RECONCILIATION.md) | `31aeb68e3f77d182c3ae2b144850721318f156ca313baaa599d467940b7e3d8a` |

<a id="tdl-evd-019"></a>

### TDL-EVD-019 — Gate 2 humano

- **Evidence ID:** TDL-EVD-019.
- **Tipo de artefacto:** Universo aprobado / resolución.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-010, TDL-CAP-011, TDL-CAP-013.
- **Qué acredita:** Universo final revisado y excepciones documentadas antes de materialización.
- **Limitaciones conocidas:** No genera mappings, reglas ni una conclusión de cumplimiento.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv](../../03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_FINAL_ATOMIC_UNIVERSE.csv) | `4f7c0a3342a91c148a56c6f73c50a384501f1baff5b61e278e322193624906c5` |
| [03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_EXCEPTION_RESOLUTION.md](../../03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_EXCEPTION_RESOLUTION.md) | `1137de90d01ffb6aab7efa4bdc1cc53a36e1452665dc42846b6af1f38633da95` |

<a id="tdl-evd-020"></a>

### TDL-EVD-020 — Infraestructura mapping/audit

- **Evidence ID:** TDL-EVD-020.
- **Tipo de artefacto:** DDL.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-014, TDL-CAP-015.
- **Qué acredita:** Definiciones de tablas mapping y audit que existen en la base.
- **Limitaciones conocidas:** DDL no es motor operativo; 0 mappings, reglas, runs y resultados.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/sql/00_setup/001_create_compliance_database.sql](../../03_Compliance/sql/00_setup/001_create_compliance_database.sql) | `74cc1273b58ac8560dec4c01a13ad1a873de2cfddcd78b0bae66e41cd50b7061` |

<a id="tdl-evd-021"></a>

### TDL-EVD-021 — Inventario de operadores

- **Evidence ID:** TDL-EVD-021.
- **Tipo de artefacto:** Inventario / alcance.
- **Componente:** GTFS_Lab / benchmark.
- **Capability IDs relacionados:** TDL-CAP-016.
- **Qué acredita:** Veinte entradas de investigación y separación de datos originales.
- **Limitaciones conocidas:** No son veinte clientes comerciales; no prueba auditoría de veinte operadores.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/benchmark_manifest.csv](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/benchmark_manifest.csv) | `293caa25d298e802fd9a759cf22ca1e8f89d6711e68a5a001724a3222153fe3d` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/README.md](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/README.md) | `ba404f7307cd83eeb6abedb1c49c7bbf8afc235464a9fa28ac770b873fc42920` |

<a id="tdl-evd-022"></a>

### TDL-EVD-022 — Censo piloto

- **Evidence ID:** TDL-EVD-022.
- **Tipo de artefacto:** Censo JSON / informe.
- **Componente:** GTFS_Lab / piloto.
- **Capability IDs relacionados:** TDL-CAP-016, TDL-CAP-019.
- **Qué acredita:** Cinco datasets: archivos, filas, campos y hashes físicos.
- **Limitaciones conocidas:** No valida semántica; censo histórico, no adquisición automatizada.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/source_census.json](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/source_census.json) | `0741520fbac7d03b79c246d4d36545d14204d68d8c7e2ebc1aa836cae7a4fbfa` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/source_census.md](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/source_census.md) | `581c4a536db456708939504957e7d7ec48b43851075ae2dc7f7a24c295665907` |

<a id="tdl-evd-023"></a>

### TDL-EVD-023 — Herramientas de piloto

- **Evidence ID:** TDL-EVD-023.
- **Tipo de artefacto:** Python.
- **Componente:** GTFS_Lab / piloto.
- **Capability IDs relacionados:** TDL-CAP-016, TDL-CAP-019.
- **Qué acredita:** Implementación de censo, parsing de informes y comparación.
- **Limitaciones conocidas:** Escriben fuera de Business; no ejecutadas ni importadas en esta fase.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/tools/generate_pilot_01.py](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/tools/generate_pilot_01.py) | `6cbb5333048449897aa05a6e66c4c824d6ef03e049460109bed321adcf579622` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/tools/audit_gtfs_explorer_pilot_01.py](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/tools/audit_gtfs_explorer_pilot_01.py) | `bc0d37279a52fcdbc133ec6cf79d703a9684bcf62f3ba0c3d46a85532c2889ab` |

<a id="tdl-evd-024"></a>

### TDL-EVD-024 — Comparación piloto

- **Evidence ID:** TDL-EVD-024.
- **Tipo de artefacto:** Comparación / informes.
- **Componente:** GTFS_Lab / piloto.
- **Capability IDs relacionados:** TDL-CAP-017, TDL-CAP-018, TDL-CAP-019, TDL-CAP-020.
- **Qué acredita:** Comparación de agregados NAP con detalle GTE, separa poblaciones y desconocidos.
- **Limitaciones conocidas:** Narrativa histórica Bizkaibus superada por EVD-027; ninguna equivalencia de reglas probada.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/differential_matrix.csv](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/differential_matrix.csv) | `dbb73f5e17baa786dcde2e3770d8d4518fcb681a921d22daa5e68eedfbbe0d35` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/final_report.md](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/final_report.md) | `aafdff8b3bd05af407c0edc4949f83afd7df00c546bd5059797216e723eff49a` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/docs/PILOT_01_EVIDENCE_MODEL_OBSERVATIONS.md](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/docs/PILOT_01_EVIDENCE_MODEL_OBSERVATIONS.md) | `c560ca7babcec0c36684242be521880ef7727bae9df6a6cea99bddeba4d917e8` |

<a id="tdl-evd-025"></a>

### TDL-EVD-025 — Informe GTE Kbus

- **Evidence ID:** TDL-EVD-025.
- **Tipo de artefacto:** HTML / manifiesto.
- **Componente:** GTFS Explorer (evidencia recibida en Lab).
- **Capability IDs relacionados:** TDL-CAP-017, TDL-CAP-018.
- **Qué acredita:** Reporte conservado de ejecución 0.2.1; hash recomprobado coincide.
- **Limitaciones conocidas:** No acredita runtime vigente, build canónica ni cobertura universal.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/informe-validacion.html](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/informe-validacion.html) | `d67c57a206e0d052bdbd78cdd3bde1a1eacd41681f3547bb6341253ef46e7d5f` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/informe-validacion.html.manifest.json](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/informe-validacion.html.manifest.json) | `22c15f172042235bd792af66b3b15a5298e2edf403fff2a554b0cc1d07a78197` |

<a id="tdl-evd-026"></a>

### TDL-EVD-026 — Export JSON Kbus

- **Evidence ID:** TDL-EVD-026.
- **Tipo de artefacto:** JSON / manifiesto.
- **Componente:** GTFS Explorer (evidencia recibida en Lab).
- **Capability IDs relacionados:** TDL-CAP-018.
- **Qué acredita:** Export de datos de rutas y servicios almacenado; hash coincide.
- **Limitaciones conocidas:** No export de evidencias de auditoría; no replay de export ni round-trip. Selección AH/H/L2/L3, pero routes contiene AH/H/L2; no acredita completitud ni L3.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/gtfs-export-route-AH-H-L2-L3-service-1-2-json.json](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/gtfs-export-route-AH-H-L2-L3-service-1-2-json.json) | `8de77f94cac49559d070dd06211afc7ce75a63adf69a9aa6de2d19d1a9608048` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/gtfs-export-route-AH-H-L2-L3-service-1-2-json.json.manifest.json](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/020_kbus/03_gtfs_explorer/run_001/gtfs-export-route-AH-H-L2-L3-service-1-2-json.json.manifest.json) | `42245ad3f7ec9328e260775b11bffe26f41c042f414080f8b065a801b91af848` |

<a id="tdl-evd-027"></a>

### TDL-EVD-027 — Procedencia Bizkaibus

- **Evidence ID:** TDL-EVD-027.
- **Tipo de artefacto:** Registro de aceptación / proyecto.
- **Componente:** GTFS Explorer (evidencia recibida en Lab).
- **Capability IDs relacionados:** TDL-CAP-017, TDL-CAP-019.
- **Qué acredita:** Declara run_004 aceptado y hallazgos enum históricos invalidados.
- **Limitaciones conocidas:** Forense y ejecutable citados fuera del read scope no inspeccionados; no confirmar build vigente.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/README.md](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/README.md) | `894e561f8aca810b1798b8247b2659c7a4395ea968ba0e31c80a3ca88c1d913f` |
| [02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_004_gtfs023_candidate001/project.json](../../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_004_gtfs023_candidate001/project.json) | `8e3440b1691e13605c1e27d54d00bc235eea7f7a3404289b08c2d51604702c65` |

<a id="tdl-evd-028"></a>

### TDL-EVD-028 — Diseño de requirements

- **Evidence ID:** TDL-EVD-028.
- **Tipo de artefacto:** Documento técnico.
- **Componente:** Compliance.
- **Capability IDs relacionados:** TDL-CAP-010, TDL-CAP-014, TDL-CAP-015.
- **Qué acredita:** Alcance extracción 2017/1926 y pipeline iniciado; no mappings ni auditoría.
- **Limitaciones conocidas:** Describe estado inicial del seed; estado final lo determina congelación EVD-011.

| Ruta exacta | SHA-256 observado |
| --- | --- |
| [03_Compliance/PHASE_2_REQUIREMENTS_ENGINE.md](../../03_Compliance/PHASE_2_REQUIREMENTS_ENGINE.md) | `79f6c49991bd216786464d48bb8cbd6662d118cdb14b826c736f62c3b3658a73` |

## Resolución de contradicciones y evidencia insuficiente

EVD-011 y la base activa prevalecen sobre documentación de extracción inicial (EVD-028) o informes anteriores que todavía indicaban Phase 2 abierta. No se reescriben estos históricos. EVD-027 prevalece sobre la narrativa antigua Bizkaibus de EVD-024: run_002_rc002 no tiene procedencia canónica aceptada; run_004 figura aceptado y sus resultados anteriores enum están invalidados. La revisión Business no inspecciona ejecutable/UserAssist externos al alcance y por ello no confirma independientemente la build vigente.

La baseline técnica no está fijada mediante commit del repositorio padre: Git está sin commits y las bases/feeds están ignorados. La congelación de Compliance es documental y por hash; no se transforma en una release reproducible del contenedor. Las rutas absolutas en evidencia histórica se conservan como procedencia, sin corregirlas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Verificación final de alcance

Comparación antes/después de 2026-09-27: 899 archivos fuera de Business en las áreas autorizadas, incluidos archivos ignorados por Git. Inventario ordenado por ruta, SHA-256 de cada archivo y SHA-256 agregado de la concatenación `ruta + espacio + hash + salto de línea` codificada UTF-8. Rutas y bytes sin cambios; no altas/bajas detectadas en esos inventarios. No se inspecciona ni se opera sobre 06_Products.

| Área / archivo | Archivos | SHA-256 agregado antes = después |
| --- | ---: | --- |
| 02_Data_Engineering | 451 | `bd32f9660aa4954c84b9d298f83eef50dd49868bd2e2da9e57c91c39ab07277a` |
| 03_Compliance | 436 | `25cafcbd5403fb7fd8cb1e8ed8059d65435a8c42a02d7a3d5b1201fe0bd80333` |
| reports | 9 | `675e7345e507dd2e51b4a7f0d8911f0db9486301d9cee8e7cd40b1521b9e86d1` |
| PROJECT_CURRENT_STATE.md | 1 | `714bc8eae1880be7d51479e5953eb729d8d4cd4512a08cf086c03bb690b4f742` |
| project_baseline.json | 1 | `bd20ad89c667f5a82f1c271bd083651e8bc9da283ec7994925ffafcbd160895b` |
| .gitignore | 1 | `597010ff7d204714660b1b745bc854a98e36fe19d4bc7c955e6e2ec28ef65a31` |

Ejecutados `git status --short`, `git diff --stat`, `git diff --check` y `git diff -- 07_Business`: exit 0; diff vacío porque el repositorio padre no tiene commits y sus archivos son untracked. Git por sí solo no prueba ausencia de cambios en estos archivos; se complementa con los inventarios anteriores. Escrituras de esta tarea: exclusivamente CAPABILITY_REGISTER, EVIDENCE_INDEX, CAPABILITY_GAPS, BUSINESS_STATUS y DECISION_LOG dentro de 07_Business. No staging, commit ni Phase 3.

## Revisión final para BUSINESS_CAPABILITY_BASELINE_V1

2026-09-27: 28 Evidence IDs y 76 rutas únicas recomprobadas, 76/76 disponibles y SHA-256 concordantes. Correspondencia capability → Evidence ID → capability confirmada para las 20 capacidades. Los enlaces registrados no están rotos. La clasificación individual de los 28 conjuntos como declarativos, ejecutables o resultados persistidos figura en [BASELINE_REVIEW_V1.md](BASELINE_REVIEW_V1.md). Estos documentos y las salidas Business de review_v1 son registros de revisión, no Evidence IDs técnicos adicionales: el índice mantiene 28/76.

Controles de cierre: [review_v1/checks.json](review_v1/checks.json), [review_v1/final_summary.json](review_v1/final_summary.json), consultas y salidas completas con exit codes en review_v1. Se conservó el FAIL inicial de cinco comparaciones case-sensitive de hashes del censo: eran hexadecimales en mayúsculas frente a minúsculas, sin diferencia binaria. La normalización y los cinco hashes actuales están documentados en final_summary.json; no se alteró el censo ni se ocultó el resultado inicial del comparador.

Sentinel actual read-only persistido: 42 PASS / 4 FAIL, exit 0, global WARNING. Ausencias: analysis, core, validation y validation.results. Esto no constituye un validador GTFS completo. Diez suites Compliance contrastadas desde resultados completos, exit codes y hashes SQL; sin rerun. Bases, 7/7 pares Asturias, 10/10 fuentes jurídicas, cinco ZIP del censo y dos manifiestos Kbus concordantes. Inventarios antes/después de 899 archivos técnicos iguales; no se realizaron escrituras fuera de Business. Las referencias absolutas históricas declaradas no implican portabilidad; documentos superados no se usan como fuente del estado activo.

El índice queda integrado en V1: nuevas evidencias técnicas requieren revisión Business, no actualización automática ni modificación silenciosa de esta huella.
