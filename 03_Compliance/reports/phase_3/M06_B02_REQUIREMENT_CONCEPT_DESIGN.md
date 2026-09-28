# M06-B02 Requirement Concept Design

## Problem

`phase3_requirement_capabilities` ya implementa N:M entre requirements y capabilities: admite capabilities distintas por requirement y prohíbe repetir la pareja requirement/capability. Sin embargo, esa pareja no identifica qué concepto del requirement motiva la relación. B02 muestra que varios conceptos y estados parciales o no resueltos pueden coexistir bajo P02.

Este informe diseña la capa y una migración futura. No cambia SQL, DB, mappings ni validators.

## Current model

Inspección directa de la base actual en DuckDB `-readonly`, contrastada con `005_phase_3_m02_mapping_framework.sql`, `007_phase_3_m04b_semantic_coverage.sql` y `009_phase_3_m06_b01_unbound_capabilities.sql`:

- `mapping.phase3_requirement_capabilities.mapping_id` es la PK; `requirement_id` y `capability_id` son columnas `NOT NULL`; `capability_id` referencia `phase3_capabilities`.
- La constraint real es `UNIQUE(requirement_id, capability_id)`, no `UNIQUE(requirement_id)`. No hay FK de requirement a `compliance.requirements`.
- `phase3_mapping_reviews.mapping_id` es PK y FK a `mapping_id`.
- `phase3_automatability.mapping_id` es FK a `mapping_id`.
- `phase3_observed_evidence` puede referenciar `mapping_id` y/o `capability_id`; exige al menos uno. No refiere requirement directamente.
- `phase3_representability` refiere `capability_id`, no mapping ni requirement.
- `phase3_requirement_coverage` tiene `coverage_id` PK y `requirement_id UNIQUE`; es una decisión única por requirement. No tiene FK a mappings.
- `phase3_source_references` refiere capability; no mapping ni requirement.
- `phase3_exceptions` guarda `requirement_id`, sin FK a requirement ni a mapping.
- Hay seis mappings sustantivos actuales: cinco M04 y uno M06-B01. La DB también contiene seis reviews, ocho decisiones de coverage, seis automatability, cero representability, cero observed evidence y cero `audit.rules`. El inventario de source references es ocho y el de exceptions sustantivas seis.
- Ninguna tabla actual identifica el subalcance conceptual de un mapping. Los nombres y condiciones en texto no sustituyen una relación estructurada.

Los FKs entre `mapping` y `compliance` no se emplean en el esquema Phase 3 observado. El diseño no dependerá de añadir uno.

## Evidence from B02

Decisiones humanas registradas en `M06_B02_HUMAN_REVIEW.md` y su addendum post revisión:

- C01 y C04: aceptados con limitaciones; concepto acotado de estado/incidencias de carretera, no todo Annex 2.1.
- C07: aceptado con limitaciones; estado en tiempo real del servicio de pasajeros.
- C08: aceptado con limitaciones; estado de instalaciones/accesos, con crosswalk de elemento Annex pendiente.
- C02/C05 y C03/C06: rechazados para el alcance de estos requirements; sus perfiles existentes no demuestran correspondencia con este alcance.
- U01 y U03 siguen abiertos para investigación acotada; U02 queda sin resolver. No son mappings.

Estas decisiones justifican conceptos separados bajo P02, conceptos reutilizables entre requirements cuando el fundamento y ámbito lo permitan, y estados sin capability/mapping cuando no se ha demostrado una ruta.

## Design goals

1. Mantener la identidad y significado históricos de cada `mapping_id`.
2. No asignar concepts retroactivamente por similitud textual.
3. Requerir crosswalk explícito y revisado para nuevos mappings B02.
4. Representar conceptos `PARTIAL` y `UNRESOLVED` aunque no tengan mapping.
5. Preservar N:M requirement-capability, reviews, coverage, provenance y rutas funcionales/no técnicas.
6. Permitir concepts funcionales sin `standard_id` y conceptos cubiertos por una excepción/manual path.
7. Evitar que un resultado de concept se confunda con coverage completa, representability observada o compliance legal.

## Proposed concept model

Nombre recomendado: `mapping.phase3_requirement_concepts`. Cada fila es un concepto/subalcance situado dentro de un requirement, no una capability ni un fragmento jurídico materializado nuevo.

Propuesta de identidad y campos:

| Campo | Regla propuesta |
|---|---|
| `concept_id` | PK estable, ID legible con namespace del milestone; no derivado de texto mutable. |
| `requirement_id` | NOT NULL; ID literal del requirement, comprobado por validator read-only porque no se añade FK cross-schema. |
| `concept_code` | NOT NULL; código estable y único dentro del requirement (`UNIQUE(requirement_id, concept_code)`). |
| `concept_name` | NOT NULL; etiqueta legible. |
| `concept_description` | NOT NULL; alcance positivo, exclusiones y unidad semántica explícitos. |
| `scope_status` | `IN_SCOPE`, `PARTIAL`, `UNRESOLVED`, `OUT_OF_SCOPE`; estado del alcance, no de review/cobertura. |
| `applicability_conditions` | Nullable; condicionantes demostrados, separados de descripción y review. |
| `source_basis` | NOT NULL; referencia de origen con provision/Annex y sección. Conservar cita/URL/versionado en reporte o fuente capturada, no asumir que este campo por sí solo es provenance suficiente. |
| `review_status` | Vocabulario existente: `UNREVIEWED`, `NEEDS_REVIEW`, `REVIEWED`, `APPROVED`, `REJECTED`. |
| `review_outcome` | Nullable inicialmente; cuando haya revisión, `ACCEPTED`, `ACCEPTED_WITH_LIMITATIONS`, `REJECTED`, `UNRESOLVED`, conforme a vocabulario existente. Si limitations es aceptado, exigir texto no vacío. |
| `review_justification`, `limitations` | Motivo y límites de la decisión semántica del concept. No reutilizar la review de un mapping como si revisara el concept. |
| `created_at`, `created_by`, `reviewed_at`, `reviewed_by` | Provenance temporal/persona. Las fechas no se infieren para legacy. |
| `notes` | Contexto adicional sin semántica normativa implícita. |

Restricciones: PK en `concept_id`; `UNIQUE(requirement_id, concept_code)`; CHECKs de `scope_status`, `review_status` y outcome contra valores definidos; checks de texto no vacío para identificadores/nombre/description/source; limitar review metadata coherentemente; exigir `limitations` en `ACCEPTED_WITH_LIMITATIONS`. Introducir valores en `phase3_vocabularies` y CHECKs sincronizados solo en la misma migración controlada. No llamar `LEGACY_UNSCOPED` a un concept: no es un concept y el legacy se expresa con ausencia de asociación.

La tabla describe estado conceptual. `UNRESOLVED` no crea capability, mapping, ausencia de datos ni resultado de auditoría.

## Schema proposal

Añadir, sin ejecutar:

1. `mapping.phase3_requirement_concepts`, según el modelo anterior.
2. `mapping.phase3_concept_mappings`, puente explícito entre concept y mapping existente:

```sql
-- DRAFT / NOT EXECUTED
CREATE TABLE mapping.phase3_concept_mappings (
    concept_id VARCHAR NOT NULL
        REFERENCES mapping.phase3_requirement_concepts(concept_id),
    mapping_id VARCHAR NOT NULL
        REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
    relation_note VARCHAR NOT NULL,
    PRIMARY KEY (concept_id, mapping_id)
);
```

La PK compuesta permite N:M: un mapping puede relacionarse con varios concepts y un concept con varios mappings, sin duplicar el mismo par. El borrador inicial proponía `UNIQUE(mapping_id)`; se elimina antes de migrar porque no hay una razón arquitectónica demostrable para imponer 1:N y el encargo aprobado exige preservar N:M. El validator comprobará además que el `requirement_id` del concept coincide con el del mapping; DuckDB no puede expresar esa comprobación como FK compuesta con las constraints actuales sin reconstruir la tabla padre o añadir una clave compuesta. La relación debe fallar en validator si hay mismatch. No se añaden mappings de concept a capability separados: el mapping existente conserva review, tipo, condiciones e ID canónicos.

Los campos de provenance del concept registran revisión de su semántica; la evidencia fuente de capability permanece en `phase3_source_references`. Si en una fase posterior se necesita normalizar fuentes por concept, proponer tabla source-link propia, no sobrecargar referencias de capability.

Para rutas de excepción/manuales, el concept puede existir sin mapping. Un vínculo estructurado concept-exception requiere decisión propia (p. ej., `phase3_concept_exceptions`) y validator de requisito coincidente; no es necesario para el primer crosswalk técnico B02 ni debe simularse como mapping. No se obliga a que un concept tenga `standard_id`: este reside en capability y puede ser NULL según M06-B01, o no existir si no se ha demostrado una ruta.

## Mapping relation proposal

**Recomendación: opción B refinada, tablas nuevas de concepts + puente a `mapping_id`, tabla `phase3_requirement_capabilities` intacta.** El puente es una clasificación revisada del mapping existente, no un segundo sistema de mapping.

| Alternativa | Integridad y claridad | Migración y compatibilidad | Consultas/validators/mantenimiento |
|---|---|---|---|
| A: añadir `concept_id NULL` al mapping | Relación directa; FK concept/requisito compuesto requiere columnas/constraint adicional. La unicidad actual req-cap seguiría impidiendo repetir la misma capability en dos concepts. | `phase3_requirement_capabilities` tiene varias tablas dependientes. El patrón M06-B01 indica que DuckDB requiere reconstruir el subgrafo FK para alterar tabla padre; alto coste y riesgo relativo. | Join simple, pero acopla esquema histórico y permite que el NULL se interprete erróneamente como estado semántico. |
| B: mantener mapping intacto y crear concepts + puente | Mapping mantiene autoridad; el puente identifica alcance. FK individuales; consistencia de requirement comprobada por validator. | Solo objetos aditivos; los seis mappings y sus dependencias quedan intactos y pueden permanecer sin puente. Riesgo bajo. | Un join más; reglas simples y auditables. Bridge insertado en misma transacción que futuro mapping B02; validator obliga el crosswalk. |
| C: tabla concepto-capability paralela | Puede modelar conceptos sin tocar mappings, pero duplica mapping/review/conditions o deja estos sin la semántica conceptual. | Preserva legacy, pero obliga a conciliar dos relaciones de mapping y su historia. | Ambiguo cuál relation impulsa review, evidence y automatability; más mantenimiento y riesgo de drift. |

La limitación de `UNIQUE(requirement_id, capability_id)` se mantiene explícita: no se pueden crear dos mapping rows para la misma pareja aun si tienen scopes conceptuales distintos. Si el caso real lo exige, la futura decisión debe rediseñar la cardinalidad y reconstruir la tabla y subgrafo con un plan probado. No levantar esa uniqueness de forma incidental en esta migración.

## Coverage implications

La decisión de coverage permanece agregada a nivel requirement en `phase3_requirement_coverage`; su `UNIQUE(requirement_id)` expresa actualmente una decisión por requirement.

- **A. Solo requirement-level:** conserva contrato vigente, pero obliga a expresar el desglose concept-level en `identified_paths`/texto; no permite queries estructuradas ni agregación reproducible.
- **B. Concept-level + agregado de requirement:** representa directamente estados de cada concepto y conserva una decisión humana agregada por requirement. Recomendado como evolución cuando se requiera persistir B02 coverage. No duplicar la tabla actual; añadir `phase3_concept_coverage` con FK concept, vocabulario de coverage existente, justificación, límites, reviewer y baseline; conservar requirement aggregate con regla de reconciliación versionada.
- **C. Scoped coverage component:** crea unidad más amplia para coverage/mapping/evidence. Aporta robustez para rutas híbridas, pero puede confundir un componente de evaluación con un concept jurídico si no tiene source basis y límites propios.

Para este diseño elegir B como destino de coverage futura, manteniendo la tabla requirement actual como roll-up humano explícito. No calcular automáticamente `ESTABLISHED` desde todos los concepts sin definición de agregación aprobada. Cualquier concept `UNRESOLVED` o `PARTIAL` debe poder conducir a overall `PARTIAL`/`UNRESOLVED` con condiciones; rejected/out-of-scope no se cuentan como cubiertos. Coverage sigue siendo evaluación semántica, nunca cumplimiento.

## Representability implications

La tabla actual está anclada solo a `capability_id` y no señala qué mapping/requirement motiva la evaluación. Para una capacidad reutilizable, conservar este nivel como propiedad técnica general; para afirmar representability bajo un requirement y concept, el anchor recomendado futuro es `mapping_id` (con concept recuperable por el puente). Esto evita afirmar que el requirement entero es representable y deja el standard opcional en capabilities funcionales.

No crear representability por el mero hecho de aceptar un concepto B02. El futuro esquema podría introducir una tabla scoped de assertions o ampliar mediante migración controlada la representability para referenciar mapping; agregar `concept_id` directo solo si hay assertions sin mapping. Mantener `AVAILABLE/MAPPABLE/PARTIAL/MISSING/UNKNOWN/NOT_APPLICABLE` existentes y sus evidencias/conditions. Ahora hay cero filas sustantivas.

## Observed evidence implications

Actualmente la observación puede referir `mapping_id`, `capability_id` o ambos, y exige uno. Un mapping identificado permite recuperar el concept por `phase3_concept_mappings`; así se puede expresar `dataset/feed/document → evidencia para el concept` sin atribuir coverage al requirement completo. Para evidencia de un concept aún no mapeado (p. ej. exploración de una categoría unresolved), la tabla actual no ofrece concept anchor; una futura ampliación debería añadir `concept_id` nullable o tabla de evidencia conceptual, conservando sus actuales anchors y exigiendo al menos uno. Todo registro necesita locator y fecha/provenance verificables. Actualmente hay cero observed evidence sustantivas.

## Automatability/audit implications

El mapping actual es el anchor de `phase3_automatability`; con el puente, concept se deriva sin reanclar su historial. Automatability de mapping evalúa condiciones de una posible prueba, no ejecución ni resultado. Un concept parcial/unresolved sin mapping no debe recibir automatability inventada.

Antes de cualquier `audit.rules`, cada futura regla necesitaría enlazar requirement + concept + mapping/capability, condición de aplicabilidad, evidencia esperada, versión/contrato y revisión de falsos positivos. `audit.rules = 0`; no hay contrato de ejecución aprobado. Este diseño solo prepara IDs y relaciones. No se propone vocabulario de resultado.

## Legacy compatibility

Los seis mapping rows históricos permanecen sin filas en `phase3_concept_mappings`; no se añade un concept artificial `LEGACY_UNSCOPED`. El NULL/ausencia de relación significa solamente “sin concept estructurado persistido”, no que el mapping fuera inválido, incompleto o sin review.

| `mapping_id` | Clasificación | ¿Backfill con evidencia revisada explícita? | Motivo |
|---|---|---|---|
| `M04-MAP-A04P01-GTFS-TRIP-STOP` | `KEEP_NULL` | NO demostrada | Scope de servicio programado descrito, pero no hay concept ID/subalcance revisado ligado a este mapping. |
| `M04-MAP-A04P01-NETEX-PT` | `KEEP_NULL` | NO demostrada | Scope de red/horario está en condiciones; no existe crosswalk conceptual persistido y revisado. |
| `M04-MAP-A04P02-NETEX-PT` | `KEEP_NULL` | NO demostrada | Profile/category remains unresolved; no concepto explícito revisado. |
| `M04-MAP-A08P03-GTFS-ATTRIBUTION` | `KEEP_NULL` | NO demostrada | Condiciones de metadata de atribución no son un concept ID aprobado. |
| `M04-MAP-A08P03-GTFS-PUBLISHER` | `KEEP_NULL` | NO demostrada | Alcance publisher metadata no trae una asociación a concept formal revisada. |
| `M06-B01-MAP-A03-P03-001-NAP-DISCOVERY` | `KEEP_NULL` | NO demostrada | Capability funcional y review están aprobadas con límites, pero no se creó concept/subalcance en B01. Su mapping/review no deben reinterpretarse retroactivamente. |

`SAFE_TO_BACKFILL = 0`; `REQUIRES_HUMAN_REVIEW = 0` para esta migración, pues no se propone backfill que luego quede pendiente de revisión; `KEEP_NULL = 6`. Estos conteos no prejuzgan una decisión humana futura separada.

## B01 compatibility

Un concept no exige `standard_id`. `NAP_DATA_DISCOVERY` es capability funcional reutilizable con standard NULL; la relación concept→mapping puede referirla normalmente. Para `A03-P01-001` y `A03-P01-002`, las rutas son `LEGAL_PROCESS` y `ORGANIZATIONAL`, sin mapping técnico: un concept puede existir sin capability y seguir sin mapping. `A03-P03-001` mantiene capability/mapping funcional junto a `MANUAL_ASSESSMENT`; ambas rutas no se colapsan.

Si se requiere que exception path se estructure por concept, diseñar vínculo concept-exception separado y añadirlo al validator global accounting. No exigir un mapping falso para excepciones. Las tres coverage B01 existentes siguen agregadas por requirement y no se reescriben.

## B02 worked example

Esquema ilustrativo; no persistir:

```text
P02 = EU-2017-1926-REQ-A05-P02-001
├── ROAD_STATUS
│   └── C04 → DATEX II road status capability (accepted with limitations)
├── PASSENGER_REALTIME_STATUS
│   └── C07 → SIRI EPIP-RT capability (accepted with limitations)
├── FACILITY_ACCESS_STATUS
│   └── C08 → SIRI facility capability (accepted with limitations; Annex-to-element crosswalk remains bounded)
├── PARKING_TARIFF (U01)
│   └── PARTIAL / research requested / no capability or mapping
├── SHARED_VEHICLE_AVAILABILITY (U02)
│   └── UNRESOLVED / no capability or mapping
└── PARKING_SPACE_AVAILABILITY (U03)
    └── PARTIAL / research requested / no capability or mapping

Requirement-level coverage: PARTIAL (future human decision, not auto-derived)
```

C01 is a separate road-status mapping for P01 and may reuse an appropriate capability; it is not another P02 concept. Rejected C02/C03/C05/C06 are not persisted as B02 scoped mappings. The example proves the model represents multiple scoped routes and unresolved/partial concepts without fabricating mappings. The accepted B02 decisions remain bounded and do not claim full P02 coverage.

## Migration plan

Design only. A later migration proposal should be a single guarded transaction with fail-safe pre/postconditions.

### Prechecks

- Assert DB identity/path and expected Phase 3 schema version/objects; assert concept tables/columns do not already exist (otherwise abort and inspect, not silently `IF NOT EXISTS`).
- Record exact row counts and ordered key/pair snapshots for the six mappings, six reviews, eight coverage rows, six automation rows, source references, exceptions, zero substantive representability/evidence, and zero audit rules.
- Inspect PK/UNIQUE/FK/check constraints and all referencing tables for `mapping_id`; verify all six mapping IDs and requirement-capability pairs match recorded pre-state.
- Verify Phase 1/2 protected objects, DB SHA-256 before migration, branch and worktree baseline. No global dataset walk.
- Validate that each proposed B02 concept references an existing requirement and carries reviewed source basis; no automatic source/text derivation.

### Migration

- Create `phase3_requirement_concepts`, its controlled vocabulary entries/checks and `phase3_concept_mappings`; add only needed indexes on `requirement_id`, `concept_id`, and mapping lookup if query plans justify them.
- Do not modify or rebuild `phase3_requirement_capabilities`, its mapping IDs, or dependent tables. Do not seed B02 concepts in the schema migration; concept and B02 persistence would be a separate authorized, reviewed seed.
- Legacy rows receive no association. New B02 mapping writes must insert mapping + bridge in one transaction after human-approved crosswalk. Since existing pair uniqueness persists, abort on duplicate requirement-capability pair rather than silently reusing a mapping with a different concept.

### Postchecks

- Existing six `mapping_id` values and six requirement-capability pairs remain byte-for-byte equivalent; six reviews, eight coverage, source references and exceptions unchanged.
- No Phase 1/2 rows or snapshots change; no pre-existing concept associations are synthesized; no concept promotion from mapping prose.
- Zero orphan concepts, mapping IDs, or requirement mismatches; all concepts satisfy controlled vocabularies/review constraints.
- Legacy null/absent associations count exactly six; B02 crosswalk count equals only the specifically approved mappings; no rejected candidate is linked.
- Counts for representability, observed evidence, audit rules remain unchanged unless a separately authorized batch addresses them.

### Idempotence

Migration: single-run, fail-safe; fail if any target objects already exist. Do not mask partial or mismatched state with `IF NOT EXISTS`. Seed: separately idempotent by stable concept IDs and `(requirement_id, concept_code)`, with preflight that an existing ID has identical reviewed content; incompatible row is an error. Mapping+bridge seed must be transactionally all-or-nothing and preserve stable mapping IDs. This follows the guarded M06-B01 transaction style while avoiding its FK-subgraph rebuild.

## Validator plan

Future read-only validator set:

1. Unique concept IDs and `(requirement_id, concept_code)`; non-empty fields; allowed scope/review/outcome vocabularies and review metadata consistency.
2. Requirement existence in `compliance.requirements`; report orphan IDs (logical cross-schema check, not assumed FK).
3. Bridge references resolve; concept and mapping requirement IDs match; no mapping linked to multiple concepts; concept mappings attach only reviewed/eligible rows per the authorized B02 contract.
4. All newly persisted B02 capability mappings have a concept crosswalk; pre-existing M04/B01 mappings may remain unscoped. Rejected B02 candidates are not linked.
5. `PARTIAL`/`UNRESOLVED` concepts can have no mapping; absence of mapping is not converted to `MISSING`/no data. If a mapping exists, its concept is not unresolved unless a reviewed exception explicitly permits the relation.
6. Concept-coverage rows, when later approved, have one row per concept; requirement roll-up reconciles to components using a versioned, human-approved aggregation rule. Until then, no auto-rollup claim.
7. Regression checks ensure no Phase 1/2 mutation and no change in global Phase 3 accounting, especially exceptions, mapping/review counts and audit rules.

Existing M04, M04B, M05B and B01 validators are historical/batch scoped. Do not rewrite their expected counts to absorb concepts. Add a B02 validator and update global accounting only through a future authorized milestone with explicit scope. `quick_validate` remains `NOT_EXECUTED` while YAML is missing.

## Rollback/failure behaviour

The setup migrations include non-transactional framework setup (`005`), transactional guarded M04B (`007`), and transactional guarded M06-B01 (`009`). M06-B01 explicitly rebuilds the FK-dependent mapping subgraph inside a transaction because DuckDB cannot alter the referenced parent table in place; its historical migration/validator reports say its rollback fixture was tested. Follow the explicit transaction plus `error()` guards pattern for this additive design; do not depend on autocommit behavior.

- Precheck failure: abort before DDL; if inside transaction, issue `ROLLBACK`; preserve DB SHA and emit failure evidence.
- Any DDL/insert/constraint/postcheck error before commit: `ROLLBACK`; do not attempt repair-in-place or retry blindly.
- Commit only after all postchecks pass. If a post-commit independent check fails, stop and classify the DB as needing controlled recovery; a committed transaction cannot be rolled back by issuing a later rollback. Restore only from the verified pre-migration snapshot through an explicitly approved recovery procedure.
- Confirm rollback semantics with a disposable fixture in the future migration test before touching the protected DB. Current session executes no migration/fixture.

## Alternatives rejected

- Direct N:M alone: valid current arrangement but leaves concept basis in prose and cannot express structured unresolved/partial subscopes.
- Add nullable `concept_id` to the current mapping row for this migration: semantically viable, but forces a risky rebuild of referenced mapping tables in DuckDB and still needs a cardinality decision around existing pair uniqueness. Prefer additive bridge now.
- Parallel concept-capability mappings: duplicates semantic links and splits which mapping ID owns reviews, evidence and automation.
- Automatic `LEGACY_UNSCOPED` concept/backfill: invents a semantic row and can be mistaken for reviewed scope; lack of bridge is sufficient and truthful.
- Make coverage concept-only: loses the current human-reviewed requirement aggregate and breaks its single-row-per-requirement contract.
- Force standard ID on concepts: incompatible with B01 functional capabilities and manual/legal routes.

## Risks

- Logical requirement consistency in the bridge depends on a validator because cross-schema/composite FK support is absent in the current shape.
- Existing `UNIQUE(requirement_id, capability_id)` prevents multiple mappings for the same capability under one requirement even when concepts differ; a real case would need a separate cardinality migration.
- Concept status and review status describe different axes; users/validators must not conflate them.
- Coverage aggregation can conceal unresolved scope unless rules are explicit and human-approved.
- Accepted-with-limitations C08 still has a bounded Annex-to-element crosswalk; its concept must retain that limitation.
- No actual NAP implementation or dataset was inspected; representability, observed evidence, automatability and legal compliance are not established by this design.

## Open questions

1. Approve the separate concept table plus mapping bridge, including one concept maximum per mapping and the current pair uniqueness limitation?
2. Approve the proposed concept status and review fields/vocabularies, and whether source citation normalization is needed at first migration?
3. Should concept-level coverage be included in a later migration, with requirement coverage remaining a separately reviewed aggregate?
4. Should exception-to-concept linkage be in scope for a later B01-compatible extension?
5. Are the precise C01/C04/C07/C08 labels, bounds and C08 crosswalk limitations the intended persistence scope after profile/crosswalk prerequisites are met?

## Recommended decision

Adopt additive `phase3_requirement_concepts` plus `phase3_concept_mappings` linked by existing `mapping_id`. Keep `phase3_requirement_capabilities`, its six historic mappings, their reviews, requirement coverage, provenance, representability/evidence/automation references and legacy meaning unchanged. Require explicit concept review and bridge insertion for new B02 mappings; permit standalone `PARTIAL`/`UNRESOLVED` concepts without mappings. Retain requirement-level coverage now; design per-concept coverage as a later additive layer with explicit aggregate policy. Do not infer concepts from legacy text.

To authorize a future migration, Yeison must approve the architecture, schema vocabularies/provenance fields, bridge cardinality and duplicate-pair behavior, legacy KEEP_NULL policy, coverage evolution boundary, and whether exception linkage is deferred. Migration approval and B02 data persistence approval should be explicit and separate.

```text
REQUIREMENT_CONCEPT_DESIGN = READY_FOR_HUMAN_REVIEW
SCHEMA_MIGRATION = NOT_AUTHORIZED
DB_PERSISTENCE = NOT_AUTHORIZED
```
