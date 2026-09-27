# GTFS Explorer — Pilot Audit 01

## STATUS

PASS_WITH_OBSERVATIONS — cinco operadores procesados; evidencia histórica preservada y comparación completada. En Bizkaibus, `run_001` tiene detalle truncado por el límite observado del informe (`100.000` persistidas de `1.040.852` detectadas). Es una ejecución histórica no canónica de `validation-100k`, no evidencia del comportamiento de RC-002. No es una conclusión jurídica ni de cumplimiento.

La reconciliación del 2026-09-23 no promovió `run_002_rc002`: su base es schema
9, no el schema 11 esperado de RC-002, y no existe evidencia que vincule el
proceso al hash canónico. Se conserva como intento con `PROVENANCE MISMATCH`.
Las conclusiones de producto canónico quedan pendientes de un run atribuible a
RC-002.

## OPERATORS PROCESSED

| ID | Operator | Output | Product |
|---|---|---|---|
| 002 | Ancebus | `03_gtfs_explorer/run_001` | 0.2.1 |
| 005 | Viagón | `03_gtfs_explorer/run_001` | 0.2.1 |
| 014 | Gilsanz | `03_gtfs_explorer/run_001` | 0.2.1 |
| 019 | Bizkaibus | `03_gtfs_explorer/run_001` | 0.2.1 histórica `validation-100k` |
| 020 | Kbus | `03_gtfs_explorer/run_001` | 0.2.1 |

## GTFS EXPLORER RUN INTEGRITY

| Operator | run_id | status | detected | persisted | detail_complete | omitted | filter |
|---|---|---|---:|---:|---|---:|---|
| Ancebus | `e403acfe-4c56-411f-be4f-750c2b6c4e89:structure` | INVALID | 12 | 12 | True | 0 | null/null |
| Viagón | `fcae88c4-3ff5-4361-9289-5dec3896efe8:structure` | INVALID | 56 | 56 | True | 0 | null/null |
| Gilsanz | `32f00f4e-2328-4720-aebf-38acd351ef64:structure` | INVALID | 1 | 1 | True | 0 | null/null |
| Bizkaibus | `70cdab72-6664-493e-b459-a1ce4c7abb4e:structure` | INVALID | 1040852 | 100000 | False | 940852 | null/null |
| Kbus | `3c2717db-3bea-475f-979e-917092952dd9:structure` | INVALID | 644 | 644 | True | 0 | null/null |

`legacy_truncated` no aparece en los informes inspeccionados: `null`. `omitted_occurrences` se ha tomado de `batch.omitted_issue_count`.

## SEVERITY SUMMARY

| operator | NAP errors | NAP warnings | GTE errors | GTE warnings | GTE notices | GTE best practices | GTE detected occurrences |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ancebus | 0 | 0 | 6 | 0 | 6 | 6 | 12 |
| Viagón | 0 | 22 | 22 | 0 | 34 | 23 | 56 |
| Gilsanz | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| Bizkaibus | 0 | 0 | 100000 | 0 | 0 | 0 | 1040852 |
| Kbus | 0 | 317 | 644 | 0 | 0 | 0 | 644 |

## KEY DIFFERENTIALS

- GTE proporciona reglas y localizaciones por hallazgo; NAP solo aporta agregados en el baseline disponible.
- Bizkaibus es el único run con truncado de detalle: `940.852` incidencias omitidas.
- En Bizkaibus esta observación corresponde a `run_001`, una build histórica no canónica. `run_002_rc002` repite el patrón, pero su procedencia es incompatible con RC-002 y no sustituye la evidencia histórica.
- GTE clasifica como ERROR findings que NAP presenta como warnings o no muestra con rule_id comparable; esto demuestra diferencia de taxonomía/alcance, no equivalencia jurídica.

## GTFS EXPLORER ONLY

0 reglas clasificadas de forma concluyente como exclusivas de GTE; las reglas sin correspondencia NAP quedan `UNKNOWN`.

## NAP ONLY

0 reglas clasificadas de forma concluyente como exclusivas de NAP; los agregados NAP sin regla comparable quedan `NOT_COMPARABLE`.

## BOTH

0 reglas clasificadas de forma concluyente como detectadas por ambos; no existe rule_id NAP suficiente para probarlo.

## PRODUCT GAPS OBSERVED

Hechos documentados en `docs/PILOT_01_PRODUCT_GAPS.md`.

## DATA INTEGRITY

- Los hashes SHA-256 actuales de los ZIP originales coinciden con los registrados en `source_census.json` para los cinco operadores.
- Los outputs GTE se preservaron y se inventariaron con tamaño y SHA-256 en `04_audit/pilot_01/gte_output_inventory.md` y `.json`.
- No se modificaron GTFS Explorer, feeds ni fuentes extraídas. No se ejecutó ninguna operación remota ni se creó Working Copy durante esta tarea.
- Los exports JSON contienen un `source.sha256`/`manifest_sha256` de la ejecución; se conservan como evidencia y no se reinterpretan como el SHA-256 del ZIP original.

## OUTPUTS CREATED

- `03_gtfs_explorer/parsed_rule_summary.csv` por operador.
- `pilot_01_baseline.csv` y `docs/PILOT_01_BASELINE_MATRIX.md` completados solo en columnas GTE.
- `04_audit/pilot_01/gte_output_inventory.md` y `.json`.
- `04_audit/pilot_01/NAP_VS_GTFS_EXPLORER.md`.
- `04_audit/pilot_01/differential_matrix.csv` y `.md`.
- `docs/PILOT_01_PRODUCT_GAPS.md`.
- Este informe en `04_audit/pilot_01/final_report.md`.

## NEXT STEP

Review Pilot Audit 01 differential evidence and define the first Audit/Quality requirement model.

No se inicia automáticamente esa fase.
