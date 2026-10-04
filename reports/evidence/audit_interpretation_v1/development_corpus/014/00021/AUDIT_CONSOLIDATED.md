# Audit Interpretation & Consolidation V1

## 1. Dataset Identity

- Dataset: `GTFS-da9daa4f60d798fc`
- SOURCE SHA-256: `da9daa4f60d798fc45b3a71ef81926e447a1eaa6c061cddf96c34ea3388272f9`

## 2. Execution Identity

- Audit execution: `GTFSRUN-7f9823e69e794fce`
- GTFS_Lab: `1.0.0-dev`
- Interpretation contract: `1.0.0`
- TDL ref: `9cafe0703abf47e80f67f80a6b423c938e1979aa+WORKTREE_DIRTY.`

## 3. Audit Result

Interpretation status: **COMPLETE**.

## 4. Coverage

- Raw occurrences: 69
- Classified occurrences: 69
- Unclassified occurrences: 0
- Accounting gap: 0

## 5. Raw Finding Summary

`source_findings` contiene 69 findings de origen, preservados en el artefacto JSON.

## 6. Consolidated Finding Families

| Rule | Pattern | Status | Raw | Direct entities | Population | Affected % |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| GTFS-G07-DISTANCE-PROGRESSION | QUANTIZATION_COMPATIBLE | FAIL_TECHNICAL | 69 | 27 | 246 | 10.9756% |

## 7. Pattern Analysis

- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): 27 entidades directas únicas.
- `GTFS-G07-DISTANCE-PROGRESSION` (CALCULATED): G07 total_shapes=246; affected_shapes=27; total_transitions=4745; affected_transitions=69; affected_transition_percentage=1.45416228; increase=4676; equal=69; decrease=0; movimiento geográfico por bucket (m): 0=0; 0-0.25m=0; 0.25-0.50m=0; 0.50-0.75m=0; 0.75-1m=0; >1m=69; precisión shape_dist_traveled=INTEGER_ONLY.
- `GTFS-G07-DISTANCE-PROGRESSION` (INFERRED): Distancia declarada igual con coordenadas distintas es compatible con cuantización; no demuestra su causa.

## 8. Direct Impact

- `GTFS-G07-DISTANCE-PROGRESSION`: 27 shape directos afectados.

## 9. Operational Propagation

- `GTFS-G07-DISTANCE-PROGRESSION`: 18 route, 17 service, 72 trip

## 10. Probable Explanations

- No se emitieron explicaciones causales.

## 11. Remediation Assessment

- `GTFS-G07-DISTANCE-PROGRESSION`: `NOT_EVALUABLE`.

## 12. Compliance Boundary

Los findings son técnicos. Este informe no declara incumplimiento legal, conformidad de perfil ni aceptación NAP.

## 13. Limitations

- Interpretación técnica; no determina cumplimiento jurídico.
- Las poblaciones ausentes o no fiables no producen porcentaje evaluable.

## 14. Evidence References

- `GTFS-G07-DISTANCE-PROGRESSION`: 69 raw IDs; fichero `shapes.txt`; ejecución `GTFSRUN-7f9823e69e794fce`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
