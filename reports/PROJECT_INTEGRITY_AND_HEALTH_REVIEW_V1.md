# Transit Data Lab — revisión de integridad y salud V1

**Fecha de corte:** 2026-10-07\
**Raíz canónica:** `P:\TransitDataLab`\
**Checkout principal:** `01_Project/Transit Data Lab`\
**HEAD observado:** `f8befd4fdc980782ddb75b6ae7dd552f7bfb0436` (`main`, alineado con `origin/main` al inicio de la revisión)

## Dictamen

| Gate | Resultado | Alcance |
|---|---|---|
| Entorno canónico P: | **PASS_WITH_LIMITATIONS** | Rutas, raíces y pruebas controladas resuelven en P:. El Python base del venv y Node/npm son instalaciones de Windows en C:, no datos ni checkout TDL. |
| Integridad del proyecto | **PASS_WITH_LIMITATIONS** | Sin dependencia activa encontrada de las antiguas raíces C:; referencias, hashes seleccionados, bases, datos y junctions coherentes. La historia local de repositorios de producto conserva excepciones explicadas. |
| Validación técnica | **PASS_WITH_LIMITATIONS** | Suites y gates actuales de TDL y NeTEx pasan; quedan skips documentados. No se sometió el producto Desktop independiente a su suite completa. |
| Prueba controlada de producto | **PASS_WITH_LIMITATIONS** | Flujo sintético completo, artefactos y replay verificados; no equivale a piloto externo ni a validación comercial. |
| Ejecución solo desde rutas canónicas | **PASS** | Flujo sintético completado desde P:, sin rutas locales C: en los informes. Runtime base de Windows sigue en C:. |

**Salud global:** coherente para el alcance interno probado; con limitaciones documentadas. **Piloto real externo: NO autorizado/listo** hasta validar recuperación independiente y resolver autorización de contacto y tratamiento de datos externos. El estado previo `READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS` sigue describiendo readiness técnica interna; no se amplía con esta revisión.

## Método y límites de protección

La inspección usó metadatos de filesystem/reparse points, referencias/manifiestos y hashes ya exigidos por contratos. Se consultaron ambas DuckDB en solo lectura. No se abrió ni hasheó contenido de HOLDOUT ni el PFX; no se modificó evidencia histórica, bases, fuentes, repositorios anidados, junctions, versión de Desktop ni estado de release. Los archivos generados de la revisión están bajo `04_Runtime/Outputs/project_health_review_v1` y no forman parte del checkout.

La evidencia post-migración de HOLDOUT continúa siendo de nivel metadatos, no una nueva prueba de integridad a nivel de contenido. Estado conservador: `HOLDOUT_POST_KILL_INTEGRITY = NOT_REPROVEN_CONTENT_LEVEL`; no hay evidencia observada de modificación y no se requiere reparación. No se debe convertir esa limitación en un PASS de contenido.

## Resultados por dominio

### Filesystem, rutas y configuración

- Las nueve raíces canónicas están presentes. Configuración y activador apuntan a `P:\TransitDataLab`; `NETEX_SCHEMA_PATH`, Artifact Store y TEMP resuelven en P:. Espacio libre observado: 223.959.351.296 bytes (~208,6 GiB).
- Registro central de rutas y variables validados. Búsqueda de rutas heredadas en código/configuración activa: cero coincidencias para `C:\TDL`, `C:\TDL_DATA`, antiguos `Proyectos`, runtime y evidencia. Las apariciones en historia/informes se conservan.
- Conteo metadata-only del árbol, excluyendo los subárboles Holdout y Private: 23.510 directorios, 98.524 archivos y 34 reparse points; cero errores de acceso, cero destinos rotos, cero extras o faltantes frente al registro. No se siguieron junctions durante el conteo. Las 34 apuntan a destinos P: existentes y se detallan en el apéndice.
- No se encontraron nombres `.partial`, `.tmp`, `bank.lock` o `.lck`. Los 79 blobs versionados de cero bytes se explican por capturas stderr/diffs vacías o capturas HTML marcadas `UNAVAILABLE_EMPTY_RESPONSE`; no son autoridad para reconstruir contenido fuente y no se alteraron.
- El binario aceptado del cliente conserva SHA-256 `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266`.

### Git y repositorios independientes

`git fsck --full --no-reflogs --no-dangling` finalizó con salida 0 y sin diagnósticos en los cinco repositorios inspeccionados: checkout principal, Artifacts, Desktop, Engineering y repositorio de restore histórico.

| Repositorio | Estado observado | Tratamiento |
|---|---|---|
| TDL principal | `main`, `f8befd4…`, limpio y alineado con `origin/main`; sin submódulos | Integridad PASS al comienzo de la revisión. |
| GTFS Explorer Artifacts | `main`, `d49ef16…`, limpio, sin origin | Repo independiente; conservar. |
| GTFS Explorer Desktop | `main`, `07e2c2a…`, limpio y alineado con remoto | Repo independiente. Mantener baseline 0.2.2. Existe un worktree obsoleto/prunable a una ruta temporal ya ausente; no podado. |
| GTFS Explorer Engineering | `main`, `efdfe91…`, 5 modificaciones locales preexistentes, sin untracked | Cambios clasificados UNKNOWN/preexistentes; no se leyeron diffs ni se modificaron. |
| Restore test histórico | detached `85c7005…`; bundle asociado P: verificado | Evidencia histórica. Remote local apunta a bundle C: ausente; no se reconfiguró ni alteró. |

No se detectaron submódulos en el checkout principal. El escaneo dirigido de secretos conocidos no encontró candidatos; no cubre todo el historial Git ni constituye certificación de secretos. Los repositorios de productos siguen siendo repositorios separados y no deben incorporarse al índice del padre.

### Datos, manifests y Test Bank

- Corpus Development: 14 entradas; 13 ZIP se verificaron según el contrato y coinciden con inventario/split. `dataset019` quedó sin abrir ni hashear por su límite de coste/alcance. IDs de HOLDOUT se filtraron antes del acceso a sus rutas.
- DB GTFS: SHA observado `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`; recuentos raw: 41 agencies, 609 routes, 21.015 trips, 354.287 stop_times y 6.368 stops. La duplicación documentada `main.stops`/`raw.stops` persiste.
- DB Compliance: SHA `4db39fa5494c525f339f68bf0b96087b5ff2e1e0cb830eea882336174bc8048b`; 48 requirements, 36 source facts, 92 provisions, 10 deadlines, 15 capacidades Phase 3 y 10 estados de cobertura (9 PARTIAL, 1 UNRESOLVED). Un SQL histórico que esperaba 8 filas no se ejecutó sobre esta baseline de 10; el gate portable actual y tests de transición sí pasan.
- Test Bank: 30 IDs únicos (`00001`–`00030`); 29 OK y 1 NOT_OK, ambos coherentes con `case.json`. 29 manifests de entrega y 4.260 referencias de artefactos, con tamaño/ruta concordantes. El caso NOT_OK sin manifest de entrega es el comportamiento esperado.
- Bases, fuentes y evidencia originales no se repararon ni regeneraron. El piloto controlado no usó datos de clientes.

### Motores, reporting y cliente

GTFS Lab conserva invariantes de contabilidad en cero en los recorridos probados. Compliance mantiene estados PARTIAL/UNRESOLVED sin elevarlos a PASS. Interpretación mantiene separación entre hallazgo técnico y conclusión legal, y entre anomalía espacial y error automático. NeTEx pasa su alcance V1 acotado: no se afirma conformidad nacional/universal.

La suite `unittest` de GTFS Lab ejecutó 320 pruebas: 318 PASS, 0 FAIL, 2 SKIP, 12,295 s. Python 3.12.10; pytest no está instalado, pero estos tests se ejecutan con `unittest`. Trust persistence gate, golden corpus (2 casos), golden regression (incluye mutaciones negativas), Test Bank E2E sintético y Client Workflow E2E sintético pasan. El último produjo PDF/Markdown/JSON, manifest y seal válidos, 34 artefactos por run y accounting gap 0; no accedió a HOLDOUT ni subió datos.

La prueba controlada adicional usó GTFS sintético con shapes. Generó 37 artefactos de entrega, PDF/Markdown/JSON y GeoJSON/KML; tamaños, hashes y seal válidos; fuente inmutable; informe del motor idéntico en replay; accounting gap 0; `INTERPRETATION_COMPLETED`; conclusión de publicación `NO ES POSIBLE EMITIR CONCLUSIÓN`. Esto demuestra la tubería seleccionada y no su comportamiento sobre todo dato/cliente.

El cliente interno conserva el hash aceptado. Se auditaron contratos/unit tests y el flujo sintético; no se repitió aceptación GUI manual ni clean-machine W08. El repo Desktop independiente no ejecutó suite completa: sus AGENTS locales condicionan la fase integrada a un descriptor que no estaba presente. No se modificó ese repositorio.

### Runtime y seguridad de dependencias

Python del venv vive en P:, aunque `sys.base_prefix` apunta a una instalación Python de Windows en C:. Node/npm también están en `C:\Program Files`; cache npm y datos/runtime TDL inspeccionados apuntan a P:. Son dependencias del runtime de la estación, no antiguas raíces de proyecto. Por tanto, la ejecución P-only queda probada para este equipo, pero no la reconstrucción en máquina limpia exclusivamente desde P:.

MapLibre: `maplibre-gl 6.3.0`, directo en el repo independiente Desktop; severidad crítica autoritativa (CVSS 10 en el [advisory GHSA-jrc7-96c5-q579](https://github.com/advisories/GHSA-jrc7-96c5-q579)), versiones afectadas hasta 6.4.0 y parche desde 6.4.1. El advisory describe XSS al renderizar attribution no confiable. El repo permite paquetes locales con attribution, así que existe una superficie potencial; no se probó explotación ni se afirma que haya un payload malicioso. Recomendación: tarea de seguridad independiente, actualizar a versión corregida y ejecutar regresión específica; no alterar baseline 0.2.2 dentro de esta revisión de TDL.

## Reconciliación documental y reparaciones

Se actualizaron los documentos operativos desfasados que describían rutas antiguas a bases/restore. Se añadió el contrato mínimo de recuperación: backup separado para datos/evidencia/privado, destino independiente, restauración y hashes dirigidos antes de afirmar recuperabilidad. No existe actualmente backup externo integral ni restore probado.

Se añadieron este informe, la matriz y el análisis de gaps; se enlazan desde README y se refleja el dictamen en `PROJECT_STATUS.md` y `PROJECT_STATUS_TREE.md`. Los registros históricos permanecen sin reescritura. No se aplicaron cambios de código porque no se halló bug activo de rutas en el alcance inspeccionado; no se tocó MapLibre.

## Hallazgos pendientes

1. **Antes de piloto externo:** copia de recuperación independiente y restauración validada de datos y evidencia no regenerables, incluido el tratamiento restringido del material privado; autorización explícita para contacto externo y manejo de datos.
2. **Antes de distribuir GTFS Explorer Desktop:** actualizar MapLibre a versión corregida y validar regresiones; cambio separado en su repositorio independiente.
3. **Portabilidad:** documentar/probar reconstrucción limpia del Python base y herramientas Windows necesarias, sin confundir instalaciones de sistema con datos TDL.
4. **Repos locales:** resolver explícitamente los cinco cambios Engineering y el worktree Desktop obsoleto cuando exista autorización y contexto del producto; conservar mientras tanto.
5. Dataset 019, feeds extremos, certificaciones y estándares diferidos siguen siendo alcance futuro; no son fallos de esta prueba sintética.

## Apéndice — 34 junctions registradas

Los motivos, dependencias declaradas y condiciones de retirada se transcriben del registro de migración. `ACTIVE_REFERENCE_FOUND` se reporta como **contrato documentado; consumidor exacto no localizado individualmente**: no se infiere búsqueda exhaustiva por junction. Todas están presentes y sus targets existen en P:. Retirada solo tras cumplir la condición registrada y volver a comprobar consumidores y compatibilidad; ninguna se retira aquí.

| OLD_PATH | TARGET | TARGET_EXISTS | ACTIVE_REFERENCE_FOUND | WHY_STILL_NEEDED | REMOVAL_CONDITION |
|---|---|---:|---|---|---|
| P:\TransitDataLab\01_Project\Transit Data Lab\.vscode | P:\TransitDataLab\Private\Editor\.vscode | True | Contrato documentado; consumidor exacto no localizado individualmente | Preserved local editor settings with P interpreter | Native editor integration can read settings outside source |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\.tmp | P:\TransitDataLab\04_Runtime\Temp\DesktopScratch | True | Contrato documentado; consumidor exacto no localizado individualmente | Rebuilt runtime used by existing tools | Update tool recipe to use TDL_RUNTIME_ROOT directly |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\.venv | P:\TransitDataLab\04_Runtime\Current\Desktop | True | Contrato documentado; consumidor exacto no localizado individualmente | Rebuilt runtime used by existing tools | Update tool recipe to use TDL_RUNTIME_ROOT directly |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\.vscode | P:\TransitDataLab\Private\Editor\06_Products\GTFS Explorer\GTFS Explorer Desktop\.vscode | True | Contrato documentado; consumidor exacto no localizado individualmente | Preserved local editor settings with P interpreter | Native editor integration can read settings outside source |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\web\map\dist | P:\TransitDataLab\04_Runtime\Current\Map\dist | True | Contrato documentado; consumidor exacto no localizado individualmente | Rebuilt runtime used by existing tools | Update tool recipe to use TDL_RUNTIME_ROOT directly |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\web\map\node_modules | P:\TransitDataLab\04_Runtime\Current\Map\node_modules | True | Contrato documentado; consumidor exacto no localizado individualmente | Rebuilt runtime used by existing tools | Update tool recipe to use TDL_RUNTIME_ROOT directly |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\tests\.runtime | P:\TransitDataLab\04_Runtime\Temp\DesktopTests | True | Contrato documentado; consumidor exacto no localizado individualmente | Rebuilt runtime used by existing tools | Update tool recipe to use TDL_RUNTIME_ROOT directly |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\tests\fixtures\generated | P:\TransitDataLab\02_Data\CanonicalAssets\06_Products\GTFS Explorer\GTFS Explorer Desktop\tests\fixtures\generated | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\06_Products\GTFS Explorer\GTFS Explorer Desktop\examples\golines-asturias\generated | P:\TransitDataLab\02_Data\CanonicalAssets\06_Products\GTFS Explorer\GTFS Explorer Desktop\examples\golines-asturias\generated | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\03_Compliance\databases | P:\TransitDataLab\02_Data\External\Databases\Compliance | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\databases | P:\TransitDataLab\02_Data\External\Databases\GTFS | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\feeds | P:\TransitDataLab\02_Data\CanonicalAssets\02_Data_Engineering\GTFS_Lab\feeds | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\runs | P:\TransitDataLab\03_Evidence\Historical\CanonicalAssets\02_Data_Engineering\GTFS_Lab\runs | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_D_MATURE_BENCHMARK\020_kbus\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset020\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_D_MATURE_BENCHMARK\019_bizkaibus\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset019\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_D_MATURE_BENCHMARK\018_bilbobus\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset018\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_D_MATURE_BENCHMARK\017_tuvisa\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset017\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_D_MATURE_BENCHMARK\016_alu\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset016\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_C_COMPLEX_REGIONAL\015_rias_baixas\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset015\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_C_COMPLEX_REGIONAL\014_gilsanz\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset014\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_C_COMPLEX_REGIONAL\013_lazara\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset013\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_B_SME_OPERATIONAL\012_costa\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset012\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_B_SME_OPERATIONAL\011_autocorb\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset011\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_B_SME_OPERATIONAL\010_rodil\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset010\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_B_SME_OPERATIONAL\009_medina\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset009\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_B_SME_OPERATIONAL\008_baraza\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset008\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\007_perez_cubero\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset007\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\006_rafael_nadal\02_sources | P:\TransitDataLab\02_Data\Holdout\dataset006\02_sources | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\005_viagon\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset005\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\004_alvarez_viajeros\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset004\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\003_j_cristeto\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset003\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\002_ancebus\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset002\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\02_Data_Engineering\GTFS_Lab\20_clientes_reales\FAMILY_A_SMALL_BASIC\001_galan_gomez\02_sources\gtfs_schedule\original | P:\TransitDataLab\02_Data\Development\dataset001\original | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
| P:\TransitDataLab\01_Project\Transit Data Lab\01_Research_Standards\NeTEx\schemas\v2.0.0\xsd | P:\TransitDataLab\02_Data\External\netex-schema-v2.0.0\xsd | True | Contrato documentado; consumidor exacto no localizado individualmente | Current relative data/schema/evidence contract | Replace consuming relative contract with explicit TDL_* resource configuration |
