# Gate 2 - universo atómico final propuesto

FINAL_ATOMIC_UNIVERSE = 48

45 - 2 padres sustituidos + 5 hijos = 48. Los padres G2-032 y G2-037 son SUPERSEDED_BY_SPLIT y no podrán materializarse.

El CSV es la propuesta completa; los campos adicionales preservan alcance, excepciones, texto fuente y trazabilidad. Celda vacía en deadline_date representa NULL. source_fact_id de G2-045 permanece vacío; proposed_source_fact_id no es un identificador persistido. Elegibilidad preparatoria, sin autorización de escritura.

### G2-001

Cada Estado miembro debe establecer un punto de acceso nacional.

- Propuesta: `EU-2017-1926-PROP-A03-P01-001`
- Fuente: Artículo 3, apartado 1; `EU-2017-1926-ART03`; fact `EU-2017-1926-SF-A03-P01-ESTABLISH`
- Actor: Estado miembro
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: ALREADY_MATERIALIZED_MATCH
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-002

El punto de acceso nacional debe servir como punto único de acceso a las categorías de datos y actualizaciones enumeradas para el territorio del Estado miembro.

- Propuesta: `EU-2017-1926-PROP-A03-P01-002`
- Fuente: Artículo 3, apartado 1; `EU-2017-1926-ART03`; fact `EU-2017-1926-SF-A03-P01-SINGLE`
- Actor: Estado miembro
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: ALREADY_MATERIALIZED_MATCH
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-003

El punto de acceso nacional debe prestar servicios de localización a los usuarios de datos.

- Propuesta: `EU-2017-1926-PROP-A03-P03-001`
- Fuente: Artículo 3, apartado 3; `EU-2017-1926-ART03`; fact `EU-2017-1926-SF-A03-P03`
- Actor: Punto de acceso nacional
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-004

El Estado miembro, en cooperación con las partes interesadas pertinentes de los STI, alcanzará un acuerdo sobre los requisitos en materia de metadatos.

- Propuesta: `A03-P04-001-01`
- Fuente: Artículo 3, apartado 4; `EU-2017-1926-ART03`; fact `EU-2017-1926-SF-A03-P04`
- Actor: Estado miembro
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-005

El titular de datos facilitará metadatos sobre la base de los requisitos acordados.

- Propuesta: `A03-P04-001-02`
- Fuente: Artículo 3, apartado 4; `EU-2017-1926-ART03`; fact `EU-2017-1926-SF-A03-P04`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-006

Los titulares facilitarán por el punto de acceso nacional acceso a los datos estáticos, históricos y observados incluidos en el punto 1 del anexo.

- Propuesta: `EU-2017-1926-PROP-A04-P01-001`
- Fuente: Artículo 4, apartado 1; `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P01`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-007

Facilitar los datos de carretera mediante el formato normalizado al que remite el artículo 4.

- Propuesta: `EU-2017-1926-PROP-A04-P01-002`
- Fuente: Artículo 4, apartado 1, letra a); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P01-ROAD`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Reglamento Delegado (UE) 2015/962; formato normalizado / formatos indicados en artículos 4-6
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-008

Para otros modos, utilizar una norma/especificación enumerada o un formato digital legible por máquina que pueda demostrarse plenamente compatible e interoperable con ellas.

- Propuesta: `EU-2017-1926-PROP-A04-P01-003`
- Fuente: Artículo 4, apartado 1, letra b); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P01-OTHER`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Reglamento (UE) n.º 454/2011; especificaciones técnicas establecidas en el Reglamento
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-009

Para la red espacial, aplicar los requisitos a los que remite el artículo 7 de la Directiva 2007/2/CE.

- Propuesta: `EU-2017-1926-PROP-A04-P01-004`
- Fuente: Artículo 4, apartado 1, letra c); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P01-SPATIAL`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Directiva 2007/2/CE; requisitos establecidos en el artículo 7 de la Directiva 2007/2/CE
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-010

Los datos estáticos, históricos y observados del anexo a los que sean aplicables NeTEx y DATEX II se representarán mediante perfiles mínimos de la UE o nacionales.

- Propuesta: `EU-2017-1926-PROP-A04-P02-001`
- Fuente: Artículo 4, apartado 2; `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P02`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Los datos estáticos, históricos y observados enumerados en el punto 1 del anexo a los que sean aplicables NeTEx y DATEX II.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-011

Para la red RTE-T global, facilitar los datos del punto 1.1 del anexo, salvo el punto 1.1, letra d), inciso ix), a más tardar el 1 de diciembre de 2019.

- Propuesta: `EU-2017-1926-PROP-A04-P03-001`
- Fuente: Artículo 4, apartado 3, letra a); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-A`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: En relación con los datos del punto 1.1 del anexo para la red RTE-T global, con excepción del punto 1.1, letra d), inciso ix).
- Temporal: EXPLICIT_DATE; 2019-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-012

Para la red RTE-T global, facilitar los datos del punto 1.2 del anexo, salvo los incisos expresamente exceptuados en el artículo 4, apartado 3, letra b), a más tardar el 1 de diciembre de 2020.

- Propuesta: `EU-2017-1926-PROP-A04-P03-002`
- Fuente: Artículo 4, apartado 3, letra b); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-B`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: En relación con los datos del punto 1.2 del anexo para la red RTE-T global, con excepción de los puntos 1.2, letra a), incisos i) y iii), y 1.2, letra c), inciso ii).
- Temporal: EXPLICIT_DATE; 2020-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-013

Para la red RTE-T global, facilitar los datos del punto 1.3 del anexo, salvo el punto 1.3, letra c), inciso iii), a más tardar el 1 de diciembre de 2021.

- Propuesta: `EU-2017-1926-PROP-A04-P03-003`
- Fuente: Artículo 4, apartado 3, letra c); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-C`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: En relación con los datos del punto 1.3 del anexo para la red RTE-T global, con excepción del punto 1.3, letra c), inciso iii).
- Temporal: EXPLICIT_DATE; 2021-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-014

Para las demás partes de la red de transporte de la Unión, facilitar los datos de los puntos 1.1 a 1.3 del anexo dentro del alcance y excepciones expresos de la letra d), a más tardar el 1 de diciembre de 2023.

- Propuesta: `EU-2017-1926-PROP-A04-P03-004`
- Fuente: Artículo 4, apartado 3, letra d); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-D`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: En relación con los datos de los puntos 1.1, 1.2 y 1.3 del anexo, con las excepciones y el transporte a la demanda enumerados en el artículo 4, apartado 3, letra d), para las demás partes de la red de transporte de la Unión.
- Temporal: EXPLICIT_DATE; 2023-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-015

Para toda la red de transporte de la Unión, facilitar las categorías de los puntos 1.1, 1.2 y 1.3 expresamente enumeradas en la letra e), a más tardar el 1 de diciembre de 2024.

- Propuesta: `EU-2017-1926-PROP-A04-P03-005`
- Fuente: Artículo 4, apartado 3, letra e); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-E`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: En relación con las categorías y excepciones enumeradas en el artículo 4, apartado 3, letra e), para toda la red de transporte de la Unión.
- Temporal: EXPLICIT_DATE; 2024-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-016

Facilitar el punto 1.4 del anexo en toda la red de la Unión a más tardar el 1 de diciembre de 2025.

- Propuesta: `EU-2017-1926-PROP-A04-P03-006`
- Fuente: Artículo 4, apartado 3, letra f); `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P03-F`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: EXPLICIT_DATE; 2025-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-017

Las API que proporcionen acceso a los datos estáticos, históricos y observados del anexo a través del punto de acceso nacional serán públicamente accesibles para los usuarios de datos; cuando proceda, estos estarán previamente registrados.

- Propuesta: `EU-2017-1926-PROP-A04-P04-001`
- Fuente: Artículo 4, apartado 4; `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P04`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando proceda, los usuarios de datos estarán previamente registrados.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-018

Usuarios y titulares colaborarán para notificar sin demora las inexactitudes al titular de origen.

- Propuesta: `EU-2017-1926-PROP-A04-P05-001`
- Fuente: Artículo 4, apartado 5; `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P05`
- Actor: Usuarios de datos y titulares de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: FUNCTIONAL_TIME_REQUIREMENT; sin demora
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-019

Los datos facilitados por titulares a través del punto de acceso nacional no incluirán datos personales conforme a la definición remitida.

- Propuesta: `EU-2017-1926-PROP-A04-P06-001`
- Fuente: Artículo 4, apartado 6; `EU-2017-1926-ART04`; fact `EU-2017-1926-SF-A04-P06`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Reglamento (UE) 2016/679; datos personales, tal como se definen en el artículo 4, apartado 1
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-020

Los titulares proporcionarán por el punto de acceso nacional acceso a los datos dinámicos de los puntos 2.1 y 2.2 del anexo.

- Propuesta: `EU-2017-1926-PROP-A05-P01-001`
- Fuente: Artículo 5, apartado 1; `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P01`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-021

Facilitar datos dinámicos de carretera mediante los formatos a los que remiten los artículos 5 y 6.

- Propuesta: `EU-2017-1926-PROP-A05-P01-002`
- Fuente: Artículo 5, apartado 1, letra a); `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P01-ROAD`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Reglamento Delegado (UE) 2015/962; formato normalizado / formatos indicados en artículos 4-6
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-022

Para otros modos, utilizar una norma/especificación enumerada o un formato digital legible por máquina que pueda demostrarse plenamente compatible e interoperable.

- Propuesta: `EU-2017-1926-PROP-A05-P01-003`
- Fuente: Artículo 5, apartado 1, letra b); `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P01-OTHER`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: PARTIAL; Reglamento (UE) n.º 454/2011; especificaciones técnicas establecidas en el Reglamento
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-023

Los datos dinámicos de los puntos 2.1 y 2.2 del anexo a los que sean aplicables SIRI y DATEX II se representarán mediante perfiles mínimos de la UE o nacionales.

- Propuesta: `EU-2017-1926-PROP-A05-P02-001`
- Fuente: Artículo 5, apartado 2; `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P02`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Los datos dinámicos de los puntos 2.1 y 2.2 del anexo a los que sean aplicables SIRI y DATEX II.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-024

Facilitar los datos del punto 2.1 del anexo para la red RTE-T global a más tardar el 1 de diciembre de 2025.

- Propuesta: `EU-2017-1926-PROP-A05-P03-001`
- Fuente: Artículo 5, apartado 3, letra a); `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P03-A`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: EXPLICIT_DATE; 2025-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-025

Facilitar los datos del punto 2.2 del anexo para la red RTE-T global a más tardar el 1 de diciembre de 2026.

- Propuesta: `EU-2017-1926-PROP-A05-P03-002`
- Fuente: Artículo 5, apartado 3, letra b); `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P03-B`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: EXPLICIT_DATE; 2026-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-026

Facilitar datos de los puntos 2.1 y 2.2 para las demás partes de la red de la Unión a más tardar el 1 de diciembre de 2028.

- Propuesta: `EU-2017-1926-PROP-A05-P03-003`
- Fuente: Artículo 5, apartado 3, letra c); `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P03-C`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: EXPLICIT_DATE; 2028-12-01
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-027

Si el Estado miembro decide que los titulares faciliten por el punto de acceso nacional los datos dinámicos del punto 2.3 del anexo, los titulares utilizarán SIRI o un formato digital legible por máquina demostrablemente plenamente compatible e interoperable.

- Propuesta: `EU-2017-1926-PROP-A05-P04-001`
- Fuente: Artículo 5, apartado 4; `EU-2017-1926-ART05`; fact `EU-2017-1926-SF-A05-P04`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: El Estado miembro ha decidido que los titulares faciliten, a través del punto de acceso nacional, los datos dinámicos enumerados en el punto 2.3 del anexo.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-028

Cuando se produzcan cambios en los datos del artículo 6, apartado 1, el titular actualizará los datos pertinentes enumerados en el anexo y los hará accesibles a través del punto de acceso nacional en un plazo que permita su utilización fiable y efectiva, de conformidad con el artículo 8.

- Propuesta: `A06-P02-001-01`
- Fuente: Artículo 6, apartado 2; `EU-2017-1926-ART06`; fact `EU-2017-1926-SF-A06-P02`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando se produzcan cambios en los datos a que se refiere el artículo 6, apartado 1.
- Temporal: FUNCTIONAL_TIME_REQUIREMENT; en un plazo que permita su utilización fiable y efectiva
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-029

Cuando los cambios se conozcan con antelación, el titular facilitará dichas actualizaciones a los usuarios de datos con antelación.

- Propuesta: `A06-P02-001-02`
- Fuente: Artículo 6, apartado 2; `EU-2017-1926-ART06`; fact `EU-2017-1926-SF-A06-P02`
- Actor: Titular de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando los cambios se conozcan con antelación.
- Temporal: FUNCTIONAL_TIME_REQUIREMENT; con antelación
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-030

El titular corregirá oportunamente cualquier inexactitud que detecte o que le indiquen los usuarios de datos y los usuarios finales.

- Propuesta: `A06-P02-001-03`
- Fuente: Artículo 6, apartado 2; `EU-2017-1926-ART06`; fact `EU-2017-1926-SF-A06-P02`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: FUNCTIONAL_TIME_REQUIREMENT; oportunamente
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-031

A solicitud, los proveedores comunicarán a otro proveedor resultados de encaminamiento basados en los datos enumerados.

- Propuesta: `EU-2017-1926-PROP-A07-P01-001`
- Fuente: Artículo 7, apartado 1; `EU-2017-1926-ART07`; fact `EU-2017-1926-SF-A07-P01`
- Actor: Proveedor de servicios de información sobre desplazamientos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Previa solicitud de otro proveedor de servicios de información sobre desplazamientos.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-032-A

Los datos de desplazamientos y tráfico enumerados en el anexo y los metadatos correspondientes, incluida la información sobre su calidad, serán accesibles para su intercambio y reutilización dentro de la Unión de forma no discriminatoria, a través del punto de acceso nacional establecido de conformidad con el artículo 3.

- Propuesta: `A08-P01-001-01-A`
- Fuente: Artículo 8, apartado 1; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P01`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-032-B

Los datos de desplazamientos y tráfico enumerados en el anexo y los metadatos correspondientes, incluida la información sobre su calidad, serán accesibles en un plazo que permita la reutilización fiable y efectiva de los datos.

- Propuesta: `A08-P01-001-01-B`
- Fuente: Artículo 8, apartado 1; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P01`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: FUNCTIONAL_TIME_REQUIREMENT; en un plazo que permita la reutilización fiable y efectiva
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-033

Los datos serán exactos y actualizados.

- Propuesta: `A08-P01-001-02`
- Fuente: Artículo 8, apartado 1; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P01`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-034

Los datos se basarán en requisitos mínimos de calidad.

- Propuesta: `A08-P01-001-03`
- Fuente: Artículo 8, apartado 1; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P01`
- Actor: Titular de datos
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-035

El Estado miembro, en cooperación con las partes interesadas pertinentes de los STI, alcanzará un acuerdo sobre los requisitos mínimos de calidad de los datos.

- Propuesta: `A08-P01-001-04`
- Fuente: Artículo 8, apartado 1; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P01`
- Actor: Estado miembro
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-036

Los datos del artículo 8, apartado 1, se reutilizarán de manera neutral, sin discriminación o parcialidad con respecto al titular de los datos.

- Propuesta: `A08-P02-001-01`
- Fuente: Artículo 8, apartado 2; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P02`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-037-A

Los criterios utilizados para ordenar las opciones de desplazamiento de los diferentes modos de transporte, o combinaciones de estos, o ambas cosas, deberán ser transparentes.

- Propuesta: `A08-P02-001-02-A`
- Fuente: Artículo 8, apartado 2; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P02`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-037-B

Los criterios utilizados para ordenar las opciones de desplazamiento de los diferentes modos de transporte, o combinaciones de estos, o ambas cosas, no estarán basados en ningún factor directa o indirectamente relacionado con la identidad del usuario de datos o del usuario final o, si la hubiera, la consideración comercial relacionada con la reutilización de los datos.

- Propuesta: `A08-P02-001-02-B`
- Fuente: Artículo 8, apartado 2; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P02`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-037-C

Los criterios utilizados para ordenar las opciones de desplazamiento de los diferentes modos de transporte, o combinaciones de estos, o ambas cosas, deberán aplicarse de forma no discriminatoria a todos los usuarios de datos o usuarios finales participantes.

- Propuesta: `A08-P02-001-02-C`
- Fuente: Artículo 8, apartado 2; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P02`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-038

La primera presentación de itinerario de viaje no inducirá a error al usuario final.

- Propuesta: `A08-P02-001-03`
- Fuente: Artículo 8, apartado 2; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P02`
- Actor: UNSPECIFIED_IN_PROVISION
- Modalidad: MANDATORY_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-039

Cuando se reutilicen los datos de desplazamientos y tráfico, se indicará su fuente si el titular de datos así lo solicita.

- Propuesta: `A08-P03-001-01`
- Fuente: Artículo 8, apartado 3; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P03`
- Actor: Usuario de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando se reutilicen los datos y el titular de datos solicite la indicación de la fuente.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-040

Cuando se reutilicen los datos, se indicará su intervalo de actualización; para los datos dinámicos, solo cuando sea posible.

- Propuesta: `A08-P03-001-02`
- Fuente: Artículo 8, apartado 3; `EU-2017-1926-ART08`; fact `EU-2017-1926-SF-A08-P03`
- Actor: Usuario de datos
- Modalidad: CONDITIONAL_MANDATORY_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando se reutilicen los datos; la indicación del intervalo para datos dinámicos se exige cuando sea posible.
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-041

Los Estados miembros evaluarán el cumplimiento por titulares y proveedores de los requisitos de los artículos 3 a 8.

- Propuesta: `EU-2017-1926-PROP-A09-P01-001`
- Fuente: Artículo 9, apartado 1; `EU-2017-1926-ART09`; fact `EU-2017-1926-SF-A09-P01`
- Actor: Estado miembro
- Modalidad: ASSESSMENT_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-042

Los Estados miembros deben remitir a la Comisión un informe sobre medidas para establecer el punto de acceso nacional y sus modalidades de funcionamiento, a más tardar el 1 de diciembre de 2019.

- Propuesta: `EU-2017-1926-PROP-A10-P01-001`
- Fuente: Artículo 10, apartado 1; `EU-2017-1926-ART10`; fact `EU-2017-1926-SF-A10-P01`
- Actor: Estado miembro
- Modalidad: REPORTING_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: EXPLICIT_DATE; 2019-12-01
- Dependencia: NONE; ; 
- Estado DB: ALREADY_MATERIALIZED_MATCH
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-043

Los Estados miembros proporcionarán en los informes de progreso información sobre avances, cobertura/calidad, conexiones, resultados de evaluación y cambios del NAP cuando proceda.

- Propuesta: `EU-2017-1926-PROP-A10-P02-001`
- Fuente: Artículo 10, apartado 2; `EU-2017-1926-ART10`; fact `EU-2017-1926-SF-A10-P02`
- Actor: Estado miembro
- Modalidad: REPORTING_DUTY; obligatorio=TRUE; condicional=TRUE
- Condición: Cuando proceda, se incluirá una descripción de los cambios en el punto de acceso nacional.
- Temporal: EXTERNAL_SCHEDULE_REFERENCE; Dentro de los informes sobre los progresos realizados a que se refiere el artículo 17, apartado 3, de la Directiva 2010/40/UE. No determinar periodicidad aquí.
- Dependencia: PARTIAL; Directiva 2010/40/UE; Directiva 2010/40/UE; informes sobre los progresos realizados a que se refiere el artículo 17, apartado 3; Artículo 17, apartado 3 (periodicidad no interpretada)
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_WITH_EXTERNAL_DEPENDENCY
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-044

A fin de llevar a cabo la evaluación del artículo 9(1), las autoridades competentes de los Estados miembros podrán solicitar a titulares de datos y proveedores de servicios de información sobre desplazamientos: a) descripción de los datos accesibles a través del NAP, información sobre su calidad y condiciones de reutilización; b) descripción de los servicios de información sobre desplazamientos disponibles y, cuando proceda, sus conexiones con otros servicios; c) declaración y justificantes correspondientes del cumplimiento de los artículos 3 a 8; d) licencia o acuerdos contractuales con proveedores de servicios de información sobre desplazamientos.

- Propuesta: `EU-2017-1926-PROP-A09-P02-DOCUMENT_REQUEST`
- Fuente: Artículo 9, apartado 2; `EU-2017-1926-ART09`; fact `EU-2017-1926-SF-A09-P02`
- Actor: Autoridades competentes de los Estados miembros
- Modalidad: PROCEDURAL_POWER; obligatorio=FALSE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: APPROVED_PENDING_MATERIALIZATION
- Elegibilidad preparatoria: TRUE; bloqueo: Ninguno

### G2-045

Los Estados miembros efectuarán comprobaciones aleatorias de la exactitud de las declaraciones mencionadas en el artículo 9, apartado 2, letra c).

- Propuesta: `EU-2017-1926-PROP-A09-P03-RANDOM_CHECKS`
- Fuente: Artículo 9, apartado 3; `EU-2017-1926-ART09`; fact `NOT_PERSISTED`
- Actor: Estados miembros
- Modalidad: VERIFICATION_DUTY; obligatorio=TRUE; condicional=FALSE
- Condición: No aplicable
- Temporal: NONE; Sin expresión
- Dependencia: NONE; ; 
- Estado DB: NOT_MATERIALIZED
- Estado humano: READY_PENDING_SOURCE_FACT_PERSISTENCE
- Elegibilidad preparatoria: FALSE; bloqueo: SOURCE_FACT_NOT_PERSISTED

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
