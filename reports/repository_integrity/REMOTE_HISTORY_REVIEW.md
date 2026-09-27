# Transit Data Lab — revisión del historial remoto

Fecha: 2026-09-27. Inspección de objetos y metadatos Git; sin checkout ni lectura de blobs, datasets o bases.

## Resultado

REMOTE_HISTORY_REVIEW = PASS

- origin/main y main remoto observado al inicio: `38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd`.
- main / HEAD local: `3c122f48ce4425c2e34313a2a65dcb9218bc77f5`; etiqueta tdl-baseline-v0.1 apunta a ese commit.
- Relación comprobada: UNRELATED_HISTORIES (merge-base sin resultado, exit code 1).
- Commits remotos: 18; raíz única; 17 commits con un padre; ninguna fusión.
- Clasificación: C. PARTIAL_TRANSIT_DATA_LAB_HISTORY.
- UNIQUE_HISTORICAL_VALUE = YES. La evolución remota no es alcanzable desde main local; abandonarla sin conservar una referencia accesible perdería el acceso habitual a estos 18 commits. Esto no afirma superioridad técnica ni descarta copias en otros repositorios.

## Evidencia e interpretación

Los asuntos de commits identifican expresamente GTFS Explorer / GTFS Explorer Desktop y sus versiones 0.1.0-rc1, rc2, estable, 0.2.0, 0.2.1 y v0.2.2. Las rutas src, tests, packaging, schemas, web, LICENSES y docs corroboran un repositorio de producto software, con ingeniería, instalación, pruebas, identidad y releases. La base local contiene 02_Data_Engineering, 03_Compliance y 07_Business: el alcance de gobierno consolidado es más amplio. Por estos metadatos, el remoto representa una historia de producto parcial respecto a Transit Data Lab; no una base consolidada temprana ni solo un prototipo. Esta clasificación es una inferencia acotada a asuntos y rutas; no se ha auditado el contenido ni la calidad del producto.

## Cronología

Fecha de autor ISO 8601; orden ancestral, coincidente con fechas crecientes. Todos los autores: Yeison Aclemus. Los SHA completos se conservan en la sección de cambios.

| SHA corto | Fecha de autor | Autor | Asunto | Padres |
|---|---|---|---|---:|
| afd790c | 2026-08-11T18:02:49+02:00 | Yeison Aclemus | chore: initialize Codex project | 0 |
| 3cfccdb | 2026-08-15T13:47:44+02:00 | Yeison Aclemus | align project with GitHub | 1 |
| 31a4b90 | 2026-08-29T02:43:14+02:00 | Yeison Aclemus | chore(release): freeze GTFS Explorer 0.1.0-rc1 | 1 |
| 39fb597 | 2026-08-29T02:44:13+02:00 | Yeison Aclemus | docs(release): record local Git checkpoint | 1 |
| 2ccdb88 | 2026-08-29T02:44:26+02:00 | Yeison Aclemus | chore(docs): normalize checkpoint whitespace | 1 |
| dc673e2 | 2026-09-01T19:47:58+02:00 | Yeison Aclemus | chore(release): prepare GTFS Explorer 0.1.0-rc2 | 1 |
| 3b25ccc | 2026-09-02T22:57:38+02:00 | Yeison Aclemus | chore(engineering): complete post-rc2 professionalization | 1 |
| 7bc0a5d | 2026-09-03T00:30:41+02:00 | Yeison Aclemus | chore(release): freeze GTFS Explorer 0.1.0 stable | 1 |
| c547443 | 2026-09-06T21:19:22+02:00 | Yeison Aclemus | release: GTFS Explorer Desktop 0.2.0 | 1 |
| e93abe4 | 2026-09-07T01:50:10+02:00 | Yeison Aclemus | chore: clean and organize repository after v0.2.0 | 1 |
| 3b59085 | 2026-09-08T00:36:33+02:00 | Yeison Aclemus | feat(brand): refresh GTFS Explorer welcome and product identity | 1 |
| e5889c8 | 2026-09-08T00:40:52+02:00 | Yeison Aclemus | chore(release): bump GTFS Explorer to 0.2.1 | 1 |
| 0445855 | 2026-09-08T01:04:20+02:00 | Yeison Aclemus | chore(repo): enforce LF for Python sources | 1 |
| 2fd5632 | 2026-09-08T03:16:57+02:00 | Yeison Aclemus | fix(installer): align GTFS Explorer Desktop branding | 1 |
| 866d553 | 2026-09-08T03:46:33+02:00 | Yeison Aclemus | test: stabilize WebEngine readiness synchronization | 1 |
| 47d6d1a | 2026-09-22T04:37:16+02:00 | Yeison Aclemus | release: prepare GTFS Explorer Desktop 0.2.1 | 1 |
| 85c7005 | 2026-09-24T13:00:25+02:00 | Yeison Aclemus | release: GTFS Explorer Desktop v0.2.2 | 1 |
| 38e0e96 | 2026-09-24T22:15:43+02:00 | Yeison Aclemus | docs: align current state after v0.2.2 release | 1 |

## Evolución de árboles

Primer commit: `afd790c70f980c68d0d4a16b851d6845e3fa725f`; 5 archivos:

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/CURRENT_STATE.md`
- `docs/DECISIONS.md`
- `docs/DOMAIN.md`

Último commit: `38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd`; 430 archivos. Inventario por rutas superiores, con muestras acotadas:

| Ruta superior | Archivos | Ejemplos |
|---|---:|---|
| (raíz) | 8 | `.gitattributes`; `.gitignore`; `AGENTS.md`; `CHANGELOG.md` |
| LICENSES | 3 | `LICENSES/MAP_WEB_DEPENDENCIES.md`; `LICENSES/README.md`; `LICENSES/maplibre-gl-6.3.0.txt` |
| docs | 61 | `docs/0.2.0_PRODUCT_ARCHITECTURE.md`; `docs/0.2.0_WINDOWS_ACCEPTANCE_CHECKLIST.md`; `docs/A030_AUDITORIA_VERSIONES_2026-08-23.md`; `docs/A031_DEPENDENCY_UPDATE.md` |
| examples | 2 | `examples/golines-asturias/README.md`; `examples/golines-asturias/style.json` |
| packaging | 6 | `packaging/nsis/README.md`; `packaging/nsis/installer.nsi`; `packaging/nsis/resources/installer_welcome_finish.bmp`; `packaging/portable/README.md` |
| schemas | 10 | `schemas/gtfs_schedule/2026-04-27/build_spec.py`; `schemas/gtfs_schedule/2026-04-27/spec.json`; `schemas/json_export/1.0.0/README.md`; `schemas/json_export/1.0.0/examples/complete.json` |
| spikes | 12 | `spikes/map_webengine/README.md`; `spikes/map_webengine/assets/index.html`; `spikes/map_webengine/assets/loopback_index.html`; `spikes/map_webengine/assets/map_bundle.js` |
| src | 173 | `src/gtfs_explorer/__init__.py`; `src/gtfs_explorer/__main__.py`; `src/gtfs_explorer/application/__init__.py`; `src/gtfs_explorer/application/commands/__init__.py` |
| tests | 120 | `tests/Test exporta e importa/data.duckdb`; `tests/Test exporta e importa/project.json`; `tests/Test real C5 de validación/data.duckdb`; `tests/Test real C5 de validación/project.json` |
| tools | 22 | `tools/README_ORQUESTADOR.md`; `tools/acceptance_feed_smoke.py`; `tools/benchmark.py`; `tools/benchmark_feed.py` |
| web | 13 | `web/map/README.md`; `web/map/build.mjs`; `web/map/package-lock.json`; `web/map/package.json` |

Rutas superiores representadas en alguno de los 18 árboles (443 nombres de archivo distintos): `(raíz)`, `LICENSES`, `docs`, `examples`, `packaging`, `schemas`, `spikes`, `src`, `tests`, `tools`, `web`.

Los recuentos de árboles son entradas hoja de Git, no enumeraciones del sistema de archivos. No se ha materializado ningún árbol remoto.

## Cambios por commit

Comparación frente al único padre; para la raíz, frente al árbol vacío. Renombres detectados por Git con -M (umbral predeterminado); su ausencia no demuestra ausencia de movimientos conceptuales. A=añadidos, M=modificados, D=borrados, R=renombres, C=copias, T=cambio de tipo. Los directorios cuentan entradas de cambio y un renombre entre directorios puede afectar a ambos.

| SHA | A | M | D | R | C | T | Rutas superiores afectadas |
|---|---:|---:|---:|---:|---:|---:|---|
| afd790c | 5 | 0 | 0 | 0 | 0 | 0 | (raíz) (1), docs (4) |
| 3cfccdb | 277 | 4 | 0 | 0 | 0 | 0 | (raíz) (5), LICENSES (3), docs (11), examples (2), packaging (5), schemas (10), spikes (12), src (122), tests (82), tools (16), web (13) |
| 31a4b90 | 53 | 95 | 0 | 0 | 0 | 0 | (raíz) (4), docs (20), packaging (4), schemas (2), src (62), tests (46), tools (9), web (1) |
| 39fb597 | 1 | 5 | 0 | 0 | 0 | 0 | docs (6) |
| 2ccdb88 | 0 | 1 | 0 | 0 | 0 | 0 | docs (1) |
| dc673e2 | 10 | 47 | 0 | 0 | 0 | 0 | (raíz) (2), docs (3), packaging (2), src (23), tests (21), tools (4), web (2) |
| 3b25ccc | 12 | 5 | 0 | 0 | 0 | 0 | (raíz) (3), docs (5), tests (8), tools (1) |
| 7bc0a5d | 0 | 4 | 0 | 0 | 0 | 0 | (raíz) (2), docs (2) |
| c547443 | 62 | 70 | 0 | 0 | 0 | 0 | (raíz) (4), docs (37), spikes (2), src (52), tests (29), tools (6), web (2) |
| e93abe4 | 3 | 9 | 13 | 0 | 0 | 0 | (raíz) (3), docs (8), schemas (1), spikes (1), tests (12) |
| 3b59085 | 13 | 11 | 0 | 0 | 0 | 0 | (raíz) (1), docs (1), src (19), tests (3) |
| e5889c8 | 0 | 8 | 0 | 0 | 0 | 0 | (raíz) (2), src (3), tests (2), tools (1) |
| 0445855 | 1 | 0 | 0 | 0 | 0 | 0 | (raíz) (1) |
| 2fd5632 | 1 | 5 | 0 | 0 | 0 | 0 | packaging (2), src (1), tests (2), tools (1) |
| 866d553 | 0 | 2 | 0 | 0 | 0 | 0 | spikes (2) |
| 47d6d1a | 5 | 28 | 0 | 0 | 0 | 0 | (raíz) (2), docs (2), src (20), tests (9) |
| 85c7005 | 0 | 22 | 0 | 0 | 0 | 0 | (raíz) (3), docs (3), schemas (1), src (3), tests (9), tools (3) |
| 38e0e96 | 0 | 1 | 0 | 0 | 0 | 0 | docs (1) |

- `afd790c70f980c68d0d4a16b851d6845e3fa725f` — chore: initialize Codex project. Muestras: `A AGENTS.md`; `A docs/ARCHITECTURE.md`; `A docs/CURRENT_STATE.md`; `A docs/DECISIONS.md`.

- `3cfccdba7554ca815f4eff77d3cb376b8eb228da` — align project with GitHub. Muestras: `A .gitignore`; `A CHANGELOG.md`; `A LICENSES/MAP_WEB_DEPENDENCIES.md`; `A LICENSES/README.md`.

- `31a4b90f4190d410c5937fb6683c17fd60475ab9` — chore(release): freeze GTFS Explorer 0.1.0-rc1. Muestras: `M .gitignore`; `M README.md`; `A docs/A030_AUDITORIA_VERSIONES_2026-08-23.md`; `A docs/A031_DEPENDENCY_UPDATE.md`.

- `39fb597970d9c3ac549eca8806a30f7865dce7fa` — docs(release): record local Git checkpoint. Muestras: `M docs/A030_AUDITORIA_VERSIONES_2026-08-23.md`; `M docs/A031_DEPENDENCY_UPDATE.md`; `M docs/CURRENT_STATE.md`; `M docs/E2E.md`.

- `2ccdb888a419b14da30fbf29fee9c5c940cd4dfb` — chore(docs): normalize checkpoint whitespace. Muestras: `M docs/LOCAL_GIT_CHECKPOINT.md`.

- `dc673e2834acf95677d4b37329eb638a6ecb302f` — chore(release): prepare GTFS Explorer 0.1.0-rc2. Muestras: `M CHANGELOG.md`; `M README.md`; `M docs/CURRENT_STATE.md`; `A docs/PHASE2_RELEASE_READINESS.md`.

- `3b25ccc3fce6f4251a4e72e7392aed96173ab423` — chore(engineering): complete post-rc2 professionalization. Muestras: `M README.md`; `A REPRODUCIBILITY.md`; `A docs/BUILD.md`; `A docs/CONTRIBUTING.md`.

- `7bc0a5d103e445f540e22101fee8b447719e8383` — chore(release): freeze GTFS Explorer 0.1.0 stable. Muestras: `M CHANGELOG.md`; `M README.md`; `M docs/CURRENT_STATE.md`; `M docs/RELEASE_CHECKLIST.md`.

- `c54744312392356750aa4d217f448cb91d5a2aaa` — release: GTFS Explorer Desktop 0.2.0. Muestras: `M AGENTS.md`; `A GTFS-020-FINAL-SOURCE-REGATE-004.json`; `M README.md`; `M REPRODUCIBILITY.md`.

- `e93abe4eaa0ada2d40ac43300af0c1ec31f5987c` — chore: clean and organize repository after v0.2.0. Muestras: `M .gitignore`; `D GTFS-020-FINAL-SOURCE-REGATE-004.json`; `M README.md`; `M docs/ARCHITECTURE.md`.

- `3b59085650fe6f48ed1f327550c7f35f21577393` — feat(brand): refresh GTFS Explorer welcome and product identity. Muestras: `A docs/BRAND_WELCOME_RASTER_ACCEPTANCE_2026-09-08.md`; `M pyproject.toml`; `M src/gtfs_explorer/presentation/desktop/main_window.py`; `M src/gtfs_explorer/presentation/desktop/startup_intro.py`.

- `e5889c826da78b861d998583bd772af13cceea48` — chore(release): bump GTFS Explorer to 0.2.1. Muestras: `M CHANGELOG.md`; `M README.md`; `M src/gtfs_explorer/infrastructure/exporting/kml.py`; `M src/gtfs_explorer/infrastructure/exporting/working_copy.py`.

- `0445855fa9374c825a490c12e5e7118d6d651fb6` — chore(repo): enforce LF for Python sources. Muestras: `A .gitattributes`.

- `2fd5632fc45858380a3b6859adda409a7910255b` — fix(installer): align GTFS Explorer Desktop branding. Muestras: `M packaging/nsis/installer.nsi`; `A packaging/nsis/resources/installer_welcome_finish.bmp`; `M src/gtfs_explorer/product.py`; `M tests/test_build_installer.py`.

- `866d553e941b2f5752c388386f88453bcdce3b4a` — test: stabilize WebEngine readiness synchronization. Muestras: `M spikes/map_webengine/assets/map_bundle.js`; `M spikes/map_webengine/web/src/app.js`.

- `47d6d1a9a6d2c52304a3ee65824385c3782c8b4e` — release: prepare GTFS Explorer Desktop 0.2.1. Muestras: `M CHANGELOG.md`; `M README.md`; `M docs/CURRENT_STATE.md`; `M docs/SESSION_CONTEXT.md`.

- `85c700587ffec06d73d84825e1951fb73259b62c` — release: GTFS Explorer Desktop v0.2.2. Muestras: `M .gitignore`; `M CHANGELOG.md`; `M README.md`; `M docs/CURRENT_STATE.md`.

- `38e0e96dbeabaf00d53ed4d85509e5a4ce0b06fd` — docs: align current state after v0.2.2 release. Muestras: `M docs/CURRENT_STATE.md`.

## Comparación estructural

- Archivos remotos: 430.
- Archivos locales seguidos por main: 839.
- Comunes: 2: `.gitattributes`, `.gitignore`.
- Exclusivos remotos: 428.
- Exclusivos locales: 837.

Coincidir por nombre no demuestra igualdad de contenido. No se compararon bytes de archivos. Las cifras no incluyen informes sin seguimiento ni directorios vacíos, ignorados o repositorios anidados fuera del árbol raíz.

| Árbol | Ruta superior | Archivos |
|---|---|---:|
| remoto | (raíz) | 8 |
| remoto | LICENSES | 3 |
| remoto | docs | 61 |
| remoto | examples | 2 |
| remoto | packaging | 6 |
| remoto | schemas | 10 |
| remoto | spikes | 12 |
| remoto | src | 173 |
| remoto | tests | 120 |
| remoto | tools | 22 |
| remoto | web | 13 |
| local | (raíz) | 8 |
| local | 02_Data_Engineering | 214 |
| local | 03_Compliance | 433 |
| local | 07_Business | 166 |
| local | reports | 18 |

Exclusivos remotos — ejemplos distribuidos por ruta superior:

- (raíz): `AGENTS.md`; `CHANGELOG.md`; `README.md`.
- LICENSES: `LICENSES/MAP_WEB_DEPENDENCIES.md`; `LICENSES/README.md`; `LICENSES/maplibre-gl-6.3.0.txt`.
- docs: `docs/0.2.0_PRODUCT_ARCHITECTURE.md`; `docs/0.2.0_WINDOWS_ACCEPTANCE_CHECKLIST.md`; `docs/A030_AUDITORIA_VERSIONES_2026-08-23.md`.
- examples: `examples/golines-asturias/README.md`; `examples/golines-asturias/style.json`.
- packaging: `packaging/nsis/README.md`; `packaging/nsis/installer.nsi`; `packaging/nsis/resources/installer_welcome_finish.bmp`.
- schemas: `schemas/gtfs_schedule/2026-04-27/build_spec.py`; `schemas/gtfs_schedule/2026-04-27/spec.json`; `schemas/json_export/1.0.0/README.md`.
- spikes: `spikes/map_webengine/README.md`; `spikes/map_webengine/assets/index.html`; `spikes/map_webengine/assets/loopback_index.html`.
- src: `src/gtfs_explorer/__init__.py`; `src/gtfs_explorer/__main__.py`; `src/gtfs_explorer/application/__init__.py`.
- tests: `tests/Test exporta e importa/data.duckdb`; `tests/Test exporta e importa/project.json`; `tests/Test real C5 de validación/data.duckdb`.
- tools: `tools/README_ORQUESTADOR.md`; `tools/acceptance_feed_smoke.py`; `tools/benchmark.py`.
- web: `web/map/README.md`; `web/map/build.mjs`; `web/map/package-lock.json`.

Exclusivos locales — ejemplos distribuidos por ruta superior:

- (raíz): `BACKUP_AND_RECOVERY.md`; `PROJECT_CURRENT_STATE.md`; `PROJECT_SNAPSHOT_V0.1.md`.
- 02_Data_Engineering: `02_Data_Engineering/GTFS_Lab/20_clientes_reales/.gitignore`; `02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/BIZKAIBUS_LARGE_RUN_ANALYSIS.md`; `02_Data_Engineering/GTFS_Lab/20_clientes_reales/04_audit/pilot_01/NAP_VS_GTFS_EXPLORER.md`.
- 03_Compliance: `03_Compliance/EU/01_Primary_Law/Directive_2010_40_EU/Directive_2010_40_EU_CONSOLIDATED_2023-12-20_ES.pdf`; `03_Compliance/EU/01_Primary_Law/Directive_2023_2661/Directive_EU_2023_2661_ES.pdf`; `03_Compliance/EU/01_Primary_Law/Historical/Regulation_1305_2014/Regulation_1305_2014_CONSOLIDATED_2021-04-18_ES.pdf`.
- 07_Business: `07_Business/01_Governance/ASSUMPTIONS_REGISTER.md`; `07_Business/01_Governance/BUSINESS_MASTER_ROADMAP.md`; `07_Business/01_Governance/DECISION_LOG.md`.
- reports: `reports/repository_integrity/ABSOLUTE_PATH_REGISTER.csv`; `reports/repository_integrity/ABSOLUTE_PATH_REVIEW.md`; `reports/repository_integrity/COMPLIANCE_INTEGRITY_REPORT.md`.

## Estrategias futuras: documentadas, sin selección ni ejecución

| Opción | Conservación del historial | Complejidad | Riesgo | Claridad resultante |
|---|---|---|---|---|
| A. Conservar main remoto y crear un repositorio nuevo para la base | Mantiene íntegro el remoto; la base conserva su historia independiente | Baja técnicamente; dos repositorios que gobernar | Confusión si no se documenta cuál es canónico | Alta con nombres y enlaces claros; el antiguo puede seguir activo |
| B. Archivar la historia remota en rama/etiqueta y convertir después la base en main | Conserva los 18 commits si la referencia se crea y verifica antes del cambio | Media/alta: transición de main, protecciones, etiquetas y consumidores | Cambio de main no fast-forward; referencias archivadas que se borren o no se protejan; automatizaciones afectadas | Un único repositorio, pero dos líneas históricas independientes |
| C. Integración histórica explícita de ambas historias | Hace ambas ancestrías alcanzables desde un commit con dos padres | Alta: diseñar árbol final, resolver coincidencias y explicar semántica | Mezcla conceptual, conflictos y asociación engañosa entre versiones del producto y base | Un grafo conectado, más difícil de interpretar sin decisión documentada |
| D. Mantener GitHub actual como archivo histórico y crear nuevo canónico Transit Data Lab | Conserva íntegra la historia antigua y separa la nueva | Baja/media: archivo formal, referencias, mantenimiento y canonicidad | Enlaces y automatizaciones al repositorio antiguo; archivo debe continuar accesible | Alta: función histórica frente a función canónica explícitas |

A y D comparten la separación en dos repositorios; D añade explícitamente el carácter de archivo histórico y la canonicidad del nuevo. B y C necesitarían autorización y diseño específicos; aquí no se ejecuta ninguna transición.

## Conservación y guardas

- local HEAD changed = NO; local main changed = NO; origin/main changed = NO.
- remote changed = NO entre las dos observaciones read-only de refs/heads/main; no se ejecutó ninguna escritura remota. No se afirma ausencia de cambios concurrentes transitorios no observados.
- real index changed = NO, comprobado por SHA-256 dirigido al archivo de índice.
- REMOTE_GITHUB_ALIGNMENT.md conservado byte a byte, comprobado por SHA-256 dirigido.
- tdl-baseline-v0.1 conservada; destino verificado.
- working-directory recursive scan = NO.
- datasets traversed = NO.
- databases read = NO.
- repository-wide hash = NO.
- RESOURCE_GUARD_TRIGGERED = NO.
- Solo se enumeró la raíz inmediata al inicio; no se hizo enumeración recursiva del workspace.
- No push, force push, merge, rebase, pull, checkout, reset, cherry-pick, stage, commit ni borrado de refs.
- files created = reports/repository_integrity/REMOTE_HISTORY_REVIEW.md.
- files modified = ninguno preexistente.
- files deleted = ninguno.
- files moved = ninguno.

## Verificación reproducible y evidencias

Comandos de solo lectura: rev-parse HEAD/main/origin/main y etiqueta resuelta; log --reverse con SHA, fecha, autor, asunto y padres; ls-tree -r --name-only -z para árboles; diff-tree --root --no-commit-id -r --name-status -z -M por commit; merge-base; ls-remote origin refs/heads/main al inicio y al final; ls-files --error-unmatch para el informe. No fetch ni inspección de refs ajenas.

- SHA-256 índice antes/después: `fb5dd05780e89e67168a342fcc8d8e30caf3f468b8d49019a207461bf944884c`.
- SHA-256 informe de alineación antes/después: `77c2e65dda0329b52cf7ee538b6b1575aba8e716b4909fa64e88f241738563af`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
