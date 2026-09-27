# Estructura lógica y estado

Fecha: 2026-09-27. Manifest de componentes; no inventario exhaustivo de datasets. Estado vigente: [PROJECT_STATUS.md](PROJECT_STATUS.md). Los directorios vacíos son estructuras locales planificadas y no se conservarán en un checkout Git.

| Componente | Ubicación | Estado y clasificación |
| --- | --- | --- |
| Research & Standards | 01_Research_Standards | NON_GIT_DIRECTORY; estructura vacía, planificada, CORRECTLY_LOCATED |
| Data Engineering | 02_Data_Engineering/GTFS_Lab | ROOT_TRACKED_AREA; raw implementado, integrity baseline frozen; core/validation/analysis pendientes |
| GTFS-RT, NeTEx, SIRI | 02_Data_Engineering/*_Lab | NON_GIT_DIRECTORY; estructura planificada sin implementación |
| Compliance | 03_Compliance | ROOT_TRACKED_AREA; Phase 1 y 2 FROZEN, requisitos 48, source facts 36, provisions 92, deadlines 10 |
| Interoperability | 04_Interoperability | NON_GIT_DIRECTORY; estructura vacía, mappings pendientes |
| Audits | 05_Audits | NON_GIT_DIRECTORY; estructura vacía |
| Products | 06_Products/GTFS Explorer | Contenedor NON_GIT_DIRECTORY de repos independientes y backups |
| Business | 07_Business | ROOT_TRACKED_AREA; V1 FROZEN; Phase 3 IN_PROGRESS; evidencia/readiness PASS documentales |
| Gobierno raíz | raíz y reports/repository_integrity | ROOT_REPOSITORY; documentación y revisión de consolidación |

ROOT_TRACKED_AREA significa que sus fuentes/documentos pertenecen al Git padre, con los datos excluidos según .gitignore. NON_GIT_DIRECTORY identifica un directorio sin repositorio propio, no una ausencia de versionado de sus descendientes. Desktop mantiene su identidad de producto y baseline 0.2.2 dentro de Transit Data Lab.

- `06_Products/GTFS Explorer/GTFS Explorer Artifacts`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Desktop`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Engineering`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.

## Organización conservada

CORRECTLY_LOCATED: SQL, scripts, corpus jurídico, requisitos, Business y gobierno. LEGACY_BUT_VALID: auditoría de 20 operadores bajo GTFS_Lab/20_clientes_reales; referencias anteriores a la reestructuración. DUPLICATE documentado históricamente: main.stops y ZIP/manifests Bizkaibus run_001/run_002; no nueva comparación binaria ni borrado. TEMPORARY: cachés, temp, entornos y artefactos generados excluidos. MISPLACED: ninguno que justifique mover automáticamente. UNKNOWN: finalidad de main.stops y reproducibilidad integral GIS; se preservan.

## Business y gates

36 evidencias aceptadas, diez problemas, ocho casos de procurement, once capacidades EXISTING y cuatro gaps potenciales; PROB-001 es el candidato documental. BUSINESS_PHASE_3_MARKET_EVIDENCE y BUSINESS_PHASE_3_VALIDATION_READINESS = PASS. READY_FOR_CUSTOMER_DISCOVERY = YES solo en el sentido del gate documental previo para solicitar autorización. El gobierno posterior de Stage 1 sigue INCOMPLETE, S1-EXIT-09 INSUFFICIENT_EVIDENCE, STAGE_1_GATE NOT_REACHED; Stage 2 no autorizado. Son evaluaciones diferentes, no equivalen a autorización de ejecutar discovery.

GTFS core, validation y analysis pendientes; GIS funcional sin pipeline plenamente reproducible. Compliance: fidelidad textual no certificada, cumplimiento jurídico no evaluado, mapping no completado, reglas de auditoría no creadas, anomalías Annex 1.3 B-I/D-I y siete dependencias PARTIAL. Tres rutas absolutas en la base se conservan. Business: MARKET_VALIDATED = NO, DEMAND_VALIDATED = NO, WILLINGNESS_TO_PAY = NO, DIFFERENTIATION = UNPROVEN. No discovery, Compliance Phase 3 ni Phase 4 iniciados por esta tarea.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
