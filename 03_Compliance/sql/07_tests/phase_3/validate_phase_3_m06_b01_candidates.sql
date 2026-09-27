-- M06-B01-HR reviewed-state validator. Covers semantic decisions and guards.
WITH b01(requirement_id) AS (VALUES
 ('EU-2017-1926-REQ-A03-P01-001'),
 ('EU-2017-1926-REQ-A03-P01-002'),
 ('EU-2017-1926-REQ-A03-P03-001')
), checks AS (
 SELECT 'B01_EXCEPTION_SET' check_name,
   (SELECT count(*) FROM (VALUES
     ('M06-B01-EXC-A03-P01-001','EU-2017-1926-REQ-A03-P01-001','LEGAL_PROCESS'),
     ('M06-B01-EXC-A03-P01-002','EU-2017-1926-REQ-A03-P01-002','ORGANIZATIONAL'),
     ('M06-B01-EXC-A03-P03-001','EU-2017-1926-REQ-A03-P03-001','MANUAL_ASSESSMENT')
   ) e(exception_id,requirement_id,exception_type)
   LEFT JOIN mapping.phase3_exceptions a USING(exception_id)
   WHERE a.exception_id IS NULL OR a.requirement_id IS DISTINCT FROM e.requirement_id
      OR a.exception_type IS DISTINCT FROM e.exception_type OR a.review_status IS DISTINCT FROM 'NEEDS_REVIEW'
      OR a.fixture_kind IS NOT NULL)
   + (SELECT count(*) FROM mapping.phase3_exceptions a
      WHERE (a.requirement_id IN (SELECT requirement_id FROM b01) OR a.exception_id LIKE 'M06-B01-%')
        AND a.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
        AND a.exception_id NOT IN ('M06-B01-EXC-A03-P01-001','M06-B01-EXC-A03-P01-002','M06-B01-EXC-A03-P03-001')) failures
 UNION ALL
 SELECT 'B01_REQUIREMENT_SET', CASE WHEN (SELECT count(*) FROM b01)=3 AND
   (SELECT count(*) FROM compliance.requirements r JOIN b01 USING(requirement_id))=3 THEN 0 ELSE 1 END
 UNION ALL SELECT 'F01_ASSIGNMENTS', count(*) FROM b01 LEFT JOIN mapping.phase3_requirement_families f USING(requirement_id)
   WHERE f.family_id IS DISTINCT FROM 'F01' OR f.relation_type IS DISTINCT FROM 'PRIMARY_FAMILY'
 UNION ALL SELECT 'P01_001_NONTECHNICAL_ONLY',
   (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id='EU-2017-1926-REQ-A03-P01-001') +
   CASE WHEN (SELECT count(*) FROM mapping.phase3_exceptions WHERE exception_id='M06-B01-EXC-A03-P01-001' AND exception_type='LEGAL_PROCESS')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'P01_002_NONTECHNICAL_ONLY',
   (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id='EU-2017-1926-REQ-A03-P01-002') +
   CASE WHEN (SELECT count(*) FROM mapping.phase3_exceptions WHERE exception_id='M06-B01-EXC-A03-P01-002' AND exception_type='ORGANIZATIONAL')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'P03_MAPPING_AND_REVIEW', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_requirement_capabilities m JOIN b01 USING(requirement_id)
    WHERE requirement_id='EU-2017-1926-REQ-A03-P03-001' AND mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY'
      AND capability_id='NAP_DATA_DISCOVERY' AND mapping_type='PARTIAL' AND review_status='REVIEWED' AND fixture_kind IS NULL)=1 AND
   (SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY'
      AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS' AND length(trim(coalesce(limitations,'')))>0)=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'NAP_CAPABILITY_AND_STANDARD_BOUNDARY', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY' AND standard_id IS NULL
      AND review_status='REVIEWED')=1 AND
   (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY')=1 AND
   (SELECT count(*) FROM mapping.phase3_standards WHERE standard_id='NAP_DATA_DISCOVERY')=0 AND
   (SELECT count(*) FROM mapping.phase3_capabilities WHERE standard_id IS NULL)=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'OFFICIAL_LEGAL_SOURCE', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id='M06-B01-SRC-REG-2017-1926'
     AND capability_id='NAP_DATA_DISCOVERY' AND source_kind='OFFICIAL_LEGAL_SOURCE')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'P03_MANUAL_PATH_PRESERVED', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_exceptions WHERE exception_id='M06-B01-EXC-A03-P03-001'
      AND requirement_id='EU-2017-1926-REQ-A03-P03-001' AND exception_type='MANUAL_ASSESSMENT')=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'B01_AUTOMATABILITY', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id)
      WHERE m.mapping_id='M06-B01-MAP-A03-P03-001-NAP-DISCOVERY' AND a.automatability_state='PARTIAL'
        AND a.review_status='REVIEWED')=1 AND
   (SELECT count(*) FROM mapping.phase3_automatability a JOIN mapping.phase3_requirement_capabilities m USING(mapping_id)
      JOIN b01 USING(requirement_id))=1 THEN 0 ELSE 1 END
 UNION ALL SELECT 'B01_COVERAGE', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_requirement_coverage c JOIN b01 USING(requirement_id)
     WHERE coverage_state='PARTIAL' AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS' AND review_status='REVIEWED'
       AND coverage_id LIKE 'M06-B01-COV-%')=3 AND
   (SELECT count(*) FROM mapping.phase3_requirement_coverage c JOIN b01 USING(requirement_id))=3 THEN 0 ELSE 1 END
 UNION ALL SELECT 'NO_REPRESENTABILITY_OR_OBSERVED_EVIDENCE_OR_RULES', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
   (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
   (SELECT count(*) FROM audit.rules)=0 THEN 0 ELSE 1 END
 UNION ALL SELECT 'TOTALS', CASE WHEN
   (SELECT count(*) FROM mapping.phase3_capabilities)=6 AND
   (SELECT count(*) FROM mapping.phase3_source_references)=8 AND
   (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
   (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN (SELECT requirement_id FROM b01))=1 AND
   (SELECT count(*) FROM mapping.phase3_mapping_reviews)=6 AND
   (SELECT count(*) FROM mapping.phase3_requirement_coverage)=8 AND
   (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 AND
   (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=6 THEN 0 ELSE 1 END
 UNION ALL SELECT 'FAMILIES_UNCHANGED', CASE WHEN (SELECT count(*) FROM mapping.phase3_families)=9 AND
      (SELECT count(*) FROM mapping.phase3_requirement_families WHERE relation_type='PRIMARY_FAMILY')=48 AND
      (SELECT count(*) FROM mapping.phase3_requirement_families WHERE relation_type='SECONDARY_CHARACTERISTIC')=0 THEN 0 ELSE 1 END
 UNION ALL SELECT 'PILOT_MAPPING_COUNT_UNCHANGED', CASE WHEN count(*)=5 THEN 0 ELSE 1 END
   FROM mapping.phase3_requirement_capabilities WHERE requirement_id IN
   ('EU-2017-1926-REQ-A04-P01-001','EU-2017-1926-REQ-A04-P02-001','EU-2017-1926-REQ-A08-P03-001-01','EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')
)
SELECT CASE WHEN sum(failures)=0 THEN 'PASS' ELSE 'FAIL' END b01_structural_validation,
       sum(failures) structural_failures,
       string_agg(check_name || '=' || failures::VARCHAR, '; ' ORDER BY check_name) checks
FROM checks;
