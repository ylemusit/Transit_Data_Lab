from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent.parent
E=ROOT/'evidence'
sources={}
for p in E.glob('source_manifest*.json'):
 for r in json.loads(p.read_text(encoding='utf-8')):sources[r['name']]=r
for r in json.loads((E/'tuvisa_sources.json').read_text(encoding='utf-8')):sources[r['name']]=r

# ID, snapshot key, type, description, source date, geography, reliability,
# problems, capabilities, limits, locator. No claim of source completeness.
rows=[
(1,'tuvisa_notice','CONTRATO','TUVISA adjudica generación/despliegue/validación multiformato a Datik por 31.866,25 EUR sin IVA.','30/03/2022; adjudicación 26/05/2022; actualización 02/04/2025','España','Alta: ficha pública','PROB-002/003/005/007','002/003/004/018/019','Fechas/garantía divergen respecto del contrato; sin pagos verificados.','Adjudicación / contrato'),
(2,'tuvisa_ppt','PLIEGO','Actualización semanal, coherencia estático/RT, vigilancia, informes, soporte y SLA.','Expediente 2022; fecha de firma no individualizada','España','Alta: PPT oficial','PROB-002/003/005/007','002/003/004/018/019','Requisito de compra, no prevalencia de errores ni ejecución satisfactoria.','§§1–6, pp. 3–11; tabla p. 9 vista'),
(3,'tuvisa_pcap','PLIEGO','Criterios 75 precio y 25 técnicos; condiciones administrativas.','Expediente 2022','España','Alta: PCAP oficial','PROB-007','011','No determina aptitud jurídica/comercial TDL.','§8, pp. 6–8'),
(4,'tuvisa_propuesta','ADJUDICACIÓN','Oferta Datik, 22 puntos técnicos, cero precio; total de cuatro años.','26/05/2022','España','Alta: propuesta oficial','PROB-002/005/007','003/004','La propuesta se contrasta con ficha y contrato, no se cuenta como otro expediente.','pp. 1–2'),
(5,'tuvisa_contract','CONTRATO','Importe total, prorratas, cuatro años desde formalización y hitos 2022.','Firma empresa indicada en ficha 01/07/2022; administración 27/03/2025','España','Alta: contrato publicado','PROB-005/007','002/011/018','Sin liquidación/pagos/recepción ni fecha final resuelta. No reproducir identificadores personales.','Cláusulas 3–4; pp. 2–3'),
(6,'attg_notice','ADJUDICACIÓN','ATTG E3/2019/01 adjudica mantenimiento/generación GTFS a Ingartek por 60.000 EUR.','11/01/2019; adjudicación 28/02/2019; actualización 12/03/2020','España','Alta: ficha pública','PROB-002/003/007','002/003/004/019','Histórico; no prueba compra actual o compra de auditoría separada.','Datos de adjudicación'),
(7,'attg_ppt','PLIEGO','Cambios en 17 operadores, mantenimiento y coherencia; hoja de ruta europea.','Expediente 2019','España','Alta: PPT oficial','PROB-002/003/007','003/004/019','NeTEx/SIRI son estudio; no generación comprometida por ese apartado.','§§1–3/6'),
(8,'ctm_document','EVALUACIÓN','CTM OB202317 evalúa plataforma BI/RT, adquisición programable GTFS y trazabilidad.','Expediente 202317; fecha exacta no verificada','España','Alta: documento oficial; limitada para adjudicación','PROB-006','001/002/004/018','Informe juicio de valor; no resolución/PPT original; sin importe verificado.','pp. 1–3, 9–11, 18–27'),
(9,'puglia_purchase','PROPUESTA COMPRA','RAP evolución NeTEx nivel 3, estimación 149.710 EUR sin IVA, 12 meses.','17/05/2024','Italia/UE','Alta: acto regional','PROB-004/006/008','001/004/009/010','Determinación a contratar; sin adjudicatario ni gasto realizado.','pp. 3–6'),
(10,'wiltshire_award','ADJUDICACIÓN','Modernización RTPI adjudicada r2p; aviso publica rango de ofertas.','22/08/2022 conclusión; aviso 2022','Reino Unido','Alta: aviso oficial leído vía web','PROB-010','004/019','Descarga 403; rango no es precio ganador; duración no verificada.','F03 023202-2022 II.1.4/V.2'),
(11,'ley9_consolidated','LEGISLACIÓN','Deberes de provisión/actualización/corrección, digitalización y acceso NAP.','04/12/2025; consolidación 21/03/2026','España','Alta: BOE; consolidado informativo','PROB-005/008/009','009/010/011/012','No dictamen de aplicabilidad; no actualización del corpus técnico.','Arts. 85/86/90; anexo I'),
(12,'boe_original','LEGISLACIÓN','Texto oficial original de Ley 9/2025, contrastado con consolidado en apartados de datos.','04/12/2025','España','Alta: publicación oficial','PROB-008/009','009/011','Texto original no sustituye revisión de modificaciones posteriores.','Arts. 85/86/90; anexo I'),
(13,'eu_2024_490','LEGISLACIÓN','Reforma 2017/1926: NAP, formatos, dinámicos, calidad, actualización y justificantes.','29/11/2023; DO 13/02/2024','UE','Alta fuente; cobertura parcial consultada','PROB-004/008','009/010/011/012','Extractos oficiales recuperados por búsqueda web; PDF timeout y alternativa vacía; no vigencia exhaustiva certificada.','Art. 1.3/1.4/1.6/1.7; arts. 3–9 modificados'),
(14,'uk_regulation','LEGISLACIÓN / GUÍA','SI 2020/749 y guía DfT regulan publicación de datos de bus en Inglaterra.','2020; guía actualizada 31/05/2022','Inglaterra','Alta: legislación/guía oficial','PROB-005/008','009/011','Guía no estatutaria; exenciones/alcance local; sin extrapolar a todo Reino Unido.','Contents made; guía Who must publish / Publishing data'),
(15,'nap_catalog','ORGANISMO PÚBLICO','Catálogo NAP España incluye bus, ferroviario y marítimo.','Página dinámica, sin fecha editorial','España','Alta: catálogo oficial leído vía web','PROB-005/006','016/019','Descarga directa 404; presencia no acredita calidad, licencia ni comprador; no fijar conteos dinámicos.','Filtros de modo'),
(16,'moveuskadi','ORGANISMO PÚBLICO','Índices oficiales de datos GTFS, RT, SIRI y NeTEx de Euskadi.','Sin fecha editorial comprobada','España','Alta: publicador oficial','PROB-004/005','016/019','Índice no prueba todas las implementaciones/actualización o acceso sin condiciones.','Descargar datos'),
(17,'france_stats','ORGANISMO PÚBLICO','PAN publica indicadores de validez/frescura y calidad de GTFS/NeTEx.','Página dinámica','Francia/UE','Alta para indicador publicado','PROB-001/002','003/004/019','Contadores variables; no extrapolar incidencia española ni ground truth.','Zoom sur fraîcheur / qualité'),
(18,'france_sncf','RESULTADO PÚBLICO','SNCF publica GTFS/NeTEx/RT/SIRI Lite; hallazgos de validación visibles.','Datos dinámicos; consulta 27/09/2026','Francia/UE','Alta para hallazgo publicado','PROB-001/003','003/004/019','Snapshot 383 errores RT versus índice web 580; hallazgos no corroborados uno a uno.','Datos estáticos y tiempo real'),
(19,'france_news','ORGANISMO PÚBLICO','PAN integra MobilityData y reportes NeTEx XSD/perfiles.','Entradas diciembre 2025 / febrero 2026','Francia/UE','Alta: novedades oficiales','PROB-001/004','003/019','No inferir cobertura completa SIRI o auditoría normativa; contradice ayuda NeTEx obsoleta.','Nouveautés'),
(20,'mobilitydata_readme','OPEN SOURCE','Validador GTFS Schedule Apache-2.0, interfaces y reportes HTML/JSON.','README rama master sin fecha editorial; snapshot 27/09/2026','Global/Norteamérica','Alta para funciones documentadas','PROB-001','003/004','No ejecutado; no certifica exactitud real/ley; versión debe fijarse para benchmark.','README Visualize results / Validation rules / License'),
(21,'mobilitydata_rules','REGLAS TÉCNICAS','Catálogo de notices por severidad, reglas de referencia/buenas prácticas.','Página sin fecha editorial; snapshot 27/09/2026','Global','Alta para cobertura documentada','PROB-001/009','003','No todas las reglas son obligaciones legales; cobertura depende versión.','Rules'),
(22,'mobilitydata_web','HERRAMIENTA GRATUITA','Interfaz de validación gratuita de ZIP/URL y política de almacenamiento publicada.','Página sin fecha editorial','Global','Alta para interfaz/política publicada','PROB-001','003','No se ha subido feed; web informa hasta 30 días/EE. UU.; no evaluación jurídica.','Interfaz / aviso almacenamiento'),
(23,'rt_validator','OPEN SOURCE','Proyecto separado de validación GTFS Realtime.','README sin fecha editorial','Global','Alta para documentación técnica','PROB-001/003','003','No instalado/ejecutado; no asegurar mantenimiento/soporte operativo por existencia del repo.','README'),
(24,'otp_formats','OPEN SOURCE','OpenTripPlanner documenta soporte y límites NeTEx/SIRI.','Documentación latest, sin fecha editorial','Global/UE','Alta para documentación técnica','PROB-004','004','No auditor completo/conversor universal ni capacidad TDL.','Compatibility / limitations'),
(25,'enroute_chouette','PROVEEDOR','Chouette SaaS: colección, edición, controles, historial y publicación GTFS/NeTEx.','Sin fecha editorial','Francia/UE','Media: oferta declarada','PROB-002/004/006','001/003/004/018','Prestaciones anunciadas no benchmark; oferta RT contrastada en página operator.','Fonctionnalités / SaaS; enroute_operator'),
(26,'skedgo','PROVEEDOR','Consumo de GTFS/GBFS para MaaS, APIs/SDKs e integración.','Página How SkedGo uses GBFS; fecha exacta no comprobada','Australia/global','Media: oferta declarada vía web','PROB-006','004/016','Descarga 403; consumidor/proveedor adyacente, no cliente TDL; sin ingresos asumidos.','Artículo / modelo plataforma'),
(27,'nommon','PROVEEDOR ADYACENTE','Oferta de software/servicios de analítica y modelización de movilidad.','Sin fecha editorial','España','Media: oferta declarada','PROB-006','004','No se verifica oferta de validación GTFS en la página.','Qué hacemos / productos'),
(28,'trillium_terms','PROVEEDOR','Términos de creación/validación y mantenimiento GTFS con suscripción anual.','Revisado 01/12/2022 según sitio','EE. UU.','Media: términos proveedor vía web','PROB-002/007','003/004','Descarga 403; sin precio/clientes/ingresos inferidos; GTFS página complementar.','Purpose / Payment / Accuracy; trillium_gtfs'),
(29,'ito_quality','PROVEEDOR','Plataforma de calidad, revisión humana y corrección downstream anunciadas.','Sin fecha editorial','Reino Unido/global','Media: oferta declarada vía web','PROB-001/007','003/004/011/019','Descarga 403; no verificar desempeño, conteo de checks o cuota.','Quality dimensions / Human control'),
(30,'ted_nantes_award','ADJUDICACIÓN TED','Okina adjudicataria de plataforma multiformato Nantes: 795.310 EUR con opciones.','28/04/2023 conclusión; 08/05/2023 publicación','Francia/UE','Alta: TED HTML oficial descargado','PROB-004/006/007','001/003/004/018/019','Tramo firme 660.810; opciones no acreditadas como ejecutadas; no CCTP completo.','II.2.4; V.2; VI.3'),
(31,'ted_rome_award','ADJUDICACIÓN TED','BIGO Solutions, software GTFS y mantenimiento, 188.873,75 EUR sin IVA.','29/09/2022 conclusión; 12/10/2022 publicación','Italia/UE','Alta: TED HTML oficial descargado','PROB-002/006','001/002/004/016/018','Duración numérica ausente; no atribuir formatos no publicados.','II.1.4; II.2.4; V.2'),
(32,'placsp_43_22','PLIEGO CONCESIÓN','Alicante exige generación GTFS/RT/NeTEx/SIRI dentro de concesión bus.','Expediente 2022; fecha exacta no verificada','España','Alta: PCAP oficial','PROB-004/005','002/004/018','Importe global no precio de datos; sin adjudicación/entrega verificadas.','Portada / p. 20'),
(33,'siri_france','ESTÁNDAR / PERFIL','Perfil francés SIRI define convenciones e interfaces técnicas.','16/03/2026','Francia/UE','Alta: perfil publicado por organismo','PROB-003/004','009/010','Requisito técnico contextual; no obligación española autónoma.','Avant-propos / conventions'),
(34,'netex_france','ESTÁNDAR / PERFIL','Perfil francés NeTEx v2.4, elementos comunes e intercambio.','16/03/2026 según publicación','Francia/UE','Alta: perfil oficial','PROB-004','009/010','No probar equivalencia universal con GTFS.','Éléments communs'),
(35,'entur_siri','PERFIL TÉCNICO','Perfil noruego trata corrección, completitud y frescura de datos SIRI.','Sin fecha editorial verificada','Noruega/Europa','Alta: documentación técnica del organismo','PROB-003/004','009/010','Reglas/perfil contextual, no convertir a legislación española.','Data correctness / completeness / freshness'),
(36,'bods_notice','ANUNCIO PREVIO','DfT anuncia intención de contratación de soporte BODS.','Aviso 025414-2023, año 2023','Reino Unido','Alta: aviso oficial vía web','PROB-005/008','009/019','No adjudicación ni importe contractual aceptado; título 24000000 no se interpreta como presupuesto.','II.1.4'),
]

overrides={
 'skedgo':'https://skedgo.com/how-skedgo-uses-gbfs/',
 'uk_regulation':'https://www.legislation.gov.uk/uksi/2020/749/contents/made',
}
header='''# Market evidence register

Consulta: **2026-09-27**, Europe/Madrid. **36 entradas aceptadas**, cada una restringida a la afirmación descrita; aceptación no significa validación comercial o comprobación de rendimiento. Fuentes principales: contratación pública española/TED, BOE, EUR-Lex, organismos, documentación técnica y proveedores. No se usan directorios comerciales para aceptar importes.

Fiabilidad evalúa la fuente para esa afirmación: alta para publicación oficial/documentación propia, media para oferta declarada. La cobertura puede ser parcial incluso con fuente alta. Fecha de fuente no es fecha de consulta. “Sin fecha” no se inventa. CAP-xxx en campos es TDL-CAP-xxx de V1; relación inferida, no capacidad ampliada.

Conservación: HTML/PDF/README y extracciones cuando fue posible; manifiestos JSON con URL, fecha, bytes y SHA-256. Para fuentes solo recuperadas vía herramienta web, se conserva URL/localizador y nota de consulta; **no copia íntegra verificada**. Una descarga vacía o 403 nunca acredita contenido. Los documentos originales pueden contener datos personales publicados: los resúmenes no los reproducen.

Navegación: [segmentos](CUSTOMER_SEGMENTS.md), [problemas](PROBLEM_REGISTER.md), [contratación](PROCUREMENT_EVIDENCE.md), [alternativas](COMPETITOR_LANDSCAPE.md), [regulación](REGULATORY_DEMAND.md), [gaps y evaluación A–G](MARKET_GAPS.md), [búsqueda](evidence/SEARCH_LOG.md).

'''
text=header
for n,key,typ,desc,date,geo,rel,prob,caps,lim,locator in rows:
 r=sources.get(key,{})
 url=overrides.get(key,r.get('url',''))
 path=E/(key+'.txt')
 saved=path.exists() and path.stat().st_size>0
 local=f'[Texto conservado](evidence/{key}.txt)' if saved else 'Lectura web oficial/documentación del proveedor; sin copia local íntegra'
 text+=f'## MKT-EVD-{n:03d}\n\n| Campo | Valor |\n| --- | --- |\n'
 fields={'Tipo':typ,'Descripción':desc,'Fuente':f'[Fuente primaria]({url})','Localizador':locator,'Fecha fuente':date,'Fecha consulta':'2026-09-27','Geografía':geo,'Fiabilidad':rel,'Relación problema':prob,'Relación capability':'TDL-CAP-'+caps.replace('/',' / TDL-CAP-'),'Limitaciones':lim,'Conservación':local}
 for a,b in fields.items():text+=f'| {a} | {b} |\n'
 text+='\n'
text+='Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n'
(ROOT/'MARKET_EVIDENCE_REGISTER.md').write_text(text,encoding='utf-8')
(E/'accepted_evidence.json').write_text(json.dumps([dict(id=f'MKT-EVD-{r[0]:03d}',source_key=r[1],description=r[3]) for r in rows],ensure_ascii=False,indent=2),encoding='utf-8')
print('Created register with',len(rows),'entries')
