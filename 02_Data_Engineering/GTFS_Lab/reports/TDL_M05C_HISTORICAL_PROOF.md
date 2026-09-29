# M05-C — Prueba histórica M04 B1 → B3

Veredicto: `M05C_HISTORICAL_PROOF_READY_FOR_REVIEW`. Evidencia persistida; no se reejecutó HOLDOUT.

Base: `reports/evidence/holdout_evaluation_v1/first_evaluation_summary.json`
Candidata: `reports/evidence/holdout_evaluation_v2/evaluation_summary.json`

| Dataset | SHA fuente | Cambio de resultados | Atribución M05-A | Causas admitidas | Evidencia | Lineage |
|---|---|---|---|---|---|---|
| 006 | MATCH | UNCHANGED_STATUS | MULTIPLE_CAUSES | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE | PARTIAL | DATASET-006 |
| 008 | MATCH | NOT_COMPARABLE | NOT_COMPARABLE | — | NOT_COMPARABLE | DATASET-008 |
| 013 | MATCH | STATUS_CHANGED | MULTIPLE_CAUSES | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE | PARTIAL | LINEAGE-013-015 |
| 015 | MATCH | STATUS_CHANGED | MULTIPLE_CAUSES | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE | PARTIAL | LINEAGE-013-015 |
| 017 | MATCH | STATUS_CHANGED | MULTIPLE_CAUSES | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE | PARTIAL | DATASET-017 |
| 018 | MATCH | STATUS_CHANGED | MULTIPLE_CAUSES | COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE | PARTIAL | DATASET-018 |

## Notas de evidencia

- 008: B1 registró `PIPELINE_FAILED` en `shapes.txt`, registro 1869; no persistió resultados de reglas. B3 registra `EMPTY_CSV_RECORD_IGNORED` y 8 PASS. La clasificación histórica guardada es `PARSER_IMPLEMENTATION_CHANGE`; `NEWLY_OBSERVABLE_DATA_RESULT` queda como interpretación de apoyo. M05-A declara el par no comparable.
- 013, 015, 017 y 018: la identidad de parser también cambió globalmente. La atribución refleja todos los cambios de identidad admitidos por M05-A; no se fuerza una causa única.
- 013 y 015 forman una unidad de lineage; son seis datasets y cinco unidades independientes.
- Las advertencias V1 no están persistidas en B1. No se reconstruyen findings ni listas faltantes.
- La identidad de paquete no se compara porque B1 no la persistió. B3 tampoco persistió la versión global GTFS_Lab; la evidencia queda `PARTIAL`.
- `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0` se conserva como límite contractual; ante esa condición la salida es `NOT_COMPARABLE`.

Fuentes: reports/evidence/holdout_evaluation_v1/first_evaluation_summary.json; reports/evidence/holdout_evaluation_v2/evaluation_summary.json.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
