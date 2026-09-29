# Audit comparison

- Comparison: `CA-20dd6212be68afda`
- Baseline: `TDL-GTFSRUN-7ac901a32b214fdf`
- Candidate: `TDL-GTFSRUN-2e1588590ce0469b`
- Comparability: `PARTIALLY_COMPARABLE`
- Attribution: `DATASET_CHANGE`

## What changed

- Result change: `FINDING_SET_CHANGED`; changed=`True`
- Finding change: changed=`True`
- Supported causes: DATASET_CHANGE

## Identity differences

- `dataset.dataset_id`: `"GTFS-26baf9a07d4b6e3b"` → `"GTFS-57c6720aed07167d"`
- `dataset.source_sha256`: `"26baf9a07d4b6e3b2155bfaa4e82bb7a6bf45550218fc2f711e8cbc425ed0af8"` → `"57c6720aed07167dd8a238fb089542e5331f7b74846fbf25372b421b66acbf0b"`

## Result differences

- `{"change":"FINDING_SET_CHANGED","rule_id":"V1-RULE-GTFS"}`

## Findings added

- `TDLF-3eee5bd97bf432800f45`: `NEW_FINDING`

## Findings resolved

- `TDLF-afeca96b8c509a1cf0ac`: `RESOLVED_FINDING`

## Findings changed

- None

## Unresolved causes

- None

## Evidence references

- `reports/evidence/m05d_productive_sources/baseline/audit/audit_manifest.json`
- `reports/evidence/m05d_productive_sources/baseline`
- `reports/evidence/m05d_productive_sources/candidate/audit/audit_manifest.json`
- `reports/evidence/m05d_productive_sources/candidate`

## Contracts

- Record: `AuditComparisonRecord 1.0.0`
- Snapshot: `1.0.0`
- Change attribution: `1.0.0`
