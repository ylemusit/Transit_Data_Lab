# GTFS Lab M04-A3b — Split sensitivity review

**Verdict:** `M04A_SPLIT_SENSITIVITY_DECISION_RECORDED`
**Base proposal at analysis time:** `corpus/split_v1.json` was `UNDER_REVIEW`; M04-A4 records the human decision and changes its status to `APPROVED`.
**Scope:** compare dataset count with independent lineage-unit count using registered input metadata and M04-A2 lineage evidence. No findings, validator outputs, or holdout execution were used. The split contract was not changed.

## A. Why lineage-unit count matters

Generalization is evaluated across source lineages, not merely file entries. Datasets `013` and `015` are one known lineage, `LINEAGE-013-015`, so a holdout containing both has five datasets but four independent lineage units. The two datasets may both remain in HOLDOUT, but reporting them as two independent sources would overstate the holdout's independence.

Counting rule: every singleton unit is `DATASET-<id>` and the atomic pair is one `LINEAGE-013-015` unit. Examples: `DATASET-006 = 1`, `DATASET-008 = 1`, `LINEAGE-013-015 = 1`, `DATASET-017 = 1`. The current holdout therefore has `5 datasets / 4 lineage units`.

## B. Scenario A — current

HOLDOUT: `006, 008, 013, 015, 017`. It contains all four benchmark families, three calendar models, both shape states and both `feed_info` states, and 15 distinct GTFS tables. Its route, stop, and trip count ranges are 276, 2,446, and 4,352. All three corpus-derived size bands are represented. The pair 013/015 stays intact; no known-exposure dataset is in HOLDOUT. DEVELOPMENT contains 15 datasets.

## C. Scenario B — 6 datasets / 5 lineages

Deterministic exhaustive search over six-dataset subsets of non-exposed inputs, requiring 013/015 together, at least five lineage units, and coverage of A/B/C/D, produces the best candidate:

`HOLDOUT: 006, 008, 013, 015, 017, 018`

There are 375 eligible candidates before ranking. Applying the exact M04-A3 lexicographic structural order yields this winner: calendar-model count; shapes states; `feed_info` states; distinct table names; size bands; route-count range; stop-count range; trip-count range; ZIP-size range. Dataset IDs in sorted order break any remaining tie. The candidate retains the current three calendar models, both states for shapes and `feed_info`, and three size bands; it expands table coverage from 15 to 16 and the trip range from 4,352 to 15,222. It has five lineage units because 013/015 count once and 006, 008, 017, and 018 are singletons. It leaves 14 datasets in DEVELOPMENT.

## D. Scenario C — 5 independent lineages / no C

With 013 and 015 in DEVELOPMENT, exhaustive search over five-dataset subsets of eligible singleton lineages does not require family C. There are 1,287 candidates. Under the same structural ranking and deterministic tie-break, the best is:

`HOLDOUT: 006, 008, 012, 017, 018`

It has five datasets and five independent lineage units, covers A/B/D, three calendar models, both shapes and `feed_info` states, 16 distinct tables, and all three size bands. Route, stop, and trip ranges are 56, 529, and 15,222. Its dataset count in DEVELOPMENT remains 15. Family C is absent from HOLDOUT because its only non-exposed lineage is 013/015, which this scenario deliberately leaves in DEVELOPMENT.

## E. Structural comparison

Coverage shorthand: calendar models `3` means calendar-only (`calendar.txt`), both calendar files, and dates-only (`calendar_dates.txt`); shape and `feed_info` columns count represented presence states. Ranges are max-minus-min from inventory input counts or ZIP size. Family coverage lists represented families, not a lineage measure. `Known exposure in holdout` refers to the documented `KNOWN_DEVELOPMENT_EXPOSURE` set. `Lineage violation` records whether a known atomic lineage is split across assignments.

| scenario | dataset_count | lineage_unit_count | development_count | family_coverage | calendar_models | shape_states | feed_info_states | distinct_tables | size_bands | route_range | stop_range | trip_range | known_exposure_in_holdout | lineage_violation |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| A — current | 5 | 4 | 15 | A/B/C/D | 3 | 2 | 2 | 15 | 3 | 276 | 2,446 | 4,352 | NO | NO |
| B — 6 / 5 | 6 | 5 | 14 | A/B/C/D | 3 | 2 | 2 | 16 | 3 | 276 | 2,446 | 15,222 | NO | NO |
| C — 5 / 5, no C | 5 | 5 | 15 | A/B/D | 3 | 2 | 2 | 16 | 3 | 56 | 529 | 15,222 | NO | NO |

Ranking includes ZIP-size range after trip range, with values 1,012,883 (A), 2,957,911 (B), and 2,957,911 (C). This is a lexicographic ordering of separate structural criteria, not a composite score. Size bands are rank-based over the 20 input ZIP sizes, using the M04-A3 groups (ranks 1–7 SMALL, 8–14 MEDIUM, 15–20 LARGE); they describe the corpus and do not imply quality.

## F. Development capacity impact

Scenario B transfers `018` from DEVELOPMENT and leaves 14 development datasets, one fewer than A and C. A and C each leave 15. C keeps both 013 and 015 in DEVELOPMENT while excluding family C from HOLDOUT. This is the direct capacity/coverage trade-off for obtaining five independent holdout units without splitting known lineage.

## G. Holdout independence impact

A has five dataset entries but four independent units. B has six entries and five independent units while retaining family C. C has five entries and five independent units, but no family C coverage. Therefore dataset count alone does not describe independence; future reporting must show both counts and preserve the 013/015 grouping.

## H. Decision adopted

The human decision in M04-A4 adopts `USE_6_DATASET_5_LINEAGE_SPLIT`. The selected HOLDOUT is `006, 008, 013, 015, 017, 018`: six datasets and five independent lineage units, with A/B/C/D and all categorical structural coverage retained. DEVELOPMENT has 14 datasets. This accepts one fewer DEVELOPMENT dataset than A and avoids the family C exclusion of scenario C. The contract approval and freeze policy are recorded in [M04-A4](GTFS_LAB_M04A4_SPLIT_APPROVAL.md).

## I. Human decision required

Decision recorded: Yeison Arbey Carrillo Lemus approved scenario B on 2026-09-29. M04-B remains unstarted and HOLDOUT remains unopened until its separately controlled opening. M04-B must report dataset-level results and lineage-unit-level results; six datasets must not be described as six independent sources because 013/015 form one lineage. No combined score or percentage threshold is defined.

## Reproducibility and gates

`tests/test_split_sensitivity.py` exhaustively enumerates the two candidate sets using only `inventory_v1.json` and the split's current assignments, reproduces candidate counts and winning tuples, and checks the current 5/4 unit count. It does not open source ZIPs or use results. Commands:

```powershell
python -m unittest discover -s 02_Data_Engineering/GTFS_Lab/tests -p "test_split_sensitivity.py" -v
python -m py_compile 02_Data_Engineering/GTFS_Lab/tests/test_split_sensitivity.py
git diff --check
```

The M04-A3 split and contract remain unchanged. This review does not approve a proposal, open HOLDOUT, or begin M04-B.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
