WITH expected(requirement_id, concept_code, scope_status, review_outcome) AS (
 VALUES
 ('EU-2017-1926-REQ-A05-P01-002','ROAD_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
 ('EU-2017-1926-REQ-A05-P02-001','ROAD_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
 ('EU-2017-1926-REQ-A05-P02-001','PASSENGER_RT_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
 ('EU-2017-1926-REQ-A05-P02-001','FACILITY_ACCESS_NODE_STATUS','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
 ('EU-2017-1926-REQ-A05-P02-001','PARKING_TARIFF','PARTIAL',NULL),
 ('EU-2017-1926-REQ-A05-P02-001','SHARED_VEHICLE_AVAILABILITY','UNRESOLVED','UNRESOLVED'),
 ('EU-2017-1926-REQ-A05-P02-001','PARKING_AVAILABILITY','PARTIAL',NULL)
), checks AS (
 SELECT 'COUNT_7' check_name, abs((SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE concept_id LIKE 'M06-B02-CPT-A05-%')-7) bad
 UNION ALL SELECT 'EXPECTED_SET', (SELECT count(*) FROM expected e LEFT JOIN mapping.phase3_requirement_concepts c USING(requirement_id,concept_code) WHERE c.concept_id IS NULL OR c.scope_status IS DISTINCT FROM e.scope_status OR c.review_outcome IS DISTINCT FROM e.review_outcome)
 UNION ALL SELECT 'REQUIREMENTS', (SELECT count(*) FROM mapping.phase3_requirement_concepts c LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL)
 UNION ALL SELECT 'DUP_ID', (SELECT count(*) FROM (SELECT concept_id FROM mapping.phase3_requirement_concepts GROUP BY 1 HAVING count(*)>1))
 UNION ALL SELECT 'DUP_REQ_CODE', (SELECT count(*) FROM (SELECT requirement_id,concept_code FROM mapping.phase3_requirement_concepts GROUP BY 1,2 HAVING count(*)>1))
 UNION ALL SELECT 'SCOPE_VOCAB', (SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE scope_status NOT IN (SELECT value FROM mapping.phase3_vocabularies WHERE vocabulary='REQUIREMENT_CONCEPT_SCOPE'))
 UNION ALL SELECT 'REJECTED_TRAVEL_CONCEPTS', (SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001') AND (lower(concept_code || ' ' || concept_name || ' ' || concept_description) LIKE '%travel time%' OR lower(concept_code || ' ' || concept_name || ' ' || concept_description) LIKE '%predicted%'))
 UNION ALL SELECT 'B02_BRIDGES', (SELECT count(*) FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id LIKE 'M06-B02-CPT-A05-%')
 UNION ALL SELECT 'B02_MAPPINGS', (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'LEGACY_ASSOCIATIONS', (SELECT count(*) FROM mapping.phase3_concept_mappings WHERE mapping_id IN ('M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT','M04-MAP-A08P03-GTFS-ATTRIBUTION','M04-MAP-A08P03-GTFS-PUBLISHER','M06-B01-MAP-A03-P03-001-NAP-DISCOVERY'))
 UNION ALL SELECT 'PROTECTED_COUNTERS', abs((SELECT count(*) FROM source.provisions)-92)+abs((SELECT count(*) FROM compliance.source_facts)-36)+abs((SELECT count(*) FROM compliance.requirements)-48)+abs((SELECT count(*) FROM compliance.deadlines)-10)+abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)+abs((SELECT count(*) FROM mapping.phase3_requirement_coverage)-8)+abs((SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)+abs((SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'))+abs((SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'))+(SELECT count(*) FROM audit.rules)
)
SELECT CASE WHEN coalesce(sum(bad),0)=0 THEN 'PASS' ELSE 'FAIL' END status, count(*) checks, coalesce(sum(bad),0) failures FROM checks;
