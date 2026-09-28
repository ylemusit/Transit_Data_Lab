# M06-B02B Targeted Closure

Fecha: 2026-09-28. Resultado documental de M06-B02B-R1 (DATEX II) y R2 (SIRI/EPIP-RT). El paquete queda READY_FOR_HUMAN_REVIEW; no todos los candidatos están listos para persistencia. B02_MAPPING_PERSISTENCE = NOT_AUTHORIZED.

## Scope

Solo C01, C04, C07 y C08. Se parte de los conceptos B02A aceptados con limitaciones. No se reabren C02/C03/C05/C06 ni U01/U02/U03. Se hizo investigación técnica/legal focalizada en fuentes oficiales/primarias, sin inspeccionar datasets. No se alteraron requirements, Phase 1/2 ni sus evidencias.

## R1 — DATEX II

### Legal bridge

La fuente congelada de C01 mantiene literalmente Article 5(1)(a) y referencia a 2015/962; C04 mantiene Article 5(2) condicional. El handbook de la Comisión, Q&A 4 (2024), declara que las referencias son dinámicas y se aplica la versión RTTI más reciente al interpretar el acto. Regulation 2015/962 fue derogada desde 2025-01-01; Regulation 2022/670 es el marco RTTI actual con categorías de carretera DATEX II. La guía es explícita como interpretación, pero informativa/no vinculante: bridge = PARTIAL, sin equivalencia de reglamentos ni reescritura del texto congelado.

Fuentes: [Commission MMTIS handbook, Q&A 4](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en), [consolidated Regulation 2017/1926](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng), [Regulation 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng). Consulta 2026-09-28. La regulación establece clases/ámbito; el catálogo DATEX II es documentación técnica RRP, no legislación.

### Category analysis

ROAD_STATUS_DISRUPTION se representa de forma defendible con las ocho categorías Anexo 4/5 de 2022/670: cierres de vía, cierres de carril, obras, gestión temporal, cierres de puente, accidentes/incidentes, malas condiciones viales y clima que afecte calzada/visibilidad. Las seis primeras son disrupciones/eventos; las dos últimas estados/condiciones con impacto vial. No incluir volumen, velocidad, colas o travel times (Anexo 6), reglas/restricciones, tariffs, disponibilidad de combustible/recarga ni parking. Son categorías técnicas o concepts distintos.

RRP exactos: 4-SN-A Road closures; 4-SN-B Lane closures; 4-SN-C Roadworks; 4-SN-D Temporary traffic management measures; 5-SN-A Bridge closures; 5-SN-B Accidents and incidents; 5-SN-C Poor road conditions; 5-SN-D Weather conditions affecting road surface and visibility. Comparten patrones Situation/event, con LocationReference/Validity y Publication según perfil; modelos citados por páginas incluyen EN 16157-7:2018, -2:2019 y -3:2018. La página 5-SN-D usa inconsistentemente el término “RSP”.

El catálogo expone downloads hasta modelo DATEX II 3.7, pero no prueba que cada RRP se haya emitido con 3.7. Perfil e identidad de categoría están identificados; release exacta de perfil y release de modelo por perfil permanecen PARTIAL.

Fuentes individuales: [catálogo RTTI](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/); [4-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-a-road-closures/), [4-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-b-lane-closures/), [4-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-c-roadworks/), [4-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-d-temporary-traffic-management-measures/), [5-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-a-bridge-closures/), [5-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-b-accidents-and-incidents/), [5-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-c-poor-road-conditions/), [5-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-d-weather-conditions-affecting-road-surface-and-visibility/). Organismo DATEX II; páginas vivas consultadas 2026-09-28, sin release individual estable identificada.

### Capability granularity

Recomendar capability por categoría y relación many-to-many desde el concept. Mantiene semantic fidelity, permite reuso por C01/C04 sin duplicar capabilities, conserva reporting y revisión independientes, soporta representability/automatability/reglas por perfil y hace visible el versionado. Ocho no es exceso porque los RRPs están separados por categoría; una capability agregada podría ser una agrupación derivada, no sustituir las identidades.

### C01 decision

Requirement/concept ESTABLISHED; bridge legal PARTIAL; las ocho categorías y perfil IDs ESTABLISHED como identidad técnica; release/profile PARTIAL; capability/mapping PARTIAL. Resultado individual PARTIAL, no READY_FOR_PERSISTENCE. Mapping documental sugerido: M06-B02-MAP-A05-P01-002-DATEX-ROAD-STATUS.

### C04 decision

Requirement/concept y wording condicional de Art. 5(2) ESTABLISHED; applicability por categoría PARTIAL; mismos RRP técnicos reutilizables; release PARTIAL. Resultado PARTIAL, no READY_FOR_PERSISTENCE. Mapping documental sugerido: M06-B02-MAP-A05-P02-001-DATEX-ROAD-STATUS. C01/C04 pueden compartir las ocho capabilities técnicas, manteniendo mapping/provenance separados por requirement, base legal y condición.

Detalle por perfil, objetos y gaps: [informe R1](M06_B02B_R1_DATEX_II_TARGETED_CLOSURE.md).

## R2 — SIRI / EPIP-RT

### Profile/version

EPIP-RT = CEN/TS 15531-7:2025; perfil especificado sobre SIRI 2.1 (2021). Perfil y modelo son capas distintas; revisión de XSD concreto no está fijada. La vista nacional ÚNMS SR es parcial; no se revisó el texto íntegro.

Fuente primaria/estándar: [vista CEN/TS 15531-7:2025, ÚNMS SR](https://normy.normoff.gov.sk/norma/141185/nahlad/) y [ficha NEN](https://www.nen.nl/cen-ts-15531-7-2025-en-341552), consultadas 2026-09-28; alcance de la vista y límite de copyright constan en R2.

### Service analysis

ET (Estimated Timetable, CEN/TS 15531-3) aporta estado estimado del journey/llamadas: retrasos, cancelaciones, servicios adicionales, cambios de parada/recorrido. SX (Situation Exchange, CEN/TS 15531-5) aporta avisos de situación/disrupción, impactos y validez/revocación. Ambos necesarios para el scope C07; el crosswalk campo-a-cada-subitem del Annex sigue parcial. VM aporta posición/actividad de vehículo, concept distinto: excluir. FM corresponde a facilities y se revisa solo para C08.

### C07 crosswalk

Requirement/concept/profile/service identity ESTABLISHED; applicability Art. 5(1)(b)/(2) PARTIAL y limitada a otros modos; version SIRI 2.1 ESTABLISHED; detalle completo Annex-to-message/constraints PARTIAL. Capability recomendada CAP-SIRI-EPIP-RT-PASSENGER-STATUS con ET+SX declarados; mapping sugerido M06-B02-MAP-A05-P02-001-SIRI-PASSENGER-STATUS. C07 = PARTIAL, no READY_FOR_PERSISTENCE.

### C08 facility crosswalk

FM y caso EPIP-RT “Elevator out of business” respaldan una fracción. Lifts/elevators: SUPPORTED como slice técnica. Escalators y facilities generales: PARTIAL. Estado operativo de platforms y closed entrances/exits: UNRESOLVED. El caso ET “platform changes” significa cambio de plataforma asignada al journey, no estado de la instalación. No asumir que FM cubre todo FACILITY_ACCESS_NODE_STATUS.

Mantener el concept padre y limitar una futura capability CAP-SIRI-EPIP-RT-FM-STATION-EQUIPMENT-STATUS al scope demostrado, con mapping PARTIAL. No crear subconcept ahora. Si facility classes requieren representability/coverage independiente, abrir ARCHITECTURE_REVIEW_REQUIRED antes de rediseñar. Mapping sugerido M06-B02-MAP-A05-P02-001-SIRI-FACILITY-STATUS. C08 = PARTIAL, no READY_FOR_PERSISTENCE.

Detalle de servicio y elementos: [informe R2](M06_B02B_R2_SIRI_TARGETED_CLOSURE.md).

## Crosswalk completeness matrix

| Layer | C01 | C04 | C07 | C08 |
|---|---|---|---|---|
| Requirement | ESTABLISHED | ESTABLISHED | ESTABLISHED | ESTABLISHED |
| Concept | ESTABLISHED | ESTABLISHED | ESTABLISHED | ESTABLISHED |
| Legal applicability | PARTIAL: handbook no vinculante | PARTIAL: Art. 5(2) condicional | PARTIAL: ramas otros modos | PARTIAL: rama y clase de dato condicional |
| Standard | ESTABLISHED: DATEX II | ESTABLISHED condicional | ESTABLISHED: SIRI | ESTABLISHED: SIRI |
| Profile | ESTABLISHED: ocho RRP técnicos | ESTABLISHED como candidatos | ESTABLISHED: EPIP-RT | ESTABLISHED: FM en EPIP-RT |
| Version | PARTIAL: RRP/model release | PARTIAL: RRP/model release | ESTABLISHED: 15531-7:2025/SIRI 2.1; XSD no fijado | igual que C07 |
| Exact category/service | ESTABLISHED IDs de categoría; release parcial | igual, applicability parcial | ESTABLISHED: ET+SX | PARTIAL: FM slice |
| Exact elements | PARTIAL por constraints/release | PARTIAL | PARTIAL: falta Annex-to-field íntegro | PARTIAL: ascensores; plataformas/entradas unresolved |
| Capability design | PARTIAL, por categoría | PARTIAL, reutiliza C01 | PARTIAL, ET+SX | PARTIAL, FM estrecho |
| Mapping readiness | PARTIAL | PARTIAL | PARTIAL | PARTIAL |

## Capability proposals

Las capabilities listadas son no persistidas y requieren revisión humana.

| Capabilities | Scope/reuso | Estado |
|---|---|---|
| CAP-DATEXII-RRP-ROAD-CLOSURE; LANE-CLOSURE; ROADWORKS; TEMP-TRAFFIC-MGMT; BRIDGE-CLOSURE; ACCIDENT-INCIDENT; POOR-ROAD-CONDITION; ROAD-WEATHER-IMPACT | Respectivamente 4-SN-A/B/C/D y 5-SN-A/B/C/D; C01+C04 | PARTIAL |
| CAP-SIRI-EPIP-RT-PASSENGER-STATUS | EPIP-RT ET+SX; C07 | PARTIAL |
| CAP-SIRI-EPIP-RT-FM-STATION-EQUIPMENT-STATUS | FM; C08, scope estrecho | PARTIAL |

Ready: ninguna. Partial: todas las anteriores. Blocked/not ready: reutilizar CAP-DATEXII-RRP-ROAD-TRAVEL para estado vial; capability genérica SIRI para todo C07/C08; assertions de que las facilities no resueltas están representadas.

## Mapping readiness

| Mapping propuesto, no ejecutado | Semantic status / revisión |
|---|---|
| M06-B02-MAP-A05-P01-002-DATEX-ROAD-STATUS | PARTIAL; handbook informativo, profile release abierta |
| M06-B02-MAP-A05-P02-001-DATEX-ROAD-STATUS | PARTIAL; applicability por categoría condicional y release abierta |
| M06-B02-MAP-A05-P02-001-SIRI-PASSENGER-STATUS | PARTIAL; falta crosswalk íntegro a elementos EPIP-RT |
| M06-B02-MAP-A05-P02-001-SIRI-FACILITY-STATUS | PARTIAL; FM scope acotado; no cubre demostrado todas las facilities |

Ready: ninguno. Partial: los cuatro mappings documentales. Blocked: afirmaciones completas/legalmente concluyentes, cobertura FULL de cualquiera de los requirements basada solo en esta revisión.

## Representability readiness

| Candidate | Resultado | Límite |
|---|---|---|
| C01 | PARTIAL | Perfiles técnicos representables; interpretación no vinculante y release por perfil no fijada. |
| C04 | PARTIAL | Scope vial técnico; applicability condicional y release parcial. |
| C07 | PARTIAL | ET/SX cubren funcionalmente status/disruption; falta exhaustive profile field crosswalk. |
| C08 | PARTIAL | FM respalda una fracción; las instalaciones restantes no están cerradas. |

No se emite representability assertion ni se inspeccionaron datasets; observado = NO/NO_INSPECTED, no significa ausencia de datos.

## Coverage implications

P01 = PARTIAL. C01 es una fracción de datos dinámicos de carretera; no acredita todo el requirement. P02 = PARTIAL. U01/U02/U03 siguen abiertos y cuentan contra FULL. No persistir coverage; una relación técnica no acredita cumplimiento legal.

## Remaining uncertainties

- Decisión humana sobre el handbook como contexto interpretativo aceptable, sin equivalencia normativa.
- Release exacta por RRP DATEX II; discrepancia terminológica 5-SN-D.
- Applicability MMTIS y selección de categorías concretas para C04.
- Acceso a texto normativo íntegro EPIP-RT y crosswalk exacto por Annex item para C07/C08.
- Elementos exactos para escalators, estado operativo de plataformas y entrances/exits en C08.
- XSD/implementación/observed data no examinados.

## Human decisions required

1. Autorizar en una futura sesión cuáles capabilities propuestas pasan a persistencia tras fijar versiones y revisar los crosswalks.
2. Mantener los cuatro mappings fuera de persistencia hasta que sus limitaciones indicadas se revisen y acepten.
3. Decidir si C08 acepta mapping parcial FM limitado al scope demostrado; no mapear lo no resuelto.
4. No declarar coverage FULL P02 mientras U01/U02/U03 sigan abiertos.

## Validación y DB

Validaciones ejecutadas desde la raíz; cada SQL contra DuckDB con -no-init -batch -bail -readonly -json:

| Comprobación | Resultado |
|---|---|
| Populated schema | PASS, 13 checks, 0 failures, exit 0 |
| B02A validator | PASS, 11 checks, 0 failures, exit 0 |
| Phase 3 Level A | PASS, 6 mappings/capabilities/exceptions; 0 invalid references, 0 invalid states, 0 missing reasons; exit 0 |
| Otros validators | no ejecutados; sin necesidad identificada |
| diff-check | Git diff --check ejecutado; sin errores de whitespace; advertencia CRLF en PROJECT_STATUS.md preexistente. Los tres informes nuevos también se revisaron directamente: sin espacios finales y con newline final |
| DB modificada | NO |
| SHA-256 antes | 9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6 |
| SHA-256 después | 9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6 |

## Estado final

M06_B02B_TARGETED_CLOSURE = READY_FOR_HUMAN_REVIEW. Candidate status: C01 PARTIAL; C04 PARTIAL; C07 PARTIAL; C08 PARTIAL. B02_MAPPING_PERSISTENCE = NOT_AUTHORIZED. La sesión termina aquí y no autoriza persistencia ni siguiente fase.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
