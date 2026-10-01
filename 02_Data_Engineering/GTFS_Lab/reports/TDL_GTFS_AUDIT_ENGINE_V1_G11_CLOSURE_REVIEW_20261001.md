# GTFS Audit Engine V1 — G11 candidate closure review

**Status:** PR #28 head `39fd2aa052b4c6fb1f2637d11e7db2e7dd41be6a`; remote CI PASS (run 36803441534); merge pending; post-merge verification pending; final human G11 decision pending.
**Authoritative development base:** `89b199f1ffa114922047113a8460e2933cfa60f8`.
**Specification revision:** GTFS Schedule `2026-04-27`.

## Stage disposition

| Stage | Scope and evidence | Current disposition |
|---|---|---|
| G01 | Frozen inventory of 32 official GTFS Schedule files and their support classification. | CLOSED on `main`; 14 files in full/conditional technical support, 18 deferred. |
| G02 | Typed `RuleDefinition`, native statuses, rule identity/version and authority/severity/requirement contracts. | CLOSED on `main`; unchanged. |
| G03 | Archive inventory, CSV structure, header schema and file presence, executable field types and formats. | Existing baseline CLOSED; local bounded-evidence fix is regression-tested and awaits merge. Capability map: 106 executable, 11 partial, 15 unresolved; extension policy remains unresolved. |
| G04 | Four identity/referential rules: primary-key uniqueness, populated-reference existence, identity-domain resolution, and contextual translations references. | Existing baseline CLOSED; local two-table LRU fix preserves output and awaits merge. Identity inventory remains `CREATED_LOCAL_UNPUBLISHED`, a known contract debt. |
| G05 | Five calendar/temporal rules. | CLOSED on `main`; regression included. |
| G06 | Three stop sequence and operational rules. | CLOSED on `main`; regression included. |
| G07 | Three shapes/spatial rules. | CLOSED on `main`; regression included. |
| G08 | Three `feed_info.txt` declaration recommendations, typed through G02 and separate from conformance. | Local implementation and E2E evidence complete; awaiting merge/post-merge gate. |
| G09 | Deterministic machine and human report of independent G03–G08 results. | Local implementation and synthetic partial/deferred/recommendation evidence complete; awaiting merge/post-merge gate. M02 is unchanged and does not register the supplemental report. |
| G10 | Reproducible full pipeline over only the 14 DEVELOPMENT sources; per-dataset outcomes, findings, limitations, and stability check. | Local run complete: 14 completed, zero pipeline errors, stability PASS; awaiting merge/post-merge gate. HOLDOUT was not accessed. |

The machine-readable candidate state is in [g11_closure_candidate.json](evidence/g11_closure_candidate.json). Detailed G08–G10 execution and corpus results are in [the local progress record](TDL_GTFS_AUDIT_ENGINE_G08_G10_LOCAL_PROGRESS_20261001.md) and [the G10 result artifact](evidence/g10_development/g10_development_results.json).

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

## Evidencia y puertas pendientes

La evaluación G10 verificó SHA-256 del split y de cada fuente DEVELOPMENT antes de uso, terminó 14 pipelines, registró las diferencias por regla/etapa y repitió el dataset `001` con el mismo SHA-256 de `engine_report.json`. Cada hash de informe por dataset se conserva en la evidencia; el replay de estabilidad comparó el dataset `001`. Los datos de G10 no contienen salida de HOLDOUT.

El HEAD autorizado de PR #28 es `39fd2aa052b4c6fb1f2637d11e7db2e7dd41be6a`; CI remoto PASS (run `36803441534`). Merge y verificación post-merge siguen pendientes. Tras el merge se repetirá el gate, se verificará `origin/main` y se actualizarán los estados. La decisión humana final G11 queda separada del PASS técnico/CI.

## Afirmaciones expresamente excluidas

Este informe no declara cumplimiento GTFS completo, cumplimiento jurídico, certificación, market validation, readiness comercial, NeTEx complete readiness, SIRI readiness, ni resultados de HOLDOUT.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## DEVELOPMENT G04–G06 evaluability

G10 completed 14/14 DEVELOPMENT pipelines with zero pipeline errors. However, G04, G05 and G06 each reported NOT_EVALUABLE at stage level for all 14 datasets. This is a coverage/evidence outcome, not a pipeline failure or a PASS. Rule-level counts and the missing upstream evidence are recorded in the accompanying G10 report; G10 must expose stage and rule evaluability separately from execution completion. The final G11 decision remains pending.
