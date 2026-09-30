# G03 — normative gap burn-down (2026-09-30)

**Verdict:** `G03_REMAINS_IN_PROGRESS_WITH_KNOWN_GAPS`

## Método y límite de evidencia

Contraste del capability map y contrato local con la referencia primaria GTFS Schedule, revisión 2026-04-27: <https://gtfs.org/documentation/schedule/reference/>. No se ha usado código legacy ni validadores de terceros. No se ha leído contenido, metadatos de evaluación ni artefactos HOLDOUT.

El contrato local conserva `Conditionally Required/Forbidden` y anchor por campo, pero no la frase normativa original. La expresión “original” de este inventario es una transcripción normalizada de la referencia oficial, no una recuperación de metadatos que no estén en el contrato.

En la tabla, “bloquea” identifica el comportamiento actual: el evaluador G03 de cabeceras emite `NOT_EVALUABLE` para los 31 campos. Semánticamente estas condiciones regulan presencia/ausencia del valor por fila, no tipo/formato ni presencia del archivo; varias no deciden por sí solas si el nombre de columna debe existir. Ninguna cambia reglas de presencia de archivo.

## A. Inventario de 31 condiciones sin resolver

### RESOLVABLE_FROM_OFFICIAL_REFERENCE (16)

En el estado inicial del burn-down, estas reglas deterministas se marcaban `NOT_EVALUABLE` porque aún faltaba conectar la interpretación de efectos `required/optional/forbidden` al runtime. La sección D registra la implementación local posterior.

| file | field | source anchor | original condition (normalizada) | expresión representable | ownership propuesto | bloquea |
|---|---|---|---|---|---|---|
| stops.txt | stop_name | [stops](https://gtfs.org/documentation/schedule/reference/#stopstxt) | Required para location_type 0, 1, 2; optional para 3, 4. | `FIELD_VALUE_IN(location_type,[0,1,2])` | G03_SCHEMA | presencia condicional de valor/cabecera |
| stops.txt | stop_lat | [stops](https://gtfs.org/documentation/schedule/reference/#stopstxt) | Required para location_type 0, 1, 2; optional para 3, 4. | `FIELD_VALUE_IN(location_type,[0,1,2])` | G03_SCHEMA; bounds G07 | presencia condicional de valor/cabecera |
| stops.txt | stop_lon | [stops](https://gtfs.org/documentation/schedule/reference/#stopstxt) | Required para location_type 0, 1, 2; optional para 3, 4. | `FIELD_VALUE_IN(location_type,[0,1,2])` | G03_SCHEMA; bounds G07 | presencia condicional de valor/cabecera |
| stops.txt | parent_station | [stops](https://gtfs.org/documentation/schedule/reference/#stopstxt) | Required para 2, 3, 4; optional para 0; forbidden para 1. | `FIELD_VALUE_IN(location_type,[2,3,4])`; forbidden `FIELD_VALUE_EQUALS(location_type,1)` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| stops.txt | stop_access | [stops](https://gtfs.org/documentation/schedule/reference/#stopstxt) | Forbidden para location_type 1, 2, 3, 4 o si parent_station está vacío; optional otherwise. | `ANY(FIELD_VALUE_IN(location_type,[1,2,3,4]), FIELD_VALUE_EQUALS(parent_station,""))` | G03_SCHEMA | presencia condicional de valor/cabecera |
| routes.txt | route_short_name | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Required si route_long_name está vacío; recommended otherwise. | `FIELD_VALUE_EQUALS(route_long_name,"")` | G03_SCHEMA | presencia condicional de valor/cabecera |
| routes.txt | route_long_name | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Required si route_short_name está vacío; optional otherwise. | `FIELD_VALUE_EQUALS(route_short_name,"")` | G03_SCHEMA | presencia condicional de valor/cabecera |
| stop_times.txt | stop_id | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Required si location_group_id AND location_id no están definidos; forbidden si cualquiera está definido. | `ALL(location_group_id empty, location_id empty)` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| stop_times.txt | location_group_id | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Forbidden si stop_id o location_id están definidos. | `ANY(stop_id defined, location_id defined)` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| stop_times.txt | location_id | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Forbidden si stop_id o location_group_id están definidos. | `ANY(stop_id defined, location_group_id defined)` | G03_SCHEMA; existencia GeoJSON G04 / feature diferida | presencia condicional de valor/cabecera |
| stop_times.txt | pickup_type | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | pickup_type=0 o 3 forbidden si start/end window está definido; optional otherwise. | `FIELD_VALUE_IN(pickup_type,[0,3]) AND ANY(window defined)` | G03_SCHEMA; semántica de ventana G05 | presencia condicional del valor |
| stop_times.txt | drop_off_type | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | drop_off_type=0 forbidden si start/end window está definido; optional otherwise. | `FIELD_VALUE_EQUALS(drop_off_type,0) AND ANY(window defined)` | G03_SCHEMA; semántica de ventana G05 | presencia condicional del valor |
| transfers.txt | from_stop_id | [transfers](https://gtfs.org/documentation/schedule/reference/#transferstxt) | Required si transfer_type vacío, 0, 1, 2, 3; optional si 4 o 5. | `FIELD_VALUE_IN(transfer_type,["",0,1,2,3])` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| transfers.txt | to_stop_id | [transfers](https://gtfs.org/documentation/schedule/reference/#transferstxt) | Required si transfer_type vacío, 0, 1, 2, 3; optional si 4 o 5. | `FIELD_VALUE_IN(transfer_type,["",0,1,2,3])` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| transfers.txt | from_trip_id | [transfers](https://gtfs.org/documentation/schedule/reference/#transferstxt) | Required si transfer_type es 4 o 5; optional otherwise. | `FIELD_VALUE_IN(transfer_type,[4,5])` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |
| transfers.txt | to_trip_id | [transfers](https://gtfs.org/documentation/schedule/reference/#transferstxt) | Required si transfer_type es 4 o 5; optional otherwise. | `FIELD_VALUE_IN(transfer_type,[4,5])` | G03_SCHEMA; referencia G04 | presencia condicional de valor/cabecera |

### AMBIGUOUS_OFFICIAL_PROSE (0)

No se encontró prosa ambigua en las 31 condiciones consultadas. Que una regla sea clara no implica que su operador esté ejecutado.

### CROSS_STAGE_NOT_G03 (10)

La regla puede ser determinista, pero la prueba requiere conteos, registros relacionados, orden del viaje o semántica asignada a etapas posteriores. No transferir ownership a G03.

| file | field | source anchor | original condition (normalizada) | motivo / operador ausente | ownership | bloquea |
|---|---|---|---|---|---|---|
| agency.txt | agency_id | [agency](https://gtfs.org/documentation/schedule/reference/#agencytxt) | Required si el dataset contiene varias agencias; recommended otherwise. | `COUNT(agency rows)>1`; `ENTITY_EXISTS` no expresa cardinalidad >1. | G04 identidad/cardinalidad; G03_SCHEMA consume resultado | presencia condicional de valor/cabecera |
| routes.txt | agency_id | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Required si hay varias agencias definidas en agency.txt; recommended otherwise. | Igual: operador de conteo ausente. | G04 identidad/cardinalidad; G03_SCHEMA consume resultado | presencia condicional de valor/cabecera |
| routes.txt | continuous_pickup | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Cualquier valor distinto de 1/vacío forbidden si existe ventana en cualquier trip de la ruta; optional otherwise. | Cuantificación sobre trips y stop_times relacionados. | G05 temporal/multirregistro | presencia condicional del valor |
| routes.txt | continuous_drop_off | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Igual para continuous drop-off. | Cuantificación sobre trips y stop_times relacionados. | G05 temporal/multirregistro | presencia condicional del valor |
| trips.txt | shape_id | [trips](https://gtfs.org/documentation/schedule/reference/#tripstxt) | Required si pickup/drop-off continuo se define en routes o stop_times; optional otherwise. | Resolución por ruta/trips/stop_times; relación multirregistro. | G05 temporal/multirregistro | presencia condicional del valor |
| stop_times.txt | arrival_time | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Required en primera y última parada del trip y para timepoint=1; forbidden si hay ventana; optional otherwise. | Primera/última parada requiere agrupación/orden por trip y stop_sequence. | G06 secuencia; G05 temporal | presencia condicional del valor |
| stop_times.txt | departure_time | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Required para timepoint=1; forbidden si hay ventana; optional otherwise. | Aun con señal escalar, sus exclusiones pertenecen a reglas de servicio/ventanas temporalmente acopladas. | G05 temporal | presencia condicional del valor |
| stop_times.txt | continuous_pickup | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Valor distinto de 1/vacío forbidden si hay ventana; optional otherwise. | La condición de fila parece escalar, pero el significado/precedencia de comportamiento continuo está asignado a G05. | G05 temporal | presencia condicional del valor |
| stop_times.txt | continuous_drop_off | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Igual para continuous drop-off. | Igual: ownership temporal y precedencia de servicio continuo. | G05 temporal | presencia condicional del valor |
| translations.txt | record_id | [translations](https://gtfs.org/documentation/schedule/reference/#translationstxt) | Forbidden si table_name=feed_info o field_value está definido; required si field_value está vacío. | El significado de record_id depende de tabla y claves primarias heterogéneas. | G04 identidad referencial | presencia condicional de valor/cabecera |

### DEFERRED_FEATURE (1)

| file | field | source anchor | original condition (normalizada) | motivo | ownership | bloquea |
|---|---|---|---|---|---|---|
| routes.txt | network_id | [routes](https://gtfs.org/documentation/schedule/reference/#routestxt) | Forbidden si existe route_networks.txt o networks.txt; optional otherwise. | FILE_PRESENT existe, pero ambas tablas están fuera del subconjunto FULL_V1 de G01; habilitarlas ampliaría feature scope. | G01/G03 catálogo diferido | presencia condicional de columna/valor a partir de archivo |

### NO_MACHINE_EXECUTABLE_RULE (4)

| file | field | source anchor | original condition (normalizada) | motivo | ownership | bloquea |
|---|---|---|---|---|---|---|
| stop_times.txt | start_pickup_drop_off_window | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Required si location_group_id, location_id o end window están definidos; forbidden si arrival_time o departure_time están definidos; optional otherwise. | La política debe producir distintos efectos (required/forbidden/optional) según expresiones compuestas; el modelo actual conserva un predicado, no la función outcome. | G03_SCHEMA; intervalo G05 | presencia condicional del valor |
| stop_times.txt | end_pickup_drop_off_window | [stop_times](https://gtfs.org/documentation/schedule/reference/#stop_timestxt) | Required si location_group_id, location_id o start window están definidos; forbidden si arrival_time o departure_time están definidos; optional otherwise. | Igual: no se puede expresar de forma ejecutable una función de presencia con varios outcomes usando el contrato actual. | G03_SCHEMA; intervalo G05 | presencia condicional del valor |
| translations.txt | record_sub_id | [translations](https://gtfs.org/documentation/schedule/reference/#translationstxt) | Forbidden si table_name=feed_info o field_value definido; required si table_name=stop_times y record_id definido. | La regla requiere mapear secondary key por nombre de tabla; esa política relacional no existe en G03. | G04 identidad referencial | presencia condicional de valor/cabecera |
| translations.txt | field_value | [translations](https://gtfs.org/documentation/schedule/reference/#translationstxt) | Forbidden si table_name=feed_info o record_id definido; required si record_id está vacío. | La selección de objetivo y precedence entre record_id/field_value pertenece a identidad/traducciones, no a la mera cabecera G03. | G04 identidad referencial | presencia condicional de valor/cabecera |

**Control de grupos:** 16 + 0 + 10 + 1 + 4 = 31. En el snapshot inicial, las 16 expresiones representables aún no eran ejecutables. La sección D registra su conexión sin ampliar operadores ni dominios; los restantes gaps conservan su clasificación.

## B. Cuatro gaps de tipo/formato

| file.field | evidencia normativa | clase | decisión G03 | motivo |
|---|---|---|---|---|
| agency.txt.agency_phone | El tipo `Phone number`; descripción: cadena típica del área de servicio, puntuación para agrupar dígitos y texto marcable permitido, sin otro texto descriptivo. | Prosa, no gramática léxica completa | `NOT_EVALUABLE` | “Typical” y ejemplos no fijan gramática determinista; no inventar regex ni adoptar formato de terceros. |
| agency.txt.agency_email | Tipo definido como “An email address”; sin gramática formal. | Solo prosa | `NOT_EVALUABLE` | Sin regla lexical reproducible para validar aceptación exacta. |
| pathways.txt.stair_count | Tipo `Non-null integer`; descripción define número de escalones, positivo sube y negativo baja. Field Presence = Optional. | Semántica y prosa numérica; serialización/nulidad sin aclarar | `NOT_EVALUABLE` | No asumir que `Non-null integer` equivale al token `Integer`, ni inferir qué significa celda vacía. |
| feed_info.txt.feed_contact_email | Tipo “An email address”; sin gramática formal. | Solo prosa | `NOT_EVALUABLE` | Igual gap léxico que agency email; la recomendación email-or-URL es advisory cross-field, no formato G03. |

Para estos cuatro no hay enum, rango numérico explícito ni sintaxis estructurada adicional que permita normalización G03 local. No se ejecuta validación relacional, temporal ni espacial.

## C. Snapshot del capability map antes del runtime

En el momento del burn-down normativo, antes de completar el runtime, ninguna regla había llegado a ejecución demostrable. Esta tabla conserva esa observación histórica del 2026-09-30.

| métrica | antes | después |
|---|---:|---:|
| primary `EXECUTABLE_G03` | 97 | 97 |
| primary `PARTIALLY_EXECUTABLE_G03` | 4 | 4 |
| primary `UNRESOLVED_CONDITION` | 31 | 31 |
| secondary `UNRESOLVED_TYPE_FORMAT` | 4 | 4 |
| secondary `EMPTY_SEMANTICS_NOT_SPECIFIED` | 98 | 98 |
| secondary `NEEDS_REVIEW` | 39 | 39 |
| secondary `DEFERRED_G04/G05/G06/G07/G08` | 24/11/0/4/0 | 24/11/0/4/0 |
| empty semantics `SOURCE_METADATA_RETAINED` | 34 | 34 |
| type definitions `EXPLICIT/PARTIAL/NEEDS_REVIEW` | 128/3/1 | 128/3/1 |
| `presence_condition` executable / unresolved | 101/31 | 101/31 |
| `type_format` executable / unresolved | 128/4 | 128/4 |
| normative ranges / range metadata needs review | 14/1 | 14/1 |
| explicit enum lists / enum domains by field reference | 24/6 | 24/6 |
| ownership `G03_SCHEMA` conservative / needs review | 47/31 | 47/31 |
| ownership `G03_TYPE_FORMAT` conservative | 132 | 132 |
| deferred ownership G04/G05/G07 | 24/11/4 | 24/11/4 |
| range `NO_EXPLICIT_RANGE/NORMATIVE_RANGE/NOT_NORMALIZED_REQUIRES_REVIEW` | 117/14/1 | 117/14/1 |
| enum `EXPLICIT_OFFICIAL_LIST/DEFINED_BY_FIELD_REFERENCE` | 24/6 | 24/6 |
| nuevas constraints ejecutables | 0 | 0 |

En ese snapshot, la cifra primaria ejecutable era 97 y no había predicados condicionales ejecutados. La sección posterior registra la implementación local aditiva.

## D. Fronteras, tests y cierre

- G04 referencias/identidad, G05 temporal, G06 secuencias, G07 espacial y G08 calidad permanecen en sus ownerships; no se inició ninguno.
- Cabeceras extra continúan sin fallo solo por ser extra.
- Vacíos `NOT_SPECIFIED` continúan sin inferencia.
- El burn-down inicial registró 29/29 tests; tras la conexión del runtime, el conjunto focalizado actual suma 45/45 tests (5 de runtime, 11 de contrato, 10 de G02 y 19 de catálogo/estructura). No se ejecuta regresión completa previa a publicación.
- HOLDOUT: sin acceso a contenido ni replay.
- En el estado inicial, `G03_READY_FOR_FULL_REVIEW` no procedía. La sección siguiente registra el avance local, sin promover G03 ni publicación.


## D. G03 Condition Runtime Completion — implementación local

Se conectaron las 16 condiciones clasificadas `RESOLVABLE_FROM_OFFICIAL_REFERENCE` al runtime G03. Se reutilizan exclusivamente operadores G02 (`FIELD_PRESENT`, `FIELD_VALUE_EQUALS`, `FIELD_VALUE_IN`, `ALL`, `ANY`) mediante el evaluador trivalente existente; no se amplió el vocabulario. Las políticas por campo declaran reglas ordenadas y efecto `REQUIRED`, `OPTIONAL` o `FORBIDDEN`. El evaluador consume filas CSV, conserva cadenas vacías como `""`, devuelve `UNKNOWN` cuando falta una cabecera-señal o ninguna regla cubre un dominio declarado; añade trazas por fila. Una condición desconocida no produce finding.

El capability map local queda en 113 `EXECUTABLE_G03`, 4 `PARTIALLY_EXECUTABLE_G03` y 15 `UNRESOLVED_CONDITION`. Persisten los 10 casos `CROSS_STAGE_NOT_G03`, 1 `DEFERRED_FEATURE` y 4 `NO_MACHINE_EXECUTABLE_RULE`; los cuatro gaps de formato permanecen sin regex inferidas. G03 continúa `IN_PROGRESS` y queda `READY_FOR_FULL_REGRESSION = YES_LOCAL`; la regresión completa sigue pendiente y `G03_PUBLICATION = HOLD`. Antes de cierre, revisar si las dos reglas de ventanas inicialmente clasificadas `NO_MACHINE_EXECUTABLE_RULE` pueden aprovechar este modelo de efectos múltiples; translations sigue bajo G04. No se accedió a HOLDOUT ni se publicó.

Pruebas ejecutadas: runtime 5/5, contrato 11/11, G02 10/10 y catálogo/estructura 19/19; `py_compile` y `git diff --check` también pasan. El endpoint oficial devolvió HTTP 403 durante esta tarea; la implementación conserva las expresiones y anclas normalizadas documentadas en este inventario y no afirma una nueva verificación en vivo de la referencia.

## E. Revisión de ownership de las reglas de ventana — 2026-09-30

Se revisaron únicamente `stop_times.txt.start_pickup_drop_off_window` y `stop_times.txt.end_pickup_drop_off_window`, usando las expresiones y anchors ya capturados en este contrato. Sus condiciones de presencia dependen de la presencia de campos de la misma fila (`location_group_id`, `location_id`, el otro extremo de ventana, `arrival_time` y `departure_time`); no comparan los valores horarios ni calculan duración u orden temporal. Esa evaluación de presencia local corresponde a G03_SCHEMA. La comprobación de que ambos valores forman un intervalo válido, su orden, duración o coherencia temporal corresponde a G05_TEMPORAL.

Esta decisión de ownership no normaliza las expresiones normativas pendientes ni acredita ejecución: ambas entradas siguen `NEEDS_REVIEW` / `UNRESOLVED_CONDITION` en el contrato y capability map. No se amplió el runtime ni se promovieron artificialmente a ejecutables. La resolución de su forma normativa exacta queda pendiente de la fuente capturada ya asociada; cualquier futura validación entre valores se mantiene fuera de G03. No se reconstruyó ni reinterpretó normativa nueva.

## F. Regresión previa a revisión — estado local

La suite focalizada G03 pasó 35/35; G02 RuleRegistry, ChangeAttribution, comparación/audit persistence, corpus split/lineage y engine preconditions pasaron en sus comprobaciones dirigidas. El gate GTFS_Lab V1 sintético pasó con todas las fixtures, flujo completo y GIS direccional; M02 trust persistence pasó 21/21 checks; M01, contratos Golden y gates de metadatos split/lineage pasaron. `compileall` de `tools`, `gtfs_lab` y `tests`, `git diff --check` y el gate whitespace pasaron.

La primera ejecución amplia registró 151 PASS y 1 error ambiental en `test_compliance_v1_transition`, porque falta `03_Compliance/databases/transit_compliance.duckdb` en el worktree aislado. La inspección documental confirmó que DuckDB se excluye de Git y debe restaurarse desde backup separado; no existe una reconstrucción del estado congelado exacto demostrada aquí. El test ahora declara explícitamente el contrato: si la DB falta, se marca `skipped`; si está presente, debe coincidir con el SHA-256 congelado `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` antes de iniciar el replay. La repetición de `unittest discover -s tests -q` finalizó con 152 tests, 151 PASS y 1 SKIP esperado. Así, la revisión técnica G03 puede comenzar (`G03_READY_FOR_REVIEW = YES_LOCAL`); el replay de integración Compliance no se ejecutó. La publicación sigue HOLD; no se ejecutó HOLDOUT.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
