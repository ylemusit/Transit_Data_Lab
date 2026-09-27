# Procurement evidence

Fecha de consulta: 2026-09-27. Investigación documental; importes nominales históricos, sin IVA salvo indicación. Una adjudicación acredita compromiso contractual, no facturas pagadas ni recepción satisfactoria. Evidencias y fuentes primarias en [MARKET_EVIDENCE_REGISTER.md](MARKET_EVIDENCE_REGISTER.md).

## Resultado económico

| Magnitud | Importe | Alcance |
| --- | ---: | --- |
| Dos adjudicaciones españolas directamente relacionadas | 91.866,25 EUR | TUVISA 31.866,25 + ATTG 60.000; contratos distintos de cuatro años, fechas distintas |
| Roma, adjudicación software GTFS | 188.873,75 EUR | Sistema y mantenimiento; sin desglose de validación |
| Nantes, tramo firme adjudicado | 660.810,00 EUR | Plataforma multimodal, integración y mantenimiento |
| Nantes, valor publicado total | 795.310,00 EUR | Incluye opciones y un máximo de pedidos; no afirmar ejecución de todas las opciones |
| Puglia, propuesta de compra aprobada | 149.710,00 EUR | Estimación para evolución RAP; no adjudicación verificada |
| Wiltshire, rango de ofertas considerado | 742.605–2.030.292 GBP | No identifica el precio ganador; no sumar como adjudicación |

Suma descriptiva de los dos contratos españoles, Roma y tramo firme Nantes: **941.550,00 EUR** de valores contractuales publicados. Incluyendo todo el valor publicado de Nantes: **1.076.050,00 EUR**, de los que 134.500 EUR corresponden a opciones/máximo variable. Ninguna suma es tamaño de mercado, ingresos recurrentes, gasto liquidado ni precio de una auditoría TDL. Se excluyen Puglia, Wiltshire, CTM y la concesión de Alicante del agregado.

## PROC-001 — TUVISA, caso inicial obligatorio

| Campo | Evidencia |
| --- | --- |
| Entidad / país / expediente | Transportes Urbanos de Vitoria-Gasteiz, S.A.; España; 2022-14LT |
| Fechas | Primera publicación 30/03/2022; adjudicación 26/05/2022; ficha actualizada 02/04/2025 |
| Objeto | Generación, desarrollo, despliegue y validación de datos avanzados de transporte |
| Estándares | GTFS, GTFS-RT, SIRI, NeTEx; PPT §1.4 cita EN 15531 / EN 16614 |
| Presupuesto / adjudicación / adjudicatario | 31.866,25 EUR sin IVA en ambos; Datik Información Inteligente, S.L.; un licitador publicado |
| Duración | Cuatro años; contrato cláusula 4 desde formalización; sin prórroga ordinaria. Prevé continuidad excepcional, no acreditada |
| Fuentes oficiales | MKT-EVD-001 a 005; aviso, PPT, PCAP, propuesta y contrato conservados en evidence/ |
| Capabilities potenciales | TDL-CAP-002/003/004/018/019, únicamente como componentes conceptualmente próximos y con sus límites V1; no cobertura del contrato |

**Qué se compró, comprobado en PPT de 11 páginas y contrato:**

- PPT §1.1, pp. 3–4: generar los ficheros necesarios; actualización al menos semanal; publicar mediante Google partners y enviar simultáneamente a Google, Ayuntamiento y Moveuskadi. Acceso de TUVISA a informes de validación. Exige ausencia de errores y contempla faltas por repetición.
- PPT §1.2, p. 4: vincular datos estáticos y tiempo real conservando identificadores de parada; describir controles, filtros e integridad.
- PPT §1.3, p. 5 y contrato cláusula 4: documento de cambios y cronograma diario; GTFS/GTFS-RT preparados el 30/10/2022; conversión SIRI/NeTEx el 15/11/2022. El contrato aclara el año omitido en ese párrafo del PPT.
- PPT §§1.4–2, pp. 6–7: disponer de formatos europeos y responsabilizarse de despliegue/validación cuando TUVISA lo solicite; vigilancia y bolsa de 30 horas. El pliego no atribuye a esas horas una periodicidad: no asumir 30 horas mensuales.
- PPT §3, pp. 7–9: corrección, soporte, monitorización, documentación y reporte mensual de defectos/cambios, tiempos de respuesta/resolución y seguimiento. Tabla p. 9 comprobada visualmente: urgentes 8/32 horas; normales 32/72 horas; objetivo de corregir el 95% dentro de esos tiempos; informe de defectos de más de 15 días.
- PPT §§4–5, pp. 9–10: coordinación y gestor técnico, memoria con metodología, diagramas y controles. Las titulaciones/experiencia aparecen como preferibles; no convertirlas en una certificación necesaria para TDL.

**Criterios:** PPT §6 / PCAP §8: precio 75 puntos; generación GTFS 10; vinculación tiempo real 5; GTFS-RT 5; SIRI/NeTEx 5. Propuesta p. 2: Datik obtuvo 22 puntos técnicos y 0 por precio, total 22; presupuesto sin baja. No demuestra ausencia de competencia en todo el mercado.

**Precisión contractual:** contrato p. 2 confirma importe total por cuatro años, prorratas mensuales y falta de revisión de precios. La ficha indica inicio 26/05/2022, firma empresa 01/07/2022 y firma administración 27/03/2025; la cláusula habla de duración desde formalización. Se conserva esta discrepancia; no se calcula una fecha final efectiva ni se afirma que continúe activo hoy solo por la etiqueta del portal. La ficha dice sin garantía definitiva, pero contrato cláusula 6 registra una garantía: prevalece el documento para ese dato; no extrapolar reglas jurídicas. No se ha verificado ejecución, pagos o cumplimiento de SLA.

**Relación con TDL:** hashes y consultas permiten conservar/inspeccionar evidencia; el sentinel solo cubre propiedades de Asturias y tiene WARNING (42 PASS/4 FAIL). Exportación Kbus es histórica y no demuestra completitud. TDL **no puede acreditar actualmente** generación operativa multiformato, GTFS-RT, NeTEx/SIRI, publicación Google/Moveuskadi, monitorización continua, corrección mantenida, disponibilidad o SLA. Mapping/audit están IN_DEVELOPMENT; no son oferta actual. Este contrato no es un precio general de mercado.

## PROC-002 — ATTG

| Campo | Evidencia |
| --- | --- |
| Entidad / país / fecha / expediente | Autoridad Territorial del Transporte de Gipuzkoa; España; adjudicación 28/02/2019; E3/2019/01 |
| Objeto / problema | Generación y mantenimiento de datos GTFS; cambios de red y coherencia de datos de 17 operadores Mugi (PPT §2) |
| Estándares | GTFS; GTFS-RT desde segundo año. Transmodel/NeTEx/SIRI: estudio y hoja de ruta durante tercer año, **no generación de esos tres estándares** en este contrato |
| Entregables | Feeds, publicación/controles, mantenimiento correctivo, informes mensuales, informe de evolución europea |
| Presupuesto / valor estimado | 63.000 / 78.750 EUR sin IVA; magnitudes diferentes |
| Adjudicación / adjudicatario | 60.000 EUR sin IVA; Ingartek Consulting, S.L. |
| Duración | Cuatro años; ficha contempla una prórroga; no se acredita ejercicio |
| Fuente oficial | MKT-EVD-006/007; ficha y PPT, §§1–3 y 6 |
| Capabilities | TDL-CAP-002/003/004/019: inspección y comparación acotadas; sin mantenimiento universal ni SLA |

## PROC-003 — CTM, valoración técnica, sin adjudicación confirmada

| Campo | Evidencia |
| --- | --- |
| Entidad / país / expediente / fecha | Consorci de Transports de Mallorca; España; OB202317 (portada 202317); fecha de firma/publicación no establecida con certeza en el documento leído |
| Objeto | Sistema BI/Big Data/Machine Learning: diseño, desarrollo, puesta en marcha y mantenimiento |
| Problema / entregables | Integrar información de posicionamiento y ticketing; adquisición GTFS automática/programable, predicciones, Trip Updates, Vehicle Positions, API REST, trazabilidad y calidad |
| Estándares | GTFS y GTFS-RT; no inferir NeTEx/SIRI para este expediente |
| Presupuesto / adjudicación / duración | No verificados; no estimar |
| Empresa observada | Alestis Consulting / GeoActio, como oferta evaluada; no afirmar adjudicatario |
| Fuente | MKT-EVD-008: PLACSP, informe de juicio de valor, pp. 1–3, 9–11, 18–27. Es **informe de evaluación**, no PPT original ni resolución |
| Capabilities | TDL-CAP-001/002/004/018: ingestión/inspección/export histórico; muy inferiores al sistema solicitado |

## PROC-004 — Región Puglia, propuesta de adquisición

| Campo | Evidencia |
| --- | --- |
| Entidad / país / fecha / expediente | Regione Puglia, sección transporte público e intermodalidad; Italia; 17/05/2024; 078/DIR/2024/00076 |
| Objeto / estándares | Evolución del Regional Access Point al nivel 3 del perfil italiano NeTEx; GTFS/CSV como entrada y NeTEx como salida |
| Problema / entregables | RAP existente cubre niveles 1/2; ampliar funciones, mantenimiento correctivo/adecuativo, formación, soporte y seguridad |
| Presupuesto / adjudicación / adjudicatario | 149.710 EUR sin IVA estimados/aprobación de propuesta; adjudicación y empresa no verificadas |
| Duración | 12 meses desde estipulación prevista; no fecha efectiva comprobada |
| Fuente | MKT-EVD-009, acto oficial pp. 3–6; Acuerdo Consip ID2213 lote 11 |
| Capabilities | TDL-CAP-001/002/004/009/010; sin conversión NeTEx ni integración RAP/NAP demostradas |

## PROC-005 — Wiltshire

| Campo | Evidencia |
| --- | --- |
| Entidad / país / fecha / expediente | Wiltshire Council; Reino Unido; conclusión 22/08/2022; PT1562 / DN604464 |
| Objeto / problema / entregables | Suministro y mantenimiento RTPI; arquitectura antigua y adaptación BODS; sistema de información al viajero |
| Estándares | BODS citado; formatos específicos no confirmados por el anuncio consultado |
| Presupuesto / adjudicación | Presupuesto no confirmado; rango de ofertas 742.605–2.030.292 GBP sin IVA; **precio adjudicado no individualizado** |
| Adjudicatario / duración | r2p UK Systems Ltd; duración no verificada |
| Fuente | MKT-EVD-010, anuncio F03 023202-2022, II.1.4 y V.2; lectura web oficial, descarga local 403 |
| Capabilities | TDL-CAP-004/019, proximidad débil a inspección/comparación; sin sistema RTPI |

## PROC-006 — Nantes, TED

| Campo | Evidencia |
| --- | --- |
| Entidad / país / fecha / expediente | SEMITAN mandataria de Nantes Métropole; Francia; conclusión 28/04/2023, publicación 08/05/2023; 22MB4/262; TED 272975-2023 |
| Objeto | Gestión centralizada multimodal de información al viajero y tráfico: concepción, desarrollo, implantación y mantenimiento |
| Estándares / problema | NeTEx, SIRI, GTFS, GTFS-RT; normalización, conversión, completitud, calidad e integración de fuentes |
| Entregables | Módulos de datos, información tráfico e indicadores; APIs y open data; conectores opcionales; pruebas, formación y seguimiento |
| Presupuesto / adjudicación | Presupuesto inicial no verificado. Valor adjudicado publicado 795.310 EUR sin IVA; tramo firme 660.810 y opciones/máximo 134.500 |
| Adjudicatario / duración | Okina; firme 24 meses desde notificación; opciones 1–4 seis meses y opción 5 cinco meses desde orden correspondiente |
| Criterios | Técnica 70%, precio 30%; tres ofertas |
| Fuente | MKT-EVD-030, TED II.2.4, V.2 y VI.3; HTML oficial conservado; anuncio previo 582917-2022 no se cuenta como otro contrato |
| Capabilities | TDL-CAP-001/002/003/004/018/019; relación parcial; TDL no acredita plataforma/conversión/operación |

## PROC-007 — Roma, TED

| Campo | Evidencia |
| --- | --- |
| Entidad / país / fecha / identificador | Roma Servizi per la Mobilità S.r.l.; Italia; conclusión 29/09/2022, publicación 12/10/2022; CIG 9072480F53 / CUI S10735431008202100014; TED 560078-2022 |
| Objeto / entregables / problema | Desarrollar software para adquirir, conservar, procesar y transferir GTFS y mantenerlo durante el servicio TPL |
| Estándares | GTFS; no inferir RT/NeTEx/SIRI |
| Estimación / adjudicación / adjudicatario | 285.000 EUR estimación inicial; 188.873,75 EUR adjudicados sin IVA; BIGO Solutions SRL |
| Duración / criterios | Número de meses no publicado en el aviso leído; vinculado al servicio TPL. Técnica 70, precio 30; tres ofertas |
| Fuente | MKT-EVD-031, TED II.1.4, II.2.4 y V.2 |
| Capabilities | TDL-CAP-001/002/004/016/018; funcionalidades próximas, sin producto de adquisición/mantenimiento general |

## PROC-008 — Alicante, obligación incorporada a concesión

| Campo | Evidencia |
| --- | --- |
| Entidad / país / expediente / fecha | Junta de Gobierno Local del Ayuntamiento de Alicante; España; 43/22; año de expediente 2022, fecha exacta no verificada |
| Objeto | Concesión de transporte urbano colectivo: regular, demanda rural y Turibús |
| Estándares / entregable | PCAP p. 20 requiere generación GTFS/GTFS-RT/NeTEx/SIRI; no prueba que el servicio esté entregado |
| Problema | Distribuir e intercambiar oferta de transporte como parte de la operación |
| Presupuesto / adjudicación / adjudicatario | Concesión completa: 145.570.280 EUR presupuesto, 385.709.149,20 EUR valor estimado, IVA no aplicable según portada. Parte de datos sin desglose; adjudicación/empresa no verificadas |
| Duración | Diez años previstos para concesión completa |
| Fuente | MKT-EVD-032; PCAP oficial PLACSP pp. 1/20 |
| Capabilities | TDL-CAP-002/004/018; no generación multiformato. **Importes excluidos del volumen económico de datos** |

## Búsqueda y cobertura

Orden de investigación: TUVISA primero; búsquedas indexadas PLACSP, Euskadi, Cataluña, TED y Find a Tender; recuperación directa de documentos; API pública TED para GTFS/NeTEx/SIRI y GTFS desde 2022. Registro reproducible de consultas y límites en [evidence/SEARCH_LOG.md](evidence/SEARCH_LOG.md), respuestas TED completas conservadas. Búsqueda de contratos menores sin caso directamente pertinente aceptado; no significa que no existan.

Es una muestra intencional, no censo ni estimación de cuota. No doble contar publicaciones sucesivas, valores estimados, presupuesto y adjudicación. Contratos mixtos requieren separar el componente de datos; tampoco se interpreta presupuesto como disposición a pagar por las capacidades concretas de V1.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
