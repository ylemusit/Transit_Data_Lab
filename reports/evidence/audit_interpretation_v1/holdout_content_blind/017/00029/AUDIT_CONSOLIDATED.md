# Audit Interpretation & Consolidation V1

## 1. Dataset Identity

- Dataset: `GTFS-7b60390d8f3e3b78`
- SOURCE SHA-256: `7b60390d8f3e3b7853eb3f8a873797cb8ffa36e371bc6086570fd687e805546a`

## 2. Execution Identity

- Audit execution: `GTFSRUN-8c2b43cc6e6c43c0`
- GTFS_Lab: `1.0.0-dev`
- Interpretation contract: `1.0.0`
- TDL ref: `3fba5cbabee000267a511c65b9bc8d90a78b8880.`

## 3. Audit Result

Interpretation status: **COMPLETE**.

## 4. Coverage

- Raw occurrences: 529
- Classified occurrences: 529
- Unclassified occurrences: 0
- Accounting gap: 0

## 5. Raw Finding Summary

`source_findings` contiene 529 findings de origen, preservados en el artefacto JSON.

## 6. Consolidated Finding Families

| Rule | Pattern | Status | Raw | Direct entities | Population | Affected % |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| GTFS-G07-DISTANCE-PROGRESSION | EXACT_DUPLICATE_GEOMETRY | FAIL_TECHNICAL | 6 | 6 | 56 | 10.7143% |
| GTFS-G07-DISTANCE-PROGRESSION | QUANTIZATION_COMPATIBLE | FAIL_TECHNICAL | 523 | 44 | 56 | 78.5714% |

## 7. Pattern Analysis

- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): 6 entidades directas únicas.
- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): G07 total_shapes=56; affected_shapes=6; total_transitions=23857; affected_transitions=6; affected_transition_percentage=0.02514985; increase=23328; equal=529; decrease=0; movimiento geográfico por bucket (m): 0=6; 0-0.25m=72; 0.25-0.50m=89; 0.50-0.75m=20; 0.75-1m=342; >1m=0; precisión shape_dist_traveled=FRACTIONAL.
- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): 44 entidades directas únicas.
- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): G07 total_shapes=56; affected_shapes=44; total_transitions=23857; affected_transitions=523; affected_transition_percentage=2.1922287; increase=23328; equal=529; decrease=0; movimiento geográfico por bucket (m): 0=6; 0-0.25m=72; 0.25-0.50m=89; 0.50-0.75m=20; 0.75-1m=342; >1m=0; precisión shape_dist_traveled=FRACTIONAL.
- `GTFS-G07-DISTANCE-PROGRESSION` (INFERRED): Distancia declarada igual con coordenadas distintas es compatible con cuantización; no demuestra su causa.

## 8. Direct Impact

- `GTFS-G07-DISTANCE-PROGRESSION`: 6 shape directos afectados.
- `GTFS-G07-DISTANCE-PROGRESSION`: 44 shape directos afectados.

## 9. Operational Propagation

- `GTFS-G07-DISTANCE-PROGRESSION`: 4 route, 9 service, 567 trip
- `GTFS-G07-DISTANCE-PROGRESSION`: 14 route, 9 service, 3439 trip

## 10. Probable Explanations

- No se emitieron explicaciones causales.

## 11. Remediation Assessment

- `GTFS-G07-DISTANCE-PROGRESSION`: `NOT_EVALUABLE`.
- `GTFS-G07-DISTANCE-PROGRESSION`: `NOT_EVALUABLE`.

## 12. Compliance Boundary

Los findings son técnicos. Este informe no declara incumplimiento legal, conformidad de perfil ni aceptación NAP.

## 13. Limitations

- Interpretación técnica; no determina cumplimiento jurídico.
- Las poblaciones ausentes o no fiables no producen porcentaje evaluable.

## 14. Evidence References

- `GTFS-G07-DISTANCE-PROGRESSION`: 6 raw IDs; fichero `shapes.txt`; ejecución `GTFSRUN-8c2b43cc6e6c43c0`.
- `GTFS-G07-DISTANCE-PROGRESSION`: 523 raw IDs; fichero `shapes.txt`; ejecución `GTFSRUN-8c2b43cc6e6c43c0`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
