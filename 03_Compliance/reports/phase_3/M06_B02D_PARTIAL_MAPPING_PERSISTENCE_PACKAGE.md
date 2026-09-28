# M06-B02D Partial Mapping Persistence Package

Fecha: 2026-09-28. Estado: `M06_B02D_PARTIAL_MAPPING_PACKAGE = READY_FOR_HUMAN_REVIEW`; `B02_PARTIAL_MAPPING_PERSISTENCE = NOT_AUTHORIZED`.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Scope

Paquete documental y dry-run de C01, C04, C07 y C08. No se ejecutaron seeds ni se escribieron capabilities, mappings, concept bridges, scope units, referencias, coverage, representability, observed evidence, automatizability ni audit rules. No se modificó el esquema.

La propuesta solo plantea mappings `PARTIAL`. `PARTIAL` describe el vínculo técnico acotado y no implica cobertura completa, representabilidad, implementación observada o cumplimiento jurídico. Los estados `INCLUDED`, `UNRESOLVED` y `EXCLUDED` se limitan a unidades de alcance evaluadas bajo un mapping concreto.

## Current authoritative state

La base consultada con DuckDB `-readonly` es `03_Compliance/databases/transit_compliance.duckdb`.

| Control | Estado observado |
|---|---:|
| Requirements | 48 |
| Concepts B02 | 7 (1 P01, 6 P02) |
| Mappings globales no sintéticos | 6 |
| Mappings B02 | 0 |
| Concept bridges B02 | 0 |
| Scope units B02 | 0 |
| Coverage B02 | 0 |
| Observed evidence global | 0 |
| `audit.rules` | 0 |
| `phase3_mapping_scope_units` | existe |
| `phase3_scope_source_references` | existe |
| Source references actuales | 8 |

Los siete conceptos persisten bajo los IDs M06-B02A y conservan los estados de revisión documentados. Los seis mappings legacy y sus seis capabilities se mantienen intactos. U01 = PARTIAL, U02 = UNRESOLVED y U03 = PARTIAL; siguen fuera del paquete técnico.

SHA-256 inicial de la DB: `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`.

## Persistence policy

El contrato real separa los campos: `mapping.phase3_requirement_capabilities.review_status` solo admite estados de workflow (`NEEDS_REVIEW`, `APPROVED`, etc.); `ACCEPTED_WITH_LIMITATIONS` pertenece a `phase3_mapping_reviews.semantic_review_outcome`. Por tanto, el dry-run deja los mappings en `NEEDS_REVIEW` y propone el resultado semántico `ACCEPTED_WITH_LIMITATIONS` únicamente para decisión humana. No se registra una aceptación humana por adelantado. Si se autorizara persistencia, cada mapping tendría `mapping_type=PARTIAL`, limitaciones explícitas, provenance y fuente técnica vinculada a la unidad correspondiente.

Los bridges futuros enlazarían cada mapping solo con el concept del mismo requirement. Las filas C04 no se proponen para inserción hasta demostrar la aplicabilidad del Art. 5(2) por categoría. Una capability puede compartirse entre C01/C04, pero sus mappings y bridges continuarían separados.

Todo seed futuro deberá insertar si falta, comparar la fila completa si ya existe y abortar ante conflicto semántico. No se autoriza un `UPDATE` silencioso. Este paquete no incluye seeds ejecutables.

## DATEX II capability package

Se proponen ocho capabilities independientes, todas `CREATE_NEW`, vinculadas a `M03-DATEXII-MMTIS-RRP`. No se reutiliza `CAP-DATEXII-RRP-ROAD-TRAVEL`, cuyo alcance registrado son tiempos de viaje.

| Capability | RRP / alcance técnico acotado | Release/version disponible | Source reference propuesta | Limitación y readiness |
|---|---|---|---|---|
| `CAP-DATEXII-RRP-ROAD-CLOSURE` | 4-SN-A, Road closures; eventos de cierre localizados | RTTI 670/2022; release de modelo/perfil individual no fijada | `M06-B02D-SRC-DATEX-4-SN-A`, página RRP 4-SN-A | `READY_FOR_PARTIAL_PERSISTENCE`; alta confianza en identidad RRP, release exacta abierta |
| `CAP-DATEXII-RRP-LANE-CLOSURE` | 4-SN-B, Lane closures | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-4-SN-B` | `READY_FOR_PARTIAL_PERSISTENCE`; misma limitación de release |
| `CAP-DATEXII-RRP-ROADWORKS` | 4-SN-C, Roadworks | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-4-SN-C` | `READY_FOR_PARTIAL_PERSISTENCE`; misma limitación de release |
| `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT` | 4-SN-D, Temporary traffic management measures | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-4-SN-D` | `READY_FOR_PARTIAL_PERSISTENCE`; acotada a medidas temporales |
| `CAP-DATEXII-RRP-BRIDGE-CLOSURE` | 5-SN-A, Bridge closures | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-5-SN-A` | `READY_FOR_PARTIAL_PERSISTENCE`; misma limitación de release |
| `CAP-DATEXII-RRP-ACCIDENT-INCIDENT` | 5-SN-B, Accidents and incidents | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-5-SN-B` | `READY_FOR_PARTIAL_PERSISTENCE`; no extiende a cualquier peligro SRTI |
| `CAP-DATEXII-RRP-POOR-ROAD-CONDITION` | 5-SN-C, Poor road conditions | RTTI 670/2022; modelo individual sin fijar | `M06-B02D-SRC-DATEX-5-SN-C` | `READY_FOR_PARTIAL_PERSISTENCE`; acotada a condiciones adversas de carretera |
| `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT` | 5-SN-D, Weather conditions affecting road surface and visibility | RTTI 670/2022; release individual por confirmar | `M06-B02D-SRC-DATEX-5-SN-D` | `READY_FOR_PARTIAL_PERSISTENCE`; conservar la nota de identidad interna “RSP” pendiente de aclaración |

En todas las capabilities el alcance semántico propuesto son eventos/estados de la categoría RRP indicada, con las clases de evento y límites de localización/validez descritos en su página. La familia de páginas no fija una release de modelo DATEX II común e inmutable para cada perfil. El catálogo expone modelos hasta 3.7, pero no se atribuye 3.7 a estos perfiles por inferencia. La versión quedaría expresada como `RTTI 670/2022; profile-specific model release unresolved`.

## C01 mapping package

Requirement `EU-2017-1926-REQ-A05-P01-002`; concept `M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION`. Readiness del paquete: `READY_FOR_PARTIAL_PERSISTENCE`, sujeto a revisión humana de los ocho mappings propuestos abajo.

Cada mapping se limita a un RRP y a su unidad de categoría. La base congelada cita 2015/962, mientras el handbook de MMTIS aporta interpretación informativa del carácter dinámico de la referencia. Se conserva el texto legal original; no se declara equivalencia o modificación normativa. El mapping resultante es técnico y parcial, no una conclusión jurídica.

| Mapping ID propuesto | Capability | Scope unit | Disposition | Fuente técnica |
|---|---|---|---|---|
| `M06-B02-MAP-A05-P01-002-DATEX-4-SN-A` | `CAP-DATEXII-RRP-ROAD-CLOSURE` | `ROAD_CLOSURE` | INCLUDED | RRP 4-SN-A |
| `M06-B02-MAP-A05-P01-002-DATEX-4-SN-B` | `CAP-DATEXII-RRP-LANE-CLOSURE` | `LANE_CLOSURE` | INCLUDED | RRP 4-SN-B |
| `M06-B02-MAP-A05-P01-002-DATEX-4-SN-C` | `CAP-DATEXII-RRP-ROADWORKS` | `ROADWORKS` | INCLUDED | RRP 4-SN-C |
| `M06-B02-MAP-A05-P01-002-DATEX-4-SN-D` | `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT` | `TEMP_TRAFFIC_MGMT` | INCLUDED | RRP 4-SN-D |
| `M06-B02-MAP-A05-P01-002-DATEX-5-SN-A` | `CAP-DATEXII-RRP-BRIDGE-CLOSURE` | `BRIDGE_CLOSURE` | INCLUDED | RRP 5-SN-A |
| `M06-B02-MAP-A05-P01-002-DATEX-5-SN-B` | `CAP-DATEXII-RRP-ACCIDENT-INCIDENT` | `ACCIDENT_INCIDENT` | INCLUDED | RRP 5-SN-B |
| `M06-B02-MAP-A05-P01-002-DATEX-5-SN-C` | `CAP-DATEXII-RRP-POOR-ROAD-CONDITION` | `POOR_ROAD_CONDITION` | INCLUDED | RRP 5-SN-C |
| `M06-B02-MAP-A05-P01-002-DATEX-5-SN-D` | `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT` | `ROAD_WEATHER_IMPACT` | INCLUDED | RRP 5-SN-D; confirmar etiqueta “RSP” y release |

La inclusión indica que la categoría RRP trata cierres, obras, incidentes o condiciones que afectan al estado/disrupción vial del concept acotado. No afirma que el NAP publique esa categoría, que todos sus campos sean representables en el perfil aplicable ni que C01 esté cubierto por completo. La referencia exacta a 2015/962 y su relación con el régimen sucesor permanece como limitación sustantiva; requiere aceptación humana explícita para sostener esta propuesta.

## C04 mapping package

Requirement `EU-2017-1926-REQ-A05-P02-001`; concept `M06-B02-CPT-A05-P02-001-ROAD-STATUS-DISRUPTION`. Estado: `NOT_READY` para persistencia parcial.

El Art. 5(2) conserva una condición: solo aplica donde SIRI/DATEX II corresponda a los puntos 2.1/2.2 del Annex. Las fuentes disponibles identifican perfiles RTTI 670/2022, pero no cierran de forma suficiente el puente entre cada RRP 4/5 y la categoría Annex aplicable a este requirement. Las ocho capabilities propuestas para C01 podrían reutilizarse (`REUSE_EXISTING` en caso de autorizarse C01), pero no se crea un mapping C04 vacío de scope incluido ni se duplican capabilities por requirement.

| Mapping alternativo (no insertar) | Capability reutilizable | Scope C04 ahora | Condición explícita |
|---|---|---|---|
| `M06-B02-MAP-A05-P02-001-DATEX-4-SN-A` | `CAP-DATEXII-RRP-ROAD-CLOSURE` | UNRESOLVED | Art. 5(2); probar categoría Annex y aplicabilidad |
| `M06-B02-MAP-A05-P02-001-DATEX-4-SN-B` | `CAP-DATEXII-RRP-LANE-CLOSURE` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-4-SN-C` | `CAP-DATEXII-RRP-ROADWORKS` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-4-SN-D` | `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-5-SN-A` | `CAP-DATEXII-RRP-BRIDGE-CLOSURE` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-5-SN-B` | `CAP-DATEXII-RRP-ACCIDENT-INCIDENT` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-5-SN-C` | `CAP-DATEXII-RRP-POOR-ROAD-CONDITION` | UNRESOLVED | Igual |
| `M06-B02-MAP-A05-P02-001-DATEX-5-SN-D` | `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT` | UNRESOLVED | Igual; confirmar perfil/release |

Los IDs son propuestas condicionadas, no mappings listos para seed. Una vez cerrada la applicability, C04 requerirá mappings y bridges separados de C01 aunque reutilice las mismas capabilities. Hasta entonces no forma parte del dry-run de inserción.

## SIRI capability package

El perfil identificado es EPIP-RT, CEN/TS 15531-7:2025, sobre SIRI 2.1 revisado (2021). La preview consultada no es el texto normativo íntegro y no fija el XSD nacional/de despliegue.

| Capability | Decision | Servicio y alcance | Fuente propuesta | Version/confidence/limitación |
|---|---|---|---|---|
| `CAP-SIRI-EPIPRT-ET` | CREATE_NEW | ET: estado estimado de journeys/calls, demoras, cancelaciones y cambios documentados | `M06-B02D-SRC-SIRI-EPIPRT-ET`, EPIP-RT §8 | CEN/TS 15531-7:2025; SIRI 2.1. Alta confianza en identidad del perfil; correspondencia Annex→elemento parcial |
| `CAP-SIRI-EPIPRT-SX` | CREATE_NEW | SX: avisos de situación/disrupción, impactos y consecuencias | `M06-B02D-SRC-SIRI-EPIPRT-SX`, EPIP-RT §7 | Misma versión. Alta confianza en servicio; detalle completo de constraints/elementos pendiente |
| `CAP-SIRI-EPIPRT-FM-FACILITY-STATUS` | CREATE_NEW | FM: slice de estado de instalaciones/equipos; no declara cobertura general de nodos | `M06-B02D-SRC-SIRI-EPIPRT-FM`, EPIP-RT §10 | Misma versión; evidencia de preview limitada. Vínculo exacto a elementos Annex pendiente |

No se reutiliza una capability genérica de todo SIRI. CM permanece `UNRESOLVED / pending evidence` y no genera capability, mapping o unidad persistible. VM queda fuera de C07; monitorización/posición de vehículos no demuestra el estado de servicio/disrupción del concept.

## C07 mapping package

Requirement `EU-2017-1926-REQ-A05-P02-001`; concept `M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION`. Readiness: `READY_FOR_PARTIAL_PERSISTENCE` para ET y SX, con dos mappings independientes. El cruce exhaustivo del Annex con elementos y constraints sigue abierto.

| Mapping ID propuesto | Servicio/capability | Scope unit | Disposition | Límite |
|---|---|---|---|---|
| `M06-B02-MAP-A05-P02-001-SIRI-ET` | ET / `CAP-SIRI-EPIPRT-ET` | `JOURNEY_DELAY_CANCELLATION` | INCLUDED | Casos de demora/cancelación demostrados a nivel de servicio; no prueba todos los campos/constraints del Annex |
| `M06-B02-MAP-A05-P02-001-SIRI-SX` | SX / `CAP-SIRI-EPIPRT-SX` | `PASSENGER_DISRUPTION_NOTICE` | INCLUDED | Aviso/impacto de disrupción demostrado a nivel de servicio; alcance exacto de cada elemento pendiente |

La identidad de perfil/version está suficientemente determinada para describir los candidatos como parciales. SIRI-CM y el seguimiento de conexiones garantizadas continúan como candidatos de investigación sin mapping, porque la evidencia cerrada no demuestra ese bridge en el concept C07. No se crea una unidad huérfana bajo ET/SX para representar CM.

## C08 mapping package

Requirement `EU-2017-1926-REQ-A05-P02-001`; concept `M06-B02-CPT-A05-P02-001-FACILITY-ACCESS-NODE-STATUS`. Readiness: `READY_FOR_PARTIAL_PERSISTENCE` como candidato estrecho, condicionado a que la revisión humana acepte una rebanada FM parcial. Una capability y un mapping; nunca cobertura total del concept.

Mapping propuesto: `M06-B02-MAP-A05-P02-001-SIRI-FM-FACILITY-STATUS`, `mapping_type=PARTIAL`, capability `CAP-SIRI-EPIPRT-FM-FACILITY-STATUS`.

| Scope unit | Disposition | Base documental y limitación |
|---|---|---|
| `LIFT_OPERATIONAL_STATUS` | INCLUDED | EPIP-RT FM incluye el caso “Elevator out of business”; campos/constraints normativos exactos no verificados en la preview |
| `ESCALATOR_OPERATIONAL_STATUS` | UNRESOLVED | Pertinencia de FM no demuestra un elemento/caso de escalera mecánica dentro de EPIP-RT |
| `PLATFORM_OPERATIONAL_STATUS` | UNRESOLVED | El cambio de plataforma de ET no demuestra estado operativo de la instalación |
| `ENTRANCE_CLOSURE_STATUS` | UNRESOLVED | No se encontró el elemento FM exacto |
| `EXIT_CLOSURE_STATUS` | UNRESOLVED | No se encontró el elemento FM exacto |

No se usa analogía para subir escalators a INCLUDED ni se confunden mensajes SX con estados estructurados FM. El mapping mantendría las limitaciones del perfil y del preview en provenance.

## Scope-unit matrix

IDs de scope propuestos: `M06-B02-SCOPE-C01-4-SN-A`, `...C01-4-SN-B`, `...C01-4-SN-C`, `...C01-4-SN-D`, `...C01-5-SN-A`, `...C01-5-SN-B`, `...C01-5-SN-C`, `...C01-5-SN-D`; `M06-B02-SCOPE-C07-ET-JOURNEY-DELAY-CANCELLATION`; `M06-B02-SCOPE-C07-SX-PASSENGER-DISRUPTION-NOTICE`; y `M06-B02-SCOPE-C08-LIFT-OPERATIONAL-STATUS`, `...C08-ESCALATOR-OPERATIONAL-STATUS`, `...C08-PLATFORM-OPERATIONAL-STATUS`, `...C08-ENTRANCE-CLOSURE-STATUS`, `...C08-EXIT-CLOSURE-STATUS`.

La matriz DATEX de aplicabilidad (es distinta del plan de inserción) queda así:

| Category | RRP/Profile | Capability | C01 scope | C04 scope | Evidence | Status |
|---|---|---|---|---|---|---|
| Road closures | RTTI 670/2022 · 4-SN-A | `CAP-DATEXII-RRP-ROAD-CLOSURE` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 4-SN-A, evento de cierre | C01 incluido; C04 espera applicability |
| Lane closures | RTTI 670/2022 · 4-SN-B | `CAP-DATEXII-RRP-LANE-CLOSURE` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 4-SN-B | Igual |
| Roadworks | RTTI 670/2022 · 4-SN-C | `CAP-DATEXII-RRP-ROADWORKS` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 4-SN-C | Igual |
| Temporary traffic management | RTTI 670/2022 · 4-SN-D | `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 4-SN-D | Igual |
| Bridge closures | RTTI 670/2022 · 5-SN-A | `CAP-DATEXII-RRP-BRIDGE-CLOSURE` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 5-SN-A | Igual |
| Accidents and incidents | RTTI 670/2022 · 5-SN-B | `CAP-DATEXII-RRP-ACCIDENT-INCIDENT` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 5-SN-B | Igual; no todo SRTI |
| Poor road conditions | RTTI 670/2022 · 5-SN-C | `CAP-DATEXII-RRP-POOR-ROAD-CONDITION` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 5-SN-C | Igual |
| Weather affecting road surface/visibility | RTTI 670/2022 · 5-SN-D | `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT` | INCLUDED | UNRESOLVED, Art. 5(2) | Página RRP 5-SN-D; etiqueta interna RSP por conciliar | C01 provisionalmente incluido, release por fijar; C04 abierto |
| Travel time, traffic volume, speed, queues | Otros RRP RTTI de uso de red | Ninguna de este paquete | EXCLUDED | EXCLUDED | Las fuentes los describen como medición/tiempo, no disrupción por sí mismos | Excluidos del concept C01/C04 |
| Regulación, tarifas, parking y charging availability | Otros dominios/categorías RTTI | Ninguna de este paquete | EXCLUDED | EXCLUDED | R1 los distingue de road-status/disruption | Fuera de estos concepts; no insertar unidades bajo estos mappings |

`EXCLUDED` de las dos últimas filas solo documenta elementos relacionados descartados al delimitar el candidate set; no genera scope units bajo mappings que no se insertan.

## Source/profile references

Las 11 source references propuestas (ocho RRP DATEX, tres vistas EPIP-RT —ET, SX y FM—) son nuevas porque las 8 referencias existentes están ligadas por FK a otras capabilities. No se puede reutilizar una fila con `capability_id` distinto. Las referencias SIRI se diferencian por servicio/sección (§8, §7 y §10), aunque pertenecen al mismo documento de perfil. No se duplican identidades de fuente idénticas sin distinción de sección. Referencias de contexto legal se conservan en provenance del mapping y en las fuentes de los cierres R1/R2; el contrato de `phase3_source_references` no ofrece `OFFICIAL_LEGAL_SOURCE` como clase para estas capabilities.

| Profile/source artifact | Standard family/version | Confidence | Limit |
|---|---|---|---|
| DATEX II RRP pages 4-SN-A/B/C/D, 5-SN-A/B/C/D bajo catálogo RTTI 670/2022 | DATEX II; release de modelo por perfil no fijada | Alta para ID/categoría; media para versión del artefacto | Catálogo vivo/model index 3.7 no prueba que cada RRP use 3.7 |
| EPIP-RT, CEN/TS 15531-7:2025 §8 ET / §7 SX / §10 FM | SIRI 2.1 revisado (2021); XSD de despliegue no fijado | Alta para identidad de perfil; media para servicios; baja-media para crosswalk de elementos | Vista/preview parcial, no texto normativo íntegro |
| Reglamento 2017/1926 consolidado 2024-03-04; Reglamento 2022/670; handbook MMTIS Q&A 4 | Fuente legal congelada, régimen sucesor y guía informativa | Media para puente interpretativo, no vinculante | No sustituye ni reescribe el source fact congelado |

Fuentes primarias descritas por los paquetes R1/R2: [catálogo DATEX II RTTI 670/2022](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/); páginas RRP por [4-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-a-road-closures/), [4-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-b-lane-closures/), [4-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-c-roadworks/), [4-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-d-temporary-traffic-management-measures/), [5-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-a-bridge-closures/), [5-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-b-accidents-and-incidents/), [5-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-c-poor-road-conditions/) y [5-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-d-weather-conditions-affecting-road-surface-and-visibility/); [CEN/TS 15531-7:2025 preview](https://normy.normoff.gov.sk/norma/141185/nahlad/) y [ficha NEN](https://www.nen.nl/cen-ts-15531-7-2025-en-341552); [Reglamento (UE) 2017/1926 consolidado](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng), [Reglamento delegado (UE) 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng) y [handbook MMTIS Q&A 4](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en).

## Persistence readiness

| Candidate | Capability | Mapping | Included scopes | Unresolved scopes | Profile/version | Persistence readiness |
|---|---|---|---|---|---|---|
| C01 | 8 × CREATE_NEW, listas con limitación | 8 por RRP, PARTIAL | 8 categorías RRP | Release/modelo; puente legal | RTTI 670/2022; modelo por RRP sin fijar | `READY_FOR_PARTIAL_PERSISTENCE`, pendiente de aprobación humana de las limitaciones |
| C04 | REUSE de las 8 capabilities propuestas para C01, si llegan a existir | 8 IDs alternativos; sin filas listas | 0 | 8 categorías con applicability Article 5(2) abierta | Igual que C01 | `NOT_READY`; no incluir en dry-run de inserción |
| C07 | ET y SX, CREATE_NEW por servicio | 2, PARTIAL | Delay/cancellation ET; disruption notice SX | CM/conexiones garantizadas fuera, sin bridge demostrado; crosswalk exacto pendiente | EPIP-RT 2025 / SIRI 2.1 | `READY_FOR_PARTIAL_PERSISTENCE`, con limitaciones y review humano |
| C08 | FM facility/equipment, CREATE_NEW | 1, PARTIAL | Lift operational status | Escalator, platform, entrance, exit | EPIP-RT 2025 / SIRI 2.1 | `READY_FOR_PARTIAL_PERSISTENCE` solo como rebanada candidata; requiere aceptación humana |

La capability existente `CAP-DATEXII-RRP-ROAD-TRAVEL` se clasifica `NOT_READY` para estos conceptos y no aparece en la propuesta. Cada unidad incluida tiene estado de disposición explícito; readiness para persistir no equivale a representability revisada.

## Coverage implications

Propuesta futura, no persistida: `P01 = PARTIAL`, porque los ocho mappings describen categorías delimitadas de estado/disrupción y no agotan el requirement ni resuelven el puente legal. `P02 = PARTIAL`, porque ET/SX y la rebanada FM son parciales y C04/U01/U02/U03 conservan límites o incógnitas. Coverage B02 seguirá en cero hasta autorización y decisión separada. No se calcula automáticamente desde los mappings.

## Representability readiness

Unidad futura de evaluación: `scope_unit_id`. En este paquete, todas las 11 unidades `INCLUDED` quedan `NOT_READY` para abrir una conclusión de representability: DATEX requiere fijar release/modelo por RRP; ET/SX requiere cruzar cada caso con elementos/constraints normativos; FM necesita confirmar el path del ascensor en EPIP-RT completo. Esto no revoca el estado `INCLUDED` de la propuesta semántica de scope; significa que no hay assertion de representabilidad lista. Unidades `UNRESOLVED` permanecen `NOT_READY`.

## Dry-run

Conteos exactos si se autorizara la propuesta recomendada C01+C07+C08:

### Capabilities
- count: 11
- IDs: ocho DATEX de la tabla anterior; `CAP-SIRI-EPIPRT-ET`; `CAP-SIRI-EPIPRT-SX`; `CAP-SIRI-EPIPRT-FM-FACILITY-STATUS`.

### Mappings
- count: 11
- IDs: los 8 IDs C01; `M06-B02-MAP-A05-P02-001-SIRI-ET`; `M06-B02-MAP-A05-P02-001-SIRI-SX`; `M06-B02-MAP-A05-P02-001-SIRI-FM-FACILITY-STATUS`.
- todos `mapping_type=PARTIAL`; mapping workflow `NEEDS_REVIEW`; proposed semantic review outcome `ACCEPTED_WITH_LIMITATIONS`, sujeto a decisión humana.

### Concept bridges
- count: 11, uno por cada mapping anterior, hacia el concept C01/C07/C08 correspondiente.
- igualdad requirement–concept verificada por diseño de IDs: C01 → P01-002; C07/C08 → P02-001. Se revalidará en seed/validator.

### Scope units
- count: 15
- INCLUDED: 11 (8 DATEX C01, ET delay/cancellation, SX disruption notice, C08 lift status).
- UNRESOLVED: 4 (C08 escalator, platform, entrance closure, exit closure).
- EXCLUDED insertadas: 0. Categorías RTTI ajenas se excluyen en la matriz, sin filas scope bajo mappings candidatos.
- C04: 0 mappings/bridges/scope units en el dry-run recomendado; 8 mappings alternativos fuera hasta resolver Article 5(2).

### Source references
- new: 11 (8 perfiles DATEX + 3 secciones/servicios EPIP-RT).
- reused: 0; la FK existente ata cada fila a otra capability.

### Coverage
- 0 en este paquete.

## Expected deltas

Solo con autorización futura separada: +11 capabilities, +11 mappings, +11 mapping reviews, +11 concept bridges, +15 scope units, +15 scope-source links (11 `SUPPORT` y 4 `BOUNDARY`) y +11 source references. Sin cambios en requirements/concepts, legacy mappings/reviews/scopes, coverage, representability, observed evidence, automatizability o audit rules. Para C04, la delta prevista ahora es cero.

## Invariants

Tras una futura transacción autorizada deben seguir: requirements 48; concepts B02 7; legacy mappings 6 y scopes legacy 0; Phase 1 = 92 provisions/36 source facts y Phase 2 = 48 requirements/10 deadlines; coverage global 8 y cobertura B02 0; representability y observed evidence 0; `audit.rules` 0; automatizability global 6. Los únicos deltas admisibles serán las capas B02 listadas arriba. La DB no se escribió en esta sesión.

## Validation

Todos los comandos DuckDB se ejecutaron con `-readonly`; exit code 0 en cada validator:

| Validator | Resultado |
|---|---|
| `validate_phase_3_m06_b02c_scope_schema.sql` | PASS, 26 checks, 0 failures |
| `validate_phase_3_m06_b02a_populated_schema.sql` | PASS, 13 checks, 0 failures |
| `validate_phase_3_m06_b02a_requirement_concepts.sql` | PASS, 11 checks, 0 failures |
| `validate_phase_3_level_a.sql` | PASS; 6 mappings/capabilities/exceptions; 0 referencias, estados o razones inválidas |
| `validate_phase_3_exception_accounting.sql` | PASS; 3 M04 + 3 B01, 0 sin cuenta/incompatibles |
| `validate_phase_3_m04b_semantic_coverage.sql` | PASS; 0 fallos estructurales, 8 coverage y 6 reviews legacy |
| `validate_phase_3_m05b_family_baseline_v1.sql` | PASS; 41 HIGH, 7 MEDIUM, 0 LOW |
| `validate_phase_3_m06_b01_candidates.sql` | PASS; 0 fallos estructurales |
| `validate_phase_3_m04_pilot.sql` | PASS; 5/5 mappings piloto esperados, 0 accepted, 0 reglas |
| `git diff --check` | Exit 0; aviso de normalización CRLF/LF en `PROJECT_STATUS.md`, cambio local preexistente |

El informe nuevo tiene newline final y cero líneas con whitespace final. Conteos read-only después de los validators: requirements 48; provisions/source facts/deadlines 92/36/10; B02 concepts/mappings/bridges/scopes/scope-source links/coverage 7/0/0/0/0/0; mappings globales/coverage global 6/8; representability/observed evidence/audit.rules 0/0/0. SHA-256 DB antes y después: `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`. `DB_WRITES=0`.

## Seed design

No se preparan SQL seeds ejecutables: C04 no está listo y las filas de los tres mapping reviews dependen de aprobación humana. El dry-run incluye identidades estables y cardinalidad para que la revisión decida cada mapping por separado. Cuando haya autorización, producir seeds `DRAFT / NOT AUTHORIZED FOR EXECUTION` por tabla, con preflight de ausencia/conflicto, verificación exacta de filas existentes, inserción únicamente si faltan, transacción fail-fast y snapshot pre/post de legacy y fases protegidas.

## Validator design

El futuro validator de datos, separado de B02C/B02A, comprobará: IDs esperados; no más de los 11 mappings autorizados; `mapping_type=PARTIAL`; estado workflow y outcome semántico separados; mappings aceptados con limitaciones no vacías; equality requirement entre concept y mapping; bridge 1:1 para cada mapping y ningún bridge huérfano; 15 scope IDs/códigos y disposiciones 11 INCLUDED/4 UNRESOLVED; reasons para unresolved; fuentes enlazadas a cada scope y capabilities correctas; profile/version/artifact/provenance y limitaciones; C04 sin filas hasta resolución; C02/C03/C05/C06 ausentes; ningún mapping FULL/condicional inesperado; seis legacy exactos sin scope; Phase 1/2 y coverage/representability/evidence/automatizability/audit.rules intactos. El validator debe correr en `-readonly` después de una ejecución autorizada y no sustituye aceptación humana.

## Risks

- El source fact C01 conserva la referencia a 2015/962; el handbook es informativo y no resuelve por sí solo su relación con 2022/670.
- Las páginas RRP identifican 8 perfiles, pero no fijan release DATEX de modelo por perfil; 5-SN-D conserva una inconsistencia “RSP” en la documentación revisada.
- C04 no tiene demostrada la aplicabilidad Article 5(2) por categoría; mantener los mappings alternativos fuera.
- El preview EPIP-RT es parcial. Los casos a nivel de servicio no sustituyen un crosswalk normativo Annex→elemento/constraint.
- C08 depende de que un reviewer acepte el lift como porción incluida aunque la traza exacta de elementos FM siga pendiente. Escalator no se promociona por analogía.
- Los `INCLUDED` de este paquete son decisiones técnicas propuestas y no legalmente revisadas; requieren revisión humana por mapping/unidad antes de persistir.

## Human decisions required

### Autorizar o rechazar por separado

- C01 capabilities nuevas: `CAP-DATEXII-RRP-ROAD-CLOSURE`, `CAP-DATEXII-RRP-LANE-CLOSURE`, `CAP-DATEXII-RRP-ROADWORKS`, `CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT`, `CAP-DATEXII-RRP-BRIDGE-CLOSURE`, `CAP-DATEXII-RRP-ACCIDENT-INCIDENT`, `CAP-DATEXII-RRP-POOR-ROAD-CONDITION`, `CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT`.
- C01 mappings parciales: `M06-B02-MAP-A05-P01-002-DATEX-4-SN-A`, `...DATEX-4-SN-B`, `...DATEX-4-SN-C`, `...DATEX-4-SN-D`, `...DATEX-5-SN-A`, `...DATEX-5-SN-B`, `...DATEX-5-SN-C`, `...DATEX-5-SN-D`, con las expansiones completas ya listadas en C01.
- C01 scope units: `M06-B02-SCOPE-C01-4-SN-A`, `M06-B02-SCOPE-C01-4-SN-B`, `M06-B02-SCOPE-C01-4-SN-C`, `M06-B02-SCOPE-C01-4-SN-D`, `M06-B02-SCOPE-C01-5-SN-A`, `M06-B02-SCOPE-C01-5-SN-B`, `M06-B02-SCOPE-C01-5-SN-C`, `M06-B02-SCOPE-C01-5-SN-D` (propuestas `INCLUDED`).
- C07 capabilities/mappings: `CAP-SIRI-EPIPRT-ET` con `M06-B02-MAP-A05-P02-001-SIRI-ET`; `CAP-SIRI-EPIPRT-SX` con `M06-B02-MAP-A05-P02-001-SIRI-SX`. Scope units `M06-B02-SCOPE-C07-ET-JOURNEY-DELAY-CANCELLATION` y `M06-B02-SCOPE-C07-SX-PASSENGER-DISRUPTION-NOTICE` (propuestas `INCLUDED`).
- C08 capability/mapping: `CAP-SIRI-EPIPRT-FM-FACILITY-STATUS` con `M06-B02-MAP-A05-P02-001-SIRI-FM-FACILITY-STATUS`. Scope units: `M06-B02-SCOPE-C08-LIFT-OPERATIONAL-STATUS` (`INCLUDED` candidato), `M06-B02-SCOPE-C08-ESCALATOR-OPERATIONAL-STATUS`, `M06-B02-SCOPE-C08-PLATFORM-OPERATIONAL-STATUS`, `M06-B02-SCOPE-C08-ENTRANCE-CLOSURE-STATUS` y `M06-B02-SCOPE-C08-EXIT-CLOSURE-STATUS` (las cuatro últimas `UNRESOLVED`).
- Aprobar/rechazar las 11 source references propuestas y las 15 relaciones scope→source (11 `SUPPORT`, 4 `BOUNDARY`). Aceptar únicamente las identidades/versiones descritas, con limitaciones explícitas.

### Mantener fuera

- C04: no autorizar ahora `M06-B02-MAP-A05-P02-001-DATEX-4-SN-A/B/C/D` ni `...DATEX-5-SN-A/B/C/D`, ni bridges o scopes; son alternativas sin applicability Article 5(2) demostrada. Si se resuelve, reutilizar las capabilities C01 aprobadas en vez de duplicarlas.
- C07: `SIRI-CM`, conexiones garantizadas y `SIRI-VM` no reciben capability, mapping, bridge ni scope en este paquete.
- C08: no promover escalator, platform, entrance o exit a `INCLUDED`; no ampliar FM por analogía.
- Fuera de candidatos: U01/U02/U03 y C02/C03/C05/C06. No hay mapping FULL, coverage ni representability persistida.
- `CAP-DATEXII-RRP-ROAD-TRAVEL` no se reutiliza para status/disruptions.

Estas decisiones humanas son revisión del paquete. No autorizan escritura de DB. Cualquier persistencia requiere autorización explícita distinta; `B02_PARTIAL_MAPPING_PERSISTENCE = NOT_AUTHORIZED` sigue vigente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
