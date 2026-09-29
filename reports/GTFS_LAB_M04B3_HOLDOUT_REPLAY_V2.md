# TDL Trust Foundation — M04-B3 Controlled HOLDOUT Replay V2

**Evaluation:** `TDL-M04B3-V2-1564c27f9de8415e96e6998ee129db03`
**Access:** `TDL-HOLDOUT-ACCESS-6a42ecc422ea46fabdd8c88e4899c44c`
**Fecha:** 2026-09-29
**Estado:** `M04B3_HOLDOUT_V2_COMPLETED`

## A. Authorization and frozen identity

Ejecución autorizada sobre el commit `08cf344750f44a1527b261a15074afa1c40fb35a`, igual a `origin/main` al inicio, en worktree aislado. El worktree estaba limpio antes del acceso. Checkpoint `TDL_HOLDOUT_ENGINE_CHECKPOINT_V2`, SHA-256 `CEEEC24A72211DD0F0B59A663C3AF34C3697820FEACA015384DFDF534392C978`; identidad de motor preservada en el commit `6a4afd4663f7a3ef4b8ae6560cfa314e137c3a72`. Parser `gtfs-lab-csv/2`; validator `1.0.0`; reglas `gtfs-lab-v1/1`; regla semántica `V1-RULE-GTFS / compliance-v1/1`; evaluator `compliance-v1/2`, SHA `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; paquete `8633fe32cf081e8b43a0a176088966aa5941d7b2d3a63e57d6668d70e49a9c9b`. Split `TDL-CORPUS-SPLIT-V1 / 1.0.0`, SHA canónico `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d`.

## B. Access chronology

Registro previo persistido `2026-09-29T17:28:58.5629445Z`, antes de cualquier ZIP. Primera resolución fallida de la ruta del inventario bajo `corpus/`: `2026-09-29T17:29:59.58001Z`; no leyó bytes y se conserva. La ruta correcta se resolvió bajo `20_clientes_reales`. **La hora UTC exacta de las seis lecturas SHA-256 iniciales no quedó capturada** por un error en la expresión temporal de PowerShell. Los timestamps permanecen nulos; no se han reconstruido ni repetido los hashes. El pipeline abrió el primer ZIP a las `2026-09-29T17:32:27.1809298Z`; la sexta ejecución terminó a las `2026-09-29T17:32:34.6521520Z`. Los artefactos externos registran una sola invocación por dataset. Esta limitación de trazabilidad queda expuesta para revisión humana.

## C. Source identity

Los seis hashes coinciden con el split aprobado. Identidades y rutas lógicas están en `reports/evidence/holdout_evaluation_v2/source_identity.json`. Orden autorizado: 006, 008, 013, 015, 017 y 018. La primera resolución fallida queda en `access_record.json`.

## D. Dataset outcomes

| ID | Unidad lineage | Pipeline V1 | Pipeline V2 | Compliance V1 | Compliance V2 | Hallazgos V1 | Hallazgos V2 | Atribución |
|---|---|---|---|---|---|---:|---:|---|
| 006 | DATASET-006 | PIPELINE_COMPLETED | PIPELINE_COMPLETED | PASS | PASS | 0 | 0 | NO_CHANGE |
| 008 | DATASET-008 | PIPELINE_FAILED | PIPELINE_COMPLETED | NOT_RUN | PASS | None | 0 | PARSER_IMPLEMENTATION_CHANGE; downstream rule results are newly observable after ingestion |
| 013 | LINEAGE-013-015 | PIPELINE_COMPLETED | PIPELINE_COMPLETED | INSPECTION_ERROR | PASS | 0 | 0 | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE |
| 015 | LINEAGE-013-015 | PIPELINE_COMPLETED | PIPELINE_COMPLETED | INSPECTION_ERROR | PASS | 0 | 0 | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE |
| 017 | DATASET-017 | PIPELINE_COMPLETED | PIPELINE_COMPLETED | INSPECTION_ERROR | PASS | 0 | 0 | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE |
| 018 | DATASET-018 | PIPELINE_COMPLETED | PIPELINE_COMPLETED | INSPECTION_ERROR | PASS | 0 | 0 | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE |

Los seis pipelines completaron con ingestión, integridad, análisis, GIS, DuckDB y manifiesto Trust `ACCEPTED`. Los 48 resultados de reglas V2 fueron `PASS`; cero `FAIL_TECHNICAL`, cero hallazgos y cero errores de inspección.

## E. Lineage outcomes

Cinco unidades independientes: `DATASET-006`, `DATASET-008`, `LINEAGE-013-015`, `DATASET-017`, `DATASET-018`. Las seis ejecuciones son interpretables; 013 y 015 se conservan como resultados separados y cuentan como una unidad lineage.

## F. Dataset 008 comparison

V1 terminó `PIPELINE_FAILED` al rechazar el registro vacío físico de `shapes.txt`, registro 1869, antes de ejecutar reglas. V2 completó con `EMPTY_CSV_RECORD_IGNORED table=shapes.txt lines=1869 count=1`; las líneas y el conteo quedaron en warning de ingestión y el manifiesto Trust fue aceptado. Las ocho reglas, incluida Compliance, dieron PASS. Atribución de ingestión: `PARSER_IMPLEMENTATION_CHANGE`; resultados downstream: `NEWLY_OBSERVABLE_DATA_RESULT`.

## G. Scale-limit datasets comparison

013, 015, 017 y 018 tenían siete reglas locales PASS y Compliance `INSPECTION_ERROR` por `SCALE_LIMIT` en V1. V2 completó las ocho reglas con Compliance PASS en los cuatro casos bajo el evaluator incremental aprobado. No aparecieron hallazgos técnicos. Atribución: `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE`.

## H. Dataset 006 stability comparison

El control 006 conserva pipeline completado, ocho reglas PASS y cero hallazgos. Solo cambian las identidades de parser/evaluator fijadas por V2. Atribución `NO_CHANGE` en resultado semántico.

## I. Rule-result comparison V1/V2

V1: 36 PASS, 4 `INSPECTION_ERROR`; dataset 008 no alcanzó reglas. V2: 48 PASS y ningún error. Los siete resultados GTFS_Lab locales de cada dataset evaluable permanecieron PASS. En 008 V1 no hay resultados comparables porque la ingestión impidió ejecutar reglas. Parser: `gtfs-lab-csv/1` → `gtfs-lab-csv/2`. Evaluator Compliance: V1 SHA `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70` → V2 SHA `60ce250684f97e25d77bbe031055b3b458d2a013497b4076989aa7c30ea521eb`; regla semántica no cambió. B1 no persistió listas de warnings por dataset, así que la comparación de warnings V1/V2 no está disponible; el warning V2 observado fue el de 008 descrito arriba.

## J. Findings

No hubo resultados nuevos `FAIL_TECHNICAL`; no se inicia ciclo de finding de operador. Hallazgos persistidos V1/V2: cero. No hay base para declarar defectos del operador.

## K. Inspection errors

V1: límites de inspección en 013/015/017/018; no son findings. V2: cero `INSPECTION_ERROR`; no se alcanzó el guard de recursos.

## L. Change attribution

006 `NO_CHANGE`; 008 `PARSER_IMPLEMENTATION_CHANGE` y resultados downstream nuevamente observables; 013/015/017/018 `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE`. Sin `TOOL_DEFECT` observado.

## M. Reproducibility evidence

V2 se ejecutó una vez por dataset con `python -m gtfs_lab.cli <fuente autorizada> --output <runtime externo>`. IDs de run y artefactos persistentes figuran en `evaluation_summary.json`; runtime completo fuera del repositorio en `TDL_HOLDOUT_EVALUATION_V2/runtime`. Los seis manifiestos son `1.1.2`, aceptados y ligados a los SHA verificados.

## N. Regression

M01 Trust Contract, M02 Trust Persistence, M03-A Golden Contract, Golden Corpus, Golden Evaluator, Golden Regression, split, lineage, GTFS_Lab synthetic/current, Compliance strict current, compileall y `git diff --check`: PASS. La primera invocación Compliance strict current se detuvo antes de evaluar al faltar la GTFS DB protegida en el worktree. Se verificó su SHA `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`, se copió sin cambios y la segunda invocación pasó. Se conserva el histórico `UNCHANGED_COUNT_audit.rules` (esperado 0, actual 2), separado de los 386 checks actuales PASS.

## O. Protected integrity

Checkpoint, evaluator, paquete Compliance, split canónico, Golden Corpus canónico, Compliance DB y GTFS DB coinciden con sus hashes protegidos. La Compliance DB fue `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` antes y después del gate. Parser y evaluator coinciden con el commit de trabajo. B1 no se modificó. Sin cambios de código, reglas, umbrales, paquete ni split tras abrir HOLDOUT.

## P. M04 conclusion candidate

`M04B3_HOLDOUT_V2_COMPLETED`; seis datasets y cinco unidades lineage con estado terminal e interpretable. `M04_READY_FOR_HUMAN_CLOSURE_REVIEW`. No se declara M04 completo. El revisor humano deberá considerar la limitación registrada de timestamps exactos para los hashes iniciales antes de la decisión de cierre.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
