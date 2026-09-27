-- Phase 3 M02: additive framework only. No legal mappings or researched capabilities.
CREATE SCHEMA IF NOT EXISTS mapping;

CREATE TABLE IF NOT EXISTS mapping.phase3_vocabularies (
    vocabulary VARCHAR NOT NULL,
    value VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    PRIMARY KEY (vocabulary, value)
);

INSERT INTO mapping.phase3_vocabularies VALUES
('MAPPING_TYPE','DIRECT','Direct representation'),('MAPPING_TYPE','DERIVED','Derived from multiple elements'),('MAPPING_TYPE','PARTIAL','Only part of the requirement is represented'),('MAPPING_TYPE','CONDITIONAL','Representation depends on conditions'),('MAPPING_TYPE','EXTERNAL_EVIDENCE','Evidence outside the data format'),('MAPPING_TYPE','NON_FORMAT_EVIDENCE','Evidence is not a format representation'),
('REPRESENTABILITY','AVAILABLE','Semantic concept can be represented'),('REPRESENTABILITY','MAPPABLE','Representation requires a defined transformation'),('REPRESENTABILITY','PARTIAL','Only part of the concept can be represented'),('REPRESENTABILITY','MISSING','No representation identified for this scoped capability'),('REPRESENTABILITY','UNKNOWN','Not yet assessed'),('REPRESENTABILITY','NOT_APPLICABLE','Representation does not apply in this context'),
('EVIDENCE_TYPE','DATASET','Dataset'),('EVIDENCE_TYPE','FILE','File'),('EVIDENCE_TYPE','ENTITY','Entity or table'),('EVIDENCE_TYPE','FIELD','Field or element'),('EVIDENCE_TYPE','API_SERVICE','API or service'),('EVIDENCE_TYPE','METADATA_DOCUMENT','Metadata document'),('EVIDENCE_TYPE','EXTERNAL_DOCUMENT','External document'),
('AUTOMATABILITY','AUTOMATIC','Potentially fully machine-auditable'),('AUTOMATABILITY','PARTIAL','Some checks may be automated'),('AUTOMATABILITY','MANUAL','Requires human assessment'),('AUTOMATABILITY','NOT_AUDITABLE','No audit approach currently identified'),('AUTOMATABILITY','UNKNOWN','Not yet assessed'),
('REVIEW_STATE','UNREVIEWED','Not reviewed'),('REVIEW_STATE','NEEDS_REVIEW','Requires review'),('REVIEW_STATE','REVIEWED','Reviewed'),('REVIEW_STATE','APPROVED','Approved for reuse'),('REVIEW_STATE','REJECTED','Rejected'),
('FAMILY_RELATION','PRIMARY_FAMILY','Primary semantic family'),('FAMILY_RELATION','SECONDARY_CHARACTERISTIC','Secondary characteristic'),
('EXCEPTION_TYPE','LEGAL_PROCESS','Legal or process obligation'),('EXCEPTION_TYPE','DEADLINE','Deadline or temporal obligation'),('EXCEPTION_TYPE','ORGANIZATIONAL','Organizational duty'),('EXCEPTION_TYPE','CONDUCT','Conduct obligation'),('EXCEPTION_TYPE','EXTERNAL_EVIDENCE','Requires evidence outside format'),('EXCEPTION_TYPE','MANUAL_ASSESSMENT','Requires manual assessment')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS mapping.phase3_standards (
    standard_id VARCHAR PRIMARY KEY,
    standard_name VARCHAR NOT NULL,
    standard_kind VARCHAR NOT NULL CHECK (standard_kind IN ('GTFS_SCHEDULE','GTFS_REALTIME','NETEX','SIRI')),
    version VARCHAR,
    profile VARCHAR,
    service_or_subprofile VARCHAR,
    jurisdiction_context VARCHAR,
    valid_from DATE,
    valid_to DATE,
    source_metadata VARCHAR,
    registry_status VARCHAR NOT NULL CHECK (registry_status IN ('IDENTITY_ONLY','REVIEWED')),
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_capabilities (
    capability_id VARCHAR PRIMARY KEY,
    standard_id VARCHAR NOT NULL,
    domain VARCHAR,
    entity VARCHAR,
    field_or_element VARCHAR,
    semantic_meaning VARCHAR NOT NULL,
    cardinality VARCHAR,
    required_or_optional VARCHAR CHECK (required_or_optional IS NULL OR required_or_optional IN ('REQUIRED','OPTIONAL','CONDITIONAL')),
    conditions VARCHAR,
    profile_dependency VARCHAR,
    evidence_type VARCHAR,
    limitations VARCHAR,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    FOREIGN KEY (standard_id) REFERENCES mapping.phase3_standards(standard_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_source_references (
    source_reference_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR NOT NULL,
    source_kind VARCHAR NOT NULL CHECK (source_kind IN ('OFFICIAL_SPECIFICATION','OFFICIAL_PROFILE','OTHER')),
    specification_name VARCHAR,
    version VARCHAR,
    section VARCHAR,
    url_or_document_id VARCHAR NOT NULL,
    retrieved_on DATE,
    reviewed_on DATE,
    notes VARCHAR,
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    FOREIGN KEY (capability_id) REFERENCES mapping.phase3_capabilities(capability_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_requirement_capabilities (
    mapping_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR NOT NULL,
    capability_id VARCHAR NOT NULL,
    mapping_type VARCHAR NOT NULL CHECK (mapping_type IN ('DIRECT','DERIVED','PARTIAL','CONDITIONAL','EXTERNAL_EVIDENCE','NON_FORMAT_EVIDENCE')),
    mapping_conditions VARCHAR,
    limitations VARCHAR,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    UNIQUE(requirement_id, capability_id),
    FOREIGN KEY (capability_id) REFERENCES mapping.phase3_capabilities(capability_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_representability (
    representability_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR NOT NULL,
    representability_state VARCHAR NOT NULL CHECK (representability_state IN ('AVAILABLE','MAPPABLE','PARTIAL','MISSING','UNKNOWN','NOT_APPLICABLE')),
    explanation VARCHAR,
    conditions VARCHAR,
    assessed_on DATE,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    CHECK (representability_state NOT IN ('PARTIAL','MISSING','UNKNOWN','NOT_APPLICABLE') OR length(trim(coalesce(explanation,''))) > 0),
    FOREIGN KEY (capability_id) REFERENCES mapping.phase3_capabilities(capability_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_observed_evidence (
    evidence_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR,
    mapping_id VARCHAR,
    evidence_type VARCHAR NOT NULL CHECK (evidence_type IN ('DATASET','FILE','ENTITY','FIELD','API_SERVICE','METADATA_DOCUMENT','EXTERNAL_DOCUMENT')),
    locator VARCHAR NOT NULL,
    observed_value VARCHAR,
    observed_on DATE,
    notes VARCHAR,
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    CHECK (capability_id IS NOT NULL OR mapping_id IS NOT NULL),
    FOREIGN KEY (capability_id) REFERENCES mapping.phase3_capabilities(capability_id),
    FOREIGN KEY (mapping_id) REFERENCES mapping.phase3_requirement_capabilities(mapping_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_automatability (
    automatability_id VARCHAR PRIMARY KEY,
    mapping_id VARCHAR NOT NULL,
    automatability_state VARCHAR NOT NULL CHECK (automatability_state IN ('AUTOMATIC','PARTIAL','MANUAL','NOT_AUDITABLE','UNKNOWN')),
    explanation VARCHAR,
    prerequisites VARCHAR,
    assessed_on DATE,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    FOREIGN KEY (mapping_id) REFERENCES mapping.phase3_requirement_capabilities(mapping_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_families (
    family_id VARCHAR PRIMARY KEY,
    family_name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    provisional BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS mapping.phase3_requirement_families (
    requirement_id VARCHAR NOT NULL,
    family_id VARCHAR NOT NULL,
    relation_type VARCHAR NOT NULL CHECK (relation_type IN ('PRIMARY_FAMILY','SECONDARY_CHARACTERISTIC')),
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    PRIMARY KEY(requirement_id, family_id, relation_type),
    FOREIGN KEY (family_id) REFERENCES mapping.phase3_families(family_id)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_exceptions (
    exception_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR NOT NULL,
    exception_type VARCHAR NOT NULL CHECK (exception_type IN ('LEGAL_PROCESS','DEADLINE','ORGANIZATIONAL','CONDUCT','EXTERNAL_EVIDENCE','MANUAL_ASSESSMENT')),
    reason VARCHAR NOT NULL,
    justification VARCHAR NOT NULL,
    evidence_expectations VARCHAR NOT NULL,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST')
);

CREATE INDEX IF NOT EXISTS idx_phase3_mapping_requirement ON mapping.phase3_requirement_capabilities(requirement_id);
CREATE INDEX IF NOT EXISTS idx_phase3_mapping_capability ON mapping.phase3_requirement_capabilities(capability_id);
