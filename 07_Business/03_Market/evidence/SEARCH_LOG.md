# Registro de búsqueda y conservación

Fecha: 2026-09-27. Trabajo iniciado leyendo TUVISA 2022-14LT antes de ampliar contratación. Fecha del expediente/documento se extrae de fuente; no se usa fecha de rastreo del buscador como fecha de publicación.

## Consultas efectuadas y cobertura

Las siguientes consultas representan las rutas de búsqueda realmente realizadas; no se afirma exhaustividad del universo de contratos. Búsqueda web por dominio más apertura de documentos; no extracción completa de todas las plataformas.

| Ruta | Consultas ejecutadas (selección reproducible) | Resultado / límite |
| --- | --- | --- |
| TUVISA oficial | `site.contratacion.euskadi.eus 2022-14LT GTFS`; `"2022-14LT" "Desarrollo"`; `"2022-14LT" "técnicas"` | Ficha oficial; recuperar IDs de documentos desde HTML y descargar PPT/PCAP/propuesta/memoria/contrato |
| Euskadi | `site.contratacion.euskadi.eus "GTFS" "Presupuesto" -2022-14LT -desarrollo`; `site.contratacion.euskadi.eus "GTFS" -"2022-14LT" -"Desarrollo, despliegue" -"NETEX"` | ATTG E3/2019/01 y PPT; adjudicación Ingartek |
| PLACSP formatos | `site.contrataciondelestado.es GTFS NeTEx`; `site.contrataciondelestado.es "GTFS" "Adjudicatario"`; `site.contrataciondelestado.es ("GTFS-RT" OR "GTFS Realtime" OR "SIRI" OR "Transmodel") transporte` | CTM informe, Alicante PCAP y otros documentos candidatos; resultados mixtos |
| PLACSP problemas | `site.contrataciondelestado.es ("datos transporte" OR "datos movilidad" OR "información transporte" OR "NAP")`; `site.contrataciondelestado.es ("calidad datos" OR "validación datos transporte" OR "información al viajero")` | No convertir menciones genéricas/CPV en contratación independiente de calidad |
| Contratos menores | `site.contrataciondelestado.es "GTFS" "menor"`; `site.contrataciondelestado.es "GTFS" "contrato menor"` | Sin caso menor directamente pertinente aceptado en esta muestra; no evidencia de ausencia |
| Cataluña | `site.contractaciopublica.cat GTFS NeTEx` | Plataforma y documento tribunal; no contrato nuevo cuantificado aceptado |
| TED indexado | `site.ted.europa.eu NeTEx SIRI data quality`; `site.ted.europa.eu "NeTEx" "France"`; `"GTFS" site.ted.europa.eu/udl`; `"NeTEx" site.ted.europa.eu/en/notice/-/detail` | Indexación insuficiente; ampliar con API pública oficial |
| TED API | POST `https://api.ted.europa.eu/v3/notices/search`; query `FT ~ "GTFS"`, `FT ~ "NeTEx"`, `FT ~ "SIRI"`, limit 10; luego `FT ~ "GTFS" AND PD >= 20220101`, limit 30 | JSON completos guardados; búsqueda textual da ruido, no contratos aceptados automáticamente. Última devuelve 146 resultados y se examinan 30 títulos: no censo ni 146 contratos de datos |
| TED documentos | HTML oficiales 272975-2023, 582917-2022 y 560078-2022 | Nantes y Roma aceptados; anterior Nantes se vincula al mismo contrato. Avisos con objetos militares/obras y siglas coincidentes excluidos |
| UE regional | Búsquedas NeTEx/TED conducen a acto Regione Puglia 078/DIR/2024/00076 | Propuesta aprobada, no adjudicación; no sumar con Roma/Nantes como gasto ejecutado |
| Reino Unido | `site.find-tender.service.gov.uk "bus open data" contract awarded` | Wiltshire adjudicado con rango de ofertas; DfT anuncio previo BODS sin adjudicación confirmada |
| Norteamérica | Trillium términos/mantenimiento y 511.org/open-data/transit | Oferta y distribución de datos; no importe contractual norteamericano aceptado |

Otros candidatos PLACSP (PPT Extremadura, SAE/ticketing 04-2024, documento 2022/0143, informe inicio de expediente) se localizaron por snippets pero no se aceptan como contratos nuevos sin identificar cadena suficiente. Fuentes secundarias encontradas no se usan para cifras aceptadas.

## Regulación / problemas / proveedores

Consultas BOE Ley 9/2025, EUR-Lex 2017/1926 consolidado y 2024/490; guía/legislación GOV.UK BODS. En UE el HTML devolvía desafío/vacío y PDF timeout: requisitos se delimitan a extractos de fuente primaria recuperados por búsqueda, con localizadores, sin afirmar revisión íntegra consolidada vigente.

Consulta PAN Francia stats, SNCF y nouveautés. Se detecta desactualización de la ayuda de validadores que niega NeTEx, frente a novedades 2026 con reportes XSD: no aceptar esa ausencia como gap. Snapshot SNCF y resultado indexado difieren en contador RT; usar observación local fechada, sin tasa de mercado.

Búsquedas por sitios propios/documentación: enRoute, Trillium, Ito, GeoActio, Datik, Ingartek, Nommon, SkedGo; MobilityData README/rules/web, proyecto RT y OpenTripPlanner. Datik/Ingartek/Okina/BIGO se acreditan por contratos, sin inferir servicio amplio por nombre. Fuentes tecnológicas y regulatorias primarias; no rankings ni ventas/ingresos/clientes privados asumidos.

## Persistencia y fallos

`collect_sources.py` guarda bytes originales, extracción con páginas cuando PDF, URL final, tamaño y SHA-256 en manifiestos. Los intentos vacíos EU se marcan UNAVAILABLE_EMPTY_RESPONSE. Un SAVED solo se utiliza como copia cuando contiene texto relevante. Otros fallos: 403 Find a Tender/Trillium/Ito/SkedGo/GTFS.org; 404 descarga directa catálogo NAP. Lectura web permitió contrastar algunas afirmaciones; ello no convierte descarga fallida en snapshot.

`tuvisa_sources.json` conserva cuatro descargas iniciales; `source_manifest_extra.json` incluye contrato. Tabla SLA p. 9 del PPT renderizada e inspeccionada en `tuvisa_ppt_page9.png`: extracción de texto omitía las celdas.

`scope_before.json` guarda hashes de archivos fuera de Business antes de autoría/investigación persistida (snapshot inicial tardó y terminó antes de crear documentos); `verification.json` compara después y comprueba hashes integrantes/descriptor V1, documentos, enlaces/IDs y límites. Sin rerun técnico, commit o contacto.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
