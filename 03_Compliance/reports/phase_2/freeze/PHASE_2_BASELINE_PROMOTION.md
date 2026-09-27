# Phase 2 — Baseline promotion stopped

PHASE_2_BASELINE_PROMOTION = FAIL
PHASE_2 = NOT_FORMALLY_FROZEN

Recorded at: 2026-09-27T01:12:06.442781+00:00

Blocking check: REQUESTED_GTFS_BASELINE_SHA.
- Requested GTFS SHA (62 characters): `f4186d603c455021b807261bdac8770f5f4d2bed7830214eb98c223efd99fc`.
- Actual and existing baseline GTFS SHA (64 characters): `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance entry SHA: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3` (matches approved candidate).

The supplied GTFS SHA is inconsistent with the preserved official baseline and live file. No correction was inferred. Promotion stopped before metadata changes; the authorized candidate remains unpromoted. Resolve the expected GTFS SHA before repeating the promotion.

Previous official Compliance baseline (Phase 1): `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`. No new official baseline was created. Phase 1 and GTFS history are preserved.

Modified files: none.
Created files: PHASE_2_BASELINE_PROMOTION.md, PHASE_2_BASELINE_PROMOTION.csv, PHASE_2_BASELINE_PROMOTION_FAILURE.json, all in this directory.

Final tests and promoted-document validations: NOT RUN, due to STOP on blocker. Historical freeze review PASS remains evidence of the approved candidate, not a successful promotion. No formal FROZEN record or success hash manifest was created.

Scope: no database writes, corpus changes, decisions recalculated, mappings, audit rules, Gate reopening, Phase 3, git add, commit or push.

Git before:
```text
?? .gitignore
?? 02_Data_Engineering/
?? 03_Compliance/
?? PROJECT_CURRENT_STATE.md
?? project_baseline.json
?? reports/
```

Git after is recorded in PHASE_2_BASELINE_PROMOTION_FAILURE.json. Root Git has no commits; existing untracked groups contain the failure reports.

Final DB SHA and protected-file checks are recorded in PHASE_2_BASELINE_PROMOTION_FAILURE.json.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
