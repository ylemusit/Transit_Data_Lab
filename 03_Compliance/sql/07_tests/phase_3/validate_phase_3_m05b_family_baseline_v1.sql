WITH memberships AS (
 SELECT * FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
), expected_family_counts(family_id,expected_count) AS (VALUES
 ('F01',8),('F02',8),('F03',9),('F04',4),('F05',3),('F06',4),('F07',5),('F08',1),('F09',6)
), checks AS (
 SELECT 'REQUIREMENTS' check_name,abs((SELECT count(*) FROM compliance.requirements)-48) invalid_count
 UNION ALL SELECT 'FAMILY_COUNT',abs((SELECT count(*) FROM mapping.phase3_families)-9)
 UNION ALL SELECT 'CLASSIFIED_REQUIREMENTS',48-(SELECT count(DISTINCT requirement_id) FROM memberships WHERE relation_type='PRIMARY_FAMILY')
 UNION ALL SELECT 'PRIMARY_ASSIGNMENTS',abs((SELECT count(*) FROM memberships WHERE relation_type='PRIMARY_FAMILY')-48)
 UNION ALL SELECT 'WITHOUT_PRIMARY',(SELECT count(*) FROM compliance.requirements r WHERE NOT EXISTS (SELECT 1 FROM memberships m WHERE m.requirement_id=r.requirement_id AND m.relation_type='PRIMARY_FAMILY'))
 UNION ALL SELECT 'MULTIPLE_PRIMARY',(SELECT count(*) FROM (SELECT requirement_id FROM memberships WHERE relation_type='PRIMARY_FAMILY' GROUP BY requirement_id HAVING count(*)<>1))
 UNION ALL SELECT 'UNKNOWN_REQUIREMENTS',(SELECT count(*) FROM memberships m LEFT JOIN compliance.requirements r USING(requirement_id) WHERE r.requirement_id IS NULL)
 UNION ALL SELECT 'DUPLICATES',(SELECT count(*) FROM (SELECT requirement_id,family_id,relation_type FROM memberships GROUP BY 1,2,3 HAVING count(*)>1))
 UNION ALL SELECT 'SECONDARY_ASSIGNMENTS',abs((SELECT count(*) FROM memberships WHERE relation_type='SECONDARY_CHARACTERISTIC'))
 UNION ALL SELECT 'MISSING_REASON',(SELECT count(*) FROM memberships WHERE length(trim(coalesce(classification_reason,'')))=0)
 UNION ALL SELECT 'INVALID_CONFIDENCE',(SELECT count(*) FROM memberships WHERE classification_confidence NOT IN ('HIGH','MEDIUM','LOW'))
 UNION ALL SELECT 'CONFIDENCE_COUNTS',abs((SELECT count(*) FROM memberships WHERE classification_confidence='HIGH')-41)+abs((SELECT count(*) FROM memberships WHERE classification_confidence='MEDIUM')-7)+abs((SELECT count(*) FROM memberships WHERE classification_confidence='LOW'))
 UNION ALL SELECT 'FAMILY_COUNTS',(SELECT count(*) FROM expected_family_counts e LEFT JOIN mapping.phase3_families f USING(family_id) WHERE f.family_id IS NULL OR (SELECT count(*) FROM memberships m WHERE m.family_id=e.family_id AND m.relation_type='PRIMARY_FAMILY')<>e.expected_count)+(SELECT count(*) FROM mapping.phase3_families WHERE family_id NOT IN (SELECT family_id FROM expected_family_counts))
 UNION ALL SELECT 'INVALID_RELATION',(SELECT count(*) FROM memberships WHERE relation_type NOT IN ('PRIMARY_FAMILY','SECONDARY_CHARACTERISTIC'))
 UNION ALL SELECT 'INVALID_REVIEW',(SELECT count(*) FROM memberships WHERE review_status NOT IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED'))
 UNION ALL SELECT 'PILOTS',(SELECT count(*) FROM (VALUES
  ('EU-2017-1926-REQ-A04-P01-001'),('EU-2017-1926-REQ-A04-P02-001'),('EU-2017-1926-REQ-A08-P03-001-01'),('EU-2017-1926-REQ-A05-P03-001'),('EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')
 ) p(requirement_id) WHERE (SELECT count(*) FROM memberships m WHERE m.requirement_id=p.requirement_id AND m.relation_type='PRIMARY_FAMILY')<>1)
 UNION ALL SELECT 'B01',(SELECT count(*) FROM (VALUES
  ('EU-2017-1926-REQ-A03-P01-001'),('EU-2017-1926-REQ-A03-P01-002'),('EU-2017-1926-REQ-A03-P03-001')
 ) b(requirement_id) WHERE (SELECT count(*) FROM memberships m WHERE m.requirement_id=b.requirement_id AND m.relation_type='PRIMARY_FAMILY' AND m.family_id='F01')<>1)
 UNION ALL SELECT 'FAMILY_REFERENCES',(SELECT count(*) FROM memberships m LEFT JOIN mapping.phase3_families f USING(family_id) WHERE f.family_id IS NULL)
 UNION ALL SELECT 'PILOT_MAPPINGS',abs((SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id LIKE 'M04-%')-5)
 UNION ALL SELECT 'NONPILOT_MAPPINGS',(SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND mapping_id NOT LIKE 'M04-%'
   AND requirement_id NOT IN ('EU-2017-1926-REQ-A03-P01-001','EU-2017-1926-REQ-A03-P01-002','EU-2017-1926-REQ-A03-P03-001'))
 UNION ALL SELECT 'MAPPING_REVIEWS',abs((SELECT count(*) FROM mapping.phase3_mapping_reviews WHERE mapping_id LIKE 'M04-MAP-%')-5)
 UNION ALL SELECT 'COVERAGE_DECISIONS',abs((SELECT count(*) FROM mapping.phase3_requirement_coverage WHERE coverage_id LIKE 'M04B-COV-%')-5)
 UNION ALL SELECT 'ASSERTIONS',(SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'OBSERVED_EVIDENCE',(SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')
 UNION ALL SELECT 'AUDIT_RULES',(SELECT count(*) FROM audit.rules)
), summary AS (
 SELECT count(*) FILTER (WHERE relation_type='SECONDARY_CHARACTERISTIC') secondary_assignments,
 count(*) FILTER (WHERE classification_confidence='HIGH') high_confidence,
 count(*) FILTER (WHERE classification_confidence='MEDIUM') medium_confidence,
 count(*) FILTER (WHERE classification_confidence='LOW') low_confidence
 FROM memberships
)
SELECT CASE WHEN (SELECT coalesce(sum(invalid_count),0) FROM checks)=0 THEN 'PASS' ELSE 'FAIL' END AS family_baseline_validation,
 (SELECT coalesce(sum(invalid_count),0) FROM checks) AS failures,
 (SELECT secondary_assignments FROM summary) secondary_assignments,
 (SELECT high_confidence FROM summary) high_confidence,
 (SELECT medium_confidence FROM summary) medium_confidence,
 (SELECT low_confidence FROM summary) low_confidence;

SELECT f.family_id,f.family_name,count(m.requirement_id) FILTER (WHERE m.relation_type='PRIMARY_FAMILY') total_primary,
 count(m.requirement_id) FILTER (WHERE m.relation_type='PRIMARY_FAMILY' AND m.requirement_id IN (
 'EU-2017-1926-REQ-A04-P01-001','EU-2017-1926-REQ-A04-P02-001','EU-2017-1926-REQ-A08-P03-001-01','EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')) pilot_primary,
 count(m.requirement_id) FILTER (WHERE m.relation_type='PRIMARY_FAMILY' AND m.requirement_id NOT IN (
 'EU-2017-1926-REQ-A04-P01-001','EU-2017-1926-REQ-A04-P02-001','EU-2017-1926-REQ-A08-P03-001-01','EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')) remaining_primary
FROM mapping.phase3_families f LEFT JOIN mapping.phase3_requirement_families m USING(family_id)
GROUP BY f.family_id,f.family_name ORDER BY f.family_id;

SELECT r.requirement_id,m.family_id,m.classification_confidence,m.classification_reason
FROM compliance.requirements r JOIN mapping.phase3_requirement_families m USING(requirement_id)
WHERE r.requirement_id IN ('EU-2017-1926-REQ-A04-P01-001','EU-2017-1926-REQ-A04-P02-001','EU-2017-1926-REQ-A08-P03-001-01','EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS','EU-2017-1926-REQ-A03-P01-001','EU-2017-1926-REQ-A03-P01-002','EU-2017-1926-REQ-A03-P03-001')
 AND m.relation_type='PRIMARY_FAMILY' ORDER BY r.requirement_id;
