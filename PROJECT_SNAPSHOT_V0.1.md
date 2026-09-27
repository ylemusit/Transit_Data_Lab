# Transit Data Lab baseline v0.1 — preparado, BLOCKED

Fecha: 2026-09-27. Rama: main. Snapshot objetivo: primer commit raíz formal y etiqueta local anotada tdl-baseline-v0.1. Estado real: no staging, commit ni etiqueta por SECRET_BLOCKER = YES. Este documento no es evidencia de un snapshot ya creado.

## Alcance

Consolidación de gobierno y revisión de organización, sin desarrollo, investigación, migración, regeneración o contacto externo. Fuentes, documentación, evidencia seleccionada y PDF legales; repos anidados independientes. Conclusiones congeladas intactas.

## Estado conservado

GTFS raw implementado e integrity baseline frozen; GIS funcional con reproducibilidad pendiente; core, validation y analysis pendientes. Compliance Phase 1 y 2 FROZEN: 92 provisions, 36 source facts, 48 requirements y 10 deadlines. Gates 1/2 CLOSED; materialization, freeze review y promotion PASS según evidencia persistida. Business V1 FROZEN, Phase 3 IN_PROGRESS, market evidence/readiness documentales PASS; ninguna validación comercial. PROB-001 candidato, autorización pendiente y gate Stage 1 no alcanzado según registro posterior.

- GTFS raw: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance Phase 1 histórico: `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`.
- Compliance Phase 2 actual: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.
- Business V1 agregado: `5e0635956f40c6fbf27d6c6b16fcac8d4762f3fc1c93793d628c7df24dea30c2`.

## Límites

GTFS core, validation y analysis pendientes; GIS funcional sin pipeline plenamente reproducible. Compliance: fidelidad textual no certificada, cumplimiento jurídico no evaluado, mapping no completado, reglas de auditoría no creadas, anomalías Annex 1.3 B-I/D-I y siete dependencias PARTIAL. Tres rutas absolutas en la base se conservan. Business: MARKET_VALIDATED = NO, DEMAND_VALIDATED = NO, WILLINGNESS_TO_PAY = NO, DIFFERENTIATION = UNPROVEN. No discovery, Compliance Phase 3 ni Phase 4 iniciados por esta tarea.

## Exclusiones y recuperación

Bases/WAL, datos raw/original/extracted, backups, cachés, entornos y grandes generados se conservan fuera de Git. No convertir repos anidados a submódulos ni absorber sus árboles. Ver REPOSITORY_POLICY.md, PROJECT_STRUCTURE.md, BACKUP_AND_RECOVERY.md y reports/repository_integrity/FIRST_FORMAL_COMMIT_AUDIT.md. La identidad inmutable será el commit cuando llegue a existir; no insertar su SHA posteriormente en este documento ni crear un bucle de commits.


Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
