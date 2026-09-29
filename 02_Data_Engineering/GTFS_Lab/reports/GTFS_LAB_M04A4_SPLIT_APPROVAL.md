# GTFS Lab M04-A4 — Split approval and freeze

**Verdict:** `M04A_SPLIT_APPROVED_AND_FROZEN`
**Contract:** `CorpusSplit 1.0.0`, status `APPROVED`
**Decision:** `USE_6_DATASET_5_LINEAGE_SPLIT`
**Reviewed against:** Draft PR #7 head `f6f98ec20204ebce071d565ff132b1d989438b98`; base `main` `b363079e5b8c8131f484917098d06b3a12a13eeb`.

## A. Human approval

The approval comes from Yeison Arbey Carrillo Lemus's explicit decision supplied for M04-A4. It selects `USE_6_DATASET_5_LINEAGE_SPLIT` and accepts six HOLDOUT datasets, five independent lineage units, 14 DEVELOPMENT datasets, the atomic 013/015 lineage, and the known provenance and prior-exposure limitations.

| Field | Recorded value |
|---|---|
| `reviewed_by` | `Yeison Arbey Carrillo Lemus` |
| `reviewed_at_utc` | `2026-09-29T12:26:20Z` |
| `review_basis` | Explicit approval of `USE_6_DATASET_5_LINEAGE_SPLIT`, accepting 6 HOLDOUT datasets, 5 independent lineage units, 14 DEVELOPMENT datasets, 013/015 as one atomic unit, and known provenance and prior-exposure limitations. |

No cryptographic signature is claimed.

## B. Final DEVELOPMENT

`001, 002, 003, 004, 005, 007, 009, 010, 011, 012, 014, 016, 019, 020` — 14 datasets.

All documented `KNOWN_DEVELOPMENT_EXPOSURE` datasets (`002, 005, 014, 019, 020`) remain in DEVELOPMENT.

## C. Final HOLDOUT

`006, 008, 013, 015, 017, 018` — six datasets. The set covers families A, B, C, and D. No known-development-exposure dataset is present.

No HOLDOUT ZIP was read, re-hashed, evaluated, or otherwise opened for this approval. No validator or findings were consulted.

## D. Dataset count / lineage count

HOLDOUT contains six dataset records and five independent lineage units. Count each singleton as `DATASET-<id>` and the known pair as one unit:

```ini
DATASET-006 = 1
DATASET-008 = 1
LINEAGE-013-015 = 1
DATASET-017 = 1
DATASET-018 = 1
```

DEVELOPMENT contains 14 datasets. Counts describe allocation and independence; they do not form a quality score.

## E. 013/015 atomic lineage

`013` and `015` remain assigned to `LINEAGE-013-015` and both remain in HOLDOUT. The persisted M04-A2 decision for their pair is `NO` for opposite split sides. The pair contributes one independent lineage unit, not two.

## F. 018 assignment change

Only the `assignment` field for dataset `018` changed within its dataset record: `DEVELOPMENT` → `HOLDOUT`. Its source SHA-256, dataset ID, family/lineage identity, and provenance were preserved. The split status, review record, and canonical split SHA were updated to record this human approval. The M04-A2 lineage matrix was not changed.

## G. New split SHA

The canonical SHA uses sorted dataset IDs and only `dataset_id`, lowercase `source_sha256`, `family_or_lineage`, and `assignment`, serialized as compact UTF-8 JSON with sorted keys.

| State | `split_sha256` |
|---|---|
| Before approval | `b30b1de464984b8c61f41e51279005cf3a32f9a11509e9996803c8f18be261e2` |
| Approved and frozen | `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d` |

The change is expected from 018's reassignment.

## H. Freeze policy

From this approval, `CorpusSplit V1` is frozen. A later dataset move requires a new `split_version`, an explicit reason, and human review. Allowed reasons remain:

- `PROVENANCE_CORRECTION`
- `DUPLICATE_DISCOVERED`
- `LINEAGE_CORRECTION`
- `DATASET_RETIRED`
- `CORPUS_EXPANSION`

A HOLDOUT failure never authorizes silently moving that dataset into DEVELOPMENT. No M04-B result, validator status, finding, or quality observation can amend this freeze.

For the future M04-B report, persist both dataset-level results (six datasets) and independent-lineage-unit-level results (five units). Because 013/015 are one lineage, never describe the six datasets as six independent feeds. Do not create a combined score or a quality percentage.

## I. Split gate

`python -m gtfs_lab.corpus_split_gate --inventory corpus/inventory_v1.json --split corpus/split_v1.json --lineage-review corpus/lineage_review_m04a2.json` — **PASS** (`TDL_CORPUS_SPLIT_GATE_PASS`). The approved contract gate enforces 20 inventory datasets, the exact 14/6 allocation, the approved six HOLDOUT IDs including 018, five HOLDOUT lineage units, families A/B/C/D, no known exposure in HOLDOUT, the atomic 013/015 unit, no split `NO` relation, zero `UNRESOLVED`, complete human review, reproducible split SHA, and rejection of results/runtime outputs and absolute paths.

The persisted M04-A2 matrix was validated separately without rebuilding it or reading source archives:

`python -m gtfs_lab.corpus_split_gate --lineage-review-only --lineage-review corpus/lineage_review_m04a2.json` — **PASS** (`M04A2_LINEAGE_REVIEW_PASS`), 29 pairs: 28 `YES`, one `NO` (013/015), zero `UNRESOLVED`.

## J. Negative tests

- Split contract and approval-policy tests: **20/20 PASS**; covers incomplete review, exposure in HOLDOUT, unresolved lineage, wrong 018 assignment, lineage separation, hash drift, results/runtime outputs, and absolute paths.
- Persisted lineage review tests: **6/6 PASS**.
- Split sensitivity tests: **4/4 PASS**; confirms the chosen six-dataset/five-lineage candidate and the alternatives using input metadata only.

## K. Regression

| Gate | Result |
|---|---|
| M01 Trust Contract | PASS, 12 checks |
| M02 Trust Persistence | PASS, 21 checks; synthetic gate evidence only |
| M03-A Golden Contract | PASS, 18 checks |
| Golden Corpus | PASS, approved corpus identity unchanged |
| Golden Evaluator | PASS, 11 checks |
| Golden Regression | PASS, both approved synthetic cases and negative expectations |
| GTFS_Lab V1 synthetic/current gate | PASS; synthetic fixtures only |
| Compliance V1 current gate | PASS; details and protected hashes below |
| Python compile | PASS for all changed Python modules/tests |
| `git diff --check` | PASS |

The Compliance V1 current gate used the operational checkout because the protected Compliance database is excluded from the isolated PR worktree. Its gate and evaluator sources match this PR worktree. The fixture writer has a later newline-portability correction in the operational checkout; the phase SQL differs only in checkout line endings. The gate ran read-only against the registered Compliance state and wrote evidence outside the repository. Phase 1: 22 current checks passed. Phase 2: 386 checks passed; the one preserved historical `UNCHANGED_COUNT_audit.rules` assertion is explicitly excluded by the current gate. Protected Compliance database SHA-256 remained `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` before and after. Protected GTFS raw SHA-256 remained `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`.

No full provenance archive re-hash was run.

## L. Golden integrity

Golden Corpus V1 remains `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3`. No Golden cases or manifest entries were modified. The Golden Corpus, Evaluator, and Regression gates passed; regression executed only its two approved synthetic cases.

## M. Files changed

- `corpus/split_v1.json` — approved allocation, human review, and new split SHA.
- `gtfs_lab/corpus_split_gate.py` — strict approved-split and persisted-lineage checks.
- `tests/test_corpus_split_gate.py` — approved contract and negative tests.
- `tests/test_split_sensitivity.py` — sensitivity assertions aligned with the adopted scenario.
- `reports/GTFS_LAB_M04A3B_SPLIT_SENSITIVITY_REVIEW.md` — recommendation marked as adopted decision.
- `reports/GTFS_LAB_M04A4_SPLIT_APPROVAL.md` — this closure and freeze record.
- `02_Data_Engineering/GTFS_Lab/README.md` and `PROJECT_STATUS.md` — current project status.

## N. Commit / PR

To be recorded after the approval changes and gates are committed. PR #7 remains the target Draft; do not merge or mark Ready.

## O. Verdict

`M04A_SPLIT_APPROVED_AND_FROZEN`.

This is not `M04_MERGED_AND_VERIFIED` and does not declare `TDL_TRUST_FOUNDATION = PASS`. HOLDOUT remains unopened. M04-B remains unstarted.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
