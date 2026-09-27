-- M02A: remove the closed standard_kind identity list, preserving all Phase 3 rows.
-- DuckDB cannot replace a referenced parent table in place. Rebuild the full FK subgraph atomically.
BEGIN TRANSACTION;

CREATE TEMP TABLE m02a_standards AS SELECT * FROM mapping.phase3_standards;
CREATE TEMP TABLE m02a_capabilities AS SELECT * FROM mapping.phase3_capabilities;
CREATE TEMP TABLE m02a_source_references AS SELECT * FROM mapping.phase3_source_references;
CREATE TEMP TABLE m02a_requirement_capabilities AS SELECT * FROM mapping.phase3_requirement_capabilities;
CREATE TEMP TABLE m02a_representability AS SELECT * FROM mapping.phase3_representability;
CREATE TEMP TABLE m02a_observed_evidence AS SELECT * FROM mapping.phase3_observed_evidence;
CREATE TEMP TABLE m02a_automatability AS SELECT * FROM mapping.phase3_automatability;

-- Guard the expected M03 state and ensure the migration is based on the live records.
SELECT CASE WHEN
  (SELECT count(*) FROM m02a_standards)=3 AND
  (SELECT count(*) FROM m02a_capabilities)=5 AND
  (SELECT count(*) FROM m02a_source_references)=7 AND
  (SELECT count(*) FROM mapping.phase3_exceptions)=3 AND
  (SELECT count(*) FROM m02a_requirement_capabilities)=0 AND
  (SELECT count(*) FROM m02a_representability)=0
  THEN 'M02A_PREFLIGHT_PASS' ELSE error('M02A preflight counts differ from expected M03 state') END;

-- Explicit reverse-FK dependency order (DuckDB does not cascade-drop these FK dependents).
DROP TABLE mapping.phase3_observed_evidence;
DROP TABLE mapping.phase3_automatability;
DROP TABLE mapping.phase3_requirement_capabilities;
DROP TABLE mapping.phase3_representability;
DROP TABLE mapping.phase3_source_references;
DROP TABLE mapping.phase3_capabilities;
DROP TABLE mapping.phase3_standards;

CREATE TABLE mapping.phase3_standards (
    standard_id VARCHAR PRIMARY KEY,
    standard_name VARCHAR NOT NULL,
    standard_kind VARCHAR NOT NULL,
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

CREATE TABLE mapping.phase3_capabilities (
    capability_id VARCHAR PRIMARY KEY,
    standard_id VARCHAR NOT NULL REFERENCES mapping.phase3_standards(standard_id),
    domain VARCHAR, entity VARCHAR, field_or_element VARCHAR,
    semantic_meaning VARCHAR NOT NULL, cardinality VARCHAR,
    required_or_optional VARCHAR CHECK (required_or_optional IS NULL OR required_or_optional IN ('REQUIRED','OPTIONAL','CONDITIONAL')),
    conditions VARCHAR, profile_dependency VARCHAR, evidence_type VARCHAR, limitations VARCHAR,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST')
);
CREATE TABLE mapping.phase3_source_references (
    source_reference_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR NOT NULL REFERENCES mapping.phase3_capabilities(capability_id),
    source_kind VARCHAR NOT NULL CHECK (source_kind IN ('OFFICIAL_SPECIFICATION','OFFICIAL_PROFILE','OTHER')),
    specification_name VARCHAR, version VARCHAR, section VARCHAR,
    url_or_document_id VARCHAR NOT NULL, retrieved_on DATE, reviewed_on DATE, notes VARCHAR,
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST')
);
CREATE TABLE mapping.phase3_requirement_capabilities (
    mapping_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR NOT NULL,
    capability_id VARCHAR NOT NULL REFERENCES mapping.phase3_capabilities(capability_id),
    mapping_type VARCHAR NOT NULL CHECK (mapping_type IN ('DIRECT','DERIVED','PARTIAL','CONDITIONAL','EXTERNAL_EVIDENCE','NON_FORMAT_EVIDENCE')),
    mapping_conditions VARCHAR, limitations VARCHAR,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    UNIQUE(requirement_id, capability_id)
);
CREATE TABLE mapping.phase3_representability (
    representability_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR NOT NULL REFERENCES mapping.phase3_capabilities(capability_id),
    representability_state VARCHAR NOT NULL CHECK (representability_state IN ('AVAILABLE','MAPPABLE','PARTIAL','MISSING','UNKNOWN','NOT_APPLICABLE')),
    explanation VARCHAR, conditions VARCHAR, assessed_on DATE,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    CHECK (representability_state NOT IN ('PARTIAL','MISSING','UNKNOWN','NOT_APPLICABLE') OR length(trim(coalesce(explanation,''))) > 0)
);
CREATE TABLE mapping.phase3_observed_evidence (
    evidence_id VARCHAR PRIMARY KEY,
    capability_id VARCHAR REFERENCES mapping.phase3_capabilities(capability_id),
    mapping_id VARCHAR REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
    evidence_type VARCHAR NOT NULL CHECK (evidence_type IN ('DATASET','FILE','ENTITY','FIELD','API_SERVICE','METADATA_DOCUMENT','EXTERNAL_DOCUMENT')),
    locator VARCHAR NOT NULL, observed_value VARCHAR, observed_on DATE, notes VARCHAR,
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    CHECK (capability_id IS NOT NULL OR mapping_id IS NOT NULL)
);
CREATE TABLE mapping.phase3_automatability (
    automatability_id VARCHAR PRIMARY KEY,
    mapping_id VARCHAR NOT NULL REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
    automatability_state VARCHAR NOT NULL CHECK (automatability_state IN ('AUTOMATIC','PARTIAL','MANUAL','NOT_AUDITABLE','UNKNOWN')),
    explanation VARCHAR, prerequisites VARCHAR, assessed_on DATE,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST')
);

INSERT INTO mapping.phase3_standards SELECT * FROM m02a_standards;
INSERT INTO mapping.phase3_capabilities SELECT * FROM m02a_capabilities;
INSERT INTO mapping.phase3_source_references SELECT * FROM m02a_source_references;
INSERT INTO mapping.phase3_requirement_capabilities SELECT * FROM m02a_requirement_capabilities;
INSERT INTO mapping.phase3_representability SELECT * FROM m02a_representability;
INSERT INTO mapping.phase3_observed_evidence SELECT * FROM m02a_observed_evidence;
INSERT INTO mapping.phase3_automatability SELECT * FROM m02a_automatability;

CREATE INDEX idx_phase3_mapping_requirement ON mapping.phase3_requirement_capabilities(requirement_id);
CREATE INDEX idx_phase3_mapping_capability ON mapping.phase3_requirement_capabilities(capability_id);

-- Validate row preservation and reference integrity before COMMIT; any failure aborts the transaction.
SELECT CASE WHEN
  (SELECT count(*) FROM mapping.phase3_standards)=(SELECT count(*) FROM m02a_standards) AND
  (SELECT count(*) FROM mapping.phase3_capabilities)=(SELECT count(*) FROM m02a_capabilities) AND
  (SELECT count(*) FROM mapping.phase3_source_references)=(SELECT count(*) FROM m02a_source_references) AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities)=(SELECT count(*) FROM m02a_requirement_capabilities) AND
  (SELECT count(*) FROM mapping.phase3_representability)=(SELECT count(*) FROM m02a_representability) AND
  (SELECT count(*) FROM mapping.phase3_automatability)=(SELECT count(*) FROM m02a_automatability) AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_standards EXCEPT ALL SELECT * FROM m02a_standards))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_standards EXCEPT ALL SELECT * FROM mapping.phase3_standards))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_capabilities EXCEPT ALL SELECT * FROM m02a_capabilities))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_capabilities EXCEPT ALL SELECT * FROM mapping.phase3_capabilities))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_source_references EXCEPT ALL SELECT * FROM m02a_source_references))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_source_references EXCEPT ALL SELECT * FROM mapping.phase3_source_references))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_capabilities EXCEPT ALL SELECT * FROM m02a_requirement_capabilities))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_requirement_capabilities EXCEPT ALL SELECT * FROM mapping.phase3_requirement_capabilities))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_representability EXCEPT ALL SELECT * FROM m02a_representability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_representability EXCEPT ALL SELECT * FROM mapping.phase3_representability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_observed_evidence EXCEPT ALL SELECT * FROM m02a_observed_evidence))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_observed_evidence EXCEPT ALL SELECT * FROM mapping.phase3_observed_evidence))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_automatability EXCEPT ALL SELECT * FROM m02a_automatability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m02a_automatability EXCEPT ALL SELECT * FROM mapping.phase3_automatability))=0 AND
  (SELECT count(*) FROM mapping.phase3_capabilities c LEFT JOIN mapping.phase3_standards s USING (standard_id) WHERE s.standard_id IS NULL)=0 AND
  (SELECT count(*) FROM mapping.phase3_source_references s LEFT JOIN mapping.phase3_capabilities c USING (capability_id) WHERE c.capability_id IS NULL)=0
  THEN 'M02A_COPY_VALIDATION_PASS' ELSE error('M02A copy/reference validation failed') END;

COMMIT;
