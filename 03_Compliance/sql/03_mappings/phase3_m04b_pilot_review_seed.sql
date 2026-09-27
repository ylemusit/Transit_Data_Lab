-- Persist the human M04 semantic decisions. Workflow review_status on M04 mappings
-- remains unchanged; this seed records the distinct semantic decisions idempotently.
BEGIN TRANSACTION;

INSERT INTO mapping.phase3_mapping_reviews
(mapping_id,semantic_review_outcome,justification,limitations,reviewed_by,reviewed_at)
VALUES
('M04-MAP-A04P01-GTFS-TRIP-STOP','ACCEPTED','Valid semantic relationship for scheduled trip and stop time concepts.','Does not establish all Annex point-1 coverage, historical/observed data, all modes, NAP access/publication, or legal compliance.','Yeison Arbey Carrillo Lemus',DATE '2026-09-27'),
('M04-MAP-A04P01-NETEX-PT','ACCEPTED','Valid semantic relationship for the evidenced NeTEx public transport network and timetable scope.','Available source is not the full normative profile; does not establish all Annex point-1 coverage, historical/observed data, NAP access/publication, or legal compliance.','Yeison Arbey Carrillo Lemus',DATE '2026-09-27'),
('M04-MAP-A04P02-NETEX-PT','ACCEPTED_WITH_LIMITATIONS','Valid bounded NeTEx relationship for existing network and timetable concepts.','Applicable minimum profile and category scope remain unresolved; no complete representability or legal compliance is asserted.','Yeison Arbey Carrillo Lemus',DATE '2026-09-27'),
('M04-MAP-A08P03-GTFS-PUBLISHER','ACCEPTED_WITH_LIMITATIONS','Valid bounded technical relationship for publisher identity/URL metadata where the conditional reuse context applies.','Publisher metadata does not establish each datum source, request/response handling, disclosure, or legal compliance.','Yeison Arbey Carrillo Lemus',DATE '2026-09-27'),
('M04-MAP-A08P03-GTFS-ATTRIBUTION','ACCEPTED_WITH_LIMITATIONS','Valid bounded technical relationship for GTFS attribution at dataset or related entity scope.','Attribution may not identify the legally relevant source for each reused datum and does not establish request/response handling, disclosure, or legal compliance.','Yeison Arbey Carrillo Lemus',DATE '2026-09-27')
ON CONFLICT (mapping_id) DO UPDATE SET
 semantic_review_outcome=excluded.semantic_review_outcome,justification=excluded.justification,
 limitations=excluded.limitations,reviewed_by=excluded.reviewed_by,reviewed_at=excluded.reviewed_at;

INSERT INTO mapping.phase3_requirement_coverage
(coverage_id,requirement_id,coverage_state,semantic_review_outcome,justification,limitations,identified_paths,review_status,reviewed_by,reviewed_at,reviewed_against_baseline)
VALUES
('M04B-COV-A04-P01','EU-2017-1926-REQ-A04-P01-001','PARTIAL','ACCEPTED_WITH_LIMITATIONS','Reviewed technical paths cover bounded scheduled network and timetable concepts.','Does not establish full Annex coverage, historical/observed data, NAP publication/access, or legal compliance.','MAPPING:M04-MAP-A04P01-GTFS-TRIP-STOP;MAPPING:M04-MAP-A04P01-NETEX-PT','REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M04_LOCAL_PILOT_MAPPING_SET_2026-09-27'),
('M04B-COV-A04-P02','EU-2017-1926-REQ-A04-P02-001','UNRESOLVED','UNRESOLVED','A bounded NeTEx relationship is identified, but applicable profile/category coverage cannot yet be resolved.','Applicable minimum profile and category scope remain unresolved; do not infer complete coverage or legal compliance.','MAPPING:M04-MAP-A04P02-NETEX-PT','REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M04_LOCAL_PILOT_MAPPING_SET_2026-09-27'),
('M04B-COV-A08-P03','EU-2017-1926-REQ-A08-P03-001-01','PARTIAL','ACCEPTED_WITH_LIMITATIONS','Hybrid technical and external evidence paths cover bounded publisher/attribution and request-context aspects.','Publisher metadata and attribution do not establish all provenance, request/response, disclosure, or reuse facts; no legal compliance is asserted.','MAPPING:M04-MAP-A08P03-GTFS-PUBLISHER;MAPPING:M04-MAP-A08P03-GTFS-ATTRIBUTION;EXCEPTION:M03-EXC-A08-SOURCE-REQUEST','REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M04_LOCAL_PILOT_MAPPING_SET_2026-09-27'),
('M04B-COV-A05-P03','EU-2017-1926-REQ-A05-P03-001','PARTIAL','ACCEPTED_WITH_LIMITATIONS','A reviewed deadline/procedural path is identified without manufacturing a technical mapping.','Calendar/feed date fields do not establish timely legal provision; dated NAP publication/access and applicable scope evidence remain necessary.','EXCEPTION:M03-EXC-A05-DEADLINE','REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M04_LOCAL_PILOT_MAPPING_SET_2026-09-27'),
('M04B-COV-A09-RANDOM-CHECKS','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS','PARTIAL','ACCEPTED_WITH_LIMITATIONS','A reviewed manual assessment path is identified without manufacturing a technical mapping.','Operational records, sampled declarations and corroboration are needed; the pilot does not define method, frequency, sample size, or legal compliance outcome.','EXCEPTION:M03-EXC-A09-RANDOM-CHECKS','REVIEWED','Yeison Arbey Carrillo Lemus',DATE '2026-09-27','M04_LOCAL_PILOT_MAPPING_SET_2026-09-27')
ON CONFLICT (requirement_id) DO UPDATE SET
 coverage_state=excluded.coverage_state,semantic_review_outcome=excluded.semantic_review_outcome,
 justification=excluded.justification,limitations=excluded.limitations,identified_paths=excluded.identified_paths,
 review_status=excluded.review_status,reviewed_by=excluded.reviewed_by,reviewed_at=excluded.reviewed_at,
 reviewed_against_baseline=excluded.reviewed_against_baseline;

COMMIT;
