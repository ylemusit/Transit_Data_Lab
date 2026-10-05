# Windows Self-Service Client V1 — W00-P: prueba de optimización JSON

**Estado:** `W00P_READY_FOR_HUMAN_REVIEW`
**Decisión técnica:** `W00P_PASS_WITH_RESOURCE_LIMITATION`
**Base:** `f53335747562206936e5db7704dfb093844d768e` (`origin/main`; rama W00 específica)
**Alcance:** `gtfs_lab.core.write_json`; W01 no iniciado.

## P01–P04 — Serialización y equivalencia

Antes: `json.dumps(data, ensure_ascii=False, indent=2) + "\n"`; UTF-8; indentación 2; separadores por defecto del encoder indentado (coma + salto/indentación, dos puntos + espacio); `ensure_ascii=False`; `sort_keys=False`; modo texto create/truncate con permisos observados `0666` en Windows, sujetos a permisos del sistema; traducción de `\n` a CRLF verificada en bytes (1.189.306 CRLF, cero LF sueltos).

Después: `json.JSONEncoder(ensure_ascii=False, indent=2).iterencode(data)` escribe lotes al alcanzar un umbral de 65.536 caracteres y añade el mismo salto final. El lote puede superar el umbral por el tamaño de un fragmento individual del encoder. Mantiene UTF-8, indentación, separadores, orden, modo y traducción de saltos; no construye una cadena JSON completa.

**BYTE_EQUIVALENCE = PASS.** Para el mismo modelo S4 determinista (35,967,635 bytes), la fuente y ambas serializaciones producen SHA-256 `960631593d982f1c952ca2b8e707965c809c8c41a56501b55c76c45458250eac`. Tamaños iguales y fuente idéntica a la serialización anterior.

**SEMANTIC_EQUIVALENCE = PASS.** Identidad de fuente/dataset, referencias de evidencia y hashes de las tablas de entrada, findings, accounting, interpretación, semántica del informe y versiones de contrato: todo PASS. El replay sintético confirma informes de motor idénticos y hashes de entrega verificados.

## P05–P07 — Medición sintética antes/después

Se usó el harness W00-M de árbol de procesos con intervalo de muestreo 100 ms. Las dos corridas completaron S1, S4, S8, S16, S32 y S64 con preflight PASS; las ejecuciones fueron secuenciales. Los picos son observaciones muestreadas, no máximos exactos del sistema.

| Escala | Privada árbol antes → después | Cambio | Pared antes → después (s) | JSON serialización antes → después (s) | Escritura antes → después (s) | Subetapa del pico antes → después |
|---|---:|---:|---:|---:|---:|---|
| S1 | 67,112,960 → 45,068,288 | -22,044,672 B (-32.85%) | 0.692 → 0.796 (+15.03%) | 0.159 → 0.177 | 0.013 → 0.011 | `JSON_SERIALIZATION` → `AUDIT` |
| S4 | 321,392,640 → 86,949,888 | -234,442,752 B (-72.95%) | 1.911 → 1.902 (-0.47%) | 0.569 → 0.629 | 0.056 → 0.039 | `JSON_FILE_WRITE` → `AUDIT` |
| S8 | 545,861,632 → 140,374,016 | -405,487,616 B (-74.28%) | 3.597 → 3.653 (+1.56%) | 1.124 → 1.313 | 0.108 → 0.081 | `JSON_SERIALIZATION` → `AUDIT` |
| S16 | 1,192,898,560 → 297,779,200 | -895,119,360 B (-75.04%) | 7.307 → 7.446 (+1.90%) | 2.484 → 2.685 | 0.227 → 0.181 | `JSON_FILE_WRITE` → `AUDIT` |
| S32 | 2,351,116,288 → 429,879,296 | -1,921,236,992 B (-81.72%) | 14.704 → 15.352 (+4.41%) | 4.718 → 5.403 | 0.469 → 0.431 | `JSON_FILE_WRITE` → `AUDIT` |
| S64 | 4,662,751,232 → 866,676,736 | -3,796,074,496 B (-81.41%) | 28.966 → 30.166 (+4.14%) | 9.270 → 10.864 | 0.988 → 0.747 | `JSON_FILE_WRITE` → `AUDIT` |

El pico privado de proceso raíz coincide con el del árbol en estas corridas (un único proceso en el pico). El working set de raíz/árbol, el tamaño y SHA-256 de `run.json`, los conteos/intervalos de muestra, el hash de cada fixture y el motivo/gate de cada escala están en el [manifiesto completo](evidence/windows_client_v1/w00/json_streaming_optimization/w00p_before_after_manifest.json). Cada `run.json` cambia entre corridas por su identidad y marcas temporales; la prueba byte a byte anterior compara el mismo objeto, que es la comparación requerida.

**MEMORY_CHANGE = MATERIAL_IMPROVEMENT.** Reducción observada en las seis escalas, entre 32,85 % y 81,72 %, sin umbral inventado. `LARGEST_SAFE_SCALE = S64`.
**RUNTIME_CHANGE:** de −0,47 % en S4 a +15,03 % en S1; S64 aumentó 4,14 % (1,20 s). La serialización aumentó modestamente y la escritura disminuyó en S4–S64. Se informa como trade-off medido, sin fijar umbral.
**ROOT_CAUSE_SYNTHETIC = CONFIRMED.** Antes, el pico se muestreó en serialización/escritura; después, el pico global se muestreó en `AUDIT` y el proceso usó 81,41 % menos memoria en S64. Esto confirma el mecanismo solo para la reproducción sintética; no atribuye la causa de dataset 019.

## P08–P13 — Límites, regresión y empaquetado

- G03, `header_schema.not_evaluable`, cardinalidad `CONDITION_UNKNOWN` y su representación de evidencia no se modificaron ni deduplicaron. Son únicamente una posible superficie de optimización futura y requieren revisión humana aparte.
- Dataset 019 = `DEFERRED_FOR_HIGH_MEMORY_ENVIRONMENT`; HOLDOUT no accedido.
- Regresión completa: **291 total / 290 PASS / 0 FAIL / 1 SKIP documentado**. El SKIP requiere una base de Compliance separada ausente deliberadamente del checkout.
- PyInstaller onedir = `PASS`: worker reconstruido, self-check PASS, auditoría sintética S1 PASS, hash del `run.json` empaquetado coincide byte a byte con su serialización en streaming. DuckDB CLI 1.5.5 está bajo `_internal` y se confirmó `DUCKDB_BUNDLED = YES`.
- Validación en máquina limpia = `PENDING`; la máquina del benchmark no es un entorno limpio.
- Los árboles sintéticos grandes permanecen locales y no se versionan. Se preservan manifests, hashes, generador/escala, comparaciones e instrucciones. No se hizo limpieza recursiva.

## P14 — Decisión y límites de fase

```ini
W00P_PASS_WITH_RESOURCE_LIMITATION
SERIALIZATION_CHANGE = JSONEncoder.iterencode + 65,536-character flush threshold
BYTE_EQUIVALENCE = PASS
SEMANTIC_EQUIVALENCE = PASS
S1_BEFORE_PEAK = 67,112,960 BYTES; OBSERVED_SAMPLED
S1_AFTER_PEAK = 45,068,288 BYTES; OBSERVED_SAMPLED
S4_BEFORE_PEAK = 321,392,640 BYTES; OBSERVED_SAMPLED
S4_AFTER_PEAK = 86,949,888 BYTES; OBSERVED_SAMPLED
LARGEST_SAFE_SCALE = S64
MEMORY_CHANGE_BYTES = S4 -234,442,752; S64 -3,796,074,496
MEMORY_CHANGE_PERCENT = S4 -72.95%; S64 -81.41%
RUNTIME_CHANGE = S4 −0.47%; S64 +4.14%; all scale measurements in manifest
ROOT_CAUSE_SYNTHETIC = CONFIRMED
DATASET_019 = DEFERRED
PYINSTALLER_ONEDIR = PASS
DUCKDB_BUNDLED = YES
CLEAN_MACHINE_VALIDATION = PENDING
FUNCTIONAL_ENGINE_CHANGED = YES
ENGINE_SEMANTICS_CHANGED = NO
HOLDOUT_ACCESSED = NO
FULL_REGRESSION = 291 / 290 / 0 / 1
W01 = NOT_STARTED
STOP = W00P_READY_FOR_HUMAN_REVIEW
```

La clasificación `PASS_WITH_RESOURCE_LIMITATION` conserva 019 diferido y deja el límite de recursos V1 para decisión humana. No se inicia W01 ni se hace merge automáticamente.

## Reproducción y archivos de evidencia

- Before: `reports/evidence/windows_client_v1/w00/json_streaming_optimization/before_scales/resource_scaling_analysis.json`.
- After: `reports/evidence/windows_client_v1/w00/json_streaming_optimization/after_final/resource_scaling_analysis.json`.
- Semántica y referencias: `reports/evidence/windows_client_v1/w00/json_streaming_optimization/semantic_comparison_final.json`.
- Replay: `reports/evidence/windows_client_v1/w00/json_streaming_optimization/synthetic_replay_e2e_final.json`.
- PyInstaller: `reports/evidence/windows_client_v1/w00/json_streaming_optimization/packaging_validation.json`.
- Regresión: `02_Data_Engineering/GTFS_Lab/reports/evidence/windows_client_v1/w00/json_streaming_optimization/full_regression_unittest.log`.

Comando de benchmark desde `02_Data_Engineering/GTFS_Lab`:
```powershell
python -m tools.synthetic_resource_benchmark --ladder <evidence-root> --scales 1,4,8,16,32,64 --interval 0.1
```

Comprobaciones finales: `python -m unittest discover -s tests -v` PASS; `git diff --check` PASS. No hubo commit, push ni merge. Todos los derechos reservados.

## Validación del repositorio

- `git diff --check`: PASS.
- `git status --short --branch`: rama `feat/windows-client-v1-w00` basada en `origin/main`. El worktree conserva cambios anteriores de W00-M/W00-O/W00-R en `client_workflow.py`, `ingestion.py`, `pipeline.py`, `test_bank.py`, instrumentación y evidencia. Esta fase añade el cambio de `core.py`, la comparación semántica W00-P y documentación/evidencia W00-P. Los cambios preexistentes se preservaron.
- No se creó commit, push ni merge; no se inició W01 ni se hizo limpieza recursiva.
