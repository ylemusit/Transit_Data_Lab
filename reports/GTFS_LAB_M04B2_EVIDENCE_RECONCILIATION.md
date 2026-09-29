# M04-B2 clean integration — evidence reconciliation

Fecha: 2026-09-29
Base: `8d4f2ad7fa0545b76dd5d5ec5503890ed0c396d9`
Fuente aprobada: PR #9, head `699f1299df2961519e4e566a8064448104e03adf`
Rama limpia: `feat/tdl-trust-foundation-m04b2-clean`

## Inventario y clasificación de PR #9

Inventario completo: 332 rutas cambiadas según la API de archivos del PR. La clasificación es exhaustiva y no solapada: las listas explícitas de fuentes, tests, informes, contratos y evidencia de abajo, más las reglas de prefijo de artefactos, asignan exactamente una categoría a cada ruta. `HISTORICAL_PROTECTED_REFERENCE` y `NEEDS_REVIEW` tienen cero entradas.

| Categoría | Archivos |
| --- | ---: |
| `CANONICAL_SOURCE` | 5 |
| `CANONICAL_TEST` | 2 |
| `CANONICAL_CONTRACT` | 3 |
| `CANONICAL_REPORT` | 5 |
| `CANONICAL_EVIDENCE` | 3 |
| `REPRODUCIBLE_EXECUTION_ARTIFACT` | 267 |
| `REDUNDANT_INTERMEDIATE` | 47 |
| `HISTORICAL_PROTECTED_REFERENCE` | 0 |
| `NEEDS_REVIEW` | 0 |
| **Total PR #9** | **332** |

Reglas para las 315 rutas clasificadas por prefijo: los 264 ficheros bajo `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2d_regression/` y estos tres resúmenes reproducibles de `m04b2a_transition_20260929/` son `REPRODUCIBLE_EXECUTION_ARTIFACT`: `GTFS_Lab_synthetic/gate.json`, `Golden_regression/golden_regression_gate.json` y `M02_trust/gate.json`. Los 33 ficheros restantes bajo `03_Compliance/reports/evidence/compliance_v1_20260929/` y los 14 de `m04b2_development_triage_20260929/` son `REDUNDANT_INTERMEDIATE`; se conserva únicamente `current_gate_m04b2d_final4/summary.json` como resumen del gate estricto vinculado a la aprobación. Estos prefijos cubren todas las rutas de evidencia restantes sin excepciones.

## Estado limpio y archivos conservados

El PR limpio contiene 19 archivos: los 18 canónicos que siguen y este informe de reconciliación.

- `CANONICAL_SOURCE` (5): `02_Data_Engineering/GTFS_Lab/gtfs_lab/compliance_adapter.py`, `02_Data_Engineering/GTFS_Lab/gtfs_lab/ingestion.py`, `tools/compliance_v1_current_gate.py`, `tools/compliance_v1_engine.py`, `tools/compliance_v1_transition_candidate.py`.
- `CANONICAL_TEST` (2): `02_Data_Engineering/GTFS_Lab/tests/test_compliance_v1_transition.py`, `02_Data_Engineering/GTFS_Lab/tests/test_m04b2_synthetic_triage.py`.
- `CANONICAL_REPORT` (5): `02_Data_Engineering/GTFS_Lab/README.md`, `02_Data_Engineering/GTFS_Lab/reports/GTFS_LAB_M04B2_DEVELOPMENT_TRIAGE.md`, `03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md`, `PROJECT_STATUS.md`, `reports/GTFS_LAB_M04B2A_COMPLIANCE_PACKAGE_TRANSITION.md`.
- `CANONICAL_CONTRACT` (3): `03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final/package_candidate.json`, `03_Compliance/reports/evidence/compliance_v1_20260929_transition_candidate_final/transition_manifest.json`, `03_Compliance/reports/evidence/compliance_v1_current_implementation_v2.json`.
- `CANONICAL_EVIDENCE` (3): `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/compliance_transition_evidence.json`, `02_Data_Engineering/GTFS_Lab/reports/evidence/m04b2a_transition_20260929/historical_package_replay.json`, `03_Compliance/reports/evidence/compliance_v1_20260929/current_gate_m04b2d_final4/summary.json`.

Se excluyen 314 rutas: 267 salidas de ejecución reproducibles y 47 intermedios redundantes. Los gates y tests generan de nuevo los escenarios y resultados sintéticos; IDs de ejecución y marcas temporales pueden variar, pero las aserciones, identidades y resultados comprobados no dependen de conservar esos directorios. Los ZIP sintéticos, feeds extraídos, runs, GeoJSON/KML, logs, snapshots repetidos y bases temporales no respaldan ninguna afirmación exclusiva. La DB Compliance protegida se conserva fuera del commit.

## Identidad, aprobación y protección

Comparación contra PR #9 head: estado funcional idéntico. Identidades comprobadas en la rama limpia: regla `V1-RULE-GTFS`; regla `compliance-v1/1`; evaluator `compliance-v1/2`, SHA-256 `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; parser `gtfs-lab-csv/2`; paquete actual SHA-256 `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`.

La aprobación existente permanece byte-identificada en el manifiesto: Yeison Arbey Carrillo Lemus, `APPROVE`, `2026-09-29T16:18:55Z`, transición `COMPLIANCE_V1_IMPLEMENTATION_TRANSITION_V1_TO_V2`. No se emitió una aprobación humana nueva.

| Referencia protegida | SHA-256 comprobado |
| --- | --- |
| Paquete histórico | `2f85c9bd92ad603bab696e34c886b3f85ac22c05ba7aa0e90dc10137bb061981` |
| Evaluator histórico | `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70` |
| Freeze histórico | `3BBB6D87500608364972CFE841D6B2D3D03558FC73F1960A28579905FAEC6A3E` |
| DB Compliance | `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` |
| Golden Corpus y split | Identidades registradas sin cambio: `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3` y `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d` |
| M04-B1 | Árbol versionado idéntico a la base; cero diferencias |

HOLDOUT V2: no ejecutado ni accedido. No se abrió, leyó, extrajo ni hasheó ningún ZIP HOLDOUT.

## Gates ejecutados en la rama limpia

Todos PASS: M01, M02, M03-A, Golden Corpus, Golden Evaluator, Golden Regression, split, lineage, GTFS_Lab sintético/actual, replay histórico, replay del paquete v2, Compliance V1 strict current gate, diferencial semántico 28/28, fixtures ampliados 2/2, tests completos GTFS_Lab 52/52, `compileall` y `git diff --check`.

El gate estricto devolvió `PASS`; DB Compliance inicial y final: `4DB39FA5…048B`. Phase 1: 22/22 PASS. Phase 2: 386 PASS y el mismatch histórico documentado `UNCHANGED_COUNT_audit.rules` (0 esperado, 2 actual) preservado. No se relajó el contrato.

## Integración

El PR #9 continúa como registro histórico y no se ha fusionado. Esta rama parte exactamente de la base indicada, sin cherry-pick de commits del PR #9. El PR limpio se abrirá como draft tras commit y verificación de mergeabilidad. No se hizo merge. Veredicto previsto tras esa verificación: `M04B2_CLEAN_INTEGRATION_READY_FOR_MERGE`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.\n