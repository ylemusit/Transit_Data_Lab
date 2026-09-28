# M06-B02B-R1 DATEX II Targeted Closure

Fecha: 2026-09-28. Scope: C01 y C04, concepto ROAD_STATUS_DISRUPTION. Solo investigación y propuesta documental: no se inspeccionaron datasets ni se persistieron capabilities, mappings, bridges, coverage o resultados derivados.

## Puente legal

| Candidato | Base congelada y contexto | Estado |
|---|---|---|
| C01 | EU-2017-1926-REQ-A05-P01-002, Art. 5(1)(a), cita literalmente Arts. 5 y 6 de 2015/962. El handbook MMTIS de la Comisión, Q&A 4 (2024), dice que la referencia es dinámica y se aplica la RTTI más reciente al interpretar el acto. 2015/962 fue derogado desde 2025-01-01; el marco vigente incluye 2022/670. | PARTIAL: puente interpretativo explícito de la Comisión, pero handbook informativo/no vinculante; no es enmienda ni identidad entre reglamentos. |
| C04 | EU-2017-1926-REQ-A05-P02-001, Art. 5(2), exige perfil mínimo solo para categorías 2.1/2.2 donde SIRI o DATEX II sean aplicables. 2022/670 Arts. 6/7 contiene categorías RTTI de estado/uso vial y prescribe DATEX II en su ámbito. | PARTIAL: coincidencia técnica por categorías, sin extender DATEX II a todo el Anexo MMTIS. |

Cadena defendible: requirement congelado → interpretación de referencia dinámica del handbook → categoría vial de 2022/670 → RRP específico. Fuente legal literal preservada. Fuentes: [Reglamento consolidado 2017/1926](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng), [handbook MMTIS, Q&A 4](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en), [Reglamento 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng).

## Categorías y RRP

El catálogo DATEX II dice que los RRP son subconjuntos por caso de uso y que se combinan para cubrir la información publicada. La lista de abajo incluye categorías de estado/disrupción, no cualquier cosa que aparezca en RTTI.

| Categoría 2022/670 | RRP exacto | Scope técnico y modelo publicado | Decisión |
|---|---|---|---|
| Anexo 4(a), cierres de vía | 4-SN-A Road closures | Common, LocationReferencing, Situation; evento SituationPublication/Situation/SituationRecord, acción de operador y tipo de cierre. Partes citadas: EN 16157-7:2018, EN 16157-2:2019, EN 16157-3:2018. | Incluir |
| Anexo 4(b), cierres de carril | 4-SN-B Lane closures | Mismos paquetes modelados para cierres de carril; evento localizado. | Incluir separado de cierre de vía |
| Anexo 4(c), obras | 4-SN-C Roadworks | Common, LocationReferencing, Validity, Publication y Situation; eventos de obra vial. Partes 7/2/3 citadas como 2018/2019/2018. | Incluir |
| Anexo 4(d), gestión temporal | 4-SN-D Temporary traffic management measures | Paquetes Common, LocationReferencing, Validity, Publication y Situation, acotados a medidas temporales. | Incluir |
| Anexo 5(a), cierre de puente | 5-SN-A Bridge closures | Common, LocationReferencing, Validity, Publication y Situation; evento de cierre de puente. Partes 7/2/3. | Incluir |
| Anexo 5(b), accidentes/incidentes | 5-SN-B Accidents and incidents | Common, LocationReferencing, Validity, Publication y Situation; evento de accidente/incidente. Partes 7/2/3. | Incluir; no implica cualquier peligro SRTI |
| Anexo 5(c), malas condiciones de carretera | 5-SN-C Poor road conditions | Paquetes de evento vial Common, LocationReferencing, Validity, Publication y Situation. Partes 7/2/3. | Incluir, solo condición vial adversa |
| Anexo 5(d), clima que afecta calzada/visibilidad | 5-SN-D Weather conditions affecting road surface and visibility | Página documenta Situation/event publishing pero llama al artefacto “RSP” en una sección, inconsistente con su catálogo RRP. | Incluir provisionalmente; confirmar identidad de release |
| Anexo 6, volumen, velocidad, colas, tiempos | Otros RRP RTTI de uso de red | Mediciones y tiempo de viaje. | Excluir de disrupción |
| Regulaciones/restricciones, tarifas, disponibilidad de parking/recarga | Categorías de regulación, infraestructura o uso | No son estado/disrupción por ser RTTI. | Excluir salvo concept separado |

Fuentes oficiales DATEX II (organismo: DATEX II; páginas vivas consultadas 2026-09-28; sin fecha/release individual estable observada): [catálogo RTTI 670/2022](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/); [4-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-a-road-closures/), [4-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-b-lane-closures/), [4-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-c-roadworks/), [4-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/4-sn-d-temporary-traffic-management-measures/), [5-SN-A](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-a-bridge-closures/), [5-SN-B](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-b-accidents-and-incidents/), [5-SN-C](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-c-poor-road-conditions/), [5-SN-D](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/5-sn-d-weather-conditions-affecting-road-surface-and-visibility/).

## Version y capability

El portal expone catálogo/model downloads hasta DATEX II 3.7 y archivo 3.6…2.0. Esto identifica la release descargable del modelo/catálogo, pero no prueba que los ocho perfiles hayan sido generados con 3.7. Las páginas relacionan Common EN 16157-7:2018, LocationReferencing EN 16157-2:2019 y Situation EN 16157-3:2018; no fijan en conjunto release de perfil/modelo inmutable. Identidad de familia, perfil, release de perfil y release de modelo son campos distintos. Confianza en IDs/categorías: alta; release exacta por perfil: parcial.

Recomendación: capabilities por categoría, no una única CAP-DATEXII-RRP-ROAD-STATUS. La capacidad agregada simplifica reporting, pero oculta diferentes objetos y limita representability, audit rules, versionado y reuso selectivo. Ocho perfiles separados conservan trazabilidad con granularidad acorde al catálogo; una vista agrupada podría derivarse después.

| Capability propuesta, no persistida | Perfil | Reutilizable por | Estado |
|---|---|---|---|
| CAP-DATEXII-RRP-ROAD-CLOSURE | 4-SN-A | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-LANE-CLOSURE | 4-SN-B | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-ROADWORKS | 4-SN-C | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT | 4-SN-D | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-BRIDGE-CLOSURE | 5-SN-A | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-ACCIDENT-INCIDENT | 5-SN-B | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-POOR-ROAD-CONDITION | 5-SN-C | C01, C04 | PARTIAL |
| CAP-DATEXII-RRP-ROAD-WEATHER-IMPACT | 5-SN-D | C01, C04 | PARTIAL |

No reutilizar la capability existente CAP-DATEXII-RRP-ROAD-TRAVEL: es de travel times. C01 y C04 podrían compartir estas mismas capabilities técnicas y deberían mantener mappings separados por requirement, artículo, applicability, source reference y límites.

## Decisiones por candidato

| Candidato y mapping propuesto (documental) | Cadena y resultado |
|---|---|
| C01; M06-B02-MAP-A05-P01-002-DATEX-ROAD-STATUS | Requirement/concept ESTABLISHED; interpretation legal PARTIAL; identidades y scope técnico de los ocho RRP ESTABLISHED; release/profile y capability PARTIAL. Resultado: PARTIAL, no READY_FOR_PERSISTENCE. |
| C04; M06-B02-MAP-A05-P02-001-DATEX-ROAD-STATUS | Requirement/concept ESTABLISHED; Art. 5(2) condicional PARTIAL; RRP técnicamente identificados pero su applicability MMTIS por categoría y release sigue PARTIAL. Resultado: PARTIAL, no READY_FOR_PERSISTENCE. |

Ambos mappings propuestos serían semánticamente PARTIAL. Representability readiness de C01 y C04: PARTIAL; no es assertion ni evidencia observada. No existe bridge persistido.

## Incertidumbres y decisiones humanas

1. Aceptar o no el handbook informativo como interpretación de contexto, conservando la fuente literal y sin declarar equivalencia normativa.
2. Fijar para cada RRP artefacto y release exactos; no inferir 3.7 para todos.
3. Confirmar 5-SN-D ante la etiqueta interna “RSP”.
4. Seleccionar categorías aplicables a C04 sin extrapolar 2022/670 a todo Annex 2.1.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
