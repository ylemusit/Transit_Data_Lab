# Market gaps

Consulta 2026-09-27. Solo las 11 EXISTING del [BUSINESS_CAPABILITY_BASELINE_V1](../02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md). Cada fila expresa **relación potencial**, no oferta, demanda por TDL ni gap comercial validado. Confianza distingue el vínculo conceptual de la incertidumbre de compra/diferenciación.

| CAPABILITY | PROBLEMA OBSERVADO | SEGMENTO | EVIDENCIA | ALTERNATIVA EXISTENTE | GAP POTENCIAL | CONFIANZA |
| --- | --- | --- | --- | --- | --- | --- |
| TDL-CAP-001 Ingestión raw Asturias | PROB-006 adquirir/conservar GTFS (compra) | Autoridades/consorcios | MKT-EVD-008/031 | BIGO, GeoActio, enRoute; herramientas abiertas | Preservar raw antes de transformar; portabilidad/adquisición universal no demostradas; necesidad insatisfecha no probada | Media vínculo; baja gap |
| TDL-CAP-002 Integridad/procedencia binaria | PROB-005/007 identificar versiones y cambios (requisito contractual) | Operadores/autoridades/integradores | MKT-EVD-002/005/030 | Historial enRoute; registros/indicadores de sistemas | Cadena de evidencia fuente→resultado para revisión independiente; hashes prueban identidad, no calidad/licencia | Media vínculo; baja diferenciación |
| TDL-CAP-003 Controles Asturias | PROB-001/003 hallazgos de calidad/coherencia | Bus/ferrocarril/autoridades | MKT-EVD-007/018/020 | MobilityData gratuito, PAN, Ito | Controles específicos complementarios según regla acordada; no cobertura universal, no ventaja sobre gratuito | Alta existencia problema; baja gap |
| TDL-CAP-004 SQL read-only | PROB-001/006 inspección/integración | Consorcios/integradores | MKT-EVD-008/031 | enRoute APIs; herramientas SQL y sistemas de datos | Diagnóstico explicable de un subconjunto; no biblioteca/informe automático consolidado | Media vínculo; baja compra |
| TDL-CAP-009 Corpus normativo trazable | PROB-008 demostrar requisitos y fuentes | Autoridades/NAP/operadores | MKT-EVD-011/013, OBL-011 | BOE/EUR-Lex gratuitos; revisión interna/asesoramiento (alternativa organizativa, gasto no contrastado) | Evidencia de qué versión se interpretó; corpus V1 no actualizado por esta investigación | Media vínculo; baja diferenciación |
| TDL-CAP-010 Requirements engine 2017/1926 | PROB-008 estructurar requisitos | NAP/autoridades/integradores | MKT-EVD-013 | Perfiles técnicos oficiales; revisión interna | Seguimiento requisito→evidencia pendiente; anomalías/dependencias parciales, mapping sin resultados | Media vínculo; baja gap |
| TDL-CAP-011 Revisión humana Gate 1/2 | PROB-007/008 revisión/aprobación | Autoridades/operadores | MKT-EVD-002/013/029 | Ito control humano; aceptación contractual interna | Responsabilidad/justificación por requisito; no auditoría completa ni dictamen jurídico | Media vínculo; baja gap |
| TDL-CAP-012 Regresión Compliance | PROB-008 mantener interpretación consistente | NAP/integradores | MKT-EVD-013/020 | Tests de herramientas abiertas / procesos internos | Detectar cambios del baseline de requisitos; no monitor de feed, no replay integral | Media método; baja compra |
| TDL-CAP-016 Censo cinco datasets | PROB-006 conocer fuentes/inventario | Autoridades/consorcios/NAP | MKT-EVD-015/016/030 | Catálogos públicos NAP/PAN/511 | Inventario físico y procedencia de lote autorizado; cinco datasets históricos no son 20 clientes | Media vínculo; baja gap |
| TDL-CAP-018 Export GTE con manifiesto | PROB-005/006 entrega/transferencia | Bus/autoridades/integradores | MKT-EVD-002/031 | Generadores enRoute/Trillium/BIGO | Identificación de entrega preservada; Kbus histórico con discrepancia de selección L3, sin round-trip/completitud | Baja capacidad de cubrir compra |
| TDL-CAP-019 Comparación NAP/GTE | PROB-001/004 comparar resultados/fuentes | Autoridades/NAP/consultoras | MKT-EVD-015/018/030 | PAN validación, MobilityData, dashboards proveedores | Explicar discrepancias de resultados con procedencia; no equivalencia de reglas ni superioridad | Media vínculo; baja diferenciación |
| — Observación de exactitud operativa (sin capability V1 acreditada) | PROB-011 comparar horarios/rutas publicados con servicio observado | Agencias y reutilizadores | MKT-EVD-037 | MobilityData Schedule Validator; informes mensuales públicos Cal-ITP | Medir diferencias entre lo programado y patrones reales de vehículos; el alcance publicado de alternativas describe validación/feed y no documenta esa comparación GPS/RT específica | Media para existencia del método/problema; baja para extensión/demanda |

## Gaps potenciales, no oportunidades definitivas

- **GAP-001 — evidencia independiente entre fuentes, reglas y resultados.** Contratos exigen controles/reportes y norma prevé justificantes. V1 ofrece partes de trazabilidad/revisión. Falta demostrar que comprador necesite separarlas de su proveedor, que alternativas no las cubran y que pague por ellas.
- **GAP-002 — interpretación y seguimiento de hallazgos específicos.** Validación gratuita produce avisos; contratos compran corrección y vigilancia. TDL tiene inspección acotada, no capacidad mantenida de corrección. No se ha probado demanda por un diagnóstico separado.
- **GAP-003 — conexión normativa documentada con datos.** Hay requisitos aplicables y perfiles; V1 tiene corpus/engine/revisión, pero mapping/audit sin resultados. Es sobre todo **gap interno TDL**, no ausencia de oferta: existen proveedores multiformato y perfiles abiertos.
- **GAP-004 — coherencia entre publicación estática, RT y varios consumidores.** TUVISA, Nantes y ATTG lo exigen. Mercado ya ofrece integración/conversión; TDL no acredita RT, NeTEx o SIRI. No tratarlo como hueco listo para explotar.
- **GAP-005 — exactitud de la oferta publicada frente a la operación observada.** Un estudio institucional define métricas comparando GTFS Schedule/RT con recorridos reales de vehículos (MKT-EVD-037). MobilityData documenta validación contra referencia y buenas prácticas; Cal-ITP publica informes mensuales de reglas y operaciones representadas (MKT-EVD-038/039), sin documentar en ese alcance cotejo GPS/RT con servicio realizado. Es un límite de lo publicado, no incapacidad absoluta; evidencia internacional/metodológica acotada, sin prevalencia española, comprador, frecuencia, cobertura universal ni demanda demostrados. No existe capability V1 acreditada para esa comparación.

No se acepta como gap probado “no hay validación gratuita”, “nadie ofrece mantenimiento”, “no hay proveedores NeTEx/SIRI” o “los hashes garantizan compliance”. Las fuentes contradicen o no permiten esas formulaciones. GIS, replay y GTE vigente siguen PENDING_VERIFICATION; motor GTFS/analítica/findings PLANNED y mapping/audit IN_DEVELOPMENT solo son contexto futuro, sin oferta actual ni cambios autorizados.

## Evaluación A–G y resultado

| Criterio | Evaluación | Evidencia / límite |
| --- | --- | --- |
| A Problema | Suficiente | Hallazgos PAN Francia y necesidad de cambios/controles contratada en España; prevalencia española no cuantificada |
| B Sujetos | Suficiente | 15 segmentos clasificados; no todos compradores |
| C Contratación | Suficiente | Cuatro adjudicaciones EUR cuantificadas, una británica sin precio ganador individualizado; propuestas/contratos mixtos separados |
| D Alternativas | Suficiente | 11 proveedores/actores; cinco clases de herramientas/infraestructura gratuita; sin ranking |
| E Regulación | Suficiente para identificar presión | 12 registros OBL; obligaciones separadas; vigencia/exhaustividad individual no certificada |
| F Gaps | Suficiente para evaluar incertidumbre | Cuatro gaps potenciales y límites; ninguno declarado oportunidad comercial definitiva |
| G Capabilities | Suficiente | Matriz completa de las 11 EXISTING, manteniendo límites y congelación |

**BUSINESS_PHASE_3_MARKET_EVIDENCE = PASS** para evaluación documental A–G. No equivale a validar demanda suficiente para TDL, readiness, product-market fit, precios o una oferta. STATUS permanece IN PROGRESS según autorización; dossier preparado para revisión del usuario, sin cierre/aprobación inferidos. Phase 4 no iniciada.

## Incertidumbres principales

Muestra española histórica/concentrada en Euskadi; compras de auditoría independiente no demostradas; datos de gasto ejecutado ausentes; presupuesto de componente datos en contratos mixtos desconocido; necesidades ferroviarias/marítimas y privadas sin gasto específico; coste de errores/beneficio/costes TDL sin medir; derechos/licencias de reutilización y viabilidad jurídica no evaluados; equivalencia GTFS/NeTEx por perfil no comprobada; corpus V1 no actualizado; cambios de contadores PAN entre consultas; fuentes web sin copia local en algunos casos. Búsqueda TED limitada, siglas con ruido y múltiples avisos por contrato: no usar número de resultados como número de clientes.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
