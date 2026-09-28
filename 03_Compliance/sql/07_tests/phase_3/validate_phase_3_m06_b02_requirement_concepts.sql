-- Read-only structural/regression validator for the M06-B02 schema migration.
WITH checks AS (
  SELECT 'CONCEPT_TABLE' AS check_id, CASE WHEN count(*)=1 THEN 0 ELSE 1 END failures
  FROM information_schema.tables WHERE table_schema='mapping' AND table_name='phase3_requirement_concepts'
  UNION ALL SELECT 'BRIDGE_TABLE', CASE WHEN count(*)=1 THEN 0 ELSE 1 END
  FROM information_schema.tables WHERE table_schema='mapping' AND table_name='phase3_concept_mappings'
  UNION ALL SELECT 'EMPTY_SCHEMA_ONLY', (SELECT count(*) FROM mapping.phase3_requirement_concepts)+(SELECT count(*) FROM mapping.phase3_concept_mappings)
  UNION ALL SELECT 'CONCEPT_PK', CASE WHEN count(*)=1 THEN 0 ELSE 1 END
  FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_requirement_concepts' AND constraint_type='PRIMARY KEY'
  UNION ALL SELECT 'BRIDGE_PAIR_PK', CASE WHEN count(*)=1 THEN 0 ELSE 1 END
  FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_concept_mappings' AND constraint_type='PRIMARY KEY'
  UNION ALL SELECT 'BRIDGE_NO_MAPPING_ONLY_UNIQUE', count(*)
  FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_concept_mappings' AND constraint_type='UNIQUE'
  UNION ALL SELECT 'REQUIREMENTS', abs((SELECT count(*) FROM compliance.requirements)-48)
  UNION ALL SELECT 'LEGACY_MAPPING_COUNT', abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
  UNION ALL SELECT 'LEGACY_IDS',
    (SELECT count(*) FROM (SELECT unnest(['M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT','M04-MAP-A08P03-GTFS-ATTRIBUTION','M04-MAP-A08P03-GTFS-PUBLISHER','M06-B01-MAP-A03-P03-001-NAP-DISCOVERY']) mapping_id
      EXCEPT SELECT mapping_id FROM mapping.phase3_requirement_capabilities))
    + (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id NOT IN
      ('M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT','M04-MAP-A08P03-GTFS-ATTRIBUTION','M04-MAP-A08P03-GTFS-PUBLISHER','M06-B01-MAP-A03-P03-001-NAP-DISCOVERY'))
  UNION ALL SELECT 'LEGACY_ASSOCIATIONS', count(*)
    FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_capabilities m USING(mapping_id)
    WHERE m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
  UNION ALL SELECT 'BRIDGE_ORPHANS',
    (SELECT count(*) FROM mapping.phase3_concept_mappings cm LEFT JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id IS NULL)
    +(SELECT count(*) FROM mapping.phase3_concept_mappings cm LEFT JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_id IS NULL)
  UNION ALL SELECT 'REQUIREMENT_REFERENCE_ORPHANS', count(*)
    FROM mapping.phase3_requirement_concepts c LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL
  UNION ALL SELECT 'REQUIREMENT_MISMATCH', count(*)
    FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_concepts c USING(concept_id)
    JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE c.requirement_id<>m.requirement_id
  UNION ALL SELECT 'DUPLICATE_PAIRS', count(*) FROM
    (SELECT concept_id,mapping_id FROM mapping.phase3_concept_mappings GROUP BY ALL HAVING count(*)>1)
  UNION ALL SELECT 'SCOPE_VOCABULARY', abs((SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='REQUIREMENT_CONCEPT_SCOPE')-4)
  UNION ALL SELECT 'COVERAGE_ROWS', abs((SELECT count(*) FROM mapping.phase3_requirement_coverage)-8)
  UNION ALL SELECT 'REVIEWS', abs((SELECT count(*) FROM mapping.phase3_mapping_reviews)-6)
  UNION ALL SELECT 'EXCEPTIONS', abs((SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
  UNION ALL SELECT 'PHASE1_PROVISIONS', abs((SELECT count(*) FROM source.provisions)-92)
  UNION ALL SELECT 'PHASE1_SOURCE_FACTS', abs((SELECT count(*) FROM compliance.source_facts)-36)
  UNION ALL SELECT 'PHASE2_REQUIREMENTS', abs((SELECT count(*) FROM compliance.requirements)-48)
  UNION ALL SELECT 'PHASE2_DEADLINES', abs((SELECT count(*) FROM compliance.deadlines)-10)
  UNION ALL SELECT 'OBSERVED_EVIDENCE', (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
  UNION ALL SELECT 'REPRESENTABILITY', (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
  UNION ALL SELECT 'AUDIT_RULES', (SELECT count(*) FROM audit.rules)
)
SELECT check_id, failures, CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END status
FROM checks ORDER BY check_id;
