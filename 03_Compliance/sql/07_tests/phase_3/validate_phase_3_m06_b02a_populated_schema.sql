-- Authoritative populated-schema gate after M06-B02A.
-- Read-only. Does not authorize or persist capabilities, mappings, bridges, or coverage.
WITH expected(concept_id, requirement_id, concept_code, scope_status, review_outcome) AS (
  VALUES
    ('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','EU-2017-1926-REQ-A05-P01-002','ROAD_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
    ('M06-B02-CPT-A05-P02-001-ROAD-STATUS-DISRUPTION','EU-2017-1926-REQ-A05-P02-001','ROAD_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
    ('M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','EU-2017-1926-REQ-A05-P02-001','PASSENGER_RT_STATUS_DISRUPTION','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
    ('M06-B02-CPT-A05-P02-001-FACILITY-ACCESS-NODE-STATUS','EU-2017-1926-REQ-A05-P02-001','FACILITY_ACCESS_NODE_STATUS','PARTIAL','ACCEPTED_WITH_LIMITATIONS'),
    ('M06-B02-CPT-A05-P02-001-PARKING-TARIFF','EU-2017-1926-REQ-A05-P02-001','PARKING_TARIFF','PARTIAL',NULL),
    ('M06-B02-CPT-A05-P02-001-SHARED-VEHICLE-AVAILABILITY','EU-2017-1926-REQ-A05-P02-001','SHARED_VEHICLE_AVAILABILITY','UNRESOLVED','UNRESOLVED'),
    ('M06-B02-CPT-A05-P02-001-PARKING-AVAILABILITY','EU-2017-1926-REQ-A05-P02-001','PARKING_AVAILABILITY','PARTIAL',NULL)
), checks AS (
  SELECT 'SCHEMA_TABLES' check_name,
    CASE WHEN (SELECT count(*) FROM information_schema.tables WHERE table_schema='mapping' AND table_name IN ('phase3_requirement_concepts','phase3_concept_mappings'))=2 THEN 0 ELSE 1 END failures
  UNION ALL SELECT 'SCHEMA_CONSTRAINTS',
    CASE WHEN
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_requirement_concepts' AND constraint_type='PRIMARY KEY' AND constraint_text='PRIMARY KEY(concept_id)')=1 AND
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_requirement_concepts' AND constraint_type='UNIQUE' AND constraint_text='UNIQUE(requirement_id, concept_code)')=1 AND
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_requirement_concepts' AND constraint_type='CHECK')>=6 AND
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_concept_mappings' AND constraint_type='PRIMARY KEY' AND constraint_text='PRIMARY KEY(concept_id, mapping_id)')=1 AND
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_concept_mappings' AND constraint_type='FOREIGN KEY')=2 AND
      (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_concept_mappings' AND constraint_type='UNIQUE')=0
    THEN 0 ELSE 1 END
  UNION ALL SELECT 'CONCEPT_SET',
    (SELECT count(*) FROM expected e LEFT JOIN mapping.phase3_requirement_concepts c USING(concept_id, requirement_id, concept_code)
      WHERE c.concept_id IS NULL OR c.scope_status IS DISTINCT FROM e.scope_status OR c.review_outcome IS DISTINCT FROM e.review_outcome)
    + (SELECT count(*) FROM mapping.phase3_requirement_concepts c LEFT JOIN expected e USING(concept_id) WHERE e.concept_id IS NULL)
    + abs((SELECT count(*) FROM mapping.phase3_requirement_concepts)-7)
  UNION ALL SELECT 'P01_P02_SPLIT',
    abs((SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE requirement_id='EU-2017-1926-REQ-A05-P01-002')-1)
    + abs((SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE requirement_id='EU-2017-1926-REQ-A05-P02-001')-6)
  UNION ALL SELECT 'REQUIREMENT_REFERENCES',
    (SELECT count(*) FROM mapping.phase3_requirement_concepts c LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL)
  UNION ALL SELECT 'VALID_VOCABULARY',
    (SELECT count(*) FROM mapping.phase3_requirement_concepts c LEFT JOIN mapping.phase3_vocabularies v ON v.vocabulary='REQUIREMENT_CONCEPT_SCOPE' AND v.value=c.scope_status WHERE v.value IS NULL)
    + abs((SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='REQUIREMENT_CONCEPT_SCOPE')-4)
  UNION ALL SELECT 'FORBIDDEN_TRAVEL_TIME_CONCEPTS',
    (SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE
      (lower(concept_code || ' ' || concept_name || ' ' || concept_description) LIKE '%road%link%travel%time%') OR
      (lower(concept_code || ' ' || concept_name || ' ' || concept_description) LIKE '%predicted%travel%time%'))
  UNION ALL SELECT 'B02_MAPPINGS',
    (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
  UNION ALL SELECT 'B02_BRIDGES',
    (SELECT count(*) FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id LIKE 'M06-B02-CPT-A05-%')
  UNION ALL SELECT 'B02_COVERAGE',
    (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
  UNION ALL SELECT 'B02_OTHER_LAYERS',
    (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
    + (SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id)
       WHERE m.requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
    + (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
    + (SELECT count(*) FROM audit.rules)
  UNION ALL SELECT 'LEGACY_MAPPINGS',
    abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
    + (SELECT count(*) FROM (VALUES
      ('M04-MAP-A04P01-GTFS-TRIP-STOP'),('M04-MAP-A04P01-NETEX-PT'),('M04-MAP-A04P02-NETEX-PT'),
      ('M04-MAP-A08P03-GTFS-ATTRIBUTION'),('M04-MAP-A08P03-GTFS-PUBLISHER'),('M06-B01-MAP-A03-P03-001-NAP-DISCOVERY')
    ) e(mapping_id) LEFT JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_id IS NULL)
    + (SELECT count(*) FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
  UNION ALL SELECT 'PROTECTED_PHASES',
    abs((SELECT count(*) FROM source.provisions)-92)+abs((SELECT count(*) FROM compliance.source_facts)-36)
    +abs((SELECT count(*) FROM compliance.requirements)-48)+abs((SELECT count(*) FROM compliance.deadlines)-10)
), summary AS (SELECT count(*) checks, coalesce(sum(failures),0) failures FROM checks)
SELECT CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END populated_schema_gate,
       checks, failures,
       (SELECT string_agg(check_name || '=' || failures::VARCHAR, '; ' ORDER BY check_name) FROM checks WHERE failures<>0) failing_checks
FROM summary;
