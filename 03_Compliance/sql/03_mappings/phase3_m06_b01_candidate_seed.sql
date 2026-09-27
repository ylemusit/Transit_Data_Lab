-- M06-B01 candidate-only seed. Adds three unreviewed non-technical paths.
-- No capability, mapping, automatability, coverage, evidence, or audit rows are created.
BEGIN TRANSACTION;

CREATE TEMP TABLE _m06_b01_expected_exceptions AS
SELECT * FROM (VALUES
    ('M06-B01-EXC-A03-P01-001','EU-2017-1926-REQ-A03-P01-001','LEGAL_PROCESS',
     'Establishing the national access point is assigned to a Member State and is not represented by the existing transport-format capabilities.',
     'The materialized requirement describes an institutional act. No current capability establishes the existence or legal establishment of a national access point.',
     'Authoritative institutional record identifying the national access point and the responsible Member State; evidence provenance and effective date.'),
    ('M06-B01-EXC-A03-P01-002','EU-2017-1926-REQ-A03-P01-002','ORGANIZATIONAL',
     'The single-access-point role concerns institutional scope and organization; existing format capabilities do not establish that role.',
     'The materialized requirement defines a point serving as the single access point for covered categories and data holders. No current technical capability establishes that organizational arrangement.',
     'Authoritative institutional description of the designated access point, its scope, and the categories and data holders it covers.'),
    ('M06-B01-EXC-A03-P03-001','EU-2017-1926-REQ-A03-P03-001','MANUAL_ASSESSMENT',
     'The materialized term location services does not specify a technical mechanism, interface, or machine-readable representation.',
     'No existing catalog capability contributes a demonstrated semantic mapping. The operational meaning of location services remains unresolved; do not infer a transport format or NAP mechanism.',
     'Targeted authoritative evidence defining the expected location-service behavior, interface, users, and any applicable technical specification; separately, evidence of the NAP service and its operation.')
) AS t(exception_id,requirement_id,exception_type,reason,justification,evidence_expectations);

-- Refuse to overwrite or silently accept an incompatible prior B01 exception.
SELECT CASE WHEN NOT EXISTS (
    SELECT 1 FROM mapping.phase3_exceptions e
    JOIN _m06_b01_expected_exceptions x USING (exception_id)
    WHERE e.requirement_id IS DISTINCT FROM x.requirement_id
       OR e.exception_type IS DISTINCT FROM x.exception_type
       OR e.reason IS DISTINCT FROM x.reason
       OR e.justification IS DISTINCT FROM x.justification
       OR e.evidence_expectations IS DISTINCT FROM x.evidence_expectations
       OR e.review_status IS DISTINCT FROM 'NEEDS_REVIEW'
       OR e.fixture_kind IS NOT NULL
) THEN TRUE ELSE error('M06-B01 incompatible preexisting exception state') END;

INSERT INTO mapping.phase3_exceptions
    (exception_id,requirement_id,exception_type,reason,justification,evidence_expectations,review_status,fixture_kind)
SELECT x.exception_id,x.requirement_id,x.exception_type,x.reason,x.justification,x.evidence_expectations,'NEEDS_REVIEW',NULL
FROM _m06_b01_expected_exceptions x
WHERE NOT EXISTS (SELECT 1 FROM mapping.phase3_exceptions e WHERE e.exception_id=x.exception_id);

SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_exceptions e JOIN _m06_b01_expected_exceptions x USING(exception_id))=3
    THEN TRUE ELSE error('M06-B01 exception seed did not produce exactly three rows') END;
COMMIT;
