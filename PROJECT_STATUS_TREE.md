# Transit Data Lab — mapa de estado GTFS Audit Engine V1

**Fuente vigente:** [PROJECT_STATUS.md](PROJECT_STATUS.md), sección «remediación G08–G11».

```text
GTFS AUDIT ENGINE V1 — PREPARACIÓN PARA DECISIÓN FINAL
│
├── G01–G03                               ✅ CERRADOS E INTEGRADOS
├── G04–G07                               ✅ CERRADOS EN CHECKPOINTS ANTERIORES
│   └── Corrección de consumo G03 CSV      🔧 Local; CI/merge post-corrección pendientes
├── G08 Quality                           ✅ Criterios técnicos PASS; cierre registrado en rama
├── G09 Reporting                         ✅ Criterios técnicos PASS; M02 sin cambios
├── G10 DEVELOPMENT                       ✅ Replay local 14/14; 0 errores; estabilidad PASS
├── G10 atribución                        ✅ Por regla/dataset/archivo/campo/causa
├── G11 revisión técnica                  ✅ PASS local; integración y post-merge pendientes
├── Engine V1                             ⏳ READY_FOR_FINAL_HUMAN_CLOSURE_DECISION tras integrar
└── HOLDOUT                               🔒 NOT_ACCESSED
```

## Checkpoint integrado PR #28

- Merge commit / `origin/main` observado: `07bd0beaaf158718430ee53a5001e5f01655dac7`.
- Head revisado: `af8c9b157fd52b0e4b5a753dcc0813272f4e06c8`; CI PASS run `36804031563`; post-merge CI PASS run `36804060651`.
- El replay G10 descubrió que G03 emite `files_inspected` y sus consumidores G04–G07 buscaban `inspected`. La corrección y las regresiones están pendientes de integrar.
- HOLDOUT no accedido; M02 sin cambios; sin código específico por operador.

## Límites

- Los cierres G04–G07 anteriores conservan su evidencia histórica; la corrección actual actualiza su consumo de evidencia y todavía no está integrada.
- El estado técnico no implica cumplimiento GTFS completo, jurídico o comercial.
- G04 conserva la deuda de inventario `CREATED_LOCAL_UNPUBLISHED`; legacy y M02 conservan sus fronteras.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
