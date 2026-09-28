-- M06-B02C schema validator. Run against the populated current database read-only.
WITH expected_legacy(mapping_id) AS (VALUES
 ('M04-MAP-A04P01-GTFS-TRIP-STOP'),('M04-MAP-A04P01-NETEX-PT'),('M04-MAP-A04P02-NETEX-PT'),
 ('M04-MAP-A08P03-GTFS-ATTRIBUTION'),('M04-MAP-A08P03-GTFS-PUBLISHER'),('M06-B01-MAP-A03-P03-001-NAP-DISCOVERY')
), checks AS (
 SELECT 'SCOPE_TABLES' check_name, CASE WHEN
  (SELECT count(*) FROM information_schema.tables WHERE table_schema='mapping' AND table_name IN ('phase3_mapping_scope_units','phase3_scope_source_references'))=2 THEN 0 ELSE 1 END failures
 UNION ALL SELECT 'SCOPE_IDENTITY_AND_COLUMNS', CASE WHEN
  (SELECT count(*) FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_mapping_scope_units' AND column_name IN
   ('scope_unit_id','concept_id','mapping_id','unit_code','unit_name','unit_definition','scope_disposition'))=7 THEN 0 ELSE 1 END
 UNION ALL SELECT 'SCOPE_PRIMARY_KEY', CASE WHEN
  (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_mapping_scope_units' AND constraint_type='PRIMARY KEY' AND constraint_text='PRIMARY KEY(scope_unit_id)')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'SCOPE_UNIQUENESS', CASE WHEN
  (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_mapping_scope_units' AND constraint_type='UNIQUE' AND constraint_text='UNIQUE(concept_id, mapping_id, unit_code)')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'SCOPE_BRIDGE_FOREIGN_KEY', CASE WHEN
  (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_mapping_scope_units' AND constraint_type='FOREIGN KEY')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'SOURCE_BRIDGE_CONSTRAINTS', CASE WHEN
  (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_scope_source_references' AND constraint_type='PRIMARY KEY')=1 AND
  (SELECT count(*) FROM duckdb_constraints() WHERE schema_name='mapping' AND table_name='phase3_scope_source_references' AND constraint_type='FOREIGN KEY')=2 THEN 0 ELSE 1 END
 UNION ALL SELECT 'SCOPE_DISPOSITION_VOCABULARY', CASE WHEN
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='MAPPING_SCOPE_DISPOSITION' AND value IN ('INCLUDED','UNRESOLVED','EXCLUDED'))=3 AND
  (SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='MAPPING_SCOPE_DISPOSITION')=3 THEN 0 ELSE 1 END
 UNION ALL SELECT 'EMPTY_SCOPE_STATE', (SELECT count(*) FROM mapping.phase3_mapping_scope_units)+(SELECT count(*) FROM mapping.phase3_scope_source_references)
 UNION ALL SELECT 'GLOBAL_MAPPINGS', abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
 UNION ALL SELECT 'LEGACY_MAPPING_IDS', (SELECT count(*) FROM expected_legacy e LEFT JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_id IS NULL OR m.fixture_kind='SYNTHETIC_TEST')
 UNION ALL SELECT 'LEGACY_SCOPE_ASSIGNMENTS', (SELECT count(*) FROM mapping.phase3_mapping_scope_units s JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'B02_CONCEPTS', abs((SELECT count(*) FROM mapping.phase3_requirement_concepts WHERE concept_id LIKE 'M06-B02-CPT-A05-%')-7)
 UNION ALL SELECT 'B02_MAPPINGS', (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'B02_BRIDGES', (SELECT count(*) FROM mapping.phase3_concept_mappings cm JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id LIKE 'M06-B02-CPT-A05-%')
 UNION ALL SELECT 'B02_SCOPE_ROWS', (SELECT count(*) FROM mapping.phase3_mapping_scope_units s JOIN mapping.phase3_concept_mappings cm USING(concept_id,mapping_id) JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id LIKE 'M06-B02-CPT-A05-%')
 UNION ALL SELECT 'B02_SOURCE_BRIDGES', (SELECT count(*) FROM mapping.phase3_scope_source_references sr JOIN mapping.phase3_mapping_scope_units s USING(scope_unit_id) JOIN mapping.phase3_concept_mappings cm USING(concept_id,mapping_id) JOIN mapping.phase3_requirement_concepts c USING(concept_id) WHERE c.concept_id LIKE 'M06-B02-CPT-A05-%')
 UNION ALL SELECT 'B02_COVERAGE', (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'B02_REPRESENTABILITY', (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'B02_AUTOMATABILITY', (SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.requirement_id IN ('EU-2017-1926-REQ-A05-P01-002','EU-2017-1926-REQ-A05-P02-001'))
 UNION ALL SELECT 'B02_OBSERVED_EVIDENCE', (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'AUDIT_RULES', (SELECT count(*) FROM audit.rules)
 UNION ALL SELECT 'PROTECTED_PHASES', abs((SELECT count(*) FROM source.provisions)-92)+abs((SELECT count(*) FROM compliance.source_facts)-36)+abs((SELECT count(*) FROM compliance.requirements)-48)+abs((SELECT count(*) FROM compliance.deadlines)-10)
 UNION ALL SELECT 'COVERAGE_GLOBAL', abs((SELECT count(*) FROM mapping.phase3_requirement_coverage)-8)
 UNION ALL SELECT 'REPRESENTABILITY_GLOBAL', (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'OBSERVED_GLOBAL', (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'AUTOMATABILITY_GLOBAL', abs((SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')-6)
), summary AS (SELECT count(*) checks, coalesce(sum(failures),0) failures FROM checks)
SELECT CASE WHEN failures=0 THEN 'PASS' ELSE 'FAIL' END status, checks, failures,
 (SELECT string_agg(check_name || '=' || failures::VARCHAR, '; ' ORDER BY check_name) FROM checks WHERE failures<>0) failing_checks
FROM summary;
