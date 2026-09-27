-- Global inventory of substantive Phase 3 exceptions.
-- A future controlled batch must validate its own rows locally and add its exact
-- exception IDs, requirement IDs, and types here; historical validators stay local.
WITH recognized(exception_id,requirement_id,exception_type,baseline) AS (
    VALUES
      ('M03-EXC-A05-DEADLINE','EU-2017-1926-REQ-A05-P03-001','DEADLINE','M04'),
      ('M03-EXC-A08-SOURCE-REQUEST','EU-2017-1926-REQ-A08-P03-001-01','EXTERNAL_EVIDENCE','M04'),
      ('M03-EXC-A09-RANDOM-CHECKS','EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS','MANUAL_ASSESSMENT','M04'),
      ('M06-B01-EXC-A03-P01-001','EU-2017-1926-REQ-A03-P01-001','LEGAL_PROCESS','M06-B01'),
      ('M06-B01-EXC-A03-P01-002','EU-2017-1926-REQ-A03-P01-002','ORGANIZATIONAL','M06-B01'),
      ('M06-B01-EXC-A03-P03-001','EU-2017-1926-REQ-A03-P03-001','MANUAL_ASSESSMENT','M06-B01')
), substantive AS (
    SELECT exception_id,requirement_id,exception_type,review_status,fixture_kind
    FROM mapping.phase3_exceptions
    WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
), accounting AS (
    SELECT
      (SELECT count(*) FROM substantive a LEFT JOIN recognized r USING(exception_id)
       WHERE r.exception_id IS NULL) AS unaccounted_substantive_exceptions,
      (SELECT count(*) FROM recognized r LEFT JOIN substantive a USING(exception_id)
       WHERE a.exception_id IS NULL OR a.requirement_id IS DISTINCT FROM r.requirement_id
          OR a.exception_type IS DISTINCT FROM r.exception_type) AS missing_or_incompatible_recognized_exceptions,
      (SELECT count(*) FROM recognized WHERE baseline='M04') AS m04_expected_exceptions,
      (SELECT count(*) FROM recognized WHERE baseline='M06-B01') AS b01_expected_exceptions
)
SELECT CASE WHEN unaccounted_substantive_exceptions=0 AND missing_or_incompatible_recognized_exceptions=0
                 AND m04_expected_exceptions=3 AND b01_expected_exceptions=3
            THEN 'PASS' ELSE 'FAIL' END AS global_exception_accounting,
       m04_expected_exceptions,b01_expected_exceptions,
       unaccounted_substantive_exceptions,missing_or_incompatible_recognized_exceptions
FROM accounting;
