# Audit Interpretation V1 — campaña de corpus DEVELOPMENT

**Fecha:** 2026-10-04
**Baseline:** `9cafe0703abf47e80f67f80a6b423c938e1979aa`
**Rama:** `feat/audit-interpretation-development-hardening`
**Alcance:** solo los 14 datasets DEVELOPMENT del split aprobado.
**Estado:** `PASS_WITH_PROTOCOL_DEVIATION`; freeze humano aprobado con limitaciones documentadas.

## Resultado agregado

| Métrica | Resultado |
|---|---:|
| Datasets intentados / completados / finales OK | 14 / 14 / 14 |
| Casos Test Bank / auditorías internas | 14 / 28 |
| Fallos de pipeline / datasets con retry | 0 / 0 |
| Findings raw / familias consolidadas | 92 / 7 |
| Datasets interpretados / parcialmente interpretados | 11 / 3 |
| Familias interpretadas / parciales / UNKNOWN / no soportadas | 1 / 6 / 0 / 0 |
| Reglas observadas / especializadas / solo genéricas | 6 / 1 / 5 |
| Replay PASS / FAIL; fallos de determinismo | 14 / 0; 0 |
| Gaps de accounting (violaciones / total) | 0 / 0 |
| Candidatas a falsa consolidación | 0 |
| Fixes genéricos / tests sintéticos nuevos / código específico de operador | 0 / 0 / 0 |

Cada dataset tiene `AUDIT_CONSOLIDATED.json` y `.md` junto al registro Test Bank en `reports/evidence/audit_interpretation_v1/development_corpus/<dataset>/<case>/`. No hubo intentos fallidos ni retries. Runtime agregado Test Bank: 846.2 s; ventana total: 931.1 s.

## Resultados por dataset

| Dataset | SHA-256 | Caso | Resultado / clase | Raw | Familias (rule / pattern / count) | I / P / U / UNKNOWN | Retry | Replay | Runtime | Notas |
|---|---|---:|---|---:|---|---|---:|---|---:|---|
| 001 | `1c70a6ea458370fa9a689f04a4f5300ffb0873d85dba4e8e5e8ec57de9964430` | 00011 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.7 s | No findings emitted. |
| 002 | `42bf756a88336dacb085ec49dbdd0f019fd37afe7c7e5c24c1d8d2c1df0de27d` | 00012 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.4 s | No findings emitted. |
| 003 | `70b14647471462975b9b646d738b76c2f27454d8d9f49311bb31289a888e411a` | 00013 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.3 s | No findings emitted. |
| 004 | `1fe7adb7486766672ddef94917a881a0bacc5450ba00591d9a3c0e7067e63cb6` | 00014 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.4 s | No findings emitted. |
| 005 | `f35192f9ac9f91e39f10357dad6cc88ebdffdeedfc3bf4053b383d09636de100` | 00015 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.7 s | No findings emitted. |
| 007 | `81ef87bfe4c8500dc9f4b48f75ae2992131eb86e566fb4a60c73ea54431a9f1a` | 00016 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 1.2 s | No findings emitted. |
| 009 | `0c588ca4a7547b36777f9aaf8a997ae35307d4ed74ac0cee04e8ff543c8f40f8` | 00017 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 3.7 s | No findings emitted. |
| 010 | `3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf` | 00018 | OK / PARTIALLY_INTERPRETED (P) | 1 | GTFS-G03-FIELD-TYPE / TECHNICAL_FINDING / 1 | 0 / 1 / 0 / 0 | 0 | PASS | 3.1 s | GTFS-G03-FIELD-TYPE TECHNICAL_FINDING (1) |
| 011 | `5c139120f8424b69dd98024cbeda9a2a3f0f694772e14cb795e20f154663c23b` | 00019 | OK / PARTIALLY_INTERPRETED (P) | 19 | GTFS-G04-IDENTITY-DOMAIN / TECHNICAL_FINDING / 3, GTFS-G04-IDENTITY-DOMAIN / TECHNICAL_FINDING / 16 | 0 / 2 / 0 / 0 | 0 | PASS | 13.5 s | GTFS-G04-IDENTITY-DOMAIN TECHNICAL_FINDING (3); GTFS-G04-IDENTITY-DOMAIN TECHNICAL_FINDING (16) |
| 012 | `da2d07f8d0e2dbad98f4a6b05b927ed1a2f3f660a61054b7fd6401418cad5eb7` | 00020 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 8.8 s | No findings emitted. |
| 014 | `da9daa4f60d798fc45b3a71ef81926e447a1eaa6c061cddf96c34ea3388272f9` | 00021 | OK / INTERPRETED (I) | 69 | GTFS-G07-DISTANCE-PROGRESSION / QUANTIZATION_COMPATIBLE / 69 | 1 / 0 / 0 / 0 | 0 | PASS | 30.2 s | GTFS-G07-DISTANCE-PROGRESSION QUANTIZATION_COMPATIBLE (69) |
| 016 | `cdae69f98c44d5e19bba3f5f87791740e2477515a03249568b275f8e4e509216` | 00022 | OK / PARTIALLY_INTERPRETED (P) | 3 | GTFS-G08-FEED-END-DATE-DECLARED / TECHNICAL_FINDING / 1, GTFS-G08-FEED-START-DATE-DECLARED / TECHNICAL_FINDING / 1, GTFS-G08-FEED-VERSION-DECLARED / TECHNICAL_FINDING / 1 | 0 / 3 / 0 / 0 | 0 | PASS | 5.2 s | GTFS-G08-FEED-END-DATE-DECLARED TECHNICAL_FINDING (1); GTFS-G08-FEED-START-DATE-DECLARED TECHNICAL_FINDING (1); GTFS-G08-FEED-VERSION-DECLARED TECHNICAL_FINDING (1) |
| 019 | `e15d963ba3dc774e47b4f9f46dbd954ece6a720d49a71bfc22a104a12027bd73` | 00023 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 763.0 s | No findings emitted. |
| 020 | `65130fd01470593cd2e234177f3c4cb810154d0b8e13fbee3aa91f1973072ace` | 00024 | OK / INTERPRETED (I) | 0 | — | 0 / 0 / 0 / 0 | 0 | PASS | 10.1 s | No findings emitted. |

I = interpretada; P = parcialmente interpretada (solo consolidación genérica); U = no soportada; N = fallo de pipeline. Un dataset sin findings se clasifica INTERPRETED porque no emitió familias pendientes de interpretar. 010 es parcial por una familia G03 `TECHNICAL_FINDING` agrupada genéricamente, sin interpretación específica. 011 es parcial por dos familias G04 `TECHNICAL_FINDING` (3 y 16 hallazgos) agrupadas genéricamente, sin interpretación de dominio especializada. 016 es parcial por tres recomendaciones G08 (`feed_start_date`, `feed_end_date`, `feed_version`) con estado `INFO`, consolidadas genéricamente y sin interpretación específica. No se inventa semántica ausente. `COMPLETED_WITH_LIMITATIONS` no equivale a fallo de Test Bank.

## Inventario de reglas y familias

| Rule ID | Datasets | Familias | Occurrences | Capa |
|---|---|---:|---:|---|
| `GTFS-G03-FIELD-TYPE` | 010 | 1 | 1 | Consolidación genérica |
| `GTFS-G04-IDENTITY-DOMAIN` | 011 | 2 | 19 | Consolidación genérica |
| `GTFS-G07-DISTANCE-PROGRESSION` | 014 | 1 | 69 | Especializada G07 |
| `GTFS-G08-FEED-END-DATE-DECLARED` | 016 | 1 | 1 | Consolidación genérica |
| `GTFS-G08-FEED-START-DATE-DECLARED` | 016 | 1 | 1 | Consolidación genérica |
| `GTFS-G08-FEED-VERSION-DECLARED` | 016 | 1 | 1 | Consolidación genérica |

Se observaron seis rule IDs en cuatro stages. Una familia G07 fue interpretada con geometría; las otras seis familias observadas siguen con consolidación genérica. No hubo UNKNOWN ni familias fuera de alcance. Ninguna rule con findings se repitió en dos datasets DEVELOPMENT; no se demuestra recurrencia entre operadores.

## Análisis G07
Solo 014 emitió G07: 69 findings; 27 de 246 shapes afectados; 69 transiciones iguales, 0 decrecientes y 4676 crecientes. Clasificación: `QUANTIZATION_COMPATIBLE`.

Sobre 4745 transiciones, 69 (1.45416228%) quedaron afectadas. Duplicado geométrico exacto: 0; compatibles con cuantización: 69; mixtas: 0; desconocidas: 0. Precisión `shape_dist_traveled`: `INTEGER_ONLY`; las 69 transiciones iguales mostraron movimiento >1 m. Propagación: 72 trips, 18 routes y 17 services.

El intérprete especializado funcionó en un dataset DEVELOPMENT; al haber un solo dataset con G07 findings, esto no acredita generalización amplia.

## Falsa consolidación y patrones entre datasets

Los miembros raw se revisaron por rule, archivo, stage, estado, razón/expected domain, campos, requirement y authority. Las firmas de cada familia se mantuvieron coherentes; no se registra `FALSE_CONSOLIDATION_CANDIDATE` y no se alteró la taxonomía. G04 en 011 agrupa referencias sin dominio de servicio por archivo; G07 en 014 agrupa transiciones iguales con movimiento de coordenadas y precisión entera.

Patrones: G03 agency URL no válida en 010; G04 identity-domain en dos archivos en 011; G07 cuantización compatible en 014; tres recomendaciones G08 ausentes en 016. No hubo recurrencia entre datasets. No se infiere calidad de operadores.

## Rendimiento y artefactos

Dataset 019: ZIP de 18,245,454 bytes y `stop_times.txt` descomprimido de 52,049,844 bytes. Runtime observado: 12m43s; terminó Test Bank `OK`, replay PASS y cero findings. El muestreo manual observó un pico de memoria privada de aproximadamente 18.89 GiB; no fue perfilado continuo y no constituye SLA. Funcionalidad en dataset grande: PASS; optimización de rendimiento: REQUIRED.

Mayor `AUDIT_CONSOLIDATED.json`: 122,584 bytes; mayor `engine_report.json`: 75,316 bytes; mayor `findings.json`: 99,805 bytes. No se inventan umbrales.

## Regresión final

`python -m unittest discover -s tests -p 'test_*.py'`: 280 tests, 279 PASS, 0 FAIL, 1 SKIP. El skip requiere la base Compliance V1 respaldada por separado, ausente por diseño en el checkout limpio.

No se hicieron fixes ni cambios de código; no se agregaron regresiones sintéticas.

## Integridad de alcance y cierre

**Desviación de protocolo:** durante el reconocimiento inicial se listaron por error directorios por familia, revelando nombres/IDs de carpetas asignadas a HOLDOUT. Se registra `HOLDOUT_ACCESSED = YES` y `HOLDOUT_ACCESS_LEVEL = METADATA_ONLY`; `HOLDOUT_DIRECTORY_NAMES_EXPOSED = YES`. No se leyó contenido, abrieron fuentes, calcularon hashes ni ejecutó el pipeline sobre HOLDOUT. Tampoco se usó HOLDOUT para tuning, fixes o diseño de tests. Por tanto `PRISTINE_BLIND_HOLDOUT = NO`, mientras `CONTENT_BLIND_HOLDOUT = YES`. Los seis datasets permanecen protegidos de acceso a contenido hasta autorización separada. No se reescribe ni minimiza la incidencia.

**Clasificación técnica:** `PASS_WITH_PROTOCOL_DEVIATION`: 14/14 datasets finales OK y replay PASS; sin fallos de pipeline ni gaps de accounting. Tres datasets son parcialmente interpretados por los motivos documentados; seis familias permanecen solo genéricamente consolidadas. Dataset 019 completó funcionalmente con latencia y memoria elevadas; requiere optimización, sin SLA establecido.

**Decisión humana:** Yeison aprobó el freeze tras la campaña. `INTERPRETATION_V1_FREEZE_DECISION = APPROVED`; `AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = FROZEN_WITH_DOCUMENTED_LIMITATIONS`. El freeze fija la implementación validada en `ENGINE_FREEZE_BASE = 9cafe0703abf47e80f67f80a6b423c938e1979aa`; los commits documentales posteriores no cambian ese baseline. No se autorizan ajustes conductuales antes de validación HOLDOUT controlada. No se inicia esa validación ni Windows Self-Service Client V1 en esta fase.

```ini
DEVELOPMENT_DATASETS = 14
DEVELOPMENT_FINAL_OK = 14
DEVELOPMENT_REPLAY_PASS = 14
RAW_FINDINGS = 92
CONSOLIDATED_FAMILIES = 7
INTERPRETED_DATASETS = 11
PARTIALLY_INTERPRETED_DATASETS = 3
UNKNOWN_FAMILIES = 0
UNSUPPORTED_FAMILIES = 0
PIPELINE_FAILURES = 0
ACCOUNTING_GAPS = 0
GENERIC_FIXES_APPLIED = 0
NEW_TESTS_REQUIRED_BY_CAMPAIGN = 0
OPERATOR_SPECIFIC_CODE = 0

HOLDOUT_ACCESSED = YES
HOLDOUT_ACCESS_LEVEL = METADATA_ONLY
HOLDOUT_DIRECTORY_NAMES_EXPOSED = YES
HOLDOUT_CONTENT_READ = NO
HOLDOUT_SOURCE_FILES_OPENED = NO
HOLDOUT_SOURCE_HASHES_COMPUTED = NO
HOLDOUT_PIPELINE_EXECUTED = NO
HOLDOUT_USED_FOR_TUNING = NO
HOLDOUT_USED_FOR_FIXES = NO
HOLDOUT_USED_FOR_TEST_DESIGN = NO
PRISTINE_BLIND_HOLDOUT = NO
CONTENT_BLIND_HOLDOUT = YES
```

```makefile
DEVELOPMENT_CORPUS_CAMPAIGN = PASS_WITH_PROTOCOL_DEVIATION
INTERPRETATION_V1_FREEZE_DECISION = APPROVED
AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = FROZEN_WITH_DOCUMENTED_LIMITATIONS
DEVELOPMENT_DATASET_019_RUNTIME ≈ 12m43s
DEVELOPMENT_DATASET_019_PEAK_PRIVATE_MEMORY ≈ 18.89 GiB
DEVELOPMENT_DATASET_019_RESULT = OK
DEVELOPMENT_DATASET_019_REPLAY = PASS
DEVELOPMENT_DATASET_019_FINDINGS = 0
LARGE_DATASET_FUNCTIONALITY = PASS
LARGE_DATASET_PERFORMANCE_OPTIMIZATION = REQUIRED
```

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
