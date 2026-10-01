# GTFS Audit Engine V1 — G11 final closure decision

**Estado vigente (2026-10-01):** Yeison aprobó expresamente la decisión humana final G11. G08–G11 y GTFS Audit Engine V1 quedan `PASS / CLOSED` para el alcance técnico documentado. PR #29 se integró mediante merge normal en `d5c770d5015faa856963a363e14da24124da5a12`; CI post-merge PASS, run `36809106494`. Esta decisión acepta los gaps y deferrals descritos aquí sin ampliación de cobertura.
**Authoritative development base:** `89b199f1ffa114922047113a8460e2933cfa60f8`.
**Specification revision:** GTFS Schedule `2026-04-27`.

## Stage disposition

| Stage | Scope and evidence | Current disposition |
|---|---|---|
| G01 | Frozen inventory of 32 official GTFS Schedule files and their support classification. | CLOSED on `main`; 14 files in full/conditional technical support, 18 deferred. |
| G02 | Typed `RuleDefinition`, native statuses, rule identity/version and authority/severity/requirement contracts. | CLOSED on `main`; unchanged. |
| G03 | Archive inventory, CSV structure, header schema and file presence, executable field types and formats. | CLOSED; bounded-evidence fix integrated in PR #28 and post-merge CI passed. Capability map: 106 executable, 11 partial, 15 unresolved; extension policy remains unresolved. |
| G04 | Four identity/referential rules: primary-key uniqueness, populated-reference existence, identity-domain resolution, and contextual translations references. | CLOSED; two-table bounded cache fix integrated in PR #28 and post-merge CI passed. Identity inventory remains `CREATED_LOCAL_UNPUBLISHED`, a known contract debt. |
| G05 | Five calendar/temporal rules. | CLOSED on `main`; regression included. |
| G06 | Three stop sequence and operational rules. | CLOSED on `main`; regression included. |
| G07 | Three shapes/spatial rules. | CLOSED on `main`; regression included. |
| G08 | Three `feed_info.txt` declaration recommendations, typed through G02 and separate from conformance. | PR #28 merged; synthetic suite passes. Technical acceptance is recorded in this remediation. |
| G09 | Deterministic machine and human report of independent G03–G08 results. | PR #28 merged; synthetic suite passes. Technical acceptance is recorded; M02 is unchanged and does not register the supplemental report. |
| G10 | Reproducible full pipeline over only the 14 DEVELOPMENT sources; per-dataset outcomes, findings, limitations, evaluability and stability check. | Recovery replay completed 14/14, zero pipeline errors, stability PASS. The replay preserves bounded G03 reason counts, file statuses, per-rule coverage and a separate evaluability attribution. HOLDOUT was not accessed. |
| G11 | Technical closure gate and final human closure decision for the documented V1 scope. | PASS / CLOSED; final human decision APPROVED on 2026-10-01. |

La candidatura machine-readable está en [g11_closure_candidate.json](evidence/g11_closure_candidate.json). El replay está en [G10 recovery](evidence/g10_development/g10_development_recovery_20261001.json); cobertura y causas por regla/dataset, en [G10 evaluability attribution](evidence/g10_development/g10_evaluability_attribution_20261001.json). El artefacto histórico de PR #28 se conserva.

## Qué audita V1

V1 identifica y ejecuta reglas técnicas declaradas sobre GTFS Schedule, revisión `2026-04-27`. Los archivos con soporte técnico V1 son: `agency.txt`, `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, `calendar.txt`, `calendar_dates.txt`, `shapes.txt`, `frequencies.txt`, `transfers.txt`, `pathways.txt`, `levels.txt`, `translations.txt` y `feed_info.txt`. Incluye estructura CSV, presencia/condiciones declaradas y los campos para los que el capability map permite evaluación. Este mapa registra 106 evaluaciones ejecutables G03, 11 parciales y 15 condiciones sin resolver. G04 audita claves, dominios de identidad y referencias según su inventario; G05 audita cinco reglas temporales; G06, tres reglas de secuencia/operación; G07, tres reglas de secuencia/espacio; G08 solo declara tres recomendaciones de `feed_info.txt`. El pipeline registra cada etapa por separado. G09 permite revisar estado, versión de regla, authority, severity, findings, coverage, recomendaciones y limitaciones en JSON y Markdown.

El validador legacy sigue ejecutándose y mantiene su propia salida. G03–G09 se presentan como etapas independientes; no se afirma equivalencia total ni se incorporan sus findings a `validation.findings` o al normalizador M02.

## Qué no audita V1

- Los 18 archivos oficiales diferidos en G01 no reciben auditoría completa: `fare_attributes.txt`, `fare_rules.txt`, `timeframes.txt`, `rider_categories.txt`, `fare_media.txt`, `fare_products.txt`, `fare_leg_rules.txt`, `fare_leg_join_rules.txt`, `fare_transfer_rules.txt`, `areas.txt`, `stop_areas.txt`, `networks.txt`, `route_networks.txt`, `location_groups.txt`, `location_group_stops.txt`, `locations.geojson`, `booking_rules.txt` y `attributions.txt`. G03 puede reconocer su identidad/presencia sin declarar que sus reglas estén implementadas.
- G03 no resuelve las 15 condiciones aún no ejecutables, la política normativa de extensiones ni semánticas de valores vacíos no definidas. Los resultados dependientes de evidencia insuficiente permanecen `NOT_EVALUABLE`.
- G04 depende del inventario de identidad/referencias local y no publicado; permanece la deuda `CREATED_LOCAL_UNPUBLISHED`.
- G08 no evalúa valores, relevancia para un feed ni calidad integral del servicio: solo observa presencia de cabecera para `feed_start_date`, `feed_end_date` y `feed_version`.
- G09 es suplementario; su JSON/Markdown reproducible no está registrado ni firmado por M02. La persistencia de los findings G03–G09 queda fuera de este cambio.
- El corpus G10 es DEVELOPMENT. HOLDOUT no forma parte de esta evaluación ni de sus resultados.
- GTFS-RT, SIRI, NeTEx y otros feeds/modelos quedan fuera del producto V1 declarado aquí.
- No determina cumplimiento jurídico, certificación, validez comercial, demanda, readiness de mercado ni cumplimiento completo de GTFS.

La inspección del runtime G03–G10 no encontró ramas condicionadas por operador ni código añadido por dataset. El finding observado en `010 / agency.txt / agency_url` (`empresarodil.es` sin esquema) permanece como finding técnico; no se añadió una excepción específica.

## Evidencia, evaluabilidad y gate G11

La recuperación localizó los 14 ZIP DEVELOPMENT bajo el `20_clientes_reales` del checkout raíz. Se verificaron con SHA-256 contra inventario y split, y se copiaron solo esos 14 a un source root temporal externo a Git. El replay volvió a comprobar los hashes antes de abrirlos. Resultado: `DEVELOPMENT_SOURCE_RECOVERY = 14/14`, `ALL_SHA256_MATCH = YES`, `zero pipeline errors`, replay de estabilidad del dataset `001` PASS (`engine_report_sha256 = 51a2c5b0125fb2582839e8889e6a2780d39d571de3d5d0ebe58e37f6bb3a8371`), `HOLDOUT_ACCESSED = NO`.

La revisión detectó un bug de integración: G03 publica la evidencia CSV por archivo como `files_inspected`, pero G04–G07 consultaban `inspected`. Los consumidores marcaban ausente evidencia presente y propagaban `NOT_EVALUABLE`. Se corrigió el contrato de lectura y se añadió regresión. También se acotó la incertidumbre G03 de G05–G07 a los campos que cada regla consume, evitando que gaps de `feed_lang`/correo bloqueen evaluaciones de fechas de feed.

### Cobertura observada en DEVELOPMENT

- **G04:** identidad de servicio, 32.002 evaluaciones (13 datasets PASS, un dataset con finding técnico); unicidad de claves, 102 evaluaciones y 80 no aplicables; referencias, 1.168.910 evaluaciones, 83 no evaluables y 158 no aplicables. Las 83 no evaluables reconcilian con campos fuente opcionales/condicionales ausentes de cabeceras. El finding de `011` conserva las referencias `service_id` sin resolver en `calendar_dates.txt`/`trips.txt`.
- **G05:** 417 rangos de calendario evaluados y 13/14 sets de fechas evaluados. En `011`, el set depende del dominio G04 no resuelto. El rango `feed_info` evaluó seis; siete feeds no tienen el archivo y `016` carece de un valor de fecha de periodo. Las reglas de frecuencias no aplican a los 14; las cabeceras de ventanas pickup/drop-off no aparecen.
- **G06:** secuencia de parada evaluada en 558.810 filas y PASS en 14/14. El orden temporal entre paradas permanece `NOT_EVALUABLE` por `DEFERRED_BY_SCOPE`: la referencia fijada no declara un MUST de monotonía. Las reglas de frecuencia no aplican a los 14.
- **G07:** nueve feeds PASS, cuatro no aplicables y un feed con finding técnico de progresión de distancia; findings limitados y sin valores observados en el artefacto.
- **G08/G09:** integración PR #28 y suites sintéticas PASS. Sus cierres técnicos se registran separadamente; M02 no registra el reporte suplementario G09.
- **G10:** 14/14 pipelines completados, errores cero y estabilidad PASS. No se usan thresholds inventados. La cobertura real queda como conteos PASS/FAIL/N/E/N/A, no como score agregado.

La evidencia G03 agrupa por dataset, archivo, campo y código con recuentos completos y muestras limitadas. Conserva los gaps `CONDITION_UNKNOWN`, `UNRESOLVED_CONDITION`, `UNRESOLVED_EXTENSION_POLICY`, `UNRESOLVED_TYPE_FORMAT` y `UNSUPPORTED_LEXICAL_VALIDATOR`. No incluye valores observados de los feeds. La atribución separada reconcilia las 83 ausencias de campos fuente G04; clasifica la dependencia G04→G05 de `011`, el campo de fecha vacío de `016`, las features no presentes y el deferral G06.

### Generalización y límites

No se encontró lógica específica por operador o dataset: `operator_specific_code_changes = false`. El finding observado en `010 / agency.txt / agency_url` se conserva como finding técnico, sin excepción por operador.

V1 cubre solo los archivos y campos declarados en su perfil técnico. No resuelve las 15 condiciones G03 pendientes, la política normativa de extensiones ni semánticas no especificadas de valores vacíos. Los 18 archivos diferidos en G01 no reciben auditoría completa. El inventario G04 sigue `CREATED_LOCAL_UNPUBLISHED`. El flujo legacy sigue produciendo su propia salida; G03–G09 no se copian a `validation.findings`, M02 no los normaliza y G09 no está registrado ni firmado por M02. Esto no declara equivalencia total con legacy, cumplimiento GTFS completo, cumplimiento jurídico, certificación, validación comercial, demanda, readiness de mercado, NeTEx/SIRI ni GTFS-RT.

`M02 = PASS` y los límites de identidad/legacy se mantienen como fronteras; los cierres Business y Compliance no se alteran. `HOLDOUT = NOT_ACCESSED`.

## Decisión humana final y cierre

```ini
G11_HUMAN_CLOSURE_DECISION = APPROVED
G11 = PASS
G11_CLOSED = YES
GTFS_AUDIT_ENGINE_V1 = PASS
GTFS_AUDIT_ENGINE_V1_CLOSED = YES
GTFS_AUDIT_ENGINE_V1_CLOSURE_DATE = 2026-10-01
PR29_MERGE_COMMIT = d5c770d5015faa856963a363e14da24124da5a12
POST_MERGE_CI_RUN = 36809106494
POST_MERGE_CI = PASS
HOLDOUT = NOT_ACCESSED
M02_CHANGED = NO
OPERATOR_SPECIFIC_CODE = NO
GTFS_COMPLETE_COVERAGE = NOT_CLAIMED
LEGAL_COMPLIANCE = NOT_CLAIMED
COMMERCIAL_VALIDATION = NOT_CLAIMED
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.


## Verificación de integración PR #29 — 2026-10-01

PR #29 se fusionó mediante **merge normal** después de revisión aprobada. Head revisado: `44e92012b1ab8a27b232b69154abc043c55d21e8`; merge commit y `origin/main`: `d5c770d5015faa856963a363e14da24124da5a12`. CI pre-merge PASS, run `36808289990`; CI post-merge PASS sobre el merge commit, run `36809106494`.

Con esta integración quedan registrados `G08 = PASS / CLOSED`, `G09 = PASS / CLOSED` y `G10 = PASS / CLOSED`. `G11_TECHNICAL_REVIEW = PASS`. El replay DEVELOPMENT permanece 14/14, cero errores y estabilidad PASS; HOLDOUT no se accedió. No hubo cambios M02 ni código específico por operador.

La evaluabilidad observada G03–G08, sin umbrales inventados, fue: G03, 106 ejecutables / 11 parciales / 15 condiciones sin resolver; G04, 32.002 evaluaciones de dominio (13 PASS, un finding), 102 de unicidad (80 N/A) y 1.168.910 referencias (83 N/E, 158 N/A); G05, 417 rangos calendario, 13/14 conjuntos de fechas evaluables y rango de feed 6 PASS / 7 N/A / 1 N/E; G06, 558.810 filas de secuencia PASS y orden temporal 14 N/E por deferral; G07, 9 PASS / 4 N/A / 1 finding; G08, 7 PASS / 7 N/A para tres recomendaciones de presencia.

Siguen abiertos como gaps conocidos las 15 condiciones G03, los estados `CONDITION_UNKNOWN`, `UNRESOLVED_CONDITION`, `UNRESOLVED_EXTENSION_POLICY`, `UNRESOLVED_TYPE_FORMAT` y `UNSUPPORTED_LEXICAL_VALIDATOR`, la política de extensiones y el inventario G04 `CREATED_LOCAL_UNPUBLISHED`. Se difieren los 18 archivos enumerados en la sección «Qué no audita V1»; GTFS-RT, SIRI y NeTEx quedan fuera. M02 no incorpora findings G03–G09 ni registra el reporte suplementario G09; legacy conserva salida independiente y no se afirma equivalencia total.

La decisión cierra técnicamente el alcance V1 documentado. `pending_gates` queda vacío para Engine V1. No se inicia ningún track posterior. Los gaps y deferrals listados en este informe siguen siendo límites aceptados de V1; este PASS no implica cobertura GTFS completa, cumplimiento jurídico, certificación, validación comercial ni readiness de otros formatos.
