# M06-B02C Partial Mapping Contract & Scoped Evaluation Design

Fecha: 2026-09-28. Estado: `READY_FOR_HUMAN_REVIEW` (diseño). `SCHEMA_CHANGE = PROPOSED_NOT_AUTHORIZED`; `B02_MAPPING_PERSISTENCE = NOT_AUTHORIZED`. Ninguna fila, migración, coverage, representability, observación o regla queda aprobada para escritura por este informe.

## Problem

Un concept aceptado con limitaciones puede contener unidades demostradas y otras pendientes. Una relación SIRI-FM que demuestra el estado de ascensores no representa por ello todo `FACILITY_ACCESS_NODE_STATUS`. El contrato debe conservar la frontera de cada prueba y permitir consultas sin interpretar notas libres.

## Current model

`phase3_requirement_capabilities` une requirement y capability (`mapping_id` PK, `UNIQUE(requirement_id, capability_id)`), con `mapping_type`, condiciones, límites y `review_status`. `phase3_concept_mappings` une concept y mapping N:M con PK `(concept_id,mapping_id)`; el requisito coincidente se comprueba por validator. `phase3_mapping_reviews` aporta outcome, justificación, límites, persona y fecha. `phase3_source_references` cuelga de capability. `phase3_standards` identifica familia/perfil, pero `IDENTITY_ONLY` no prueba una release de RRP. `phase3_requirement_coverage` contiene una decisión por requirement. Representability cuelga de capability; observed evidence admite capability y/o mapping. Ninguna de estas tablas registra unidades evaluadas con estados diferentes dentro de un mismo concept/mapping.

La inspección `duckdb -readonly` confirma siete concepts B02, cero mappings/bridges B02, seis mappings legacy, cero representability y observed evidence sustantivas y cero `audit.rules`. Los concepts U01/U02/U03 están persistidos y no requieren relaciones técnicas ficticias.

## Requirements

Conservar el puente N:M y los seis legacy intactos; una unidad evaluada debe pertenecer a un par concept–mapping existente. Diferenciar evidencia positiva, exclusión fundada y falta de demostración; fijar capability, perfil/versión, fuentes, limitación y revisión; mantener la decisión de coverage separada. Un cambio de fuente o versión exige nueva revisión de las unidades afectadas. C02/C03/C05/C06 siguen rechazados para estos requirements y no se incorporan mediante otra ruta nominal.

## Definition of partial mapping

`mapping_type = PARTIAL` designa una relación semántica revisada cuyo alcance demostrado está delimitado por unidades `INCLUDED` y cuyo resto evaluado queda visible como `EXCLUDED` o `UNRESOLVED`. Requiere al menos una unidad incluida con fuente identificable, límites explícitos y review semántica aceptada con limitaciones; si no se demuestra ninguna unidad, se conserva como candidato documental, sin mapping persistido. Un mapping parcial no es coverage `ESTABLISHED`, representabilidad íntegra del concept, implementación observada ni cumplimiento jurídico. `review_status = APPROVED` puede coexistir con `mapping_type = PARTIAL`: aprobación de la relación acotada, no de todo el concept.

El vocabulario actual ya contiene `PARTIAL` en `MAPPING_TYPE`, `APPROVED` en `REVIEW_STATE` y `ACCEPTED_WITH_LIMITATIONS` en la review. No se añade `ESTABLISHED`, `REJECTED` o `UNRESOLVED` como nuevos mapping types. `REJECTED` es un resultado de revisión/candidato y la política B02 no persiste mappings rechazados. `DIRECT`, `DERIVED` y `CONDITIONAL` describen modalidad distinta; para B02 con unidades pendientes se propone `PARTIAL`, expresando la condición en `mapping_conditions` hasta una revisión futura de la taxonomía.

## Scope semantics

Cada unidad tiene código estable solo dentro del par concept–mapping, etiqueta y definición positiva, `scope_disposition` y justificación. `INCLUDED` significa cruce semántico respaldado bajo la versión citada, no presencia de datos. `EXCLUDED` significa que la unidad evaluada no pertenece a esta relación técnica por una razón explícita; no significa que otro perfil no pueda representarla. `UNRESOLVED` significa que puede pertenecer al concept o a la relación, pero la evidencia no cierra ese cruce. Un elemento ajeno al concept, como vehicle position frente a C07, se documenta como límite de concept/candidato; solo se registra `EXCLUDED` en la relación si se evaluó expresamente y conviene conservar el rechazo trazable. Nunca se usa `EXCLUDED` para ocultar una ausencia de prueba.

La suma de unidades de un mapping no certifica exhaustividad del concept. El universo evaluado debe declararse en la revisión (`evaluated_scope_basis`, p. ej. Annex item y fecha); cualquier resto no enumerado impide conclusiones FULL. `UNRESOLVED` y `EXCLUDED` requieren razón; `INCLUDED` exige fuente concreta. No se crea subconcept: las unidades carecen de identidad jurídica/lifecycle independiente. Si en el futuro necesitan coverage, representability o revisión independientes de cualquier mapping, habrá que decidir una identidad propia.

## Architecture options

| Criterion | Option A: campos en mapping | Option B: unidades hijas | Option C: unidad global | Recommended |
|---|---|---|---|---|
| Traceability | Listas/JSON sin FK por unidad | PK y FK al par concept–mapping | Identidad estable transversal | B: traza suficiente para B02 |
| Normalization | Repite estado/fuente dentro de texto | Una fila por unidad y estado | Normaliza también decisiones futuras | B: separa hechos sin duplicar capas |
| Query simplicity | Una fila, parseo difícil | Join sencillo desde mapping | Múltiples relaciones/roles | B: consultas tipadas |
| Versioning | Una versión general oculta mezcla | Fuente por unidad y versión de perfil | Versionado independiente completo | B: revisar unidad afectada |
| Auditability/reporting | Ambigüedad al contar | Conteo y lista por disposición | Flexible, mayor disciplina de gobierno | B: filtros explícitos |
| Representability | No ofrece anchor estable | `scope_unit_id` bajo mapping | Anchor global reusable | B: scope unit como anchor futuro |
| Audit rules | Texto difícil de validar | Regla puede apuntar a unidad incluida | Potente para reglas transversales | B: evita inferir todo el concept |
| Estados distintos en concept | Posibles solo en arrays | Filas por unidad y mapping | Filas autónomas | B: estado por unidad |
| Riesgo de texto libre | Alto | Texto descriptivo más disposición y FK | Bajo si bien gobernada | B: evidencia vinculada |
| Legacy compatibility | Altera tabla padre con FKs | Objetos aditivos; cero backfill | Objetos aditivos pero más puentes | B: preserva seis filas |
| Migration risk | Alto: reconstrucción posible del subgrafo FK | Bajo, aditivo con validator | Medio: más objetos y conciliación | B: menor superficie |
| Long-term maintainability | Difícil controlar semántica | Dos objetos nuevos y gates | Mayor lifecycle y reconciliación | B hasta necesidad real de identidad global |

Option A, para C08, requeriría listas `included=[lift]`, `excluded=[]`, `unresolved=[escalator, platform, entrance, exit]` en el mapping FM; el esquema no podría comprobar cada elemento ni su fuente. Option B produce cinco filas tipadas bajo `(C08, mapping FM)`. Option C crearía cinco `evaluation_unit_id` globales y una relación por mapping, aun cuando hoy ninguna unidad tiene lifecycle propio. La matriz es cualitativa: la elección B conserva precisión y evita adelantar esa identidad global.

## Recommended model

Mantener `phase3_requirement_capabilities` como identidad de la relación requirement–capability y `phase3_concept_mappings` como N:M. Añadir, en una migración **futura y separada**, `phase3_mapping_scope_units`, hija de la pareja del bridge, y `phase3_scope_source_references` para asociar una o más fuentes existentes a cada unidad. La unidad se evalúa *bajo un mapping y capability concretos*; no pretende catalogar todo el concept universalmente. Un mismo concept puede tener dos mappings con unidades y estados distintos. Un mapping puede enlazar varios concepts y cada pareja conserva sus unidades.

`mapping_id` seguirá siendo el anchor de review semántica y automatability actuales. `scope_unit_id` es el anchor propuesto para representability, observación y reglas futuras cuando se evalúe una porción; esas capas no se crean ahora. No hay tabla `Evaluated Scope` global ni subconcepts nuevos.

## Schema proposal

**Propuesta, no SQL ejecutable aprobado.** Objetos nuevos:

| Objeto/campo | Contrato propuesto |
|---|---|
| `phase3_mapping_scope_units.scope_unit_id` | PK estable, no derivada de etiqueta editable. |
| `concept_id, mapping_id` | NOT NULL; FK compuesta a PK de `phase3_concept_mappings`. Así se exige bridge real. |
| `unit_code` | NOT NULL; `UNIQUE(concept_id,mapping_id,unit_code)`; no hay código `ALL`. |
| `unit_name, unit_definition` | Textos no vacíos, unidad atómica consultable; los códigos se gobiernan en el paquete revisado. |
| `scope_disposition` | CHECK `INCLUDED`, `EXCLUDED`, `UNRESOLVED`; vocabulario nuevo **solo** de disposición de unidad porque no existe equivalente en el esquema. No es mapping status ni coverage. |
| `basis_section, limitation, rationale` | Annex/criterio evaluado, límite y motivo; `limitation` obligatorio si existe incertidumbre. |
| `profile_artifact_ref` | Referencia a identidad/artefacto de perfil versionado cuando exista; no reemplaza `standard_id` de capability. Nullable solo para unidad no incluida con gap explícito. |
| `review_status, reviewed_at, reviewed_by` | Vocabulario de review existente; para `INCLUDED` se requiere revisión aprobada y fecha/persona. La review de mapping continúa en `phase3_mapping_reviews`. |
| `decision_document_id, milestone_id` | Referencias estructuradas al paquete de decisión y hito, validadas contra manifiesto documental futuro; no se presume FK inexistente. |
| `phase3_scope_source_references(scope_unit_id, source_reference_id, evidence_role)` | PK del par, FKs a unidad y `phase3_source_references`; `evidence_role` distingue soporte técnico de límite/contraejemplo, con vocabulario controlado futuro. Validator exige capability de la fuente = capability del mapping. |

No alterar tablas existentes en B02C. Para una migración posterior, decidir si `profile_artifact_ref` puede ser FK a registry ampliado; hoy `phase3_standards` solo guarda versión/perfil generales y `phase3_source_references` permite `version`, `section`, URL/documento y fecha, pero no fija por sí solo release inmutable de cada RRP/XSD. No insertar una release inferida. `mapping_id` ya determina requirement/capability; `concept_id` ya determina requirement. No duplicar esas columnas en cada unidad. `mapping_type`, `review_status`, limitaciones y review humana siguen en sus tablas actuales.

## Mapping-status contract

La relación parcial usa `mapping_type=PARTIAL`, `review_status=APPROVED` solo después de revisión humana, `phase3_mapping_reviews.semantic_review_outcome=ACCEPTED_WITH_LIMITATIONS`, limitaciones no vacías y al menos una unidad `INCLUDED` revisada. `UNRESOLVED` no se persiste como mapping sin porción demostrada. `REJECTED` queda en el expediente de candidato y no origina mapping, bridge o scope unit. Un mapping con `DIRECT`/`DERIVED` y unidad `UNRESOLVED` en el mismo par sería inconsistente hasta revisión; no se convierte automáticamente en FULL aunque todas las unidades listadas sean `INCLUDED`.

## Profile/version contract

Cadena: mapping → capability → `standard_id`; unidad → fuente(s) específicas con `specification_name`, `version`, `section`, `url_or_document_id`, `retrieved_on`; registro de artefacto/release cuando exista. Distinguir versión de norma, perfil, RRP/categoría, modelo, XSD y despliegue. `M03-DATEXII-MMTIS-RRP` es `IDENTITY_ONLY`, no identidad de los ocho RTTI RRP ni prueba de DATEX II 3.7 para ellos. SIRI EPIP-RT CEN/TS 15531-7:2025 y SIRI 2.1 están identificados documentalmente, pero falta XSD/restricciones completas. Bloquear una unidad `INCLUDED` si la versión exacta necesaria para su afirmación no se puede localizar; una fuente viva con fecha puede sustentar identidad de categoría y dejar release `UNRESOLVED`. El registry necesita granularidad adicional antes de una futura persistencia versionada; no se modifica aquí.

## Provenance

El mapping responde a quién lo aprobó mediante `phase3_mapping_reviews.reviewed_by/reviewed_at`, a qué se aceptó mediante outcome/justificación, y a fuentes técnicas mediante los links por unidad. `decision_document_id` apunta al human review B02 y `milestone_id` a B02C o revisión sucesora; ambos requieren manifiesto/control de rutas antes de persistir. Un cambio de fuente/version/alcance invalida solo la aprobación de las unidades afectadas y obliga a re-review del mapping si cambia su frontera. `relation_note` conserva el vínculo concept–mapping, no sirve como depósito único de provenance. La fuente legal congelada y la interpretación informativa del handbook permanecen separadas.

## Coverage implications

**Change required now: NO.** `phase3_requirement_coverage` conserva una decisión semántica humana por requirement. Una unidad incluida puede aportar evidencia para esa decisión, sin calcularla mecánicamente. U01/U02/U03 y la aplicabilidad condicional impiden declarar P02 FULL solo por C04/C07/C08. Si más adelante se necesita desglose persistido, añadir coverage por concept/unidad y un agregado explícito revisado; no reutilizar `scope_disposition` como `coverage_state`.

## Representability implications

La tabla actual ancla `capability_id` y sirve para capacidad general, pero no separa lifts de plataformas. Futuro anchor recomendado: `scope_unit_id` más `mapping_id` recuperable y perfil/version fijados; conservar la assertion capability-level para preguntas generales. Solo una unidad `INCLUDED` y revisada puede plantear representability `AVAILABLE`/`MAPPABLE` bajo ese perfil; aún exige evaluación específica. Una unidad `UNRESOLVED` no es `MISSING`, y ninguna suma de assertions declara representabilidad íntegra del concept.

## Observed evidence implications

Una futura observación necesitará dataset/implementación, locator, fecha, versión efectiva y `scope_unit_id`; los anchors actuales capability/mapping continúan para legacy. Distinguir `present`, `absent after inspection` y `not inspected` en un contrato futuro; cero filas hoy no significan ausencia de datos. No ampliar `phase3_observed_evidence` en esta misión.

## Audit-rule implications

Una regla futura apuntará a unidad `INCLUDED` revisada, estructura técnica esperada y versión/perfil, luego a evidencia y finding. Ante un resultado inesperado se comprobarán especificación, interpretación, validador, scope, versión, input y ejecución antes de atribuir defecto al operador (lección Bizkaibus). `audit.rules` sigue en cero; ninguna regla o estado de finding se propone aquí.

## Legacy compatibility

Los seis mappings legacy conservan filas, reviews, constraints y cero concept bridges/scopes. La ausencia de scope estructurado significa “no revisado a esta granularidad”, no `ALL`, FULL ni inválido. Cualquier backfill requiere revisión humana nueva y migración aparte. U01/U02/U03 continúan como concepts sin mapping ni unidad hija; “no mapping yet” no requiere fila técnica artificial.

## C01/C04 example

Ejemplo **de diseño, no seed**. C01 `EU-2017-1926-REQ-A05-P01-002` y C04 `EU-2017-1926-REQ-A05-P02-001` conservan dos concept IDs `ROAD_STATUS_DISRUPTION`. El R1 recomienda ocho capabilities por RRP: 4-SN-A/B/C/D y 5-SN-A/B/C/D (road/lane closures, roadworks, temporary management, bridge closures, accidents/incidents, poor conditions, weather impact). Una capability de categoría puede compartirse entre requisitos, pero cada pareja requirement–capability recibe `mapping_id` propio y bridge al concept de ese requirement: hasta 8×2 relaciones, solo tras selección de categorías aplicables. Cada pareja tendría unidad `INCLUDED` para la identidad/alcance de categoría demostrado; cualquier subalcance del concept cuya correspondencia no se haya demostrado iría en unidad `UNRESOLVED`. La incertidumbre sobre release/constraints se guarda como limitación y gap de perfil, no como falsa unidad de scope. Categorías no aplicables a C04 se omiten, no se fingen como excluidas del concept. La fuente de cada unidad es la página RRP correspondiente; limitaciones: release exacta por RRP, bridge legal informativo para C01 y aplicabilidad Art. 5(2) para C04. La propuesta agregada anterior `...DATEX-ROAD-STATUS` no sirve como ID de ocho mappings distintos con la unicidad actual; sus IDs deben aprobarse en un futuro paquete. `CAP-DATEXII-RRP-ROAD-TRAVEL` no se usa para B02.

| C01/C04 concept | Capability propuesta compartida | Mapping propuesto por requirement | Unidad evaluada y estado documental | Fuente y límite |
|---|---|---|---|---|
| `ROAD_STATUS_DISRUPTION` en P01 y P02 | `CAP-DATEXII-RRP-ROAD-CLOSURE` | `MAP-P01-4-SN-A` / `MAP-P02-4-SN-A` | `ROAD_CLOSURE`: categoría identificada; relación `PARTIAL` | R1, RRP 4-SN-A; release y puente legal/aplicabilidad abiertos |
| idem | `CAP-DATEXII-RRP-LANE-CLOSURE` | `MAP-P01-4-SN-B` / `MAP-P02-4-SN-B` | `LANE_CLOSURE`: categoría identificada; `PARTIAL` | R1, 4-SN-B; mismo límite |
| idem | `CAP-DATEXII-RRP-ROADWORKS` | `MAP-P01-4-SN-C` / `MAP-P02-4-SN-C` | `ROADWORKS`: categoría identificada; `PARTIAL` | R1, 4-SN-C; mismo límite |
| idem | `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT` | `MAP-P01-4-SN-D` / `MAP-P02-4-SN-D` | `TEMP_TRAFFIC_MGMT`: categoría identificada; `PARTIAL` | R1, 4-SN-D; mismo límite |
| idem | `CAP-DATEXII-RRP-BRIDGE-CLOSURE` | `MAP-P01-5-SN-A` / `MAP-P02-5-SN-A` | `BRIDGE_CLOSURE`: categoría identificada; `PARTIAL` | R1, 5-SN-A; mismo límite |
| idem | `CAP-DATEXII-RRP-ACCIDENT-INCIDENT` | `MAP-P01-5-SN-B` / `MAP-P02-5-SN-B` | `ACCIDENT_INCIDENT`: categoría identificada; `PARTIAL` | R1, 5-SN-B; mismo límite |
| idem | `CAP-DATEXII-RRP-POOR-ROAD-CONDITION` | `MAP-P01-5-SN-C` / `MAP-P02-5-SN-C` | `POOR_ROAD_CONDITION`: categoría identificada; `PARTIAL` | R1, 5-SN-C; mismo límite |
| idem | `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT` | `MAP-P01-5-SN-D` / `MAP-P02-5-SN-D` | `ROAD_WEATHER_IMPACT`: categoría identificada; `PARTIAL` | R1, 5-SN-D; release y etiqueta interna “RSP” pendientes |

Los `MAP-P01/P02-*` son claves didácticas, no IDs persistibles. Cada pareja se materializaría solo con un ID definitivo, review `ACCEPTED_WITH_LIMITATIONS`, fuente de categoría enlazada a la unidad y selección de aplicabilidad aprobada. La disposición `INCLUDED` quedaría restringida a la **identidad/alcance de categoría** demostrado; la representabilidad de elementos y release exacta sigue `UNRESOLVED` y no se afirma con esa fila.

## C07 example

Concept `M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION`. Para auditar servicios por separado, proponer capability ET y capability SX, cada una con mapping P02 propio y bridge al mismo concept. ET tendría unidades `INCLUDED` para retrasos/cancelaciones de journey/call; SX una para avisos de disrupción/impacto. Ambas quedarían `PARTIAL` por el crosswalk Annex→elemento pendiente, con fuente EPIP-RT CEN/TS 15531-7:2025 / SIRI 2.1 y límites de XSD/constraints. CM/guaranteed connections solo figura como candidato a investigar: R2 no demuestra su aplicabilidad al C07 actual, por lo que no recibe capability ni mapping ni unidad `INCLUDED`. VM/posición de vehículo queda fuera del concept. La alternativa de capability ET+SX agregada de R2 es documental; separarla aquí responde a la necesidad de review/version/regla independiente por servicio y precisa aprobación humana antes de persistencia.

| Servicio | Capability/mapping propuestos | Scope y disposición | Fuente / limitación |
|---|---|---|---|
| ET | `CAP-SIRI-EPIPRT-ET` / `MAP-P02-ET` | `JOURNEY_DELAY_CANCELLATION` `INCLUDED` en alcance funcional; mapping `PARTIAL` | R2, EPIP-RT §8 y SIRI-ET; campo/constraint Annex exactos pendientes |
| SX | `CAP-SIRI-EPIPRT-SX` / `MAP-P02-SX` | `PASSENGER_DISRUPTION_NOTICE` `INCLUDED` en alcance funcional; mapping `PARTIAL` | R2, EPIP-RT §7 y SIRI-SX; impacto/validez exactos pendientes |
| CM | Sin capability ni mapping | Guaranteed connections por investigar; ninguna unidad `INCLUDED` | R2 no cierra este bridge para C07 |

Estos IDs ET/SX son didácticos. Cada mapping requiere review `ACCEPTED_WITH_LIMITATIONS`; `INCLUDED` designa el servicio/caso funcional documentado, no conformidad de campos ni presencia observada.

## C08 stress test

Concept `M06-B02-CPT-A05-P02-001-FACILITY-ACCESS-NODE-STATUS`; una capability SIRI-FM estrecha, un mapping P02–FM `PARTIAL` y su bridge. Ejemplo exacto de **filas propuestas, no persistidas** bajo ese par:

| `unit_code` | Disposition según evidencia R2 hoy | Fuente/limitación |
|---|---|---|
| `LIFT_OPERATIONAL_STATUS` | `INCLUDED` | EPIP-RT FM, caso “Elevator out of business”; elementos/constraints exactos pendientes. |
| `ESCALATOR_OPERATIONAL_STATUS` | `UNRESOLVED` | R2 considera FM pertinente, pero no demuestra caso/elemento escalator específico. |
| `PLATFORM_OPERATIONAL_STATUS` | `UNRESOLVED` | ET platform change no demuestra estado operativo de la instalación. |
| `ENTRANCE_CLOSURE_STATUS` | `UNRESOLVED` | Elemento FM exacto no localizado. |
| `EXIT_CLOSURE_STATUS` | `UNRESOLVED` | Elemento FM exacto no localizado. |

El ejemplo deseado de lift+escalator `INCLUDED` cabe en la opción B cambiando solo la disposición/review de `ESCALATOR_OPERATIONAL_STATUS` tras nueva prueba; **hoy no está demostrado**. Si se añade un elemento realmente fuera de la relación FM, tendría una fila `EXCLUDED` con motivo y fuente, nunca se reclasificaría una de las cuatro incertidumbres como exclusión. El mapping permanece PARTIAL y no da representabilidad completa de C08. En A estas cinco disposiciones serían listas sin integridad por elemento; en C serían cinco identidades globales con lifecycle aún injustificado.

## Migration plan

**Required for future persistence: YES; executed: NO.** Precheck de ruta/hash DB, esquema/constraints y exactitud de 48 requirements, 7 concepts, 6 mappings/reviews legacy, 8 coverage, 6 automatability, cero representability/evidence/rules y Phase 1/2 (92/36/48/10); snapshots por PK y contenido, no solo conteos. Verificar ausencia de objetos nuevos e IDs en conflicto. Migración aditiva en transacción: vocabulario de disposición y roles de fuente, `phase3_mapping_scope_units` y tabla de links, FK compuesta al bridge, FK a source references, CHECKs de no vacío/estados y unique por pareja+código; índices en `mapping_id`, `concept_id` y `source_reference_id` según consultas. No alterar mapping padre ni su `UNIQUE(requirement_id,capability_id)`; scope no exige backfill y los seis legacy quedan sin filas. Las constraints intertabla (requirement igual, capability de fuente igual, unidad incluida con revisión/fuente) se comprueban en validator y en precommit, no se fingen como CHECK local. Si falla cualquier pre/postcheck, `ROLLBACK` integral, conservar evidencia de fallo, comparar hash y no sustituir expectativa histórica. Un seed futuro de datos B02 necesitará autorización distinta, IDs finales, fuentes/versiones fijadas y revisión de cada unidad.

## Validator plan

Gate futuro poblado: FK/huérfanos, unicidad, vocabulario, no vacíos; concept y mapping con mismo requirement; source reference y mapping con misma capability; `PARTIAL` aprobado con al menos una unidad `INCLUDED` aprobada, evidence link y límites; `UNRESOLVED`/`EXCLUDED` con rationale y sin inferencia de cobertura; mapping `DIRECT`/FULL-like incompatible con unidades sin resolver; candidate rejects C02/C03/C05/C06 ausentes; U01/U02/U03 sin filas técnicas; seis legacy byte a byte y sin scope; Phase 1/2 y contadores protegidos sin delta. Comprobar perfil, versión, artefacto, fecha y documento de decisión antes de aprobar unidades incluidas. Separar gate de esquema de gate de datos para no invalidar los validators históricos B02A cuando una futura persistencia cambie los conteos. B02C no cambia SQL de validators.

## Risks

- El registro `IDENTITY_ONLY` DATEX y fuentes web vivas no fijan release por RRP; aprobar un `INCLUDED` más fuerte que la fuente produciría falsa precisión.
- El handbook de la Comisión sustenta una interpretación informativa, no equivalencia legislativa ni modificación del source fact congelado.
- Una unidad hija de mapping no representa por sí sola un concept sin mapping; U01/U02/U03 permanecen a nivel concept y requieren investigación.
- `UNIQUE(requirement_id,capability_id)` impide mappings duplicados con la misma capability bajo un requisito; los servicios/categorías con evaluación independiente necesitan capabilities distintas o una revisión explícita de cardinalidad.
- El estado aprobado de una unidad puede quedar obsoleto por versión; hace falta política de re-review y artefacto inmutable antes de persistencia.

## Open questions

1. ¿Qué artefacto/release inmutable y registry granulado respaldará cada RRP DATEX II y servicio/XSD SIRI?
2. ¿Qué unidades C04 son realmente aplicables bajo Art. 5(2), y qué fuente cierra cada bridge?
3. ¿El texto íntegro EPIP-RT confirma escalators y campos de platform/entrance/exit? ¿CM pertenece al C07 evaluado?
4. ¿Cómo se identificará y versionará el manifiesto de decisiones humanas para FKs documentales antes del seed?

## Validation (read-only)

Comandos: `duckdb -no-init -batch -bail -readonly 03_Compliance/databases/transit_compliance.duckdb -json -f <validator>`. Cada ejecución terminó con exit code 0; ninguna fue seed o migración.

| Gate | Resultado observado |
|---|---|
| `validate_phase_3_m06_b02a_populated_schema.sql` | PASS; 13 checks, 0 failures |
| `validate_phase_3_m06_b02a_requirement_concepts.sql` | PASS; 11 checks, 0 failures |
| `validate_phase_3_level_a.sql` | PASS; 6 mappings, 6 capabilities, 6 exceptions; 0 referencias/estados/razones inválidas |
| `validate_phase_3_exception_accounting.sql` | PASS; 3 M04 + 3 B01; 0 excepciones sin cuenta o incompatibles |
| `validate_phase_3_m04b_semantic_coverage.sql` | PASS; 0 structural failures, 8 coverage decisions, 6 mapping reviews; cinco regresiones true |
| `git diff --check` | Exit 0; aviso de conversión CRLF en `PROJECT_STATUS.md` preexistente. El archivo nuevo, aún untracked, se comprobó directamente: 0 líneas con whitespace final y newline final presente. |

SHA-256 de `transit_compliance.duckdb` antes y después: `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`. `DB_WRITES = 0`; DB modificada: NO. La comprobación de esquema poblado es el gate vigente; no se ejecutó el gate histórico `EMPTY_SCHEMA_ONLY`. `PROJECT_STATUS.md` y los demás cambios locales preexistentes quedaron intactos.

## Human decision required

Yeison debe aprobar **el contrato y la migración futura concretos**: opción B, granularidad de capability/mapping por RRP y por ET/SX, los tres estados de unidad y sus condiciones, esquema/FKs/validators, estrategia de perfil y artefacto versionado, provenance y preservación legacy. Esa aprobación sería solo autorización de diseño/migración si se formula así; cualquier ejecución de esquema y cualquier persistencia B02 exigen autorización explícita posterior y paquete de IDs/fuentes/reviews revisable. En particular, la dirección metodológica ya aprobada no autoriza convertir escalators o CM en soportados.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
