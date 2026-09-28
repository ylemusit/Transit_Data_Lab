-- M06-B02C schema only. Adds scoped-evaluation structure; inserts no scope data.
-- Authorized: SCHEMA_MIGRATION. All B02 data persistence remains unauthorized.
BEGIN TRANSACTION;

SELECT CASE WHEN
  (SELECT count(*) FROM compliance.requirements)=48 AND
  (SELECT count(*) FROM source.provisions)=92 AND
  (SELECT count(*) FROM compliance.source_facts)=36 AND
  (SELECT count(*) FROM compliance.deadlines)=10 AND
  (SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE concept_id LIKE 'M06-B02-CPT-A05-%')=7 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))=0 AND
  (SELECT count(*) FROM mapping.phase3_concept_mappings)=0 AND
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))=0 AND
  (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
  (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
  (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
  (SELECT count(*) FROM audit.rules)=0 AND
  NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='mapping' AND table_name IN ('phase3_mapping_scope_units','phase3_scope_source_references')) AND
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='MAPPING_SCOPE_DISPOSITION')=0 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id IN (
    'M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT',
    'M04-MAP-A08P03-GTFS-ATTRIBUTION','M04-MAP-A08P03-GTFS-PUBLISHER','M06-B01-MAP-A03-P03-001-NAP-DISCOVERY'))=6
THEN 'M06B02C_PRECHECK_PASS' ELSE error('M06-B02C precheck failed; migration aborted') END;

CREATE TEMP TABLE m06b02c_mappings_before AS
 SELECT mapping_id,requirement_id,capability_id,mapping_type,mapping_conditions,limitations,review_status,fixture_kind
 FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST';
CREATE TEMP TABLE m06b02c_concepts_before AS SELECT * FROM mapping.phase3_requirement_concepts;
CREATE TEMP TABLE m06b02c_bridges_before AS SELECT * FROM mapping.phase3_concept_mappings;
CREATE TEMP TABLE m06b02c_coverage_before AS SELECT * FROM mapping.phase3_requirement_coverage;
CREATE TEMP TABLE m06b02c_reviews_before AS SELECT * FROM mapping.phase3_mapping_reviews;
CREATE TEMP TABLE m06b02c_sources_before AS SELECT * FROM mapping.phase3_source_references;
CREATE TEMP TABLE m06b02c_representability_before AS SELECT * FROM mapping.phase3_representability;
CREATE TEMP TABLE m06b02c_observed_before AS SELECT * FROM mapping.phase3_observed_evidence;
CREATE TEMP TABLE m06b02c_automatability_before AS SELECT * FROM mapping.phase3_automatability;
CREATE TEMP TABLE m06b02c_audit_before AS SELECT * FROM audit.rules;

CREATE TABLE mapping.phase3_mapping_scope_units (
  scope_unit_id VARCHAR PRIMARY KEY,
  concept_id VARCHAR NOT NULL,
  mapping_id VARCHAR NOT NULL,
  unit_code VARCHAR NOT NULL,
  unit_name VARCHAR NOT NULL,
  unit_definition VARCHAR NOT NULL,
  scope_disposition VARCHAR NOT NULL CHECK (scope_disposition IN ('INCLUDED','UNRESOLVED','EXCLUDED')),
  basis_section VARCHAR,
  limitation VARCHAR,
  rationale VARCHAR,
  review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
  reviewed_at DATE,
  reviewed_by VARCHAR,
  decision_document_id VARCHAR,
  milestone_id VARCHAR,
  UNIQUE(concept_id,mapping_id,unit_code),
  FOREIGN KEY (concept_id,mapping_id) REFERENCES mapping.phase3_concept_mappings(concept_id,mapping_id),
  CHECK (length(trim(scope_unit_id))>0 AND length(trim(unit_code))>0 AND
         length(trim(unit_name))>0 AND length(trim(unit_definition))>0),
  CHECK (scope_disposition NOT IN ('UNRESOLVED','EXCLUDED') OR length(trim(coalesce(rationale,'')))>0),
  CHECK (scope_disposition <> 'INCLUDED' OR
         (review_status='APPROVED' AND reviewed_at IS NOT NULL AND length(trim(coalesce(reviewed_by,'')))>0))
);

CREATE TABLE mapping.phase3_scope_source_references (
  scope_unit_id VARCHAR NOT NULL REFERENCES mapping.phase3_mapping_scope_units(scope_unit_id),
  source_reference_id VARCHAR NOT NULL REFERENCES mapping.phase3_source_references(source_reference_id),
  evidence_role VARCHAR NOT NULL CHECK (evidence_role IN ('SUPPORT','BOUNDARY','COUNTEREXAMPLE')),
  PRIMARY KEY(scope_unit_id,source_reference_id,evidence_role)
);

INSERT INTO mapping.phase3_vocabularies(vocabulary,value,description) VALUES
 ('MAPPING_SCOPE_DISPOSITION','INCLUDED','Unit demonstrated by reviewed mapping evidence within the stated scope.'),
 ('MAPPING_SCOPE_DISPOSITION','UNRESOLVED','Unit relevant to the concept but not demonstrated yet.'),
 ('MAPPING_SCOPE_DISPOSITION','EXCLUDED','Unit explicitly determined not to belong to this mapping.')
;

CREATE INDEX idx_phase3_scope_units_mapping ON mapping.phase3_mapping_scope_units(mapping_id);
CREATE INDEX idx_phase3_scope_units_concept ON mapping.phase3_mapping_scope_units(concept_id);
CREATE INDEX idx_phase3_scope_source_reference ON mapping.phase3_scope_source_references(source_reference_id);

SELECT CASE WHEN
  (SELECT count(*) FROM mapping.phase3_mapping_scope_units)=0 AND
  (SELECT count(*) FROM mapping.phase3_scope_source_references)=0 AND
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='MAPPING_SCOPE_DISPOSITION')=3 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' EXCEPT ALL SELECT * FROM m06b02c_mappings_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_mappings_before EXCEPT ALL SELECT * FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_concepts EXCEPT ALL SELECT * FROM m06b02c_concepts_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_concepts_before EXCEPT ALL SELECT * FROM mapping.phase3_requirement_concepts))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_concept_mappings EXCEPT ALL SELECT * FROM m06b02c_bridges_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_bridges_before EXCEPT ALL SELECT * FROM mapping.phase3_concept_mappings))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_requirement_coverage EXCEPT ALL SELECT * FROM m06b02c_coverage_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_coverage_before EXCEPT ALL SELECT * FROM mapping.phase3_requirement_coverage))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_mapping_reviews EXCEPT ALL SELECT * FROM m06b02c_reviews_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_reviews_before EXCEPT ALL SELECT * FROM mapping.phase3_mapping_reviews))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_source_references EXCEPT ALL SELECT * FROM m06b02c_sources_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_sources_before EXCEPT ALL SELECT * FROM mapping.phase3_source_references))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_representability EXCEPT ALL SELECT * FROM m06b02c_representability_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_representability_before EXCEPT ALL SELECT * FROM mapping.phase3_representability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_observed_evidence EXCEPT ALL SELECT * FROM m06b02c_observed_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_observed_before EXCEPT ALL SELECT * FROM mapping.phase3_observed_evidence))=0 AND
  (SELECT count(*) FROM (SELECT * FROM mapping.phase3_automatability EXCEPT ALL SELECT * FROM m06b02c_automatability_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_automatability_before EXCEPT ALL SELECT * FROM mapping.phase3_automatability))=0 AND
  (SELECT count(*) FROM (SELECT * FROM audit.rules EXCEPT ALL SELECT * FROM m06b02c_audit_before))=0 AND
  (SELECT count(*) FROM (SELECT * FROM m06b02c_audit_before EXCEPT ALL SELECT * FROM audit.rules))=0 AND
  (SELECT count(*) FROM compliance.requirements)=48 AND (SELECT count(*) FROM source.provisions)=92 AND
  (SELECT count(*) FROM compliance.source_facts)=36 AND (SELECT count(*) FROM compliance.deadlines)=10
THEN 'M06B02C_POSTCHECK_PASS' ELSE error('M06-B02C postcheck failed; transaction rolled back') END;

COMMIT;
