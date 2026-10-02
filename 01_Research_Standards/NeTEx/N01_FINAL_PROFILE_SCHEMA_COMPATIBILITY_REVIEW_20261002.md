# NeTEx N01 — revisión final de compatibilidad perfil/schema

**Fecha de corte:** 2026-10-02
**Estado del gate:** `N01_TECHNICAL_REVIEW = PASS`; `N01 = READY_FOR_HUMAN_SCOPE_DECISION`
**Límite:** revisión documental. No se ejecutó validación XSD de feeds, no se capturaron ni congelaron schemas y no se implementaron reglas.

## A. Baseline técnica propuesta

Propuesta para deliberación, no decisión adoptada:

```ini
TARGET_MARKET = SPAIN
TARGET_MODE = REGULAR_SCHEDULED_BUS
DATA_DOMAIN = STATIC_SCHEDULED_PASSENGER_INFORMATION
NETEX_SCHEMA_BASELINE = v2.0.x
REFERENCE_RELEASE = v2.0.0
PROFILE_BASELINE = EPIP / CEN/TS 16614-4:2026
SPANISH_PROFILE_LAYER = NO_ADDITIONAL_PUBLIC_PROFILE_IDENTIFIED
NAP_ACCEPTANCE_CONTRACT = NOT_PUBLICLY_IDENTIFIED
```

`v2.0.0` es una base de schema razonable para desarrollar el caso de uso de red y horarios: el repositorio asociado al grupo NeTEx/CEN marca ese release como producción para las partes 1, 2, 3 y 5, y recomienda fijar release de tres componentes para desarrollo. La propuesta **no** afirma que ese XSD aplique por sí solo todas las restricciones EPIP 2026. EPIP debe derivarse del texto normativo versionado y verificarse requisito a requisito contra la implementación elegida.

```ini
EPIP_2026_MODEL_COMPATIBLE_WITH_NETEX_V2 = PARTIAL
NETEX_V2_0_0_USABLE_AS_V1_SCHEMA_BASELINE = YES_WITH_LIMITATIONS
PROFILE_NORMATIVE_BASELINE = KNOWN
PROFILE_MACHINE_IMPLEMENTATION = PARTIAL
EXACT_EPIP_2026_XSD_OR_SCHEMATRON = NOT_PUBLICLY_IDENTIFIED
```

La compatibilidad parcial significa que la edición EPIP 2026 se publica como parte revisada de la serie NeTEx que acompaña la revisión v2, y que la base NeTEx v2 cubre los dominios de red y horarios pertinentes; el cotejo de todas las restricciones, dependencias, cardinalidades y condiciones del perfil contra `v2.0.0` no está demostrado. La muestra pública de la edición 2026 conserva una afirmación de que EPIP fue especificado para NeTEx 1.1. Se trata como ambigüedad documental que debe resolverse con el texto íntegro controlado y trazabilidad normativa, no como prueba automática de incompatibilidad ni como texto que se pueda ignorar.

No se clasificó ningún concepto objetivo como `NOT_REPRESENTABLE`: con la evidencia parcial revisada no se ha probado una carencia de expresividad del modelo v2. Eso no significa que todas las restricciones EPIP estén implementadas; los requisitos sin cotejo permanecen `UNKNOWN` o `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED`.

## B. Fuentes de autoridad y artefactos EPIP 2026

El inventario identifica artefactos públicos relacionados encontrados en esta revisión; no afirma que no existan recursos no publicados o distribuidos por canal restringido. `N02_SOURCE_REGISTER_INITIAL_20261002.md` conserva el registro general anterior; las fuentes nuevas deben añadirse allí con IDs N02-27 en adelante si se incorpora una revisión posterior.

| ID | Artefacto / autoridad | Versión y estado | Formato / relación | Clasificación y límite |
|---|---|---|---|---|
| A1 | CEN/TS 16614-4, CEN/TC 278; edición identificada también como UNE-CEN/TS en BOE | `2026`, activa; ratificada como UNE en abril de 2026 | Norma de perfil; versión íntegra bajo acceso/licencia. La muestra pública consultada consta de 15 páginas de vista previa, no documento completo | Autoridad normativa del perfil. Define EPIP para intercambio de información al pasajero, con datos básicos de red y horarios. El extracto público no permite construir una lista completa de requisitos. |
| A2 | Repositorio `TransmodelEcosystem/NeTEx`, asociado al trabajo NeTEx/CEN | Rama estable `v2.0`; release `v2.0.0`, febrero de 2026 | XSD para framework y partes 1, 2, 3 y 5; examples funcionales y de estándares; changelog/README | Artefacto de implementación del modelo/schema base. No incluye paquete de schemas Parte 4/EPIP. La rama es mutable; releases son snapshots. Hay que fijar tag/commit y hashes antes de usarla en corpus. |
| A3 | Ejemplos de estándares en el repositorio NeTEx | Rama `v2.0` y carpetas de ejemplos | XML machine-readable; README los define como ejemplos ilustrativos, a usar en conjunto | Útiles para explorar representaciones. Rama mutable; no se ha demostrado qué ejemplos corresponden a EPIP 2026 ni que implementen todas sus reglas. |
| A4 | `NeTEx-Profile-EPIP`, TransmodelEcosystem/Data4PT | Archivo desde 2026-05-03; XSD creado en 2021 sobre NeTEx 1.3.1; no mantenido | `NeTEx_publication_EPIP.xsd`, variante sin restricciones, contenido XSD y GML simplificado | `LEGACY_IMPLEMENTATION_REFERENCE`. Comparación histórica/migración solamente; no autoridad ni validador EPIP 2026. |
| A5 | Publicación NAPCORE MMTIS Quality Framework y diccionario NAPCORE de ejemplos | Guías públicas de proyecto, no norma CEN ni legislación | Recomiendan EPIP para interoperabilidad y enlazan ejemplos del repo NeTEx | Contexto interpretativo/descubrimiento. No sustituyen norma ni prueban compatibilidad 2.0. |
| A6 | Material de migración | No se identificó guía pública específica de migración EPIP 1.3.1→EPIP 2026 o NeTEx 2.0 | README/changelog del schema describen versiones, releases y ramas WIP | Gap. El paso de versión requiere un análisis de diferencias controlado; no inferirlo por número de versión. |
| A7 | Schematron, constraints profile-specific, tests de conformidad o implementación oficial EPIP 2026 | No identificados en el material público revisado | El XSD general v2 incorpora algunas constraints de schema; el README recomienda el XSD de publicación para validación, pero no declara que implemente EPIP | La disponibilidad de XSD v2 no equivale a implementación del perfil. No se encontró Schematron ni suite oficial de conformidad EPIP 2026. |
| A8 | Modelo/documentación de conceptos | La norma EPIP 2026 describe conceptos y restricciones; repo XSD da documentación estructural del schema | Texto de la norma + XSD/modularización del modelo NeTEx | No se identificó un modelo formal descargable aparte que una perfil 2026 con schema 2.0.0. Mantener norma y XSD como capas separadas. |
| A9 | Implementaciones oficiales/de referencia | No identificadas para EPIP 2026 + NeTEx 2.0.0 | Los ejemplos son evidencia ilustrativa, no software de validación | No atribuir estatus oficial a herramientas externas ni a implementaciones de perfiles nacionales. |

### Inventario machine-readable y autoridad

| SOURCE_ID | TITLE | AUTHORITY | VERSION / DATE | STATUS | PUBLIC_URL | MACHINE_READABLE | RELATION_TO_EPIP_2026 | RELATION_TO_NETEX_V2 |
|---|---|---|---|---|---|---|---|---|
| N01-COMP-01 | Public transport — NeTEx — Part 4: Passenger Information European Profile | CEN/TC 278; adopción española UNE confirmada en BOE | CEN/TS 16614-4:2026; aprobado 2026-02-09, publicado 2026-02-18; ratificación UNE abril 2026 | Norma vigente; texto íntegro comercial/controlado; preview público incompleto | https://app.nbn.be/data/r/platform/frontend/detail?p40_id=3499334&p40_language_code=en ; https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-10207 | Documento normativo no distribuido como artefacto abierto; preview PDF indexable | Autoridad primaria de EPIP | La ficha dice serie revisada publicada como NeTEx v2; falta mapear constraints/refs exactas |
| N01-COMP-02 | NeTEx XML Schema repository, branch v2.0 / release v2.0.0 | Repositorio TransmodelEcosystem asociado al grupo NeTEx/CEN | Rama v2.0; release v2.0.0, febrero 2026; branch mutable y release snapshot | Activo estable con bug fixes en rama; release clasificado producción | https://github.com/TransmodelEcosystem/NeTEx/tree/v2.0 ; https://github.com/TransmodelEcosystem/NeTEx/releases/tag/v2.0.0 | Sí: XSD XML, ejemplos XML; relación exacta debe fijarse por tag/commit/hash | Artefacto de modelo/schema base, no perfil Parte 4 | Implementación schema v2 de partes 1/2/3/5; no se halló EPIP-specific schema |
| N01-COMP-03 | NeTEx standards examples | Repositorio TransmodelEcosystem/NeTEx | Rama v2.0 actual; fecha/commit varía | Ejemplos públicos, rama mutable, sin garantía de conformidad total | https://github.com/TransmodelEcosystem/NeTEx/tree/v2.0/examples/standards | Sí: XML | Relación EPIP 2026 no documentada ejemplo por ejemplo; ejemplos son ilustrativos | Ejemplos contra árbol v2; no sustituyen release fijo ni norma |
| N01-COMP-04 | NeTEx-Profile-EPIP XSD | Data4PT / TransmodelEcosystem repository | XSD basado en NeTEx 1.3.1; creado 2021; archivado 2026-05-03 | Archivo legado, no mantenido | https://github.com/TransmodelEcosystem/NeTEx-Profile-EPIP | Sí: XSD XML | Implementa referencia EPIP histórica; no autoridad para EPIP 2026 | No valida baseline v2 ni sirve como prueba de compatibilidad |
| N01-COMP-05 | NAPCORE MMTIS Quality Framework v1 | NAPCORE | v1, publicado 2025 | Guía técnica informativa | https://napcore.eu/wp-content/uploads/2025/06/NAPCORE-MMTIS-Quality-Framework_v1_250411.pdf | Sí: PDF | Recomienda EPIP y/o EPIAP para interoperabilidad programada | No demuestra implementación ni mapping a release v2.0.0 |
| N01-COMP-06 | NeTEx 1.3.1 to EPIP 2026 / NeTEx 2 migration notes | No se identificó una autoridad o artefacto público | No identificado | No identificado en fuentes públicas revisadas | — | No identificado | Gap de transición del perfil | Gap de migración del schema |
| N01-COMP-07 | EPIP 2026 Schematron, conformance ruleset or test suite | CEN/TC 278 / repositorios públicos revisados | No identificado | No identificado en fuentes públicas revisadas | — | No identificado | No hay ruleset público que implemente de forma demostrada el perfil completo | Los XSD generales no constituyen ese ruleset |
| N01-COMP-08 | EPIP 2026 model files / implementation guide | CEN/TC 278 / repositorios públicos revisados | No se identificó artefacto separado; conceptos documentados en texto EPIP | No identificado como paquete machine-readable | — | No identificado como artefacto separado; XSD base sí | El texto EPIP sigue siendo autoridad de los conceptos/restricciones | No hay mapping formal publicado entre perfil y release schema |
| N01-COMP-09 | Official/reference EPIP 2026 + NeTEx 2 implementation | No identificada | No identificada | No identificada en fuentes públicas revisadas | — | No identificado | No hay implementación oficial/referencia establecida | Los ejemplos XML no prueban implementación del perfil |

La serie CEN/TS 16614 distingue formato/modelo (partes 1/2, entre otras) y perfil EPIP (parte 4). El repo XSD se declara esquema para partes 1, 2, 3 y 5; incluye una publicación general de NeTEx, pero no una capa EPIP 2026. El texto íntegro CEN es necesario para cerrar los puntos de cardinalidad y condición. La BOE confirma ratificación UNE-CEN/TS 16614-4:2026, que no crea por sí misma una capa de perfil nacional española ni reglas NAP.

## C. Matriz de compatibilidad (nivel de concepto)

La matriz es una clasificación documental inicial, no catálogo de requisitos normativos exhaustivo. Los conceptos se obtienen del alcance público y de la estructura/índice visible de EPIP; no se inventan cardinalidades del documento completo. Cuando no se dispone del texto controlado, se conserva `UNKNOWN` y se identifica el dato que falta.

| Requisito / concepto EPIP | Representación candidata NeTEx v2 | Artefacto schema | Fuente de constraint | Cardinalidad / condición | ¿Machine-checkable hoy? | Clasificación / ambigüedad |
|---|---|---|---|---|---|---|
| Red, paradas y jerarquía de StopPlace | Objetos de red y `StopPlace`/componentes del dominio topológico | XSD framework + parte 1, release 2.0.0 | Reglas detalladas EPIP 2026, incluidos selección de objetos, atributos y cardinalidades | No extraíble íntegramente de la muestra. Aplicabilidad depende del bloque Stop Profile y la edición controlada | XSD v2 comprueba estructura/tipos/constraints que contiene; perfil completo no | `REPRESENTABLE_WITH_PROFILE_CONSTRAINT`; restricciones EPIP v2 sin cotejar |
| Operadores/autoridades y responsabilidad | `Operator`, `Authority`, relaciones de responsabilidad/refs | XSD framework/parte 1; validar nombres exactos en release fijado | EPIP 2026 y referencias normativas NeTEx | Condiciones, obligatoriedad de referencias y cardinalidades deben extraerse de texto completo | Parcial en XSD para estructura/referencias; reglas del perfil no confirmadas | `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED`; no asumir que `ResponsibilitySet` requerido salvo fuente versionada |
| Líneas, sentidos, rutas y destino mostrado | `Line`, direcciones/rutas, `DestinationDisplay`, refs asociadas | XSD parte 1/framework y parte 2 donde aplique | EPIP 2026, perfil Network and Timetables | Muestra visible incluye estos conceptos; cardinalidades, campos requeridos y excepciones pendientes del texto íntegro | Estructura probable validable con XSD base; constraints EPIP incompletas | `REPRESENTABLE_WITH_PROFILE_CONSTRAINT`; el uso de `Route` u objetos similares no debe inferirse de ejemplos |
| Servicios, patrón de viaje, viajes y paradas/horas de paso | `ServiceJourney`, `JourneyPattern`, `VehicleJourney`/times y referencias a línea/paradas | XSD framework + parte 2 | EPIP 2026 y NeTEx 2 Part 2 | EPIP cubre datos de horario programado; regla de tiempos en cada parada es ejemplo de regla de calidad del perfil. Umbrales y excepciones exactos pendientes | Datos y cardinalidad estructural comprobables en parte; consistencia de secuencia/espaciado requiere reglas | `REPRESENTABLE_WITH_PROFILE_CONSTRAINT`; no todo se reduce a XSD |
| Calendario y validez temporal | `OperatingPeriod`, `DayType`, `DayTypeAssignment` y calendarios equivalentes | XSD parte 2/framework | EPIP 2026 + definiciones NeTEx 2 | Lógica de aplicación/solapamiento y obligatoriedad por servicio requieren cotejo normativo | XSD valida tipos; lógica temporal requiere reglas adicionales | `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED` |
| Traducciones y nombres localizados | Elementos multilingües de texto/`Name` y estructuras de idioma del modelo | XSD framework/partes pertinentes | EPIP 2026 | La muestra afirma soporte de traducciones alternativas; idiomas requeridos no especificados aquí | Sintaxis posiblemente verificable; cobertura de idiomas no sin perfil parametrizado | `REPRESENTABLE_WITH_PROFILE_CONSTRAINT` |
| Información básica de accesibilidad informativa | Atributos/entidades de accesibilidad relacionados con sitios/servicios | XSD base puede admitir parte del modelo; v2 README no lista Parte 6 | EPIP 2026 para información básica; EPIAP CEN/TS 16614-6 para alcance completo | La muestra dice que la accesibilidad EPIP es informativa y remite a EPIAP para descripción integral | No se ha demostrado integración de EPIAP en release 2.0.0 | `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED`; no excluir toda accesibilidad: incluir solo EPIP básico después de cotejo, diferir EPIAP completo |
| Consistencia referencial, unicidad, completitud estructural | IDs, refs y cardinalidades del modelo | XSD publicación v2 con constraints | XSD v2 + reglas de calidad EPIP 2026 | Depende de constraint concreta presente en release | Parte puede validarse por XSD; calidad referencial/semántica puede excederlo | `DIRECTLY_REPRESENTABLE` para estructura/modelo; conformidad EPIP global no se deriva |
| Coherencia de calidad: tiempos plausibles, stop names faltantes/duplicados | Cruces entre servicios, secuencia temporal y entidades de parada | XSD + futura capa de constraints/reglas | Reglas de consistencia/calidad EPIP 2026 | Ejemplos normativos públicos indican comprobaciones automáticas posibles; reglas exactas requieren texto íntegro | Algunas sí con reglas explícitas; ninguna regla local implementada en esta tarea | `REPRESENTABLE_WITH_PROFILE_CONSTRAINT`; completitud y verdad de campo no se prueban solo con schema |
| Tarifas, salvo zonas tarifarias básicas | Entidades de Fare de parte 3 si aplicable | XSD parte 3 existe en v2 | EPIP 2026 declara tarifas fuera de alcance salvo zonas básicas; perfil futuro de tarifas separado | Mantener solo zona básica si el caso de uso y texto normativo lo requieren | XSD puede validar forma, pero no alcance de tarifa EPIP automáticamente | `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED`; proponer solo zonas tarifarias básicas en V1, excluir fares completos |
| Tiempo real / operación | SIRI para tiempo real; ciertos objetos NeTEx de referencia estática | `netex_siri.xsd` integra NeTEx en SIRI, pero el dominio dinámico pertenece a SIRI | SIRI y perfil específico, no EPIP de datos estáticos | Fuera del caso V1 | No evaluado | `UNKNOWN` para compatibilidad de cualquier caso dinámico; fuera de alcance por decisión propuesta |
| Modos alternativos / ferrocarril complejo / multimodal | NeTEx partes 1/2/5 y clases modales especializadas | Parte 5 existe en v2; complejidad modal de partes 1/2 también | Perfil modal/nacional, EPIP y normativa aplicable | Bus regular limita la selección; las condiciones de extensiones no se infieren | XSD representa algunos conceptos; perfil bus no se ha probado | `REPRESENTABLE_BUT_IMPLEMENTATION_UNCONFIRMED`; deferir alcance especializado |
| Identificadores nacionales y extensiones españolas/operador | Identificadores/atributos de NeTEx y extensiones permitidas | XSD general v2 más mecanismos de extensión a cotejar | Perfil español o contrato NAP, no identificado públicamente | Reglas y sistema de autoridad desconocidos | No hasta identificar perfil/contrato | `UNKNOWN`; no derivar perfil de muestras de feeds |

### Capas de resultado

| Capa | Qué se conoce | Qué falta / qué no implica |
|---|---|---|
| A. Modelo NeTEx | La serie y el repo XSD contienen conceptos de red, paradas y horarios adecuados como candidatos para datos programados. | El modelo amplio no afirma obligación EPIP ni perfil exacto. |
| B. NeTEx XSD | Hay `v2.0.0` de producción para partes 1, 2, 3 y 5; el XSD principal de publicación es el recomendado por el README para validación. | No se identificó XSD de Parte 4/EPIP 2026. XSD válido no acredita restricciones EPIP. |
| C. Perfil EPIP | CEN/TS 16614-4:2026 es la referencia normativa europea identificada y ratificada por España. | Falta relevar el documento íntegro, sus cardinalidades/reglas y el cotejo de cada requisito con 2.0.0. La vista previa contiene una referencia heredada a NeTEx 1.1. |
| D. Publicación española/NAP | No se identificó perfil nacional adicional ni contrato de aceptación técnica en fuentes públicas revisadas. | No equivale a que no existan materiales no públicos ni a aceptación NAP. Solo un proceso/evidencia NAP identificado puede fundamentar `NAP_ACCEPTANCE`. |

### Evidencia española de uso NeTEx previamente inspeccionada

Los tres feeds CTB (LeioaBus, KBus y Bizkaibus) se mantienen como evidencia de uso real; no como inferencia de perfil:

```ini
PUBLIC_SPANISH_NETEX_USE = CONFIRMED
DECLARED_NETEX_VERSION = UNKNOWN
DECLARED_PROFILE = UNKNOWN
NAP_BYTE_IDENTITY = NOT_PROVEN
XSD_CONFORMANCE = NOT_TESTED
PROFILE_CONFORMANCE = NOT_TESTED
```

## D. Gaps y E. incertidumbres

1. Obtener acceso legítimo al texto íntegro controlado de CEN/TS 16614-4:2026 y registrar edición, anexos, tablas, referencias fechadas y licencia.
2. Resolver con fuente normativa el pasaje que aún especifica NeTEx 1.1 en la muestra pública de la edición 2026, frente a la información editorial de que la serie revisada se publica como NeTEx v2.
3. Fijar release/tag y commit exactos del schema 2.0.0, inventariar XSD importados/dependencias y hashes en un corpus autorizado. `v2.0` por sí sola es rama mutable.
4. Extraer por filas los requisitos EPIP para bus: objeto/clase, condición, cardinalidad, código de valores, regla de calidad, ancla textual y representación v2; registrar `UNKNOWN` cuando el texto no resuelva el mapeo.
5. Verificar si CEN publica artefactos asociados al texto completo bajo canal de miembro/secretaría (XSD, Schematron, conformance suite, model files o guidance). No se identificaron públicamente en esta revisión.
6. Mapear categorías del Anexo I del Reglamento (UE) 2017/1926 consolidado a los campos estáticos de red y horario de autobús del alcance aprobado; EPIP no determina por sí solo qué sujetos/servicios están jurídicamente obligados.
7. El contrato operativo NAP sigue `NOT_IDENTIFIED_IN_PUBLIC_SOURCES_REVIEWED`; el NAP no publica en la FAQ un criterio de XSD/perfil. No se ha iniciado contacto con terceros.

## F. Propuesta de out-of-scope V1

Proponer límites de producto técnico, sujetos a aprobación del usuario:

| Área | Propuesta | Motivo / tratamiento |
|---|---|---|
| Tarifas completas | Fuera; considerar únicamente zonas tarifarias básicas si el texto EPIP y scope regulatorio seleccionado las requieren | EPIP declara fares fuera de alcance salvo zonas básicas. No inferir conformidad tarifaria por tener XSD Parte 3. |
| Modos alternativos | Fuera | Parte 5/modelo existe en v2, pero no corresponde al caso bus regular. |
| Accesibilidad más allá de EPIP básico | Fuera EPIAP completo; evaluar la parte informativa básica prevista por EPIP dentro del scope | EPIAP es perfil aparte (Parte 6); el README v2 no lista una implementación XSD Parte 6. No excluir toda información básica accesible. |
| Tiempo real y SIRI | Fuera | Dominio/estándar y gate distintos; NeTEx estático podrá contener datos de referencia sin validar SIRI. |
| Complejidad ferroviaria | Fuera | No corresponde a bus regular y puede implicar estructuras modales especializadas. |
| Multimodalidad | Fuera del primer alcance, salvo referencias necesarias para el intercambio de un servicio de autobús | Mantener límite modal explícito; no afirmar compatibilidad multimodal de conjunto. |
| Perfiles/extensiones nacionales u operador | Fuera de las reglas generales hasta disponer de fuente, versión y autoridad publicadas | España/NAP no identificados públicamente; extensiones pueden quedar como `UNKNOWN`, no automáticamente inválidas. |
| Auditoría de feeds de operador, aceptación NAP, conversiones, remediación | Fuera | Requieren gates y tareas posteriores; expresamente no iniciar N03+. |

## G. Claims permitidos

- Se identificó CEN/TS 16614-4:2026 como edición EPIP y su ratificación española como UNE-CEN/TS.
- La edición normativa proporciona una baseline conocida para modelar requisitos del perfil una vez se tenga acceso al texto controlado.
- El repositorio NeTEx publica release 2.0.0 de schemas para las partes 1, 2, 3 y 5 y lo clasifica como versión de producción más reciente; la base representa candidatos de red y horario.
- `v2.0.0` puede proponerse como baseline de schema para el alcance V1 con limitaciones: versión exacta fijada, restricciones EPIP derivadas de fuente y gaps reportados separadamente.
- Los tres feeds CTB citados previamente demuestran uso público real de NeTEx, con versión/perfil declarados desconocidos y conformance no probada.
- Perfil adicional español y contrato técnico NAP: no identificados en fuentes públicas oficiales revisadas al corte.

## H. Claims prohibidos

- “NeTEx v2.0.0 está certificado/conforme con EPIP 2026” o “el XSD v2 implementa EPIP 2026 completo”.
- “La edición EPIP 2026 es plenamente compatible con v2” hasta cerrar el cotejo normativo, en particular la referencia 1.1 de la muestra.
- “No existe perfil español” o “NAP no valida XSD/perfil”; la búsqueda solo sustenta `NOT_IDENTIFIED` en fuentes públicas revisadas.
- “Feed NAP aceptado”, “feed español conforme” o versión/perfil conocida basándose en las muestras CTB.
- “Cumplimiento del Reglamento 2017/1926” a partir de validación sintáctica o de perfil; no se ha determinado applicability jurídica del operador ni completitud frente al Anexo.
- “Accesibilidad cubierta” sin distinguir atributos informativos EPIP de EPIAP completo.

## I–K. Recomendación y decisión humana requerida

**I. NeTEx v2.0.0:** aprobarlo como release de referencia de schema para el modelado V1 condicionado a fijar tag/commit/hash, comprobar el texto íntegro CEN y mantener requisitos de perfil no mapeados como gap. El principal beneficio es la base estable y contemporánea para las partes 1/2; la limitación central es la falta de una implementación EPIP 2026 pública y la tensión textual del fragmento normativo.

**J. EPIP 2026:** adoptarlo como perfil normativo europeo candidato para la deliberación del alcance de bus estático. No declararlo implementado ni usar el XSD EPIP 1.3.1 como evidencia de conformidad. El contenido del texto completo debe alimentar trazabilidad para cualquier futura regla.

**K. Decisión exacta requerida:** Yeison debe decidir si aprueba el scope propuesto (España, bus regular programado, información estática de pasajero), acepta NeTEx `v2.0.0` como baseline XSD condicionada y adopta CEN/TS 16614-4:2026 como baseline normativa EPIP con las limitaciones/gaps anteriores; también decidir si el alcance acepta solo accesibilidad informativa EPIP y difiere EPIAP completo, y si tarifas se limitan a zonas básicas. Hasta esa decisión, `N01` permanece abierto en `READY_FOR_HUMAN_SCOPE_DECISION`; no se inicia N03.

## Estado de cierre

```ini
N01_TECHNICAL_REVIEW = PASS
N01 = READY_FOR_HUMAN_SCOPE_DECISION
N01_SCOPE_DECISION = PENDING
PROFILE_SCHEMA_COMPATIBILITY = PARTIAL
NETEX_V2_0_0 = CANDIDATE_BASELINE_WITH_LIMITATIONS
EPIP_2026_FULL_IMPLEMENTATION = NOT_PUBLICLY_IDENTIFIED
SPANISH_PROFILE = NOT_IDENTIFIED_IN_PUBLIC_SOURCES_REVIEWED
NAP_ACCEPTANCE_CONTRACT = NOT_PUBLICLY_IDENTIFIED
N03_STARTED = NO
```

### Fuentes consultadas

- BOE-A-2026-10207, relación de normas ratificadas en abril de 2026: <https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-10207>.
- Ficha CEN/TS 16614-4:2026, organismo nacional belga NBN: <https://app.nbn.be/data/r/platform/frontend/detail?p40_id=3499334&p40_language_code=en>.
- Muestra pública SIST-TS CEN/TS 16614-4:2026, adoptada idéntica a CEN/TS 16614-4:2026; extracto, no texto completo: <https://cdn.standards.iteh.ai/samples/sist/sist-ts-cen-ts-16614-4-2026/34a3da8da59e48e4831474ed903bc6bf/sist-ts-cen-ts-16614-4-2026.pdf>.
- README del repositorio NeTEx v2: <https://github.com/TransmodelEcosystem/NeTEx/blob/v2.0/README.md>.
- Archive EPIP XSD legado: <https://github.com/TransmodelEcosystem/NeTEx-Profile-EPIP>.
- Reglamento Delegado (UE) 2017/1926 consolidado: <https://eur-lex.europa.eu/eli/reg_del/2017/1926/2024-03-04/eng>.
- NAPCORE MMTIS Quality Framework v1: <https://napcore.eu/wp-content/uploads/2025/06/NAPCORE-MMTIS-Quality-Framework_v1_250411.pdf>.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
