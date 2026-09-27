# Bizkaibus large-run analysis — Pilot Audit 01A

## Scope and evidence

Read-only analysis of the existing GTFS Explorer Desktop 0.2.1 outputs in `FAMILY_D_MATURE_BENCHMARK/019_bizkaibus/03_gtfs_explorer/run_001`. GTFS Explorer was not rerun and no product source was inspected or changed.

Primary evidence:

- `informe-validacion.html`, SHA-256 `49811aa1aaf67ce28c0678ce4f8a9b2578d48ea20f51e853ff9435c435a1cd98`.
- `informe-validacion.html.manifest.json`, which binds that hash and the size `103218958` bytes.
- `data.duckdb`, SHA-256 `893978a20237ad853fd354312916beaee746cd37316d296d973f8429f85bd293`.
- `project.json` and the route-export JSON/ZIP plus their manifests.
- `pilot_01_baseline.csv` and the five existing `parsed_rule_summary.csv` files for the cross-operator comparison.

The HTML embeds a `gtfs-explorer.validation` payload with schema `1.0.0`. Its top-level fields are `batch`, `filter`, `summary_by_severity` and `issues`. The filter is unfiltered (`severities=null`, `categories=null`), but that does not imply complete detail.

## Run counts

| Field | Value |
|---|---:|
| `batch.total_issue_count` | 1,040,852 |
| `batch.stored_issue_count` | 100,000 |
| `batch.omitted_issue_count` | 940,852 |
| Derived `detail_complete` | `false` |
| Number of objects in `issues` | 100,000 |

The arithmetic is internally consistent: `100,000 + 940,852 = 1,040,852`.

## Severity completeness

The exact `summary_by_severity` object is:

| Severity | Count |
|---|---:|
| FATAL | 0 |
| ERROR | 100,000 |
| WARNING | 0 |
| NOTICE | 0 |
| **Sum** | **100,000** |

- `sum(summary_by_severity) == detected_issue_count`: **false** (`100,000 != 1,040,852`).
- `sum(summary_by_severity) == persisted_issue_count`: **true** (`100,000 == 100,000`).

Classification: **PERSISTED_ONLY**.

`BEST_PRACTICE` is not a severity in this report schema. It is an issue `category`; Bizkaibus has zero persisted rows in that category. Therefore it must not be added to `summary_by_severity`. The existing baseline column `gte_best_practice_count` is a category-derived count, not an additional mutually exclusive severity.

## Rule-summary completeness

There is no independent all-detected rule-summary object in the HTML payload. The available `parsed_rule_summary.csv` was derived by grouping `issues` by rule, severity, category, file, field and message key.

| Persisted rule | Persisted rows / occurrence sum | Share of persisted detail |
|---|---:|---:|
| `GTFS_STOP_TIMES_TXT_CONTINUOUS_PICKUP_CONDITIONALLY_FORBIDDEN` | 98,442 | 98.442% |
| `GTFS_STOPS_TXT_WHEELCHAIR_BOARDING_OPTIONAL` | 1,360 | 1.360% |
| `GTFS_ROUTES_TXT_CONTINUOUS_DROP_OFF_CONDITIONALLY_FORBIDDEN` | 99 | 0.099% |
| `GTFS_ROUTES_TXT_CONTINUOUS_PICKUP_CONDITIONALLY_FORBIDDEN` | 99 | 0.099% |
| **Sum** | **100,000** | **100.000%** |

- `sum(issue.occurrence_count) == detected_issue_count`: **false** (`100,000 != 1,040,852`).
- `sum(issue.occurrence_count) == persisted_issue_count`: **true** (`100,000 == 100,000`).

Classification: **PERSISTED_ONLY**.

The full detected count, omitted count and percentage of the detected total cannot be assigned to individual rules from the existing outputs. Those cells are intentionally empty in `bizkaibus_large_run_rule_distribution.csv`. The report proves four rules among persisted details; it does not prove that only four rules were detected across all 1,040,852 occurrences.

## Detail-persistence behaviour

Observed facts:

- Every persisted issue object has `occurrence_count=1`.
- All 100,000 persisted rows are `ERROR` / `FIELD` and use `validation.enum_value_invalid`.
- The four persisted rules occur throughout the stored sequence rather than in four contiguous blocks. Their observed first/last positions are respectively `1/100000`, `55/99969`, `85/99893` and `2998/99754`; there are 3,066 rule transitions.
- Consequently, the first rule does not occupy the persisted capacity exclusively, and all four observed rules retain detail.
- Exactly 940,852 detected occurrences have no row in `issues`.

The evidence is consistent with a **global observed persistence ceiling of 100,000 rows** for this run. It is not sufficient to prove a hard-coded threshold, a per-rule quota, the selection algorithm, whether omitted occurrences belong to these four rules, or whether additional detected rules have zero persisted rows.

## Export coverage

| Artifact | Classification | Evidence retained |
|---|---|---|
| `informe-validacion.html` | `SUMMARY_ONLY` for all detected; `PERSISTED_ONLY` for detail | Complete run-level totals (`detected`, `stored`, `omitted`), persisted-only severity summary, and 100,000 issue rows. No all-detected per-rule summary. |
| `informe-validacion.html.manifest.json` | `SUMMARY_ONLY` | Artifact name, schema version, hash and size only. |
| `data.duckdb` | `PERSISTED_ONLY` plus run-level summary | Existing database artifact is the persistence source identified by `project.json`; its embedded catalogue exposes `validation_runs` fields for total/stored/omitted and `validation_issues`. No separate all-detected per-rule summary was evidenced. |
| Route-export JSON | `UNKNOWN` for validation coverage | Transit selection data and empty `warnings`; no validation or rule fields. Numeric text matches are data values and are not validation evidence. |
| Route-export JSON manifest | `UNKNOWN` | Artifact integrity metadata only. |
| GTFS ZIP | `UNKNOWN` | Nine GTFS data entries; no validation/report/issue/manifest entry. |
| GTFS ZIP manifest | `UNKNOWN` | Export/integrity metadata; no issue distribution. |
| `project.json` | `UNKNOWN` | Project/feed references only. |
| `parsed_rule_summary.csv` | `PERSISTED_ONLY` | Derived grouping of the HTML `issues` array; sum 100,000. |
| Screenshot | `UNKNOWN` | Not a machine-readable occurrence distribution and does not establish per-rule totals. |

No inspected artifact provides `FULL_DETECTED_COVERAGE` at rule or occurrence-detail level. The HTML and database retain the complete run-level detected total, but not complete detected detail.

## Five-operator comparison

`ERROR`, `WARNING` and `NOTICE` below are the report's mutually exclusive severity summary. `BEST_PRACTICE category` is shown separately because it can overlap with `NOTICE`.

| Operator | Detected | Persisted | Omitted | Detail complete | Distinct persisted rules | ERROR | WARNING | NOTICE | BEST_PRACTICE category |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| Ancebus | 12 | 12 | 0 | true | 2 | 6 | 0 | 6 | 6 |
| Viagón | 56 | 56 | 0 | true | 4 | 22 | 0 | 34 | 23 |
| Gilsanz | 1 | 1 | 0 | true | 1 | 1 | 0 | 0 | 0 |
| Kbus | 644 | 644 | 0 | true | 3 | 644 | 0 | 0 | 0 |
| Bizkaibus | 1,040,852 | 100,000 | 940,852 | false | 4 | 100,000 | 0 | 0 | 0 |

Only Bizkaibus loses detail among these five runs. The evidence establishes neither the exact point at which loss begins nor a hard-coded threshold; it establishes an observed 100,000-row persistence ceiling in the sole run above that value.

## Open evidence limits

- Detected occurrence totals per rule are unavailable.
- Omitted occurrence totals and detected-total percentages per rule are unavailable.
- Rules present only among omitted occurrences, if any, are unknowable.
- Severity distribution of the 940,852 omitted occurrences is unavailable.
- The persistence selection/order algorithm is not demonstrated by the outputs.
