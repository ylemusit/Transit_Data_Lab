# M06-B02 Human Review Package

## Scope

- Requirements: `EU-2017-1926-REQ-A05-P01-002`, `EU-2017-1926-REQ-A05-P02-001`.
- Candidates: 8 (`B02-P01-C01`–`C03`; `B02-P02-C01`–`C05`).
- Unresolved concepts: 3 under P02, Annex 2.2.
- DB writes: 0.
- Human gate: REQUIRED.

Review date: 2026-09-28. This package reviews the local R1/R2/R3 research and candidate generation against the frozen source facts, current Phase 3 schema and a read-only view of the Compliance database. The two existing B02 documents and other pre-existing untracked files were preserved. In this file, `AGENT RECOMMENDATION` records the research proposal, while `HUMAN DECISION — YEISON` records Yeison's authorized disposition; these fields are independent and must never be conflated.

## Candidate summary

| Candidate | Requirement | Route | Standard/Profile | AGENT RECOMMENDATION | Confidence | HUMAN DECISION — YEISON |
|---|---|---|---|---|---|---|
| C01 (`B02-P01-C01`) | P01-002 | TECHNICAL | DATEX II RTTI RRP; exact RRP/version open | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C02 (`B02-P01-C02`) | P01-002 | TECHNICAL | DATEX II MMTIS Level 2, current road-link travel times; model version unstated | ACCEPT_WITH_LIMITATIONS | MEDIUM | REJECT |
| C03 (`B02-P01-C03`) | P01-002 | TECHNICAL | DATEX II MMTIS Level 3, future predicted road-link travel times; model version unstated | HOLD_FOR_RESEARCH | LOW | REJECT |
| C04 (`B02-P02-C01`) | P02-001 | TECHNICAL | DATEX II RTTI RRP; exact category RRP/version open | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C05 (`B02-P02-C02`) | P02-001 | TECHNICAL | DATEX II MMTIS Level 2, current road-link travel times; model version unstated | ACCEPT_WITH_LIMITATIONS | MEDIUM | REJECT |
| C06 (`B02-P02-C03`) | P02-001 | TECHNICAL | DATEX II MMTIS Level 3, future predicted road-link travel times; model version unstated | HOLD_FOR_RESEARCH | LOW | REJECT |
| C07 (`B02-P02-C04`) | P02-001 | TECHNICAL | SIRI EPIP-RT, CEN/TS 15531-7:2025 | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C08 (`B02-P02-C05`) | P02-001 | TECHNICAL | SIRI EPIP-RT, CEN/TS 15531-7:2025; facility-monitoring service | HOLD_FOR_RESEARCH | LOW | ACCEPT_WITH_LIMITATIONS |

The shared legal basis is the frozen Spanish consolidated MMTIS text dated 2024-03-04. Its Article 5(1)(a) road source fact is `EU-2017-1926-SF-A05-P01-ROAD`; Article 5(2)'s conditional profile source fact is `EU-2017-1926-SF-A05-P02`. The materialized requirement descriptions are shorter interpretations and remain separate from those literal source facts.

P01 summary: facilitate dynamic road data using the formats referred to in Articles 5 and 6. P02 summary: represent dynamic Annex 2.1/2.2 data to which SIRI and/or DATEX II apply through minimum EU or national profiles. The P02 applicability condition is part of its scope; it does not say that both standards apply to every category.

Both requirements are classified in Phase 3 family `Availability and format representation` with HIGH family-classification confidence. That is planning metadata, not a legal interpretation. The schema defines `UNIQUE(requirement_id, capability_id)`, not `UNIQUE(requirement_id)`: distinct capabilities may already be linked to one requirement, while repeating the same pair is prohibited. The mapping row has no explicit concept/component identifier, so separate concepts using the same capability cannot be distinguished structurally without a design decision. No schema change or seed is authorized here.

Keep these layers separate throughout review:

```text
identity of standard != capability != mapping != coverage
                       != representability != observed evidence
                       != legal compliance
```

### Legal succession and source authority

The frozen source fact still names Regulation (EU) 2015/962. R3 examined the European Commission's November 2024 implementation handbook, Q&A 4: it describes the legal citations as dynamic references and says the latest applicable RTTI delegated regulation is used for interpretation. The handbook expressly says it is informational and does not bind the Commission; it is interpretive context, not an amendment, judgment, or declaration that Regulations 2015/962 and 2022/670 are identical. Regulation 2022/670 is the current RTTI context and identifies DATEX II in its technical framework. Keep both records visible and category-specific. Do not rewrite Phase 2.

Primary legal sources: [consolidated Regulation (EU) 2017/1926, 2024-03-04](https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:02017R1926-20240304); [Regulation (EU) 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng). Informative interpretive source: [Commission implementation handbook, November 2024, Q&A 4](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en). The handbook also says the court alone authoritatively interprets Union law. Thus the bridge is explicit Commission guidance, but remains non-binding.

Primary technical sources used in the existing research: [DATEX II MMTIS RRP overview](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/), [MMTIS Level 2 current road-link travel times](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls2a-current-road-link-travel-times/), [MMTIS Level 3 future predicted road-link travel times](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls3-future-predicted-road-link-travel-times/), and [DATEX II RTTI 2022/670 RRP catalog](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/). The catalog identifies category profiles, but the MMTIS pages do not consistently state an exact model version. For SIRI, [CEN-CENELEC's EPIP-RT announcement](https://www.cencenelec.eu/news-events/news/2025/eninthespotlight/2025-08-21-siri-7/) identifies CEN/TS 15531-7:2025 and its stated real-time passenger/facility scope. The standards-body and standards-catalog claims establish technical scope/profile identity; they are not legislation and do not prove implementation.

## Candidate reviews

### Candidate C01 — `B02-P01-C01`

#### Requirement

`EU-2017-1926-REQ-A05-P01-002`: facilitate dynamic road data using the formats referred to in Articles 5 and 6. It is not conditional in the materialized row.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P01-ROAD`, Article 5(1)(a), consolidated 2024-03-04: road transport uses formats indicated in Articles 5 and 6 of Regulation 2015/962. Current contextual bridge: Commission 2024 handbook Q&A 4 (informative, non-binding), with 2022/670 as successor RTTI context.

#### Concept

Road disruptions and road traffic status: only road concepts with a category-specific RTTI profile basis. This is not every Annex 2.1 disruption or every traffic concept across all modes.

#### Proposed route

TECHNICAL.

#### Proposed standard/profile

DATEX II, RTTI RRP family for categories in Regulation 2022/670. Exact category-specific profile and model version are not pinned down by the candidate evidence. No national profile is asserted.

#### Proposed capability

New concept-scoped proposal `CAP-DATEXII-RRP-ROAD-STATUS`. The existing `CAP-DATEXII-RRP-ROAD-TRAVEL` has travel-time scope and is a `NONE` match for disruptions/status.

#### Evidence

Primary technical sources: official MMTIS RRP overview and RTTI 2022/670 catalog. Primary legal source: frozen EUR-Lex MMTIS text. Secondary/informative source: Commission 2024 handbook Q&A 4 supplies an explicit dynamic-reference interpretation, with the authority limitation above.

#### Limitations

The exact profile/category pair and version still need to be named before persistence. No implementation or dataset was inspected. The candidate supports a road concept only and cannot stand for all P01 data.

#### Uncertainty

Medium legal/profile crosswalk uncertainty; low-to-medium technical-family uncertainty. No contradictory source was found, but profile family membership alone does not select the exact profile.

#### Contradictions

No source-to-source contradiction identified. The existing travel-time capability returning `NONE` for this concept is a scope distinction, not evidence against the separate status-profile family.

#### Candidate state

Documentary candidate status `AVAILABLE`; not persisted.

#### AGENT RECOMMENDATION

`ACCEPT_WITH_LIMITATIONS` — evidence supports a narrow road-status profile family; it does not yet resolve exact RRP/version. If accepted, a later reviewed design may record only the road disruption/status concept against a matching capability, after defining how the concept scope is represented and naming the specific applicable profile. It would not authorize a broad P01 mapping by itself.

#### Confidence

MEDIUM.

#### If accepted

It would authorize treating this concept/profile relationship as semantically accepted for a future persistence proposal, bounded to the demonstrated road status/disruption elements. It would not authorize a seed. The schema permits distinct capabilities per requirement but prohibits a duplicate requirement-capability pair; explicit concept scope still needs a design decision.

#### Does NOT establish

It does not establish all P01 coverage, the legal effect of an individual profile, a NAP's implementation, data presence, representability of a concrete dataset, or legal compliance.

#### HUMAN DECISION — YEISON

```text
ACCEPT_WITH_LIMITATIONS
```

### Candidate C02 — `B02-P01-C02`

#### Requirement

`EU-2017-1926-REQ-A05-P01-002`: facilitate dynamic road data using the formats referred to in Articles 5 and 6.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P01-ROAD`, Article 5(1)(a). Regulation 2022/670 and the Commission handbook Q&A 4 provide current RTTI context and an explicitly non-binding interpretation of the dynamic reference.

#### Concept

Current measured road-link travel times.

#### Proposed route

TECHNICAL.

#### Proposed standard/profile

DATEX II MMTIS Level 2 — Current road-link travel times. Exact DATEX II model version is not stated in the linked MMTIS page.

#### Proposed capability

Existing `CAP-DATEXII-RRP-ROAD-TRAVEL`; DB description is travel-time-centred, status `NEEDS_REVIEW`, and explicitly cautions against inferring each Annex assignment. Candidate relation is concept-level, not persisted.

#### Evidence

Primary technical sources: official Level 2 page and MMTIS RRP overview. Primary legal source: frozen EUR-Lex MMTIS text. Secondary/informative source: Commission 2024 handbook Q&A 4 for current RTTI context; it does not textually replace 2015/962.

#### Limitations

Exact model version and detailed Annex-category crosswalk are not recorded. No dataset or NAP implementation was inspected. The candidate document's `FULL` capability match means only that this capability's semantics match this concept; it is not full requirement coverage.

#### Uncertainty

Medium: technical concept fit is strong; legal pairing and dataset state remain separate and unproven.

#### Contradictions

No contradictory source identified. The capability catalog's `NEEDS_REVIEW` status means its registry entry is not finally reviewed; it does not contradict the profile's technical scope.

#### Candidate state

Documentary candidate status `AVAILABLE`; not persisted.

#### AGENT RECOMMENDATION

`ACCEPT_WITH_LIMITATIONS` — the Level 2 profile and existing travel-time capability are concept-aligned. If accepted, later work may propose the narrow current-road-link-travel-time relationship, retaining version and legal-context limitations and the schema cardinality constraint.

#### Confidence

MEDIUM.

#### If accepted

It would support a future semantic decision for current measured road-link travel times only. It would not permit claiming all P01 data is represented.

#### Does NOT establish

No complete requirement coverage, concrete dataset representability, observed publication, or legal compliance follows from this decision.

#### HUMAN DECISION — YEISON

```text
REJECT — REJECT_FOR_THIS_REQUIREMENT_SCOPE. Current road-link travel-time profile existence does not establish that this concept belongs to this B02 requirement's current scope derived from Annex 2.1/2.2 (`PROFILE_EXISTS != REQUIREMENT_SCOPE_MATCH`). This is not a rejection of DATEX II; retain the technical evidence for another requirement if relevant.
```

### Candidate C03 — `B02-P01-C03`

#### Requirement

`EU-2017-1926-REQ-A05-P01-002`: facilitate dynamic road data using the formats referred to in Articles 5 and 6.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P01-ROAD`, Article 5(1)(a), with the same non-binding current RTTI interpretation context described above.

#### Concept

Future predicted road-link travel times.

#### Proposed route

TECHNICAL, if the requirement-to-concept link is demonstrated.

#### Proposed standard/profile

DATEX II MMTIS Level 3 — Future Predicted Road Link travel times. Exact model version is not stated in the cited page.

#### Proposed capability

Provisional association with `CAP-DATEXII-RRP-ROAD-TRAVEL`; the capability's persisted semantic description is specifically about road-link travel times and does not itself establish forecast semantics or a legal category link.

#### Evidence

Official DATEX II documentation identifies a Level 3 future predicted road-link travel-time RRP. The candidate's own research says this forecast concept is not established as a discrete Annex 2.1/2.2 category.

#### Limitations

Missing exact Annex category and legal requirement-to-forecast connection. The Level 3 profile's existence cannot supply that missing legal/conceptual link. No data evidence exists.

#### Uncertainty

High; the requirement anchor is unresolved even though a technical profile exists.

#### Contradictions

The candidate row says `AVAILABLE` while its relation is provisional and category fit unresolved. These describe different layers (profile candidate versus requirement mapping); read `AVAILABLE` narrowly and do not treat it as an available mapping.

#### Candidate state

Documentary candidate status `AVAILABLE`, with relationship/representability proposed as partial; not persisted. `AVAILABLE` here describes a profile candidate, not a demonstrated requirement mapping.

#### AGENT RECOMMENDATION

`HOLD_FOR_RESEARCH` — first establish the exact Annex 2.1/2.2 data item that makes forecast road-link time part of P01. If accepted now, the requirement would be connected to a concept whose legal category fit is admitted as unproven.

#### Confidence

LOW.

#### If accepted

Acceptance should mean only that the issue is approved for continued research, not that a mapping may be persisted. Revisit the mapping decision after an exact Annex category and profile version are evidenced.

#### Does NOT establish

The standard's support for forecasting does not establish that the requirement covers future predicted times, nor coverage, representability, observed data, or compliance.

#### HUMAN DECISION — YEISON

```text
REJECT — REJECT_FOR_THIS_REQUIREMENT_SCOPE. Future predicted road-link travel-time profile existence does not create an Annex item, requirement, or legal link to this B02 requirement. This is not a rejection of DATEX II; retain the technical evidence for another requirement if relevant.
```

### Candidate C04 — `B02-P02-C01`

#### Requirement

`EU-2017-1926-REQ-A05-P02-001`: dynamic Annex 2.1/2.2 data to which SIRI and DATEX II apply are represented through minimum EU or national profiles. Applicability conditions the requirement.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P02`, Article 5(2), consolidated 2024-03-04. This review does not turn DATEX II applicability into a universal Annex-wide premise.

#### Concept

Road disruptions/status within the road subset of Annex 2.1(i) and relevant road traffic status in 2.1(ii).

#### Proposed route

TECHNICAL.

#### Proposed standard/profile

DATEX II RTTI RRP family for the category concerned. The exact profile/version is not stated for the candidate.

#### Proposed capability

New scoped proposal `CAP-DATEXII-RRP-ROAD-STATUS`; existing road travel capability is `NONE` for this concept.

#### Evidence

Official MMTIS overview and the DATEX II RTTI 2022/670 catalog show category-specific road profile families; Article 5(2) allows only the concepts to which the named standards apply to be represented by their minimum EU or national profiles.

#### Limitations

This covers only supported road categories, not the conditional P02 requirement as a whole. Exact category RRP/version must be selected. No dataset inspection.

#### Uncertainty

Medium legal/category crosswalk uncertainty; lower technical-family uncertainty.

#### Contradictions

No contradictory source identified. The separate Article 5(1)(a) successor context and conditional Article 5(2) applicability are distinct legal links, not interchangeable grounds.

#### Candidate state

Documentary candidate status `AVAILABLE`; not persisted.

#### AGENT RECOMMENDATION

`ACCEPT_WITH_LIMITATIONS` — accept only the road disruption/status concept as a bounded candidate. If accepted, a later proposal may record this one concept under P02 with its DATEX applicability condition and exact selected category profile. Do not generalize to parking, shared vehicles, passenger service, or all Annex 2.1/2.2.

#### Confidence

MEDIUM.

#### If accepted

It would support a concept-level semantic decision for the evidenced road subset only; subsequent persistence still needs explicit concept scope and an exact profile reference.

#### Does NOT establish

It does not establish that DATEX II applies to every P02 concept, full P02 coverage, a dataset, or legal compliance.

#### HUMAN DECISION — YEISON

```text
ACCEPT_WITH_LIMITATIONS
```

### Candidate C05 — `B02-P02-C02`

#### Requirement

`EU-2017-1926-REQ-A05-P02-001`, conditional Article 5(2) profile representation.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P02`. Only this road-link travel-time concept is reviewed here; no conclusion is made for the remainder of the condition.

#### Concept

Current measured road-link travel times.

#### Proposed route

TECHNICAL.

#### Proposed standard/profile

DATEX II MMTIS Level 2 — Current road-link travel times; exact model version not stated.

#### Proposed capability

Existing `CAP-DATEXII-RRP-ROAD-TRAVEL`, a semantic fit for travel time. Its review status remains `NEEDS_REVIEW` in the catalog.

#### Evidence

Official DATEX II Level 2 RRP page describes current road-link travel times. The profile provides an identifiable technical candidate for this concept.

#### Limitations

Must still demonstrate that DATEX II applies to this specific P02 concept under the Article 5(2) condition and select/record the applicable model/profile version. No dataset was examined.

#### Uncertainty

Medium: strong profile-to-concept fit; conditional legal applicability and dataset evidence are unresolved.

#### Contradictions

No source-to-source contradiction identified. The registry capability is marked `NEEDS_REVIEW`; this limits reuse pending its review and is not a conflicting technical profile claim.

#### Candidate state

Documentary candidate status `AVAILABLE`; not persisted.

#### AGENT RECOMMENDATION

`ACCEPT_WITH_LIMITATIONS` — the technical profile and capability semantics align for this concept. If accepted, a future proposal can record only current road-link times, conditioned on demonstrated DATEX II applicability, with explicit concept scope; the schema already permits different capability mappings for the requirement.

#### Confidence

MEDIUM.

#### If accepted

It authorizes semantic treatment of this concept only for a future design. It does not authorize overall P02 coverage or persistence without explicit concept-scope review.

#### Does NOT establish

No full conditional coverage, representation of other Annex categories, actual NAP data, or legal compliance.

#### HUMAN DECISION — YEISON

```text
REJECT — REJECT_FOR_THIS_REQUIREMENT_SCOPE. Current road-link travel-time profile existence does not establish that this concept belongs to this B02 requirement's current scope derived from Annex 2.1/2.2 (`PROFILE_EXISTS != REQUIREMENT_SCOPE_MATCH`). This is not a rejection of DATEX II; retain the technical evidence for another requirement if relevant.
```

### Candidate C06 — `B02-P02-C03`

#### Requirement

`EU-2017-1926-REQ-A05-P02-001`, conditional Article 5(2) profile representation.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P02`.

#### Concept

Future predicted road-link travel times.

#### Proposed route

TECHNICAL, if the exact Annex and conditional-applicability link is demonstrated.

#### Proposed standard/profile

DATEX II MMTIS Level 3 — Future Predicted Road Link travel times. Exact model version not stated.

#### Proposed capability

Provisional association with `CAP-DATEXII-RRP-ROAD-TRAVEL`; forecast-specific semantics are not explicitly established in the persisted capability description.

#### Evidence

Official Level 3 technical profile exists. Existing research does not establish a discrete Annex 2.1/2.2 category-to-profile link for this concept.

#### Limitations

Both the Annex concept anchor and Article 5(2) DATEX applicability need evidence. Profile existence alone does not satisfy either link.

#### Uncertainty

High.

#### Contradictions

As with C03, `AVAILABLE` describes a profile candidate while the proposed P02 relation is partial and not established. These states must not be collapsed into an accepted mapping.

#### Candidate state

Documentary candidate status `AVAILABLE`, but the relationship and representability are only partial proposals; not persisted.

#### AGENT RECOMMENDATION

`HOLD_FOR_RESEARCH` — identify the exact Annex item and applicable standard/profile before recommending semantic acceptance. If accepted now as a mapping, it would bypass two unresolved links.

#### Confidence

LOW.

#### If accepted

Acceptance should authorize only targeted research on Annex/profile applicability; no mapping persistence should follow until that research is reviewed.

#### Does NOT establish

It does not establish P02 applicability, mapping, coverage, dataset representability, observed evidence, or compliance.

#### HUMAN DECISION — YEISON

```text
REJECT — REJECT_FOR_THIS_REQUIREMENT_SCOPE. Future predicted road-link travel-time profile existence does not create an Annex item, requirement, or legal link to this B02 requirement. This is not a rejection of DATEX II; retain the technical evidence for another requirement if relevant.
```

### Candidate C07 — `B02-P02-C04`

#### Requirement

`EU-2017-1926-REQ-A05-P02-001`, conditional Article 5(2) profile representation.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P02`. The separate Article 5(1)(b) source fact names SIRI CEN/TS 15531 and later versions for other modes; the Article 5(2) candidate remains limited to concepts for which SIRI applies.

#### Concept

Non-road public-transport passenger real-time service status and disruptions in relevant Annex 2.1(i)/(ii) concepts.

#### Proposed route

TECHNICAL.

#### Proposed standard/profile

SIRI, Passenger Real-Time Information European Profile (EPIP-RT), CEN/TS 15531-7:2025. Version is evidenced. The profile does not apply to the road limb by analogy.

#### Proposed capability

New scoped proposal `CAP-SIRI-EPIP-RT-PASSENGER-STATUS`.

#### Evidence

CEN-CENELEC identifies the 2025 technical specification and says EPIP-RT covers delays/cancellations, disruptions and passenger real-time information, and supports MMTIS. This is technical profile evidence, not legal authority or proof of an implementation.

#### Limitations

The exact Annex concept-to-SIRI element selection was not exhaustively checked. P02's condition and non-road mode boundary remain. No NAP dataset was inspected.

#### Uncertainty

Medium: profile identity and broad scope are strong; exact element mapping/applicability is incomplete.

#### Contradictions

No source contradiction identified. SIRI's non-road scope here is consistent with the legal route for other modes; it does not support applying SIRI to C01/C04 road concepts.

#### Candidate state

Documentary candidate status `AVAILABLE`; proposed representability `PARTIAL`; not persisted.

#### AGENT RECOMMENDATION

`ACCEPT_WITH_LIMITATIONS` — accept EPIP-RT as a candidate for the bounded relevant non-road passenger status/disruption concepts, subject to item-level Annex mapping. If accepted, later work may review a SIRI capability for those concepts only; do not create a generic SIRI/P02 mapping.

#### Confidence

MEDIUM.

#### If accepted

It supports semantic treatment of the named non-road passenger real-time concepts for a future persistence proposal, after exact elements and a concept-scope model are resolved.

#### Does NOT establish

It does not extend SIRI to road transport, establish every P02 concept, prove implementation/data presence, or establish legal compliance.

#### HUMAN DECISION — YEISON

```text
ACCEPT_WITH_LIMITATIONS
```

### Candidate C08 — `B02-P02-C05`

#### Requirement

`EU-2017-1926-REQ-A05-P02-001`, conditional Article 5(2) profile representation.

#### Legal / source basis

Frozen source fact `EU-2017-1926-SF-A05-P02`. Relevant legal context is the Article 5(1)(b) other-mode limb, which references SIRI CEN/TS 15531 and later versions, subject to its alternatives and compatibility wording.

#### Concept

Scheduled public-transport access-node/facility status, associated with Annex 2.1(iii) in the candidate document.

#### Proposed route

TECHNICAL, if the exact Annex element corresponds to the cited profile service.

#### Proposed standard/profile

SIRI EPIP-RT, CEN/TS 15531-7:2025; facility-monitoring scope. Version is evidenced, but the exact access-node concept correspondence is not.

#### Proposed capability

Provisional proposal `CAP-SIRI-EPIP-RT-FACILITY-STATUS`.

#### Evidence

CEN-CENELEC describes SIRI-FM as a service for monitoring station facilities and mentions station/stop information. This supports the existence of a relevant technical area, not the precise Annex 2.1(iii) field mapping.

#### Limitations

The candidate research itself says exact access-node elements and Annex mapping remain to be confirmed. A station facility is not automatically identical to every access-node status item.

#### Uncertainty

High at the requirement-to-element layer.

#### Contradictions

The candidate is listed `AVAILABLE` although its concept relationship is explicitly `PARTIAL` and its exact Annex mapping is open. This is an apparent status-layer inconsistency; interpret `AVAILABLE` only as documentary candidate existence.

#### Candidate state

Documentary candidate status `AVAILABLE`; relationship proposed as partial; not persisted.

#### AGENT RECOMMENDATION

`HOLD_FOR_RESEARCH` — obtain the exact EPIP-RT element/service definition and compare it to the frozen Annex 2.1(iii) text before accepting a mapping. If accepted now, it would overstate the demonstrated correspondence.

#### Confidence

LOW.

#### If accepted

Acceptance should authorize only targeted profile-to-Annex research. Defer mapping and capability persistence until the element-level link is documented and reviewed.

#### Does NOT establish

The existence of a facility-monitoring SIRI service does not establish a match to every scheduled access-node status field, P02 coverage, actual implementation, observed evidence, or compliance.

#### HUMAN DECISION — YEISON

```text
ACCEPT_WITH_LIMITATIONS
```

## Unresolved concepts

These are P02 Annex 2.2 concepts. `UNRESOLVED` remains a candidate-generation state; none becomes a mapping merely because a route is proposed.

### U01 — Annex 2.2(a), parking tariff information

- Requirement: `EU-2017-1926-REQ-A05-P02-001`.
- Concept: parking tariff information.
- Investigated standards: DATEX II MMTIS Level 2 availability/tariff category is mentioned in R1–R3; a dedicated current MMTIS RRP page/version and exact legal category-to-profile mapping are not established. No SIRI route is evidenced.
- Missing evidence: exact applicable profile, element(s), version, and Article 5(2) applicability chain for this tariff concept.
- Why unresolved: a Level 2 category label and general DATEX II parking model are insufficient to prove the specific profile mapping.
- Profile known but not demonstrated: a broader Level 2 availability/tariff group is known; an exact matching profile is not demonstrated.
- Necessary now: not needed to decide the eight bounded candidates, but needed before claiming or persisting broader P02 concept coverage.
- Agent proposal: `RESEARCH_NOW`, narrowly check official current MMTIS/RTTI profile material for tariff elements and applicability.
- Consequence: until resolved, keep the concept outside candidate mappings and preserve P02 as partial/unresolved at this concept level.
- Yeison decision: `RESEARCH_NOW`.

### U02 — Annex 2.2(b)(i), shared-vehicle availability/location

- Requirement: `EU-2017-1926-REQ-A05-P02-001`.
- Concept: availability/location of shared cars, bicycles, scooters and other shared vehicles.
- Investigated standards: DATEX II and SIRI were considered; no applicable minimum EU/national profile or element mapping was established. Do not infer DATEX II from road association or SIRI from real-time similarity.
- Missing evidence: mode/category-specific legal applicability, authoritative profile and exact elements for the several vehicle types; a single profile should not be presumed across them.
- Why unresolved: the concept spans heterogeneous modes and the sources reviewed do not close each path.
- Profile known but not demonstrated: none for the full grouped concept.
- Necessary now: no for deciding supported C01–C08 concepts; yes before asserting this category's coverage. It may warrant separate concept research if P02 breadth is prioritized.
- Agent proposal: `KEEP_UNRESOLVED` until a category/mode-scoped question and authoritative candidate profile are identified.
- Consequence: no capability or mapping for this grouped concept; later research should split categories where their legal/technical paths differ.
- Yeison decision: `KEEP_UNRESOLVED`.

### U03 — Annex 2.2(b)(ii), parking-space availability

- Requirement: `EU-2017-1926-REQ-A05-P02-001`.
- Concept: on-street and off-street parking-space availability.
- Investigated standards: DATEX II availability-check category/parking model references appear in R1–R3; no dedicated current MMTIS RRP and exact category/profile/legal applicability chain are established. No SIRI mapping is evidenced.
- Missing evidence: the exact current EU profile/version and element match for both on/off-street scope, plus the Article 5(2) applicability chain.
- Why unresolved: broad DATEX II model references and a Level 2 availability label do not identify an applicable MMTIS profile or demonstrate all facility types.
- Profile known but not demonstrated: a general availability-check category is known; exact matching profile is not demonstrated.
- Necessary now: not needed to decide the supported candidates, but required for wider P02 coverage claims.
- Agent proposal: `RESEARCH_NOW`, targeted to current official DATEX II profile definitions and on/off-street element scope.
- Consequence: keep unresolved; no parking capability/mapping or representability assertion follows until reviewed.
- Yeison decision: `RESEARCH_NOW`.

## Validation and integrity

- Read-only database: `03_Compliance/databases/transit_compliance.duckdb`.
- Confirmed current totals: 48 requirements; 36 source facts. Target requirements: 2. Target B02 mappings: 0; target B02 coverage decisions: 0; target B02 representability: 0; target B02 automatability: 0. Global observed evidence: 0; `audit.rules`: 0.
- Requirement family: both targets classified as `Availability and format representation`, confidence HIGH.
- Capability catalog: `CAP-DATEXII-RRP-ROAD-TRAVEL` exists with `standard_id = M03-DATEXII-MMTIS-RRP`, status `NEEDS_REVIEW`, and explicit limitation that it does not establish applicability to every Annex element. No B02 capability exists.
- Database SHA-256 before and after read-only queries: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4`.
- Phase 3 Level A: PASS (6 mappings, 6 capabilities, 6 exceptions, 0 invalid references/states/missing reasons). This is a structural validator result, not B02 semantic acceptance.
- `quick_validate`: `NOT_EXECUTED`; reason: missing YAML dependency. The attempted command exited 1 with `ModuleNotFoundError: No module named 'yaml'`; no dependency was installed.
- No B02-specific human-review validator exists in the inspected Phase 3 test directory; no historical or write-capable gate was run.

## Session result

```text
M06_B02_HUMAN_REVIEW_PACKAGE = READY
M06_B02_HUMAN_DECISION = RECORDED
M06_B02_DB_PERSISTENCE = NOT_AUTHORIZED
M06_B02 = NOT_COMPLETE
```

`READY` was the pre-decision package state. The post-review addendum records every decision. The current uniqueness is on `(requirement_id, capability_id)`; the remaining design question is how to persist distinct concept scopes, not whether a requirement can have different capabilities. No persistence is authorized.

DB writes: 0. Phase 1 modified: NO. Phase 2 modified: NO. DB modified: NO. Historical evidence rewritten: NO. Pre-existing local changes preserved: YES.

Next action: perform only the bounded post-review research and architecture analysis; persistence and migration remain unauthorized.

# Recorded human decisions

| ID | AGENT RECOMMENDATION | Confidence | HUMAN DECISION — YEISON |
|---|---|---|---|
| C01 | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C02 | ACCEPT_WITH_LIMITATIONS | MEDIUM | REJECT |
| C03 | HOLD_FOR_RESEARCH | LOW | REJECT |
| C04 | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C05 | ACCEPT_WITH_LIMITATIONS | MEDIUM | REJECT |
| C06 | HOLD_FOR_RESEARCH | LOW | REJECT |
| C07 | ACCEPT_WITH_LIMITATIONS | MEDIUM | ACCEPT_WITH_LIMITATIONS |
| C08 | HOLD_FOR_RESEARCH | LOW | ACCEPT_WITH_LIMITATIONS |
| U01 | RESEARCH_NOW | MEDIUM | RESEARCH_NOW |
| U02 | KEEP_UNRESOLVED | LOW | KEEP_UNRESOLVED |
| U03 | RESEARCH_NOW | MEDIUM | RESEARCH_NOW |

## Post-review addendum — 2026-09-28

The `AGENT RECOMMENDATION` and `HUMAN DECISION — YEISON` columns above remain separate: the first preserves the research recommendation; the second records the human disposition. The authorized human values are:

| ID | AGENT RECOMMENDATION | HUMAN DECISION — YEISON |
|---|---|---|
| C01 | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C02 | ACCEPT_WITH_LIMITATIONS | REJECT |
| C03 | HOLD_FOR_RESEARCH | REJECT |
| C04 | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C05 | ACCEPT_WITH_LIMITATIONS | REJECT |
| C06 | HOLD_FOR_RESEARCH | REJECT |
| C07 | ACCEPT_WITH_LIMITATIONS | ACCEPT_WITH_LIMITATIONS |
| C08 | HOLD_FOR_RESEARCH | ACCEPT_WITH_LIMITATIONS |
| U01 | RESEARCH_NOW | RESEARCH_NOW |
| U02 | KEEP_UNRESOLVED | KEEP_UNRESOLVED |
| U03 | RESEARCH_NOW | RESEARCH_NOW |

C02/C05 and C03/C06 are `REJECT_FOR_THIS_REQUIREMENT_SCOPE`. These decisions do not reject DATEX II as a standard and do not discard technical profile evidence that may fit another requirement. For C02/C05, `PROFILE_EXISTS != REQUIREMENT_SCOPE_MATCH`; for C03/C06, a future-travel-time profile does not create an Annex requirement or legal link.

The earlier cardinality claim is corrected by schema and live database inspection documented in `M06_B02_POST_HUMAN_REVIEW.md`: the uniqueness constraint is `(requirement_id, capability_id)`. This correction does not alter the preserved agent recommendation or authorize persistence.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
