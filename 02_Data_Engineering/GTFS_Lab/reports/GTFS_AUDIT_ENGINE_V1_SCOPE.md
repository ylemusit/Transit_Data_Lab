# GTFS Audit Engine V1 — Scope and architecture (G01)

**Baseline reviewed:** `4bb2275d9792942d5c879ca22d01fa250413457f`
**Specification:** official GTFS Schedule Reference, revised 2026-04-27; 32 official Schedule file entries
**Verdict:** `GTFS_AUDIT_ENGINE_V1_SCOPE_READY`

This is an analysis and design result. It adds no productive GTFS rules and does not authorize G02. Review this scope before implementation.

## Authority and evidence

The specification baseline is the [official GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/) and its [revision history](https://gtfs.org/documentation/schedule/change-history/revision-history/). Retrieved 2026-09-30. The reference identifies itself as revised 2026-04-27. The revision history records April 2026 safe-duration fields, February 2026 transfer requirements, earlier changes to conditional `stops.txt`, `feed_info.txt`, GTFS Flex and network files. This is technical specification authority only; it is not legal or regulatory authority.

The machine-readable file catalog is [gtfs_schedule_2026_04_27.json](../spec/gtfs_schedule_2026_04_27.json). It records all 32 current Schedule files and keeps `official_presence`, `official_condition`, and `tdl_v1_support` separate. It is normalized metadata, not a copied replacement for the normative reference. Where the key is shown as `*`, the specification defines all provided fields as the key; `none` means one row. Conditions on the file catalog do not replace field-level presence and forbidden rules.

## Current GTFS_Lab architecture observed

- `ingestion.py` reads ZIP members, applies path/size/CSV safeguards, validates only a small `REQUIRED_COLUMNS` subset, and catalogs a fixed `KNOWN` list of `.txt` files. It does not ingest `locations.geojson`; several newer official files are absent from `KNOWN`. Unsupported and nested files are warned/ignored. Current `REQUIRED` always includes `stops`.
- `validation.py` has a single `_validate()` dispatcher, a global `RULES` map, row scans, and hard-coded applicability/status handling. The active local rules are structural required files/calendar, trip→route/service/shape, uniqueness for four ID columns, and stop/shape coordinate ranges. This is not full schema or field validation.
- `compliance_adapter.py` is a separate narrow fixed-stop references evaluator; its status can be `NOT_EVALUABLE` or `INSPECTION_ERROR`. It is technical Compliance V1 integration, not full Schedule validation.
- `analysis.py` summarizes counts, identifiers and calendar dates. `gis.py` exports stop and selected route/shape GeoJSON/KML. `database.py` builds a per-run DuckDB database. These are analysis/export/storage functions and do not establish conformance for their inputs.
- `pipeline.py` sequences ingestion, compliance adapter, local validation, analysis, GIS, database, report and audit persistence. It assigns overall statuses across components.
- `audit_contract.py` normalizes findings and rule results, constrains status/severity vocabularies, and derives stable finding IDs. `audit_persistence.py` persists evidence and currently derives a rule-version map from emitted results. Neither owns normative GTFS applicability.
- ChangeAttribution 1.0 is legacy; `change_attribution_v1_1.py` implements contract 1.1.0 and compares `identity.rules.rule_versions` by stable rule ID. It can already distinguish per-rule semantic versions when supplied correctly.
- CI and tests include engine preconditions, audit contract/persistence, attribution, pipeline and synthetic fixture coverage. The existing suite protects current behavior; it does not establish full specification coverage.

### Current rules: validity and limits

| Current rule | Assessment | Reason |
|---|---|---|
| `GTFS-REF-TRIP-ROUTE` | `CURRENTLY_CORRECT` in intended fixed-stop subset | Checks non-empty `trips.route_id` against routes when those files are loaded. Missing parents can suppress evaluation, and blank/type/schema handling is incomplete. |
| `GTFS-REF-SERVICE` | `PARTIALLY_CORRECT` | Checks service IDs from calendar files, but does not prove dates, condition triggers, service validity or all required fields. |
| `GTFS-REF-SHAPE` | `PARTIALLY_CORRECT` | Checks supplied shape IDs only when shapes exist; a supplied dangling ID is not caught when shapes are absent. |
| `GTFS-UNIQUE-PRIMARY-ID` | `PARTIALLY_CORRECT` | Checks agency/route/trip/stop IDs only. It does not cover all primary/composite keys and empty values are excluded from `seen` semantics inconsistently. |
| `GTFS-COORDINATE-RANGE` | `PARTIALLY_CORRECT` | Latitude/longitude bounds match the specification for examined stops/shapes, but missing columns, conditional row types and unsupported spatial entities are not schema-aware. |
| `GTFS-STRUCT-REQUIRED` | `OUTDATED_ASSUMPTION` | Hard-requires `stops.txt` even though the reference allows its omission when demand-responsive zones are defined in `locations.geojson`. It also means the ingestion prerequisite rejects some otherwise valid feature shapes. |
| `GTFS-STRUCT-SERVICE-CALENDAR` | `PARTIALLY_CORRECT` | Correctly allows either calendar file to exist, but presence alone does not validate that `calendar_dates.txt` enumerates all service dates when `calendar.txt` is absent. |

Other proven omissions/oversimplifications: `feed_info.txt` is required if `translations.txt` is supplied and recommended otherwise; `levels.txt` is required when pathways include elevators; `networks.txt` and `route_networks.txt` are conditionally forbidden when `routes.network_id` is used; and `stops.txt` presence also affects which stop/location ID references and `stop_times` alternatives are legal. The current engine does not model these applicability branches. File presence metadata and required-column checks are not equivalent to file/field conformance.

## Rule and result model

Keep requirement kind, authority, category and severity as separate fields:

- `requirement`: `REQUIRED`, `CONDITIONALLY_REQUIRED`, `OPTIONAL`, `RECOMMENDED`, `PROHIBITED_WHEN`.
- `authority`: `GTFS_REQUIRED`, `GTFS_CONDITIONAL`, `GTFS_RECOMMENDED`, `TDL_QUALITY`. A rule must cite an exact official anchor or state a TDL heuristic. No legal authority value belongs here.
- `category`: `STRUCTURE`, `SCHEMA`, `TYPE_FORMAT`, `IDENTITY`, `REFERENTIAL`, `TEMPORAL`, `SEQUENCE`, `SPATIAL`, `DATA_CONSISTENCY`, `QUALITY`.
- `severity`: `ERROR`, `WARNING`, `INFO`; derive default severity from authority but permit explicit reviewable overrides. Severity never determines authority. A `QUALITY` finding cannot be presented as a specification violation.
- `status`: `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `NOT_APPLICABLE`, `INSPECTION_ERROR`. A rule only passes after complete evaluation over its declared scope. Unsupported is `NOT_EVALUABLE`, not `PASS`; a false condition is `NOT_APPLICABLE`, not failure.

Represent applicability using a small declarative AST, not executable operator-specific configuration: `FILE_PRESENT`, `FILE_ABSENT`, `FIELD_PRESENT`, `FIELD_VALUE_EQUALS`, `FIELD_VALUE_IN`, `PARENT_ENTITY_EXISTS`, `RELATED_FILE_PRESENT`, `ONE_OF_FILES_PRESENT`, `DEPENDENT_FIELDS`, and boolean `ALL`/`ANY`/`NOT`. Each node has an explicit file/field/column path and operands. Evaluation returns both a truth value and evidence; missing prerequisites propagate `NOT_EVALUABLE`. Make versioned specification metadata data-driven, but keep evaluation logic in typed code for auditable semantics.

Suggested serialized contract (illustrative, with generic conditions and no operator-specific constants):

```yaml
rule_id: GTFS-STRUCT-FEED-INFO-REQUIRED-WITH-TRANSLATIONS
semantic_version: 1.0.0
category: STRUCTURE
authority: GTFS_CONDITIONAL
severity: ERROR
requirement: CONDITIONALLY_REQUIRED
applicable_files: [translations.txt, feed_info.txt]
specification_reference:
  revision: 2026-04-27
  url: https://gtfs.org/documentation/schedule/reference/#feed_infotxt
applicability:
  op: FILE_PRESENT
  file: translations.txt
evaluator: file_presence
```

For field presence/forbiddance, the same tree can express `ALL(FIELD_PRESENT(file=booking_rules.txt, field=booking_type), FIELD_VALUE_EQUALS(...))`. A rule result includes `applicability_status`, `status`, `evaluated_scope`, `checked_records`, and `coverage`. Condition trace records the tested paths and observed values. No serialized condition can name an operator or feed-specific ID.

## Minimum registry architecture

`RuleDefinition` contains `rule_id`, `semantic_version`, `category`, `authority`, `severity`, `requirement`, `applicable_files`, `specification_reference` (URL plus stable heading/field anchor and reference revision), `applicability`, `evaluator` and declared evaluation coverage. An evaluator accepts a read-only dataset view and returns one rule result with status, counts, findings, and inspected/unsupported feature coverage.

`RuleRegistry` is an immutable-at-run-start collection with `register` (reject duplicate IDs and invalid definitions), `enumerate`, `resolve_applicability`, `execute`, and `identity_map`. Execute each independent rule once, isolate evaluator exceptions as `INSPECTION_ERROR`, and retain the declared identity map for every registered rule, including not-applicable and not-evaluable rules. This is a small typed registry, not a plugin framework.

For ChangeAttribution 1.1.0, serialize the map as `identity.rules.rule_versions: {rule_id: semantic_version}`. Rule ID is stable identity; semantic version changes when meaning or evaluation semantics change. Registry version, spec revision, and engine build remain separate identities. Persist applicability and coverage result with each rule so skipped work is visible. The current audit contract has no `NOT_APPLICABLE` result status and includes `WARNING` among statuses; G02 must update/version that contract or add a lossless adapter so status and severity are no longer conflated. Do not serialize `NOT_APPLICABLE` into today's validator unchanged.

## Proposed V1 product scope

V1 targets a general, unknown-provider **scheduled fixed-stop Schedule feed**. It must not require operator-specific code. It validates the feed as supplied without inferring local policies. Engine support means a complete, named set of checks, not an assertion that every optional feature of the entire specification is understood.

### `V1_REQUIRED` — core full audit

- ZIP/root file and CSV structural safety; exact case-sensitive file/field catalog; complete schema and type/format validation for the supported profile.
- Core `agency.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, and `stops.txt` or its applicable conditional alternative; and calendar coverage using `calendar.txt`, `calendar_dates.txt`, or both as permitted by the reference. Do not require both calendar files in every feed. Include conditional presence, keys, references, time/date validity, trip stop sequence and service-date coherence.
- Cross-file identity and referential integrity for all fields exercised by that supported core profile, including parent locations and unique IDs.
- Explicit discovery of every official file plus unknown file, with per-file support/evaluation statuses and report-level coverage; no whole-feed PASS if a detected feature has unevaluated semantics.
- Deterministic findings with stable identity, rule semantic version, source hash, and reference anchor; `PASS` only for fully evaluated rules.

### `V1_SUPPORTED_OPTIONAL` — full V1 technical audit when present

- `shapes.txt`: schema, identity, references, coordinate and sequence checks. This is normative validation where the reference imposes requirements; geometry/route plausibility beyond those requirements is quality analysis.
- `frequencies.txt`: schema, keys, references and interval/time checks.
- `transfers.txt`: schema, key, endpoint references and condition-sensitive fields.
- `feed_info.txt`: fields, keys and conditional requirement when translations are present.
- `pathways.txt`: full deterministic technical conformance for schema, required fields, pathway identity, stop references, pathway mode and bidirectionality domains, applicable conditional fields, and basic technical/referential consistency. Real-world navigation and accessibility quality are out of scope.
- `levels.txt`: full deterministic technical conformance for level identity, `level_index` type, applicable stop references, and the conditional requirement when `pathways.pathway_mode=5`.
- `translations.txt`: full deterministic technical conformance for allowed `table_name`, applicable `field_name`, language, translation, `record_id`, `record_sub_id`, `field_value`, and objectively resolvable references. `feed_info.txt` is required whenever translations are present. Linguistic quality is out of scope.
- GTFS recommended practices can be emitted only as `GTFS_RECOMMENDED` warnings; TDL heuristics only as `TDL_QUALITY` warnings/info, optically and structurally separated from conformance.

### `DEFERRED_WITH_EXPLICIT_LIMITATION`

- **Full GTFS Flex / `locations.geojson`, `location_groups.txt`, `location_group_stops.txt`, `booking_rules.txt`:** complex mutually conditional fixed-stop and demand-responsive representations, GeoJSON validity and trip-window semantics. Detect each present domain and report it as deferred, with affected checks; never silently pass it or produce an operator finding merely because TDL lacks support. `stops.txt` is conditionally required: it may be absent when qualifying demand-responsive zones are represented in `locations.geojson`. G01 establishes this condition awareness only; it does not implement full Flex.
- **Fares V1/V2** (`fare_attributes.txt`, `fare_rules.txt`, `timeframes.txt`, `rider_categories.txt`, `fare_media.txt`, `fare_products.txt`, `fare_leg_rules.txt`, `fare_leg_join_rules.txt`, `fare_transfer_rules.txt`, `areas.txt`, `stop_areas.txt`): extensive independent linked models and conditional composites. Detect present files/features and report `DEFERRED_FEATURE_PRESENT`; inventory only, with no operator finding for unsupported fare semantics.
- **Networks** (`networks.txt`, `route_networks.txt`): detect both files and `routes.network_id`; report present unsupported network semantics as `DEFERRED_FEATURE_PRESENT`, including the official conditional prohibition as unevaluated.
- **`attributions.txt`:** detect and report `DEFERRED_FEATURE_PRESENT`; no silent pass or operator finding for unsupported semantics.
- Any other deferred official domain: detect its files/feature signals, report `DEFERRED_FEATURE_PRESENT` with affected checks and coverage limitation, and do not emit an operator non-conformance solely because the domain is deferred. Unknown or extension files are preserved and reported as unknown/uninspected; never classify them as valid optional features.

Allowed claim: “Dataset evaluated against all applicable rules in the declared GTFS Audit Engine V1 scope.” Forbidden claim: “Dataset fully conforms to every feature in the complete GTFS Schedule specification” unless a future version objectively achieves that coverage. Report specification revision, supported profile and per-feature coverage. A detected official feature outside V1 is `DEFERRED_FEATURE_PRESENT`: a coverage limitation, never `PASS` for that feature and never an operator finding by itself. The exact aggregate status encoding is a G02 design detail; this contract forbids an unqualified whole-Schedule PASS whenever deferred feature semantics are present.

The feature coverage state model is `FEATURE_NOT_PRESENT`, `FEATURE_PRESENT_FULLY_AUDITED`, `FEATURE_PRESENT_PARTIALLY_AUDITED`, and `FEATURE_PRESENT_DEFERRED`. The future machine-readable coverage manifest records, per feature, presence (`PRESENT`/`ABSENT`/`UNKNOWN`), audit support (`FULL_V1_TECHNICAL`/`PARTIAL`/`DEFERRED`), applicability/evaluation status, and the associated limitation. G01 fixes these semantics; G02 designs the schema.

## Gap and capability mapping

See [GAP_MATRIX](GTFS_AUDIT_ENGINE_V1_GAP_MATRIX.md). Program capability IDs and historic wording come from `reports/SERVICE_AUDIT_ALIGNMENT_MATRIX.md`; their definitions are not changed here.

| Capability | G01 disposition |
|---|---|
| SA-002 | `SUPPORTED_BY_CURRENT_CORE`: ZIP/hash/isolated-run ingestion exists for the current catalog. Its extension to the full V1 profile still requires G02/G03 discovery and unsupported-feature reporting. |
| SA-003 | `REQUIRES_ENGINE_V1`: current local rules and Compliance adapter are narrow, not structural conformance coverage. |
| SA-004 | `REQUIRES_ENGINE_V1`: DuckDB pipeline exists, but supported rule execution must prove large-feed completeness; old Compliance V1 cap is not conformance evidence. |
| SA-005 | `REQUIRES_ENGINE_V1`: separate normative validation from recommendation and TDL quality checks. |
| SA-006 | `DEFERRED`: exports exist, but spatial QA methods, CRS/threshold decisions and evidence contracts are not fixed by G01. Core coordinate range checks are in V1. |
| SA-008 | `REQUIRES_ENGINE_V1`: reports exist; require coverage-aware reporting and explicit limitations before presenting an engine audit result. |
| SA-023 | `SUPPORTED_BY_CURRENT_CORE`: audit persistence and report/artifact outputs exist. A portable package with per-rule identity, applicability and complete scope coverage still requires G09. |

## Implementation roadmap (logical blocks)

1. **G02 — Rule Registry + Specification Contract:** typed definitions/registry, conditions, identity map, spec revision and status/coverage contract; preserve legacy behavior through an explicit adapter.
2. **G03 — Structural / Schema / Type:** complete catalog, header, presence, type/format, conditional/forbidden field checks and ingestion support.
3. **G04 — Identity + Referential Integrity:** primary/composite keys and linked IDs across core supported files.
4. **G05 — Service Calendar + Temporal Coherence:** calendar alternatives, exceptions, date ranges, service resolution and temporal edge cases.
5. **G06 — stop_times + Sequence / Operational Coherence:** required/conditional fields, location forms, ordered sequences, times, frequencies; unsupported Flex remains explicit.
6. **G07 — Shapes + Spatial Evidence:** shape schema, sequence/references, coordinates and evidence artifacts; spatial heuristics remain separate.
7. **G08 — Quality / Recommendation Layer:** distinct authority/severity channels, optional evaluation and confidence/context requirements.
8. **G09 — Audit Reporting + Evidence Integration:** coverage summary, rule map to ChangeAttribution 1.1.0, stable findings and durable provenance.
9. **G10 — Development Corpus Evaluation:** authorized DEVELOPMENT fixtures/corpus only; no HOLDOUT access or tuning.
10. **G11 — Engine V1 Closure Gate:** demonstrate rule completeness, supported profile acceptance, unsupported-feature fail-safe reporting, scale and regression gates.

These are logical blocks, not a required PR count. Consolidate only when contracts and evidence remain independently reviewable.

## Test strategy

Every rule needs a positive fixture, negative fixture, boundary case, and a not-applicable/conditional case when relevant; each asserts status, stable finding identity, rule semantic version and exact source reference. Also test missing inputs as `NOT_EVALUABLE`, evaluator exceptions as `INSPECTION_ERROR`, and optional absent features as `NOT_APPLICABLE`. Tests use synthetic fixtures and authorized DEVELOPMENT material only; never HOLDOUT. Registry tests cover duplicate IDs, deterministic ordering, applicability trace, per-rule versions, evaluator isolation and no false aggregate PASS.

## Explicit answers

1. **Full conformance today?** No. Evidence: only seven local rule definitions, narrow fixed-stop Compliance reference checking, partial required columns and a limited ingestion catalog; core and optional semantics are not exhaustively evaluated.
2. **Rules valid unchanged?** `GTFS-REF-TRIP-ROUTE` retains its narrow referential check; coordinate bounds retain their numeric boundaries; supplied service-reference checks remain useful. These remain partial checks, not proof of complete conformance. Others require applicability or coverage corrections before being described as spec-complete.
3. **Conflicting/oversimplified assumptions?** Universal `stops.txt`; calendar file presence treated as enough; fixed supported catalog and required-column subsets treated as sufficient structural integrity; shape references skipped if shapes absent; only four ID sets checked; no complete conditional/forbidden presence model; additional Schedule features are ignored or unsupported.
4. **Exact V1 feature set?** `V1_REQUIRED / CORE FULL AUDIT`: `agency.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, `stops.txt` or applicable conditional alternative, and `calendar.txt` / `calendar_dates.txt` under official conditional semantics. `V1_SUPPORTED_OPTIONAL`: `shapes.txt`, `frequencies.txt`, `transfers.txt`, `feed_info.txt`, `pathways.txt`, `levels.txt`, `translations.txt`. Other objectively selected optional files are not added casually. All remaining official domains are `DEFERRED_WITH_EXPLICIT_LIMITATION` and explicitly detected/reported.
5. **Unknown normal scheduled operator dataset?** `YES`, as the architectural acceptance target, without operator-specific code.
6. **Detected but unaudited official features?** Report `DEFERRED_FEATURE_PRESENT` per feature with affected checks and coverage; it is a coverage limitation, cannot receive feature `PASS`, and is not an operator finding by itself.
7. **Registry sufficient for per-rule versioning?** Yes. Registry identity must include independent stable semantic identity for every rule, including unevaluated/not-applicable rules, serialized compatibly with ChangeAttribution 1.1.0 as `identity.rules.rule_versions: {rule_id: semantic_version}`.
8. **Blocks?** G02–G11 above, with consolidation allowed subject to coherent evidence.

## Review gate

`GTFS_AUDIT_ENGINE_V1_SCOPE_READY`: the product-scope decisions in G01 are resolved. G02 remains a separate milestone and is not authorized by this document.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
