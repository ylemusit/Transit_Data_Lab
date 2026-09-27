# Phase 3 M03 — catálogo piloto de evidencia

Revisado: 2026-09-27. Alcance limitado a los cinco requisitos piloto indicados en el protocolo M03. Este documento registra capacidades técnicas observadas; no declara cumplimiento jurídico, conformidad de un dataset ni representabilidad integral de un requisito.

## Requisitos piloto y extracción conceptual

| ID canónico congelado | Fuente legal | Concepto que se evalúa | Relevancia de formato | Evidencia adicional no proporcionada por un formato |
| --- | --- | --- | --- | --- |
| `EU-2017-1926-REQ-A04-P01-001` | Reglamento (UE) 2017/1926, art. 4(1), Anexo punto 1 | Acceso desde el NAP a datos de desplazamientos y tráfico estáticos, históricos y observados de varios modos | Parcial: puede haber datos de horarios estáticos; la amplitud de categorías, modos, acceso NAP y condición histórico/observado requiere análisis por perfil y sistema | Disponibilidad real en NAP, cobertura de categorías/modos, permisos y acceso efectivo |
| `EU-2017-1926-REQ-A04-P02-001` | Art. 4(2), Anexo punto 1 | Representación mediante perfiles mínimos de la UE o nacionales cuando sean aplicables NeTEx/DATEX II | Sí; NeTEx es el único estándar de los cuatro dentro de este piloto nombrado expresamente por este requisito | Perfil mínimo nacional aplicable, DATEX II para su ámbito, condición de aplicabilidad y validación de implementación |
| `EU-2017-1926-REQ-A08-P03-001-01` | Art. 8(3) | Indicar la fuente al reutilizar datos si el titular lo solicita | Parcial: un feed puede contener publisher/attribution metadata, pero esos campos no prueban la fuente de cada dato ni el cumplimiento de una solicitud | Identidad de la fuente del dato, solicitud, respuesta, trazabilidad del dato y evidencia de entrega al usuario |
| `EU-2017-1926-REQ-A05-P03-001` | Art. 5(3)(a) | Fecha límite para datos del Anexo punto 2.1 para la red RTE-T global (2025-12-01) | No para la obligación temporal; fechas de validez de un feed no acreditan cumplimiento de la fecha jurídica | Evidencia documental/procedimental de disponibilidad en plazo y aplicabilidad geográfica |
| `EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS` | Art. 9(3) | Comprobaciones aleatorias de exactitud de declaraciones del art. 9(2)(c) por Estados miembros | No: es una actividad de supervisión institucional | Registros, metodología y evidencia de ejecución de comprobaciones; la norma no concreta aquí frecuencia, muestra ni método |

## Fuentes oficiales revisadas

| Fuente | Emisor | Versión/perfil | Localizador usado | Capacidades relacionadas | Fecha | Límite |
| --- | --- | --- | --- | --- | --- | --- |
| [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/) | MobilityData / proyecto GTFS | Revisión indicada en la propia referencia: 2026-04-27 | “Dataset Files”; `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt`; `feed_info.txt`; `attributions.txt` | `CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES`, `CAP-GTFS-FEED-PUBLISHER-METADATA`, `CAP-GTFS-DATASET-ATTRIBUTION` | 2026-09-27 | Referencia viva, no versión congelada. Define estructura/campos, no cobertura legal, fuente de cada dato ni disponibilidad en NAP. Los datos descritos son GTFS Schedule; esta evidencia no demuestra cobertura histórica/observada o todos los modos del Anexo. |
| [NeTEx extension for New Modes — Detailed Scope](https://www.netex-cen.eu/wp-content/uploads/2021/04/NeTEx-extension-for-New-Modes-Detailed-Scope.pdf) | CEN PT0303 / sitio NeTEx-CEN | Documento de alcance publicado en el sitio CEN; describe contexto NeTEx y perfiles | pp. 2–3: estructura de especificación, XML/schema; uso de perfiles; Part 4 European Profile; pp. 4–5: conceptos de red/horarios | `CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE` | 2026-09-27 | Documento de alcance, no el texto normativo completo ni el contenido de cada elemento del EPIP. El PDF menciona explícitamente que el perfil determina elementos/códigos requeridos. No prueba el perfil mínimo nacional que corresponda. |
| [Standards for implementation — Transmodel](https://transmodel-cen.eu/index.php/standards-for-implementation/) | Transmodel/CEN ecosystem | CEN/TS 16614-4:2017 EPIP; CEN/TS 16614-6:2024 EPIAP listado separadamente | Tabla “NeTEx Profiles”, filas Part 4 y Part 6; tabla de relación Transmodel–NeTEx | Identidad y contexto de perfil para `CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE` | 2026-09-27 | Página de índice, no texto normativo. No se infiere que EPIP sea automáticamente el perfil mínimo nacional exigible bajo el art. 4(2). |
| [DATEX II Specifications](https://datex2.eu/specifications/) y [documentación oficial v3.3](https://docs.datex2.eu/v3.3/general/index.html) | DATEX II organisation; estándar CEN/TC 278 | Familia DATEX II v3; partes CEN EN/TS 16157 | Página “Specifications”: Partes 1–13 y alcance por familia; portal general: modelo de datos de tráfico/viajes y publicaciones de datos medidos/elaborados | Revisión de la mención expresa a DATEX II en A04(2); no se creó capacidad en M02 | 2026-09-27 | Estas fuentes acreditan el ámbito general road traffic/travel, pero no relacionan aquí cada categoría del Anexo punto 1 con un perfil concreto. El registro M02 limita `standard_kind` a GTFS Schedule, GTFS Realtime, NeTEx y SIRI; no se amplió el framework para encajar DATEX II. |
| [Reglamento Delegado (UE) 2017/1926 — EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2017/1926/oj/eng/pdf) | Unión Europea / EUR-Lex | Texto oficial del Reglamento | Arts. 4(1)–(3), 5(3)(a), 8(3), 9(1)–(3), Anexo punto 1 | Base legal para delimitar conceptos; no se usa para probar detalle técnico de formatos | 2026-09-27 | Fuente legal, separada de evidencia técnica. No se deduce frecuencia, muestra o método para las comprobaciones aleatorias. |

## Catálogo técnico registrado

| Capability ID | Estándar/contexto | Afirmación acotada respaldada | Limitación explícita |
| --- | --- | --- | --- |
| `CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES` | GTFS Schedule, referencia viva revisada 2026-04-27 | La referencia define rutas, viajes, paradas y tiempos de llegada/salida asociados a viajes | No demuestra datos de todos los modos ni satisface por sí sola las categorías estáticas/históricas/observadas del Reglamento |
| `CAP-GTFS-FEED-PUBLISHER-METADATA` | GTFS Schedule | `feed_info.txt` permite expresar identidad/URL del editor del dataset y metadatos del feed | Editor del feed no equivale necesariamente a fuente de cada dato; no representa prueba de solicitud/respuesta del art. 8(3) |
| `CAP-GTFS-DATASET-ATTRIBUTION` | GTFS Schedule | `attributions.txt` permite atribuciones a nivel dataset o agencia/ruta/viaje | La presencia de atribución no demuestra que identifique la fuente legalmente relevante de todos los datos reutilizados |
| `CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE` | NeTEx, EPIP CEN/TS 16614-4:2017 como perfil identificado | Las fuentes públicas revisadas sitúan NeTEx como formato de intercambio de datos estáticos de transporte público y describen perfiles para fijar elementos/códigos; CEN identifica la familia de red y horarios | Detalle normativo del perfil no revisado por falta de texto público completo; el perfil mínimo nacional aplicable permanece sin determinar |

Todos los registros están marcados `NEEDS_REVIEW`; son evidencia preliminar reutilizable, no aprobación semántica. No se registran afirmaciones de representabilidad ni mappings requisito-capacidad.

## Fuera de alcance / pendientes de evidencia

- GTFS Realtime y SIRI no se investigaron: ninguno de los conceptos congelados del piloto requiere explícitamente intercambio dinámico en tiempo real para responder a la pregunta M03 acotada.
- DATEX II sí se investigó a nivel mínimo porque A04(2) lo nombra expresamente. Las fuentes oficiales confirman su ámbito general de tráfico y viajes por carretera y la familia CEN EN/TS 16157, pero no bastan para asociar las categorías concretas del Anexo a un perfil. M02 no permite registrar DATEX II como `standard_kind`; no se cambió el framework ni se inventó una capacidad. Esta limitación reduce la preparación del catálogo para A04(2).
- No se establece que GTFS Schedule cumpla el Anexo punto 1, los perfiles mínimos nacionales o el art. 8(3).
- No se pudo establecer el contenido normativo detallado del EPIP ni identificar un perfil mínimo nacional concreto. `EVIDENCE_NOT_ESTABLISHED`: equivalencia/identidad entre EPIP CEN/TS 16614-4:2017 y el perfil mínimo nacional aplicable al requisito A04(2).
- `EVIDENCE_NOT_ESTABLISHED`: perfil DATEX II concreto y categorías del Anexo punto 1 que representa para el requisito A04(2); la evidencia pública consultada solo respalda el ámbito general.
- No se pudo establecer desde las fuentes técnicas un identificador de origen del dato por elemento equivalente a la obligación de indicar su fuente bajo solicitud; los campos GTFS observados solo respaldan publisher/attribution con los límites descritos.

## Clasificación para revisión futura

- Requieren evaluar capacidad técnica potencial: A04-P01-001 (parcial), A04-P02-001, A08-P03-001-01 (parcial).
- Requieren principalmente evidencia legal, temporal, institucional o manual: A05-P03-001 y A09-P03-RANDOM_CHECKS; A08-P03-001-01 también requiere evidencia de la solicitud y respuesta.
- Próximo paso: revisión humana del alcance de las fuentes, perfil mínimo nacional NeTEx y perfil DATEX II aplicable a A04(2). Además, M02 necesita una decisión de esquema para poder registrar DATEX II antes de poblar una capacidad DATEX. Después podrá iniciarse el primer mapping piloto revisado. Este catálogo todavía no está listo para aprobar un mapping de A04(2).

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## M03B — evidencia de perfiles para A04(2)

Fecha de investigación: 2026-09-27. Requisito focal: `EU-2017-1926-REQ-A04-P02-001`. La consulta de la fila congelada confirma el texto de condición y que este trabajo no altera la legalidad materializada. La base legal se contrastó con la versión consolidada EUR-Lex de 2024-03-04: artículo 4(2), en relación con artículo 4(1)(a)-(c), artículo 4(3) y Anexo, punto 1. El apartado 2 no asigna por sí mismo cada categoría a un formato; su condición es la aplicabilidad técnica de NeTEx o DATEX II.

### Distinciones y hechos legales

- **Legal requirement:** los datos estáticos, históricos y observados enumerados en el punto 1 del Anexo para los que NeTEx y DATEX II sean aplicables se representarán a través de perfiles mínimos UE o perfiles nacionales (art. 4(2)). El apartado no autoriza extender el análisis a los datos dinámicos del punto 2.
- **Standard technical capability:** documentación técnica de NeTEx cubre intercambio de red, horarios, tarifas y accesibilidad en perfiles/familias diferentes; DATEX II cubre información de tráfico y viajes por carretera y publica subconjuntos RRP para casos de uso.
- **Profile implementation:** disponer de un perfil o tener archivos publicados no prueba que un titular lo implemente correctamente ni que sea aplicable a una categoría legal concreta.
- **Spanish NAP practice:** la ficha NAP observada demuestra publicaciones NeTEx, pero no una especificación nacional, versión o regla de validación que formalice un perfil español. La publicación no acredita perfil nacional.

### Perfil NeTEx y precedencia

| Perfil | Versión/estado | Emisor y alcance documentado | Categorías del punto 1 potencialmente relacionadas | Evidencia y localizador | Límite |
| --- | --- | --- | --- | --- | --- |
| EPIP — European Passenger Information Profile | CEN/TS 16614-4:2017 (índice Transmodel) | Perfil europeo para intercambio de información al pasajero. Transmodel/CEN lo vincula a perfiles para NAP; incluye el mínimo de información que se comparte entre países para información al pasajero, según FAQ | 1.1, datos programados de red y horarios del transporte público; relación potencial, no correspondencia de cada elemento | [Standards for implementation](https://transmodel-cen.eu/index.php/standards-for-implementation/), tabla NeTEx Profiles; [FAQ NeTEx](https://transmodel-cen.eu/index.php/faq-netex/), apartado “recommended process” | El texto normativo completo no se revisó. Ni la FAQ ni el índice demuestran que EPIP sea el perfil mínimo jurídicamente aplicable a cada fila del Anexo o que cubra datos históricos/observados.
| EPIAP — European Passenger Accessibility Information Profile | CEN/TS 16614-6:2024, listado por Transmodel | Perfil europeo separado sobre información de accesibilidad | 1.1(d) instalaciones/características de accesibilidad asociadas a acceso y transporte programado, sujeto a análisis de elementos | [Standards for implementation](https://transmodel-cen.eu/index.php/standards-for-implementation/), fila Part 6 | El índice establece identidad/tema; no se verificó texto normativo ni correspondencia legal elemento a elemento.
| Información tarifaria NeTEx | CEN/TS 16614-3:2015 como familia técnica; perfil europeo de tarifas se indicaba en desarrollo en FAQ | Parte técnica de tarifas; FAQ declara que perfiles UE mínimos de tarifas estaban en desarrollo en su publicación consultada | 1.2(c)(i) tarifas comunes, relación técnica potencial | [NeTEx overview](https://transmodel-cen.eu/index.php/netex/); [FAQ NeTEx](https://transmodel-cen.eu/index.php/faq-netex/), líneas sobre perfiles de tarifas | No se establece un perfil EU de tarifas ya publicado/aplicable, ni perfil nacional español.

La guía de Transmodel/CEN recomienda usar perfiles mínimos UE como base y permanecer cerca de EPIP al desarrollar perfiles nacionales; esto es orientación técnica, no una obligación operativa nueva. El artículo 4(2) consolidado ofrece la alternativa “perfiles mínimos de la UE o perfiles nacionales”; no repite en su texto operativo la regla de precedencia. El considerando 7 del acto base expresa que los perfiles nacionales deben basarse en un perfil europeo mínimo común cuando exista; se conserva como apoyo interpretativo y no se eleva a condición adicional del artículo 4(2). **Precedencia: PARTIAL** — recomendación técnica clara; el alcance jurídico vinculante más allá del tenor operativo requiere revisión humana.

### DATEX II MMTIS

La documentación oficial llama a estos subconjuntos **Recommended Reference Profiles (RRP)**. Afirma que los RRP contienen el conjunto mínimo de elementos DATEX II para cada categoría específica de los reglamentos delegados y que pueden combinarse/ampliarse. Se mantiene exactamente esta denominación: no se equipara RRP con “EU minimum profile” legal del artículo 4(2).

La página MMTIS enumera: Nivel 1 perturbaciones y estados en tiempo real (todos los modos), indicando que tráfico por carretera está cubierto por perfiles de Reglamento 962; Nivel 2 tiempos actuales de tramo viario, cierres/desvíos ciclistas (bajo consideración), disponibilidad de estaciones de recarga/repostaje, plazas de aparcamiento/tarifas/tasas viarias; Nivel 3 predicción futura de tiempos de viaje viarios. La propia página advierte que perfiles y documentación evolucionan. De ello solo se establece que existen esos RRP/casos de uso en la documentación consultada, no su vigencia normativa completa ni su aplicación a todas las filas de punto 1. Las categorías de recarga/repostaje fueron retiradas del alcance MMTIS por la reforma 2024/490; no se asignan a A04(2). Perfiles de Nivel 1 son principalmente punto 2 dinámico y quedan fuera del alcance de asignación de M03B.

Fuentes: [MMTIS RRP overview](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/), apartados “Recommended Reference Profiles” y “FOR THE DELEGATED REGULATION 1926/2017”; [RRP Road Link traveltime](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls2a-current-road-link-travel-times/), alcance de tiempos actuales por enlace viario; EUR-Lex Reglamento 2024/490, considerandos y modificación del Anexo. Dependencia: los perfiles DATEX de Reglamento 962/2015 para datos de carretera son otro marco normativo/técnico y no se han investigado elemento por elemento.

### España: perfil nacional

- `NETEX_ES_NATIONAL_PROFILE = EVIDENCE_NOT_ESTABLISHED`. Búsqueda dirigida en fuentes oficiales `nap.transportes.gob.es` y `transportes.gob.es` no localizó designación o documento oficial de perfil nacional, versión, reglas de envío o validador que lo formalice. La [lista/ficha NAP](https://nap.transportes.gob.es/Files/Detail/1003) muestra formatos publicados, incluyendo NeTEx; esto acredita práctica de publicación, no perfil nacional. No es prueba de inexistencia.
- `DATEXII_ES_NATIONAL_PROFILE = EVIDENCE_NOT_ESTABLISHED`. No se localizó designación, especificación nacional MMTIS, regla NAP o validador de perfil español en la búsqueda oficial acotada. Material ministerial localizado menciona DATEX II como estándar europeo en contexto de proyectos de tráfico, no como perfil nacional MMTIS. No es prueba de inexistencia.

### Matriz acotada del Anexo, punto 1

Granularidad: subapartados jurídicos 1.1–1.4. No se inventan identificadores. El requirement A04(2) congelado no contiene campos `DATA_ELEMENT` propios; por tanto no se fuerza un join ficticio con otras obligaciones atómicas. La matriz expresa aplicabilidad técnica potencial sin afirmar compatibilidad de cada elemento.

| ANNEX_ID | ANNEX_DESCRIPTION | TRANSPORT_CONTEXT | NETEX_APPLICABILITY / PROFILE / SOURCE | DATEXII_APPLICABILITY / PROFILE / SOURCE | SPAIN_NATIONAL_PROFILE | EVIDENCE_STATUS | LIMITATION |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Nivel de servicio 1: tiempos de paso, planes de viaje e información auxiliar estática | Transporte programado y contexto de red multimodal | PARTIAL: NeTEx partes 1–2 y EPIP son técnicamente pertinentes a red/horarios de transporte público; Transmodel NeTEx overview y EPIP | PARTIAL: MMTIS RRP Nivel 1 cubre perturbaciones/tiempo real; para carretera remite a Reglamento 962. Se refiere en gran parte a datos dinámicos punto 2, así que no asigna categorías 1.1 automáticamente | No establecido | PARTIAL | Requiere comparación de subelementos 1.1 con perfiles y separar programado de observado/dinámico.
| 1.2 | Nivel de servicio 2: localización, compra/pago e información auxiliar (incluye tarifas, instalaciones) | Transporte programado, a demanda y movilidad personal según subapartado | PARTIAL: NeTEx Network/Timetable, tarifa CEN/TS 16614-3 y EPIAP parecen técnicamente relacionados con algunos conceptos; fuente Transmodel | PARTIAL: RRP MMTIS enumera estacionamiento/tarifas y otros casos, pero documentación no basta para mapear todo el punto 1.2; RRP de recarga/repostaje no vigente para MMTIS tras 2024/490 | No establecido | PARTIAL | Sin perfil tarifa UE verificado como publicado; categorías heterogéneas y ámbitos distintos.
| 1.3 | Nivel de servicio 3: tarifas especiales, reserva, detalle de red ciclista y cálculo de viaje | Programado y a demanda; bicicleta | PARTIAL: familia NeTEx admite tarifas/red; sin prueba de perfil para tarifas especiales, reservas o cada elemento ciclista | PARTIAL: RRP de predicción de tiempos de viaje es road-link; cierres ciclistas se indican “under consideration”, insuficiente para designación | No establecido | PARTIAL | Algunas categorías son cálculos/atributos y no se verificó un perfil concreto por elemento.
| 1.4 | Nivel de servicio 4: datos históricos/observados de retrasos, cancelaciones y tarifas de aparcamiento | Programado y a demanda; modos varios | UNRESOLVED: EPIP de información al pasajero no prueba cobertura histórica/observada | PARTIAL: RRP MMTIS lista estados/perturbaciones, pero vinculados en gran parte a punto 2 dinámico o carretera bajo 962; no se estableció perfil para todas las series históricas/observadas 1.4 | No establecido | UNRESOLVED | No se ha encontrado correspondencia normativa elemento a elemento para las categorías temporales multimodales 1.4. A04(2) sigue condicional a aplicabilidad demostrada.

Estado agregado de filas: `ROWS=4; ESTABLISHED=0; PARTIAL=3; UNRESOLVED=1; NOT_APPLICABLE=0`. Elementos exactos no resueltos: categorías 1.4(a)-(c), además de las correspondencias elementales de 1.1–1.3. `B_I_D_I_LIMITATION_AFFECTED_ROWS=0`: no se usaron campos fuente B-I/D-I para crear filas de matriz ni se reparó Phase 1; la matriz se limita a identificadores del Anexo literal.

### Registro y límites de M03B

El seed incorpora identidad DATEX II y una capacidad técnica genérica de perfiles RRP de tiempos viarios, con referencias oficiales, localizadores y limitaciones; ambas quedan pendientes de revisión. No se crea afirmación de representabilidad ni mapping. `NEW_REQUIREMENT_CAPABILITY_MAPPINGS=0`; `FINAL_REPRESENTABILITY_ASSERTIONS=0`. El registro no convierte RRP en perfil mínimo legal ni crea perfil español.

Fuentes primarias registradas: EUR-Lex consolidado 2024-03-04 (art. 4 y Anexo punto 1); Reglamento 2024/490; Transmodel/CEN NeTEx overview, estándares y FAQ; documentación oficial DATEX II MMTIS y RRP road-link; NAP oficial español. `EVIDENCE_NOT_ESTABLISHED`: correspondencia completa NeTEx/DATEX con filas 1.1–1.4; perfil nacional NeTEx España; perfil nacional DATEX II España; identidad del perfil tarifa mínimo UE ya publicado.

### Evaluación y siguiente paso

La evidencia **no basta aún para un mapping aprobado**. Sí basta para que una revisión humana examine el expediente y decida si alguna fila/capacidad puede mapearse, manteniendo las filas parciales como tales. La recomendación es `NEXT_ACTION=M03_HUMAN_REVIEW`, con continuación focalizada M03C solo si el revisor pide las correspondencias de 1.4 o perfiles españoles. No se amplió el esquema fuera de M02A, no se tocaron Phase 1/2 y no se crearon mappings.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Checkpoint humano M02A + M03 + M03B — 2026-09-27

Decisión de revisión humana: **M02A arquitectura ACCEPTED**; **M03 evidencia ACCEPTED_WITH_LIMITATIONS**; **M03B evidencia ACCEPTED_WITH_LIMITATIONS**. EPIP, EPIAP y DATEX II MMTIS Recommended Reference Profiles quedan `ACCEPTED_WITH_LIMITATIONS`. El perfil nacional NeTEx español y el perfil nacional DATEX II español siguen `EVIDENCE_NOT_ESTABLISHED`; no se afirma su inexistencia. La representabilidad completa de A04(2) es `NOT_ESTABLISHED` y su mapping final `NOT_APPROVED`. Las categorías no resueltas del Anexo permanecen `PRESERVED_AS_UNRESOLVED`. No se requiere investigación amplia M03C en esta etapa; una cuestión pendiente se convierte en deuda de investigación focalizada cuando un mapping concreto dependa de ella.

**Regla de validación:** `LEVEL_A = PASS` acredita solo consistencia técnica con el modelo Phase 3 y sus invariantes estructurales. No acredita corrección semántica o jurídica, cumplimiento, aceptación de mappings, revisión humana ni aprobación de reglas de auditoría. Toda consideración de aceptación sustantiva requiere revisión semántica humana.

**Límite evidencia/mapping:** estándares 3, capacidades 5, referencias fuente 7 y excepciones 3; mappings requisito-capacidad 0, assertions finales de representabilidad 0 y `audit.rules` 0. Este checkpoint cierra la preparación de evidencia y preserva el límite antes de mapping. Siguiente acción: **M04 pilot mapping and human semantic review**. Las decisiones son de revisión del expediente; no constituyen conclusión de cumplimiento jurídico.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
