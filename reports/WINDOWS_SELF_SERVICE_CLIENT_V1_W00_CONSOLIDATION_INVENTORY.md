# Windows Self-Service Client V1 — inventario de consolidación W00

**Fecha:** 2026-10-05
**Base:** `f53335747562206936e5db7704dfb093844d768e` (`origin/main`)
**Alcance:** consolidar W00-R, W00-O, W00-M y W00-P; W01 queda fuera.

## Clasificación antes del staging

El inventario inicial de la rama contenía 7 archivos modificados y 1.339 rutas no versionadas. Se clasifican por ruta y, para los árboles anidados de evidencia, por cada entrada del [manifiesto de inventario](evidence/windows_client_v1/w00/proposed_cleanup_manifest.json). El manifiesto registra ruta relativa, tamaño y clase; no lee contenidos, calcula hashes masivos ni borra archivos. Su inventario vigente cubre 2.245 archivos locales bajo `reports/evidence/windows_client_v1/w00/` (6.585.941.595 bytes): 11 `MUST_VERSION` (36.011 B), 403 `LOCAL_EVIDENCE_PRESERVE` (118.598.891 B), 534 `REPRODUCIBLE_DO_NOT_VERSION` (269.749.601 B) y 1.297 `SAFE_TO_REMOVE_AFTER_MANIFEST` (6.197.557.092 B).

| Clase | Rutas cubiertas | Decisión |
|---|---|---|
| `MUST_COMMIT` | `gtfs_lab/core.py` (serializer W00-P); `PROJECT_STATUS.md`; `PROJECT_STATUS_TREE.md`; tres informes W00; este inventario; `gtfs_lab/resource_stages.py`; los nueve módulos `tools/` de benchmark, seguridad, semántica, empaquetado y subprocesos; tests de medición/benchmark/serialización; política, manifests y evidencia compacta seleccionada | Incluir de forma explícita y limitada. |
| `SHOULD_COMMIT` | Los marcadores de etapa optativos añadidos en `client_workflow.py`, `ingestion.py`, `pipeline.py` y `test_bank.py` | Incluir porque el harness W00 necesita correlacionar muestras de proceso con etapas. Solo escriben evidencia cuando se configura `TDL_RESOURCE_STAGE_FILE`. |
| `LOCAL_EVIDENCE_PRESERVE` | Fixtures, logs de etapas, preflights, comparaciones intermedias, outputs de auditoría y mediciones completas bajo ambos árboles `.../evidence/windows_client_v1/w00/` | Conservar localmente; solo se publican las pruebas compactas necesarias. |
| `REPRODUCIBLE_DO_NOT_COMMIT` | Árboles completos de auditoría sintética, comparaciones sintéticas intermedias, serializaciones JSON brutas de 35 MB, fixtures ZIP, caches y builds/dist de PyInstaller | Permanecen locales. Las reglas W00 de `.gitignore` excluyen outputs, auditorías empaquetadas, escalas/comparaciones completas, JSON brutos, fixtures ZIP y artefactos `build/dist`; el manifiesto detalla cada ruta. |
| `SAFE_TO_REMOVE_LATER` | Candidatos exactos que el manifiesto clasifica `SAFE_TO_REMOVE_AFTER_MANIFEST` (1.295 archivos; 6.197.555.723 bytes) | No borrar durante este cierre. La clase requiere conservar manifiesto/evidencia y volver a inventariar antes de cualquier limpieza futura. |
| `UNRELATED_DO_NOT_TOUCH` | Ninguna ruta identificada | No se detectaron cambios ajenos a W00 en el inventario inicial. |
| `NEEDS_HUMAN_DECISION` | Ninguna ruta identificada | La decisión humana de W00 ya está dada; hardware mínimo/recomendado y validación limpia siguen pendientes como límites del producto, no como autorización para iniciar W01. |

### Archivos de trabajo identificados

- Modificados inicialmente: `02_Data_Engineering/GTFS_Lab/gtfs_lab/client_workflow.py`, `core.py`, `ingestion.py`, `pipeline.py`, `test_bank.py`, `PROJECT_STATUS.md` y `PROJECT_STATUS_TREE.md`.
- Herramientas nuevas: `benchmark_safety.py`, `build_w00m_evidence_manifest.py`, `build_w00o_closure_evidence.py`, `resource_measurement.py`, `subprocess_feasibility.py`, `subprocess_reclamation_check.py`, `synthetic_resource_benchmark.py`, `synthetic_resource_child.py` y `synthetic_semantic_compare.py` bajo `02_Data_Engineering/GTFS_Lab/tools/`.
- Tests nuevos/consolidados: `test_resource_measurement.py`, `test_synthetic_resource_benchmark.py` y la comprobación de igualdad byte a byte integrada en el test de integración de `test_g08_quality.py` bajo `02_Data_Engineering/GTFS_Lab/tests/`.
- Informes: `WINDOWS_SELF_SERVICE_CLIENT_V1_W00_RUNTIME_RESOURCE_READINESS.md`, `..._W00_M_MEMORY_ROOT_CAUSE_ISOLATION.md`, `..._W00_P_JSON_SERIALIZATION_OPTIMIZATION_PROOF.md` y este inventario bajo `reports/`.

## Instrumentación diagnóstica (C07)

| Cambio | Clase | Tratamiento |
|---|---|---|
| Marcadores en workflow (`INTAKE`, `INTERPRETATION`, `REPLAY`, `REPORT_GENERATION`) | `BENCHMARK_TOOLING_ONLY` | Se conservan; no escriben ni alteran la auditoría cuando `TDL_RESOURCE_STAGE_FILE` no está configurada. |
| Marcadores en ingesta (`ZIP_EXTRACTION`, `INGESTION`) | `BENCHMARK_TOOLING_ONLY` | Se conservan por la misma condición optativa. |
| Marcadores en pipeline (auditoría, preparación/informe, escritura JSON/Markdown y persistencia) | `BENCHMARK_TOOLING_ONLY` | Se conservan para reproducir atribución por etapa con el harness. |
| Marcadores de replay/limpieza en Test Bank | `BENCHMARK_TOOLING_ONLY` | Se conservan para mediciones controladas del flujo completo. |
| Cronometraje y contadores por escritura JSON añadidos durante W00-M | `DIAGNOSTIC_ONLY` | Retirados de `core.write_json`; el camino normal no toma tiempos ni emite métricas. |
| Cambio JSON de `json.dumps` a `JSONEncoder.iterencode` por lotes | `PRODUCTION_USEFUL` | Se conserva como el cambio funcional W00-P validado, sin otra optimización del motor. |

## Evidencia que se publicará

Se seleccionan manifests, resultados compactos y mediciones resumidas para reproducir las conclusiones. No se publican los JSON completos de auditoría, bases DuckDB, ZIP de fixtures, trazas duplicadas ni artefactos `build/dist`. El manifiesto de limpieza mantiene por ruta las propuestas de conservación/eliminación y registra `deletion_performed = false`; los árboles locales no se modificaron ni eliminaron.

**Resultado del staging:** la clasificación se registró antes de stagear; después se seleccionaron rutas exactas de código, tests, tooling, estado, informes y evidencia compacta. No se incluyeron outputs reproducibles, logs brutos, `build` ni `dist`. Queda prohibido `git add .`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
