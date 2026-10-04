# Audit Interpretation & Consolidation V1

## 1. Dataset Identity

- Dataset: `GTFS-cdae69f98c44d5e1`
- SOURCE SHA-256: `cdae69f98c44d5e19bba3f5f87791740e2477515a03249568b275f8e4e509216`

## 2. Execution Identity

- Audit execution: `GTFSRUN-ae0e76d932784020`
- GTFS_Lab: `1.0.0-dev`
- Interpretation contract: `1.0.0`
- TDL ref: `9cafe0703abf47e80f67f80a6b423c938e1979aa+WORKTREE_DIRTY.`

## 3. Audit Result

Interpretation status: **COMPLETE**.

## 4. Coverage

- Raw occurrences: 3
- Classified occurrences: 3
- Unclassified occurrences: 0
- Accounting gap: 0

## 5. Raw Finding Summary

`source_findings` contiene 3 findings de origen, preservados en el artefacto JSON.

## 6. Consolidated Finding Families

| Rule | Pattern | Status | Raw | Direct entities | Population | Affected % |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| GTFS-G08-FEED-END-DATE-DECLARED | TECHNICAL_FINDING | INFO | 1 | 1 | NOT_EVALUABLE | NOT_EVALUABLE |
| GTFS-G08-FEED-START-DATE-DECLARED | TECHNICAL_FINDING | INFO | 1 | 1 | NOT_EVALUABLE | NOT_EVALUABLE |
| GTFS-G08-FEED-VERSION-DECLARED | TECHNICAL_FINDING | INFO | 1 | 1 | NOT_EVALUABLE | NOT_EVALUABLE |

## 7. Pattern Analysis

- `GTFS-G08-FEED-END-DATE-DECLARED` (CALCULATED): 1 entidades directas únicas.
- `GTFS-G08-FEED-START-DATE-DECLARED` (CALCULATED): 1 entidades directas únicas.
- `GTFS-G08-FEED-VERSION-DECLARED` (CALCULATED): 1 entidades directas únicas.

## 8. Direct Impact

- `GTFS-G08-FEED-END-DATE-DECLARED`: 1 feed directos afectados.
- `GTFS-G08-FEED-START-DATE-DECLARED`: 1 feed directos afectados.
- `GTFS-G08-FEED-VERSION-DECLARED`: 1 feed directos afectados.

## 9. Operational Propagation

- `GTFS-G08-FEED-END-DATE-DECLARED`: sin relaciones propagadas evaluables
- `GTFS-G08-FEED-START-DATE-DECLARED`: sin relaciones propagadas evaluables
- `GTFS-G08-FEED-VERSION-DECLARED`: sin relaciones propagadas evaluables

## 10. Probable Explanations

- No se emitieron explicaciones causales.

## 11. Remediation Assessment

- `GTFS-G08-FEED-END-DATE-DECLARED`: `NOT_EVALUABLE`.
- `GTFS-G08-FEED-START-DATE-DECLARED`: `NOT_EVALUABLE`.
- `GTFS-G08-FEED-VERSION-DECLARED`: `NOT_EVALUABLE`.

## 12. Compliance Boundary

Los findings son técnicos. Este informe no declara incumplimiento legal, conformidad de perfil ni aceptación NAP.

## 13. Limitations

- Interpretación técnica; no determina cumplimiento jurídico.
- Las poblaciones ausentes o no fiables no producen porcentaje evaluable.

## 14. Evidence References

- `GTFS-G08-FEED-END-DATE-DECLARED`: 1 raw IDs; fichero `feed_info.txt`; ejecución `GTFSRUN-ae0e76d932784020`.
- `GTFS-G08-FEED-START-DATE-DECLARED`: 1 raw IDs; fichero `feed_info.txt`; ejecución `GTFSRUN-ae0e76d932784020`.
- `GTFS-G08-FEED-VERSION-DECLARED`: 1 raw IDs; fichero `feed_info.txt`; ejecución `GTFSRUN-ae0e76d932784020`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
