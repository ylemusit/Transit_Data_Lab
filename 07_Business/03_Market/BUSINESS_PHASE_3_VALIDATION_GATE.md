# Business Phase 3 — commercial validation readiness gate

Fecha: 2026-09-27. BUSINESS_PHASE_3_VALIDATION_READINESS = PASS según verificación documental íntegra en [verification.json](readiness_review/verification.json) y [exit_code.txt](readiness_review/exit_code.txt). Significa plan trazable para contrastar hipótesis, no mercado validado ni aprobación de experimentos. Phase 3 IN_PROGRESS; V1 FROZEN; Phase 4 NOT STARTED.

## Decisión A–G

| Pregunta | Resultado | Evidencia y límite |
| --- | --- | --- |
| A Problemas reales documentados | YES, acotado | PROB-001 hallazgos PAN/SNCF (017/018); PROB-010 obsolescencia según comprador (010); avisos no son siempre defectos reales |
| B Actores identificables | YES | Categorías/segmentos por diez problemas; no leads ni compradores TDL |
| C Recursos/compra relacionados | YES | TUVISA/ATTG/Roma/Nantes/Wiltshire; adjudicación no pago ni compra separada de auditoría |
| D Porción abordable por EXISTING | PARTIAL | Inspección/procedencia/comparación acotadas e históricas; plausibilidad sin solución operativa transferible probada |
| E Diferenciación de gratuitas | NO; UNPROVEN | MobilityData/PAN y alternativas; revisión humana/trazabilidad no exclusivas |
| F Customer validation | NO | Sin confirmación de cliente potencial sobre TDL |
| G Willingness-to-pay | NO | Sin compromiso/pago específico TDL |

MARKET_VALIDATED = NO; DEMAND_VALIDATED = NO; WILLINGNESS_TO_PAY = NO; BUSINESS_MODEL_VALIDATED = NO. READY_FOR_CUSTOMER_DISCOVERY = YES para solicitar autorización del diseño PROB-001; sin outreach.

## Niveles y selección

Nivel 0: ninguno. Nivel 1: PROB-001. Nivel 2: PROB-008/009. Nivel 3: PROB-002/003/004/005/006/007/010. Nivel 4: ninguno. Niveles 5/6: ninguno. Sin scoring, ponderación o ranking.

PROB-001 conserva nivel 1: contratos compran controles dentro de producción/mantenimiento, no prueban compra específica de interpretar avisos publicados. Los errores RT de 018 no prueban causa estático/RT de PROB-003. Los indicadores de frescura 017 no acreditan una incidencia concreta de PROB-002. Puglia propuesta y DfT anuncio previo no prueban compra específica de evidenciar requisitos PROB-008. Level 3 PAID_NEED describe compra/licitación relacionada, sin afirmar desembolso.

YES: PROB-001, solo GTFS estático. HOLD: PROB-002/005/006/007/008/009, sin incidencia específica observada suficiente. NO: PROB-003/004/010 por NO_CURRENT_FIT. NO no niega el problema ni rechaza permanentemente el segmento. PROB-010 tiene observación y compra, pero V1 no tiene RTPI. [Matriz](COMMERCIAL_VALIDATION_READINESS.csv) y [plan](MARKET_VALIDATION_PLAN.md) contienen acciones e incertidumbres.

DIRECT_FIT: ninguno. PARTIAL_FIT: 001/002/005/006/007/008/009. NO_CURRENT_FIT: 003/004/010. UNKNOWN: ninguno. SQL genérico o lectura de estándares no cubren RT/conversión/RTPI. Ningún nivel 4: falta transferencia probada de una porción diagnóstica significativa a los flujos contratados.

## Ocho expedientes

Clasificación principal por etapa/naturaleza. País, comprador, proveedor, importe/tipo, duración, alcance/entregables y problemas conservados. Fuentes y localizadores detallados en [PROCUREMENT_EVIDENCE.md](PROCUREMENT_EVIDENCE.md). Ninguno DIRECTLY_COMPARABLE_TO_TDL_V1.

| ID / clasificación | contracting_entity / country / supplier | nominal_value / value_type | duration | scope / deliverables / relevant_problem_ids | Comparabilidad |
| --- | --- | --- | --- | --- | --- |
| PROC-001 AWARDED_CONTRACT | TUVISA / España / Datik Información Inteligente SL | 31.866,25 EUR sin IVA, total adjudicado/contrato | Cuatro años desde formalización; discrepancia de fechas conservada | Generación, actualización semanal, publicación simultánea, RT, conversión, control/reportes/SLA; PROB-002/003/005/007; 001 vínculo inferido de controles | PARTIALLY_COMPARABLE: inspección/procedencia, no contrato completo |
| PROC-002 AWARDED_CONTRACT | ATTG / España / Ingartek Consulting SL | 60.000 EUR sin IVA adjudicado; presupuesto 63.000 y estimado 78.750 separados | Cuatro años; ejercicio de prórroga no probado | GTFS 17 operadores, actualización/corrección/publicación, controles, RT año 2 y estudio europeo año 3; PROB-002/003/007; 001 inferencia control | PARTIALLY_COMPARABLE: inspección limitada, sin producción/RT/mantenimiento |
| PROC-003 OTHER (evaluación de licitación) | CTM / España / Alestis Consulting–GeoActio oferta evaluada; adjudicatario UNKNOWN | UNKNOWN; sin importe aceptado | UNKNOWN | BI/Data Lake, adquisición programada, API, ticketing/posiciones/RT/predicción/trazabilidad; PROB-006 | PARTIALLY_COMPARABLE en conservación/inspección, sin adjudicación o sistema equivalente |
| PROC-004 PROPOSAL | Regione Puglia / Italia / UNKNOWN | 149.710 EUR sin IVA estimación/propuesta aprobada; NO award | 12 meses previstos desde estipulación | RAP NeTEx nivel 3, mantenimiento/formación/soporte/seguridad; PROB-004/006/008 | PARTIALLY_COMPARABLE en raw/requisitos, sin RAP/conversor |
| PROC-005 AWARDED_CONTRACT | Wiltshire Council / Reino Unido / r2p UK Systems Ltd | UNKNOWN ganador; 742.605–2.030.292 GBP sin IVA rango de ofertas | UNKNOWN | RTPI/BODS suministro/mantenimiento; PROB-010 | NOT_COMPARABLE: sin RTPI V1 |
| PROC-006 AWARDED_CONTRACT | SEMITAN por Nantes Métropole / Francia / Okina | 660.810 EUR sin IVA firme; 134.500 opciones/máximo; 795.310 total publicado | Firme 24 meses; opciones 1–4 seis meses y 5 cinco desde orden | Plataforma multimodal, conversión/normalización, APIs/open data, indicadores/pruebas/formación; PROB-004/006/007 | PARTIALLY_COMPARABLE solo inspección/conservación, no plataforma |
| PROC-007 AWARDED_CONTRACT | Roma Servizi per la Mobilità / Italia / BIGO Solutions SRL | 188.873,75 EUR sin IVA adjudicado; 285.000 estimación inicial separada | Meses UNKNOWN; ligado al servicio TPL | Software adquirir/conservar/procesar/transferir GTFS y mantenimiento; PROB-002/006 | PARTIALLY_COMPARABLE: raw/procedencia/inventario/export históricos, sin producto universal |
| PROC-008 MIXED_CONTRACT (pliego concesión, award UNKNOWN) | Ayuntamiento Alicante / España / UNKNOWN | 145.570.280 EUR presupuesto global; 385.709.149,20 estimado global; IVA no aplicable según portada | Diez años previstos globales | Concesión TPL, requisito GTFS/RT/NeTEx/SIRI sin desglose; PROB-004/005 | NOT_COMPARABLE: concesión/producción operativa, sin valor atribuible a audit |

FRAMEWORK: ninguno de estos ocho principalmente así; Puglia utiliza Consip ID2213 lote 11 como vehículo, no noveno caso/techo calculado. TENDER: CTM es evaluación de oferta y se etiqueta OTHER para no inventar anuncio original/resultado. Comparabilidad parcial es un componente conceptual/histórico, nunca sustituibilidad, compra de audit o mercado direccionable.

91.866,25 EUR y 941.550 EUR permanecen como agregados nominales históricos exclusivamente. **NOT TAM; NOT SAM; NOT SOM; NOT TDL REVENUE; NOT EXECUTED PAYMENT TOTAL**. Tampoco 1.076.050 EUR con opciones es mercado. Sin agregación nueva, tarifa o fracción atribuida a TDL.

### TUVISA: separación funcional

| Componente | Evidencia existente | Relación V1 |
| --- | --- | --- |
| Data generation | 002 §1.1 archivos y formatos; 005 hitos | No producción universal; export Kbus histórico no cubre generación contratada |
| Maintenance | 002 semanal, correctivo/vigilancia | No mantenimiento operativo; raw/procedencia CAP-001/002 solo evidencia |
| Integration | 002 §1.2 estático/RT e identificadores; §1.4 SIRI/NeTEx | Fuera V1; SQL no valida RT ni convierte |
| Quality/control | 002 controles/reportes y ausencia errores | CAP-003/004/019 parcialmente relacionados; Asturias WARNING 42 PASS/4 FAIL, comparación histórica sin equivalencia |
| SLA | 002 §3 urgentes 8/32 h, normales 32/72 h, objetivo 95%, informe defectos >15 días | Sin SLA o gestión de incidencias; Gate Compliance distinto |
| Otros | Google/Ayuntamiento/Moveuskadi, cronograma/memoria/coordinación, bolsa 30 h sin periodicidad fijada | CAP-002/018 identifican entregas históricas; no publican/operan canales |

31.866,25 EUR sin IVA total por cuatro años, no anualidad ni precio de audit. Mantener discrepancias ficha/fechas/garantía; no afirmar vigencia efectiva, pagos ni intención de comprar TDL.

### ATTG: separación funcional

| Componente | Evidencia existente | Relación V1 |
| --- | --- | --- |
| Generation | 007 §1.1 17 operadores, códigos no comunes, feeds Google/Moveuskadi | No generación multioperador; CAP-004 inspección puntual, sin ajustes universales |
| Maintenance | 007 semanal y §3 correctivo | Sin actualización operativa de feeds |
| Monitoring | 007 §3 vigilancia/informes mensuales | CAP-002/019 procedencia/comparación histórica, sin monitor continuo |
| Corrections | 007 §3 defectos y tiempos | Sin corrección mantenida/SLA; CAP-003 no cobertura completa |
| Real-time coherence | 007 §1.2 identificadores/posiciones y §1.3 RT año 2 | NO_CURRENT_FIT RT; SQL estático no cubre entregable |
| Otros | 007 estudio/hoja de ruta Transmodel/NeTEx/SIRI año 3 | CAP-009/010 método documental acotado, sin conversión/generación de esos formatos ni vigencia jurídica |

60.000 EUR sin IVA adjudicados a Ingartek, total contractual; no mercado direccionable. Inspección/control explicable son relaciones parciales, sin compra independiente demostrada.

## Once EXISTING conservadas

Autoridad: [V1](../02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md), registro e índice técnico existentes. Sin estados cambiados ni herramientas técnicas ejecutadas. Relaciones inferidas en Business; capacidad acotada no demuestra disponibilidad comercial general.

| Capability | Uso posible en problemas | Límite |
| --- | --- | --- |
| TDL-CAP-001 | 002/006 raw | Asturias, sin adquisición/importación universal |
| TDL-CAP-002 | 002/005/006/007 procedencia | Hash identifica bytes, no calidad/licencia/compliance |
| TDL-CAP-003 | 001 controles puntuales | Asturias WARNING 42 PASS/4 FAIL y capas ausentes, sin motor completo/RT |
| TDL-CAP-004 | 001/006/009 inspección | Manual Asturias, sin biblioteca universal/conversor/RTPI |
| TDL-CAP-009 | 008 corpus | Histórico, sin vigencia certificada/actualización |
| TDL-CAP-010 | 008 requisitos; contexto 004 | Dependencias/anomalías parciales; sin mapping/conversión |
| TDL-CAP-011 | 007/008 revisión humana | Gates internos, no aceptación contractual del feed/dictamen |
| TDL-CAP-012 | 007/008 regresión | Baseline requisitos, sin monitor feed/replay integral |
| TDL-CAP-016 | 002/006/009 inventario | Cinco datasets históricos, no clientes/censo nacional |
| TDL-CAP-018 | 005/006 entrega histórica | Kbus: selección L3 frente a rutas AH/H/L2, sin completitud/round-trip |
| TDL-CAP-019 | 001/009 comparación | NAP/GTE histórico sin equivalencia/superioridad ni validador actual portable |

Las relaciones conceptuales previas con PROB-003/004/010 se conservan como contexto, pero no constituyen fit de su entregable. IN_DEVELOPMENT/PLANNED/PENDING_VERIFICATION excluidas como funcionalidad disponible. Mapping/audit son infraestructura sin resultados consolidados.

## Alternativas para PROB-001

| Alternativa | Resuelve documentadamente | No demuestra | Aporte TDL que habría que probar |
| --- | --- | --- | --- |
| TOOL-001 MobilityData Schedule (020/021/022) | HTML/JSON y reglas/comprobaciones seleccionadas, local/web | Realidad del servicio/compliance integral; no ausencia de interpretación útil | Explicación contextual verificable que reduzca trabajo frente al reporte; no mera ejecución de validador |
| TOOL-004 PAN (017/018/019) | Indicadores/reportes y validación GTFS/NeTEx | Resolución de fuente operativa/responsabilidad de cada aviso | Conectar aviso con causa/acción/aceptante si se necesita; compra/transferencia no probadas |
| TOOL-002 MobilityData RT (023) | Validador RT separado | Operación mantenida ni RT TDL | Ninguna promesa RT; solo contexto excluido del piloto |

Ito/enRoute ya describen intervención humana/historial. Sin exclusividad de diagnóstico/procedencia. TOOL-003 OpenTripPlanner y TOOL-005 portales ofrecen consumo/acceso, no auditoría integral. BOE/EUR-Lex gratuitos no prueban un auditor jurídico gratuito completo. DIFFERENTIATION = UNPROVEN en diez filas.

## Cuatro gaps potenciales

| Gap | Soporte | Alternativas | Capacidad actual / missing capability | Incertidumbre | Clasificación |
| --- | --- | --- | --- | --- | --- |
| GAP-001 evidencia independiente fuente/regla/resultado | 002/005 controles/reportes, 013 OBL-011 justificantes | enRoute historial 025, Ito revisión 029, PAN/MobilityData | CAP-002/009/011/019 partes; falta flujo transferible y necesidad independiente confirmada | Sin dolor específico de trazabilidad/preferencia por separar proveedor | HOLD |
| GAP-002 interpretar hallazgos específicos | 017/018 observación; 002/007 controles | MobilityData/PAN/proveedor actual | CAP-003/004/019 acotadas; faltan transferencia/corrección mantenida (excluida) | Sin utilidad incremental ni compra | READY_FOR_CUSTOMER_VALIDATION solo entrevista PROB-001 estático; UNPROVEN |
| GAP-003 conexión normativa con datos | 011/013/033/034 y OBL | BOE/EUR-Lex/perfiles/proveedores multiformato | CAP-009/010/011/012 método; mapping/audit sin resultados | Principalmente gap interno, no ausencia de oferta | OUTSIDE_CURRENT_V1 para solución completa |
| GAP-004 coherencia estático/RT/consumidores | 002/007/030 requisitos | MobilityData RT/enRoute/Okina/integradores | CAP-002/004/019 partes estáticas; faltan RT/NeTEx/SIRI/conversión | Sin necesidad TDL insatisfecha demostrada | OUTSIDE_CURRENT_V1 |

GAP-001 no pasa a candidato por proximidad a PROB-001. Puede explorarse como contexto, sin considerarlo observado. GAP-002 listo para entrevista no acredita oportunidad, corrección o piloto disponible. No oportunidades declaradas.

## Supuestos y siguiente autorización

Ocho ASM revisadas con soporte/contradicciones/faltantes/acción en [ASSUMPTIONS_REGISTER.md](../01_Governance/ASSUMPTIONS_REGISTER.md). PARTIALLY_SUPPORTED 001–003; UNTESTED 004–008; ninguna SUPPORTED/VALIDATED. PROPOSED_STATUS_CHANGE = NONE.

Siguiente autorización humana: customer discovery limitado según plan. Sin contacto, leads, scraping, entrevistas/pilotos ejecutados, precios, código, Phase 4 ni cierre de Phase 3.

## Tipos y trazabilidad de las 36 evidencias

Identificadores, fuentes/localizadores/fechas y limitaciones permanecen en MARKET_EVIDENCE_REGISTER.md. La tabla siguiente indexa las 36 entradas existentes; no investigación nueva. `evidence_count` cuenta IDs únicos, no casos/contratos/organizaciones. PROB-001 añade 002/007 como vínculo inferido de control contratado, sin incidencia atribuida a esos contratos. PROB-007 añade 019/020 como alternativa de reporte contextual. No modifica el registro fuente.


| Evidencia | Tipo(s) | Vínculo original | Fuente/localizador existente | Límite |
| --- | --- | --- | --- | --- |
| MKT-EVD-001 | PROCUREMENT_NEED | PROB-002/003/005/007 | [Fuente primaria](https://www.euskadi.eus/anuncio_contratacion/desarrollo-despliegue-y-validacion-datos-transporte-avanzados-formatos-gtfs-gtfs-rt-siri-y-netex/web01-tramite/es/) — Adjudicación / contrato | Conservar límites del registro; no demanda TDL |
| MKT-EVD-002 | PROCUREMENT_NEED | PROB-002/003/005/007 | [Fuente primaria](https://www.contratacion.euskadi.eus/ac70cPublicidadWar/downloadDokusiREST/descargaFicheroPorIdFichero?idFichero=962030&R01HNoPortal=true) — §§1–6, pp. 3–11; tabla p. 9 vista | Conservar límites del registro; no demanda TDL |
| MKT-EVD-003 | PROCUREMENT_NEED | PROB-007 | [Fuente primaria](https://www.contratacion.euskadi.eus/ac70cPublicidadWar/downloadDokusiREST/descargaFicheroPorIdFichero?idFichero=962031&R01HNoPortal=true) — §8, pp. 6–8 | Criterio de compra, no incidencia |
| MKT-EVD-004 | PROCUREMENT_NEED | PROB-002/005/007 | [Fuente primaria](https://www.contratacion.euskadi.eus/ac70cPublicidadWar/downloadDokusiREST/descargaFicheroPorIdFichero?idFichero=1184691&R01HNoPortal=true) — pp. 1–2 | Propuesta contrastada; mismo TUVISA |
| MKT-EVD-005 | PROCUREMENT_NEED | PROB-005/007 | [Fuente primaria](https://www.contratacion.euskadi.eus/ac70cPublicidadWar/downloadDokusiREST/descargaFicheroContratoPorIdFichero?idFichero=438804&R01HNoPortal=true) — Cláusulas 3–4; pp. 2–3 | Conservar límites del registro; no demanda TDL |
| MKT-EVD-006 | PROCUREMENT_NEED | PROB-002/003/007 | [Fuente primaria](https://www.euskadi.eus/web01-tramite/es/contenidos/anuncio_contratacion/expjaso16796/es_doc/es_arch_expjaso16796.html) — Datos de adjudicación | Conservar límites del registro; no demanda TDL |
| MKT-EVD-007 | PROCUREMENT_NEED | PROB-002/003/007 | [Fuente primaria](https://www.contratacion.euskadi.eus/webkpe00-kpeperfi/es/contenidos/anuncio_contratacion/expjaso16796/es_doc/adjuntos/pliego_bases_tecnicas1.pdf) — §§1–3/6 | Conservar límites del registro; no demanda TDL |
| MKT-EVD-008 | PROCUREMENT_NEED | PROB-006 | [Fuente primaria](https://contrataciondelestado.es/wps/wcm/connect/PLACE_es/Site/area/docAccCmpnt?DocumentIdParam=9259f10b-7ff6-4991-b8d1-6d948a5fc1a5&cmpntname=GetDocumentsById&source=library&srv=cmpnt) — pp. 1–3, 9–11, 18–27 | Evaluación, no adjudicación |
| MKT-EVD-009 | PROCUREMENT_NEED | PROB-004/006/008 | [Fuente primaria](https://trasparenza.regione.puglia.it/sites/default/files/2024-07/078_DIR_2024_00076_DeterminaPUB.pdf) — pp. 3–6 | Propuesta aprobada, no adjudicación |
| MKT-EVD-010 | PROCUREMENT_NEED;OBSERVED_PROBLEM | PROB-010 | [Fuente primaria](https://www.find-tender.service.gov.uk/Notice/023202-2022) — F03 023202-2022 II.1.4/V.2 | Obsolescencia también OBSERVED_PROBLEM según comprador |
| MKT-EVD-011 | REGULATORY_DRIVER | PROB-005/008/009 | [Fuente primaria](https://www.boe.es/eli/es/l/2025/12/03/9/con) — Arts. 85/86/90; anexo I | Conservar límites del registro; no demanda TDL |
| MKT-EVD-012 | REGULATORY_DRIVER | PROB-008/009 | [Fuente primaria](https://www.boe.es/eli/es/l/2025/12/03/9) — Arts. 85/86/90; anexo I | Conservar límites del registro; no demanda TDL |
| MKT-EVD-013 | REGULATORY_DRIVER | PROB-004/008 | [Fuente primaria](https://eur-lex.europa.eu/eli/reg_del/2024/490/oj/spa/pdf) — Art. 1.3/1.4/1.6/1.7; arts. 3–9 modificados | Cobertura parcial, no vigencia certificada |
| MKT-EVD-014 | REGULATORY_DRIVER | PROB-005/008 | [Fuente primaria](https://www.legislation.gov.uk/uksi/2020/749/contents/made) — Contents made; guía Who must publish / Publishing data | Conservar límites del registro; no demanda TDL |
| MKT-EVD-015 | FREE_ALTERNATIVE | PROB-005/006 | [Fuente primaria](https://nap.transportes.gob.es/Files/List?showFilterTT=true) — Filtros de modo | Catálogo, no defecto |
| MKT-EVD-016 | FREE_ALTERNATIVE | PROB-004/005 | [Fuente primaria](https://www.euskadi.eus/contenidos/ds_movilidad/md_ideeu_moveuskadi/es_def/index.shtml) — Descargar datos | Índice, no universalidad |
| MKT-EVD-017 | OBSERVED_PROBLEM;FREE_ALTERNATIVE | PROB-001/002 | [Fuente primaria](https://transport.data.gouv.fr/stats?locale=fr) — Zoom sur fraîcheur / qualité | Hallazgos/indicadores, no incidencia específica PROB-002 |
| MKT-EVD-018 | OBSERVED_PROBLEM;FREE_ALTERNATIVE | PROB-001/003 | [Fuente primaria](https://transport.data.gouv.fr/datasets/horaires-sncf?locale=fr) — Datos estáticos y tiempo real | Hallazgos, no causa estático/RT probada ni ground truth |
| MKT-EVD-019 | FREE_ALTERNATIVE | PROB-001/004 | [Fuente primaria](https://transport.data.gouv.fr/nouveautes?locale=fr) — Nouveautés | Funciones PAN, no incidencia adicional |
| MKT-EVD-020 | FREE_ALTERNATIVE | PROB-001 | [Fuente primaria](https://raw.githubusercontent.com/MobilityData/gtfs-validator/master/README.md) — README Visualize results / Validation rules / License | Conservar límites del registro; no demanda TDL |
| MKT-EVD-021 | STANDARD_REQUIREMENT;FREE_ALTERNATIVE | PROB-001/009 | [Fuente primaria](https://gtfs-validator.mobilitydata.org/rules.html) — Rules | Reglas/buenas prácticas, no deber legal universal |
| MKT-EVD-022 | FREE_ALTERNATIVE | PROB-001 | [Fuente primaria](https://gtfs-validator.mobilitydata.org/) — Interfaz / aviso almacenamiento | Conservar límites del registro; no demanda TDL |
| MKT-EVD-023 | FREE_ALTERNATIVE | PROB-001/003 | [Fuente primaria](https://raw.githubusercontent.com/MobilityData/gtfs-realtime-validator/master/README.md) — README | Conservar límites del registro; no demanda TDL |
| MKT-EVD-024 | FREE_ALTERNATIVE | PROB-004 | [Fuente primaria](https://docs.opentripplanner.org/en/latest/features-explained/Netex-Siri-Compatibility/) — Compatibility / limitations | Conservar límites del registro; no demanda TDL |
| MKT-EVD-025 | PROVIDER_CLAIM | PROB-002/004/006 | [Fuente primaria](https://enroute.mobi/fr/chouette) — Fonctionnalités / SaaS; enroute_operator | Conservar límites del registro; no demanda TDL |
| MKT-EVD-026 | PROVIDER_CLAIM | PROB-006 | [Fuente primaria](https://skedgo.com/how-skedgo-uses-gbfs/) — Artículo / modelo plataforma | Conservar límites del registro; no demanda TDL |
| MKT-EVD-027 | PROVIDER_CLAIM | PROB-006 | [Fuente primaria](https://www.nommon.es/es/) — Qué hacemos / productos | Proveedor adyacente, sin validador acreditado |
| MKT-EVD-028 | PROVIDER_CLAIM | PROB-002/007 | [Fuente primaria](https://trilliumtransit.com/gtfs-maintenance-terms-of-service/) — Purpose / Payment / Accuracy; trillium_gtfs | Conservar límites del registro; no demanda TDL |
| MKT-EVD-029 | PROVIDER_CLAIM | PROB-001/007 | [Fuente primaria](https://www.itoworld.com/inside-ito/why-ito/data-quality/) — Quality dimensions / Human control | Conservar límites del registro; no demanda TDL |
| MKT-EVD-030 | PROCUREMENT_NEED | PROB-004/006/007 | [Fuente primaria](https://ted.europa.eu/en/notice/272975-2023/html) — II.2.4; V.2; VI.3 | Conservar límites del registro; no demanda TDL |
| MKT-EVD-031 | PROCUREMENT_NEED | PROB-002/006 | [Fuente primaria](https://ted.europa.eu/en/notice/560078-2022/html) — II.1.4; II.2.4; V.2 | Conservar límites del registro; no demanda TDL |
| MKT-EVD-032 | PROCUREMENT_NEED | PROB-004/005 | [Fuente primaria](https://contrataciondelestado.es/wps/wcm/connect/PLACE_es/Site/area/docAccCmpnt?DocumentIdParam=49bd1667-6f07-4e9a-aa3f-124a144f2ab3&cmpntname=GetDocumentsById&source=library&srv=cmpnt) — Portada / p. 20 | Pliego concesión sin desglose datos |
| MKT-EVD-033 | STANDARD_REQUIREMENT | PROB-003/004 | [Fuente primaria](https://normes.transport.data.gouv.fr/normes/siri/profil-france/) — Avant-propos / conventions | Conservar límites del registro; no demanda TDL |
| MKT-EVD-034 | STANDARD_REQUIREMENT | PROB-004 | [Fuente primaria](https://normes.transport.data.gouv.fr/normes/netex/elements_communs/) — Éléments communs | Conservar límites del registro; no demanda TDL |
| MKT-EVD-035 | STANDARD_REQUIREMENT | PROB-003/004 | [Fuente primaria](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370373/General+information+SIRI) — Data correctness / completeness / freshness | Conservar límites del registro; no demanda TDL |
| MKT-EVD-036 | PROCUREMENT_NEED | PROB-005/008 | [Fuente primaria](https://www.find-tender.service.gov.uk/Notice/025414-2023) — II.1.4 | Intención previa, sin adjudicación/importe aceptado |

INFERENCE: relaciones de utilidad TDL, traslado de muestra francesa a otro actor, separar diagnóstico del contrato mayor y valor incremental. Nunca OBSERVED_PROBLEM. No se necesita consultar originales externos para interpretar estas entradas. NEW_EXTERNAL_RESEARCH = NO.

## Verificación y recursos

Resultado completo y métricas acotadas en readiness_review/verification.json y exit_code.txt. RESOURCE_GUARD_TRIGGERED = NO; repository-wide hash = NO. No se repite la verificación previa de alcance. Hashes históricos conservados, sin recalcular; nuevos hashes solo de archivos escritos aquí. Git untracked agrupado no acredita inmutabilidad global. Las escrituras se limitan explícitamente a siete artefactos, tres registros de gobierno y evidencia de verificación Business; no herramientas técnicas ni cambios de V1.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
