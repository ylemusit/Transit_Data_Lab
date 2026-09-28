-- Read-only post-write M06-B02D-S1 validator. Must be run only after separately authorized transaction.
WITH ids(mapping_id,requirement_id,concept_id,capability_id) AS (VALUES
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-A','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ROAD-CLOSURE'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-B','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-LANE-CLOSURE'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-C','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ROADWORKS'),
 ('M06-B02-MAP-A05-P01-002-DATEX-4-SN-D','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-TEMP-TRAFFIC-MGMT'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-A','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-BRIDGE-CLOSURE'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-B','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-ACCIDENT-INCIDENT'),
 ('M06-B02-MAP-A05-P01-002-DATEX-5-SN-C','EU-2017-1926-REQ-A05-P01-002','M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','CAP-DATEXII-RRP-POOR-ROAD-CONDITION'),
 ('M06-B02-MAP-A05-P02-001-SIRI-ET','EU-2017-1926-REQ-A05-P02-001','M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','CAP-SIRI-EPIPRT-ET'),
 ('M06-B02-MAP-A05-P02-001-SIRI-SX','EU-2017-1926-REQ-A05-P02-001','M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','CAP-SIRI-EPIPRT-SX')),
checks AS (
 SELECT 'B02_CAPABILITIES' check_name,abs((SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id IN (SELECT capability_id FROM ids))-9) failures
 UNION ALL SELECT 'B02_MAPPINGS',abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE mapping_id IN (SELECT mapping_id FROM ids))-9)
 UNION ALL SELECT 'PARTIAL_ONLY',(SELECT count(*) FROM ids i JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_type<>'PARTIAL' OR m.review_status<>'NEEDS_REVIEW')
 UNION ALL SELECT 'REVIEWS',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id IN (SELECT mapping_id FROM ids))-9)
 UNION ALL SELECT 'REVIEW_OUTCOME',(SELECT count(*) FROM ids i JOIN mapping.phase3_mapping_reviews r USING(mapping_id) WHERE r.semantic_review_outcome<>'ACCEPTED_WITH_LIMITATIONS' OR coalesce(trim(r.limitations),'')='')
 UNION ALL SELECT 'BRIDGES',abs((SELECT count(*) FROM mapping.phase3_concept_mappings WHERE mapping_id IN (SELECT mapping_id FROM ids))-9)
 UNION ALL SELECT 'BRIDGE_REQUIREMENT_ALIGNMENT',(SELECT count(*) FROM ids i JOIN mapping.phase3_concept_mappings b ON b.mapping_id=i.mapping_id JOIN mapping.phase3_requirement_concepts c ON c.concept_id=b.concept_id JOIN mapping.phase3_requirement_capabilities m ON m.mapping_id=b.mapping_id WHERE c.requirement_id IS DISTINCT FROM m.requirement_id OR b.concept_id IS DISTINCT FROM i.concept_id)
 UNION ALL SELECT 'SCOPE_TOTAL',abs((SELECT count(*) FROM mapping.phase3_mapping_scope_units WHERE mapping_id IN (SELECT mapping_id FROM ids))-9)
 UNION ALL SELECT 'SCOPE_INCLUDED',(SELECT count(*) FROM mapping.phase3_mapping_scope_units WHERE mapping_id IN (SELECT mapping_id FROM ids) AND scope_disposition<>'INCLUDED')
 UNION ALL SELECT 'SCOPE_SOURCE_LINKS',abs((SELECT count(*) FROM mapping.phase3_scope_source_references sr JOIN mapping.phase3_mapping_scope_units s USING(scope_unit_id) WHERE s.mapping_id IN (SELECT mapping_id FROM ids))-9)
 UNION ALL SELECT 'SOURCE_REFERENCES',abs((SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id LIKE 'M06-B02D-SRC-%')-9)
 UNION ALL SELECT 'SOURCE_CAPABILITY_MATCH',(SELECT count(*) FROM mapping.phase3_scope_source_references sr JOIN mapping.phase3_mapping_scope_units s USING(scope_unit_id) JOIN mapping.phase3_source_references r USING(source_reference_id) JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.capability_id<>r.capability_id)
 UNION ALL SELECT 'FORBIDDEN_SUBSET',(SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id LIKE 'EU-2017-1926-REQ-A05-%' AND (mapping_id LIKE '%5-SN-D' OR mapping_id LIKE '%SIRI-CM%' OR mapping_id LIKE '%SIRI-VM%' OR mapping_id LIKE '%SIRI-FM%' OR requirement_id IN ('EU-2017-1926-REQ-A05-P01-001','EU-2017-1926-REQ-A05-P01-003','EU-2017-1926-REQ-A05-P02-002','EU-2017-1926-REQ-A05-P02-003')))
 UNION ALL SELECT 'B02_COVERAGE_UNCHANGED',(SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'B02_REPRESENTABILITY_UNCHANGED',(SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'B02_OBSERVED_UNCHANGED',(SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'B02_AUTOMATABILITY_UNCHANGED',(SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'AUDIT_UNCHANGED',(SELECT count(*) FROM audit.rules)
 UNION ALL SELECT 'LEGACY_MAPPINGS',abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id NOT IN (SELECT mapping_id FROM ids))-6)
 UNION ALL SELECT 'LEGACY_SCOPES',(SELECT count(*) FROM mapping.phase3_mapping_scope_units s JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_id NOT IN (SELECT mapping_id FROM ids))
 UNION ALL SELECT 'PHASES_1_2',abs((SELECT count(*) FROM compliance.requirements)-48)+abs((SELECT count(*) FROM compliance.source_facts)-36)+abs((SELECT count(*) FROM compliance.deadlines)-10)+abs((SELECT count(*) FROM source.provisions)-92)
), summary AS (SELECT count(*) checks,coalesce(sum(failures),0) failures FROM checks)
SELECT CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END status,checks,failures,
 (SELECT string_agg(check_name||'='||failures::VARCHAR,'; ' ORDER BY check_name) FROM checks WHERE failures>0) failing_checks FROM summary;
