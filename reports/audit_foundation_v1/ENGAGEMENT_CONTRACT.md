# TDL-AUD-01 — ficha de encargo y límites de conclusión

Contrato `TDL_AUDIT_ENGAGEMENT/1`. Fecha: 2026-10-08. Los ejemplos son internos, no acuerdos con un operador.

| Campo | Contenido requerido | Desconocido |
|---|---|---|
| engagement_id / purpose | Identidad del encargo y objetivo concreto. | No emitir un encargo sin identificador/objetivo. |
| format | GTFS_SCHEDULE o NETEX. | Otros formatos se rechazan. |
| source | Identidad del fichero y SHA-256; revisión del productor si existe. | `null`: aún no se pueden vincular resultados. |
| reference | Especificación/versión; en NeTEx esquema/hash y perfil/criterios separados. | `null`: no afirmar conformidad con versión/perfil desconocido. |
| destination | Destinatario, uso y evidencia de criterios de aceptación. | `null`: aptitud para ese destino no determinada. |
| period | Periodo del servicio o del análisis; distinguir extracción observada y periodo acordado. | `null`: no inventar vigencia ni plazos. |
| included_controls | IDs exactos incluidos, vinculados al inventario. | Lista vacía: no hay conclusión técnica delimitada. |
| exclusions | Procesos, formatos, criterios y verificaciones que no entran. | Deben declararse antes de comunicar resultados. |
| service_reference | Evidencia independiente para contrastar horarios, paradas o recorridos reales. | `null`: no concluir sobre la realidad del servicio. |
| requested_claims | Categorías de conclusión solicitadas. | Categoría desconocida se rechaza. |

La función `engagement_gate` de [audit_foundation_v1.py](../../tools/audit_foundation_v1.py) determina qué categorías pueden evaluarse con el encargo documentado. No emite una conclusión positiva: después hacen falta ejecución, cobertura y revisión de evidencia. `BLOCKED_CLAIMS` identifica solicitudes sin soporte; los resultados técnicos delimitados pueden seguir comunicándose con sus límites.

Categorías: TECHNICAL_RESULTS, SCHEMA_RESULTS, PROFILE_RESULTS, DESTINATION_SUITABILITY, SERVICE_TRUTH. LEGAL_COMPLIANCE y CERTIFICATION quedan bloqueadas en este contrato técnico. XSD, perfil, uso previsto y realidad del servicio tienen condiciones distintas.

Ejemplos: GTFS interno (evidencia local no publicada) y NeTEx sintético (evidencia local no publicada). El primero delimita una ejecución existente. El segundo es un ejemplo de encargo para un fixture, sin auditoría nueva ni decisión sobre EPIP. Sus gates se guardan en ENGAGEMENT_GATES.json (evidencia local no publicada).

Esta es una capacidad de validación invocable y comprobada por separado; su integración en el intake y en los generadores de ambos formatos pertenece a TDL-AUD-07. Ningún flujo existente queda bloqueado automáticamente por esta implementación.
