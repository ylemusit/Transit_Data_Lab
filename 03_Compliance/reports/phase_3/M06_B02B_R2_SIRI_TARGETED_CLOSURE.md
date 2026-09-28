# M06-B02B-R2 SIRI / EPIP-RT Targeted Closure

Fecha: 2026-09-28. Scope: C07 y C08 del requirement EU-2017-1926-REQ-A05-P02-001. Investigación documental dirigida, sin dataset inspection ni persistencia.

## Perfil y versión

Perfil exacto: Passenger Real-Time Information European Profile (EPIP-RT), CEN/TS 15531-7:2025, aprobado por CEN el 30-06-2025 y publicado el 01-07-2025. El perfil está especificado para SIRI 2.1 revisado (2021); versiones anteriores pueden carecer de elementos. Identidad de perfil y versión base SIRI son capas distintas. No se fijó revisión del XSD nacional/de despliegue.

Fuente: texto CEN reproducido en vista de norma nacional ÚNMS SR (15 páginas visibles) y ficha de NEN, consultados 2026-09-28. La vista no es el documento normativo completo: [CEN/TS 15531-7:2025, ÚNMS SR](https://normy.normoff.gov.sk/norma/141185/nahlad/), [ficha NEN](https://www.nen.nl/cen-ts-15531-7-2025-en-341552). Organismos: CEN y organismos nacionales de normalización. Scope: perfil europeo de información real-time para pasajeros en contexto MMTIS; limitación: vista normativa parcial.

## Service matrix

| Servicio | Modelo y scope documentado | Uso en esta tarea |
|---|---|---|
| SIRI-ET, Estimated Timetable (CEN/TS 15531-3) | EstimatedTimetableDelivery, EstimatedVehicleJourney y EstimatedCall; EPIP-RT incluye ejemplos de delays, cancellations, additional journey, stop cancellation, rerouting y platform changes. | Incluir en C07: estado de journey/servicio planificado y estimaciones. |
| SIRI-SX, Situation Exchange (CEN/TS 15531-5) | SituationExchangeDelivery, PtSituationElement, impacto/consecuencias/avisos/delays; mensajes estructurados para información de viaje con periodo de validez y revocación. | Incluir en C07: incidente/disrupción y su ámbito/consecuencias. |
| SIRI-VM, Vehicle Monitoring (CEN/TS 15531-3) | VehicleMonitoringDelivery y VehicleActivity, monitorización/posición/progreso de vehículos. | Excluir de C07: localización del vehículo es concept distinto y no añade cierre material al estado de servicio. |
| SIRI-FM, Facilities Monitoring (CEN/TS 15531-4) | EPIP-RT incluye Facilities Monitoring; FM está en SIRI desde schema 1.3 y hay caso de uso “Elevator out of business”. | Evaluar para C08; no incluir en C07. |

EPIP-RT también enumera PT, ST, SM, CT, CM y GM; no se incluyen por exhaustividad. ET + SX son el scope defendible para disrupción/estado de servicio de pasajeros. SX aporta mensajes de situación; ET aporta estado de viajes y llamadas. La vista demuestra servicios y casos, pero la correspondencia exhaustiva de cada elemento del Annex a campos obligatorios/condicionales sigue pendiente.

Fuente primaria del perfil: [vista CEN/TS ÚNMS SR](https://normy.normoff.gov.sk/norma/141185/nahlad/), secciones/índice ET (§8), SX (§7), VM (§9), FM (§10), consultada 2026-09-28. Partes CEN/TS 15531-3/-4/-5 son las referencias del prefacio EPIP-RT; sus textos completos no se revisaron. El propio perfil advierte que conformidad sintáctica no garantiza calidad completa ni correspondencia con la realidad.

## C07 crosswalk

| Layer | Estado | Evidencia/limitación |
|---|---|---|
| Requirement/concept PASSENGER_RT_STATUS_DISRUPTION | ESTABLISHED | Concept M06-B02 aceptado con limitaciones. |
| Applicability | PARTIAL | Art. 5(1)(b) menciona SIRI CEN/TS 15531 y versiones sucesivas para otros modos, sujeto a su alternativa de compatibilidad; Art. 5(2) es condicional. No aplicar SIRI al tramo vial. |
| Profile/version | ESTABLISHED | EPIP-RT CEN/TS 15531-7:2025, SIRI 2.1. |
| Services | ESTABLISHED como cruce funcional | ET para actualizaciones de journey/calls; SX para avisos y alcance de disrupciones. |
| Annex item → exact profile element/constraint | PARTIAL | Casos de uso/nombres de objetos identificados; falta verificación completa del estándar para cada subelemento del Annex 2.1. |
| Capability/mapping | PARTIAL | Propuesta EPIP-RT ET+SX; no demuestra presencia de datos ni implementaciones. |

Granularidad: recomendar una capability concept-scoped CAP-SIRI-EPIP-RT-PASSENGER-STATUS, descrita con alcance explícito ET+SX y referencias de versión por servicio. Una capability única mejora claridad/reuso/reporting para C07; dos IDs independientes tienen sentido solo si futuras revisiones necesitan estados, reglas o representability independientes por servicio. No usar una capability genérica “todo SIRI”.

Mapping propuesto, no persistido: M06-B02-MAP-A05-P02-001-SIRI-PASSENGER-STATUS, semantic status PARTIAL. C07 = PARTIAL, no READY_FOR_PERSISTENCE hasta validar la matriz íntegra Annex-to-profile.

## C08 facility crosswalk

Annex 2.1(iii) nombra estado dinámico de nodos/acceso e instalaciones: plataformas, ascensores/escaleras mecánicas operativos, entradas/salidas cerradas.

| Elemento | Estado | Evidencia/límite |
|---|---|---|
| Lifts/elevators | SUPPORTED (slice técnica) | EPIP-RT incluye FM y ejemplo “Elevator out of business”. No se cotejó el texto completo para determinar todos los campos/restricciones obligatorios. |
| Escalators | PARTIAL | FM y facility/equipment monitoring son pertinentes; la vista no demuestra elemento o caso escalator específico ni la constraint EPIP-RT. |
| Station facilities | PARTIAL | El servicio FM monitoriza facilities; eso no prueba todos los tipos de instalación del nodo. |
| Platform-related status | UNRESOLVED | ET tiene “platform changes” sobre plataforma asignada a journey; no acredita estado operativo de la plataforma como instalación. |
| Closed entrances/exits | UNRESOLVED | No se demostró elemento FM exacto. Un aviso SX no prueba por sí solo un estado estructurado/perfilado para entrada/salida. |

No asumir que SIRI-FM cubre todo C08. Recomendación de evolución: mantener el concept padre y limitar cualquier futura capability/mapping al scope demostrado (opción C); registrar semántica PARTIAL. No crear subconcept en esta sesión. Si estados de elevador/equipo, plataforma e ingreso requieren cobertura o reglas independientes, pedir ARCHITECTURE_REVIEW_REQUIRED antes de rediseñar. La capability propuesta CAP-SIRI-EPIP-RT-FM-STATION-EQUIPMENT-STATUS es PARTIAL y, por ahora, su evidencia más directa es el caso de elevador. Mapping propuesto (no persistido): M06-B02-MAP-A05-P02-001-SIRI-FACILITY-STATUS, PARTIAL. C08 = PARTIAL, no READY_FOR_PERSISTENCE.

## Incertidumbres y decisión humana

1. Consultar el texto completo 15531-7:2025 para restricciones y campos de ET/SX/FM frente a cada subelemento Annex.
2. Decidir si basta una ruta FM parcial con el scope demostrado o si hace falta futura descomposición del concepto.
3. Mantener VM fuera de C07 salvo cambio explícito de scope a posición de vehículos.
4. U01/U02/U03 del mismo requirement siguen abiertos y cuentan contra cualquier conclusión FULL de P02.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
