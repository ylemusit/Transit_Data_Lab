-- M06-B02 schema migration. Schema only; no concepts or B02 data are seeded.
-- Human decision: REQUIREMENT_CONCEPT_DESIGN=APPROVED;
-- SCHEMA_MIGRATION=AUTHORIZED; B02_DATA_PERSISTENCE=NOT_AUTHORIZED.
BEGIN TRANSACTION;

SELECT CASE WHEN
  (SELECT count(*) FROM compliance.requirements)=48 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
  (SELECT count(*) FROM mapping.phase3_mapping_reviews)=6 AND
  (SELECT count(*) FROM mapping.phase3_requirement_coverage)=8 AND
  (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
  (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
  (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
  (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
  (SELECT count(*) FROM audit.rules)=0 AND
  NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='mapping' AND table_name IN ('phase3_requirement_concepts','phase3_concept_mappings'))
THEN 'M06B02_PRECHECK_PASS' ELSE error('M06-B02 protected precheck failed; migration aborted') END;

CREATE TEMP TABLE m06b02_mappings_before AS
  SELECT mapping_id, requirement_id, capability_id, mapping_type, mapping_conditions,
         limitations, review_status, fixture_kind
  FROM mapping.phase3_requirement_capabilities;
CREATE TEMP TABLE m06b02_mapping_reviews_before AS SELECT * FROM mapping.phase3_mapping_reviews;
CREATE TEMP TABLE m06b02_coverage_before AS SELECT * FROM mapping.phase3_requirement_coverage;
CREATE TEMP TABLE m06b02_exceptions_before AS SELECT * FROM mapping.phase3_exceptions;
CREATE TEMP TABLE m06b02_source_refs_before AS SELECT * FROM mapping.phase3_source_references;
CREATE TEMP TABLE m06b02_automation_before AS SELECT * FROM mapping.phase3_automatability;
CREATE TEMP TABLE m06b02_representability_before AS SELECT * FROM mapping.phase3_representability;
CREATE TEMP TABLE m06b02_evidence_before AS SELECT * FROM mapping.phase3_observed_evidence;

SELECT CASE WHEN
  (SELECT count(*) FROM m06b02_mappings_before)=6 AND
  (SELECT count(*) FROM m06b02_mapping_reviews_before)=6 AND
  (SELECT count(*) FROM m06b02_coverage_before)=8 AND
  (SELECT count(*) FROM m06b02_exceptions_before WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6
THEN 'M06B02_SNAPSHOT_PASS' ELSE error('M06-B02 exact snapshot mismatch; migration aborted') END;

CREATE TABLE mapping.phase3_requirement_concepts (
  concept_id VARCHAR PRIMARY KEY,
  requirement_id VARCHAR NOT NULL,
  concept_code VARCHAR NOT NULL,
  concept_name VARCHAR NOT NULL,
  concept_description VARCHAR NOT NULL,
  scope_status VARCHAR NOT NULL CHECK (scope_status IN ('IN_SCOPE','PARTIAL','UNRESOLVED','OUT_OF_SCOPE')),
  applicability_conditions VARCHAR,
  source_basis VARCHAR NOT NULL,
  review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
  review_outcome VARCHAR CHECK (review_outcome IS NULL OR review_outcome IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS','REJECTED','UNRESOLVED')),
  review_justification VARCHAR,
  limitations VARCHAR,
  created_at TIMESTAMP,
  created_by VARCHAR,
  reviewed_at DATE,
  reviewed_by VARCHAR,
  notes VARCHAR,
  UNIQUE(requirement_id, concept_code),
  CHECK (length(trim(concept_id))>0 AND length(trim(requirement_id))>0 AND
         length(trim(concept_code))>0 AND length(trim(concept_name))>0 AND
         length(trim(concept_description))>0 AND length(trim(source_basis))>0),
  CHECK ((review_status IN ('UNREVIEWED','NEEDS_REVIEW') AND reviewed_at IS NULL AND reviewed_by IS NULL)
      OR (review_status IN ('REVIEWED','APPROVED','REJECTED') AND reviewed_at IS NOT NULL AND
          length(trim(coalesce(reviewed_by,'')))>0 AND length(trim(coalesce(review_justification,'')))>0)),
  CHECK (review_outcome IS DISTINCT FROM 'ACCEPTED_WITH_LIMITATIONS' OR length(trim(coalesce(limitations,'')))>0)
);

CREATE TABLE mapping.phase3_concept_mappings (
  concept_id VARCHAR NOT NULL REFERENCES mapping.phase3_requirement_concepts(concept_id),
  mapping_id VARCHAR NOT NULL REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
  relation_note VARCHAR NOT NULL CHECK (length(trim(relation_note))>0),
  PRIMARY KEY (concept_id, mapping_id)
);

INSERT INTO mapping.phase3_vocabularies(vocabulary,value,description) VALUES
 ('REQUIREMENT_CONCEPT_SCOPE','IN_SCOPE','Concept scope is explicitly included.'),
 ('REQUIREMENT_CONCEPT_SCOPE','PARTIAL','Concept is only partially resolved or scoped.'),
 ('REQUIREMENT_CONCEPT_SCOPE','UNRESOLVED','Concept candidate remains unresolved.'),
 ('REQUIREMENT_CONCEPT_SCOPE','OUT_OF_SCOPE','Concept is explicitly excluded from the requirement scope.')
;

CREATE INDEX idx_phase3_concepts_requirement ON mapping.phase3_requirement_concepts(requirement_id);
CREATE INDEX idx_phase3_concept_mappings_mapping ON mapping.phase3_concept_mappings(mapping_id);

SELECT CASE WHEN
  (SELECT count(*) FROM mapping.phase3_requirement_concepts)=0 AND
  (SELECT count(*) FROM mapping.phase3_concept_mappings)=0 AND
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='REQUIREMENT_CONCEPT_SCOPE')=4 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_capabilities EXCEPT ALL SELECT * FROM m06b02_mappings_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_mappings_before EXCEPT ALL SELECT * FROM mapping.phase3_requirement_capabilities))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_mapping_reviews EXCEPT ALL SELECT * FROM m06b02_mapping_reviews_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_mapping_reviews_before EXCEPT ALL SELECT * FROM mapping.phase3_mapping_reviews))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_coverage EXCEPT ALL SELECT * FROM m06b02_coverage_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_coverage_before EXCEPT ALL SELECT * FROM mapping.phase3_requirement_coverage))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_exceptions EXCEPT ALL SELECT * FROM m06b02_exceptions_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_exceptions_before EXCEPT ALL SELECT * FROM mapping.phase3_exceptions))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_source_references EXCEPT ALL SELECT * FROM m06b02_source_refs_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_source_refs_before EXCEPT ALL SELECT * FROM mapping.phase3_source_references))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_automatability EXCEPT ALL SELECT * FROM m06b02_automation_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_automation_before EXCEPT ALL SELECT * FROM mapping.phase3_automatability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_representability EXCEPT ALL SELECT * FROM m06b02_representability_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_representability_before EXCEPT ALL SELECT * FROM mapping.phase3_representability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_observed_evidence EXCEPT ALL SELECT * FROM m06b02_evidence_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02_evidence_before EXCEPT ALL SELECT * FROM mapping.phase3_observed_evidence))=0 AND
  (SELECT count(*) FROM compliance.requirements)=48 AND (SELECT count(*) FROM audit.rules)=0
THEN 'M06B02_POSTCHECK_PASS' ELSE error('M06-B02 postcheck failed; transaction rolled back') END;

COMMIT;
