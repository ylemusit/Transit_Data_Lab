-- M06-B01-MM: allow reusable capabilities without an asserted standard binding.
-- Rebuild the bounded FK subgraph atomically because DuckDB cannot alter a
-- referenced parent table in place. Existing substantive rows are preserved.
BEGIN TRANSACTION;

SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM information_schema.columns
  WHERE table_schema='mapping' AND table_name='phase3_capabilities'
    AND column_name='standard_id' AND is_nullable='YES'
) THEN 'M06B01_PRECONDITION_PASS'
ELSE error('M06-B01 migration already applied') END;

CREATE TEMP TABLE m06b01_standards AS SELECT * FROM mapping.phase3_standards;
CREATE TEMP TABLE m06b01_capabilities AS SELECT * FROM mapping.phase3_capabilities;
CREATE TEMP TABLE m06b01_source_references AS SELECT * FROM mapping.phase3_source_references;
CREATE TEMP TABLE m06b01_requirement_capabilities AS SELECT * FROM mapping.phase3_requirement_capabilities;
CREATE TEMP TABLE m06b01_representability AS SELECT * FROM mapping.phase3_representability;
CREATE TEMP TABLE m06b01_observed_evidence AS SELECT * FROM mapping.phase3_observed_evidence;
CREATE TEMP TABLE m06b01_automatability AS SELECT * FROM mapping.phase3_automatability;
CREATE TEMP TABLE m06b01_mapping_reviews AS SELECT * FROM mapping.phase3_mapping_reviews;

SELECT CASE WHEN
 (SELECT count(*) FROM m06b01_standards)=3 AND
 (SELECT count(*) FROM m06b01_capabilities)=5 AND
 (SELECT count(*) FROM m06b01_source_references)=7 AND
 (SELECT count(*) FROM m06b01_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=5 AND
 (SELECT count(*) FROM m06b01_mapping_reviews)=5 AND
 (SELECT count(*) FROM mapping.phase3_requirement_coverage)=5 AND
 (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
 (SELECT count(*) FROM m06b01_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
 (SELECT count(*) FROM m06b01_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
 (SELECT count(*) FROM m06b01_capabilities WHERE standard_id IS NULL)=0 AND
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id LIKE 'M06-B01-%')=0
 THEN 'M06B01_COUNTS_AND_SCOPE_PASS' ELSE error('M06-B01 preflight counts or scope mismatch') END;

-- Ensure the source-kind controlled vocabulary is either absent or consistent.
SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM mapping.phase3_vocabularies
  WHERE vocabulary='SOURCE_KIND' AND value='OFFICIAL_LEGAL_SOURCE'
) THEN 'M06B01_VOCABULARY_READY'
ELSE error('M06-B01 source kind vocabulary already exists before migration') END;

DROP TABLE mapping.phase3_mapping_reviews;
DROP TABLE mapping.phase3_observed_evidence;
DROP TABLE mapping.phase3_automatability;
DROP TABLE mapping.phase3_requirement_capabilities;
DROP TABLE mapping.phase3_representability;
DROP TABLE mapping.phase3_source_references;
DROP TABLE mapping.phase3_capabilities;

CREATE TABLE mapping.phase3_capabilities (
 capability_id VARCHAR PRIMARY KEY,
 standard_id VARCHAR REFERENCES mapping.phase3_standards(standard_id),
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
 source_kind VARCHAR NOT NULL CHECK (source_kind IN ('OFFICIAL_SPECIFICATION','OFFICIAL_PROFILE','OFFICIAL_LEGAL_SOURCE','OTHER')),
 specification_name VARCHAR, version VARCHAR, section VARCHAR,
 url_or_document_id VARCHAR NOT NULL, retrieved_on DATE, reviewed_on DATE, notes VARCHAR,
 fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST')
);
CREATE TABLE mapping.phase3_requirement_capabilities (
 mapping_id VARCHAR PRIMARY KEY, requirement_id VARCHAR NOT NULL,
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
CREATE TABLE mapping.phase3_mapping_reviews (
 mapping_id VARCHAR PRIMARY KEY REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
 semantic_review_outcome VARCHAR NOT NULL CHECK (semantic_review_outcome IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS','REJECTED','UNRESOLVED')),
 justification VARCHAR NOT NULL, limitations VARCHAR, reviewed_by VARCHAR NOT NULL, reviewed_at DATE NOT NULL,
 CHECK (semantic_review_outcome <> 'ACCEPTED_WITH_LIMITATIONS' OR length(trim(coalesce(limitations,''))) > 0)
);

INSERT INTO mapping.phase3_capabilities SELECT * FROM m06b01_capabilities;
INSERT INTO mapping.phase3_source_references SELECT * FROM m06b01_source_references;
INSERT INTO mapping.phase3_requirement_capabilities SELECT * FROM m06b01_requirement_capabilities;
INSERT INTO mapping.phase3_representability SELECT * FROM m06b01_representability;
INSERT INTO mapping.phase3_observed_evidence SELECT * FROM m06b01_observed_evidence;
INSERT INTO mapping.phase3_automatability SELECT * FROM m06b01_automatability;
INSERT INTO mapping.phase3_mapping_reviews SELECT * FROM m06b01_mapping_reviews;

CREATE INDEX idx_phase3_mapping_requirement ON mapping.phase3_requirement_capabilities(requirement_id);
CREATE INDEX idx_phase3_mapping_capability ON mapping.phase3_requirement_capabilities(capability_id);

INSERT INTO mapping.phase3_vocabularies(vocabulary,value,description) VALUES
 ('SOURCE_KIND','OFFICIAL_LEGAL_SOURCE','Authoritative legislative or regulatory source; classification does not assert legal compliance.')
ON CONFLICT DO NOTHING;

SELECT CASE WHEN
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_capabilities EXCEPT ALL SELECT * FROM m06b01_capabilities))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_capabilities EXCEPT ALL SELECT * FROM mapping.phase3_capabilities))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_source_references EXCEPT ALL SELECT * FROM m06b01_source_references))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_source_references EXCEPT ALL SELECT * FROM mapping.phase3_source_references))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_capabilities EXCEPT ALL SELECT * FROM m06b01_requirement_capabilities))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_requirement_capabilities EXCEPT ALL SELECT * FROM mapping.phase3_requirement_capabilities))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_representability EXCEPT ALL SELECT * FROM m06b01_representability))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_representability EXCEPT ALL SELECT * FROM mapping.phase3_representability))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_observed_evidence EXCEPT ALL SELECT * FROM m06b01_observed_evidence))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_observed_evidence EXCEPT ALL SELECT * FROM mapping.phase3_observed_evidence))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_automatability EXCEPT ALL SELECT * FROM m06b01_automatability))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_automatability EXCEPT ALL SELECT * FROM mapping.phase3_automatability))=0 AND
 (SELECT count(*) FROM (SELECT * FROM mapping.phase3_mapping_reviews EXCEPT ALL SELECT * FROM m06b01_mapping_reviews))=0 AND
 (SELECT count(*) FROM (SELECT * FROM m06b01_mapping_reviews EXCEPT ALL SELECT * FROM mapping.phase3_mapping_reviews))=0 AND
 (SELECT count(*) FROM mapping.phase3_capabilities WHERE standard_id IS NULL)=0 AND
 (SELECT count(*) FROM mapping.phase3_capabilities c JOIN mapping.phase3_standards s USING(standard_id) WHERE c.standard_id IS NULL)=0 AND
 (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='SOURCE_KIND' AND value='OFFICIAL_LEGAL_SOURCE')=1 AND
 (SELECT count(*) FROM mapping.phase3_source_references WHERE source_kind='OFFICIAL_LEGAL_SOURCE')=0 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND constraint_type='FOREIGN KEY')=1 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_source_references' AND constraint_type='FOREIGN KEY')=1 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_requirement_capabilities' AND constraint_type='FOREIGN KEY')=1 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_representability' AND constraint_type='FOREIGN KEY')=1 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_observed_evidence' AND constraint_type='FOREIGN KEY')=2 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_automatability' AND constraint_type='FOREIGN KEY')=1 AND
 (SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_mapping_reviews' AND constraint_type='FOREIGN KEY')=1
 THEN 'M06B01_ROW_AND_CONSTRAINT_PRESERVATION_PASS'
 ELSE error('M06-B01 row, binding, or vocabulary validation failed') END;

COMMIT;
