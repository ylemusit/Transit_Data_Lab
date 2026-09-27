# Problem register

Consulta 2026-09-27. HECHO OBSERVADO = resultado publicado o contexto explícito; NECESIDAD CONTRATADA = tarea/requisito de compra, sin acreditar incidencia real; EXIGENCIA LEGAL = deber, sin acreditar incumplimiento. Las relaciones con TDL son inferencias acotadas al [V1](../02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md).

| ID | Problema y evidencia | Sujetos / consecuencia | Clasificación | Capabilities potenciales y límites |
| --- | --- | --- | --- | --- |
| PROB-001 | Resultados de validación con errores/advertencias publicados en PAN francés, incluidos datos SNCF; MKT-EVD-017/018 | Productores ferroviarios, autoridades y reutilizadores; resultados requieren revisión | HECHO OBSERVADO: hallazgos del validador, no cada error corroborado en campo | TDL-CAP-003/004/019; solo sentinel Asturias y comparación histórica, sin validador completo |
| PROB-002 | Cambios constantes en servicios y necesidad de mantenimiento semanal: PPT TUVISA/ATTG, MKT-EVD-002/007 | Bus y autoridades; vigencia de rutas y horarios | NECESIDAD CONTRATADA, no medición de feeds españoles desactualizados | TDL-CAP-001/002/016; conservar baseline/censo no acredita monitorización ni actualizaciones |
| PROB-003 | Identificadores y coherencia entre estático y tiempo real; TUVISA §1.2, ATTG §1.2 | Operadores/integradores; asociación de posiciones/viajes/paradas | NECESIDAD CONTRATADA | TDL-CAP-003/004; RT no demostrado |
| PROB-004 | Normalización y conversión NeTEx/SIRI/GTFS/RT; Nantes II.2.4, Puglia pp. 3–4; MKT-EVD-009/030 | Autoridades, ITS, NAP/RAP; interoperabilidad | NECESIDAD CONTRATADA / propuesta aprobada | TDL-CAP-004/010/019 como inspección/requisitos; sin conversores ni mapping probado |
| PROB-005 | Publicación simultánea y acceso a fuentes/reportes, TUVISA; acceso nacional Ley 9/2025 | Operadores, ayuntamientos, ministerio; información al viajero y reutilización | NECESIDAD CONTRATADA + EXIGENCIA LEGAL | TDL-CAP-002/018; export Kbus histórico, no publicador NAP/Google |
| PROB-006 | Integrar fuentes operativas y adquirir GTFS programadamente; CTM pp. 3/9–11, Roma II.1.4 | Consorcios, integradores; acceso automático y trazabilidad | NECESIDAD EN EVALUACIÓN + NECESIDAD CONTRATADA | TDL-CAP-001/002/004; no adquisición automática universal ni Data Lake |
| PROB-007 | Defectos y cambios requieren informes, responsables, tiempos y vigilancia; TUVISA §3/ATTG §3 | Compradores/operadores; seguimiento contractual | NECESIDAD CONTRATADA | TDL-CAP-002/011/012; gates Compliance no equivalen a gestión de incidencias del feed ni SLA |
| PROB-008 | Digitalizar, actualizar y corregir datos de movilidad; Ley arts. 85/86 y anexo I, UE arts. 6/8/9 | Titulares de servicios e infraestructura; suministro verificable | EXIGENCIA LEGAL; incumplimiento individual no investigado | TDL-CAP-009/010/011/012; infraestructura probatoria, sin auditoría jurídica completa |
| PROB-009 | Localización, rutas y accesibilidad forman parte de los datos exigidos; Ley anexo I.1/3; reglas gratuitas MobilityData | Operadores, estaciones y autoridades; representar oferta utilizable | EXIGENCIA LEGAL + estándar/reglas técnicas; no incidencia española cuantificada | TDL-CAP-004/016/019; GIS pendiente; sin verificación física de accesibilidad |
| PROB-010 | Arquitectura de información al viajero antigua requiere renovación; Wiltshire II.1.4, MKT-EVD-010 | Ayuntamiento, operadores y viajeros | HECHO OBSERVADO según comprador + NECESIDAD CONTRATADA | TDL-CAP-004/019, conexión débil; sin RTPI |

## Lo que la evidencia permite concluir

Existen compras de generación/mantenimiento y exigencias de calidad, publicación e interoperabilidad; existen resultados públicos con hallazgos de validación. No se han medido tasas de error españolas, coste de errores, feeds incompletos en España, exactitud geográfica en campo o necesidad insatisfecha de una auditoría independiente. Las exigencias de completitud de Nantes y las reglas MobilityData no autorizan a afirmar que todos los feeds son incompletos.

La observación francesa es instantánea: snapshot local SNCF muestra 46 advertencias estáticas y 383 errores en Trip Updates; el índice web consultado mostraba 580. Ambos momentos difieren. No sumar ni trasladar estas cifras a España; no reproducir el hallazgo histórico enum Bizkaibus invalidado como defecto del mercado. Los validadores pueden cambiar de reglas/versiones y producir falsos positivos.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
