# Investigación externa dirigida — S1-EXIT-09

Fecha de consulta: 2026-09-27, Europe/Madrid. Autorización: petición expresa «AUTORIZADO — BUSINESS PHASE 3 STAGE 1 — TARGETED EVIDENCE RESEARCH FOR S1-EXIT-09». Alcance: únicamente resolver el tercer POTENTIAL GAP externo. Sin entrevistas/contactos, análisis de demanda, Stage 2, cambios técnicos, modificación de V1 o commit.

## Resultado

S1-EXIT-09 = PASS. GAP-CANDIDATE-005 = SUPPORTED; confianza MEDIUM. Tres POTENTIAL GAPS respaldados para el criterio: GAP-001, GAP-002 (evaluaciones previas conservadas) y GAP-005 (este trabajo). No se cuentan GAP-003 ni GAP-004. No se buscó un cuarto gap.

## GAP-CANDIDATE-005 — exactitud de oferta programada frente a operación observada

**NEED:** agencias y reutilizadores pueden necesitar medir la diferencia entre el servicio público programado y lo efectivamente observado, tanto en ubicación (Schedule frente a posiciones vehiculares) como en exactitud temporal de predicciones RT.

**EVIDENCE:** MKT-EVD-037. El resumen institucional del Mineta Transportation Institute (2024) presenta métodos y métricas para la exactitud temporal GTFS-RT y espacial GTFS Schedule mediante comparación con patrones reales de vehículos; declara que la divergencia entre servicio planeado y prestado produce métricas escalables desde parada hasta sistema. Esto documenta el problema/método y utilidad analítica posible, no incidencia general ni prevalencia española.

**EXISTING ALTERNATIVE:** MobilityData Canonical GTFS Schedule Validator (MKT-EVD-039) y los informes mensuales de calidad Cal-ITP/Caltrans (MKT-EVD-038). Son alternativas concretas documentadas; Cal-ITP explica que publica resúmenes de operaciones representadas, operaciones codificadas incorrectamente, avisos del validador, mejores prácticas y guías para proveedores.

**SCOPE/LIMIT:** La documentación del validador describe pruebas frente a GTFS Schedule Reference y Best Practices. El dashboard Cal-ITP describe informes generados con ese validador y los contenidos antes citados. En el alcance publicado consultado no figura la comparación de horario/recorrido GTFS con trayectorias GPS/RT observadas para producir métricas espaciales/temporales de exactitud. Esta es una frontera de la documentación publicada, no prueba de incapacidad absoluta de dichos actores ni de todo proveedor.

**UNRESOLVED NEED:** el estudio institucional establece que esta comparación de exactitud es medible y relevante para conocer calidad/impacto en usuarios; las alternativas revisadas publican conformidad, recomendaciones e informes de feed, sin describir esa medición concreta contra operación observada. Es razonable clasificarlo como necesidad potencial parcialmente no cubierta en el alcance documentado. No se afirma que no existan otras soluciones, que toda agencia la necesite, que el caso sea frecuente, ni que haya comprador o disposición a pagar.

**INDEPENDENT FROM TDL:** YES. La necesidad y método proceden del estudio institucional; las alternativas y sus límites se describen en sus propias fuentes. Ninguna capacidad TDL se usa como evidencia de mercado. V1 no acredita exactitud contra operación observada; GAP-005 no presupone que TDL pueda resolverla.

**RESULT:** SUPPORTED (como POTENTIAL GAP, no oportunidad). **CONFIDENCE:** MEDIUM. Una fuente institucional de investigación más documentación primaria de las alternativas sostienen un caso específico y falsable. La investigación no prueba extensión de mercado, aplicabilidad en España, ausencia universal de oferta o compra.

**Relación eventual con TDL:** relación conceptual con TDL-CAP-003, CAP-004 y CAP-019 para inspección/comparación, pero la baseline no acredita datos GPS/RT, comparación con servicio real ni métricas de exactitud. Sin encaje/roadmap/producto inferidos.

## Fuentes nuevas aceptadas

| ID | Fuente y localizador | Qué demuestra | Qué NO demuestra |
| --- | --- | --- | --- |
| MKT-EVD-037 | Mineta Transportation Institute, Assessing GTFS Accuracy, 08/2024; resumen institucional, Description; DOI 10.31979/mti.2024.2017. https://scholarworks.sjsu.edu/mti_publications/506/ | Métodos para métricas temporales de GTFS-RT y espaciales GTFS Schedule contrastando información con patrones reales de vehículos; divergencia entre servicio planificado y prestado como objeto medible. | Prevalencia, tasas, error español, incidencia comercial, compradores, gasto o estado de todos los feeds. |
| MKT-EVD-038 | Cal-ITP/Caltrans, California GTFS Quality Dashboard; About GTFS data / How to use reports. https://reports.dds.dot.ca.gov/ | Alternativa pública ejecuta mensualmente una instancia del validador en feeds californianos y publica resúmenes de operaciones representadas/miscodificadas, reglas, recomendaciones y archivo de reportes. | Comparación GPS/RT realizada o inexistente fuera de lo descrito en esa documentación; alcance más allá de California. |
| MKT-EVD-039 | MobilityData, Canonical GTFS Schedule Validator, Validation Rules and Metadata. https://gtfs-validator.mobilitydata.org/rules.html | El validador declara pruebas contra referencia GTFS Schedule y mejores prácticas y documenta avisos por severidad. | Exactitud real, operación efectiva, cobertura legal completa, incapacidad frente a datos de campo, benchmark o evaluación de todo proveedor. |

## Fuentes examinadas y no aceptadas como soporte de gap

- Documentación PAN Francia sobre indicadores de disponibilidad, conformidad y frescura, con seguimiento horario/diario e historial: confirma que existe monitorización útil; no sirve para afirmar que monitorización continua esté sin resolver, por lo que se descarta esa formulación amplia.
- Ficha individual NAP española (dataset Autobús interurbano de Navarra, registro web ID 963) muestra errores/avisos de validador y «Quality information is unknown», junto con metadato de actualización. Es una observación puntual dinámica. No acredita qué criterios eran aplicables, falsedad operacional, demanda ni una carencia en todo NAP; no se usa como premisa del GAP-005.
- La documentación MobilityData/Cal-ITP sí incluye checks semánticos internos de feed y algunas referencias a operaciones. Por ello se rechaza cualquier afirmación general de que solo hacen validación sintáctica. GAP-005 se limita a comparación explícita con movimientos reales como frontera no descrita en las páginas consultadas.
- Página de validación PAN Francia y material de publicación de RT: confirma herramientas y recomendación de calidad/frescura, pero no aporta una necesidad distinta mejor delimitada; se trata como contraste contra la hipótesis amplia, no como evidencia aceptada del gap nuevo.
- GAP-004: no se refuerza. Expedientes existentes acreditan integración y requisitos multiformato, pero no el residual específico frente a proveedores establecidos.
- GAP-003: no se cuenta. La incompletitud de mapping/corpus/engine pertenece principalmente a TDL.

## Búsqueda y límites

Consultas web realizadas: búsqueda dirigida de GTFS Schedule/RT accuracy y real-world validation; consulta de informe institucional sobre GTFS accuracy; búsqueda y apertura de documentación MobilityData; apertura de California GTFS Quality Dashboard, reglas del validador, documentación de indicadores PAN Francia, procedimiento oficial francés de publicación RT y ficha NAP España. Se usaron fuentes institucionales, organismos y documentación primaria. La descarga del PDF de investigación desde la página institucional respondió 403; se consultó su resumen institucional, que resume alcance, método y conclusión, sin copia íntegra. La ficha de MKT-EVD-037 declara esa limitación.

Fuentes consultadas adicionales, no usadas para sostener el candidato: estudio Calgary de limpieza GTFS (PMC, página con desafío anti-bot al abrir); página actual de validación PAN Francia; documentación de indicadores PAN Francia; ficha NAP ID 963. No se usaron blogs SEO, agregadores ni opiniones.

## Reevaluación y estado de gobierno

Solo se reevalúa S1-EXIT-09; los otros 14 PASS no se reabren. Conteo: 15 PASS / 0 FAIL / 0 INSUFFICIENT_EVIDENCE / 0 NOT_APPLICABLE. STAGE_1_EXECUTION = COMPLETE. GATE_READINESS = READY_FOR_HUMAN_GATE. STAGE_1_GATE = PENDING_HUMAN_DECISION. HUMAN GATE no aprobado por esta evaluación. BUSINESS PHASE 3 permanece IN_PROGRESS. BUSINESS_CAPABILITY_BASELINE_V1 permanece FROZEN. Stage 2 permanece NOT AUTHORIZED.

Escrituras dentro de 07_Business únicamente. Producto técnico no modificado. Sin commit. Verificación aplicada: revisión textual de referencias/IDs y comprobación posterior de Git limitada a 07_Business, baseline V1 y 06_Products; no se ejecutan validadores históricos ni hash global.
