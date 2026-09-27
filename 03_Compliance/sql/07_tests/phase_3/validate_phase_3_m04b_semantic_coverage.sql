WITH pilots(requirement_id) AS (VALUES
 ('EU-2017-1926-REQ-A04-P01-001'),('EU-2017-1926-REQ-A04-P02-001'),
 ('EU-2017-1926-REQ-A08-P03-001-01'),('EU-2017-1926-REQ-A05-P03-001'),
 ('EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')
), checks AS (
 SELECT 'COVERAGE_REFERENCE' check_name,count(*)::BIGINT n FROM mapping.phase3_requirement_coverage c LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL
 UNION ALL SELECT 'NON_PILOT_COVERAGE',count(*) FROM mapping.phase3_requirement_coverage
   WHERE requirement_id NOT IN (SELECT requirement_id FROM pilots)
     AND requirement_id NOT IN ('EU-2017-1926-REQ-A03-P01-001','EU-2017-1926-REQ-A03-P01-002','EU-2017-1926-REQ-A03-P03-001')
 UNION ALL SELECT 'COVERAGE_PILOT_COUNT',abs((SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id IN (SELECT requirement_id FROM pilots))-5)
 UNION ALL SELECT 'MAPPING_REVIEW_REFERENCE',count(*) FROM mapping.phase3_mapping_reviews r LEFT JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.mapping_id IS NULL
 UNION ALL SELECT 'MAPPING_REVIEW_COUNT',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id LIKE 'M04-MAP-%')-5)
 UNION ALL SELECT 'MISSING_M04_MAPPING_REVIEW',count(*) FROM mapping.phase3_requirement_capabilities m LEFT JOIN mapping.phase3_mapping_reviews r USING(mapping_id) WHERE m.mapping_id LIKE 'M04-MAP-%' AND r.mapping_id IS NULL
 UNION ALL SELECT 'A04P01_MAPPING_REVIEW',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id IN ('M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT') AND semantic_review_outcome='ACCEPTED')-2)
 UNION ALL SELECT 'A04P02_MAPPING_REVIEW',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id='M04-MAP-A04P02-NETEX-PT' AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS')-1)
 UNION ALL SELECT 'A08_MAPPING_REVIEW',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id IN ('M04-MAP-A08P03-GTFS-PUBLISHER','M04-MAP-A08P03-GTFS-ATTRIBUTION') AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS')-2)
 UNION ALL SELECT 'INVALID_COVERAGE_VOCABULARY',count(*) FROM mapping.phase3_requirement_coverage WHERE coverage_state NOT IN ('ESTABLISHED','PARTIAL','UNRESOLVED','NOT_APPLICABLE','NONE_IDENTIFIED')
 UNION ALL SELECT 'INVALID_SEMANTIC_OUTCOME',count(*) FROM (SELECT semantic_review_outcome FROM mapping.phase3_mapping_reviews UNION ALL SELECT semantic_review_outcome FROM mapping.phase3_requirement_coverage) x WHERE semantic_review_outcome NOT IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS','REJECTED','UNRESOLVED')
 UNION ALL SELECT 'MAPPING_WORKFLOW_SEPARATION',count(*) FROM mapping.phase3_mapping_reviews r JOIN mapping.phase3_requirement_capabilities m USING(mapping_id) WHERE m.review_status NOT IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED') OR r.semantic_review_outcome IS NULL
 UNION ALL SELECT 'COVERAGE_REVIEWED_BASELINE',abs((SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE reviewed_against_baseline='M04_LOCAL_PILOT_MAPPING_SET_2026-09-27')-5)
 UNION ALL SELECT 'ZERO_MAPPING_PATH_FAILURE',count(*) FROM mapping.phase3_requirement_coverage c WHERE c.requirement_id IN ('EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS') AND (length(trim(c.identified_paths))=0 OR EXISTS (SELECT 1 FROM mapping.phase3_requirement_capabilities m WHERE m.requirement_id=c.requirement_id AND m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'))
 UNION ALL SELECT 'A08_HYBRID_PATH_FAILURE',CASE WHEN EXISTS (SELECT 1 FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A08-P03-001-01' AND coverage_state='PARTIAL' AND identified_paths LIKE '%EXCEPTION:M03-EXC-A08-SOURCE-REQUEST%' AND identified_paths LIKE '%MAPPING:%') AND EXISTS (SELECT 1 FROM mapping.phase3_exceptions WHERE exception_id='M03-EXC-A08-SOURCE-REQUEST' AND exception_type='EXTERNAL_EVIDENCE') THEN 0 ELSE 1 END
 UNION ALL SELECT 'A04P02_UNRESOLVED_FAILURE',CASE WHEN EXISTS (SELECT 1 FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A04-P02-001' AND coverage_state='UNRESOLVED' AND semantic_review_outcome='UNRESOLVED' AND limitations LIKE '%unresolved%') THEN 0 ELSE 1 END
 UNION ALL SELECT 'LEGAL_COMPLIANCE_FIELD',count(*) FROM information_schema.columns WHERE table_schema='mapping' AND table_name IN ('phase3_mapping_reviews','phase3_requirement_coverage') AND column_name ILIKE '%compliance%'
 UNION ALL SELECT 'REPRESENTABILITY_ROWS',count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
 UNION ALL SELECT 'OBSERVED_EVIDENCE_ROWS',count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
 UNION ALL SELECT 'AUDIT_RULES',count(*) FROM audit.rules
), pilot_results AS (
 SELECT
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A04-P01-001' AND coverage_state='PARTIAL' AND semantic_review_outcome='ACCEPTED_WITH_LIMITATIONS' AND identified_paths LIKE '%MAPPING:%')=1 a041,
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A04-P02-001' AND coverage_state='UNRESOLVED' AND semantic_review_outcome='UNRESOLVED')=1 a042,
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A08-P03-001-01' AND coverage_state='PARTIAL' AND identified_paths LIKE '%EXCEPTION:%')=1 a08,
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A05-P03-001' AND identified_paths LIKE '%M03-EXC-A05-DEADLINE%')=1 a05,
  (SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE requirement_id='EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS' AND identified_paths LIKE '%M03-EXC-A09-RANDOM-CHECKS%')=1 a09
)
SELECT CASE WHEN (SELECT coalesce(sum(n),0) FROM checks)=0 THEN 'PASS' ELSE 'FAIL' END status,
 (SELECT coalesce(sum(n),0) FROM checks) structural_failures,
 (SELECT a041 FROM pilot_results) a04_p01_regression,
 (SELECT a042 FROM pilot_results) a04_p02_regression,
 (SELECT a08 FROM pilot_results) a08_p03_regression,
 (SELECT a05 FROM pilot_results) a05_p03_regression,
 (SELECT a09 FROM pilot_results) a09_regression,
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities m WHERE m.requirement_id IN ('EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS') AND m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') zero_mapping_pilot_mappings,
 (SELECT count(*) FROM mapping.phase3_requirement_coverage) coverage_decisions,
 (SELECT count(*) FROM mapping.phase3_mapping_reviews) mapping_reviews
FROM (SELECT 1) singleton;
