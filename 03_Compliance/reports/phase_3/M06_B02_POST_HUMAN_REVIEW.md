# M06-B02 Post Human Review

Review date: 2026-09-28. This is a documentary post-review report. The Human Review decisions are recorded separately from agent recommendations in `M06_B02_HUMAN_REVIEW.md`. No Compliance database writes, schema changes, capability/mapping/coverage persistence, Phase 1/2 changes, or checkpoint were made.

## Human decisions

| ID | Concept / candidate | Agent recommendation | Human decision — Yeison |
|---|---|---|---|
| C01 | P01 road disruption/status | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C02 | P01 current road-link travel times | ACCEPT_WITH_LIMITATIONS | REJECT |
| C03 | P01 future predicted road-link travel times | HOLD_FOR_RESEARCH | REJECT |
| C04 | P02 road disruption/status | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C05 | P02 current road-link travel times | ACCEPT_WITH_LIMITATIONS | REJECT |
| C06 | P02 future predicted road-link travel times | HOLD_FOR_RESEARCH | REJECT |
| C07 | P02 non-road passenger RT status/disruption | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C08 | P02 access-node/facility status | HOLD_FOR_RESEARCH | ACCEPT_WITH_LIMITATIONS |
| U01 | Annex 2.2(a) parking tariffs | RESEARCH_NOW | RESEARCH_NOW |
| U02 | Annex 2.2(b)(i) shared-vehicle availability/location | KEEP_UNRESOLVED | KEEP_UNRESOLVED |
| U03 | Annex 2.2(b)(ii) on/off-street parking-space availability | RESEARCH_NOW | RESEARCH_NOW |

Counts: 4 accepted with limitations, 4 rejected for this requirement scope, 2 directed research items, and 1 deferred unresolved item. Human decisions do not authorize persistence.

## Accepted with limitations

- **C01:** DATEX II road disruption/status candidate, concept limited to supported road categories. Exact profile/category and applicable model/version remain open.
- **C04:** same road-status concept under P02, only where Article 5(2) DATEX II applicability is established; not all Annex 2.
- **C07:** SIRI EPIP-RT candidate for non-road passenger real-time status, disruptions, delays and cancellations. A concrete Annex-to-service-to-element crosswalk remains required.
- **C08:** SIRI EPIP-RT / SIRI-FM is a conceptual route for station/access-node facility status. Before representability or persistence, document `Annex item → SIRI service → exact element(s)`; do not equate every facility/access-node item.

These decisions accept concepts for later bounded work only. They do not create capabilities, mappings, representability assertions, observed evidence, automatability or audit rules.

## Rejected for current requirement scope

- **C02/C05:** the DATEX II MMTIS Level 2 current road-link travel-time profile may exist technically, but that does not demonstrate that current road-link travel times belong to these B02 requirement scopes derived from Annex 2.1/2.2. `PROFILE_EXISTS != REQUIREMENT_SCOPE_MATCH`.
- **C03/C06:** the same scope rule applies to future predicted road-link travel times. A technical profile does not create an Annex item, a requirement or a legal link.

All four are `REJECT_FOR_THIS_REQUIREMENT_SCOPE`, not `REJECT_STANDARD`. The DATEX II technical evidence is retained for another requirement if a future scope establishes relevance.

## Unresolved research

- **U01:** research completed to the extent of official catalogue, legal and profile evidence; result `PARTIAL` because the exact general-parking profile/version/element set and applicability chain are not established.
- **U03:** research completed to the extent of official catalogue, legal and profile evidence; result `PARTIAL` because the exact MMTIS profile/version/elements and on/off-street scope/applicability chain are not established.

## Deferred unresolved

- **U02:** `KEEP_UNRESOLVED`. The category combines shared cars, bicycles, scooters and other shared vehicles. No common authoritative minimum profile and element crosswalk was demonstrated in the bounded review. Before future research, split by mode/vehicle category; do not create a mapping now.

## U01 research result

**Disposition: `PARTIAL`; no supported mapping candidate is authorized.**

| Chain element | Finding |
|---|---|
| Legal concept | Consolidated Regulation (EU) 2017/1926, Annex 2.2(a): “information service on parking tariffs” for transport on demand and personal transport. This is narrower than a generic parking model. |
| Applicability | Article 5(2) applies to dynamic Annex 2.1/2.2 data to which SIRI and/or DATEX II apply, requiring representation through minimum EU or national profiles. It does not make either standard automatically applicable to every Annex item. The exact parking-tariff-to-standard applicability link was not found in the reviewed authoritative evidence. |
| MMTIS profile evidence | DATEX II's official MMTIS RRP overview explicitly lists parking tariffs under Level 2 “Availability check” and says RRPs contain minimum data elements for the specific delegated-regulation category. This supports a profile-development/catalogue route, but the linked MMTIS documentation does not list a dedicated tariff RRP page alongside its documented LS1, road-link travel-time, alternative-fuel availability and future travel-time profiles. The exact profile and exact tariff elements therefore remain unpinned. |
| Model/version | DATEX II documentation publishes model v3.7 as current on the reviewed portal. That is a model release, not proof that an applicable MMTIS parking-tariff RRP is defined against v3.7. No exact applicable RRP version was found. |
| Tariff/pricing elements | DATEX II's Safe and Secure Truck Parking profile documents rate tables/lines, currency, rate values and free-of-charge representation. But this is RRP 885/2013, designed for truck/commercial-vehicle parking, and explicitly compliant with that separate regulation. These elements show a technical model route only; they do not establish equivalence to the general Annex 2.2(a) category. |
| On-street/off-street | Annex 2.2(a) does not itself distinguish on-street from off-street. The examined truck profile restricts parking usage to truck parking and off-street surface, so it cannot settle general parking scope. No official MMTIS minimum-profile crosswalk by parking location type was found. |
| Article 5(2) | Conditional profile rule; no assumption that the DATEX II truck-parking profile automatically satisfies the Article 5(2) MMTIS duty. A national profile might apply, but none was identified for this research. |

**Research conclusion:** an official DATEX II source places parking tariffs in the MMTIS Level 2 category list; however, a specific applicable minimum profile, version and element mapping for the Annex 2.2(a) requirement were not demonstrated. Do not promote this to `SUPPORTED_CANDIDATE` solely from the existence of the broad model or truck-parking RRP.

## U03 research result

**Disposition: `PARTIAL`; no supported mapping candidate is authorized.**

| Chain element | Finding |
|---|---|
| Legal concept | Consolidated Regulation (EU) 2017/1926, Annex 2.2(b)(ii): available car-parking spaces “on and off-street”, within availability check/location for on-demand and, where relevant, personal transport. |
| Applicability | Article 5(2)'s minimum EU/national profile requirement remains conditional on SIRI/DATEX II applicability. The reviewed sources do not establish a category-specific Article 5(2) bridge for all general parking spaces. |
| Profile | DATEX II's MMTIS overview explicitly lists car-parking spaces available (on and off-street), but offers no linked MMTIS parking-availability profile documentation page. A general parking class or RRP for another legal category is not enough to claim this profile. |
| Version/model | The documentation portal lists DATEX II model v3.7 as current, but no applicable MMTIS parking availability profile/version was established. The Safe and Secure Truck Parking RRP uses CEN/TS 16157-6:2022 (with EN 16157-1) and exposes static/dynamic parking structures, including parking status and occupancy/vacant spaces. Its declared scope is trucks/commercial vehicles under Regulation 885/2013, so it does not establish an on-street and off-street general-car profile. |
| Availability elements | The truck profile specifies `ParkingStatusPublication`, `PlaceStatus`, and `Occupancy.numberOfVacantSpaces`, with status or free-space count. These exact elements are evidenced only within that truck-parking RRP. No official MMTIS general-parking element crosswalk was located. |
| On-street/off-street | The legal Annex explicitly includes both. The truck RRP restricts usage to truck parking/off-street surface. The required general on-street and off-street split is therefore unresolved. |
| Article 5(2) | A generic DATEX II Parking model is not equivalent to a minimum EU/national profile applicable to this requirement. No such exact applicable profile was demonstrated in the bounded research. |

**Research conclusion:** official MMTIS catalogue evidence recognizes the category, and DATEX II has parking model elements/profile material for truck parking; neither closes the applicable general-car minimum profile and element chain for both on-street and off-street parking. Keep `PARTIAL` and unpersisted.

### Authoritative sources consulted

- [Consolidated Regulation (EU) 2017/1926, 2024-03-04, EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2017/1926/2024-03-04/eng) — Article 5 and Annex 2.2(a), (b)(ii).
- [DATEX II Recommended Reference Profiles — MMTIS](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/) — scope of RRPs, MMTIS profile/category catalogue, and links to published MMTIS documentation.
- [DATEX II Safe and Secure Truck Parking RRP](https://docs.datex2.eu/recommended-profiles/rrp/truck-parking/) — CEN/TS 16157-6:2022, truck-only scope, model elements and explicit Regulation 885/2013 context.
- [DATEX II v3.7 model release](https://docs.datex2.eu/downloads/modelv37/) — model release information; not evidence of an MMTIS parking RRP version.
- [Delegated Regulation (EU) 2022/670, EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng) — current RTTI context. It does not by itself establish the MMTIS Annex 2.2 parking-profile mapping.

Consulted 2026-09-28. All are official legal or standards/profile sources. Absence of a located profile page is reported as a bounded research gap, not proof that no national profile exists.

## Cardinality finding

### A. Original intent and current schema

The prompt's premise that the schema has `UNIQUE(requirement_id)` is contradicted by source and live schema evidence:

- M02 framework prose explicitly describes the relation as N:M between `compliance.requirements` and reusable capabilities.
- Migration `005_phase_3_m02_mapping_framework.sql` defines `UNIQUE(requirement_id, capability_id)`, with a distinct `mapping_id` primary key. It does **not** define uniqueness on `requirement_id` alone.
- M06-B01 migration `009_phase_3_m06_b01_unbound_capabilities.sql` reconstructs the table and preserves that same pair uniqueness.
- Read-only inspection of the live DB on 2026-09-28 confirmed `PRIMARY KEY(mapping_id)`, `UNIQUE(requirement_id, capability_id)`, and FK to `phase3_capabilities`; six non-synthetic mappings currently exist.
- M04 already demonstrates multiple capabilities for a requirement: two mappings for `EU-2017-1926-REQ-A04-P01-001` and two for `EU-2017-1926-REQ-A08-P03-001-01`. M04B keeps per-mapping semantic reviews separate from requirement-level coverage; M05B adds family metadata, not mapping cardinality. B01 adds a mapping and capability reuse without changing pair uniqueness. Validators include fixed expected sets/counts and global exception accounting, so future additive B02 rows require scoped validator review.

Therefore Phase 3 was intentionally designed to allow requirement↔capability N:M. The concrete B02 limitation is finer-grained semantic scope: the mapping table has no explicit `requirement_concept`/coverage-component identifier, and the capability catalogue describes reusable concepts. Encoding multiple concepts that share one capability only in free-text conditions/limitations is weak for legal traceability, coverage roll-up, and future audit rules. Do not claim the pair uniqueness is a one-mapping-per-requirement contract.

### B. B02 concept shape

```text
P01
└── road status/disruption (C01 accepted with limitations)

P02 (conditional Article 5(2) applicability)
├── road status/disruption (C04 accepted with limitations; road scope only)
├── SIRI passenger RT status/disruption (C07 accepted with limitations)
├── SIRI facility/access-node status (C08 accepted with limitations)
├── parking tariffs (U01 partial research; no mapping)
└── parking availability, on/off-street (U03 partial research; no mapping)
```

- C01 and C04 describe a similar technical concept reused across two distinct legal requirements. They are complementary requirement-scoped relationships, not alternatives.
- Within P02, the three accepted concepts are complementary scoped concepts. The candidate capability IDs are distinct for road status, passenger status and facility status; the road status capability is reusable under P01/P02.
- C02/C05 and C03/C06 are rejected for this requirement scope and must not be persisted as B02 mappings. Their DATEX II evidence may be reused only in a future requirement whose scope supports it.
- U01/U03 remain future concept candidates with no capability/mapping decision. U02 remains deferred and likely requires mode-level decomposition before research.
- A requirement-level coverage decision should aggregate scoped concept components and conditions; one accepted mapping cannot imply whole-requirement coverage.

## Schema options

### Option A — direct N:M

Keep `phase3_requirement_capabilities` as the direct requirement↔capability relation and use multiple capability rows per requirement.

- **Legal traceability / granularity:** requirement and capability IDs are traceable, but Annex item and applicability condition remain mostly prose. Same capability reused for multiple concepts under one requirement has no structured discriminator.
- **Duplication / reuse:** low duplication; capability reuse works well across P01/P02. Duplicate requirement-capability pairs are already prevented.
- **Coverage / representability:** requirement coverage is separate today, but component completeness cannot be calculated reliably; capability representability can be assessed, while its legal applicability may remain ambiguous.
- **Observed evidence / automatability / audit.rules:** mapping IDs can anchor evidence and automation, but checks cannot reliably select the Annex concept or distinguish required/conditional components without parsing prose.
- **Migration / M04/B01 / validators:** no schema migration needed; existing IDs, reviews, coverage and history remain intact. New rows still affect hard-coded M04/M05B/B01 counts, exception accounting and any broad validators; scope filters and additive B02 validators would be needed.
- **Idempotence / DuckDB / reports:** simple pair-based idempotence and joins; easy SQL, but reports show a flat mapping list and lose requirement decomposition.
- **Frozen/history risk:** low DB risk if rows were later added, but risk of semantic overstatement remains. No frozen rows need reconstruction.

### Option B — requirement concept layer

Add a `requirement_concepts` entity keyed to requirement, with Annex/source anchor, concept text, mode, applicability and provenance; scope mappings/reviews to a concept while retaining reusable capabilities.

- **Legal traceability / granularity:** strongest fit for exact requirement→Annex concept→capability trace, including road/other-mode and conditional Article 5(2) boundaries.
- **Duplication / reuse:** concept rows are per requirement (so P01/P02 may each have a legal concept row); capabilities remain reusable. Avoid duplicating capability definitions.
- **Coverage / representability:** coverage can be computed/reviewed per concept and rolled up to the requirement; representability is attached to the scoped mapping/capability relation with explicit applicability.
- **Observed evidence / automatability / audit.rules:** observation and checks can name the precise concept/mapping; future rules can state which concept elements are required and when.
- **Migration / M04/B01 / validators:** additive migration can preserve all mapping IDs, coverage/review rows and provenance. Existing rows need `LEGACY_UNSCOPED` or a reviewed concept association; do not infer/backfill semantics from their text automatically. Validators need compatibility until mappings are explicitly linked; M04 and B01 historical scopes remain fixed.
- **Idempotence / DuckDB / reports:** stable concept IDs and unique requirement+concept keys provide idempotent seeds and simple joins. Reports can display legal decomposition directly.
- **Frozen/history risk:** low-to-medium, controlled by additive tables and append-only association/provenance; risk arises if old mappings are silently assigned new concepts.

### Option C — coverage component / scoped mapping layer

Add coverage components under a requirement and attach capability mappings to those components, treating each as an auditable unit.

- **Legal traceability / granularity:** strong when each component is a requirement coverage unit, but legal Annex identity and technical concept may be conflated unless the component stores source anchors and applicability explicitly.
- **Duplication / reuse:** capabilities reusable; components are requirement-specific. Similar risks/benefits to Option B.
- **Coverage / representability:** strongest direct fit for coverage aggregation and partial/conditional coverage. Representability can be scoped through component mappings.
- **Observed evidence / automatability / audit.rules:** component IDs make evidence and rules precise and support clear audit outputs.
- **Migration / M04/B01 / validators:** additive migration possible, with existing mapping IDs preserved and associations initially unscoped. Historical validators must keep their existing expected scope; new component-aware validators can be introduced by milestone.
- **Idempotence / DuckDB / reports:** straightforward if component identity and source lineage are normalized; slightly more joins and governance because “coverage component” may be mistaken for a legal source atom.
- **Frozen/history risk:** low-to-medium under additive, controlled association; same danger of falsely backfilling old rows.

### Option D — retain requirement-level uniqueness

This is not the actual current schema. If imposed, one mapping would need to represent bundles of distinct capabilities/concepts or select one preferred route.

- **Legal traceability / granularity:** poor for P02's road, passenger and facility concepts; conditions prose cannot safely replace scoped identities.
- **Duplication / reuse:** encourages composite capability bundles or duplicates, undermining reuse.
- **Coverage / representability / evidence / automation / rules:** conflates distinct route states and makes partial coverage and observations ambiguous.
- **Migration / compatibility / idempotence:** would require invasive remapping of existing rows/reviews/evidence and validators, or hidden JSON/text bundles; higher risk to IDs and historic meaning.
- **DuckDB / reports:** superficially fewer rows, but worse queries and less intelligible reports.
- **Conclusion:** no architectural rationale supports adding this constraint; M02 prose and live M04 mappings contradict it.

## Recommended architecture

Recommend **Option B, requirement concept layer**, while preserving the existing N:M mapping table. It keeps legal concept decomposition explicit, capability reuse intact, and requirement coverage as a separate roll-up. Option C is a viable alternative if later governance defines coverage components as first-class auditable units and keeps their Annex/source lineage explicit. Direct N:M remains available for current mappings but does not fully structure B02's sub-concepts.

This is an architecture recommendation only:

```text
ARCHITECTURE_RECOMMENDATION != AUTHORIZATION_TO_MIGRATE
```

No option is implemented here. Any future change must be additive/controlled, retain existing mapping IDs and rows, reviews, coverage, provenance and historical reports, and avoid Phase 1/2 edits. Yeison must choose the concept/component model and approve how each legacy mapping is handled before a migration or B02 persistence is authorized.

## Risks

- The mission and prior Human Review prose asserted a `UNIQUE(requirement_id)` constraint that the migration and live DB do not contain. The report corrects the assertion; no schema change was made.
- Treating a general DATEX II parking model or the truck-parking RRP as the Annex 2.2 general parking profile would exceed demonstrated scope.
- `PARTIAL` U01/U03 results mean the authoritative scope/profile chain is incomplete, not that no national profile exists.
- Direct mappings without concept scope may make coverage, evidence and future audit rules ambiguous; an additive migration must not silently backfill concepts.
- Existing validators are deliberately scoped around M04/B01 historical batches. Future B02 data may need validator updates, but this mission makes none.
- No real NAP dataset was inspected. Nothing here establishes observed publication, implementation, representability of an actual dataset, or legal compliance.

## Human decision required next

Before migration or persistence, Yeison must decide:

1. Whether to adopt Option B (`requirement_concept`) or Option C (coverage component), and the identity/source fields required to preserve Annex 2.1/2.2 scope and Article 5(2) applicability.
2. Whether existing M04/B01 mappings remain legacy-unscoped initially or receive individually reviewed associations; no automatic semantic backfill.
3. Whether U01/U03 should remain `PARTIAL` pending a specific national-profile inquiry or be closed as unresolved for this milestone. Their present research does not authorize mappings.
4. The future persistence batch scope for C01/C04/C07/C08, including exact profile/version and (for C07/C08) Annex-to-element crosswalk acceptance criteria.

Until that decision and explicit authorization, DB writes and schema migration remain `NOT_AUTHORIZED`.

## Validation and integrity

- Database access: DuckDB `-readonly`; schema constraints and counts queried directly. No writes.
- Baseline DB SHA-256 before review: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4`.
- Post-review DB SHA-256: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4` (identical to pre-review).
- Level A: PASS (6 mappings, 6 capabilities, 6 exceptions; 0 invalid references, states, or missing reasons). M04, M04B, M05B family, M06-B01 candidate and global exception-accounting validators: PASS, all exit 0 in DuckDB `-readonly`.
- `quick_validate`: `NOT_EXECUTED`; reason: missing `yaml` dependency (confirmed/recorded by the skill pilot; no dependency installed).
- `git diff --check`: PASS (exit 0); direct trailing-whitespace scan of both edited documents: no matches.
- Phase 1 modified: NO. Phase 2 modified: NO. DB modified: NO. History rewritten: NO. Pre-existing changes preserved: YES.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
