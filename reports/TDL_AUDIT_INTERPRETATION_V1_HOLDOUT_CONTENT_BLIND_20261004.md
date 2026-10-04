# Audit Interpretation V1 — validación HOLDOUT content-blind

**Fecha:** 2026-10-04
**Decisión humana:** `APPROVED`
**Resultado:** `GENERALIZATION_PASS_WITH_LIMITATIONS`

## Resultado

| Métrica | Resultado |
|---|---:|
| Datasets HOLDOUT completados | 6 / 6 |
| Case IDs | 00025–00030 |
| Interpretados / parcialmente interpretados | 5 / 1 |
| No soportados / fallos de pipeline | 0 / 0 |
| Findings raw / familias consolidadas | 530 / 3 |
| Accounting gaps | 0 |
| Replay PASS / FAIL | 6 / 0 |
| Candidatas a falsa consolidación | 0 |
| Cambios del engine / código específico de operador | NO / 0 |

El resultado de generalización se acepta con limitaciones. `G04 REFERENCE-EXISTENCE` permanece en `GENERIC_CONSOLIDATION_ONLY`; su interpretación especializada no se implementa y queda como `BACKLOG_CANDIDATE`. `G07 EXACT_DUPLICATE_GEOMETRY` fue observado en HOLDOUT. En el dataset 017 (caso 00029) se registraron 529 transiciones G07 iguales: 6 `EXACT_DUPLICATE_GEOMETRY` y 523 `QUANTIZATION_COMPATIBLE`.

```ini
FINAL_HUMAN_GENERALIZATION_DECISION = APPROVED
GENERALIZATION_RESULT = GENERALIZATION_PASS_WITH_LIMITATIONS
AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = VALIDATED_WITH_DOCUMENTED_LIMITATIONS
INTERPRETATION_HARDENING_V2 = NOT_REQUIRED_NOW
G04_SPECIALIZED_INTERPRETATION = BACKLOG_CANDIDATE
```

## Historia del protocolo

Esta declaración conserva explícitamente la exposición de metadatos anterior al freeze y el acceso posterior al contenido. No se sustituye la declaración histórica previa.

```ini
HOLDOUT_METADATA_PRE_FREEZE_EXPOSURE = YES
HOLDOUT_CONTENT_PRE_FREEZE_EXPOSURE = NO
HOLDOUT_CONTENT_ACCESSED_AFTER_FREEZE = YES
PRISTINE_BLIND_HOLDOUT = NO
CONTENT_BLIND_HOLDOUT = YES
```

## Identidad funcional y regresión

El merge de freeze publicado es `3fba5cbabee000267a511c65b9bc8d90a78b8880`; la base funcional es `9cafe0703abf47e80f67f80a6b423c938e1979aa`. Los ficheros funcionales versionados no cambiaron durante HOLDOUT.

```ini
FINAL_TEST_TOTAL = 280
PASS = 279
FAIL = 0
SKIP = 1 DOCUMENTED
GIT_DIFF_CHECK = PASS
```

## Límites conservados

- G04 specialized interpretation no implementado.
- Un dataset HOLDOUT quedó `PARTIALLY_INTERPRETED`.
- Tres datasets DEVELOPMENT quedaron `PARTIALLY_INTERPRETED`.
- Sigue siendo necesaria la optimización de memoria para feeds grandes.
- No se declara preparación comercial, validación de mercado, cumplimiento legal ni cobertura GTFS completa.
- No se publica código ni fuente raw de operadores.

## Evidencia

Los seis paquetes publicables están en [holdout_content_blind](evidence/audit_interpretation_v1/holdout_content_blind/), con el mapeo verificado desde la evidencia de ejecución: `006→00025`, `008→00026`, `013→00027`, `015→00028`, `017→00029` y `018→00030`. Cada paquete conserva, sin cambios, la consolidación JSON/Markdown, `dataset_identity.json`, `audit_interpretation_status.json` y `replay.json`. Estos artefactos de entrega existentes equivalen al registro Test Bank para identidad, estado de interpretación y replay; el estado final `OK` se acredita mediante la ubicación del caso en `BANK/OK`. No se copiaron los registros `case.json`/`test_bank_record.json` porque contienen `original_filename`, con identificadores de operador.

El caso `00026` (dataset `008`) es `PARTIALLY_INTERPRETED`: el único hallazgo pertenece a `GTFS-G04-REFERENCE-EXISTENCE`, cuya familia queda `GENERIC_ONLY`; la interpretación especializada de G04 no está implementada. El hallazgo técnico identifica una referencia `parent_station` sin identidad destino coincidente en `stops.txt`. Los otros cinco casos constan como `INTERPRETED`. Los informes consolidados y el estado de interpretación conservan `interpretation_status = COMPLETE`, que indica que el proceso terminó; la clasificación de generalización del caso se documenta por separado en la evidencia de ejecución por dataset.

La reconciliación por caso reproduce 6/6 casos `OK`, 6/6 replay `PASS`, 530 findings raw, 3 familias consolidadas y cero accounting gaps. En el caso `00029` (dataset `017`) se verifican 529 transiciones G07: 6 `EXACT_DUPLICATE_GEOMETRY` y 523 `QUANTIZATION_COMPATIBLE`. El [manifiesto de evidencia](evidence/audit_interpretation_v1/holdout_content_blind_manifest.json) registra por archivo los SHA-256 de origen y copia; los 30 pares coinciden. No se publicaron fuentes raw ni rutas privadas absolutas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
