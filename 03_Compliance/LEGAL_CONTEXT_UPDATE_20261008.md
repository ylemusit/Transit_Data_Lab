# Actualización de contexto jurídico — 08/10/2026

Estado: CLOSED_WITH_EVIDENCE_LIMITS para esta actualización documental y editorial; capturas y generación corregida completadas. Cobertura jurídica completa NO DEMOSTRADA. Complementa Compliance V1, sin modificar su DB, corpus, fuentes, mappings, decisiones ni evaluador congelados.

## Fuentes y vigencia

El [registro complementario](reports/legal_update_20261008/source_registry.json) contiene 17 fuentes complementarias, seis capturas consolidadas adicionales y diez referencias con hashes verificados al corpus congelado: 33 capturas verificables. Todas incluyen URL y SHA-256. Las capturas xml.php de BOE son originales con análisis documental; las consolidaciones españolas se obtienen de la API oficial con Accept: application/xml. Se selecciona la última versión de cada bloque a la fecha de revisión; no se confunde original con consolidación. Las consolidaciones son herramientas informativas; una conclusión jurídica debe enlazar también las publicaciones oficiales y modificaciones pertinentes.

RD 450/2026: vigente desde 06/06/2026; incorpora la Directiva (UE) 2023/2661 y deroga RD 662/2012. Este último solo puede utilizarse como antecedente histórico para hechos posteriores a la derogación. La FAQ NAP conserva una referencia antigua: su captura no prueba vigencia normativa.

RGPD, INSPIRE, Directiva 2019/1024 y Ley 18/2015 están capturados y revisados en el alcance contextual de publicación. Se conservan las correcciones RGPD de 2018/2021, la corrección INSPIRE de 2018 y las modificaciones 2019/1010 y 2024/2829. Se añade Ley 14/2010 como transposición parcial de INSPIRE y RDL 24/2021, libro tercero, como transposición de datos abiertos y modificación de Ley 37/2007. También se capturan política, licencia y FAQ NAP vigentes en la fecha. No se presupone que todos los datos privados del operador sean información del sector público. La revisión es contextual y no un dictamen exhaustivo de todas las normas relacionadas.

El corpus previo ya identifica Directiva 2010/40/UE consolidada, Directiva 2023/2661, Reglamento 2017/1926 consolidado de 04/03/2024, Reglamento 2024/490, Ley 9/2025 y políticas/licencia/FAQ NAP. Las referencias RGPD e INSPIRE del seed no constituyen validadores completos. Los artefactos técnicos GTFS y NeTEx fijados por V1 conservan su identidad y alcance.

## Contrato de autoridad y trazabilidad

Cada futura evaluación debe conservar, sin inferir valores por defecto:

| Campo | Contenido necesario |
|---|---|
| source_id / source_version / source_hash | Identidad, redacción temporal y captura exacta; REFERENCE_ONLY si falta captura. |
| authority_type | EU_REGULATION, EU_DIRECTIVE, NATIONAL_LEGISLATION, NAP_PROVIDER_CONTRACT, NAP_LICENCE, ADMINISTRATIVE_GUIDANCE, TECHNICAL_SPECIFICATION, TECHNICAL_STANDARD_REFERENCED_BY_LAW o TDL_RECOMMENDATION. |
| provision / requirement | Precepto y obligación concreta; una relación temática no es un mapping aprobado. |
| applicability | APPLICABLE, NOT_APPLICABLE o UNDETERMINED, con sujeto, modo, datos, territorio, fecha, condiciones y evidencia. |
| evaluation / evidence | Comprobación realizada, versión del evaluador, localizadores y evidencia fechada; HUMAN_REVIEW_REQUIRED cuando proceda. |
| conclusion / limits | Resultado técnico separado de valoración jurídica; legal_conclusion_allowed=false para los motores actuales. |

La obligatoriedad técnica GTFS no equivale a obligatoriedad legal. GTFS aceptado operativamente por el NAP no demuestra compatibilidad plena con NeTEx ni cumplimiento de todas las obligaciones. Un error GTFS no prueba automáticamente infracción; un PASS tampoco acredita cumplimiento. NAP_PROVIDER_CONTRACT requiere acreditar las condiciones aceptadas por el proveedor; una FAQ no es legislación. Una norma técnica referenciada por ley exige determinar versión, perfil, alcance y aplicabilidad.

## Evidencia pendiente para publicación

| Dimensión | Evidencia requerida | Estado de esta actualización |
|---|---|---|
| NAP | Destino, acceso real, metadatos, perfil y acuerdo aplicable. | HUMAN_REVIEW_REQUIRED |
| Actualidad y exactitud | Horarios autorizados, servicio real, fechas y registro de actualizaciones/correcciones. | HUMAN_REVIEW_REQUIRED |
| Cobertura | Categorías y plazos aplicables del anexo; requisitos mínimos de calidad identificados. | HUMAN_REVIEW_REQUIRED |
| Privacidad | Revisión contextual de contactos, extensiones, URLs y archivos extra; no asumir que cualquier email es dato personal. | HUMAN_REVIEW_REQUIRED |
| Derechos y reutilización | Titularidad/autorización, licencia concreta, atribución y condiciones aplicables. | HUMAN_REVIEW_REQUIRED |
| Interoperabilidad espacial | Norma y perfil aplicables a la red; shapes.txt no acredita conformidad INSPIRE. | HUMAN_REVIEW_REQUIRED |

No se ha implementado un detector de datos personales, un conversor ni nuevos validadores jurídicos. No se ha evaluado un operador mediante este documento. Los 48 requisitos V1 conservan sus disposiciones y ninguno pasa a completo por incorporar fuentes.

## Corrección editorial y comprobación

La entrada ES-02 del generador comercial utiliza RD 450/2026 y explica la derogación. Los paquetes privados anteriores son evidencia histórica y no se reescriben. Nueva revisión privada COMMERCIAL-R4-LEGAL-UPDATE-20261008 generada: 67 páginas A4, nueve fichas de contexto con autoridad y aplicabilidad, 32 controles y 48 requisitos del catálogo congelado. Incluye las 33 capturas y un índice local de fuentes con hashes. Informe técnico y libro R3 preservados byte por byte; motor no repetido.

Verificación: 38/38 pruebas focalizadas PASS; controles de rechazo de hashes alterados, paths fuera de raíz, fuentes no capturadas y conclusión jurídica indebida. 33/33 hashes comprobados. QA de las 67 páginas PASS; doce láminas inspeccionadas visualmente sin defectos materiales observados. Paquete sellado y verificado. Resultados y recibo privado en PROJECT_STATUS.md.

## Cierre de esta tarea

No quedan capturas, correcciones editoriales, generación o comprobaciones técnicas pendientes de esta actualización. Las filas HUMAN_REVIEW_REQUIRED describen evidencias externas ausentes, no tareas de código sin terminar. Aplicabilidad, titularidad, licencia del conjunto, realidad del servicio y aceptación humana de emisión continúan NO DETERMINADAS sin documentos del responsable. No se cambia su estado a resuelto por disponer de normas. La navegación interactiva GIS pertenece al gate previo C06 y no se ha ejecutado aquí. Sin contacto, publicación, commit ni modificación de HOLDOUT.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
