# G03 — paquete de revisión técnica formal (2026-09-30)

**Veredicto técnico:** `G03_REVIEW_CHANGES_REQUIRED`<br>
**Estado de G03:** `IN_PROGRESS`<br>
**Publicación:** `HOLD`<br>
**HOLDOUT:** `NOT_EXECUTED`

Este informe revisa el worktree completo frente a la base indicada. No crea commit ni publica cambios. El propio informe se añade después del inventario y queda fuera de los 11 archivos candidatos revisados.

## A. Base exacta

`36259cdbbc42cc6d2958ce4bd21e5279e7c1657c` (`main` remoto al iniciar la revisión). `HEAD` del worktree G03 coincide exactamente con esta base. No hay commits G03 encima de ella.

## B. Estado del worktree

Worktree aislado: `C:\Users\yeiso\AppData\Local\Temp\tdl-gtfs-engine-g03`<br>
Rama: `feat/gtfs-engine-g03-structure-schema-types`.<br>
Estado inicial: cuatro archivos modificados y siete sin seguimiento; no había cambios staged. El checkout raíz está en otra revisión y su estado local se preservó.

## C. Inventario completo de cambios candidatos

13 archivos (4 modificados, 9 nuevos):

- `02_Data_Engineering/GTFS_Lab/gtfs_lab/pipeline.py` (modificado)
- `02_Data_Engineering/GTFS_Lab/tests/test_compliance_v1_transition.py` (modificado)
- `03_Compliance/TEST_BASELINE_POLICY.md` (modificado)
- `PROJECT_STATUS.md` (modificado)
- `02_Data_Engineering/GTFS_Lab/gtfs_lab/g03_condition_runtime.py` (nuevo)
- `02_Data_Engineering/GTFS_Lab/gtfs_lab/g03_field_contract.py` (nuevo)
- `02_Data_Engineering/GTFS_Lab/gtfs_lab/g03_structure.py` (nuevo)
- `02_Data_Engineering/GTFS_Lab/reports/TDL_GTFS_AUDIT_ENGINE_G03_NORMATIVE_GAP_BURN_DOWN_20260930.md` (nuevo)
- `02_Data_Engineering/GTFS_Lab/spec/gtfs_schedule_field_capability_map_2026_04_27.json` (nuevo)
- `02_Data_Engineering/GTFS_Lab/spec/gtfs_schedule_fields_2026_04_27.json` (nuevo)
- `02_Data_Engineering/GTFS_Lab/tests/test_g03_condition_runtime.py` (nuevo)
- `02_Data_Engineering/GTFS_Lab/tests/test_g03_field_contract.py` (nuevo)
- `02_Data_Engineering/GTFS_Lab/tests/test_g03_file_catalog.py` (nuevo)

## D. Diff y tamaño

El diff ordinario contra la base informa 71 inserciones y 9 eliminaciones en los cuatro paths versionados modificados; no cuenta los nueve paths nuevos hasta que se añadan al índice. `git diff --check` pasó. No se generó ni se normalizó ningún artefacto histórico.

## E. Cambios arquitectónicos

G03 añade un preflight de ZIP aditivo al pipeline. El catálogo G01 se carga desde su JSON versionado; el catálogo, estructura CSV, presencia, cabeceras, restricciones y tipos/formatos se serializan bajo `g03` y `g03_file_catalog`, separados de `validation` y sus findings legacy. El runtime de condiciones reutiliza el evaluador trivalente G02.

## F. Delta de RuleRegistry

Seis reglas G03 aparecen en la salida: `GTFS-G03-FILE-CATALOG`, `GTFS-G03-CSV-STRUCTURE`, `GTFS-G03-HEADER-SCHEMA` (1.1.0), `GTFS-G03-FILE-PRESENCE`, `GTFS-G03-FILE-RESTRICTIONS` y `GTFS-G03-FIELD-TYPE`. Las demás son 1.0.0. La rama G03 permanece aditiva; no se eliminan reglas legacy.

## G. Artefactos de especificación

El catálogo G01 declara 32 identidades. El contrato añade 14 archivos y 132 campos `FULL_V1_TECHNICAL`; su validador devuelve `VALIDATED_WITH_METADATA_GAPS`, sin completar cabeceras ni tipos globalmente. SHA-256 local observado del contrato: `64019665C656E33EFA5C35B55B53D46C13EFD25D255542081F8411552975C65F`. SHA-256 local del capability map: `FEE4C71E13914BB40F6061FE5989E21BC5EDE7D16A166EB9C6AFEABE9489D5B4`.

La normalización declara autoridad legal no reclamada, mantiene anclas/localizadores y registra vacíos/condiciones pendientes. La reproducción automatizada del capability map queda bloqueada por el hallazgo R-03.

## H. Capability map

El JSON declara 113 `EXECUTABLE_G03`, 4 `PARTIALLY_EXECUTABLE_G03` y 15 `UNRESOLVED_CONDITION` (132 en total). El runtime valida longitud y esos tres totales, pero en el código revisado no existe generador que vuelva a derivar cada estado desde el contrato y su metadata. Por tanto, los totales se pueden reproducir contando el JSON, pero la clasificación por campo no queda reproducida desde sus fuentes.

## I. Limitaciones abiertas

Persisten 15 condiciones no resueltas, 4 gaps de tipo/formato, política normativa de extensiones no resuelta, semántica de celdas vacías no especificada, ownership posterior G04/G05/G07 y presencia de Flex/calendario parcialmente no evaluable. No se infieren reglas de estas limitaciones.

## J. Solapamiento legacy

El resultado G03 se guarda por separado y su overlap matrix es informativa: required-file, calendario y rangos de coordenadas tienen solapamientos parciales documentados. Referencias e identidad quedan fuera de G03. Las pruebas sintéticas comprueban que findings legacy siguen en `validation`; no se encontró borrado de reglas históricas.

## K. Semántica de resultados

La forma de salida conserva etiquetas distintas (`NOT_EVALUABLE`, `NOT_APPLICABLE`, `FAIL_TECHNICAL`, `INSPECTION_ERROR`) en decisiones/resultados. No obstante, los estados agregados pueden declarar `PASS` con subcasos no evaluables (R-02), y el runtime puede convertir una precedencia incierta en un efecto conocido (R-01). Estos defectos impiden aceptar ahora el contrato semántico agregado.

## L. Matriz de verificación ejecutada

| Comprobación | Resultado |
| --- | --- |
| Tests G03 runtime + contrato + catálogo/estructura | 35/35 PASS |
| Descubrimiento amplio GTFS_Lab (`unittest discover -s tests -p 'test*.py'`) | 152; 151 PASS, 1 SKIP; 0 FAIL |
| `git diff --check` | PASS |
| Revisión manual de pipeline, registry, metadata, resultados y DB | Completada; R-01 a R-03 abiertos |
| HOLDOUT | No ejecutado ni accedido |

La comprobación amplia se ejecutó desde el worktree G03. El SKIP corresponde solo al replay contra la DB Compliance ausente.

## M. Broad discovery

`151 PASS / 1 SKIP / 0 FAIL`; el test de DB omitido declara la precondición ambiental. Este resultado de tests no resuelve los hallazgos de revisión ni cierra G03.

## Remediación de revisión formal

Estado local: `G03_REVIEW_REMEDIATION_PASS`; no implica aprobación humana, cierre, publicación ni inicio de G04.

### Semántica y agregación

- Las reglas de presencia condicional se evalúan por orden. Un `FALSE` posterior no borra un `UNKNOWN`; un `TRUE` posterior e independiente tampoco lo resuelve porque una regla anterior no evaluable podría tener precedencia. Un `TRUE` dentro de la misma expresión compuesta sí puede resolverlo conforme a Kleene: `ALL` es FALSE si algún hijo es FALSE, si no UNKNOWN si algún hijo es UNKNOWN, y TRUE en otro caso; `ANY` es TRUE si algún hijo es TRUE, si no UNKNOWN si algún hijo es UNKNOWN, y FALSE en otro caso; `NOT` conserva UNKNOWN y permuta TRUE/FALSE. El trace conserva el orden de reglas y nodos.
- El agregado nativo conserva prioridad `FAIL_TECHNICAL`, después `INSPECTION_ERROR`, después `NOT_EVALUABLE`; solo devuelve PASS si todos los casos aplicables se evaluaron sin fallo. `NOT_APPLICABLE` se excluye del denominador. `coverage` informa `evaluated_count`, `not_evaluable_count`, `not_applicable_count`, `failed_count`, `total_applicable_count` y `coverage_state` (`FULL`, `PARTIAL`, `NO_APPLICABLE_CASES`). No se añade un nuevo estado PASS.

### Mapa reproducible

`python -m gtfs_lab.g03_capability_map` deriva el mapa ordenado desde el contrato de campos, catálogo G01, metadatos de ownership y SHA del registro runtime. El JSON registra hashes de entradas, conteos derivados, clasificación con razón por campo y digest reproducible del payload. La prueba `test_capability_map_regenerates_byte_for_byte` regenera en memoria y compara los bytes con el artefacto.

Evidencia de esta remediación: mapa SHA-256 `0805373D4F934CF68A2BAE965670CB7A066937A2EC761B199EFF1A06D1ABF41A`; contrato `64019665C656E33EFA5C35B55B53D46C13EFD25D255542081F8411552975C65F`; registro runtime `7EE25E06D16CD7140AA3103DACE929208EDAE89752D44D5BD4C6F9A6E8E178A7`; catálogo `366A9CADDE04E3E2E5980FD02ACD3C9FBDA49766CC9C8E0AD7AD696F1EC712F8`.

### Regresión de remediación

Descubrimiento amplio: 164 pruebas, 163 PASS, 1 SKIP esperado (DB Compliance externa ausente), 0 FAIL/ERROR. El aumento desde 152 se debe a las pruebas añadidas. Los grupos solicitados pasan: G03 47; G02 registry 10; ChangeAttribution 1.0 16; ChangeAttribution 1.1/preconditions 10; audit comparison 23; split 23; lineage 6. Persistencia M02 y trust contract PASS; gate de corpus Golden PASS; GTFS_Lab V1 sintético PASS con E2E y GIS direccional; `compileall` PASS. El split/lineage se comprobó solo con metadatos.

`git diff --check` se ejecutó. El gate de whitespace no pasa de forma interpretable porque `git diff --check` emite un aviso CRLF relativo al cambio previo de `PROJECT_STATUS.md` en este worktree; no señala líneas con whitespace y no se alteró ese cambio ajeno. Por ello el requisito global de whitespace queda pendiente de una ejecución limpia del gate.

No se accedió a HOLDOUT, no se ejecutó G04+, no se publicó ni se creó commit.

## N. Contrato del artefacto DB protegido

El test comprueba ausencia y hace `skipTest` si falta `transit_compliance.duckdb`. Si existe, lee los bytes en modo binario para calcular SHA-256 `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`; solo tras coincidir llama a `build_candidate()`. Las importaciones revisadas declaran rutas/funciones, pero no conectan ni consultan DuckDB. La llamada de replay actual tampoco usa esa DB; el guard de identidad queda antes del generador. En esta ejecución no se encontró la DB, por lo que el replay protegido no se realizó. El contrato ambiental queda resuelto como `ausente → SKIP; presente con SHA correcto → replay; presente con SHA incorrecto → FAIL`.

## O. HOLDOUT

`HOLDOUT_REPLAY = NOT_EXECUTED`. No se leyó contenido ni se usó como fixture.

## P. Contenido candidato a commit

Los 13 paths de C son el conjunto de cambios funcionales/documentales visto al inicio de la revisión. Ninguno está staged ni committed. Este bundle se añadió posteriormente y está expresamente fuera del candidato; no se realizó commit, push ni publicación.

## Q. Hallazgos y riesgos

### R-01 — Precedencia de política pierde `UNKNOWN` (alto)

En `evaluate_presence_policy`, una regla inicial `UNKNOWN` solo marca una bandera y la iteración continúa; si una regla posterior es `TRUE`, devuelve su efecto sin conservar que una regla anterior podría tener precedencia. Probe reproducible con regla 1 `FORBIDDEN` sobre señal ausente y regla 2 `REQUIRED` sobre señal verdadera: salida actual `truth=TRUE, effect=REQUIRED`. Esto puede convertir `UNKNOWN` accidentalmente en una decisión ejecutable. Resolver la incertidumbre de precedencia o demostrar que el contrato define otra prioridad; añadir caso de regresión.

### R-02 — Agregados `PASS` con trabajo no evaluable (alto)

`_evaluate_schema` devuelve `PASS` cuando hay cualquier decisión y ningún finding, aun si `not_evaluable` contiene casos. Probe sintético observado: `header_schema.status=PASS` con `header_schema.not_evaluable` de longitud 1. `_evaluate_types` aplica patrón similar: si comprobó algún valor, devuelve `PASS` aunque `not_evaluable` no esté vacío. Un consumidor que lea el estado agregado puede entenderlo como cobertura completa. El estado debe reflejar los casos no evaluables o exponer un agregado explícitamente parcial sin colapsar estados por finding.

### R-03 — Capability map no reproducible por campo (alto)

`_load_capability_map()` valida que haya 132 filas y que los totales sean exactamente 113/4/15; no recalcula ni compara cada clasificación con el contrato. El code search no encontró generador del JSON. El artefacto incluye methodology y hashes, pero esas declaraciones no prueban que sus estados por campo se deriven de manera reproducible. Añadir un generador/validador que derive la clasificación y compare el artefacto byte a byte, o retirar la afirmación de reproducibilidad.

### Conclusión de revisión

Los tres hallazgos afectan directamente a los riesgos 2, 3 y 4 expresados para esta revisión. Por ello el veredicto es `G03_REVIEW_CHANGES_REQUIRED`. Los riesgos de contrato normativo, solapamiento legacy y guard de DB no mostraron bloqueo en la evidencia inspeccionada, dentro de los límites indicados. Este PASS parcial de revisión no equivale a cierre técnico ni aprobación humana.

## R. Decisión solicitada

Revisión técnica recomienda corregir R-01, R-02 y R-03 y volver a ejecutar regresión antes de solicitar `G03_REVIEW_PASS`. Hasta entonces: `G03 = IN_PROGRESS`, `G03_PUBLICATION = HOLD`; no commit, push ni cierre.

## S. Addendum — remediación y preparación de publicación

El estado siguiente conserva las secciones Q–R como evidencia de la revisión inicial; no las reescribe. Tras la remediación, la verificación local autorizada confirmó `G03_REVIEW_REMEDIATION = PASS_LOCAL`, `G03_FORMAL_REVIEW = PASS_LOCAL` y `G03_READY_FOR_PUBLICATION = YES`. `G03` permanece `IN_PROGRESS`; la autorización cubre preparación, no commit ni publicación.

Regeneración determinista: `python -m gtfs_lab.g03_capability_map`; SHA-256 del mapa: `0805373D4F934CF68A2BAE965670CB7A066937A2EC761B199EFF1A06D1ABF41A`.

Descubrimiento amplio: 164 pruebas, 163 PASS, 1 SKIP esperado y 0 FAIL/ERROR. El único skip es el replay de transición Compliance, condicionado a la DB protegida ausente. Gates focalizados: G03 47; G02 RuleRegistry 10; ChangeAttribution 1.0 16; ChangeAttribution 1.1/precondiciones 10; comparación 23; split 23; lineage 6; provenance 7. Trust Contract, M02 persistencia (21 checks), Golden Contract (18), Golden Evaluator (11), Golden Corpus, GTFS_Lab V1 sintético/E2E/GIS direccional, `compileall`, `git diff --check` y strict whitespace: PASS. El split/lineage usa solo metadatos. El gate estricto se ejecutó con `core.safecrlf=false` limitado al proceso para evitar que una advertencia de conversión CRLF oscurezca el resultado; no se encontraron violaciones.

No se accedió a HOLDOUT ni a una base protegida; no se inició G04+, ni se hizo commit o publicación.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
