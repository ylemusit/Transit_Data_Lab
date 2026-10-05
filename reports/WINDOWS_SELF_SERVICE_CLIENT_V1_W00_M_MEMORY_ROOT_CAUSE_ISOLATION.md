# Windows Self-Service Client V1 — W00-M: aislamiento de causa raíz de memoria

**Fecha:** 2026-10-05
**Estado:** `W00M_READY_FOR_HUMAN_REVIEW`
**Clasificación:** `W00M_ROOT_CAUSE_PROBABLE`

## Resultado

La reproducción sintética segura S4 localiza el pico de `REPORT_GENERATION` en la serialización JSON de `run.json`. La evidencia apunta a la representación `g03.header_schema.not_evaluable`, construida durante la auditoría y retenida mientras `json.dumps` materializa la cadena JSON completa. No demuestra que dataset 019 tuviera la misma causa: dataset 019 sigue diferido, no se accedió a HOLDOUT y no se modificó la semántica.

`run.json` ocupó 35.967.578 bytes. El bloque G03 ocupa 35.881.402 bytes (99,76 %); `header_schema.not_evaluable`, 34.722.909 bytes, con 22.040 entradas `CONDITION_UNKNOWN` y cero findings raw. La serialización de `run.json` tardó 0,562621 s y alcanzó 288.591.872 bytes de memoria privada muestreada en el proceso raíz. La escritura tardó 0,054801 s; su pico muestreado fue 177.221.632 bytes. Por tanto, el mecanismo más probable es la coexistencia de la estructura G03 retenida y la cadena JSON temporal, con contribución de la construcción de esa representación. La muestra no prueba el uso exacto de memoria de cada objeto ni extrapola el resultado a 019.

## Descomposición instrumentada

La instrumentación distingue `REPORT_INPUT_PREPARATION`, `JSON_SERIALIZATION`, `JSON_FILE_WRITE`, `MARKDOWN_MODEL_BUILD`, `MARKDOWN_FILE_WRITE`, `ENGINE_JSON_MODEL_BUILD`, `ENGINE_JSON_SERIALIZATION_AND_FILE_WRITE`, `ENGINE_MARKDOWN_MODEL_BUILD`, `ENGINE_MARKDOWN_FILE_WRITE` y `EVIDENCE_REFERENCE_AND_PERSISTENCE_BUILD`. El modelo principal `result` se construye durante `AUDIT`; no existe un constructor separado para `run.json`. No hay etapa de limpieza posterior en esta implementación; se registra como no aplicable, sin añadir una etapa ficticia.

La medición usó el harness de árbol de procesos existente, intervalo de 20 ms, 61 muestras y un proceso raíz sin descendientes en el pico. Se capturaron tiempo, memoria privada y working set del proceso raíz/árbol, subetapa y métricas de filas/salida observables. No se usó trazado de objetos.

## Reproducción y equivalencia

- Fixture determinista S4 ya generado: 4.000 filas `stop_times.txt`, ZIP de 42.441 bytes, SHA-256 `96d34a5d922e5054491b587c67621eb94c821c77b8afec607de3884d139e01e7`.
- Gate sintético previo: PASS. Auditoría: código de retorno 0.
- S1 frente a la base W00-O: comparación semántica PASS en identidad, findings raw, accounting, interpretación, semántica de informe y versiones de contrato. La comparación cubre semántica, no igualdad byte a byte de todos los informes.
- Dataset 019: `DEFERRED`; HOLDOUT: no accedido; `CLEAN_MACHINE_VALIDATION = PENDING`.

Los datos medidos y hashes constan en [memory_root_cause_w00m.json](evidence/windows_client_v1/w00/memory_root_cause_w00m.json), la medición por subetapa en `evidence/windows_client_v1/w00/memory_diag_s4_split/`, y la comparación en `evidence/windows_client_v1/w00/semantic_compare_w00m_s1/semantic_comparison.json`.

## Propuesta, sin optimización

Evaluar `json.dump`/`JSONEncoder.iterencode` hacia el fichero para evitar materializar de una vez la cadena de 34,8 millones de caracteres mientras vive el árbol de G03. No se implementa en W00-M. La reducción real de memoria y el coste de tiempo no están medidos; el tamaño en disco debería mantenerse, pendiente de comprobar igualdad byte a byte. El riesgo semántico se considera bajo, pero no cero hasta hacer comparación exacta y repetir el gate semántico y el benchmark antes/después. El alcance propuesto es únicamente `gtfs_lab.core.write_json`.

## Evidencia generada y limpieza

`FULL_SYNTHETIC_OUTPUTS_VERSIONED = NO`. La política y el inventario propuesto están en [w00_generated_evidence_policy.json](evidence/windows_client_v1/w00/w00_generated_evidence_policy.json) y [proposed_cleanup_manifest.json](evidence/windows_client_v1/w00/proposed_cleanup_manifest.json). El inventario no lee contenidos ni calcula hashes masivos. Se preservan los 2,4 GiB originales; no se borró nada ni se autoriza limpieza recursiva. Se añadió una regla local de Git para evitar incluir accidentalmente los grandes árboles generados al preparar cambios.

## Cierre W00-M

```ini
REPORT_SUBSTAGES_INSTRUMENTED = 10
REPRODUCTION_SCALE = S4
PEAK_SUBSTAGE = JSON_SERIALIZATION
PEAK_MEMORY = 288591872 BYTES PRIVATE; OBSERVED_SAMPLED
ROOT_CAUSE = PROBABLE: G03 ROW EVIDENCE RETAINED + FULL JSON STRING MATERIALIZATION
EVIDENCE_STRENGTH = PROBABLE
OPTIMIZATION_RECOMMENDED = CHUNKED JSON WRITING; PROPOSAL ONLY
ESTIMATED_SEMANTIC_RISK = LOW_BUT_NOT_ZERO_PENDING_BYTE_AND_SEMANTIC_COMPARISON
FULL_SYNTHETIC_OUTPUTS_VERSIONED = NO
EVIDENCE_POLICY = PASS
DATASET_019 = DEFERRED
CLEAN_MACHINE_VALIDATION = PENDING
FUNCTIONAL_ENGINE_CHANGED = YES (DIAGNOSTIC INSTRUMENTATION ONLY)
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
W01 = BLOCKED
STOP = W00M_READY_FOR_HUMAN_REVIEW
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
