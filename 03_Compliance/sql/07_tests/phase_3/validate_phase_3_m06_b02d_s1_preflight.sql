-- Read-only pre-persistence validator. PASS means expected current empty B02 target state and valid prerequisites.
WITH ids(mapping_id,requirement_id,concept_id,capability_id,source_id) AS (VALUES
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-A','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ROAD-CLOSURE','M06-B02D-SRC-DATEX-4-SN-A'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-B','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-LANE-CLOSURE','M06-B02D-SRC-DATEX-4-SN-B'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-C','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ROADWORKS','M06-B02D-SRC-DATEX-4-SN-C'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-D','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT','M06-B02D-SRC-DATEX-4-SN-D'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-A','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-BRIDGE-CLOSURE','M06-B02D-SRC-DATEX-5-SN-A'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-B','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ACCIDENT-INCIDENT','M06-B02D-SRC-DATEX-5-SN-B'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-C','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-POOR-ROAD-CONDITION','M06-B02D-SRC-DATEX-5-SN-C'),
 ('M06-B02-MAP-A05-P02-001-SIRI-ET','EU-2017-1926-REQ-A05-P02-001','M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','CAP-SIRI-EPIPRT-ET','M06-B02D-SRC-SIRI-EPIPRT-ET'),
 ('M06-B02-MAP-A05-P02-001-SIRI-SX','EU-2017-1926-REQ-A05-P02-001','M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','CAP-SIRI-EPIPRT-SX','M06-B02D-SRC-SIRI-EPIPRT-SX')
), checks AS (
 SELECT 'REQUIREMENTS' check_name, abs((SELECT count(*) FROM compliance.requirements)-48) failures
 UNION ALL SELECT 'CONCEPTS', abs((SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE concept_id LIKE 'M06-B02-CPT-A05-%')-7)
 UNION ALL SELECT 'LEGACY_MAPPINGS', abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
 UNION ALL SELECT 'TARGET_MAPPINGS_ABSENT',(SELECT count(*) FROM ids i JOIN mapping.phase3_requirement_capabilities m USING(mapping_id))
 UNION ALL SELECT 'TARGET_CAPABILITIES_ABSENT',(SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id IN (SELECT capability_id FROM ids))
 UNION ALL SELECT 'TARGET_SOURCES_ABSENT',(SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id IN (SELECT source_id FROM ids))
 UNION ALL SELECT 'TARGET_REVIEWS_ABSENT',(SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id IN (SELECT mapping_id FROM ids))
 UNION ALL SELECT 'TARGET_BRIDGES_ABSENT',(SELECT count(*) FROM mapping.phase3_concept_mappings WHERE mapping_id IN (SELECT mapping_id FROM ids))
 UNION ALL SELECT 'TARGET_SCOPE_ABSENT',(SELECT count(*) FROM mapping.phase3_mapping_scope_units WHERE mapping_id IN (SELECT mapping_id FROM ids))
 UNION ALL SELECT 'TARGET_SCOPE_LINKS_ABSENT',(SELECT count(*) FROM mapping.phase3_scope_source_references sr JOIN mapping.phase3_mapping_scope_units s USING(scope_unit_id) WHERE s.mapping_id IN (SELECT mapping_id FROM ids))
 UNION ALL SELECT 'REQUIREMENT_CONCEPT_ALIGNMENT',abs((SELECT count(*) FROM ids i JOIN mapping.phase3_requirement_concepts c USING(concept_id,requirement_id) JOIN compliance.requirements r USING(requirement_id))-9)
 UNION ALL SELECT 'DATEX_STANDARD_PRESENT',CASE WHEN EXISTS(SELECT 1 FROM mapping.phase3_standards WHERE standard_id='M03-DATEXII-MMTIS-RRP' AND standard_kind='DATEX_II') THEN 0 ELSE 1 END
 UNION ALL SELECT 'SIRI_STANDARD_ABSENT',(SELECT count(*) FROM mapping.phase3_standards WHERE standard_id='M06-B02D-SIRI-EPIPRT-2025')
 UNION ALL SELECT 'SEMANTIC_VOCABULARY',CASE WHEN EXISTS(SELECT 1 FROM mapping.phase3_vocabularies WHERE vocabulary='SEMANTIC_REVIEW_OUTCOME' AND value='ACCEPTED_WITH_LIMITATIONS') THEN 0 ELSE 1 END
 UNION ALL SELECT 'PROTECTED_LAYERS', (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 +(SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 +(SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 +(SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 +(SELECT count(*) FROM audit.rules)
), summary AS (SELECT count(*) checks,coalesce(sum(failures),0) failures FROM checks)
SELECT CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END status,checks,failures,
 (SELECT string_agg(check_name||'='||failures::VARCHAR,'; ' ORDER BY check_name) FROM checks WHERE failures>0) failing_checks FROM summary;
