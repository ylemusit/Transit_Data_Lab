# Remediation Engine V1 — ejecución del primer caso real

**Fecha:** 2026-10-02
**Resultado:** `FIRST_REAL_REMEDIATION_CASE = PASS`; `REMEDIATION_ENGINE_V1_TECHNICAL_REVIEW = PASS`; `REMEDIATION_ENGINE_V1 = READY_FOR_FINAL_HUMAN_CLOSURE_DECISION`.

## Recuperación y procedencia

El ZIP DEVELOPMENT `010` se encontró en el corpus raíz y en el source root temporal citado por el candidato de cierre G11. Ambas copias miden 13.888 bytes y coinciden exactamente con el SHA-256 esperado `3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf`. La evidencia de recuperación está en el registro machine-readable asociado. No se abrió ni leyó ningún ZIP HOLDOUT.

Se copió el ZIP validado a `C:/Users/yeiso/AppData/Local/Temp/tdl-remediation-engine-v1-010-20261002/input/` y se creó allí un derivado. El original del corpus quedó intacto. Los runs completos de Audit A, Audit B y el replay determinista también permanecen en ese workspace temporal.

## Cambio y re-audit

El finding de origen `GTFS-G03-FIELD-TYPE` de `agency.txt / ROW:1 / agency_url` observó `empresarodil.es`. La propuesta específica para `dataset_id=010` aplicó el valor autorizado `https://empresarodil.es`, con safety `SAFE_DETERMINISTIC` y autorización `HUMAN_APPROVED_CASE_SPECIFIC`.

La comparación byte a byte de los miembros demuestra que los nombres/orden del ZIP permanecen iguales, todos los demás miembros conservaron sus bytes y la celda autorizada es el único cambio. SHA-256 de entrada: `3113b5b5e78bb8d97e4895b41564a80799b087f2a86c4e28019d7db05be98faf`. SHA-256 del ZIP derivado: `ce78c804770250165daeace125cd01c4649122c7cfc1843bb0b0fd8a1b2d2691`.

Audit B ya no produce el finding de origen; el campo `agency_url` fue evaluado por el validador de tipo URL y el valor propuesto pasó. El estado agregado `GTFS-G03-FIELD-TYPE = NOT_EVALUABLE` se conserva porque hay otros valores/campos fuera de la capacidad ejecutable; no se filtran findings ni se alteran estados para ocultar ese gap. Entre G03–G08, Audit A tuvo solo el finding de origen y Audit B tuvo cero findings: `RESOLVED=1`, `UNCHANGED=0`, `NEW=0`, `NO_LONGER_EVALUABLE=0`. La comparación del pipeline general quedó `PARTIALLY_COMPARABLE` debido a identidad opcional ausente; sus resultados normativos y findings legacy permanecieron `UNCHANGED_STATUS` / sin cambios.

G08 se ejecutó separadamente como módulo opcional, sin integrarlo al pipeline ni G09. Devolvió `NOT_EVALUABLE` en A/B porque G03 no establece un resultado fiable para `feed_info.txt`. No se modificó G08 ni se usó su estado como condición para resolver el finding G03.

## Criterios de aceptación

```ini
ORIGINAL_DATASET_UNCHANGED = YES
DERIVED_DATASET_CREATED = YES
SOURCE_SHA256_VERIFIED = YES
ONLY_AUTHORIZED_VALUE_CHANGED = YES
CHANGE_ATTRIBUTION_COMPLETE = YES
ORIGINAL_FINDING_RESOLVED = YES
NEW_UNRELATED_FINDINGS = 0
REAUDIT_REPRODUCIBLE = YES
HOLDOUT_ACCESSED = NO
```

Los findings `011` (referencias sin resolver) y `014` (progresión de distancia) quedan `HUMAN_REVIEW_REQUIRED / NOT_SAFE_AUTOMATICALLY`; no hay evidencia suficiente para transformaciones seguras. No se modificaron GTFS Audit Engine V1 ni M02. La suite unitaria sintética no se usa como sustituto del caso real.

## Verificación ejecutada

- Remediation: 3/3 tests PASS.
- Regresiones GTFS G02–G08: 115/115 tests PASS.
- Comparación de auditorías: 23/23 tests PASS.
- Compliance V1 transition/gates relacionados: 3/3 tests PASS.
- Re-audit completa repetida sobre el mismo ZIP derivado: proyecciones G03–G07, validation y G08 idénticas.

El registro detallado, incluido el diff machine-readable, las identidades, los hashes, atribución, comparaciones y límites, está en [dataset_010_case_20261002.json](evidence/remediation_v1/dataset_010_case_20261002.json).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
