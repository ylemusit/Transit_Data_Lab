# Pilot Audit 01 — Evidence Model Observations

## OBSERVED FACTS

1. GTFS Explorer 0.2.1 exposes three different run-level quantities: detected occurrences (`total_issue_count`), persisted detail (`stored_issue_count`) and omitted occurrences (`omitted_issue_count`).
2. Four pilot runs have complete detail. Bizkaibus reports 1,040,852 detected, 100,000 persisted and 940,852 omitted; it is the only incomplete pilot run.
3. For Bizkaibus, both `summary_by_severity` and the sum of `issues[].occurrence_count` equal 100,000. Neither equals 1,040,852. Both summaries therefore describe persisted occurrences only.
4. The persisted Bizkaibus detail contains four rules, but the outputs do not prove the detected total per rule or whether omitted-only rules exist.
5. `BEST_PRACTICE` is an issue category, not a value in `summary_by_severity`. Category counts can overlap severity counts and must not be added to them as though both dimensions were mutually exclusive.
6. The HTML preserves full run-level detected/stored/omitted totals and persisted details. Its integrity manifest preserves only artifact metadata. Route JSON/ZIP exports are transport-data exports, not validation-evidence exports.
7. A report can be unfiltered by severity/category and still have incomplete detail. Filter completeness and persistence completeness are independent properties.
8. The observed 100,000 persisted rows are consistent with a global persistence ceiling in this run. Existing evidence does not prove a hard-coded limit or internal selection algorithm.

## DESIGN CONSEQUENCES

The future Audit/Quality model should keep these concepts separate:

| Concept | Meaning |
|---|---|
| `DETECTED OCCURRENCES` | Total occurrences detected by validation, including omitted detail. |
| `PERSISTED DETAIL` | Occurrence rows actually available for inspection and evidence. |
| `AUDIT FINDINGS` | Interpreted, deduplicated audit-level conclusions derived from one or more rules/occurrences. |
| `REPRESENTATIVE EVIDENCE` | Bounded samples supporting a finding without reproducing every occurrence. |
| `FULL DETAIL AVAILABILITY` | Explicit statement of whether all detected occurrence detail is available. |

Any aggregate should declare its population explicitly, for example `ALL_DETECTED_OCCURRENCES` or `PERSISTED_OCCURRENCES_ONLY`. A bare `count` is insufficient when detail may be truncated.

Severity and category should remain separate dimensions. In particular, a `BEST_PRACTICE` category count must not be presented as a fifth severity beside `FATAL`, `ERROR`, `WARNING` and `NOTICE` unless a future schema deliberately changes that taxonomy.

Per-rule findings need an explicit evidence-completeness state. When full per-rule detected totals are absent, the model should preserve unknowns rather than equating persisted samples with detected totals.

## Conceptual finding-versus-occurrence model

```text
VALIDATION RULE
    |
    v
OCCURRENCES
    |
    v
AUDIT FINDING
```

Conceptual fields:

| Field | Purpose in this pilot |
|---|---|
| `rule_id` | Stable validation rule identifier. |
| `severity` | Rule/occurrence severity, separate from category. |
| `occurrence_count` | Detected total only when demonstrated; otherwise unknown with a persisted count kept separately. |
| `affected_entities` | Count or set of affected entities when evidence supports it. |
| `coverage_percentage` | Calculable only with a demonstrated denominator and complete numerator. |
| `representative_samples` | Small bounded set of persisted occurrence examples. |
| `evidence_complete` | Whether all occurrence detail supporting the finding is available. |
| `audit_interpretation` | Intentionally not populated in Pilot Audit 01A. |
| `remediation` | Intentionally not populated in Pilot Audit 01A. |
| `legal_reference` | Intentionally not populated in Pilot Audit 01A. |

This structure can represent millions of occurrences without placing every row in a human report, provided the implementation preserves exact detected aggregates independently of bounded representative samples. Pilot 01A demonstrates the need for that separation; it does not prove that GTFS Explorer 0.2.1 already retains the necessary all-detected per-rule aggregates.

## Requirement-model gate

The existing evidence is insufficient to define reliable per-rule detected coverage for large runs. Before basing Audit/Quality requirements on rule occurrence totals, the detailed-evidence architecture must establish how complete per-rule aggregates survive bounded detail persistence.
