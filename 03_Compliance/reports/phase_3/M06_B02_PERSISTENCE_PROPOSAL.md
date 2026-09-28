# M06-B02 Persistence Proposal

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

```text
M06_B02_PERSISTENCE_PROPOSAL = READY_FOR_HUMAN_REVIEW
B02_DATA_PERSISTENCE = NOT_AUTHORIZED
```

## Scope

Propuesta documental para persistencia futura de concepts, capabilities, mappings, puentes y coverage de los requisitos `EU-2017-1926-REQ-A05-P01-002` (P01) y `EU-2017-1926-REQ-A05-P02-001` (P02). No se ejecutan seeds ni se modifica la base. Las decisiones humanas de candidatos se toman de `M06_B02_POST_HUMAN_REVIEW.md`; su aceptación semántica no autoriza por sí sola la escritura ni decide coverage.

Las etiquetas `ESTABLISHED/PARTIAL/UNRESOLVED` de este informe describen cada eslabón documental. No equivalen a cumplimiento legal, presencia de datos, implementación NAP ni aprobación de persistencia.

## Human decisions

| Candidato | Decisión humana vigente | Tratamiento aquí |
|---|---|---|
| C01 P01 road status/disruption | ACCEPT_WITH_LIMITATIONS | Concept y mapping estrecho propuestos. |
| C02, C03 P01 travel time / forecast | REJECT | Excluidos; no se crea ni asocia mapping. |
| C04 P02 road status/disruption | ACCEPT_WITH_LIMITATIONS | Concept y mapping estrecho propuestos. |
| C05, C06 P02 travel time / forecast | REJECT | Excluidos; no se crea ni asocia mapping. |
| C07 P02 passenger real-time status | ACCEPT_WITH_LIMITATIONS | Concept y mapping SIRI propuestos. |
| C08 P02 facility/access-node status | ACCEPT_WITH_LIMITATIONS | Concept y mapping SIRI-FM propuestos con limitación explícita del crosswalk Annex→elemento. |
| U01 parking tariff | PARTIAL | Concept sin capability/mapping. |
| U02 shared vehicle availability | UNRESOLVED | Concept sin capability/mapping; investigar por modo/categoría. |
| U03 parking availability | PARTIAL | Concept sin capability/mapping. |

Origen de decisiones: revisión humana M06-B02 y post-revisión M06-B02, 2026-09-28. No se reabren ni se reinterpretan C02/C03/C05/C06. La etiqueta `REJECTED` de esos candidatos no se introduce como fila de mapping: sencillamente no hay mapping propuesto.

## Current authoritative state

Consulta DuckDB con `-readonly` a `03_Compliance/databases/transit_compliance.duckdb`, contrastada con `PROJECT_STATUS.md` y el informe de migración:

| Objeto | Estado actual |
|---|---:|
| Requirements | 48 |
| Mappings sustantivos legacy | 6 |
| Standards / capabilities | 3 / 6 |
| Concepts / concept bridges | 0 / 0 |
| Mappings B02 | 0 |
| Coverage total | 8 |
| Coverage P01/P02 | 0 |
| Representability sustantiva / observed evidence | 0 / 0 |
| `audit.rules` | 0 |
| `phase3_requirement_concepts` y `phase3_concept_mappings` | activas, esquema vacío |

El validator M06-B02 de esquema comprueba que los seis mappings legacy siguen sin association. `CAP-DATEXII-RRP-ROAD-TRAVEL` tiene ámbito de travel-time; no es reutilizable para disruption/status. El registro DATEX existente es `IDENTITY_ONLY` y cataloga MMTIS RRP; no representa por sí solo el perfil RTTI aplicable.

## Proposed requirement concepts

Los IDs se derivan del milestone, código de requirement y `concept_code`, con lo que son deterministas y no dependen de una versión de perfil. Las filas propuestas usarían `created_by`/`reviewed_by = Yeison Arbey Carrillo Lemus`, fecha de creación/revisión posterior a la autorización futura, `review_status = APPROVED` y `review_outcome = ACCEPTED_WITH_LIMITATIONS` en los cuatro concepts aceptados. Los concepts U01–U03 usarían `review_status = REVIEWED`, outcome conforme a la decisión y sin `reviewed_by` inventado: requieren resolución/decisión de persistencia humana antes de seed.

| concept_id propuesto | requirement_id | concept_code | Nombre y límite | scope_status | source_basis y origen | Estado/outcome propuesto | Limitations |
|---|---|---|---|---|---|---|---|
| `M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION` | P01-002 | `ROAD_STATUS_DISRUPTION` | Estado dinámico e incidencias de la red viaria cubiertas por la ruta RTTI específica; no toda clase de dato dinámico de carretera. | PARTIAL | `EU-2017-1926-SF-A05-P01-ROAD`; C01; decisión humana M06-B02. | APPROVED / ACCEPTED_WITH_LIMITATIONS | Referencia literal de Art. 5(1)(a) a 2015/962; relación con RTTI actual es puente funcional/informativo, no sustitución jurídica expresa. |
| `M06-B02-CPT-A05-P02-001-ROAD-STATUS-DISRUPTION` | P02-001 | `ROAD_STATUS_DISRUPTION` | Disrupciones/status de carretera dentro de Annex 2.1(i) y rama viaria pertinente de 2.1(ii). | PARTIAL | `EU-2017-1926-SF-A05-P02`; C04; decisión humana M06-B02. | APPROVED / ACCEPTED_WITH_LIMITATIONS | P02 es condicional; no representa todas las categorías de Annex 2.1/2.2 ni las ramas de pasajeros. |
| `M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION` | P02-001 | `PASSENGER_RT_STATUS_DISRUPTION` | Estado en tiempo real del servicio público de pasajeros, incluyendo retrasos, cancelaciones y mensajes de disrupción dentro del alcance EPIP-RT. | PARTIAL | `EU-2017-1926-SF-A05-P02`; C07; decisión humana M06-B02. | APPROVED / ACCEPTED_WITH_LIMITATIONS | No todo dato dinámico P02 ni toda modalidad/elemento Annex queda demostrado por el perfil. |
| `M06-B02-CPT-A05-P02-001-FACILITY-ACCESS-NODE-STATUS` | P02-001 | `FACILITY_ACCESS_NODE_STATUS` | Estado de disponibilidad de accesos/instalaciones de nodo de transporte: p.ej. ascensor o escalera mecánica cuando el elemento perfilado corresponda. | PARTIAL | `EU-2017-1926-SF-A05-P02`; C08; decisión humana M06-B02. | APPROVED / ACCEPTED_WITH_LIMITATIONS | No se cerró el crosswalk exacto para cada elemento Annex, entrada/salida, andén/parada y facility element SIRI. |
| `M06-B02-CPT-A05-P02-001-PARKING-TARIFF` | P02-001 | `PARKING_TARIFF` | Información de tarifas de aparcamiento comprendida en el candidato U01. | PARTIAL | `EU-2017-1926-SF-A05-P02`; U01; revisión humana. | NEEDS_REVIEW / UNRESOLVED | No hay perfil, capability ni ruta técnica demostrados. Outcome final/persistencia requieren decisión humana. |
| `M06-B02-CPT-A05-P02-001-SHARED-VEHICLE-AVAILABILITY` | P02-001 | `SHARED_VEHICLE_AVAILABILITY` | Disponibilidad/localización de vehículos compartidos bajo U02, sin colapsar modos o categorías. | UNRESOLVED | `EU-2017-1926-SF-A05-P02`; U02; revisión humana. | NEEDS_REVIEW / UNRESOLVED | Investigación futura debe dividir por modo/categoría; no se crea capability o mapping. |
| `M06-B02-CPT-A05-P02-001-PARKING-AVAILABILITY` | P02-001 | `PARKING_AVAILABILITY` | Disponibilidad de aparcamiento U03, sin afirmar que disponibilidad on-street y off-street compartan perfil. | PARTIAL | `EU-2017-1926-SF-A05-P02`; U03; revisión humana. | NEEDS_REVIEW / UNRESOLVED | No hay perfil/capability/mapping demostrados ni distinción persistida de subcategorías. |

`source_basis` permite conservar IDs de source fact/candidato/decisión; `notes` puede apuntar al informe y a sus citas. No se debe fingir que `source_basis` es una FK ni añadir campos al esquema.

## Crosswalk matrix

`ESTABLISHED` se limita al puente técnico/documental demostrado; cada fila conserva sus otros puentes parciales o sin resolver.

| Concept | Requirement | Human decision | Standard/Profile | Capability | Mapping | Confidence | Persist concept? | Persist mapping? |
|---|---|---|---|---|---|---|---|---|
| ROAD_STATUS_DISRUPTION (P01) | P01-002 → `SF-A05-P01-ROAD`: PARTIAL | C01 accepted w/ limits | DATEX II RTTI RRP, categoría(s) de Annex 4/5 y solo la porción aplicable: PARTIAL | Nueva capability road-status: PARTIAL | P01→concept→fuente→perfil→capability: PARTIAL; legal reference bridge no vinculante | MEDIUM | Sí, con PARTIAL | Sí, tipo PARTIAL; límites y review separados |
| ROAD_STATUS_DISRUPTION (P02) | P02-001 → `SF-A05-P02`: PARTIAL/condicional | C04 accepted w/ limits | RTTI RRP road categories, no blanket Annex mapping: PARTIAL | Misma capability road-status que P01: PARTIAL | P02→concept→fuente→RRP→capability: PARTIAL | MEDIUM | Sí, con PARTIAL | Sí, tipo PARTIAL |
| PASSENGER_RT_STATUS_DISRUPTION | P02-001 → `SF-A05-P02`: PARTIAL | C07 accepted w/ limits | SIRI EPIP-RT, CEN/TS 15531-7:2025; ET/SX para estimated times, demoras/cancelaciones y disrupciones: PARTIAL | Nueva capability concept-scoped SIRI passenger status: PARTIAL | El perfil define dominio y servicios; la asignación a todo Annex 2.1(ii) permanece parcial | MEDIUM | Sí, con PARTIAL | Sí, tipo PARTIAL |
| FACILITY_ACCESS_NODE_STATUS | P02-001 → `SF-A05-P02`: PARTIAL | C08 accepted w/ limits | EPIP-RT integra SIRI-FM; Part 4 es servicio FM; elementos exactos aplicables: PARTIAL | Nueva capability SIRI facility monitoring, concept-scoped: PARTIAL | Falta crosswalk preciso de cada Annex item a elementos SIRI-FM | LOW–MEDIUM | Sí, con PARTIAL | Sí, solo con limitación textual y mapping PARTIAL |
| PARKING_TARIFF | P02-001: PARTIAL | U01 PARTIAL | UNRESOLVED | DO_NOT_CREATE | No mapping | LOW | Sí, concept PARTIAL si Yeison lo aprueba | No |
| SHARED_VEHICLE_AVAILABILITY | P02-001: PARTIAL | U02 UNRESOLVED | UNRESOLVED; investigar por modo/categoría | DO_NOT_CREATE | No mapping | LOW | Sí, concept UNRESOLVED si Yeison lo aprueba | No |
| PARKING_AVAILABILITY | P02-001: PARTIAL | U03 PARTIAL | UNRESOLVED; on/off-street no resuelto | DO_NOT_CREATE | No mapping | LOW | Sí, concept PARTIAL si Yeison lo aprueba | No |

Rechazos fuera de la matriz persistible: C02/C03/C05/C06. No reaparecen como concept independiente ni como ruta asociada; sus perfiles no autorizan ese vínculo requirement→concept.

## Capability decisions

| Capability | Acción | standard_id | Semantic scope / decisión | Estado y límites |
|---|---|---|---|---|
| `CAP-DATEXII-RRP-ROAD-TRAVEL` | REUSE_EXISTING solo para tiempos de viaje; **DO_NOT_CREATE/REUSE para B02 status** | `M03-DATEXII-MMTIS-RRP` | Su ámbito registrado es road-link travel time; mismatch para cierres, incidentes y estado de red. | No asociar a C01/C04. C02/C03/C05/C06 ya están rechazados para estos requirements. |
| `M06-B02-CAP-DATEXII-RRP-ROAD-STATUS` | CREATE_NEW | `M03-DATEXII-MMTIS-RRP` como identidad DATEX II existente; RTTI category profile queda en dependency/source reference | Cierres, lane closures, obras, gestión temporal y categorías acotadas de incidentes/estado RTTI aplicables al concept. | ACCEPTED_WITH_LIMITATIONS; scope parcial; registry identity existente no afirma la versión/modelo del RRP. |
| `M06-B02-CAP-SIRI-EPIPRT-PASSENGER-STATUS` | CREATE_NEW | nuevo registro de identidad SIRI EPIP-RT propuesto, versionado CEN/TS 15531-7:2025 | Servicios ET y SX para estimaciones de horario, retrasos/cancelaciones y disrupciones del pasajero, según ámbito de profile. | ACCEPTED_WITH_LIMITATIONS; no extenderlo a todo Annex 2. |
| `M06-B02-CAP-SIRI-EPIPRT-FACILITY-STATUS` | CREATE_NEW | mismo registro propuesto SIRI EPIP-RT | Monitorización de instalaciones/accesibilidad mediante SIRI-FM; no declara equivalencia completa con todos los elementos 2.1(iii). | ACCEPTED_WITH_LIMITATIONS; falta exact Annex-element crosswalk. |
| Capacidades de aparcamiento/vehículos compartidos | DO_NOT_CREATE | — | No hay profile/capability scope probado. | U01/U02/U03 sin capability ni mapping. |

No hay duplicado semántico: la capability DATEX nueva separa status de travel-time. Se comparte entre P01/P02 por tener el mismo scope técnico; mappings siguen separados por requirement y el puente apunta a concepts distintos. Se propone añadir un standard identity SIRI EPIP-RT porque no existe en las tres identidades registradas. No modificar el registro DATEX existente para aparentar RTTI.

## Mapping proposals

Todas las filas siguientes son propuestas, no registros. Mapping type `PARTIAL`, estado de review `APPROVED`, y review semántico `ACCEPTED_WITH_LIMITATIONS` reflejan las cuatro decisiones humanas; se exige limitación no vacía en mapping y review. La provenance no tiene columna propia en `phase3_requirement_capabilities`: reside en el paquete y, si luego se aprueba, en `phase3_mapping_reviews.justification`, `phase3_concept_mappings.relation_note`, `phase3_source_references` y la evidencia documental del milestone.

| mapping_id | requirement_id | capability_id | concept_id vía puente | mapping_type / review_status | Evidence y limitación | Provenance propuesta |
|---|---|---|---|---|---|---|
| `M06-B02-MAP-A05-P01-002-DATEX-ROAD-STATUS` | P01-002 | `M06-B02-CAP-DATEXII-RRP-ROAD-STATUS` | concept ROAD_STATUS_DISRUPTION P01 | PARTIAL / APPROVED | DATEX II RTTI RRP catálogo y perfiles de status aplicables. Limitado a road disruption/status; exact profile/version/category aplicable debe fijarse en fuentes y no cubre P01 entero. | `SF-A05-P01-ROAD`; C01; M06_B02_POST_HUMAN_REVIEW.md; primary profile refs |
| `M06-B02-MAP-A05-P02-001-DATEX-ROAD-STATUS` | P02-001 | `M06-B02-CAP-DATEXII-RRP-ROAD-STATUS` | concept ROAD_STATUS_DISRUPTION P02 | PARTIAL / APPROVED | RTTI RRP para carretera; P02 condicionado y perfil solo para la rama/category aplicable. | `SF-A05-P02`; C04; M06_B02_POST_HUMAN_REVIEW.md; primary profile refs |
| `M06-B02-MAP-A05-P02-001-SIRI-PASSENGER-STATUS` | P02-001 | `M06-B02-CAP-SIRI-EPIPRT-PASSENGER-STATUS` | concept PASSENGER_RT_STATUS_DISRUPTION | PARTIAL / APPROVED | CEN/TS 15531-7:2025 EPIP-RT; ET/SX domains. No todo P02. | `SF-A05-P02`; C07; M06_B02_POST_HUMAN_REVIEW.md; CEN profile ref |
| `M06-B02-MAP-A05-P02-001-SIRI-FACILITY-STATUS` | P02-001 | `M06-B02-CAP-SIRI-EPIPRT-FACILITY-STATUS` | concept FACILITY_ACCESS_NODE_STATUS | PARTIAL / APPROVED | EPIP-RT facility scope, SIRI-FM. Annex-item a exact element(s) sigue limitado; no dar por mapeados automáticamente lifts, escaleras, entradas, salidas, andenes y paradas. | `SF-A05-P02`; C08; M06_B02_POST_HUMAN_REVIEW.md; CEN profile ref |

Los mapping IDs usan milestone + requirement + standard/scope; no incluyen versión para mantener identidad semántica estable. El mapping type refleja alcance parcial, no una assertion de representability ni cobertura global.

## Concept-mapping bridge proposals

Proponer cuatro filas en `mapping.phase3_concept_mappings`, una por mapping aceptado. Para cada par, `relation_note` registrará el enlace exacto concept↔capability, fuente/profile, qué cubre, qué no cubre y el origen C01/C04/C07/C08. No habrá bridge para U01/U02/U03 ni para ninguna decisión REJECT.

Chequeos previos/posteriores: `UNIQUE(concept_id,mapping_id)` es PK real; cada `concept_id` y `mapping_id` debe existir; comparar `concept.requirement_id = mapping.requirement_id`; el par requirement/capability debe ser único; abortar si el mapping ID ya existe con contenido divergente. No reusar un mapping legacy: los seis permanecen sin concept.

## Unmapped concepts

U01, U02 y U03 se pueden expresar separadamente con `scope_status=PARTIAL/UNRESOLVED`, review outcome no resuelto y sin capability, mapping ni bridge. Esto preserva cuestiones pendientes sin inferir que no hay datos ni que un estándar no podría cubrirlas. La decisión humana autoriza el estado de análisis, pero el seed aún necesita aprobación final de Yeison junto con el paquete.

## Coverage proposal

La tabla vigente solo tiene una decisión por requirement y no puede desglosar coverage por concept. No derivar `ESTABLISHED` al sumar mappings parciales.

| Requirement | Estado propuesto | Outcome | Motivo |
|---|---|---|---|
| P01-002 | PARTIAL | ACCEPTED_WITH_LIMITATIONS | C01 sustenta una rama de road status; no demuestra la cobertura de todos los datos/formatos dinámicos del requirement. |
| P02-001 | PARTIAL | ACCEPTED_WITH_LIMITATIONS | C04/C07/C08 dan rutas parciales; U01 y U03 siguen PARTIAL y U02 UNRESOLVED; mapping presence no implica cobertura total. |

Son dos decisiones nuevas de coverage, no decisiones ya tomadas en el human review. `review_status=NEEDS_REVIEW` hasta aprobación específica. Por ello, el paquete propone sus valores pero no los incluye en un seed ejecutable. El criterio de roll-up PARTIAL es metodológico y requiere aceptación humana; no introducir automatización de coverage.

## Representability readiness

No persistir representability. Candidatos documentales:

| Mapping | representability_candidate | Base y límite |
|---|---|---|
| P01 DATEX status | PARTIAL | El catálogo RTTI ofrece categorías y profile RRP; puente legal/contextual y selección exacta de perfil no cierran P01 completo. |
| P02 DATEX status | PARTIAL | Representable dentro de categorías road pertinentes; P02 entero condicional incluye otros conceptos. |
| P02 SIRI passenger status | PARTIAL | EPIP-RT define servicios y datos de pasajero; no todo Annex 2.1/2.2. |
| P02 SIRI facility status | NOT_READY | Familia/servicio identificables, pero crosswalk Annex item→elemento todavía incompleto. |

No se infiere presence, implementación ni dataset. `observed_evidence` permanece cero.

## Automatability notes

Análisis documental, no valores DB ni reglas de auditoría:

| Concept | Lectura provisional |
|---|---|
| ROAD_STATUS_DISRUPTION (P01/P02) | POTENTIALLY_AUTOMATABLE si se fija el RRP/profile y un dataset observable. |
| PASSENGER_RT_STATUS_DISRUPTION | POTENTIALLY_AUTOMATABLE para presencia/estructura de datos bajo profile definido; significado/calidad requeriría revisión. |
| FACILITY_ACCESS_NODE_STATUS | PARTIAL_MANUAL hasta completar crosswalk y contexto operativo. |
| PARKING_TARIFF / PARKING_AVAILABILITY | UNKNOWN |
| SHARED_VEHICLE_AVAILABILITY | UNKNOWN |

No se insertan filas `phase3_automatability` ni `audit.rules`.

## Dry-run

### Before

- Requirements: 48
- Concepts / mappings B02 / bridges: 0 / 0 / 0
- Mappings globales: 6
- Capability registry: 6 capabilities, 3 standards
- Coverage total: 8, ninguna para P01/P02
- Reviews mappings: 6; source references: 8
- Representability / observed evidence / audit rules: 0 / 0 / 0

### Proposed inserts (si se aprueba el paquete completo)

- Concepts: +7 (4 aceptados con límites, 2 PARTIAL y 1 UNRESOLVED)
- Standards: +1 identidad SIRI EPIP-RT; reutilizar DATEXII como identidad, conservando su estado y metadata actuales
- Capabilities: +3 (una DATEX road status, dos SIRI concept-scoped)
- Source references: +3 o más, según división por documento/servicio; nunca sobrescribir las ocho existentes
- Mappings: +4; mapping reviews: +4
- Concept bridges: +4
- Coverage: +2 solo tras decisión humana separada
- Representability, observed evidence, automatability: +0 / +0 / +0
- `audit.rules`: +0

### After (escenario autorizado futuro con los 2 coverage aprobados)

- Requirements 48; concepts 7; standards 4; capabilities 9
- Mappings globales 10, de los cuales legacy 6 y B02 4
- Mapping reviews 10; bridges 4; coverage 10
- Source references al menos 11; representability 0; observed evidence 0; automatability sin delta; audit.rules 0
- Phase 1/2 y objetos legacy: sin delta

Los totales de standards/source references pueden cambiar si la revisión final elige más granularidad de registro, pero el límite no altera semántica ni autoriza cambiar filas existentes. Antes de seed debe congelarse el delta exacto y validar ausencia/conflicto de todos los IDs.

## Expected deltas

| Tabla/área | Delta permitido en escenario completo | Delta prohibido |
|---|---:|---|
| `phase3_requirement_concepts` | +7 | Ningún concept para C02/C03/C05/C06 |
| `phase3_standards` | +1 SIRI EPIP-RT | No editar DATEX legacy ni otros standards |
| `phase3_capabilities` | +3 | No reciclar travel-time como road status |
| `phase3_source_references` | +3 mínimo propuesto | No actualizar ni reemplazar las 8 actuales |
| `phase3_requirement_capabilities` | +4 | No editar los 6 legacy ni automatability asociada |
| `phase3_mapping_reviews` | +4 | No reescribir reviews legacy |
| `phase3_concept_mappings` | +4 | Ningún bridge rechazado/Uxx/legacy |
| `phase3_requirement_coverage` | +2, tras aprobación separada | No alterar las 8 filas actuales |
| representability / observed evidence / automatability / `audit.rules` | 0 / 0 / 0 / 0 | Cualquier assertion/dato/regla B02 |

Sin aprobar ambas filas de coverage, limitar el seed al resto aprobado y el conteo de coverage se mantiene en ocho.

## Invariants

La persistencia futura debe verificar igualdad de IDs y filas antes/después para: 48 requirements, 92 provisions, 36 source facts, 10 deadlines, todos los objetos Phase 1/2; seis mappings legacy, seis reviews legacy, ocho coverage legacy, seis automatability legacy, source references legacy, seis exceptions sustantivas y sus relaciones; cero associations conceptuales legacy antes del seed, cero representability y observed evidence sustantivas, y cero `audit.rules`. La migración activa/schema vocabularies y su hash quedan sin cambios. Cualquier diferencia fuera de la tabla de deltas permitidos aborta transacción; no reparar ni completar silenciosamente.

## Persistence risks

1. La correspondencia legal MMTIS Article 5(1)(a)→RTTI 2022/670 sigue siendo funcional/contextual, no sustitución expresa de la referencia congelada a 2015/962. Mantenerlo como limitación y conservar la fuente literal.
2. DATEX II mantiene un registro amplio `IDENTITY_ONLY`; reutilizarlo como identidad técnica sin atribuirle el RTTI RRP exacto. La fila capability y la reference deben nombrar categoría/perfil aplicable.
3. C08 no tiene crosswalk completo Annex→SIRI-FM elements. El esquema permite mapping `PARTIAL`; el mapping no puede afirmarse completo ni convertir el límite en assertion de cobertura.
4. Provenance no es columna del mapping ni del bridge; requiere `relation_note`, source references y review rationale coordinados.
5. No hay concept-level coverage. Los dos valores requirement-level son decisiones humanas nuevas.
6. `UNIQUE(requirement_id, capability_id)` prohíbe duplicar pares. El diseño de tres capabilities evita duplicados y separa el scope de travel-time.
7. No hubo observación de dataset/implementación; no se puede promover representability a evidencia observada.

## Validation plan

Validación ejecutada antes del informe: consulta DuckDB `-readonly` para conteos actuales, identidades/capabilities y columnas reales; lectura del validator M06-B02 y migration SQL; fuentes primarias oficiales DATEX II y CEN; revisión de git status/branch. No se ejecutaron seeds.

Para esta propuesta, ejecutar solo el validator de esquema M06-B02 en modo `-readonly` (comprueba estado vacío/legacy, no valida futuros seeds), checks de schema/row count, y `git diff --check`. No correr validators de batch que esperen counts históricos incompatibles. No hay validator de filas pobladas B02 todavía; debe diseñarse/aprobarse para la futura persistencia, incluyendo bridges, requisitos coincidentes, rejects ausentes, conceptos sin mapping permitidos y coverage no derivado.

## Proposed seeds/migration artifacts

No se crea SQL ejecutable ni migración: la propuesta puede revisarse aquí y `B02_DATA_PERSISTENCE` sigue NOT_AUTHORIZED. Tras aprobación, preparar artefactos separados:

1. standard identity SIRI EPIP-RT y capability seeds;
2. concept seed con verificación exacta de columnas/semantic content;
3. mapping + review + concept bridge en la misma transacción;
4. source references sin modificar existentes;
5. coverage en operación transaccional separada, solo tras decisión expresa de coverage.

Regla de idempotencia para cada seed: `SELECT` por ID; si falta, insertar; si existe y todas las columnas semánticas coinciden exactamente, tratar como ya aplicada; si existe con cualquier conflicto, abortar. Verificar también unicidad natural (`requirement_id, concept_code`, requirement/capability), no sobrescribir ni usar `ON CONFLICT DO UPDATE`. Pre/post snapshots de filas legacy y conteos; rollback integral ante fallo antes de commit.

## Human decisions required

Antes de autorizar ejecución de seeds, Yeison debe:

1. Aprobar los siete concepts, sus códigos/descripciones, `scope_status`, fuente y provenance propuesta; en particular si persistir ya U01/U02/U03 como conceptos con estado abierto.
2. Aprobar tres capabilities nuevas y una identidad SIRI EPIP-RT; confirmar que DATEX road-status se comparte entre P01/P02 y travel-time existente queda excluido.
3. Aceptar los cuatro mappings PARTIAL y sus `ACCEPTED_WITH_LIMITATIONS`, IDs, limitations y crosswalks; mantener C02/C03/C05/C06 excluidos.
4. Confirmar qué RTTI category profile(s) se registrarán para C01/C04 y que la versión/modelo se deja explícitamente desconocida donde la fuente no la declara. No extender C01/C04 a P01/P02 completos.
5. Aceptar para C07 el ámbito ET/SX descrito y para C08 el mapping SIRI-FM acotado, sabiendo que Annex→element sigue parcial; o decidir bloquear ese mapping hasta cerrar ese crosswalk.
6. Aprobar separadamente las dos decisions de coverage PARTIAL / ACCEPTED_WITH_LIMITATIONS. Sin esto no insertar filas coverage.
7. Aprobar los deltas, provenance repartida entre tablas disponibles, fuentes oficiales que se capturarán y regla idempotente/abort-on-conflict.
8. Emitir una autorización explícita nueva para `B02_DATA_PERSISTENCE`; esta propuesta no la concede.

## Fuente técnica consultada

- DATEX II, [RTTI Recommended Reference Profiles](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/): perfiles categoría-específicos y alcance del catálogo RTTI 2022/670.
- DATEX II, [RRP Road Closures](https://docs.datex2.eu/v3.4/reference_profiles/rrp/rtti/drd-1-road-closures/index.html): perfil acotado para cierres; no se extrapola a todo road status.
- CEN-CENELEC, [SIRI Part 7 / EPIP-RT](https://www.cencenelec.eu/news-events/news/2025/eninthespotlight/2025-08-21-siri-7/): CEN/TS 15531-7:2025, ET/SX/VM/FM y ejemplos de pasajeros/instalaciones. Esta nota informativa confirma el perfil/dominio, no el mapeo legal completo.
- Fuentes y legal crosswalk completos en `M06_B02_POST_HUMAN_REVIEW.md` y `M06_B02_TARGETED_RESEARCH.md`; no reabren la fuente Phase 2 congelada.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
