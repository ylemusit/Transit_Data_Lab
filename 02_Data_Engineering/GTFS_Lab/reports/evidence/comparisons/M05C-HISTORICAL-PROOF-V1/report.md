# Audit comparison

- Comparison: `M05C-HISTORICAL-PROOF-V1`
- Baseline: `M04-B1-HOLDOUT`
- Candidate: `M04-B3-HOLDOUT`
- Comparability: `PARTIALLY_COMPARABLE`
- Attribution: `HISTORICAL_MIXED`

## What changed

- Result change: `HISTORICAL_MIXED`; changed=`True`
- Finding change: changed=`None`
- Supported causes: COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE

## Identity differences

- None recorded

## Result differences

- `{"dataset_id":"006","status":"UNCHANGED_STATUS"}`
- `{"dataset_id":"008","status":"NOT_COMPARABLE"}`
- `{"dataset_id":"013","status":"STATUS_CHANGED"}`
- `{"dataset_id":"015","status":"STATUS_CHANGED"}`
- `{"dataset_id":"017","status":"STATUS_CHANGED"}`
- `{"dataset_id":"018","status":"STATUS_CHANGED"}`

## Historical comparisons

- Dataset `006`: result `UNCHANGED_STATUS`; attribution `MULTIPLE_CAUSES`; causes `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE`; evidence `PARTIAL`.
- Dataset `008`: result `NOT_COMPARABLE`; attribution `NOT_COMPARABLE`; causes `none`; evidence `NOT_COMPARABLE`.
- Dataset `013`: result `STATUS_CHANGED`; attribution `MULTIPLE_CAUSES`; causes `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE`; evidence `PARTIAL`.
- Dataset `015`: result `STATUS_CHANGED`; attribution `MULTIPLE_CAUSES`; causes `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE`; evidence `PARTIAL`.
- Dataset `017`: result `STATUS_CHANGED`; attribution `MULTIPLE_CAUSES`; causes `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE`; evidence `PARTIAL`.
- Dataset `018`: result `STATUS_CHANGED`; attribution `MULTIPLE_CAUSES`; causes `COMPLIANCE_EVALUATOR_IMPLEMENTATION_CHANGE, PARSER_IMPLEMENTATION_CHANGE`; evidence `PARTIAL`.

## Findings added

- None

## Findings resolved

- None

## Findings changed

- None

## Unresolved causes

- `BASELINE_WARNING_LIST_NOT_PERSISTED`
- `CANDIDATE_ENGINE_GTFS_LAB_VERSION_NOT_PERSISTED`
- `RULE_SEMANTIC_IDENTITY_SHAPE_UNSUPPORTED_BY_CHANGE_ATTRIBUTION_1_0_0`

## Evidence references

- `reports/evidence/holdout_evaluation_v1/first_evaluation_summary.json`
- `reports/evidence/holdout_evaluation_v2/evaluation_summary.json`
- `reports/evidence/m05c_historical_proof/summary.json`

## Contracts

- Record: `AuditComparisonRecord 1.0.0`
- Snapshot: `M05CHistoricalSourceSnapshot/1.0.0`
- Change attribution: `1.0.0`
