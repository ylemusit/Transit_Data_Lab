-- Structural guard and HUMAN SEMANTIC REVIEW preparation; not a semantic approval.
WITH pilots(requirement_id) AS (
    VALUES
      ('EU-2017-1926-REQ-A04-P01-001'),
      ('EU-2017-1926-REQ-A04-P02-001'),
      ('EU-2017-1926-REQ-A08-P03-001-01'),
      ('EU-2017-1926-REQ-A05-P03-001'),
      ('EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')
), expected(mapping_id,requirement_id,capability_id) AS (
    VALUES
      ('M04-MAP-A04P01-GTFS-TRIP-STOP','EU-2017-1926-REQ-A04-P01-001','CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES'),
      ('M04-MAP-A04P01-NETEX-PT','EU-2017-1926-REQ-A04-P01-001','CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE'),
      ('M04-MAP-A04P02-NETEX-PT','EU-2017-1926-REQ-A04-P02-001','CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE'),
      ('M04-MAP-A08P03-GTFS-PUBLISHER','EU-2017-1926-REQ-A08-P03-001-01','CAP-GTFS-FEED-PUBLISHER-METADATA'),
      ('M04-MAP-A08P03-GTFS-ATTRIBUTION','EU-2017-1926-REQ-A08-P03-001-01','CAP-GTFS-DATASET-ATTRIBUTION')
), result AS (
    SELECT
      (SELECT count(*) FROM mapping.phase3_requirement_capabilities m WHERE m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND m.requirement_id NOT IN (SELECT requirement_id FROM pilots)) AS non_pilot_mappings,
      (SELECT count(*) FROM mapping.phase3_requirement_capabilities m JOIN expected e USING (mapping_id,requirement_id,capability_id) WHERE m.mapping_type='PARTIAL' AND m.review_status='NEEDS_REVIEW' AND length(trim(coalesce(m.limitations,'')))>0 AND length(trim(coalesce(m.mapping_conditions,'')))>0) AS valid_expected_mappings,
      (SELECT count(*) FROM expected) AS expected_mappings,
      (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND review_status IN ('APPROVED','REVIEWED')) AS accepted_mappings,
      (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS representability_assertions,
      (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND automatability_state='PARTIAL' AND review_status='NEEDS_REVIEW') AS partial_automatability,
      (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS exceptions,
      (SELECT count(*) FROM audit.rules) AS audit_rules,
      (SELECT count(*) FROM compliance.requirements) AS requirements,
      (SELECT count(*) FROM compliance.deadlines) AS deadlines,
      (SELECT count(*) FROM compliance.requirement_candidates) AS candidates,
      (SELECT count(*) FROM compliance.source_facts) AS source_facts
)
SELECT CASE WHEN non_pilot_mappings=0 AND valid_expected_mappings=expected_mappings AND expected_mappings=5
                 AND accepted_mappings=0 AND representability_assertions=0 AND partial_automatability=5
                 AND exceptions=3 AND audit_rules=0 AND requirements=48 AND deadlines=10 AND candidates=34 AND source_facts=36
            THEN 'PASS' ELSE 'FAIL' END AS m04_pilot_structural_validation,
       non_pilot_mappings,valid_expected_mappings,expected_mappings,accepted_mappings,representability_assertions,
       partial_automatability,exceptions,audit_rules,requirements,deadlines,candidates,source_facts
FROM result;

-- PILOT REVIEW VIEW: one row per pilot/capability relationship, including pilots with no format mapping.
WITH pilots(requirement_id) AS (
    VALUES
      ('EU-2017-1926-REQ-A04-P01-001'),
      ('EU-2017-1926-REQ-A04-P02-001'),
      ('EU-2017-1926-REQ-A08-P03-001-01'),
      ('EU-2017-1926-REQ-A05-P03-001'),
      ('EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')
), source_refs AS (
    SELECT capability_id,string_agg(DISTINCT url_or_document_id,'; ' ORDER BY url_or_document_id) AS source_reference
    FROM mapping.phase3_source_references
    WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
    GROUP BY capability_id
)
SELECT p.requirement_id AS pilot_id,
       r.description AS legal_proposal_summary,
       c.capability_id,
       c.semantic_meaning AS capability_name,
       s.standard_name AS standard,
       m.mapping_type,
       'NOT_ASSERTED' AS representability_state,
       coalesce(a.automatability_state,CASE WHEN e.exception_type='MANUAL_ASSESSMENT' THEN 'MANUAL' WHEN e.exception_type='DEADLINE' THEN 'NOT_ESTABLISHED' END) AS automatability_state,
       e.exception_type,
       coalesce(m.mapping_conditions,e.justification) AS justification,
       coalesce(m.limitations,e.evidence_expectations) AS limitation,
       sr.source_reference,
       coalesce(m.review_status,e.review_status,'NEEDS_REVIEW') AS human_review_status,
       CASE
         WHEN p.requirement_id='EU-2017-1926-REQ-A08-P03-001-01' THEN 'HYBRID'
         WHEN p.requirement_id IN ('EU-2017-1926-REQ-A05-P03-001','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS') THEN 'PROCEDURAL'
         WHEN p.requirement_id='EU-2017-1926-REQ-A04-P02-001' THEN 'UNRESOLVED'
         ELSE 'TECHNICAL'
       END AS classification
FROM pilots p
JOIN compliance.requirements r USING (requirement_id)
LEFT JOIN mapping.phase3_requirement_capabilities m ON m.requirement_id=p.requirement_id AND m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
LEFT JOIN mapping.phase3_capabilities c USING (capability_id)
LEFT JOIN mapping.phase3_standards s USING (standard_id)
LEFT JOIN mapping.phase3_automatability a USING (mapping_id)
LEFT JOIN source_refs sr USING (capability_id)
LEFT JOIN mapping.phase3_exceptions e ON e.requirement_id=p.requirement_id AND e.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
ORDER BY p.requirement_id,c.capability_id,sr.source_reference;
