# M06-B02C Scope Schema Migration

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Authorization

```text
M06_B02C_PARTIAL_MAPPING_CONTRACT = APPROVED
SCOPE_UNIT_MODEL = APPROVED
PARTIAL_MAPPING_POLICY = APPROVED
RRP_SERVICE_GRANULARITY = APPROVED
VERSIONED_PROFILE_REFERENCES = APPROVED
PROVENANCE_CONTRACT = APPROVED
SCHEMA_MIGRATION = AUTHORIZED
B02_MAPPING/CAPABILITY/SCOPE/COVERAGE/REPRESENTABILITY/AUTOMATABILITY/AUDIT_RULE_PERSISTENCE = NOT AUTHORIZED
```

Only schema infrastructure was created. No mappings, capabilities, bridges, scope units, source-reference assignments, or other B02 records were inserted.

## Approved architecture

The design uses a scope unit as a child of an existing concept–mapping bridge:

```text
requirement concept → mapping → capability → concept-mapping bridge → scope unit → source reference(s)
```

This keeps scope local to each reviewed concept/mapping pair. It does not introduce global evaluated-scope identities or infer scope for legacy mappings.

## Pre-state

Branch `main`; pre-existing local modifications and untracked files were preserved. The pre-migration DB SHA-256 was `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`.

| Precheck | Value |
|---|---:|
| Requirements | 48 |
| Provisions / source facts / deadlines | 92 / 36 / 10 |
| Persisted B02 concepts | 7 (1 P01, 6 P02) |
| Global substantive mappings / B02 mappings | 6 / 0 |
| Concept-mapping bridges / B02 bridges | 0 / 0 |
| Global coverage / B02 coverage | 8 / 0 |
| Representability / observed evidence / audit.rules | 0 / 0 / 0 |
| Global automatability / B02 automatability | 6 / 0 |
| New scope objects / disposition vocabulary | absent / absent |

The six legacy mapping IDs were checked against the expected set. `M06_B02A_REQUIREMENT_CONCEPTS = CHECKPOINTED` is recorded in the current project status and independently confirmed by the populated-schema and B02A validators.

## Migration

Migration file: [`011_phase_3_m06_b02c_scope_units.sql`](../../sql/00_setup/011_phase_3_m06_b02c_scope_units.sql).

Executed with DuckDB 1.5.5 against `03_Compliance/databases/transit_compliance.duckdb` using the CLI file runner. The transaction runs fail-fast prechecks, snapshots protected rows, creates additive objects, verifies zero rows and exact unchanged protected data, then commits. Any SQL error or failed postcheck aborts the transaction. Rerunning fails before writes because the objects/vocabulary already exist; it is single-run and fail-safe, not a seed.

## Objects created

- `mapping.phase3_mapping_scope_units`: stable `scope_unit_id` primary key; concept/mapping identity; `unit_code`, name and definition; disposition; basis, limitation, rationale and review/provenance fields.
- `mapping.phase3_scope_source_references`: many-to-many bridge to existing `phase3_source_references`, with a controlled evidence role.
- `MAPPING_SCOPE_DISPOSITION` vocabulary values: `INCLUDED`, `UNRESOLVED`, `EXCLUDED`.
- Three supporting indexes for mapping, concept and source-reference lookups.

## Mapping contract changes

No existing mapping table, row, status, or constraint was altered. Existing mapping vocabulary already has `PARTIAL`; mapping review remains a separate dimension. The schema can therefore represent a future `PARTIAL` mapping with an accepted-with-limitations review without coupling the two statuses. No such mapping was inserted.

## Scope-state vocabulary

`INCLUDED` means the unit is demonstrated by reviewed mapping evidence; a persisted included row requires an approved review with reviewer and date. `UNRESOLVED` means relevant but not demonstrated, and `EXCLUDED` means explicitly determined outside this mapping. Unresolved and excluded rows require a rationale. These dispositions are not coverage outcomes.

Each unit has a stable primary key and is constrained by a composite foreign key to an existing `(concept_id, mapping_id)` bridge. `UNIQUE(concept_id, mapping_id, unit_code)` prevents duplicate unit codes within that evaluated pair, matching the approved design. No `ALL`, `UNKNOWN`, or inferred units were created.

## Source-reference model

The new bridge references `phase3_source_references` by FK, preserving its structured source ID, specification name, version, section, URL/document ID and retrieval/review dates. A source record may be linked to multiple units and each unit may link multiple sources. `evidence_role` distinguishes `SUPPORT`, `BOUNDARY`, and `COUNTEREXAMPLE`. Profile version remains in the existing source-reference registry; no parallel profile registry or free-text substitute was created. The source's capability-to-mapping alignment remains a semantic validator responsibility when data is eventually authorized.

## Legacy preservation

The exact six legacy mapping IDs and substantive rows remain unchanged. There are zero legacy scope assignments. No backfill or reinterpretation was performed.

## B02 state

| Layer | After migration |
|---|---:|
| Concepts | 7 |
| Mappings / concept bridges | 0 / 0 |
| Scope units / scope-source bridges | 0 / 0 |
| Coverage / representability / observed evidence | 0 / 0 / 0 |
| Automatability / audit.rules | 0 / 0 |

## Validators

All SQL validators ran read-only with `duckdb -no-init -batch -bail -readonly -json -f <file>`; every command exited 0.

| Validator | Result |
|---|---|
| M06-B02C Scope Schema | PASS, 26 checks, 0 failures |
| Populated schema gate | PASS, 13 checks, 0 failures |
| M06-B02A concepts | PASS, 11 checks, 0 failures |
| Phase 3 Level A | PASS; 6 mappings/capabilities, invalid references/states/reasons = 0 |
| M04 | PASS; 5/5 expected mappings valid, 0 accepted mappings, 0 unexpected exceptions |
| M04B | PASS; 0 structural failures, 8 coverage decisions, 6 reviews |
| M05B | PASS; 41 HIGH, 7 MEDIUM, 0 LOW; 0 failures |
| M06-B01 | PASS; 0 structural failures |
| Global exception accounting | PASS; 3 M04 + 3 B01, none unaccounted |

The historical empty-schema validator was not used as a current gate and its expectations were not changed.

## Idempotence / execution behaviour

Single-run fail-safe. The transaction's object/vocabulary precheck rejects a repeat before any DDL. Precheck failures abort; postcheck failures raise an error inside the transaction and roll back. The committed run reported `M06B02C_PRECHECK_PASS` and `M06B02C_POSTCHECK_PASS` (CLI exit 0).

## DB hash before/after

- Before: `9AA7065ABBDF52B152D888B688071F3F2FC35EF251D83317D04DD81BB4DF8EB6`
- After: `0175895ED430FC11698B5D6A0B9D9288B251175893549CC4EA5F2D29B008070F`
- The hash delta is the authorized schema and three vocabulary records only. Scope/data tables remain empty.

## Protected invariants

Migration pre/post snapshots and the selected gates confirm Phase 1/2 counts remain 92 provisions, 36 source facts, 48 requirements and 10 deadlines. Six legacy mappings and their IDs remain present. Global coverage remains 8, representability 0, observed evidence 0, automatability 6 and `audit.rules` 0. B02 remains 7 concepts and 0 mappings, bridges, scopes, coverage, representability, observed evidence, automatability or audit rules.

## Limitations

The schema supplies structural anchors only. It does not prove a semantic crosswalk, exact profile release, source-to-mapping consistency, completeness of evaluated scope, representability, observed implementation, coverage or legal compliance. `decision_document_id` and `milestone_id` are provenance pointers, not foreign keys to a document registry. Those future checks require their authorized data gate.

## Next gate

`M06_B02C_SCOPE_SCHEMA = ACTIVE`; `M06_B02A_REQUIREMENT_CONCEPTS = CHECKPOINTED`; `M06_B02 = IN_PROGRESS`; `B02_MAPPING_PERSISTENCE = NOT_AUTHORIZED`. Any future capability/mapping persistence requires its own explicit authorization and readiness gate. No mapping or capability work is authorized by this migration.
