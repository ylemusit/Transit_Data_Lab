# Compliance Phase 3 — M06-B02 candidate generation

## A. Batch scope

| Field | Value |
|---|---|
| Batch | `M06-B02-ROAD-DYNAMIC-PROFILES` |
| Requirements | `EU-2017-1926-REQ-A05-P01-002`; `EU-2017-1926-REQ-A05-P02-001` |
| Purpose | Concept-level mapping and capability proposals for Human Review only |
| Research gate | R1/R2/R3 read together; `COMPLIANCE_PHASE3_M06_B02_R3 = PASS` |
| Database writes | `0` |
| Phase 1/2 changes | `0` |
| Real NAP datasets inspected | `NO` |
| Final mapping decisions | None made |

Candidates express technical/profile relationships, not legal compliance or observed publication. They are not persisted mappings, representability assertions, or capability records.

## B. Authoritative inputs

- `03_Compliance/reports/phase_3/M06_B02_TARGETED_RESEARCH.md` — R1, R2 and R3 treated together; R3 is `PASS`.
- Exact persisted requirement records read from `compliance.requirements`:
  - `EU-2017-1926-REQ-A05-P01-002`: “Facilitar datos dinámicos de carretera mediante los formatos a los que remiten los artículos 5 y 6.”
  - `EU-2017-1926-REQ-A05-P02-001`: “Los datos dinámicos de los puntos 2.1 y 2.2 del anexo a los que sean aplicables SIRI y DATEX II se representarán mediante perfiles mínimos de la UE o nacionales.” Condition: “Los datos dinámicos de los puntos 2.1 y 2.2 del anexo a los que sean aplicables SIRI y DATEX II.”
- Research links the official legal and technical evidence for each proposed profile. No new external research was performed for this artifact.

## C. Legal-context handling

| Context field | Candidate treatment |
|---|---|
| `LITERAL_REFERENCE` | Regulation 2015/962 remains the literal reference recorded by frozen Phase 2 for the road limb. |
| `CURRENT_RTTI_CONTEXT` | Regulation 2022/670 is recorded as the current RTTI context and successor framework, with the Commission handbook bridge documented in R3. |
| `PHASE2_MODIFICATION_REQUIRED` | `NO` |
| Legal effect | Current context informs Human Review; it does not rewrite the frozen requirement or make this technical candidate a legal conclusion. |

## D. Requirement decomposition

- **P01**: three road concepts are separated: road disruptions/status, current measured road-link travel times, and future predicted road-link travel times. The latter two retain their distinct profile scopes.
- **P02**: the same three supported road concepts are separated, then two non-road passenger concepts with SIRI profile evidence: passenger service real-time status/disruptions and scheduled-service access-node/facility status. Parking tariffs, shared-vehicle availability, and parking-space availability remain separate unresolved concepts because R1/R2/R3 do not establish a sufficiently specific profile-to-category match for candidate generation.
- A concept listed under both requirements has a separate requirement-level candidate row; this does not imply that the two legal duties are interchangeable.

## E. Candidate mapping table

Evidence-source labels refer to sections and linked official sources in `M06_B02_TARGETED_RESEARCH.md`. Profile version is stated only where the research establishes one. Every row is a proposal for Human Review.

| Candidate | Requirement ID | Concept | Transport mode | Standard | Profile | Capability | Relationship type | Evidence source | Confidence | Limitation | Representability candidate | Existing capability match | Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B02-P01-C01 | `EU-2017-1926-REQ-A05-P01-002` | Road disruptions and road traffic status | ROAD | DATEX II | RTTI RRP family for Regulation 2022/670 categories; category-specific RRP, exact profile version not established | Proposed `CAP-DATEXII-RRP-ROAD-STATUS` | `REPRESENTS_CONCEPT` | Research §§ “DATEX II EU profile evidence”, R2 matrix, R3 decision; official MMTIS overview and RTTI 2022/670 RRP catalog | HIGH technical; MEDIUM legal/profile crosswalk | Existing capability is travel-time scoped. Preserve literal 2015/962 reference and current 2022/670 context; candidate does not decide legal sufficiency. | `AVAILABLE` | `NONE` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P01-C02 | `EU-2017-1926-REQ-A05-P01-002` | Current measured road-link travel times | ROAD | DATEX II | MMTIS Level 2 — Current road-link travel times; exact model version not stated | `CAP-DATEXII-RRP-ROAD-TRAVEL` | `REPRESENTS_CONCEPT` | Research §§ “DATEX II EU profile evidence” and “R3 decision”; official MMTIS LS2 profile | HIGH technical; MEDIUM legal pairing | Capability scope matches travel times; candidate does not establish an actual implementation or dataset content. Legal reference context remains for Human Review. | `AVAILABLE` | `FULL` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P01-C03 | `EU-2017-1926-REQ-A05-P01-002` | Future predicted road-link travel times | ROAD | DATEX II | MMTIS Level 3 — Future predicted road-link travel times; exact model version not stated | `CAP-DATEXII-RRP-ROAD-TRAVEL` (provisional association) | `PARTIALLY_REPRESENTS_CONCEPT` | Research §§ “DATEX II EU profile evidence” and “R3 decision”; official MMTIS LS3 profile | HIGH technical; LOW/MEDIUM legal-category pairing | Forecast times are not an explicit discrete Annex 2.1/2.2 category in the research; profile-to-requirement fit remains conditional. | `PARTIAL` | `PARTIAL` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P02-C01 | `EU-2017-1926-REQ-A05-P02-001` | Road disruptions and road traffic status (Annex 2.1(i), road subset of 2.1(ii)) | ROAD | DATEX II | RTTI RRP family for Regulation 2022/670 categories; category-specific RRP, exact profile version not established | Proposed `CAP-DATEXII-RRP-ROAD-STATUS` | `REPRESENTS_CONCEPT` | Research R2 matrix and R3 decision; official MMTIS overview, LS1 and RTTI 2022/670 RRP catalog | HIGH technical; MEDIUM category crosswalk | P02 is conditional on standard applicability. This candidate covers only its supported road concept, not the whole conditional scope. | `AVAILABLE` | `NONE` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P02-C02 | `EU-2017-1926-REQ-A05-P02-001` | Current measured road-link travel times | ROAD | DATEX II | MMTIS Level 2 — Current road-link travel times; exact model version not stated | `CAP-DATEXII-RRP-ROAD-TRAVEL` | `REPRESENTS_CONCEPT` | Research R2 matrix and R3 decision; official MMTIS LS2 profile | HIGH technical; MEDIUM legal pairing | Applies only where the distinct road-link travel-time concept and DATEX II applicability are established. | `AVAILABLE` | `FULL` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P02-C03 | `EU-2017-1926-REQ-A05-P02-001` | Future predicted road-link travel times | ROAD | DATEX II | MMTIS Level 3 — Future predicted road-link travel times; exact model version not stated | `CAP-DATEXII-RRP-ROAD-TRAVEL` (provisional association) | `PARTIALLY_REPRESENTS_CONCEPT` | Research R2 matrix and R3 decision; official MMTIS LS3 profile | HIGH technical; LOW/MEDIUM legal-category pairing | Not an explicit discrete Annex 2.1/2.2 category established by the research; do not generalize to all P02 concepts. | `PARTIAL` | `PARTIAL` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P02-C04 | `EU-2017-1926-REQ-A05-P02-001` | Non-road passenger real-time service status and disruptions (Annex 2.1(i)/(ii), applicable passenger concepts) | PUBLIC_TRANSPORT | SIRI | Passenger Real-Time Information European Profile (EPIP-RT), CEN/TS 15531-7:2025 | Proposed `CAP-SIRI-EPIP-RT-PASSENGER-STATUS` | `REPRESENTS_CONCEPT` | Research “SIRI EU profile and applicability” and R3 decision; official CEN-CENELEC profile announcement and CEN/TS 15531-7:2025 catalogue entry | HIGH profile existence; MEDIUM concept-to-element fit | Applies to relevant other-mode passenger concepts under Article 5(1)(b), not the road limb. Research did not exhaustively audit Annex-to-profile element mapping. | `PARTIAL` | `NONE` | `ACCEPT_WITH_LIMITATIONS` |
| B02-P02-C05 | `EU-2017-1926-REQ-A05-P02-001` | Scheduled public-transport access-node/facility status (Annex 2.1(iii)) | PUBLIC_TRANSPORT | SIRI | EPIP-RT, CEN/TS 15531-7:2025 (facility-monitoring scope) | Proposed `CAP-SIRI-EPIP-RT-FACILITY-STATUS` | `PARTIALLY_REPRESENTS_CONCEPT` | Research “SIRI EU profile and applicability” and R3 residual profile-mapping question; official CEN-CENELEC profile announcement | HIGH profile existence; MEDIUM/LOW item-level mapping | The profile describes facility monitoring, but the exact access-node elements and Annex 2.1(iii) mapping remain to be confirmed against profile details. | `PARTIAL` | `NONE` | `ACCEPT_WITH_LIMITATIONS` |

## F. Capability proposals

No catalog capability is created or edited. The Human Review direction is `KEEP + ADD GRANULAR CAPABILITIES`: retain `CAP-DATEXII-RRP-ROAD-TRAVEL` within its travel-time scope and add only concept-scoped capabilities if review confirms the profiles and relationship semantics.

| Proposed capability ID | Proposed name | Semantic scope | Rationale |
|---|---|---|---|
| `CAP-DATEXII-RRP-ROAD-STATUS` | DATEX II RRP — Road Disruptions and Traffic Status | Category-specific road closures, disruptions/incidents/conditions, and road traffic status supported by the RTTI RRP family; excludes travel-time-only, parking, and shared-vehicle assumptions. | R1/R2/R3 establish official road profile-family evidence for these concepts. Existing travel-time capability does not cover them. Keep legal/profile crosswalk limitations visible. |
| `CAP-SIRI-EPIP-RT-PASSENGER-STATUS` | SIRI EPIP-RT — Passenger Real-Time Service Status | Non-road passenger-service disruptions and real-time status within the documented EPIP-RT scope. | CEN/TS 15531-7:2025 is an identified profile in the SIRI family named for other modes; this is concept-specific, not a generic SIRI capability. |
| `CAP-SIRI-EPIP-RT-FACILITY-STATUS` | SIRI EPIP-RT — Passenger Access-Node Facility Status | Scheduled public-transport access-node/facility monitoring only where EPIP-RT elements are confirmed to match Annex 2.1(iii). | Profile evidence mentions facility monitoring, while exact Annex-element mapping remains a Human Review limitation. |

The current capability's per-concept classification is explicit: `FULL` for current measured road-link travel times; `PARTIAL` for future predicted road-link travel times; `NONE` for road disruptions/status and the SIRI passenger concepts. `NONE` means no semantic match in this existing capability, not that the standard or data is absent.

## G. Representability proposals

These are candidate states only; no representability rows are persisted.

| Candidate concepts | `REPRESENTABILITY_CANDIDATE` | Basis and limit |
|---|---|---|
| P01/P02 road disruptions/status | `AVAILABLE` | Research R3 says official profile/specification evidence supports standard-level representation. The legal/category crosswalk remains limited, and no dataset was examined. |
| P01/P02 current road-link travel times | `AVAILABLE` | Official MMTIS Level 2 profile establishes technical representation; says nothing about a NAP implementation or compliance. |
| P01/P02 future predicted road-link travel times | `PARTIAL` | Official Level 3 profile exists, but mapping to an explicit MMTIS Annex 2.1/2.2 category is not established. |
| P02 SIRI passenger service status/disruptions | `PARTIAL` | EPIP-RT profile scope is established; exhaustive Annex-concept-to-element mapping was not performed. |
| P02 SIRI access-node/facility status | `PARTIAL` | Facility-monitoring profile scope is cited; exact element mapping for Annex 2.1(iii) needs confirmation. |

`STANDARD_REPRESENTABILITY` is distinct from `OBSERVED_EVIDENCE` and `LEGAL_COMPLIANCE`. Observed evidence is unavailable because no real NAP dataset was inspected; this is not evidence of absent data or non-compliance.

## H. Unresolved concepts

| Requirement | Concept | `CANDIDATE_STATUS` | Missing profile/evidence |
|---|---|---|---|
| `EU-2017-1926-REQ-A05-P02-001` | Annex 2.2(a) parking-tariff information | `UNRESOLVED` | R1/R2/R3 name a MMTIS Level 2 availability/tariff group, but do not establish a dedicated current EU RRP page/version or a specific category-to-profile mapping for this concept. |
| `EU-2017-1926-REQ-A05-P02-001` | Annex 2.2(b)(i) shared-car, bicycle, scooter and other shared-vehicle availability/location | `UNRESOLVED` | The reviewed MMTIS profile sources do not establish an applicable minimum EU/national profile or element mapping for the several vehicle categories; DATEX II must not be inferred from the concept alone. |
| `EU-2017-1926-REQ-A05-P02-001` | Annex 2.2(b)(ii) on/off-street parking-space availability | `UNRESOLVED` | A Level 2 availability-check category and DATEX II parking model evidence are mentioned, but a dedicated current MMTIS EU RRP and exact category/profile/legal applicability chain are not established. |

No generic SIRI candidate is proposed. No candidate is made for any unsupported category merely to cover the entire requirement.

## I. Human Review decision points

For every candidate row, reviewers should decide:

1. Whether the decomposed concept matches the exact persisted requirement and its Annex category.
2. Whether the standard applies to that mode and concept, preserving the road/other-mode distinction.
3. Whether the cited profile is sufficient, including the conditional Annex-to-profile link and version details.
4. Whether `CAP-DATEXII-RRP-ROAD-TRAVEL` is a `FULL`, `PARTIAL`, or `NONE` match for that concept.
5. Whether each proposed granular capability is justified and sufficiently narrow.
6. Whether the proposed standard-level representability state is supported without implying dataset evidence or legal compliance.
7. Which crosswalk, profile-version, element-mapping, or dataset limitation must remain explicit.

| Review field | Candidate package recommendation |
|---|---|
| Existing capability decision | `KEEP + ADD GRANULAR CAPABILITIES`; retain the existing travel-time scope. |
| DATEX II candidates | Review road status, current travel time, and future predicted travel time as separate concept rows. |
| SIRI candidates | Review only the two proposed non-road passenger concepts; do not create a generic SIRI capability. |
| SIRI capability candidate | `PROPOSED_CONCEPT_SCOPED` — two proposed capability candidates only; neither is created in the catalog. |
| Unresolved categories | Keep the three Annex 2.2 concepts unresolved pending the specific profile evidence listed above. |
| Model change | `NO`; current model can express concept-level relationships and proposals without structural changes. |
| Phase 2 modification | `NO`. |
| Final disposition | Human decision required; candidate recommendations do not approve mappings, capabilities, representability, or compliance. |

## Candidate-generation accounting

```text
COMPLIANCE_PHASE3_M06_B02_CANDIDATE_GENERATION = PARTIAL
REQUIREMENTS = 2
P01_CONCEPTS = 3
P01_CANDIDATES = 3
P01_UNRESOLVED = 0
P02_CONCEPTS = 8
P02_CANDIDATES = 5
P02_UNRESOLVED = 3
DATEXII_CANDIDATES = 6
SIRI_CANDIDATES = 2
EXISTING_CAPABILITY_REUSE = 2
NEW_CAPABILITY_PROPOSALS = 3
REPRESENTABILITY_PROPOSALS = 5
DATABASE_WRITES = 0
PERSISTED_COUNTS_CHANGED = NO
MODEL_CHANGE_REQUIRED = NO
PHASE2_MODIFICATION_REQUIRED = NO
FILES_CREATED = 1
FILES_MODIFIED = 0
COMMITS_CREATED = 0
PUSH_EXECUTED = NO
GIT_DIFF_CHECK = PASS
HUMAN_REVIEW_READY = PARTIAL
NEXT_ACTION = M06_B02_HUMAN_REVIEW
```

Human Review readiness is partial because three P02 concepts remain explicitly unresolved and several candidate/profile links carry limitations. No final mapping or representability decision has been made.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
