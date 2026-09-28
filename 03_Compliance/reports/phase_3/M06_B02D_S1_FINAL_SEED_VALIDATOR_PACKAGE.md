# M06-B02D-S1 Final Seed & Validator Package

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Human authorization basis

Se aplica la decisión humana de esta misión: C01 limitado a siete categorías DATEX y C07 limitado a SIRI-ET/SIRI-SX. Se autoriza preparar los datos para una futura revisión de ejecución. `SEED_EXECUTION = NO`; no se ejecutaron seeds ni se escribió en la base.

La misión autoriza reviews `ACCEPTED_WITH_LIMITATIONS`. Este resultado se almacena en `phase3_mapping_reviews.semantic_review_outcome`; `phase3_requirement_capabilities.review_status` conserva el workflow `NEEDS_REVIEW`. El vocabulario real contiene `ACCEPTED_WITH_LIMITATIONS`.

## Approved subset

Paquete diseñado para 9 capabilities, 9 mappings PARTIAL, 9 reviews semánticas, 9 concept bridges, 9 unidades INCLUDED, 9 source references y 9 enlaces scope-source. DATEX C01 = 7; SIRI C07 = 2.

## Excluded/held subset

C04 entero permanece HOLD por Article 5(2). C08 entero permanece HOLD. Se excluyen DATEX 5-SN-D, SIRI-CM, SIRI-VM, U01/U02/U03 y C02/C03/C05/C06. No se preparan coverage, representability, observed evidence, automatability ni audit rules.

## Current authoritative DB state

Base: `03_Compliance/databases/transit_compliance.duckdb`, consultada con DuckDB `-readonly`.

| Dato | Estado precheck |
|---|---:|
| Requirements | 48 |
| Concepts B02 | 7 |
| Mappings globales | 6 |
| Mappings B02 | 0 |
| Bridges B02 | 0 |
| Scope units B02 | 0 |
| Scope-source links B02 | 0 |
| Coverage B02 | 0 |
| Representability sustantiva | 0 |
| Observed evidence sustantiva | 0 |
| `audit.rules` | 0 |

M06-B02C schema = ACTIVE; M06-B02A concepts = CHECKPOINTED. SHA-256 antes y después de las comprobaciones: `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`, coincidente con el valor indicado en la misión.

## Seed files

Todos llevan `FINAL SEED — NOT AUTHORIZED FOR EXECUTION`:

- `03_Compliance/sql/03_mappings/phase3_m06_b02d_capabilities_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_source_references_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_mappings_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_mapping_reviews_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_concept_bridges_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_scope_units_seed.sql`
- `03_Compliance/sql/03_mappings/phase3_m06_b02d_scope_source_refs_seed.sql`

El registro `M06-B02D-SIRI-EPIPRT-2025` se incluye como prerequisito de identidad para la FK de las capabilities SIRI. Está marcado `IDENTITY_ONLY`; refleja EPIP-RT CEN/TS 15531-7:2025 y SIRI 2.1, sin promover su crosswalk.

## Execution dependency order

En una futura operación atómica, integrar los SQL como una única transacción y respetar estas dependencias reales: identidad estándar y capabilities → source references → mappings → reviews → bridges → scope units → scope-source links → postchecks → COMMIT. Ejecutar `ROLLBACK` ante cualquier error o fallo. Los SQL preparados no se han ejecutado ni probado contra escrituras.

## Capability package

DATEX utiliza el estándar ya presente `M03-DATEXII-MMTIS-RRP`, con alcance acotado a cada RRP RTTI 670/2022. No se afirma versión 3.7: `profile-specific model release unresolved`. SIRI usa la identidad EPIP-RT/SIRI 2.1 arriba descrita. Las nueve capabilities tienen limitaciones explícitas; ninguna afirma cobertura jurídica, representability del dataset u observación de implementación.

## Mapping package

IDs: `M06-B02-MAP-A05-P01-002-DATEX-{4-SN-A,4-SN-B,4-SN-C,4-SN-D,5-SN-A,5-SN-B,5-SN-C}` y `M06-B02-MAP-A05-P02-001-SIRI-{ET,SX}`. Todos son `PARTIAL`, con condiciones y limitaciones específicas.

## Review package

Nueve filas `ACCEPTED_WITH_LIMITATIONS`, con justificación, límites, reviewer Yeison Arbey Carrillo Lemus y fecha de decisión 2026-09-28. El outcome semántico no se escribe en el campo workflow.

## Concept bridge package

Siete mappings C01 enlazan exclusivamente con `M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION`; dos mappings C07 con `M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION`. Cada concept y mapping comparte requirement.

## Scope package

Siete unidades DATEX (`ROAD_CLOSURE`, `LANE_CLOSURE`, `ROADWORKS`, `TEMP_TRAFFIC_MGMT`, `BRIDGE_CLOSURE`, `ACCIDENT_INCIDENT`, `POOR_ROAD_CONDITION`) y dos SIRI (`JOURNEY_DELAY_CANCELLATION`, `PASSENGER_DISRUPTION_NOTICE`), todas `INCLUDED`, con decisión humana y limitación. No se proponen unidades unresolved/excluded.

## Source-reference package

Siete fuentes category-specific DATEX y dos vistas de servicio SIRI. Cada unidad enlaza a la fuente de su capability exacta, con rol `SUPPORT`; no se reutilizan fuentes genéricas. Los perfiles DATEX conservan RTTI 670/2022 y release individual sin resolver. SIRI mantiene `exact Annex→element/constraint crosswalk remains partial`.

## Preflight validator

`03_Compliance/sql/07_tests/phase_3/validate_phase_3_m06_b02d_s1_preflight.sql`, solo lectura. Comprueba IDs objetivo ausentes, estado esperado, requirements/concepts, estándar DATEX presente, vocabulario y capas protegidas. Ejecutado con DuckDB `-readonly`: **PASS**, 15 checks, 0 fallos.

## Post-write validator

`03_Compliance/sql/07_tests/phase_3/validate_phase_3_m06_b02d_s1.sql`, solo lectura; diseñado para verificar conteos 9/9/9/9/9/9/9, PARTIAL, outcome semántico, bridge-requirement alignment, 9 INCLUDED, enlaces a source/capability, exclusiones, legacy, capas protegidas y Phase 1/2. No se ejecutó sobre el estado vacío porque sus conteos describen el futuro estado persistido.

## Expected deltas

| Tabla/capa | Delta esperado tras futura autorización |
|---|---:|
| Capabilities | +9 |
| Mappings | +9 |
| Reviews | +9 |
| Concept bridges | +9 |
| Scope units | +9 |
| Source references | +9 |
| Scope-source links | +9 |
| Coverage | 0 |
| Representability | 0 |
| Observed evidence | 0 |
| Automatability | 0 |
| `audit.rules` | 0 |

## Protected invariants

Phase 1 (92 provisions, 36 source facts), Phase 2 (48 requirements, 10 deadlines), los seis mappings legacy y las capas de coverage/representability/observed evidence/automatability/audit rules quedan sin cambios. SHA-256 antes/después idéntico; `DB_WRITES = 0`.

## Idempotence strategy

**Pendiente antes de declarar el paquete listo.** Los seeds actuales contienen guardas de ausencia y abortan si encuentran IDs ya existentes, pero aún no comparan cada fila completa para omitir una coincidencia exacta. Esa guarda evita duplicación/conflicto, aunque no satisface el contrato solicitado de idempotencia fila a fila. No ejecutar los seeds hasta añadir comparación exacta, inserción selectiva de ausentes y aborto de diferencias; después comprobar primera ejecución y segunda ejecución de delta semántico cero en un fixture aislado autorizado.

## Rollback strategy

La futura integración debe envolver los siete seeds y postchecks en una sola transacción. Ante conflicto, error de constraint o postcheck fallido, hacer `ROLLBACK`; nunca dejar un B02 parcialmente persistido. No se ha ensayado la transacción.

## Coverage exclusion

`B02_COVERAGE_PERSISTENCE = NOT_AUTHORIZED`. No se crea seed de coverage.

## Representability exclusion

`B02_REPRESENTABILITY_PERSISTENCE = NOT_AUTHORIZED`. Las nueve scope units son candidatas para revisión separada posterior.

## Risks

- La autorización de preparar no equivale a autorización de ejecutar.
- El diseño row-by-row idempotente todavía está incompleto según se indica arriba.
- Identidad de perfil no demuestra release de modelo DATEX, crosswalk completo SIRI, cobertura jurídica, representability ni implementación observada.
- El paquete de persistencia anterior describe un conjunto mayor y no sustituye esta decisión aprobada posterior.

## Execution authorization still required

Sí. `B02_PARTIAL_MAPPING_PERSISTENCE = NOT_AUTHORIZED`. Además, completar y revisar el contrato de idempotencia antes de considerar los seeds aptos para ejecución.

## Estado

`M06_B02D_S1_SEED_PACKAGE = INCOMPLETE — IDEMPOTENCE GUARD REQUIRED`. No se actualiza `PROJECT_STATUS.md` a `READY_FOR_EXECUTION_REVIEW`. Los SQL y validadores quedan como borrador de trabajo sujeto a corregir esa guarda.
