-- M06-B01-HR: persist the human semantic decisions after candidate generation.
-- Additive and idempotent. This records reviewed evaluation coverage, not legal compliance.
BEGIN TRANSACTION;

SELECT CASE WHEN
  (SELECT count(*) FROM compliance.requirements)=48 AND
  (SELECT count(*) FROM mapping.phase3_standards)=3 AND
  (SELECT count(*) FROM mapping.phase3_capabilities) IN (5,6) AND
  (SELECT count(*) FROM mapping.phase3_source_references) IN (7,8) AND
  (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND exception_id LIKE 'M06-B01-%')=3 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id LIKE 'M06-B01-%') IN (0,1)
THEN 'M06B01_HR_PREFLIGHT_PASS' ELSE error('M06-B01-HR preflight state mismatch') END;

SELECT CASE WHEN
  (SELECT is_nullable FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND column_name='standard_id')='YES' AND
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='SOURCE_KIND' AND value='OFFICIAL_LEGAL_SOURCE')=1 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND requirement_id IN ('EU-2017-1926-REQ-A03-P01-001','EU-2017-1926-REQ-A03-P01-002','EU-2017-1926-REQ-A03-P03-001')) IN (0,1)
THEN 'M06B01_HR_MODEL_PASS' ELSE error('M06-B01-HR model or mapping precondition failed') END;

SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM mapping.phase3_capabilities
  WHERE capability_id='NAP_DATA_DISCOVERY' AND
    (standard_id IS DISTINCT FROM NULL OR domain IS DISTINCT FROM 'digital access point' OR entity IS DISTINCT FROM 'dataset' OR
     field_or_element IS DISTINCT FROM 'corresponding metadata' OR review_status IS DISTINCT FROM 'REVIEWED')
) THEN TRUE ELSE error('Incompatible NAP_DATA_DISCOVERY capability already exists') END;

INSERT INTO mapping.phase3_capabilities
 (capability_id,standard_id,domain,entity,field_or_element,semantic_meaning,evidence_type,limitations,review_status)
VALUES
 ('NAP_DATA_DISCOVERY',NULL,'digital access point','dataset','corresponding metadata',
  'A functional capability of a digital access point that allows users to search for requested datasets using corresponding metadata and to display or expose that metadata.',
  'Technical observation of metadata-based dataset discovery behavior',
  'Does not prove legal establishment of a NAP; designation as the single point of access; presence of all legally required datasets; metadata completeness; machine-readable access unless separately evidenced; transport-format conformance; data quality; or legal compliance. Means metadata-based data discovery, not geographic localization, GPS or vehicle positioning, stop coordinates, or geocoding. No particular REST API, search engine, or implementation technology is prescribed by this capability.',
  'REVIEWED')
ON CONFLICT (capability_id) DO NOTHING;

-- The consolidated Regulation source is already captured in compliance.source_facts;
-- add one mapping source reference because none of the seven mapping references is legal.
SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM mapping.phase3_source_references
  WHERE source_reference_id='M06-B01-SRC-REG-2017-1926' AND
    (capability_id IS DISTINCT FROM 'NAP_DATA_DISCOVERY' OR source_kind IS DISTINCT FROM 'OFFICIAL_LEGAL_SOURCE' OR
     url_or_document_id IS DISTINCT FROM 'https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:02017R1926-20240304')
) THEN TRUE ELSE error('Incompatible M06-B01 official legal source reference exists') END;

INSERT INTO mapping.phase3_source_references
 (source_reference_id,capability_id,source_kind,specification_name,version,section,url_or_document_id,retrieved_on,reviewed_on,notes)
VALUES
 ('M06-B01-SRC-REG-2017-1926','NAP_DATA_DISCOVERY','OFFICIAL_LEGAL_SOURCE',
  'Regulation (EU) 2017/1926, consolidated text','Consolidated version 2024-03-04','Article 3(3)',
  'https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:02017R1926-20240304',NULL,DATE '2026-09-27',
  'Supports the functional discovery concept for this capability; not observed implementation evidence and not a legal-compliance conclusion.')
ON CONFLICT (source_reference_id) DO NOTHING;

SELECT CASE WHEN NOT EXISTS (
 SELECT 1 FROM mapping.phase3_requirement_capabilities
 WHERE mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY' AND
  (requirement_id IS DISTINCT FROM 'EU-2017-1926-REQ-A03-P03-001' OR capability_id IS DISTINCT FROM 'NAP_DATA_DISCOVERY' OR
   mapping_type IS DISTINCT FROM 'PARTIAL' OR review_status IS DISTINCT FROM 'REVIEWED' OR fixture_kind IS NOT NULL)
) THEN TRUE ELSE error('Incompatible B01 capability mapping exists') END;

INSERT INTO mapping.phase3_requirement_capabilities
 (mapping_id,requirement_id,capability_id,mapping_type,mapping_conditions,limitations,review_status)
VALUES
 ('M06-B01-MAP-A03-P03-001-NAP-DISCOVERY','EU-2017-1926-REQ-A03-P03-001','NAP_DATA_DISCOVERY','PARTIAL',
  'Technical observation is limited to searching requested datasets using corresponding metadata and displaying or exposing that metadata.',
  'Does not establish the complete requirement, legal establishment or single-point designation of a NAP, required dataset presence, metadata completeness, machine-readable access, format conformance, data quality, or legal compliance. Contextual and external evidence remains necessary; no particular API or technology is implied.',
  'REVIEWED')
ON CONFLICT (mapping_id) DO NOTHING;

SELECT CASE WHEN NOT EXISTS (
 SELECT 1 FROM mapping.phase3_mapping_reviews
 WHERE mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY' AND
  (semantic_review_outcome IS DISTINCT FROM 'ACCEPTED_WITH_LIMITATIONS' OR reviewed_by IS DISTINCT FROM 'Yeison Arbey Carrillo Lemus')
) THEN TRUE ELSE error('Incompatible B01 semantic mapping review exists') END;

INSERT INTO mapping.phase3_mapping_reviews
 (mapping_id,semantic_review_outcome,justification,limitations,reviewed_by,reviewed_at)
VALUES
 ('M06-B01-MAP-A03-P03-001-NAP-DISCOVERY','ACCEPTED_WITH_LIMITATIONS',
  'The approved functional mapping is metadata-based dataset discovery: users can search for requested datasets using corresponding metadata and the access point displays or exposes that metadata.',
  'Only discovery behavior is technically observable. Complete evaluation requires contextual and external evidence. This does not prove NAP establishment or designation, complete required datasets or metadata, machine-readable access, transport-format conformance, data quality, or legal compliance.',
  'Yeison Arbey Carrillo Lemus',DATE '2026-09-27')
ON CONFLICT (mapping_id) DO NOTHING;

INSERT INTO mapping.phase3_automatability
 (automatability_id,mapping_id,automatability_state,explanation,prerequisites,assessed_on,review_status)
VALUES
 ('M06-B01-AUTO-A03-P03-001-NAP-DISCOVERY','M06-B01-MAP-A03-P03-001-NAP-DISCOVERY','PARTIAL',
  'Some metadata-based dataset discovery behavior can potentially be observed and tested technically; complete evaluation requires contextual and external evidence.',
  'Access to the relevant access point and authoritative contextual evidence; technical observation alone is insufficient.',DATE '2026-09-27','REVIEWED')
ON CONFLICT (automatability_id) DO NOTHING;

-- Persist exactly the three human-reviewed coverage decisions. Existing M04 coverage is untouched.
INSERT INTO mapping.phase3_requirement_coverage
 (coverage_id,requirement_id,coverage_state,semantic_review_outcome,justification,limitations,identified_paths,review_status,reviewed_by,reviewed_at,reviewed_against_baseline)
VALUES
 ('M06-B01-COV-A03-P01-001','EU-2017-1926-REQ-A03-P01-001','PARTIAL','ACCEPTED_WITH_LIMITATIONS',
  'An institutional/legal-process evaluation path is identifiable, but no justified reusable technical capability mapping exists.',
  'Assessment requires authoritative external evidence establishing the relevant National Access Point. Technical accessibility or dataset-format evidence alone does not prove this obligation. No legal-compliance conclusion is made.',
  'EXCEPTION:M06-B01-EXC-A03-P01-001', 'REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M06_B01_HUMAN_SEMANTIC_REVIEW_2026-09-27'),
 ('M06-B01-COV-A03-P01-002','EU-2017-1926-REQ-A03-P01-002','PARTIAL','ACCEPTED_WITH_LIMITATIONS',
  'An organizational/institutional evaluation path concerning the access point role as the single point of access is identifiable; no justified reusable technical capability mapping exists.',
  'Assessment requires authoritative organizational/designation evidence. Dataset presence or technical accessibility alone does not prove single-access-point status. No legal-compliance conclusion is made.',
  'EXCEPTION:M06-B01-EXC-A03-P01-002', 'REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M06_B01_HUMAN_SEMANTIC_REVIEW_2026-09-27'),
 ('M06-B01-COV-A03-P03-001','EU-2017-1926-REQ-A03-P03-001','PARTIAL','ACCEPTED_WITH_LIMITATIONS',
  'A reviewed functional mapping for metadata-based dataset discovery coexists with the manual/external evaluation path.',
  'Technical observation covers only some discovery behavior. Contextual and external evidence remains necessary for complete evaluation; this is not a legal-compliance conclusion.',
  'MAPPING:M06-B01-MAP-A03-P03-001-NAP-DISCOVERY;EXCEPTION:M06-B01-EXC-A03-P03-001', 'REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M06_B01_HUMAN_SEMANTIC_REVIEW_2026-09-27')
ON CONFLICT (coverage_id) DO NOTHING;

SELECT CASE WHEN
  (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY' AND standard_id IS NULL)=1 AND
  (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY')=1 AND
  (SELECT count(*) FROM mapping.phase3_capabilities WHERE standard_id IS NULL)=1 AND
  (SELECT count(*) FROM mapping.phase3_standards WHERE standard_id='NAP_DATA_DISCOVERY')=0 AND
  (SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id='M06-B01-SRC-REG-2017-1926' AND source_kind='OFFICIAL_LEGAL_SOURCE')=1 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id LIKE 'M06-B01-%')=1 AND
  (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND requirement_id IN ('EU-2017-1926-REQ-A03-P01-001','EU-2017-1926-REQ-A03-P01-002'))=0 AND
  (SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY' AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS')=1 AND
  (SELECT count(*) FROM mapping.phase3_automatability WHERE automatability_id='M06-B01-AUTO-A03-P03-001-NAP-DISCOVERY' AND automatability_state='PARTIAL')=1 AND
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE coverage_id LIKE 'M06-B01-COV-%' AND coverage_state='PARTIAL' AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS')=3
THEN 'M06B01_HR_STATE_PASS' ELSE error('M06-B01-HR persisted state mismatch') END;

COMMIT;
