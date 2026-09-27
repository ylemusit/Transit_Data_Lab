-- M04B: separate semantic mapping review from persisted requirement coverage.
-- Additive, idempotent, and guarded to the five reviewed M04 pilot proposals.
BEGIN TRANSACTION;

SELECT CASE WHEN
    (SELECT count(*) FROM compliance.requirements)=48 AND
    (SELECT count(*) FROM compliance.deadlines)=10 AND
    (SELECT count(*) FROM compliance.requirement_candidates)=34 AND
    (SELECT count(*) FROM compliance.source_facts)=36 AND
    (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=5 AND
    (SELECT count(*) FROM mapping.phase3_automatability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=5 AND
    (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0 AND
    (SELECT count(*) FROM audit.rules)=0
THEN 'M04B_PREFLIGHT_PASS' ELSE error('M04B preflight state mismatch') END;

CREATE TABLE IF NOT EXISTS mapping.phase3_mapping_reviews (
    mapping_id VARCHAR PRIMARY KEY REFERENCES mapping.phase3_requirement_capabilities(mapping_id),
    semantic_review_outcome VARCHAR NOT NULL CHECK (semantic_review_outcome IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS','REJECTED','UNRESOLVED')),
    justification VARCHAR NOT NULL,
    limitations VARCHAR,
    reviewed_by VARCHAR NOT NULL,
    reviewed_at DATE NOT NULL,
    CHECK (semantic_review_outcome <> 'ACCEPTED_WITH_LIMITATIONS' OR length(trim(coalesce(limitations,''))) > 0)
);

CREATE TABLE IF NOT EXISTS mapping.phase3_requirement_coverage (
    coverage_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR NOT NULL UNIQUE,
    coverage_state VARCHAR NOT NULL CHECK (coverage_state IN ('ESTABLISHED','PARTIAL','UNRESOLVED','NOT_APPLICABLE','NONE_IDENTIFIED')),
    semantic_review_outcome VARCHAR NOT NULL CHECK (semantic_review_outcome IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS','REJECTED','UNRESOLVED')),
    justification VARCHAR NOT NULL,
    limitations VARCHAR,
    identified_paths VARCHAR NOT NULL,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('REVIEWED','NEEDS_REVIEW')),
    reviewed_by VARCHAR NOT NULL,
    reviewed_at DATE NOT NULL,
    reviewed_against_baseline VARCHAR NOT NULL,
    CHECK (coverage_state <> 'PARTIAL' OR length(trim(coalesce(limitations,''))) > 0),
    CHECK (coverage_state <> 'UNRESOLVED' OR semantic_review_outcome='UNRESOLVED'),
    CHECK (coverage_state <> 'NOT_APPLICABLE' OR semantic_review_outcome IN ('ACCEPTED','ACCEPTED_WITH_LIMITATIONS')),
    CHECK (coverage_state <> 'NONE_IDENTIFIED' OR semantic_review_outcome IN ('ACCEPTED_WITH_LIMITATIONS','UNRESOLVED')),
    CHECK (semantic_review_outcome <> 'ACCEPTED_WITH_LIMITATIONS' OR length(trim(coalesce(limitations,''))) > 0)
);

INSERT INTO mapping.phase3_vocabularies(vocabulary,value,description) VALUES
('SEMANTIC_REVIEW_OUTCOME','ACCEPTED','Human reviewer accepts the semantic validity of the specific mapping or coverage decision.'),
('SEMANTIC_REVIEW_OUTCOME','ACCEPTED_WITH_LIMITATIONS','Human reviewer accepts with explicit limitations; this is not a legal compliance conclusion.'),
('SEMANTIC_REVIEW_OUTCOME','REJECTED','Human reviewer rejects the semantic validity of the specific mapping or coverage decision.'),
('SEMANTIC_REVIEW_OUTCOME','UNRESOLVED','Human reviewer cannot resolve the semantic question with current scope or evidence.'),
('REQUIREMENT_COVERAGE','ESTABLISHED','Reviewed evidence paths cover the modeled proposal to the extent explicitly stated; never means legal compliance.'),
('REQUIREMENT_COVERAGE','PARTIAL','Reviewed evidence paths cover only part of the modeled proposal; limitations are required.'),
('REQUIREMENT_COVERAGE','UNRESOLVED','Coverage cannot be determined for the current scope; unresolved questions remain explicit.'),
('REQUIREMENT_COVERAGE','NOT_APPLICABLE','Coverage does not apply to this requirement in the reviewed scope.'),
('REQUIREMENT_COVERAGE','NONE_IDENTIFIED','No coverage path was identified after review; distinct from an unresolved assessment.')
ON CONFLICT DO NOTHING;

SELECT CASE WHEN
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE mapping_id IN (
 'M04-MAP-A04P01-GTFS-TRIP-STOP','M04-MAP-A04P01-NETEX-PT','M04-MAP-A04P02-NETEX-PT',
 'M04-MAP-A08P03-GTFS-PUBLISHER','M04-MAP-A08P03-GTFS-ATTRIBUTION'))=5 AND
 (SELECT count(*) FROM mapping.phase3_exceptions WHERE exception_id IN ('M03-EXC-A05-DEADLINE','M03-EXC-A08-SOURCE-REQUEST','M03-EXC-A09-RANDOM-CHECKS'))=3
THEN 'M04B_PILOT_PATHS_PASS' ELSE error('M04B pilot relationships or procedural paths missing') END;

COMMIT;
