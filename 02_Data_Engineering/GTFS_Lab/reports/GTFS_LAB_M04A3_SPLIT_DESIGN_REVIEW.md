# GTFS Lab M04-A3 — Corpus split design review

**State:** `M04A_SPLIT_READY_FOR_HUMAN_REVIEW`
**Contract:** `CorpusSplit 1.0.0`
**Proposal:** [`corpus/split_v1.json`](../corpus/split_v1.json), status `UNDER_REVIEW`
**Review:** `{}`; no reviewer, review time, or approval recorded.
**Scope:** input metadata, inventory, provenance, and M04-A2 lineage evidence only. No validator outputs or holdout execution were used.

## A. Selection principles

The split estimates generalization to unseen feeds for a deterministic rules engine. Prior evidence of development exposure takes precedence over family balance. Candidate generation is exhaustive over five-dataset subsets of eligible inputs that keep 013–015 atomic and cover families A–D; because 014 is exposure-excluded, this requires the pair plus one A, one B, and one D dataset. Candidate sets are ranked lexicographically by: distinct calendar models; shapes presence states; feed_info presence states; distinct GTFS table names; size bands represented; route-count range; stop-count range; trip-count range; ZIP-size range. Larger structural coverage/range wins at each step; the sorted dataset_id tuple breaks any remaining tie. No scalar score is calculated. Family labels are benchmark cohorts, not lineages.

Structural size bands use ascending `size_bytes` ranks from `inventory_v1.json`: ranks 1–7 SMALL, 8–14 MEDIUM, and 15–20 LARGE. This produces three equal-rank groups (7/7/6) and is descriptive only. Route, stop, and trip counts, table sets, calendar model, shapes, feed_info, provenance confidence, and operator identity are compared directly; no magic score is computed.

## B. Prior development exposure

| Classification | Dataset IDs | Basis |
|---|---|---|
| `KNOWN_DEVELOPMENT_EXPOSURE` | 002, 005, 014, 019, 020 | Pilot Audit 01 documentation records prior source audits and GTFS Explorer analysis for these five benchmark IDs. Conservatively assigned DEVELOPMENT. This records prior analysis; it does not assert the same rules or engine were used. |
| `POSSIBLE_PRIOR_EXPOSURE` | none assigned | No other feed-specific rule-development evidence was found in the reviewed historical documentation. |
| `NO_DOCUMENTED_DEVELOPMENT_EXPOSURE` | 001, 003, 004, 006–013, 015–018 | No feed-specific development use was documented in the reviewed historical records. This is not proof of absolute blindness. |

The older Asturias experiment uses a separate Consorcio de Asturias feed, documented with 41 agencies, 609 routes, and 21,015 trips. No inventory identity among the 20 is documented as that feed. The historical pilot review concerns 002, 005, 014, 019, and 020. Earlier M04 provenance and lineage work did inspect input metadata and structure across the corpus; that prior inspection is a purity limitation, not evidence of findings or rule adaptation. Exposure is not a quality judgment.

## C. Candidate splits

All candidates keep known-exposure datasets 002, 005, 014, 019, and 020 in DEVELOPMENT; keep 013 and 015 together; and use a five-dataset HOLDOUT. The other 15 datasets are DEVELOPMENT. All selected hashes come from the input inventory.

| Candidate | HOLDOUT IDs | Family A/B/C/D | Size bands S/M/L | Input structure and trade-offs |
|---|---|---:|---:|---|
| `CANDIDATE_A` | 001, 008, 013, 015, 016 | 1/1/2/1 | 1/2/2 | Balanced size bands; shapes represented throughout; 008 adds frequencies/transfers/fares and 016 adds levels. Less variation in calendar model than C. |
| `CANDIDATE_B` | 003, 010, 013, 015, 018 | 1/1/2/1 | 1/1/3 | Includes a 15,224-trip feed and shape/route/stops breadth; size is concentrated in LARGE and lacks the calendar-dates-only case. |
| `CANDIDATE_C` | 006, 008, 013, 015, 017 | 1/1/2/1 | 1/1/3 | Covers all three calendar models, shapes present/absent, feed_info present/absent, and 15 distinct table names; input counts span 2–4,354 trips. More LARGE-heavy, but has the broadest categorical structure. |

Size bands and counts use input metadata only. Family C contributes two entries because its sole eligible unit is the indivisible pair 013/015; consequently the preferred 2/1/1/1 split cannot satisfy the lineage constraint at five entries. Family totals in every candidate remain five.

## D. Selected proposal

`CANDIDATE_C` is selected as `PROPOSED_SPLIT`; exhaustive comparison makes it the unique lexicographic winner. It captures all three calendar models (006 calendar-only, the core both-files model, and 017 calendar-dates-only), both shapes and feed_info states, then 15 distinct table names. Its exhaustive lexicographic feature vector is `(3 calendar models, 2 shapes states, 2 feed_info states, 15 tables, 3 size bands, 276 routes range, 2,446 stops range, 4,352 trips range, 1,012,883 ZIP bytes range)` and is the unique maximum among eligible combinations. Candidate A has a more balanced size-band distribution; C accepts the one-small/one-medium/three-large profile to maximize the earlier categorical coverage criteria. This is a documented lexicographic trade-off, not a numeric quality score.

## E. Development set

001, 002, 003, 004, 005, 007, 009, 010, 011, 012, 014, 016, 018, 019, 020 (15 datasets).

## F. Holdout set

006, 008, 013, 015, 017 (5 datasets).

## G. Family distribution

| Family | Corpus | Development | Holdout |
|---|---:|---:|---:|
| A | 7 | 6 | 1 |
| B | 5 | 4 | 1 |
| C | 3 | 1 | 2 |
| D | 5 | 4 | 1 |
| **Total** | **20** | **15** | **5** |

## H. Structural coverage

HOLDOUT size bands: SMALL 006 (1,982 bytes); MEDIUM 008 (126,374 bytes); LARGE 013, 015, 017 (189,716; 443,076; 1,014,865 bytes). Route counts are 2, 8, 129, 278, 31; stop counts 3, 50, 1,321, 2,449, 368; trip counts 2, 75, 554, 1,653, 4,354.

Four have shapes; 006 does not. The three represented calendar models are `calendar.txt` only (006), both calendar files (008, 013, 015), and `calendar_dates.txt` only (017). The selected feeds span 7–12 tables and 15 distinct table names; 008 adds frequency/transfer/fares, 013/015 add complex network and fare structures, and 017 adds `attributions.txt` and `translations.txt`. `feed_info.txt` is present in 006, 008, and 017, and absent in 013 and 015. The inventory reports MEDIUM provenance confidence for all 20; the source resource ID, source URL, and capture date remain unknown for all 20. Operator identity is distinct across the five entries as recorded in provenance.

## I. Lineage constraints

013 and 015 both use `family_or_lineage = LINEAGE-013-015` and both remain HOLDOUT. M04-A2 records 013–015 as the only `NO` relation. No `UNRESOLVED` relations remain, and no `NO` relation crosses assignments. All other entries use an independent `DATASET-<id>` unit; family A–D is not treated as lineage.

## J. Known limitations

- Prior Pilot Audit 01 analysis means the five excluded feeds are not blind. Earlier M04 input/provenance/lineage inspection also limits absolute blindness for every feed; no claim of pristine holdout blindness is made.
- Provenance confidence is MEDIUM, but canonical NAP resource IDs, URLs, and capture dates were not recovered. Hash identity is stable against the registered inventory, not against an independently recovered source registry.
- Family stratification is necessarily 1/1/2/1 because C's available lineage is atomic. Candidate C has three LARGE size-band entries.
- No validator output, finding, status, inferred difficulty, or quality observation influenced eligibility or selection.

## K. Split SHA

Canonical SHA-256 over `dataset_id`, lowercase `source_sha256`, `family_or_lineage`, and `assignment`, sorted by `dataset_id`, compact sorted-key UTF-8 JSON:

`b30b1de464984b8c61f41e51279005cf3a32f9a11509e9996803c8f18be261e2`

Timestamp, review, paths, findings, and runtime identifiers are excluded.

## L. Human review required

The proposal remains `UNDER_REVIEW` with `review: {}`. A human must assess exposure conservatism, the C-family two-entry consequence, candidate trade-offs, and provenance limitations before any approval. This M04-A3 work does not open or execute HOLDOUT, compare motor results, alter rules, or start M04-B.

## M. Regression gates

| Gate | Result |
|---|---|
| M01 Trust Contract | PASS, 12 checks |
| M02 Trust Persistence | PASS, 21 checks; synthetic fixtures only |
| M03-A Golden Contract | PASS, 18 checks |
| Golden Corpus | PASS, two cases; corpus SHA `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3` unchanged |
| Golden Evaluator | PASS, 11 checks |
| Golden Regression | PASS, two approved synthetic cases |
| GTFS_Lab V1 synthetic/current gate | PASS; synthetic fixtures and E2E only |
| Compliance V1 current gate | PASS; protected database SHA unchanged before/after (`4DB39FA5…BC8048B`); GTFS raw SHA `F4186D60…C223EFD99FC` |
| Lineage/provenance unit tests | PASS, 13 tests |
| Corpus split gate | PASS, 20/20 entries |
| Split negative tests | PASS, 12 tests including all four requested rejection cases |
| `py_compile`, `git diff --check` | PASS |

The full `corpus_provenance.py --check` was not rerun after creating the split because it reopens and hashes all source ZIPs, including HOLDOUT. The provenance/lineage regression unit tests use synthetic fixtures; the split gate validated assignment coverage and recorded hashes against the frozen inventory without reading source ZIPs. No HOLDOUT dataset was executed or evaluated.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
