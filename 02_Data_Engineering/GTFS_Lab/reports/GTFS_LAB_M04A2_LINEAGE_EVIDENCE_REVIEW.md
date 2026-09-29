# M04-A2 — revisión de evidencia de lineage

**Estado:** `M04A_LINEAGE_MATRIX_READY_FOR_SPLIT_DESIGN`
**Base:** M04-A1 HEAD `3657fa279f00162eee4ad7a448df2c530bfdbe89`
**Split / holdout:** no creados; M04-B no iniciado.
**Alcance:** 29 pares registrados en `corpus/relationships_v1.json`; evaluación metadata-visible de identidad, ZIP y tablas GTFS, sin consultar findings del motor.

## A. Modelo revisado de evidencia

- `strong`: hash ZIP idéntico, mismo source dataset/resource URL, identidad de operador corroborada o coincidencia sustancial de trips e identidades.
- `supporting`: publisher/URL, agencia, rutas, paradas o trips coincidentes; por sí solos no prueban origen común.
- `network_identifier_signals`: IDs de agency/route/stop dentro del scope del feed; identificadores genéricos o paradas físicas no bastan para inferir lineage.
- La independencia positiva converge identidad declarada distinta, ZIP distinto, publishers/URLs distintos cuando están disponibles, ausencia de trips comunes y ausencia de identidad común de ruta/parada. `UNKNOWN` no se interpreta como evidencia positiva.

## B. Colisiones genéricas

Se detecta `GENERIC_ID_COLLISION` contextualmente: colisión pequeña de IDs sin nombres, trips u otra identidad compartida sustancial. No se usa una allowlist de IDs como decisión de lineage. Casos: agency_id `1` en la familia B; stop_id único `SALAMANCA` (002–005); pares con uno o dos IDs de parada sin identidad nominal. Todos están separados de `SOURCE_LINEAGE`.

## C. Reclasificación de los 29 pares

| Par | Assessment | Domain | Confianza | Lados opuestos | Motivo resumido |
|---|---|---|---|---|---|
| 002-005 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-010 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-012 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-013 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-014 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-015 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-017 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 008-018 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 009-019 | `LIKELY_INDEPENDENT_SOURCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage. |
| 010-012 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 010-013 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 010-014 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 010-015 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 011-016 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 011-017 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 011-018 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 011-019 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 012-013 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 012-014 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 012-015 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 013-014 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 013-015 | `LIKELY_SAME_LINEAGE` | `SOURCE_LINEAGE` | HIGH | **NO** | A shared operator/source is corroborated by substantial feed identity or trip evidence. |
| 014-015 | `NO_LINEAGE_EVIDENCE` | `IDENTIFIER_COLLISION` | MEDIUM | **YES** | Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage. |
| 016-017 | `LIKELY_INDEPENDENT_SOURCE` | `NONE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 016-018 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 016-019 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 017-018 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 017-019 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |
| 018-019 | `LIKELY_INDEPENDENT_SOURCE` | `NETWORK_STRUCTURE` | HIGH | **YES** | Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only. |

La matriz estructurada completa —incluidos `lineage_signals`, colisiones de red, diferencias de identidad, trips/rutas/nombres y razonamiento— está en [`lineage_review_m04a2.json`](../corpus/lineage_review_m04a2.json).

## D. Resultado revisado 016–019

Los seis pares no comparten agency IDs ni trips. Tampoco comparten nombres de paradas/rutas en la comparación preservada. Los operadores y publishers/URLs son distintos: ALU/Autobuses La Unión, Tuvisa, Bilbobus y Bizkaibus/Lantik. Los pares comparten stop IDs en cuatro combinaciones y route IDs en 017–018, pero sus URLs/versiones/rangos de feed difieren cuando están declarados. Los stop IDs compartidos se clasifican `NETWORK_STRUCTURE`; 016–017 queda `NONE`. Los seis pares reciben `LIKELY_INDEPENDENT_SOURCE / YES`, con evidencia convergente y sin inferir capture dates desde el nombre ZIP.

## E. Conteos

- YES: **28**
- NO: **1**
- UNRESOLVED: **0**

## F. Pares bloqueantes

**013–015**: `LIKELY_SAME_LINEAGE / SOURCE_LINEAGE / HIGH / NO`. Los ZIP contienen una coincidencia sustancial de identidad y estructura (129 route IDs, 54 nombres de rutas, 491 stop IDs, 504 nombres de parada y 543 trip IDs compartidos según la comparación previa). El par debe permanecer agrupado en cualquier diseño posterior.

## G. Preguntas restantes al custodio

Ninguna pregunta de custodia bloquea la matriz revisada. Las preguntas generales de M04-A1 sobre IDs/URLs NAP y semántica de timestamps no son necesarias para resolver los pares actuales: la evidencia de independencia convergente decide 28, y la coincidencia sustancial decide 013–015. Si aparece evidencia nueva de un source ID o de un feed derivado, deberá reabrirse la matriz antes de asignar split.

## H. Gates y regresión

La matriz añade gate sintético para agency_id genérico `1`, stop_id `SALAMANCA`, misma fuente/hash y stops de red con publishers y operadores distintos. El split gate consulta la decisión de lineage: bloquea `NO` y `UNRESOLVED`, permite `YES`, y no bloquea por IDs GTFS compartidos por sí solos.

Regresión: M01 PASS (12 checks); M02 Trust Persistence PASS; M03-A Contract PASS; Golden Corpus PASS (2 casos, SHA `29ae937e…dce1e3`); Golden Evaluator PASS (11 checks); Golden Regression PASS (2 casos); GTFS_Lab V1 PASS; Compliance V1 PASS (hash antes/después `4DB39FA5…BC8048B`, 386 checks Phase 2 actuales y 1 fallo histórico permitido `UNCHANGED_COUNT_audit.rules`); M04 tests PASS (15/15); M04 provenance gate PASS (20 datasets, 29 pares; verificado con los ZIP del checkout raíz); py_compile PASS; `git diff --check` PASS. Golden assets no cambiaron. Golden assets no cambiaron.

## I. HEAD y PR

- HEAD inicial: `3657fa279f00162eee4ad7a448df2c530bfdbe89`.
- PR [#7 — feat(trust): define development and holdout split M04](https://github.com/ylemusit/Transit_Data_Lab/pull/7): Draft abierto; actualizar su descripción con este resultado.
- HEAD final y estado remoto se registrarán tras publicar la actualización autorizada.

## J. Veredicto

`M04A_LINEAGE_MATRIX_READY_FOR_SPLIT_DESIGN`. Este veredicto solo indica que la matriz de lineage permite iniciar un diseño de split. No crea `split_v1.json`, no asigna datasets y no abre el holdout.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
