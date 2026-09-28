# Compliance Phase 3 — M06-B02-R1 targeted research: EU minimum profiles

Research date: 2026-09-27
Scope: `M06-B02-ROAD-DYNAMIC-PROFILES`; requirements `EU-2017-1926-REQ-A05-P01-002` and `EU-2017-1926-REQ-A05-P02-001`.
Mode: research only. No database writes, mappings, capabilities, representability assertions, coverage decisions, audit rules, or changes to frozen Phase 1/2.

## Decision

`COMPLIANCE_PHASE3_M06_B02_TARGETED_RESEARCH = PARTIAL`

The EU technical framework is established enough to identify DATEX II RRP families, their MMTIS Levels of Service, and the distinct SIRI profile for public-transport passenger real-time data. It is not enough to unambiguously select a current legal road-format/profile chain for the frozen Phase 2 road-format requirement: Article 5(1)(a) of consolidated Regulation 2017/1926 still names 2015/962, which Regulation 2022/670 repealed from 2025-01-01. 2022/670 expressly identifies DATEX II as an existing standard for RTTI, but does not amend that MMTIS cross-reference. Preserve this as `CURRENT_LEGAL_CONTEXT`; do not silently reinterpret or alter Phase 2.

The framework supports limited profile-level candidate preparation, but the two requirements are too broad to claim one travel-time capability covers them. The first substantive representability assertion is **not ready**: no concrete NAP dataset has been observed, and profile representation alone does not prove dataset content or legal satisfaction.

## Legal evidence

Primary legal source: [consolidated Regulation (EU) 2017/1926, as amended by 2024/490](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng) (Article 5 and Annex points 2.1–2.3). The amendment's current consolidated text retains these operative distinctions:

- Article 5(1) concerns dynamic data in Annex 2.1 and 2.2. For **road transport**, Article 5(1)(a) names formats referred to by Articles 5 and 6 of Regulation 2015/962. For **other modes**, Article 5(1)(b) names SIRI CEN/TS 15531 and later versions, or Regulation 454/2011 technical specifications, or another machine-readable format shown to be fully compatible and interoperable with those specifications.
- Article 5(2) says the Annex 2.1/2.2 data to which SIRI and DATEX II apply shall be represented through minimum EU or national profiles. This does not make SIRI a road standard or DATEX II the universal standard for other modes.
- Annex 2.1 Level of Service 1: (i) disruptions, including network closures/diversions and, where possible, cause; (ii) real-time service status, including estimated departure/arrival, delays, cancellations and guaranteed-connection monitoring; (iii) dynamic status at access nodes (platforms, working lifts/escalators, closed entrances/exits) for scheduled transport.
- Annex 2.2 Level of Service 2: (a) parking-tariff information for demand-responsive and personal transport; (b)(i) availability/location of shared cars, bikes, scooters and other shared vehicles; (b)(ii) available on/off-street parking spaces.
- These categories are not all road traffic. 2.1(i) expressly spans disruptions across modes; 2.1(ii) is service status across modes; 2.1(iii) concerns scheduled public transport access nodes. 2.2(a) spans demand-responsive and personal transport; 2.2(b)(i) is shared-mobility availability; 2.2(b)(ii) is parking availability. The relevant mode therefore depends on the item and data holder, not merely on “dynamic”.

### Cross-reference: `CURRENT_LEGAL_CONTEXT`

[Regulation (EU) 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng) is in force and expressly repealed 2015/962 from 2025-01-01. It updates the RTTI framework, covering the publicly accessible motor-road network within its scope. Its recital 13 identifies DATEX II (CEN/TS 16157 and upgraded versions) among existing technical standards; the regulation does not establish that the stale 2015/962 reference in MMTIS Article 5(1)(a) is legally replaced in that provision. Thus:

| Question | Finding |
|---|---|
| `2015_962_STATUS` | Repealed from 2025-01-01 by Article 15 of 2022/670. It remains named in consolidated MMTIS Article 5(1)(a). |
| `2022_670_RELATIONSHIP` | Current successor RTTI framework; replaces the repealed RTTI instrument and identifies DATEX II as an existing standard. It is a separate delegated regulation, not an amendment to the MMTIS text's cross-reference. |
| `DATEX_II_REMAINS_RELEVANT` | Yes as an established road-traffic technical standard and RRP ecosystem. The precise legal bridge for the MMTIS cross-reference needs a narrowly scoped legal-source check. |
| `CURRENT_LEGAL_CONTEXT_AFFECTS_FROZEN_PHASE2` | Yes, as a current contextual ambiguity relevant to applying the frozen requirement today. It does not retrospectively change what Phase 2 recorded. |
| `PHASE2_MODIFICATION_REQUIRED` | No. Preserve Phase 2 bytes and semantics; record this research only. |

Evidence class: `LEGAL_EVIDENCE`. This report is technical/legal research, not legal advice or a final legal interpretation of the cross-reference.

## DATEX II EU profile evidence

Primary technical source: [official DATEX II RRP overview for MMTIS](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/), with linked [Level of Service 1](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls1-passingtimes/), [Level of Service 2 current road-link travel times](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls2a-current-road-link-travel-times/), and [Level of Service 3 future predicted road-link travel times](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls3-future-predicted-road-link-travel-times/) documentation.

DATEX II describes RRP as use-case subsets of the standard. Its overview says RRP support EU delegated regulations, contain the minimum data elements for the specific data category, and document corresponding elements to promote harmonised modelling. Those are strong profile-author documentation claims. They do **not**, by themselves, establish the legal applicability of a particular RRP to each Annex category, prove an implementation, or establish dataset content.

The official MMTIS index identifies:

- Level 1 disruptions and real-time status for all modes; road traffic is covered by profiles supporting the road-RTTI categories (the index references the former Regulation 962 framework).
- Level 2 current road-link travel times.
- Level 3 future predicted road-link travel times.
- Level 2 availability groups including car-parking availability/tariffs/road toll tariffs; the listed linked profile pages do not provide an individually documented MMTIS RRP for all Annex 2.2 parking/shared-vehicle categories.

The profile documentation pages use a live DATEX II Docs version context and the linked profile pages do not consistently declare an explicit model/schema version. The requirement asks the research report to state version: this report records **DATEX II documented RRP family; exact profile model version not established from the cited MMTIS overview/link set** rather than inventing a version. Regulation 2022/670 itself identifies CEN/TS 16157 and upgraded versions as the DATEX II standard family.

| Profile name / category | DATEX version | MMTIS level | Regulatory category | Technical scope | Official source | Status |
|---|---|---:|---|---|---|---|
| MMTIS Level 1 data categories; road disruptions/status are directed to road-RTTI profiles | Exact version not stated on overview; DATEX II Docs RRP family | 1 | Annex 2.1(i) disruptions; 2.1(ii) real-time status | Generic MMTIS entry covers all modes; road profile cross-reference points to RTTI category profiles, while the cited overview reflects legacy 962 nomenclature | DATEX II MMTIS overview and LS1 | `PARTIAL` — family and category set established; road profile/legal successor crosswalk not closed |
| Current road-link travel times (RRP) | Exact version not stated on linked profile page; DATEX II Docs RRP family | 2 | Closest fit: 2.1 dynamic road/travel status where travel-time data is in scope; not an Annex 2.2 parking category | Current measured road-link travel times | DATEX II MMTIS LS2 page | `ESTABLISHED` as a technical profile; exact legal-category pairing remains conditional |
| Future predicted road-link travel times (RRP) | Exact version not stated on linked profile page; DATEX II Docs RRP family | 3 | Related trip-plan concept, but not an explicit category in Annex 2.1/2.2 list | Forecast road-link travel times; documentation notes correspondence with RTTI travel-time RRP | DATEX II MMTIS LS3 page | `PARTIAL` — technical profile exists; Annex 2.1/2.2 legal mapping not established |
| MMTIS Level 2 availability check / parking availability and tariffs | Exact version and a dedicated MMTIS profile page not established in cited index | 2 | Annex 2.2(a), (b)(ii) | Parking tariff information and on/off-street parking-space availability | DATEX II MMTIS overview; further category-to-profile evidence required | `PARTIAL` |

The official RRP catalog also lists RTTI 2015/962 road-status profiles and current RTTI 2022/670 RRP groups. Their existence evidences technical continuity and a current DATEX II road profile ecosystem, but it does not by itself resolve which group legally discharges MMTIS Article 5(1)(a) after repeal.

### Existing capability

The current capability registry seed describes `CAP-DATEXII-RRP-ROAD-TRAVEL` as “road traffic and travel data”, with semantic scope “road link travel times; MMTIS use cases”, and evidence specifically about MMTIS RRP and current/future predicted road-link travel-time profiles. Its notes warn that it does not establish applicability to every MMTIS category and does not infer national profiles.

| Requirement | Scope assessment of existing capability | Recommendation |
|---|---|---|
| `A05-P01-002` road formats | `PARTIAL` — capability names DATEX II/RRP and road travel but its semantic scope is travel times; legal cross-reference is currently ambiguous. | Reuse as a provisional profile-family link, then refine scope or add a separate road-format capability only after the legal crosswalk is resolved. |
| `A05-P02-001` minimum profiles | `TOO_NARROW` for the entire conditional requirement; one travel-time capability cannot cover all applicable 2.1/2.2 categories. | Likely `MULTIPLE_CAPABILITIES` if candidate generation is category-scoped: road DATEX II profiles plus public-transport SIRI profile where legally applicable, and potentially separate DATEX capabilities for parking/other road categories. Do not create them in this research task. |

Evidence class: `PROFILE_EVIDENCE` and `TECHNICAL_SPECIFICATION_EVIDENCE`; capability semantics are read from the project's existing seed and unchanged.

## SIRI EU profile and applicability

The legal standard route for **other modes** in Article 5(1)(b) names SIRI CEN/TS 15531 and subsequent versions (subject to the stated alternatives and full-compatibility condition). CEN's 2025 publication establishes **CEN/TS 15531-7:2025, Passenger Real-Time Information European Profile (EPIP-RT)**. The [CEN-CENELEC announcement](https://www.cencenelec.eu/news-events/news/2025/eninthespotlight/2025-08-21-siri-7/) says it introduces a European passenger real-time profile for delays/cancellations, vehicle location, stop/station information and disruptions, and directly supports MMTIS. The [national standards-body catalogue entry](https://www.nen.nl/cen-ts-15531-7-2025-en-341552) lists it as definitive, published 2025-07-01. CEN/TS 15531-7:2025 is therefore established as a European technical profile; no evidence here makes it the exclusive mandatory MMTIS format or proves it applies to road transport.

| Field | Finding |
|---|---|
| `PROFILE_NAME` | Passenger Real-Time Information European Profile — Real-Time (`EPIP-RT`) |
| `STANDARD_REFERENCE` | SIRI, CEN/TS 15531-7:2025 |
| `VERSION` | 2025; definitive, published 2025-07-01 |
| `LEGAL/REGULATORY_RELATIONSHIP` | Technical profile in the SIRI CEN/TS 15531 family named by Article 5(1)(b) for other modes; CEN says it supports MMTIS. This does not expand SIRI to the road limb in 5(1)(a). |
| `TECHNICAL_SCOPE` | Passenger public-transport real-time information; profile description includes disruptions, estimated timetables, vehicle monitoring and facility monitoring. |
| `STATUS` | `ESTABLISHED` as an EU technical profile; exact Annex subcategory-to-profile element mapping was not audited exhaustively here. |

`SIRI_APPLICABILITY_A05_P02_001 = NO` for the **road-only B02 scope**. SIRI could be `YES` for relevant other-mode 2.1 passenger-service concepts (especially real-time status, disruptions and dynamic access-node status); however, those are outside this road-profile candidate scope. Do not infer `dynamic data = SIRI` or create `CAP-SIRI-DYNAMIC-PT` in this report.

Evidence class: `TECHNICAL_SPECIFICATION_EVIDENCE` and `PROFILE_EVIDENCE`; CEN's description is authoritative profile context, not the legal text.

## EU versus national profile

Article 5(2) permits minimum EU **or national** profiles for data to which SIRI and DATEX II apply. The EU sources establish a usable technical framework for road profiles and EPIP-RT for public-transport real-time information. A Spanish national profile is not shown by the reviewed sources to be a prerequisite before a provisional EU-profile candidate can be formed. This is not a claim that Spain has no relevant national profile.

| Output | Finding |
|---|---|
| `EU_PROFILE_SUFFICIENT_FOR_CANDIDATE_MAPPING` | `PARTIAL` — sufficient to identify candidate profile families, not to close road legal applicability, all Annex categories, or dataset evidence. |
| `SPANISH_PROFILE_REQUIRED_BEFORE_MAPPING` | `NO` on the evidence reviewed; Article 5(2) offers EU or national profiles. No Spanish profile was required to establish this EU-level framework. |

## Required matrix

`EXISTING/PROVISIONAL CAPABILITY` refers to the existing capability catalog only. `UNKNOWN` representability means no observed NAP dataset has been examined; it must not be read as missing data or non-compliance.

| Legal requirement | Annex category | Mode | Standard | EU profile / technical category | Existing/provisional capability | Representability readiness |
|---|---|---|---|---|---|---|
| `A05-P01-002` Art. 5(1)(a): road dynamic format by reference to 2015/962 Arts. 5–6 | Road-relevant Annex 2.1 disruptions/status; exact overlap depends on data type | `ROAD` | DATEX II is named as an existing RTTI standard by 2022/670; Article 5(1)(a)'s 2015/962 reference is repealed | Road RTTI RRP groups for disruption/status; MMTIS Level 1 overview says road profiles are the profiles for road-RTTI categories | `CAP-DATEXII-RRP-ROAD-TRAVEL` partial; its current travel-time scope does not establish all disruption/status concepts | `UNKNOWN`; profile/legal bridge not closed and no dataset observed. Candidate profile identification only. |
| `A05-P02-001` Art. 5(2): minimum EU or national profile when DATEX II applies | 2.1(i) disruptions; 2.1(ii) real-time status; road subset | `ROAD` | DATEX II | LS1 category family; road RTTI profile dependencies; LS2 current travel time only where that distinct category is in scope | Existing travel capability partial/too narrow for disruptions and service-status range | `UNKNOWN`; exact road category profile selection and source dataset absent. |
| `A05-P02-001` Art. 5(2) | 2.1(iii) scheduled-service access-node status | `PUBLIC_TRANSPORT` | SIRI or qualifying alternative under 5(1)(b) | EPIP-RT (CEN/TS 15531-7:2025) profile family; item-to-element mapping not fully established in this task | No SIRI capability exists in current catalog; not needed for road-only B02 candidate | `UNKNOWN`; technical profile established, but no NAP dataset observed. |
| `A05-P02-001` Art. 5(2) | 2.2(a) parking tariff information | `MULTIMODAL` (demand-responsive + personal transport; category itself does not prescribe one mode-specific profile) | DATEX II where applicable under Art. 5(2) | MMTIS Level 2 availability/tariff group is named; dedicated current profile page/category mapping not established | Road-travel capability too narrow | `UNKNOWN`; exact profile category mapping and dataset absent. |
| `A05-P02-001` Art. 5(2) | 2.2(b)(i) shared vehicle availability/location | `OTHER_MODE` / `MULTIMODAL` depending on vehicle; includes shared cars, bikes, scooters and other shared vehicles | DATEX II only where applicable; do not infer DATEX from the category alone | Dedicated applicable EU profile not established in the reviewed MMTIS pages | Existing road-travel capability not shown to represent this category | `UNKNOWN`; profile selection remains open. |
| `A05-P02-001` Art. 5(2) | 2.2(b)(ii) on/off-street parking availability | `ROAD` / `OTHER_MODE` depending on facility and context | DATEX II where applicable | MMTIS Level 2 availability-check category and DATEX II parking-availability technical model evidence exist; exact current MMTIS EU RRP mapping not established | Existing road-travel capability too narrow | `UNKNOWN`; current profile/legal mapping and dataset absent. |

The legal/profile distinctions above precede capability and dataset conclusions. In particular:

`LEGAL/NORMATIVE SOURCE → TECHNICAL PROFILE → CAPABILITY → REPRESENTABILITY → REAL NAP DATASET → OBSERVED EVIDENCE`

A profile can establish a way to represent a concept. It does not establish that a catalog capability exists, that a particular NAP dataset contains that concept, or that a legal requirement is satisfied. No operator was audited and no dataset was examined.

## Representability gate

| Requirement / provisional capability pair | Possible later assertion states | `REPRESENTABILITY_READY` | Reason |
|---|---|---|---|
| `A05-P01-002` × `CAP-DATEXII-RRP-ROAD-TRAVEL` | `UNKNOWN` only at this stage | `NO` | The road legal cross-reference is unresolved and capability scope is travel-time-centred. Need current legal bridge and category-specific profile choice, then a real NAP dataset. |
| `A05-P02-001` × `CAP-DATEXII-RRP-ROAD-TRAVEL` | `UNKNOWN` only at this stage | `PARTIAL` | Useful profile evidence exists for some road concepts, but capability is too narrow for the conditional full requirement; multiple category-scoped capability paths and dataset evidence are unresolved. |

No `AVAILABLE`, `PARTIAL`, `MISSING`, or `NOT_APPLICABLE` assertion is supported yet. In particular, `CAPABILITY EXISTS != STANDARD REPRESENTS CONCEPT != DATASET CONTAINS CONCEPT != LEGAL REQUIREMENT SATISFIED`.

## Answers and gate

1. **EU framework for A05-P01-002:** DATEX II road-RTTI format/profile family is technically established, including the current Regulation 2022/670 RTTI regime, but the frozen legal wording points to repealed 2015/962. Candidate mapping should preserve this as a legal dependency until the applicability bridge is resolved.
2. **EU framework for A05-P02-001:** Article 5(2) minimum EU-or-national profile framework. DATEX II RRP applies to the relevant road concepts where DATEX II is applicable; SIRI/EPIP-RT applies to relevant other-mode passenger-real-time concepts. The road-only B02 branch uses DATEX II; it does not need SIRI.
3. **Is DATEX II RRP evidence sufficient to map either requirement?** `PARTIAL`. It establishes profile families and some categories; it does not settle the repealed cross-reference, all category mappings, capability breadth, or real-data representation.
4. **Is a SIRI capability actually needed?** Not for this road-only B02 branch. It is relevant to the out-of-scope public-transport branch of A05-P02-001, but should not be inferred or created here.
5. **Is a Spanish national profile required before proceeding?** `NO` on evidence reviewed; EU profiles are an explicit alternative. This does not prove no Spanish profile exists.
6. **Can either requirement support the first substantive representability assertion?** `NO` yet. No actual NAP dataset is observed; profile evidence alone is insufficient.
7. **Does the capability catalog need a new capability?** No immediate catalog change. `CAP-DATEXII-RRP-ROAD-TRAVEL` is partial for P01 and too narrow for the full P02 scope. Candidate generation may conclude that multiple capabilities or refinement are needed; this research does not create them.
8. **Is a model/schema change required?** No evidence of a model/schema change requirement from this research. Reassess only if candidate generation reveals a concrete structural gap.
9. **Can B02 proceed to candidate generation?** `PARTIAL`; candidate generation may proceed only as provisional, category-scoped proposals that retain the cross-reference and profile-selection dependencies. It must not assert representability or create a broad one-to-one mapping.
10. **Smallest unresolved question:** Under current law, what exact road-format/profile route is intended for MMTIS Article 5(1)(a) after 2015/962's repeal, and how does the existing MMTIS RRP guidance map its legacy road categories to 2022/670/current DATEX II RRP categories?

`B02_CANDIDATE_GENERATION_READY = PARTIAL`
`NEXT_ACTION = M06_B02_R2_TARGETED_RESEARCH`

R2 scope should be limited to the legal cross-reference bridge and category-by-category current DATEX II RRP mapping for road Annex 2.1/2.2 concepts. It need not investigate operators, datasets, Spanish profiles, capability creation, or schema design.

## Evidence classification and sources

| Source | Classification | Use / boundary |
|---|---|---|
| [EUR-Lex consolidated 2017/1926, 2024-03-04](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng) | `LEGAL_EVIDENCE` | Article 5 format/profile clauses; Annex 2.1/2.2 categories. |
| [EUR-Lex 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng) | `LEGAL_EVIDENCE` | Current RTTI regulation, repeal of 2015/962, DATEX II recital, scope. |
| [DATEX II MMTIS RRP overview](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/) and linked LS1/LS2/LS3 pages | `PROFILE_EVIDENCE`, `TECHNICAL_SPECIFICATION_EVIDENCE` | RRP purpose, minimum-data-element claim, profile families and categories; not proof of deployed content or legal cross-reference interpretation. |
| [CEN-CENELEC SIRI Part 7 announcement](https://www.cencenelec.eu/news-events/news/2025/eninthespotlight/2025-08-21-siri-7/) | `PROFILE_EVIDENCE`, `TECHNICAL_SPECIFICATION_EVIDENCE` | EPIP-RT purpose and functional scope. |
| [NEN CEN/TS 15531-7:2025 catalog entry](https://www.nen.nl/cen-ts-15531-7-2025-en-341552) | `TECHNICAL_SPECIFICATION_EVIDENCE` | Definitive status, title and publication date. |
| Project seed `03_Compliance/sql/03_mappings/phase3_m03_seed.sql` | `IMPLEMENTATION_GUIDANCE` / project catalog fact | Existing capability description and cautions; no mutation. |

Secondary sources were not used to determine legal meaning. No Spanish profile inventory was conducted; absence from this report is not evidence of non-existence.

## Execution accounting

| Item | Result |
|---|---|
| Preconditions | `PASS`: branch `main`; HEAD and `origin/main` both `258fad19f34e3ddc42467ba025392def27405257`; pre-write worktree clean |
| `DATABASE_WRITES` | `0` |
| `FILES_CREATED` | `1` (`03_Compliance/reports/phase_3/M06_B02_TARGETED_RESEARCH.md`) |
| `FILES_MODIFIED` | `0` |
| `COMMITS_CREATED` | `0` |
| `PUSH_EXECUTED` | `NO` |
| `GIT_DIFF_CHECK` | `PASS` — `git diff --check`; untracked report additionally checked for trailing whitespace |

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## R2 — CURRENT ROAD REGULATORY CHAIN

Research date: 2026-09-27. Scope: resolve the current road regulatory/technical chain for the two frozen requirements only. R1 above is retained unchanged. Sources checked: EUR-Lex and official DATEX II Recommended Reference Profile (RRP) documentation. This is documented project interpretation, not legal advice.

### Exact frozen requirement text and scope

The persisted Phase 2 row for `EU-2017-1926-REQ-A05-P01-002` reads: “Facilitar datos dinámicos de carretera mediante los formatos a los que remiten los artículos 5 y 6.” Its source fact reads: “Por lo que se refiere al transporte por carretera, mediante los formatos indicados en los artículos 5 y 6 del Reglamento Delegado (UE) 2015/962.” Provision: Article 5(1)(a). This is a road format requirement by reference; it does not itself enumerate individual data categories.

The persisted row for `EU-2017-1926-REQ-A05-P02-001` reads: “Los datos dinámicos de los puntos 2.1 y 2.2 del anexo a los que sean aplicables SIRI y DATEX II se representarán mediante perfiles mínimos de la UE o nacionales.” Its source fact reads: “Los datos dinámicos sobre desplazamientos y tráfico a que se refieren los puntos 2.1 y 2.2 del anexo, a los que son aplicables SIRI y DATEX II, se representarán mediante perfiles mínimos de la UE o nacionales.” Provision: Article 5(2). It is conditional and spans Annex categories, with applicability determined concept by concept; it is not a road-only requirement.

### Regulatory chain determination

| Classification | Finding |
|---|---|
| `A. LITERAL_TEXT_2017_1926` | Consolidated Article 5(1)(a) still literally points road transport to formats in Articles 5 and 6 of Regulation 2015/962. Article 5(2) still calls for minimum EU or national profiles for Annex 2.1/2.2 dynamic data to which SIRI and DATEX II apply. Neither text is rewritten here. |
| `B. CURRENT_STATUS_2015_962` | Repealed from 2025-01-01 by Article 15 of 2022/670; 2022/670 applies from that same date under Article 16. The old provisions are historical text, not the current RTTI instrument. |
| `C. CURRENT_RTTI_FRAMEWORK` | Regulation 2022/670 governs current EU-wide road RTTI data provision within its publicly accessible motorised road network scope and exceptions. Recitals 2, 3 and 26 identify 2015/962 as the previous framework, the update to its data-provision requirements, and the reason for repeal. This is an explicit relationship between RTTI instruments, not an amendment/substitution clause in MMTIS Article 5(1)(a). |
| `D. TECHNICAL_STANDARD_CURRENTLY_REQUIRED` | Category-dependent under 2022/670: Article 6(1) requires DATEX II for collected network-state data; Article 7(1) requires DATEX II for collected real-time network-use data, subject to its agreed machine-readable alternative; Article 5(1) allows listed standardised formats including DATEX II/TN-ITS for regulation/restriction data. 2022/670 does not recreate one general “DATEX II or fully compatible/interoperable format” rule for every item as old Articles 5–6 of 2015/962 did. |
| `E. CONSEQUENCE_FOR_B02` | The current RTTI framework and DATEX II profiles inform technical successor/context and candidate analysis. No operative amendment or cross-reference expressly substitutes 2022/670 for the still-literal MMTIS reference. Preserve this as `CURRENT_LEGAL_CONTEXT`; do not assert automatic legal substitution or rewrite Phase 2. |

Functional correspondence: former 2015/962 Article 5 addressed accessibility/exchange/re-use and formats for dynamic road status; its current category counterparts are principally 2022/670 Article 6 (network state) and Article 7 (real-time network use). Former Article 6 addressed traffic data; its closest current category counterpart is Article 7. Updates formerly handled in Articles 9–10 are now addressed by 2022/670 Articles 10–11 for network-state and real-time-use data. This is a functional crosswalk, not identical article numbering or scope.

EUR-Lex 2022/670 recitals 2, 3 and 26 explicitly connect the instruments: the earlier RTTI specifications were established in 2015/962, an update to data-provision requirements was needed, and 2015/962 should be repealed given the extent of changes. Separately, recital 4 of 2024/490 says its MMTIS amendments add parking data and remove charging/refuelling data to maintain consistency and avoid overlap with 2022/670. These are explicit legal links. They do not amend MMTIS Article 5(1)(a) to replace the named 2015/962 reference. That latter observation is `PROJECT_INTERPRETATION` from the operative texts.

### Atomic concepts and standard applicability

Mode labels classify the Annex concept, not every possible holder or instance. Standard applicability does not establish publication, implementation, or legal satisfaction.

| Requirement | Atomic data concept / Annex point | Mode | DATEX II | SIRI | Basis / boundary |
|---|---|---|---|---|---|
| P01 | Dynamic road status data, general road-format obligation | ROAD | YES | NO | Article 5(1)(a) names former 2015/962 Articles 5–6; current RTTI successor context includes DATEX II road profiles. Legal substitution into the literal MMTIS reference remains open. |
| P01 | Traffic/network-use data: traffic volume, speed, queues, travel times within former Article 6 subject | ROAD | YES | NO | Current RTTI Annex 6 with DATEX II format under Article 7(1); functional technical correspondence. |
| P02 | Disruptions: closures/diversions and causes if possible (2.1(i)) | ROAD for road disruption; otherwise MULTIMODAL | PARTIAL | PARTIAL | DATEX II MMTIS Level 1 directs road disruptions to RTTI profiles; SIRI may apply to non-road passenger disruption. Neither standard covers all modes by default. |
| P02 | Real-time service status: estimated departures/arrivals, delays, cancellations, guaranteed connections (2.1(ii)) | SCHEDULED_PUBLIC_TRANSPORT; MULTIMODAL | PARTIAL | YES | DATEX II MMTIS Level 1 includes all-mode concepts but directs road traffic to RTTI; SIRI is relevant for other-mode passenger service data. |
| P02 | Dynamic access-node status: platforms, lifts/escalators, closed entrances/exits (2.1(iii)) | SCHEDULED_PUBLIC_TRANSPORT | NOT_ESTABLISHED | PARTIAL | Passenger/facility real-time information is within SIRI's technical domain; exact Annex-element/profile correspondence was not established. No road RTTI equivalence found. |
| P02 | Parking tariff information (2.2(a)) | PERSONAL_TRANSPORT; TRANSPORT_ON_DEMAND | NOT_ESTABLISHED | NO | 2024/490 recital 4 places specified parking information in MMTIS to avoid overlap with RTTI 2022/670. No current RTTI road profile mapping established. |
| P02 | Shared car availability/location (2.2(b)(i)) | PERSONAL_TRANSPORT; MULTIMODAL | NOT_ESTABLISHED | NO | No matching RTTI category or official MMTIS DATEX II/SIRI profile mapping established. |
| P02 | Shared bike, scooter, and other shared-vehicle availability/location (2.2(b)(i)) | PERSONAL_TRANSPORT; MULTIMODAL; OTHER depending on vehicle | NOT_ESTABLISHED | NO | A shared car's road use does not make all shared-vehicle availability a road RTTI concept. No matching official profile mapping established. |
| P02 | On-street parking availability (2.2(b)(ii)) | PERSONAL_TRANSPORT; ROAD | NOT_ESTABLISHED | NO | 2024/490 recital 4 assigns specified parking information to MMTIS to avoid overlap with 2022/670; current DATEX II applicability/profile is not established here. |
| P02 | Off-street parking availability (2.2(b)(ii)) | PERSONAL_TRANSPORT; OTHER | NOT_ESTABLISHED | NO | Parking is within the MMTIS amendment context; off-street facilities are not automatically RTTI road-network use. |

No concept is classified `UNCLEAR`; uncertainty is represented by `PARTIAL` or `NOT_ESTABLISHED`. Annex detail comes from the frozen requirement/source text and consolidated 2017/1926 Annex 2.1/2.2.

### Current RTTI category correspondence

| MMTIS concept | Closest 2022/670 category | Relationship |
|---|---|---|
| 2.1(i) road disruptions | Annex 4: road/lane closures, roadworks, temporary traffic management; Annex 5: bridge closures, incidents, poor road conditions, adverse weather | Strong functional overlap for road disruptions; not equivalent to every all-mode MMTIS disruption. |
| 2.1(ii) road traffic status/travel time | Annex 6: volume, speed, queues, travel times, border waiting and other real-time use | Strong overlap for measured road traffic and travel time; not passenger scheduled-service status such as cancellations or guaranteed connections. |
| 2.1(ii) scheduled service status; 2.1(iii) access-node facilities | No corresponding RTTI Annex category established | Remains MMTIS passenger/mode concepts, outside the road-network mapping. |
| 2.2(a)/(b) parking and shared vehicles | No corresponding 2022/670 parking/shared-vehicle category established | 2024/490 recital 4 expressly places specified parking data in MMTIS to avoid overlap. No shared-vehicle RTTI mapping established. |

2022/670 also covers infrastructure and regulations/restrictions, but those are not additional concepts in these two frozen requirements; none are inferred into scope.

### DATEX II RRP profile match

Profile model/schema version is not stated consistently on the current profile pages; it is not inferred from the regulation's CEN/TS version family.

| CONCEPT | LEGAL_CATEGORY | CURRENT_RTTI_CATEGORY | DATEX_II_PROFILE | PROFILE_SCOPE | EVIDENCE | CONFIDENCE |
|---|---|---|---|---|---|---|
| Road disruptions/status within P02 2.1(i) and road subset of 2.1(ii) | MMTIS Annex 2.1(i)/(ii); road limb textually references 2015/962 | 2022/670 Annex 4/5 network state; Annex 6 real-time use as relevant | RTTI RRP family for 2022/670, using category-specific profile(s), not one blanket profile | Official catalog covers closures, works, incidents, poor road/weather conditions, temporary traffic management, volume/speed/queues/travel times; MMTIS Level 1 directs road profile use to RTTI | [MMTIS overview](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/); [2022/670 RTTI RRP catalog](https://docs.datex2.eu/recommended-profiles/rrp/rtti/rtti-670/); [MMTIS Level 1](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls1-passingtimes/) | HIGH technical family/scope; MEDIUM legal bridge |
| Current measured road-link travel times | MMTIS Annex 2.1 road/travel concept only where applicable | 2022/670 Annex 6(d) travel times | MMTIS Level 2 — Current road-link travel times | Current measured road-link times, not disruptions or full service status | [Profile](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls2a-current-road-link-travel-times/) | HIGH technical; MEDIUM legal pairing |
| Future predicted road-link travel times | No explicit discrete Annex 2.1/2.2 category established | 2022/670 Annex 7 predictive real-time-use data where in scope | MMTIS Level 3 — Future predicted road-link travel times | Forecast road-link travel times; not an explicit frozen concept beyond applicable scope | [Profile](https://docs.datex2.eu/recommended-profiles/rrp/mmtis/ls3-future-predicted-road-link-travel-times/) | HIGH technical; LOW/MEDIUM legal pairing |

No official current profile match is established here for parking, shared-vehicle availability, public-transport access-node status, or every non-road passenger-status concept. Do not manufacture those mappings from a general DATEX II capability statement.

### Existing capability

The `CAP-DATEXII-RRP-ROAD-TRAVEL` seed semantic scope is “road link travel times; MMTIS use cases”; evidence names current/future predicted road-link travel-time profiles and warns against assigning it to every Annex element.

| Requirement/concept | Catalog result | Reason |
|---|---|---|
| P01 road status and network-use data as a whole | PARTIALLY_COVERED | DATEX II/RRP is relevant, but the capability is travel-time-centred and does not cover all road data formats/categories. |
| P02 road disruptions, incidents, conditions, traffic state | NOT_COVERED | RTTI profile evidence exists; seed does not claim these profile scopes. |
| P02 current road-link travel times | COVERED | Expressly within the existing semantic scope. |
| P02 future predicted road-link travel times | PARTIALLY_COVERED | Seed mentions future profiles, but no assertion or dataset implementation exists. |
| P02 scheduled passenger service/access-node concepts | NOT_APPLICABLE to this road-travel capability | A separate SIRI/other-mode technical route may apply. |
| P02 parking/shared vehicles | NOT_COVERED | Not in the seed; no applicable DATEX profile mapping established here. |

`CAPABILITY_CATALOG_DECISION = MULTIPLE_CAPABILITIES` is the eventual category-scoped direction if the project elects to cover all applicable branches. `NEW_CAPABILITY_JUSTIFIED = NOT_ESTABLISHED` now because multiple mappings remain open and capability design belongs to candidate/model review. Reuse the existing capability only within its established travel-time scope.

### SIRI and representability boundary

`SIRI_B02_ACTION = PARTIAL`: no SIRI action for the road branch. Frozen P02 also includes non-road passenger concepts: scheduled service status (2.1(ii)) and access-node/facility status (2.1(iii)); SIRI is a relevant technical route under the other-mode limb of Article 5(1)(b). This boundary finding creates no SIRI capability and does not repeat a general SIRI investigation.

`STANDARD_REPRESENTABILITY` is separate from `OBSERVED_EVIDENCE`. Official specification/profile evidence is sufficient to establish standard-level DATEX II representability for road disruption/status and road-link travel-time concepts. No operator/NAP dataset is required for that finding or candidate generation. No dataset was examined: `OBSERVED_EVIDENCE_AVAILABLE = NO` for every row below; this does not mean data are absent.

| Requirement/candidate | STANDARD_REPRESENTABILITY_READY | OBSERVED_EVIDENCE_AVAILABLE |
|---|---|---|
| P01 road format concepts through current RTTI/DATEX II profile family | PARTIAL | NO |
| P02 road disruptions and traffic/travel-time concepts through DATEX II | PARTIAL | NO |
| P02 whole conditional scope including passenger status, access nodes, parking, shared vehicles | PARTIAL | NO |
| Existing `CAP-DATEXII-RRP-ROAD-TRAVEL` at its travel-time scope | YES | NO |

Whole-requirement readiness remains PARTIAL because standard applicability/profile selection is open for several concepts and the non-road branch is distinct. Dataset observation is a later evidence dimension, not a prerequisite for standard representability or provisional candidate generation.

### Phase 2 protection and decision

`CURRENT_LEGAL_CONTEXT`: MMTIS's consolidated cross-reference remains literally tied to 2015/962, now repealed. Regulation 2022/670 is the explicit current RTTI successor framework and provides functional DATEX II category/profile correspondence for portions of the road concepts. No operative source located says the MMTIS reference is automatically deemed amended to 2022/670. This is not proof of an extraction error.

`PHASE2_MODIFICATION_REQUIRED = NO`. Requirements, provisions, source facts, deadlines, Phase 2 reports, and database rows were not changed. No dataset audit or capability catalog change was made.

```text
COMPLIANCE_PHASE3_M06_B02_R2 = PARTIAL
2015_962_REPEALED = YES
CURRENT_RTTI_FRAMEWORK = Regulation (EU) 2022/670, applicable from 2025-01-01
DATEXII_CURRENT_ROLE = Required for specified network-state data under Art. 6 and real-time-use data under Art. 7, with category-specific formats/alternatives elsewhere; current RTTI technical framework, not an express replacement amendment to MMTIS Art. 5(1)(a)
A05_P01_002_DATEX_APPLICABILITY = YES
A05_P02_001_DATEX_APPLICABILITY = PARTIAL
SIRI_B02_ACTION = PARTIAL
EXISTING_CAPABILITY = PARTIAL
NEW_CAPABILITY_JUSTIFIED = NOT_ESTABLISHED
STANDARD_REPRESENTABILITY_READY = PARTIAL
REAL_NAP_DATASET_REQUIRED_BEFORE_CANDIDATE_GENERATION = NO
PHASE2_MODIFICATION_REQUIRED = NO
MODEL_CHANGE_REQUIRED = NO
B02_CANDIDATE_GENERATION_READY = PARTIAL
UNRESOLVED_BLOCKER = No explicit operative legal bridge substitutes Regulation 2022/670 for the still-literal 2015/962 reference in MMTIS Article 5(1)(a).
NEXT_ACTION = M06_B02_R3_TARGETED_RESEARCH
DATABASE_WRITES = 0
COMMITS = 0
PUSH = NO
```

R3 should resolve only the operative legal-bridge question, including whether an authoritative EU interpretive act or cross-reference exists. Once resolved, category-scoped candidate generation can proceed without a real NAP dataset; keep observed evidence `NO` until a later dataset audit is authorized.

Sources: [EUR-Lex 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng); [EUR-Lex 2024/490](https://eur-lex.europa.eu/eli/reg_del/2024/490/oj/eng); [EUR-Lex consolidated 2017/1926](https://eur-lex.europa.eu/eli/reg/2017/1926/2024-03-04/eng); [EUR-Lex 2015/962](https://eur-lex.europa.eu/eli/reg_del/2015/962/oj/eng).

## R3 — LEGAL BRIDGE RESOLUTION

Research date: 2026-09-27. Scope: resolve the remaining legal bridge only, using the exact frozen Phase 2 text and the R1/R2 findings above. Research only. No datasets were inspected; no database, capability, mapping, Phase 2, status, commit, or publication changes were made.

### Frozen text and authoritative bridge

The frozen Phase 2 source fact for `EU-2017-1926-REQ-A05-P01-002` is Article 5(1)(a): road transport is to use the formats indicated in Articles 5 and 6 of Regulation 2015/962. Its persisted requirement is “Facilitar datos dinámicos de carretera mediante los formatos a los que remiten los artículos 5 y 6.” The frozen source fact for `EU-2017-1926-REQ-A05-P02-001` is Article 5(2): applicable Annex 2.1/2.2 dynamic data are to be represented using minimum EU or national profiles. Its persisted requirement remains conditional on whether SIRI and/or DATEX II apply. These literal records remain the legal-source layer; the legal-context layer is separate.

The Commission's November 2024 revised [Implementation handbook for Regulation 2017/1926](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en) directly answers why the revised MMTIS text contains two different RTTI references (Q&A 4). It explains that most provisions of 2022/670, including repeal of 2015/962, applied only from 1 January 2025; 2022/670 could therefore be cited in MMTIS recitals while 2015/962 remained in its Articles because it remained applicable until 2025. It then expressly says legal references are “dynamic references” and that the latest applicable RTTI Delegated Regulation is applied when legally interpreting the act. This is an explicit Commission handbook bridge for interpretation of the old citation. The handbook itself states that it is for information purposes and does not legally bind the Commission; the finding records explicit Commission guidance, not a legislative amendment or a binding judgment.

Accordingly, R2's unresolved question about whether an authoritative interpretive bridge exists is resolved by this official Commission guidance. The handbook establishes dynamic-reference interpretation to the current RTTI act; it does not erase or rewrite the literal 2015/962 citation in the frozen MMTIS source. No claim is made that the two regulations are identical or that every old Article 5/6 rule has the same scope as a particular provision in 2022/670.

### Current regulation and framework evidence

EUR-Lex Regulation 2022/670 establishes the RTTI framework for accessibility, exchange, re-use and updating of data for accurate, cross-border EU-wide real-time traffic information services; its road scope is the publicly accessible motorised road network, subject to stated exceptions (Article 1). Article 16 applies it from 2025-01-01, and Article 15 repeals 2015/962 from that date. Recitals 2 and 26 identify the 2015/962 framework and the reason for its repeal. Recital 13 identifies DATEX II (CEN/TS 16157 and upgraded versions) among existing standards. Articles 6(1) and 7(1) require DATEX II for the specified collected network-state and real-time network-use data respectively, with the regulation's stated agreed/compatible alternative provisions; this is category-specific and is not a blanket rule for all MMTIS concepts. [EUR-Lex 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng)

The Commission presents these as concurrent ITS/NAP framework components: its revised MMTIS handbook describes Regulation 2017/1926 as MMTIS and says the 2024 revision increased consistency with other ITS delegated regulations, including 2022/670 for EU-wide RTTI (handbook, pp. 8–9). The Commission's [current NAP overview, updated October 2025](https://transport.ec.europa.eu/document/download/963c997d-efd9-40ae-a38b-5d4b935bdfcf_en?filename=its-national-access-points.pdf), separately labels 2017/1926 as the MMTIS NAP and 2022/670 as the RTTI NAP. Its [MMTIS page](https://transport.ec.europa.eu/transport-themes/smart-mobility/road/its-directive-and-action-plan/multimodal-travel-information_en) also continues to present 2017/1926 and its 2024 amendment as the MMTIS legal framework. This establishes current context and coexistence of distinct frameworks, not interchangeability of their scopes.

### Handbook search and R1/R2 technical consequence

Handbook search terms checked: `2015/962`, `2022/670`, `DATEX II`, `Article 5`, `dynamic road data`, and `RTTI`. The exact stale-reference issue is addressed explicitly in Q&A 4; Articles 5/6 and dynamic-data provisions are also described in the handbook. Classification: `HANDBOOK_BRIDGE = EXPLICIT`.

R1/R2 already establish official DATEX II RRP families for specified road-disruption/status and road-link travel-time concepts, and a distinct SIRI route for relevant scheduled passenger-service concepts. They also leave some Article 5(2) categories without a fully established category-to-profile link: parking and shared-vehicle concepts, certain non-road/access-node concept mappings, and the exact applicability of profiles to each data concept. The resolved cross-reference allows the legal-context chain to be modelled alongside the literal frozen source; it does not fill those profile gaps or expand DATEX II/SIRI applicability. No `2015/962 == 2022/670` equivalence is asserted.

`A05-P01-002` may proceed to candidate generation for road concepts supported by the current RTTI/DATEX II evidence, retaining its literal reference and marking the contextual current regulation. Candidate generation must remain category-scoped; the travel-time capability alone does not cover the whole road-format requirement. `A05-P02-001` may proceed concept-by-concept: supported road DATEX II concepts can have candidates; relevant SIRI passenger concepts can be considered on their own route; unsupported or unknown profile/category combinations remain `UNKNOWN` / `NEEDS_REVIEW`, with no forced single standard across the requirement.

Candidate `STANDARD_REPRESENTABILITY` can be prepared for profile-supported concepts using the chain `LEGAL SOURCE → CURRENT REGULATORY CONTEXT → OFFICIAL TECHNICAL PROFILE → CAPABILITY`. Overall readiness is partial because the whole conditional P02 scope is not mapped and existing capability coverage is incomplete. This is profile-level candidate readiness only: `OBSERVED_EVIDENCE_AVAILABLE = NO`; it does not establish that any NAP dataset publishes these elements or that an operator complies. A real dataset is not required before candidate generation.

### R3 decision

```text
COMPLIANCE_PHASE3_M06_B02_R3 = PASS
CURRENT_CONTEXT_PROPOSITION = ESTABLISHED
LITERAL_2017_1926_REFERENCE = 2015/962
2015_962_STATUS = REPEALED
2015_962_REPEAL_DATE = 2025-01-01
CURRENT_RTTI_REGULATION = 2022/670
SUCCESSOR_RELATIONSHIP = ESTABLISHED
AUTOMATIC_LEGAL_SUBSTITUTION = ESTABLISHED
AUTOMATIC_SUBSTITUTION_BASIS = Commission 2024 handbook expressly describes dynamic-reference interpretation; informational, not legally binding, and no textual amendment is implied
COMMISSION_CURRENT_FRAMEWORK_EVIDENCE = YES
HANDBOOK_BRIDGE = EXPLICIT
CURRENT_CONTEXT_MODEL_SAFE = YES
PHASE2_MODIFICATION_REQUIRED = NO
A05_P01_002_CANDIDATE_READY = YES
A05_P02_001_CANDIDATE_READY = PARTIAL
STANDARD_REPRESENTABILITY_READY = PARTIAL
REAL_NAP_DATASET_REQUIRED = NO
MODEL_CHANGE_REQUIRED = NO
B02_CANDIDATE_GENERATION_READY = PARTIAL
UNRESOLVED_LEGAL_QUESTION = None identified for the stale cross-reference. Residual non-legal profile mapping question: which official minimum EU/national profile elements apply to the remaining Article 5(2) parking/shared-vehicle and selected passenger/access-node concepts?
UNRESOLVED_QUESTION_CLASSIFICATION = NON_BLOCKING
NEXT_ACTION = M06_B02_CANDIDATE_GENERATION
DATABASE_WRITES = 0
COMMITS_CREATED = 0
PUSH_EXECUTED = NO
```

No R4 is warranted: the specified authoritative source (the post-2024 Commission implementation handbook) was located and examined, and it resolves the identified bridge. The remaining concept/profile uncertainty does not block scoped candidate generation and does not justify another legal-bridge iteration. Preserve it as an explicit concept-level review item for candidate work; do not treat it as evidence of missing data or non-compliance.

Sources: [Commission 2024 implementation handbook, Q&A 4](https://transport.ec.europa.eu/document/download/0b75db16-35b1-41df-8229-5c8abfec534d_en); [EUR-Lex 2022/670](https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng); [Commission NAP overview (October 2025)](https://transport.ec.europa.eu/document/download/963c997d-efd9-40ae-a38b-5d4b935bdfcf_en?filename=its-national-access-points.pdf); [Commission MMTIS framework page](https://transport.ec.europa.eu/transport-themes/smart-mobility/road/its-directive-and-action-plan/multimodal-travel-information_en).
