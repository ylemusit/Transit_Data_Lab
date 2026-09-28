# M06-B02A Requirement Concept Persistence

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Authorization

```text
M06_B02A_CONCEPT_PERSISTENCE = AUTHORIZED
CAPABILITY/MAPPING/BRIDGE/COVERAGE/REPRESENTABILITY/AUTOMATABILITY/AUDIT_RULE PERSISTENCE = NOT AUTHORIZED
```

Se aplicó únicamente el lote de siete concepts. `PARTIAL` y `UNRESOLVED` se guardan en `scope_status`, vocabulario activo de `REQUIREMENT_CONCEPT_SCOPE`; no se convierten silenciosamente en resultados de mapping, coverage ni auditoría. Para U01/U03, `review_outcome = NULL` conserva el hecho de que su estado de alcance es PARTIAL sin inventar una aceptación. U02 conserva `UNRESOLVED` en alcance y outcome.

## Pre-state

Rama `main`; working tree ya contenía cambios locales/untracked, preservados. DB `03_Compliance/databases/transit_compliance.duckdb`.

| Precheck | Valor |
|---|---:|
| SHA-256 | `E1CA1603D2300B90726F50C65092DB1E923B76F1F35A70E9F57CBB05E35A7BDE` |
| Concept schema / bridge schema | presentes |
| Concepts / bridges | 0 / 0 |
| Requirements / source provisions / source facts / deadlines | 48 / 92 / 36 / 10 |
| Mappings / mapping reviews / coverage | 6 / 6 / 8 |
| Automatability / representability / observed evidence / audit.rules | 6 / 0 / 0 / 0 |
| Coverage for P01/P02 target requirements | 0 |
| Target requirements | ambos presentes |

Una consulta de reconocimiento inicial usó por error `compliance.provisions`; la tabla real está en `source.provisions`. La consulta no escribió datos y el precheck corregido confirmó los conteos anteriores.

## Concepts persisted

| Concept ID | Requirement | Concept code | Scope/status | Source basis |
|---|---|---|---|---|
| `M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION` | `EU-2017-1926-REQ-A05-P01-002` | `ROAD_STATUS_DISRUPTION` | PARTIAL / ACCEPTED_WITH_LIMITATIONS | SF-A05-P01-ROAD; C01; Human Review y Post Human Review |
| `M06-B02-CPT-A05-P02-001-ROAD-STATUS-DISRUPTION` | `EU-2017-1926-REQ-A05-P02-001` | `ROAD_STATUS_DISRUPTION` | PARTIAL / ACCEPTED_WITH_LIMITATIONS | SF-A05-P02; C04; Human Review y Post Human Review |
| `M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION` | `EU-2017-1926-REQ-A05-P02-001` | `PASSENGER_RT_STATUS_DISRUPTION` | PARTIAL / ACCEPTED_WITH_LIMITATIONS | SF-A05-P02; C07; Human Review y Post Human Review |
| `M06-B02-CPT-A05-P02-001-FACILITY-ACCESS-NODE-STATUS` | `EU-2017-1926-REQ-A05-P02-001` | `FACILITY_ACCESS_NODE_STATUS` | PARTIAL / ACCEPTED_WITH_LIMITATIONS | SF-A05-P02; C08; Human Review y Post Human Review |
| `M06-B02-CPT-A05-P02-001-PARKING-TARIFF` | `EU-2017-1926-REQ-A05-P02-001` | `PARKING_TARIFF` | PARTIAL / no outcome assigned | SF-A05-P02; U01; Post Human Review; human decision PARTIAL |
| `M06-B02-CPT-A05-P02-001-SHARED-VEHICLE-AVAILABILITY` | `EU-2017-1926-REQ-A05-P02-001` | `SHARED_VEHICLE_AVAILABILITY` | UNRESOLVED / UNRESOLVED | SF-A05-P02; U02; Post Human Review; human decision KEEP_UNRESOLVED |
| `M06-B02-CPT-A05-P02-001-PARKING-AVAILABILITY` | `EU-2017-1926-REQ-A05-P02-001` | `PARKING_AVAILABILITY` | PARTIAL / no outcome assigned | SF-A05-P02; U03; Post Human Review; human decision PARTIAL |

El basis primario es jurídico/funcional. Las referencias a futuros perfiles técnicos solo aparecen como límites/contexto separado; no definen identidad ni significado de los concepts.

## Rejected concepts excluded

C02/C03/C05/C06 excluidos. No se insertaron conceptos para tiempos actuales de tramo viario ni tiempos futuros predichos.

## Database delta

| Área | Antes | Después | Delta |
|---|---:|---:|---:|
| Concepts B02 | 0 | 7 | +7 |
| Mappings B02 | 0 | 0 | 0 |
| Concept-mapping bridges B02 | 0 | 0 | 0 |
| Coverage decisiones B02 | 0 | 0 | 0 |
| Representability B02 | 0 | 0 | 0 |
| Automatability B02 | 0 | 0 | 0 |
| Observed evidence B02 | 0 | 0 | 0 |
| `audit.rules` | 0 | 0 | 0 |
| Mappings globales | 6 | 6 | 0 |
| Coverage global | 8 | 8 | 0 |

## Idempotence

Seed: `sql/03_mappings/phase3_m06_b02a_requirement_concepts_seed.sql`.

- Primera ejecución: transacción completada; siete inserts; postcheck correcto.
- Segunda ejecución: completada sin inserts ni delta semántico; el SHA-256 se mantuvo `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`.
- Los conflictos de ID/pareja requirement-code provocan abort; no hay `UPDATE` ni `ON CONFLICT DO UPDATE`.

La primera versión del postcheck abortó y revirtió al detectar una expectativa fija incorrecta para mappings B02. Se verificó SHA igual al previo (`E1CA…`), se corrigió la condición y la ejecución posterior pasó. No quedó escritura parcial.

## Validation

| Validator | Resultado observado |
|---|---|
| M06-B02A nuevo (`validate_phase_3_m06_b02a_requirement_concepts.sql`) | PASS, 11 checks, 0 fallos |
| Phase 3 Level A | PASS; 6 mappings, 6 capabilities, 6 exceptions; 0 referencias/estados/razones inválidas |
| M04 | ejecutado read-only, exit 0 |
| M04B | PASS; 0 structural failures, 8 coverage, 6 reviews |
| M05B | ejecutado read-only, exit 0; baseline/filas emitidas sin error |
| M06-B01 | PASS; 0 structural failures; contratos protegidos 0 |
| M06-B02 schema validator heredado | `EMPTY_SCHEMA_ONLY = FAIL (7)`; los restantes checks emitidos pasan. Ese validator exige que concepts y bridges estén vacíos, condición previa a B02A incompatible con la base después de la autorización. No se alteró su expected value. |
| Accounting global de excepciones | PASS; M04=3, B01=3, sin no contabilizadas |

Comandos ejecutados contra DuckDB `-readonly` para todos los validators; el seed fue el único escritor. No se usaron masters históricos incompatibles.

## Protected invariants

Los conteos y validators observaron Phase 1/2 intactas: 92 provisions, 36 source facts, 48 requirements, 10 deadlines. Mappings legacy=6, reviews=6, coverage=8, automatability=6, representability=0, observed evidence=0 y `audit.rules`=0. El validator M06-B02A confirmó también cero mappings, bridges y coverage para P01/P02 y cero asociaciones conceptuales legacy. No se actualizaron filas protegidas.

## Hashes

- DB SHA-256 BEFORE: `E1CA1603D2300B90726F50C65092DB1E923B76F1F35A70E9F57CBB05E35A7BDE`
- DB SHA-256 AFTER: `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`
- El delta de base corresponde a los siete conceptos y sus metadatos; el segundo seed mantuvo el hash posterior.

## Populated-schema gate addendum (2026-09-28)

### Gate classification

`validate_phase_3_m06_b02_requirement_concepts.sql` is the historical `EMPTY_SCHEMA_GATE`, designed for the pre-population M06-B02 schema checkpoint. Its `EMPTY_SCHEMA_ONLY` assertion correctly reports 7 persisted concepts after authorized M06-B02A; that expected historical-state mismatch is `NOT_APPLICABLE_TO_CURRENT_STATE`, not a current project defect. The validator and its expected values were not changed.

`validate_phase_3_m06_b02a_populated_schema.sql` is the authoritative `POPULATED_SCHEMA_GATE` from M06-B02A onward. It checks active schema constraints and N:M bridge structure; the exact seven concept IDs, P01/P02 split, requirement references and vocabulary; excluded current/future road-link travel-time concepts; zero B02 mappings, bridges, coverage and associated layers; six legacy mappings and no legacy concept associations; and protected Phase 1/2 counters.

### Result and validation

```text
M06_B02A_POPULATED_SCHEMA_GATE = PASS (13 checks, 0 failures)
M06_B02A_REQUIREMENT_CONCEPTS = PASS (11 checks, 0 failures)
EMPTY_SCHEMA_GATE = HISTORICAL / NOT_CURRENT_GATE
```

Executed read-only with DuckDB `-no-init -batch -bail -readonly -json`:

| Validator | Result |
|---|---|
| Populated schema | PASS, 13 checks, 0 failures |
| M06-B02A | PASS, 11 checks, 0 failures |
| Phase 3 Level A | PASS; 6 mappings, 6 capabilities, 6 exceptions; invalid references/states/reasons = 0 |
| M04 | PASS; 5 expected mappings, 0 non-pilot mappings, protected totals intact |
| M04B | PASS; 0 structural failures, 8 coverage decisions, 6 reviews |
| M05B | PASS; 48 primary memberships, 41 HIGH, 7 MEDIUM, 0 LOW |
| M06-B01 | PASS; 0 structural failures |
| Global exception accounting | PASS; 3 M04 and 3 B01, no unaccounted exceptions |
| Historical empty-schema validator | `EMPTY_SCHEMA_ONLY = FAIL (7)` as expected; every other emitted check passes |

Database SHA-256 before and after this gate/validation set: `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`. This task made no database writes. Phase 1/2 counters remain 92 provisions, 36 source facts, 48 requirements and 10 deadlines; legacy mappings remain six with zero concept associations. No capability, mapping, bridge or coverage persistence was authorized or performed. The validators are technical/data-integrity gates; no dataset implementation was observed and no legal compliance conclusion follows.

`PROJECT_STATUS.md` now records `M06_B02A_REQUIREMENT_CONCEPTS = CHECKPOINTED`, seven persisted concepts, zero B02 mappings, and M06-B02 as `IN_PROGRESS`. The B02 work is not complete; do not advance to B02B.

## Remaining B02 work

Capabilities, technical mappings, bridges, coverage, representability, automatability, observed evidence y audit rules siguen en cero/no autorizados. Los rechazos C02/C03/C05/C06 permanecen excluidos.

## Next gate

Actualizar o sustituir el validator de esquema para que valide el estado poblado M06-B02A sin cambiar evidencia histórica ni expected values incompatibles; después repetir el gate protegido correspondiente. No avanzar a capabilities ni mappings.
