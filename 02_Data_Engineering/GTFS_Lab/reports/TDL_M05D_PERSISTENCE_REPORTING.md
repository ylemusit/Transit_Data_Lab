# TDL Trust Foundation M05-D — Persistence and reporting

**Estado:** `M05D_PERSISTENCE_REPORTING_READY_FOR_REVIEW` sujeto a regresiones y revisión del cambio.
**Base:** `9a54144f51c16cfaa4d5dc8cecbdfe2149cb1c65`.
**Alcance:** persistencia aditiva de resultados M05-B; no ejecuta audits ni escribe bases.

## Contrato y almacenamiento

`AuditComparisonRecord 1.0.0` envuelve el resultado `ChangeAttribution 1.0.0` y versiones de snapshot existentes. Guarda IDs de auditoría, referencias, causas, diferencias, estado de evidencia y razones no resueltas. No copia los runs.

La API `persist_comparison(directory, baseline, candidate, source_artifacts=...)` escribe en `reports/evidence/comparisons/<comparison_id>/comparison.json` y `report.md`. El ID existente deriva del par de audit IDs. Una escritura JSON temporal se sincroniza y se instala con creación exclusiva; un payload distinto para el mismo par falla con `COMPARISON_RECORD_CONFLICT`. Una repetición idéntica conserva la hora inicial y los mismos bytes. Errores explícitos: `COMPARISON_RECORD_CONFLICT`, `COMPARISON_HASH_MISMATCH`, `EVIDENCE_REFERENCE_INVALID` y `WRITE_FAILED`.

Serialización canónica: JSON UTF-8, `ensure_ascii=false`, claves ordenadas, separadores compactos, LF y LF terminal. SHA-256 cubre ambos snapshots canónicos, el payload canónico y todos los campos del registro fuera de `integrity` mediante `record_sha256`, incluido el timestamp. `verify_comparison_record` verifica los cuatro hashes.

## Informe

El Markdown determinista separa comparabilidad, atribución/causas, resultado, findings nuevos/resueltos/modificados, causas no resueltas, referencias y versiones de contrato. Las etiquetas de causa y consecuencia siguen separadas conforme a M05-A; no se interpreta el resultado comercial o jurídico.

## CLI y prueba de integración

`python -m gtfs_lab.audit_comparison <baseline-run-dir> <candidate-run-dir> --persist <evidence-root>` imprime el resultado y persiste JSON e informe. Sin `--persist` continúa en modo de solo lectura.

La prueba de pipeline en `tests/test_audit_comparison.py` genera dos runs aislados mediante los fixtures ya usados por GTFS_Lab, compara sus artifacts persistidos M01/M02 y confirma JSON y Markdown. La matriz PD-001…PD-011 cubre NO_CHANGE, dataset, implementación, causas múltiples, no comparable, no atribuido, repetición, conflicto, Markdown estable, referencias y hashes.

`tools/persist_m05d_productive_proof.py` ejecuta una vez dos fixtures mediante el pipeline real y conserva solo los cuatro JSON M01/M02 que requiere `build_audit_snapshot` por lado en `reports/evidence/m05d_productive_sources/`. La comparación `CA-20dd6212be68afda` queda guardada con referencias estables en `reports/evidence/comparisons/`. Su atribución es `DATASET_CHANGE`, con cambio del conjunto de findings. Una segunda invocación reutiliza las fuentes guardadas y es idempotente.

## Prueba histórica M05-C

`tools/persist_m05c_historical_proof.py` adapta el resumen persistido ya existente en `reports/evidence/m05c_historical_proof/summary.json`. Escribe una referencia compacta en `reports/evidence/comparisons/M05C-HISTORICAL-PROOF-V1/` con punteros, hashes de los resúmenes M04 B1/B3 y clasificación guardada. Los hashes de snapshot corresponden al adaptador compacto `M05CHistoricalSourceSnapshot 1.0.0`; los SHA-256 de los archivos M04 originales quedan en `comparison.source_sha256`. `verify_historical_record` comprueba ambos niveles y el resumen M05-C sin ejecutar HOLDOUT ni modificar los archivos M04/M05-C originales.

Los resultados históricos siguen siendo los del informe M05-C; las identidades faltantes y evidencia parcial permanecen explícitas. Este artefacto prueba lectura y persistencia del adaptador histórico; no revalida el análisis subyacente.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
