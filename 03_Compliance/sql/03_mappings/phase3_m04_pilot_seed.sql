-- M04 candidate mappings for the five explicitly scoped pilot atomic proposals.
-- Idempotent; preserves Phase 1/2, observed evidence, representability and audit rules.
BEGIN TRANSACTION;

SELECT CASE WHEN
    (SELECT count(*) FROM compliance.requirements) = 48
    AND (SELECT count(*) FROM compliance.deadlines) = 10
    AND (SELECT count(*) FROM compliance.requirement_candidates) = 34
    AND (SELECT count(*) FROM compliance.source_facts) = 36
    AND (SELECT count(*) FROM audit.rules) = 0
    AND (SELECT count(*) FROM mapping.phase3_standards) = 3
    AND (SELECT count(*) FROM mapping.phase3_capabilities) = 5
    AND (SELECT count(*) FROM mapping.phase3_source_references) = 7
    AND (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') = 3
    AND (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND requirement_id NOT IN (
      'EU-2017-1926-REQ-A04-P01-001', 'EU-2017-1926-REQ-A04-P02-001',
      'EU-2017-1926-REQ-A08-P03-001-01', 'EU-2017-1926-REQ-A05-P03-001',
      'EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS')) = 0
    AND (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND review_status IN ('APPROVED','REVIEWED')) = 0
THEN 'M04_PREFLIGHT_PASS' ELSE error('M04 preflight guard failed; no pilot seed was applied') END;

INSERT INTO mapping.phase3_requirement_capabilities
(mapping_id,requirement_id,capability_id,mapping_type,mapping_conditions,limitations,review_status)
VALUES
('M04-MAP-A04P01-GTFS-TRIP-STOP','EU-2017-1926-REQ-A04-P01-001','CAP-GTFS-SCHEDULE-TRIP-STOP-TIMES','PARTIAL',
 'Candidate relation limited to scheduled public transport concepts; the pilot proposal also covers historical and observed data.',
 'Does not establish Annex point-1 coverage, historical/observed data representation, all modes, NAP access/publication, or legal compliance.', 'NEEDS_REVIEW'),
('M04-MAP-A04P01-NETEX-PT','EU-2017-1926-REQ-A04-P01-001','CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE','PARTIAL',
 'Candidate relation limited to the public transport network and scheduled timetable concepts described by existing public scope evidence.',
 'The available source is not the full normative profile; it does not establish complete Annex point-1 coverage, historical/observed data, NAP access/publication, or legal compliance.', 'NEEDS_REVIEW'),
('M04-MAP-A04P02-NETEX-PT','EU-2017-1926-REQ-A04-P02-001','CAP-NETEX-PT-NETWORK-TIMETABLE-EXCHANGE','PARTIAL',
 'Candidate technical relation only for the existing NeTEx network/timetable scope; the applicable minimum profile and category scope remain unresolved.',
 'Does not establish complete representability, final mapping approval, the applicable Spanish NeTEx profile, DATEX II scope, or legal compliance.', 'NEEDS_REVIEW'),
('M04-MAP-A08P03-GTFS-PUBLISHER','EU-2017-1926-REQ-A08-P03-001-01','CAP-GTFS-FEED-PUBLISHER-METADATA','PARTIAL',
 'Only a candidate metadata relationship for publisher identity/URL when the conditional reuse and request context applies.',
 'Publisher metadata does not necessarily identify the source of each reused datum and does not prove a request, response, or disclosure to the requester.', 'NEEDS_REVIEW'),
('M04-MAP-A08P03-GTFS-ATTRIBUTION','EU-2017-1926-REQ-A08-P03-001-01','CAP-GTFS-DATASET-ATTRIBUTION','PARTIAL',
 'Attribution records can provide technical source-related metadata at dataset, agency, route, or trip scope, subject to the conditional request context.',
 'Attribution may not identify the legally relevant source for each reused datum and does not prove request handling or disclosure to the requester.', 'NEEDS_REVIEW')
ON CONFLICT (requirement_id,capability_id) DO NOTHING;

INSERT INTO mapping.phase3_automatability
(automatability_id,mapping_id,automatability_state,explanation,prerequisites,assessed_on,review_status)
SELECT 'M04-AUTO-' || m.mapping_id, m.mapping_id,
       'PARTIAL',
       CASE WHEN m.requirement_id='EU-2017-1926-REQ-A08-P03-001-01'
            THEN 'Only the bounded technical metadata relationship may be machine-inspected; conditional reuse, request, provenance, response and disclosure require external evidence.'
            ELSE 'A future machine check could inspect the bounded technical representation only; scope and legal availability/access require other evidence.' END,
       CASE WHEN m.requirement_id='EU-2017-1926-REQ-A08-P03-001-01'
            THEN 'Observed dataset plus linked reuse context, request and response/disclosure records; none are established by this M04 mapping.'
            ELSE 'Observed dataset and defined legal/category scope; M04 does not establish either.' END,
       DATE '2026-09-27','NEEDS_REVIEW'
FROM mapping.phase3_requirement_capabilities m
WHERE m.mapping_id IN ('M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT','M04-MAP-A08P03-GTFS-PUBLISHER','M04-MAP-A08P03-GTFS-ATTRIBUTION')
ON CONFLICT (automatability_id) DO NOTHING;

COMMIT;
