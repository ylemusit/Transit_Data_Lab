# M06-B01 candidate review package — F01 NAP access/discovery

> Historical candidate-generation snapshot, before R1 and human semantic review. The status, proposals, and zero-write counts in this section describe that earlier stage and are preserved as recorded.

Mode: `CANDIDATE_GENERATION`
Status: `NEEDS_HUMAN_SEMANTIC_REVIEW`
Scope: the three listed requirements only. Family membership is planning metadata and does not determine mapping or legal coverage.

## Summary

The existing catalog has five capabilities, all scoped to GTFS, NeTEx, or DATEX II transport-data concepts. None establishes a national access point, its institutional single-point role, or the meaning of its location services. No new reusable technical capability is justified from the materialized requirements and current project evidence alone. No source references, mappings, automatability records, representability assertions, observed evidence, or final coverage decisions were created.

Three `NEEDS_REVIEW` exception paths preserve the institutional/procedural evidence dependencies. For the location-services requirement, targeted research is required before semantic review can resolve whether a technical capability is appropriate. No research was performed in this batch.

## Requirement analyses and proposals

### EU-2017-1926-REQ-A03-P01-001

- Source: `EU-2017-1926-ART03`; Article 3. Materialized source fact: `EU-2017-1926-SF-A03-P01`.
- Archetype: institutional establishment duty. Responsible party: Member State. Beneficiary: data users. Action: establish the national access point. Object: the access point itself.
- External/procedural dependency: authoritative evidence that the responsible Member State established/designated the national access point.
- Existing capabilities: all five reviewed; none relevant. No new capability and no candidate technical mapping.
- Exception path: `LEGAL_PROCESS`, `M06-B01-EXC-A03-P01-001` (`NEEDS_REVIEW`).
- Automatability: not applicable without a technical mapping; documentary evidence may support a later human assessment but cannot itself establish legal compliance.
- Proposed coverage: `NONE_IDENTIFIED` for technical capability coverage. This is not a final coverage decision.
- Limitations/unresolved: no official NAP identity or establishment evidence was evaluated. Targeted research: no; this is an evidence dependency, not a question needed to define a transport-format mapping.

### EU-2017-1926-REQ-A03-P01-002

- Source: `EU-2017-1926-ART03`; Article 3(1). Materialized source fact: `EU-2017-1926-SF-A03-P01`.
- Archetype: organizational/institutional access arrangement. Responsible party: Member State. Beneficiary: data users. Action/condition: the national access point serves as the single access point for covered categories and updates in the Member State's territory.
- External/procedural dependency: authoritative description of the designated point, its scope, and covered categories/data holders.
- Existing capabilities: all five reviewed; none contributes a demonstrated semantic mapping. No new capability and no candidate technical mapping.
- Exception path: `ORGANIZATIONAL`, `M06-B01-EXC-A03-P01-002` (`NEEDS_REVIEW`).
- Automatability: not applicable without a technical mapping; the organizational scope requires documentary and human assessment.
- Proposed coverage: `NONE_IDENTIFIED` for technical capability coverage. This is not a final coverage decision.
- Limitations/unresolved: materialized row does not enumerate categories/data holders. No national implementation evidence was examined. Targeted research: no, unless a later reviewer chooses to investigate the institutional designation.

### EU-2017-1926-REQ-A03-P03-001

- Source: `EU-2017-1926-ART03`; Article 3(3). Materialized source fact: `EU-2017-1926-SF-A03-P03`.
- Archetype: discovery/location service duty. Responsible party: national access point. Beneficiary: data users. Action: provide location services. Object: service behavior; its mechanism is not specified in the materialized requirement.
- External/technical dependency: definition of expected location-service behavior and any interface/specification, plus evidence of service operation.
- Existing capabilities: all five reviewed; none specifies NAP discovery or location services. No new capability and no candidate technical mapping; the term alone is insufficient to define a reusable, evidence-backed capability.
- Exception path: `MANUAL_ASSESSMENT`, `M06-B01-EXC-A03-P03-001` (`NEEDS_REVIEW`).
- Automatability: not applicable without a technical mapping. Any later assessment depends on resolving the service semantics and identifying suitable evidence.
- Proposed coverage: `UNRESOLVED`. This is a proposal only.
- Limitations/unresolved: meaning, interface, users, and evidence criteria for “location services” remain unknown. `TARGETED_RESEARCH_REQUIRED` before human semantic review of a technical mapping.

## Human review questions

1. Are the `LEGAL_PROCESS`, `ORGANIZATIONAL`, and `MANUAL_ASSESSMENT` exception paths appropriate for these three distinct duties?
2. Is `NONE_IDENTIFIED` the right technical coverage proposal for the establishment and single-point-role requirements?
3. For Article 3(3), what authoritative source should define “location services” before deciding whether a reusable technical capability exists?
4. Are the stated institutional evidence expectations sufficiently bounded without implying compliance?
5. Confirm that no final semantic mapping or coverage decision has been made in this candidate package.

Human outcomes remain open: `ACCEPT`, `ACCEPT_WITH_LIMITATIONS`, `REJECT`, or `UNRESOLVED`.

## M06-B01-R1 — targeted research: discovery services

Research date: 2026-09-27. Scope limited to `EU-2017-1926-REQ-A03-P03-001`. No database inspection or writes were needed to answer this legal/semantic question. This section supplements the candidate analysis above; it does not approve a mapping, capability, exception, or coverage state.

### Sources and legal concepts

Primary source: [Commission Delegated Regulation (EU) 2017/1926, consolidated text of 04/03/2024, Spanish](https://eur-lex.europa.eu/eli/reg/2017/1926/spa) (Article 2 definitions and Article 3(3)–(4)); the corresponding [English consolidated text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02017R1926-20240304) was used to cross-check the terms. For terminology history only: [official Spanish text published in 2017](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX%3A02017R1926-20171021).

- **Accesibilidad de los datos** (Article 2(20), consolidated text): posibilidad de solicitar y obtener los datos en cualquier momento en un formato digital legible por máquina. This is a separate concept from finding a dataset in a catalogue.
- **Metadatos** (Article 2(14)): descripción estructurada del contenido de los datos que facilita su búsqueda y utilización.
- **Servicio de búsqueda** (Article 2(19)): servicio que permite buscar los datos solicitados utilizando el contenido de los metadatos correspondientes y mostrando ese contenido. Its specified functional behavior is dataset discovery and presentation of corresponding metadata.
- **Punto de acceso** (Article 2(17)): interfaz digital through which the Annex data and corresponding metadata, or their sources and metadata, are accessible to data users for reuse. Article 3(1) requires each Member State to establish an NAP, serving as a single access point to the listed data in its territory; the definition of access point alone does not establish that a particular interface has that national designation or role.

### Article 3(3)–(4)

**Article 3(3)**

- **Actor:** los puntos de acceso nacionales.
- **Action:** deben proporcionar.
- **Function:** servicios de búsqueda para los usuarios de datos.
- **Input:** solicitud de datos y metadatos correspondientes; Article 2(19) defines the service by searching requested data using corresponding metadata. The Regulation does not prescribe a request syntax or technical input format.
- **Observable requirement:** a user can search for requested datasets using corresponding metadata and the service displays that metadata. This describes required behavior, not a mandated interface or implementation.

**Article 3(4)**

- **Data-holder actors:** the defined data holders (legal persons or public/private entities with the right to grant access to or share data under their control, including transport authorities, operators, infrastructure managers, and on-demand transport providers).
- **Metadata obligation:** Member States, cooperating with relevant ITS stakeholders, are to reach agreement on metadata requirements; data holders must provide metadata on that basis.
- **Relation to discovery:** metadata is an operational dependency of the defined discovery behavior because the search uses corresponding metadata and displays its contents. Responsibilities remain distinct: Member States/stakeholders agree requirements; data holders supply metadata; NAPs provide discovery services. This does not mean Article 3(4) itself requires any particular catalogue or metadata schema.

### Terminology and scope of the capability

The project's phrase **«servicios de localización»** reflects the official Spanish wording in the original 2017 text. In the Spanish consolidated text dated 04/03/2024 the defined term is **«servicio de búsqueda»**. The underlying definition concerns discovery of data by metadata, not geographic location, GPS positioning, vehicle localization, stop coordinates, or geocoding. Record this as a terminology clarification; do not rewrite frozen Phase 2 wording in this task.

**Capability assessment (proposal only):**

- Proposed capability: `NAP_DATA_DISCOVERY`.
- Proposed definition: functional capability of a digital access point to let data users search requested datasets using corresponding metadata and display that metadata.
- Reusable: **YES** — the behavior is separable from any one transport mode, data format, or implementation.
- Technical or functional: **YES**, functional/observable software behavior.
- Legal requirement restatement: **NO** — it models the reusable behavior described by the legal definition; the actor and duty remain in the requirement.
- Evidence sufficient: **YES** to define a conceptual capability and take it to semantic review; **NO** to assert implementation or compliance without implementation evidence.
- Capability catalog suitable: **YES**, as a proposed new functional capability, subject to human semantic review. Do not create it in this research task.

This capability does **not** prove: that an NAP has been legally established; that an interface is the legally designated national single point; that all required datasets are present; that metadata are complete; that datasets are machine-readable; that datasets conform to required formats; data quality; or legal compliance. Discovery is distinct from accessibility of dataset contents, completeness, quality, conformity, and institutional designation.

### Automatability and future evidence

- Proposed automatability: **PARTIAL**.
- Reason: observable search and metadata-display behavior can be tested automatically where a usable interface, endpoint, catalogue, and controlled query/expected result are available. Determining complete real-world coverage, metadata adequacy, representativeness, and legal designation may require documentary and human assessment. A search API, catalogue protocol, or web interface is a possible implementation/evidence source, not a mechanism mandated by Article 3(3).
- Discovery existence: authoritative NAP documentation plus a reachable search interface/catalogue/endpoint, captured with date, URL, and response or screen evidence.
- Discovery behavior: repeatable query/response evidence showing the requested dataset is findable through metadata and that corresponding metadata are displayed; include test query, expected result, observed result, and capture.
- Metadata dependency: metadata requirement agreement or specification, data-holder metadata records, and a trace showing the search uses corresponding metadata and returns/displays it.
- Legal NAP status: official Member State legal/administrative designation or authoritative government/competent-authority record identifying the NAP and its single-point role. Technical availability alone is insufficient.

### B01 impact and proposed human-review input

- `A03-P01-001` changed: **NO**. Establishment remains an institutional/legal-process path.
- `A03-P01-002` changed: **NO**. Single-point access arrangement remains an organizational/access-point architecture path.
- `A03-P03-001` research status: **RESEARCH_RESOLVED**; ready for human semantic review, not approved.
- Proposed exception path: retain `MANUAL_ASSESSMENT` provisionally for implementation/external evidence assessment; semantic reviewer may revisit it after examining evidence.
- Proposed candidate mapping: `EU-2017-1926-REQ-A03-P03-001` → `NAP_DATA_DISCOVERY` (NAP provides metadata-based dataset search and displays corresponding metadata); candidate only, not persisted.
- Proposed coverage: `UNRESOLVED` pending human review and evidence of an actual implementation. Do not infer coverage from the legal definition alone.

Research disposition: **RESEARCH_RESOLVED** for the meaning and modeling question. This work does not reopen Phase 1 or Phase 2, alter frozen wording, or determine Spain's implementation/compliance.

COMPLIANCE_PHASE3_M06_B01_R1 = **PASS** (targeted research complete; no compliance gate passed)

RESEARCH_SCOPE = `A03-P03-001_DISCOVERY_SERVICES`

CURRENT_CONSOLIDATED_VERSION = `04/03/2024`

DATABASE_WRITES = `0`
MAPPINGS_CREATED = `0`
CAPABILITIES_CREATED = `0`
COVERAGE_DECISIONS_CREATED = `0`
FILES_CHANGED = `03_Compliance/reports/phase_3/M06_B01_HUMAN_REVIEW.md`
COMMITS_CREATED = `0`
PUSH_EXECUTED = `NO`
RESOURCE_GUARD_TRIGGERED = `NO`

FINAL_ASSESSMENT: Discovery services are metadata-based dataset search and metadata display. They concern data discovery, not geographic positioning. They operationally depend on metadata. The Regulation mandates the behavior, not a particular API or search technology. `NAP_DATA_DISCOVERY` is a valid reusable functional capability proposal, bounded as above. `A03-P03-001` can proceed to human semantic review. This research does not require reopening Phase 1 or Phase 2.

NEXT_ACTION = `M06_B01_HUMAN_SEMANTIC_REVIEW`

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

---

## M06-B01-HR — human semantic review and persisted state (2026-09-27)

This section records the subsequent human review. The candidate-generation and R1 research record above is preserved as history; the earlier statement that no rows were persisted describes that earlier R1 stage only.

### Model review and migration

- Migration `009_phase_3_m06_b01_unbound_capabilities.sql` was already applied. `phase3_capabilities.standard_id` accepts `NULL`; unknown non-NULL standard IDs remain rejected by the foreign key; `OFFICIAL_LEGAL_SOURCE` is supported.
- The five original capabilities retain their non-NULL standard bindings. No capability kind, N:M standard binding, or NAP standard was added.
- Counts before human review: 3 standards, 5 capabilities, 7 mapping source references, 5 mappings, 5 mapping reviews, and 5 coverage decisions.

### Human semantic decisions

- `A03-P01-001`: `ACCEPTED_WITH_LIMITATIONS`; no technical capability mapping; `LEGAL_PROCESS`; coverage `PARTIAL`.
- `A03-P01-002`: `ACCEPTED_WITH_LIMITATIONS`; no technical capability mapping; `ORGANIZATIONAL`; coverage `PARTIAL`.
- `A03-P03-001`: `ACCEPTED_WITH_LIMITATIONS`; mapped to the reusable functional capability `NAP_DATA_DISCOVERY`; `MANUAL_ASSESSMENT` remains in force alongside it; coverage `PARTIAL`.

### Persisted state

- Created exactly one `NAP_DATA_DISCOVERY` capability with `standard_id = NULL`, catalog state `REVIEWED`, and explicit limitations. The capability is metadata-based dataset discovery and metadata display/exposure.
- Added one source reference, `M06-B01-SRC-REG-2017-1926`, classified `OFFICIAL_LEGAL_SOURCE` and pointing to the already captured consolidated Regulation text. This reuses the local source-fact URL; no web research was done. Mapping source-reference count: 7 → 8.
- Created exactly one B01 capability mapping, `M06-B01-MAP-A03-P03-001-NAP-DISCOVERY`, and one separate semantic review `ACCEPTED_WITH_LIMITATIONS`.
- Persisted one `PARTIAL` automatability record for that mapping and exactly three B01 coverage decisions, all `PARTIAL / ACCEPTED_WITH_LIMITATIONS`.
- The three candidate exception paths remain: `LEGAL_PROCESS`, `ORGANIZATIONAL`, and `MANUAL_ASSESSMENT`. The first two requirements have no capability mapping. The manual path for `A03-P03-001` coexists with the functional mapping.
- Created no representability assertions, observed-evidence rows, or audit rules. `NAP_DATA_DISCOVERY` does not assert NAP establishment/designation, complete required datasets or metadata, machine-readable access, format conformance, data quality, or legal compliance. It does not mean geographic/GPS/vehicle localization, stop coordinates, or geocoding, and it does not prescribe an API or implementation technology.

### Reproducibility and validation

- Review seed: `03_Compliance/sql/03_mappings/phase3_m06_b01_review_seed.sql`.
- The seed was executed twice. The second run changed neither substantive counts nor the database bytes; SHA-256 before and after the second run: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4`.
- The one-time migration test passed without rerunning migration 009. It verified nullable standard binding, rejection of unknown non-NULL bindings, fixture rollback, and that the five non-NAP capability rows have non-NULL bindings.
- Regression results: Level A **PASS**; M04 **PASS**; M04B **PASS**; M05B schema **PASS**; M05B family **PASS**; migration test **PASS**; B01 reviewed validator **PASS**; global exception accounting **PASS** (M04 3, B01 3, unaccounted 0).
- M04/M04B/M05B validator scope filters were updated to keep their historical five pilot mappings/reviews/coverage checks local while recognizing the separately reviewed B01 batch. No M04 rows or decisions were changed.
- Final counts: requirements 48; deadlines 10; candidates 34; source facts 36; standards 3; capabilities 6; source references 8; mappings 6 (pilot 5, B01 1); mapping reviews 6; coverage decisions 8; automatability records 6 (B01 1); families 9; family memberships 48; representability 0; observed evidence 0; audit rules 0.

COMPLIANCE_PHASE3_M06_B01_HUMAN_REVIEW = **PASS**

NO LEGAL COMPLIANCE CONCLUSION: **This review records semantic mapping and evaluation coverage only.**

NEXT_ACTION = `M06_B01_CHECKPOINT`

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
