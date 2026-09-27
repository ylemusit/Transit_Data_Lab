# Competitor landscape

Consulta 2026-09-27. Sin rankings. El proveedor describe su oferta; ello acredita que se anuncia, no rendimiento, ingresos ni todos sus clientes. Adjudicaciones sí identifican relaciones contractuales concretas, sin acreditar calidad de ejecución. No se infieren licencias de reutilización para TDL.

| COMP-ID | Empresa / país | Servicio / formatos | Tipo de cliente / modelo aparente | Evidencia | Comparable con TDL | Diferencias / límites |
| --- | --- | --- | --- | --- | --- | --- |
| COMP-001 | Datik / España | Desarrollo/despliegue/validación GTFS, RT, SIRI, NeTEx contratados | TUVISA; servicio por contrato de cuatro años | MKT-EVD-001–005 | CAP-002/003/004: inspección e integridad conceptual | Generación, publicación, soporte y SLA superan V1; no evaluar ejecución real |
| COMP-002 | Ingartek Consulting / España | Generación y mantenimiento GTFS, evolución RT/estudio europeo contratado | ATTG; contrato de cuatro años | MKT-EVD-006/007 | CAP-004/019: revisión/comparación | Mantenimiento multioperador; NeTEx/SIRI eran estudio, no conversión contratada |
| COMP-003 | GeoActio (Alestis Consulting) / España | Plataforma BI/RT, GTFS/GTFS-RT y API REST ofertadas | Consorcio CTM; SaaS descrito en oferta evaluada | MKT-EVD-008 | CAP-001/004/018: manejo de datos | Integración operativa/analítica/RT; no adjudicación verificada |
| COMP-004 | enRoute / Francia | Chouette SaaS para datos teóricos GTFS/NeTEx; Ara y oferta operador GTFS-RT/SIRI/SIRI Lite | Operadores, autoridades, NAP según proveedor; SaaS y acompañamiento | MKT-EVD-025 | CAP-001/003/004/018: colección/control/publicación conceptual | Referencial editable, agregación, historial, API, automatización y multiformato exceden V1 |
| COMP-005 | Trillium Solutions / EE. UU. | Creación, revisión, validación y mantenimiento GTFS con GTFS Manager | Agencias de transporte; términos de suscripción anual | MKT-EVD-028 | CAP-003/004: controles/inspección | Edición y mantenimiento; cliente aporta ubicación/horarios/tarifas. Términos no garantizan exactitud de datos origen; sin importes inferidos |
| COMP-006 | Ito / Reino Unido | Gestión/calidad de datos para información al viajero; oferta refiere GTFS y estándares CEN | Journey planners, MaaS y apps según proveedor; plataforma/equipo de datos, tarifa no comprobada | MKT-EVD-029 | CAP-003/004/019: controles/comparación conceptual | Calidad orientada al pasajero, intervención humana y actualización downstream; no verificar número/rendimiento de checks |
| COMP-007 | Okina / Francia | Plataforma central multimodal, conversión NeTEx→GTFS y SIRI→GTFS-RT requerida | SEMITAN/Nantes; desarrollo e implantación con mantenimiento | MKT-EVD-030 | CAP-001/003/004/018/019 | Integración, normalización, APIs/indicadores y conectores exceden V1; servicio contratado, resultados no auditados |
| COMP-008 | BIGO Solutions / Italia | Software de adquisición/conservación/procesamiento/transferencia GTFS y mantenimiento | Roma Servizi per la Mobilità; contrato software | MKT-EVD-031 | CAP-001/002/004/018 | Producto/mantenimiento general no acreditado para TDL; no inferir RT/NeTEx |
| COMP-009 | r2p UK Systems / Reino Unido | Suministro/mantenimiento RTPI | Wiltshire Council; contrato adjudicado | MKT-EVD-010 | CAP-004/019: relación muy limitada | Información al viajero operativa, no auditoría equivalente; formatos no establecidos en aviso |
| COMP-010 | SkedGo / Australia, contextual | Integración/planificación MaaS; consumo GTFS/GBFS según proveedor | Integradores, ciudades y agencias; APIs/SDKs/white label | MKT-EVD-026 | CAP-004/016: uso de datos, relación débil | Routing, personalización y aplicaciones no son V1; oferta no demuestra compra de auditoría |
| COMP-011 | Nommon / España, adyacente | Analítica/modelización de demanda y movilidad con datos masivos | Planificación/gestión; software/servicios según proveedor | MKT-EVD-027 | CAP-004: exploración, relación débil | No se acredita validador GTFS/NeTEx/SIRI en la fuente examinada; no competidor directo automático |

`CAP-xxx` = TDL-CAP-xxx. Otros nombres no contrastados quedan fuera; lista no exhaustiva. Modelos aparentes describen la evidencia del proveedor/contrato, sin inferir ingresos o márgenes.

## Herramientas gratuitas y open source

| TOOL-ID / alternativa | Funciones/cobertura comprobadas en documentación | Outputs | Limitaciones / diferencia con TDL |
| --- | --- | --- | --- |
| TOOL-001 — MobilityData Canonical GTFS Schedule Validator | GTFS Schedule; reglas de referencia y buenas prácticas; web, GUI, CLI y Docker; código Apache-2.0 | report.html, report.json y system_errors.json; avisos por severidad y metadatos | No certifica realidad del servicio ni cumplimiento jurídico integral; no es el validador RT/NeTEx/SIRI. Cobertura depende de versión/reglas. TDL-CAP-003 es mucho más acotado: Asturias, WARNING y capas ausentes; no reivindicar superioridad |
| TOOL-002 — MobilityData GTFS Realtime Validator | Proyecto separado para RT y relación con GTFS estático; documentación técnica propia | Reportes/notices de validación RT | Despliegue/operación a cargo del usuario; mantenimiento/versiones deben revisarse antes de uso. TDL no acredita RT. No ejecutado ni instalado |
| TOOL-003 — OpenTripPlanner | Routing multimodal; soporte NeTEx/SIRI con límites de perfiles documentados | Grafo/servicios de itinerarios, según configuración | No auditor normativo integral ni conversor universal. Demuestra alternativa abierta para consumo, no que V1 ofrezca routing |
| TOOL-004 — PAN Francia | Validación e indicadores publicados; novedades 2025/2026 incluyen MobilityData y validación NeTEx XSD/perfiles | Reportes, metadatos de validez/disponibilidad y errores descargables | Portal nacional con contexto/perfiles; no ejecución contractual del operador. Una página de ayuda aún dice que no hay NeTEx: desactualización contradicha por novedades 2026; no registrar ausencia actual de alternativa |
| TOOL-005 — Portales públicos NAP/Moveuskadi/511 | Catálogos y distribución de datos GTFS/RT y otros formatos publicados | Datos/APIs/catálogos | Acceso a datos no equivale a corrección/mantenimiento. No son automáticamente empresas competidoras; sí alternativas de infraestructura disponible |

Fuentes TOOL-001: MKT-EVD-020/021/022; TOOL-002: 023; TOOL-003: 024; TOOL-004: 017/018/019; TOOL-005: 015/016 y fuente contextual 511 en evidence/. Comparación documental; no benchmark ni comparación ejecutada.

## MobilityData: detalle relevante para la decisión

Entrada ZIP/directorio/URL según interfaz. Reportes legibles y JSON permiten integrar una comprobación sin desarrollar un validador propio. Reglas cubren sintaxis/referencias y comprobaciones semánticas/geográficas seleccionadas; existe catálogo de avisos por severidad. Revisar reglas y versión antes de comparar outputs: número de checks no demuestra exhaustividad ni exactitud en campo.

La web informa de almacenamiento de feeds hasta 30 días y servidores en EE. UU.; no se ha subido ningún dataset. El modo local es una alternativa documentada. El trabajo humano de interpretar, corregir fuentes, probar integración y mantener publicación aparece en contratos, pero su compra separada a TDL no está demostrada. **Ejecutar el validador gratuito, por sí solo, no constituye diferenciación acreditada**. Tampoco hay evidencia de que la trazabilidad TDL sea exclusiva: enRoute e Ito ya describen historial/control humano y Nantes exige indicadores.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
