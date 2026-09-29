# GTFS_Lab M04-B1 — First controlled HOLDOUT evaluation

**Checkpoint classification:** `HOLDOUT_EXECUTION_PARTIAL`

**Verdict:** `M04B1_CHECKPOINT_PRESERVED_AND_RECONCILED`

**Execution result:** `HOLDOUT_EXECUTION_PARTIAL`

## A. Evaluation and access identity

- Evaluation: `TDL_HOLDOUT_EVALUATION_V1`; access: `ACCESS-20260929T132226Z-M04B1-01`.
- Started: `2026-09-29T13:22:26Z`; completed: `2026-09-29T13:27:00Z`.
- Isolated branch: `feat/tdl-trust-foundation-m04b-holdout-evaluation`; start worktree was clean.
- Runtime outputs: `C:\Users\yeiso\Desktop\Folder\VSCode\Proyectos\Transit_Data_Lab_m04b_runtime\TDL_HOLDOUT_EVALUATION_V1` (outside the checkout).
- Pre-open record: [access_record.json](evidence/holdout_evaluation_v1/access_record.json); source hashes: [source_identity.json](evidence/holdout_evaluation_v1/source_identity.json); machine summary: [first_evaluation_summary.json](evidence/holdout_evaluation_v1/first_evaluation_summary.json).

## B. Engine and ruleset identity

- Git commit: `9b3a5c1207e77ae69d14e254bf560f365302e7e7`; GTFS_Lab `1.0.0-dev`; parser `gtfs-lab-csv/1`; validator `1.0.0`.
- Ruleset: `gtfs-lab-v1`; registered ruleset version `1`; M02 audit manifests record the executed per-rule versions as `1.0.0,compliance-v1/1`. AuditManifest: `1.1.2`.
- Compliance rule `V1-RULE-GTFS`; evaluator SHA-256 `efa87d537109c26c1921e32f896359e280f09e2d6cf579f61a5c2f804afa3b70`; reference SHA-256 `1ff40b8001b180bd023dd6f1899907aecbcb4600c8dbcb6fc6c841a50839b147`.
- Five completed pipelines persisted accepted M02 manifests with the same engine identities. Dataset 008 failed before Trust audit manifest creation.

## C. Split identity

- `TDL-CORPUS-SPLIT-V1`, `CorpusSplit 1.0.0`, status `APPROVED`; SHA-256 `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d`. Split and persisted lineage gates passed before first access.
- HOLDOUT: `006, 008, 013, 015, 017, 018` — **6 datasets / 5 independent lineage units**. `013 + 015 = LINEAGE-013-015`.

## D. First HOLDOUT access

- First source ZIP hash access recorded at `2026-09-29T13:23:48Z`, after the pre-open access record and engine identity had been persisted. All six entry hashes match frozen split metadata.
- One path-resolution attempt at `2026-09-29T13:23:19Z` failed before any source file was opened; the attempt remains recorded in `access_record.json`. The first actual source ZIP hash access occurred at `2026-09-29T13:23:48Z`.

## E. Dataset identities and outcomes

| Dataset | Lineage unit | Hash | Pipeline | Rules | PASS | FAIL_TECHNICAL | WARNING | NOT_EVALUABLE | INSPECTION_ERROR | Tool defect |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 006 | DATASET-006 | MATCH | PIPELINE_COMPLETED | 8 | 8 | 0 | 0 | 0 | 0 | No |
| 008 | DATASET-008 | MATCH | PIPELINE_FAILED | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 013 | LINEAGE-013-015 | MATCH | PIPELINE_COMPLETED | 8 | 7 | 0 | 0 | 0 | 1 | No |
| 015 | LINEAGE-013-015 | MATCH | PIPELINE_COMPLETED | 8 | 7 | 0 | 0 | 0 | 1 | No |
| 017 | DATASET-017 | MATCH | PIPELINE_COMPLETED | 8 | 7 | 0 | 0 | 0 | 1 | No |
| 018 | DATASET-018 | MATCH | PIPELINE_COMPLETED | 8 | 7 | 0 | 0 | 0 | 1 | No |

Counts are descriptive observations, not scores. `PIPELINE_COMPLETED` means the normal pipeline completed and its trust artifacts were accepted; rule-level inspection errors remain visible separately. Dataset 008 has zero rules executed because ingestion failed.

## F. Lineage-level outcomes

- `DATASET-006`: completed; 8 rules PASS.
- `DATASET-008`: pipeline failed at ingestion; no rules executed.
- `LINEAGE-013-015`: both dataset results are preserved; each pipeline completed, and each has one Compliance V1 `INSPECTION_ERROR`. Count this pair once for independence.
- `DATASET-017`: completed with one Compliance V1 `INSPECTION_ERROR`.
- `DATASET-018`: completed with one Compliance V1 `INSPECTION_ERROR`.

## G. Rule/status summary

- Across five completed datasets: 40 rule results — 36 `PASS`, 4 `INSPECTION_ERROR`; zero `FAIL_TECHNICAL`, `WARNING`, or `NOT_EVALUABLE`. No normalized findings were emitted by the completed runs.
- Four inspection errors are only `V1-RULE-GTFS`. The evaluator reports its existing limits of 10,000 rows and 1 MiB per file: 013 exceeds the row limit (11,988 stop_times); 015/017 exceed the per-file byte limit in stop_times (1,895,477 / 3,832,520 bytes); 018 exceeds both (15,224 trips; 11,068,499 stop_times bytes). They are safely reported as `INSPECTION_ERROR`, not as operator findings.
- Dataset 008: `INGESTION_ERROR`, `shapes.txt` record 1869 had 0 fields against a 4-column header. It is provisionally classified `DATA_AMBIGUITY` pending separate reproduction/interpretation; no engine defect is asserted.

## H. Tool defects and data ambiguities

- Confirmed tool defects: none. The size/row boundaries are existing evaluator limits, provisionally `SCALE_LIMIT`.
- Dataset 008 is provisionally `DATA_AMBIGUITY`: first-run evidence shows a blank CSV record and a safe ingestion stop; this checkpoint did not decide whether the source record or parser tolerance is responsible.

## I. Execution limitations

- One of six pipelines failed before rule execution (008); therefore the checkpoint is partial.
- The M02 pipeline left a partial extracted run directory for 008 (`GTFSRUN-ce95344c5c2e47e5`) in the external runtime location, in addition to the persisted ingestion-error run. It is retained as original execution evidence and is not committed.
- Compliance V1 could not inspect all four larger feeds within its frozen limits. Other GTFS_Lab rules completed successfully for those four.

## J. Reproducibility evidence

- Entry SHA-256 matched for all six sources. The five completed M02 manifests record `INPUT_INTEGRITY_VERIFIED` and matching source hashes before/after their pipelines.
- Each first-run `run_id`, run JSON, validation, accepted manifest, normalized findings, report, DuckDB and generated exports are referenced under the external runtime root; dataset 008 has its run/error report and partial work directory.
- A same-engine `REPRODUCTION_RUN` was not performed.

## K. No-fix declaration

No validation rule, parser, threshold, configuration, split, or source ZIP was changed after results became visible. The first observations have not been overwritten.

## L. Next decision

Preserve this partial checkpoint. If investigation of dataset 008 or the known Compliance V1 scale limits is authorized, reproduce those behaviors on DEVELOPMENT/synthetic inputs first; any changed engine requires a new checkpoint version. This report does not declare M04 complete and does not start M05.

## M. Existing regression

| Gate | Resultado |
|---|---|
| M01 Trust Contract | PASS — 12/12 |
| M02 Trust Persistence | PASS — 21/21; fixtures sintéticos |
| M03-A Golden Contract | PASS — 18/18 |
| Golden Corpus | PASS — 2 casos; SHA `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3` |
| Golden Evaluator | PASS — 11/11 |
| Golden Regression | PASS — 2 casos sintéticos aprobados |
| Split gate | PASS |
| Lineage gate | PASS |
| GTFS_Lab synthetic/current | PASS — suite, E2E sintético y GIS direccional |
| Compliance V1 current | PASS — Phase 1: 22 checks; Phase 2: 386 checks actuales. Se preservó una aserción histórica `UNCHANGED_COUNT_audit.rules` (expected 0, actual 2), fuera del conteo vigente. |
| `compileall` (`gtfs_lab`, `tests`) | PASS |
| `git diff --check` | PASS |

Las evidencias de regresión se escribieron fuera del checkout en `C:\Users\yeiso\Desktop\Folder\VSCode\Proyectos\Transit_Data_Lab_m04b_runtime\TDL_HOLDOUT_EVALUATION_V1\regression. Las bases protegidas se copiaron al worktree aislado solo después de verificar sus hashes; el gate de Compliance las abrió en modo read-only. Los hashes de origen y de las copias coinciden después del gate.

## N. Integridad de activos protegidos

| Activo | SHA-256 esperado | Resultado |
|---|---|---|
| Golden Corpus | `29ae937e3abcf8baad21d998d81c4357defe2530f9da17be370aa2b1a6dce1e3` | MATCH; gate PASS |
| Split aprobado | `7d39fc1eb3cbd9c9382c20fc30950a1cbee29befdb28bff0787b41e56111e52d` | MATCH; gate PASS |
| Compliance DB | `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B` | MATCH antes y después |
| GTFS_Lab DB | `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC` | MATCH antes y después |

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
