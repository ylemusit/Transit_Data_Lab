# NeTEx N01 — investigación inicial de scope y perfil

**Fecha de corte:** 2026-10-02
**Estado:** `IN_PROGRESS / SCOPE_NOT_DECIDED`
**Fase:** investigación documental. No se implementa parser, XSD, validador ni regla.

## Resultado ejecutivo

La evidencia disponible no basta para declarar un perfil español NeTEx ni un contrato de aceptación del NAP. La recomendación de trabajo es evaluar primero transporte público terrestre regular en autobús, con datos estáticos de red/paradas y servicios/horarios, y contrastar un perfil europeo de información de pasajeros con la evolución de NeTEx 2.0.0. Esta es una propuesta para decisión, no una selección aprobada ni una afirmación de obligación jurídica completa.

### Ronda final de autoridad (2026-10-02)

La consulta adicional de páginas públicas del MITRAMS/NAP, el texto consolidado de EUR-Lex, documentación de la Comisión/NAPCORE y la rama estable del repositorio de schemas no identificó una publicación española vigente y versionada de perfil, XSD, Schematron, guía de implementación o contrato técnico NAP específico para NeTEx. Esto es un resultado de búsqueda acotado, no prueba absoluta de inexistencia: el NAP invita a contactar y concretar pasos con proveedores, y puede haber material no publicado.

| Pregunta | Resultado de autoridad | Consecuencia para N01 |
|---|---|---|
| A. Perfil nacional español | `NATIONAL_IMPLEMENTATION_PROFILE_NOT_IDENTIFIED`; sí se identificó la ratificación española de normas CEN vigentes | El BOE de abril de 2026 publica UNE-CEN/TS 16614-1/-2/-4:2026 (entre otras). Esto adopta normas europeas en España; no es por sí mismo un perfil nacional de datos ni un contrato de aceptación NAP. La búsqueda negativa sigue limitada a perfiles/guías adicionales. |
| B. Aceptación NAP | Las páginas públicas describen formatos preferidos, URL/credenciales, actualización y calidad fiable; no especifican si la ingesta ejecuta XML well-formedness, XSD, perfil, reglas propias o revisión humana. | `NAP_PROFILE_REQUIREMENT = NOT_IDENTIFIED`; no atribuir aceptación de perfil ni `NAP_ACCEPTED`. La ruta oficial pública es contactar/registrarse como proveedor para acordar pasos, pero no se ha iniciado ese contacto. |
| C. Referencia UE | El Reglamento (UE) 2017/1926 consolidado exige que datos estáticos aplicables a NeTEx/DATEX II se representen mediante perfiles mínimos UE o nacionales. La referencia europea de información al pasajero para NeTEx es EPIP (CEN/TS 16614-4); EPIAP (Parte 6) es la extensión de accesibilidad. NAPCORE recomienda EPIP y/o EPIAP para interoperabilidad de horarios. | EPIP es el candidato de perfil europeo para el scope estático seleccionado; EPIAP es una extensión opcional/diferida salvo que se incorpore accesibilidad al scope. Aún se debe fijar texto/edición exactos y mapping de categorías regulatorias. |
| D. Compatibilidad 2.0.x | CEN/TS 16614-4:2026 está vigente y el catálogo del organismo nacional belga identifica su sustitución de la edición 2020; el resumen de la edición dice que la versión actualizada de TS 16614 se publicará como NeTEx v2. La rama XSD `v2.0` declara correspondencia con documentación CEN de febrero de 2026 para Partes 1/2/3/5, pero no incluye XSD Part 4/6. | Hay evidencia documental sólida de alineación de la **serie normativa** EPIP 2026 con NeTEx v2, y España ratificó UNE-CEN/TS 16614-4:2026. Sigue pendiente verificar restricciones y artefactos ejecutables EPIP exactos contra el release de schemas: `PROFILE_SCHEMA_ARTIFACT_COMPATIBILITY = NOT_PROVEN`. No usar EPIP XSD 1.3.1 como autoridad actual. |

**Conclusión de la ronda:** ya no procede ampliar la búsqueda mediante más feeds. Se puede registrar el perfil nacional específico y los criterios de aceptación como no identificados en la evidencia pública revisada. El fallback europeo queda identificado: EPIP CEN/TS 16614-4:2026 para información al pasajero; EPIAP CEN/TS 16614-6:2024 es una extensión específica de accesibilidad. La edición EPIP 2026 está alineada documentalmente con la serie NeTEx v2, pero resta fijar y cotejar el artefacto ejecutable/perfil completo. N01 sigue abierto para aprobar scope, baseline y categorías; la ronda resolvió la autoridad de perfil a nivel documental sin fingir conformance. No se ha validado ningún ZIP contra XSD ni perfil.

El Reglamento Delegado (UE) 2017/1926, modificado por el Reglamento Delegado (UE) 2024/490, remite a NeTEx CEN/TS 16614 y versiones posteriores para los modos pertinentes y establece que los datos a los que aplican NeTEx/DATEX II se representen mediante perfiles mínimos de la UE o perfiles nacionales. Esto no convierte cualquier submodelo de NeTEx ni cualquier fragmento XML en el perfil aplicable. La selección de categorías depende del anexo y del scope de producto.

El repositorio CEN de schemas publicado identifica `v2.0.0` (febrero de 2026) como versión más reciente de producción para las partes 1, 2, 3 y 5; recomienda citar versión mayor/menor como `2.0` para referencias y fijar un release de tres componentes al desarrollar. El artefacto EPIP heredado de Compliance es un XSD Data4PT de 2021 basado en 1.3.1; el repositorio fue archivado el 3 de mayo de 2026 y dice que el subgrupo NeTEx ya no mantiene el XSD. Por tanto, ese XSD sirve como antecedente reproducible acotado, no como autoridad suficiente para el nuevo baseline.

## Hallazgos que afectan N01

1. **Versión:** `2.0.0` es la candidata técnica actual para evaluar como baseline de producción; falta comprobar su correspondencia con las publicaciones normativas CEN y su compatibilidad con el perfil que se elija. No se adopta todavía.
2. **Perfil europeo:** EPIP/EPIAP y los perfiles mínimos UE necesitan identificación por alcance, edición y artefacto. EPIP es un perfil funcional/subconjunto; EPIAP aborda accesibilidad. El XSD EPIP histórico no está mantenido y es de 1.3.1. El diccionario NAPCORE apunta a ejemplos EPIP/EPIAP del repositorio NeTEx-CEN, útiles como guía, no sustitutos de especificación normativa.
3. **Perfil español / NAP:** BOE publica en 2026 la ratificación de UNE-CEN/TS 16614-1/-2/-4:2026; son adopciones españolas de normas CEN, no perfil nacional adicional. FAQ y alta de proveedores explican preferencia de formatos, publicación por URL/credenciales, actualización y calidad suficiente; los pasos se concretan tras el contacto. No publican perfil nacional específico ni contrato técnico que permita saber qué controles se ejecutan. Resultado: no identificado en fuentes públicas revisadas; no prueba de inexistencia.
4. **Regulación:** la regla de formato y perfil debe vincularse a las categorías de datos efectivamente aplicables del anexo consolidado de 2017/1926. El motor futuro podrá informar alineación respecto de requisitos modelados, pero no decidir alcance subjetivo, obligación del operador o cumplimiento jurídico integral.
5. **Modo:** comenzar por autobús regular terrestre es una recomendación práctica de reducción de alcance, apoyada por la presencia de datasets de autobús en el NAP; no es una decisión del NAP ni una conclusión sobre qué operadores están obligados.
6. **Integración con Compliance:** el cierre Compliance V1 ya demostró inspección segura y validación XSD de fixtures sintéticos para un fragmento `Line` con el EPIP heredado. Su evidencia limita la conclusión a ese fragmento, no prueba publicación NeTEx completa, un perfil español, importación de dataset real ni aceptación del NAP.

## Propuesta de decisión de scope

| Campo | Propuesta para deliberación | Estado / evidencia pendiente |
|---|---|---|
| `NETEX_V1_SCOPE` | Definir auditoría técnica estática de publicaciones NeTEx seleccionadas, con salidas separadas por tipo de evaluación | Abierto; no equivale a implementación |
| `NETEX_VERSION` | Evaluar NeTEx `2.0.0` como baseline de schemas/modelo | Propuesta; cotejar publicaciones CEN y perfil antes de fijar |
| `TARGET_PROFILE` | Perfil europeo mínimo de información de pasajeros compatible con la versión elegida; evaluar EPIP y EPIAP por separado | Abierto; el XSD EPIP 1.3.1 heredado no basta |
| `TARGET_MARKET` | España | Propuesto; requiere decidir si el producto cubre también interoperabilidad europea |
| `TARGET_MODE` | Autobús terrestre regular | Propuesta estrecha para V1; discrecional, demanda, ferrocarril, marítimo, aéreo y fluvial diferidos |
| `INITIAL_DATA_CATEGORIES` | Red/paradas y líneas/servicios/horarios estáticos aplicables al caso seleccionado | Propuesta; mapear con precisión al anexo regulatorio y perfil elegido |
| `NAP_CONTEXT` | Contexto informativo del NAP multimodal español; no afirmar aceptación | Falta perfil/contrato técnico oficial de ingesta y evaluación |
| `SCHEMA_AUTHORITY` | Publicación CEN aplicable; release oficial de schemas fijado por versión como artefacto de implementación trazable | Abierto hasta verificar publicación CEN ↔ release XSD |
| `PROFILE_AUTHORITY` | Texto CEN del perfil aplicable y, si existe, publicación/perfil nacional emitido por autoridad competente | Abierto; NAPCORE/EC sirven para localizar y clasificar, no para suplir autoridad normativa |
| `OUT_OF_SCOPE` | Datos dinámicos/realtime, conversión GTFS↔NeTEx, tarifas, modos distintos de bus regular, evaluación de feeds de operador, aprobación jurídica/comercial | Propuesta; validar al cerrar N01 |

## Separación obligatoria de resultados

| Resultado | Qué podría acreditar una futura evaluación | Qué no acredita por sí solo |
|---|---|---|
| `SCHEMA_VALIDITY` | El documento cumple el XSD exacto configurado | Perfil, NAP, regulación o calidad semántica |
| `PROFILE_CONFORMANCE` | Cumple las restricciones del perfil versionado que se modele y evalúe | Aceptación NAP o cumplimiento jurídico completo |
| `NAP_ACCEPTANCE` | Solo una respuesta/evidencia del NAP conforme a un procedimiento identificado | Conformidad general con NeTEx o validez jurídica universal |
| `REGULATORY_ALIGNMENT` | Cobertura técnica de requisitos normativos identificados y aplicables dentro de un alcance declarado | Opinión jurídica, determinación final de sujetos obligados o certificación |
| `DATA_QUALITY` | Hallazgos de calidad definidos mediante criterios separados y evidencia | Conformidad normativa si no está vinculada a esos requisitos |

## Decisiones abiertas para cerrar N01

- ¿Se adopta como objetivo de V1 el caso de datos estáticos de autobús regular, o se quiere otro modo/categoría?
- ¿El baseline técnico será NeTEx `2.0.0`, condicionado a compatibilidad demostrada del perfil, o se requiere una transición explícita compatible con artefactos EPIP 1.3.x?
- ¿Qué perfil exacto (documento, edición, release, dependencias y restricciones) se declara objetivo? ¿Se separa perfil europeo de accesibilidad EPIAP?
- ¿Existe un perfil mínimo nacional español publicado por MITRAMS/NAP y cuál es su autoridad/versionado?
- ¿Qué versión y publicación de CEN/TS 16614 cubre cada parte incluida, y qué documentos son accesibles/licenciados para verificarla?
- ¿Qué límites exactos de categorías del anexo UE se cubren y cuáles quedan diferidos?
- ¿Qué evidencia concreta autorizaría informar `NAP_ACCEPTANCE`? Hasta resolverlo, esa salida debe quedar fuera de las conclusiones del producto.
- ¿Qué artefacto de implementación/restricciones perfil EPIP 2026 se fija y cómo se verificará frente al release de schemas 2.0.x? La edición normativa de referencia ya está identificada como CEN/TS 16614-4:2026 (ratificada en España como UNE-CEN/TS).

## Gate propuesto de salida N01

N01 solo podrá marcarse `DEFINED` cuando cada valor de la matriz tenga una decisión aprobada, fuente autoritativa/versionada, evidencia de compatibilidad entre esquema y perfil, categorías dentro/fuera enumeradas y preguntas bloqueantes cerradas o aceptadas explícitamente como diferimientos. El registro de fuentes N02 no constituye por sí solo ese gate.

## Evidencia interna heredada

- `03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md`, apartado «NeTEx»: fija el origen y hash del XSD EPIP heredado, y limita el caso a `Line`, atributos y `Name`.
- `03_Compliance/reports/evidence/compliance_v1_20260928/netex_tree.json`: captura el árbol Git en commit `e5eaf83f15f7fd8db7991a4a8323b6ff7905c13a`.
- `03_Compliance/reports/evidence/compliance_v1_20260928/sources/`: copia congelada del XSD EPIP y dependencias usadas en el gate histórico. No se altera.
- `03_Compliance/NAP/`: capturas HTML locales de FAQ, políticas de contribución y licencia. Son antecedentes archivados; la verificación web de N01 se registra en N02.

## Fuentes externas consultadas

El inventario de autoridad, uso y límites está en [N02 — registro inicial de fuentes](N02_SOURCE_REGISTER_INITIAL_20261002.md), actualizado con esta ronda. Consulta web: 2026-10-02. Los sitios vivos pueden cambiar; fijar bytes, edición y hash de artefactos solo cuando N02 autorice una captura concreta.

Seguimiento posterior sobre perfil español y muestras públicas: [N01 follow-up — perfil y feeds públicos](N01_FOLLOWUP_ES_PROFILE_AND_PUBLIC_FEEDS_20261002.md). Aporta tres inspecciones estructurales con hashes, pero mantiene N01 abierto porque no establece versión/perfil ni payload exacto ingerido por el NAP.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Addendum — revisión de compatibilidad final (2026-10-02)

La revisión técnica documental terminó con `N01_TECHNICAL_REVIEW = PASS` y `N01 = READY_FOR_HUMAN_SCOPE_DECISION`. N01 sigue abierto: no se adoptó scope ni baseline. `v2.0.0` se propone con limitaciones; compatibilidad EPIP 2026 / NeTEx v2 se clasifica `PARTIAL`, con implementación EPIP 2026 no identificada públicamente. La muestra de la edición EPIP 2026 mantiene una referencia a NeTEx 1.1; debe resolverse con el texto controlado antes de afirmar compatibilidad completa. La matriz, artefactos, gaps, claims permitidos/prohibidos y decisión exacta están en [revisión final de compatibilidad](N01_FINAL_PROFILE_SCHEMA_COMPATIBILITY_REVIEW_20261002.md). No se inició N03.
