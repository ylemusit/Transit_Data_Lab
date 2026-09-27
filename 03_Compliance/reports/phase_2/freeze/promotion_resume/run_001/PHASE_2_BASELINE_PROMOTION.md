# Phase 2 baseline promotion — resumed

PHASE_2_BASELINE_PROMOTION = PASS
PHASE_2 = FROZEN
corrected_gtfs_sha = f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc
gtfs_sha_length = 64
GTFS_BASELINE_VALIDATION = PASS
DB_SHA_BEFORE = 823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3
DB_SHA_AFTER = 823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3
DB_CHANGED_DURING_BASELINE_PROMOTION = NO
previous_official_compliance_baseline_sha = 52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5
new_official_compliance_baseline_sha = 823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3
phase_1_baseline_preserved = True
gtfs_baseline_preserved = True
provisions = 92
source_facts = 36
requirements = 48
deadlines = 10
external_dependencies_partial = 7
gate_1 = CLOSED
gate_2 = CLOSED
materialization = PASS
freeze_review = PASS
legal_hashes = PASS (10/10)
baseline_validation = PASS
current_state_validation = PASS
blocking_issues = []
PROJECT_BASELINE_UPDATED = YES
PROJECT_CURRENT_STATE_UPDATED = YES
READY_FOR_PHASE_3_PLANNING = YES
previous_failure_class = PRECONDITION_INPUT_ERROR
previous_failure_reason = INCORRECT_EXPECTED_GTFS_SHA_IN_INSTRUCTION
previous_database_mutation = NO
previous_baseline_mutation = NO
previous_current_state_mutation = NO
previous_git_actions = No staging/commit evidenced by historical report, unchanged status and unborn repository; no independent network telemetry for push.
files_modified = ['project_baseline.json', 'PROJECT_CURRENT_STATE.md']
git_add_performed = False
commit_performed = False
push_performed = False
textual_fidelity_certified = False
legal_compliance_assessed = False
format_mapping_completed = False
audit_rules_created = False
phase_3_started = False

- Annex 1.3 B-I/D-I unresolved source fidelity anomalies
- 7 PARTIAL external dependencies; interpretation pending
- No format mapping
- No audit rules
- Textual fidelity not certified
- Human legal decisions require manual replay; Gate 1/2 report generators are not standalone scripts
- Phase 1 master and Phase 2 pre-materialization mutable assertions mismatch the later state; intact historical evidence preserved
- Three absolute local_file paths are not portable

Original failure .md/.csv/.json remain unchanged in freeze/. This successful report is stored separately to preserve history.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
