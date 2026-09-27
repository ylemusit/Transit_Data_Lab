-- ============================================================
-- TRANSIT DATA LAB
-- SOURCE INTEGRITY TEST
--
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
-- ANNEX 1.1 - Level of service 1
--
-- Expected structure verified against:
--   CELEX 02017R1926-20240304
--   Regulation (EU) 2024/490 Annex
-- ============================================================


-- ------------------------------------------------------------
-- OFFICIAL EXPECTED TERMINAL REFERENCES
-- ------------------------------------------------------------

CREATE OR REPLACE TEMP TABLE expected_annex_1_1
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);


INSERT INTO expected_annex_1_1 VALUES

('EU-2017-1926-ANNEX-1.1-A',     'ANNEX_GROUP',  '1.1(a)'),
('EU-2017-1926-ANNEX-1.1-A-I',   'DATA_ELEMENT', '1.1(a)(i)'),
('EU-2017-1926-ANNEX-1.1-A-II',  'DATA_ELEMENT', '1.1(a)(ii)'),
('EU-2017-1926-ANNEX-1.1-A-III', 'DATA_ELEMENT', '1.1(a)(iii)'),

('EU-2017-1926-ANNEX-1.1-B',     'DATA_ELEMENT', '1.1(b)'),

('EU-2017-1926-ANNEX-1.1-C',     'ANNEX_GROUP',  '1.1(c)'),
('EU-2017-1926-ANNEX-1.1-C-I',   'DATA_ELEMENT', '1.1(c)(i)'),
('EU-2017-1926-ANNEX-1.1-C-II',  'DATA_ELEMENT', '1.1(c)(ii)'),

('EU-2017-1926-ANNEX-1.1-D',      'ANNEX_GROUP',  '1.1(d)'),
('EU-2017-1926-ANNEX-1.1-D-I',    'DATA_ELEMENT', '1.1(d)(i)'),
('EU-2017-1926-ANNEX-1.1-D-II',   'DATA_ELEMENT', '1.1(d)(ii)'),
('EU-2017-1926-ANNEX-1.1-D-III',  'DATA_ELEMENT', '1.1(d)(iii)'),
('EU-2017-1926-ANNEX-1.1-D-IV',   'DATA_ELEMENT', '1.1(d)(iv)'),
('EU-2017-1926-ANNEX-1.1-D-V',    'DATA_ELEMENT', '1.1(d)(v)'),
('EU-2017-1926-ANNEX-1.1-D-VI',   'DATA_ELEMENT', '1.1(d)(vi)'),
('EU-2017-1926-ANNEX-1.1-D-VII',  'DATA_ELEMENT', '1.1(d)(vii)'),
('EU-2017-1926-ANNEX-1.1-D-VIII', 'DATA_ELEMENT', '1.1(d)(viii)'),
('EU-2017-1926-ANNEX-1.1-D-IX',   'DATA_ELEMENT', '1.1(d)(ix)'),
('EU-2017-1926-ANNEX-1.1-D-X',    'DATA_ELEMENT', '1.1(d)(x)'),
('EU-2017-1926-ANNEX-1.1-D-XI',   'DATA_ELEMENT', '1.1(d)(xi)'),

('EU-2017-1926-ANNEX-1.1-E',     'ANNEX_GROUP',  '1.1(e)'),
('EU-2017-1926-ANNEX-1.1-E-I',   'DATA_ELEMENT', '1.1(e)(i)'),
('EU-2017-1926-ANNEX-1.1-E-II',  'DATA_ELEMENT', '1.1(e)(ii)'),
('EU-2017-1926-ANNEX-1.1-E-III', 'DATA_ELEMENT', '1.1(e)(iii)');


-- ------------------------------------------------------------
-- ACTUAL DATA
-- ------------------------------------------------------------

CREATE OR REPLACE TEMP VIEW actual_annex_1_1 AS

SELECT
    provision_id,
    provision_type,
    section
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.1-%';


-- ------------------------------------------------------------
-- TEST 01 - EXPECTED COUNT
-- ------------------------------------------------------------

SELECT
    '01_EXPECTED_COUNT' AS test,

    CASE
        WHEN COUNT(*) = 24
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    24 AS expected,
    COUNT(*) AS actual

FROM actual_annex_1_1;


-- ------------------------------------------------------------
-- TEST 02 - DATA ELEMENT COUNT
-- ------------------------------------------------------------

SELECT
    '02_DATA_ELEMENT_COUNT' AS test,

    CASE
        WHEN COUNT(*) = 20
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    20 AS expected,
    COUNT(*) AS actual

FROM actual_annex_1_1

WHERE provision_type = 'DATA_ELEMENT';


-- ------------------------------------------------------------
-- TEST 03 - GROUP COUNT
-- ------------------------------------------------------------

SELECT
    '03_GROUP_COUNT' AS test,

    CASE
        WHEN COUNT(*) = 4
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    4 AS expected,
    COUNT(*) AS actual

FROM actual_annex_1_1

WHERE provision_type = 'ANNEX_GROUP';


-- ------------------------------------------------------------
-- TEST 04 - MISSING PROVISIONS
-- ------------------------------------------------------------

SELECT
    '04_MISSING_PROVISIONS' AS test,

    CASE
        WHEN COUNT(*) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    0 AS expected,
    COUNT(*) AS actual

FROM
(
    SELECT provision_id
    FROM expected_annex_1_1

    EXCEPT

    SELECT provision_id
    FROM actual_annex_1_1
);


-- ------------------------------------------------------------
-- TEST 05 - UNEXPECTED PROVISIONS
-- ------------------------------------------------------------

SELECT
    '05_UNEXPECTED_PROVISIONS' AS test,

    CASE
        WHEN COUNT(*) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    0 AS expected,
    COUNT(*) AS actual

FROM
(
    SELECT provision_id
    FROM actual_annex_1_1

    EXCEPT

    SELECT provision_id
    FROM expected_annex_1_1
);


-- ------------------------------------------------------------
-- TEST 06 - SECTION MATCH
-- ------------------------------------------------------------

SELECT
    '06_SECTION_MATCH' AS test,

    CASE
        WHEN COUNT(*) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    0 AS expected,
    COUNT(*) AS actual

FROM expected_annex_1_1 e

JOIN actual_annex_1_1 a
    ON e.provision_id = a.provision_id

WHERE e.section <> a.section;


-- ------------------------------------------------------------
-- TEST 07 - TYPE MATCH
-- ------------------------------------------------------------

SELECT
    '07_TYPE_MATCH' AS test,

    CASE
        WHEN COUNT(*) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    0 AS expected,
    COUNT(*) AS actual

FROM expected_annex_1_1 e

JOIN actual_annex_1_1 a
    ON e.provision_id = a.provision_id

WHERE e.provision_type <> a.provision_type;


-- ------------------------------------------------------------
-- TEST 08 - SOURCE REFERENCES
-- ------------------------------------------------------------

SELECT
    '08_SOURCE_REFERENCE_NOT_NULL' AS test,

    CASE
        WHEN COUNT(*) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status,

    0 AS expected,
    COUNT(*) AS actual

FROM source.provisions

WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.1-%'
  AND source_reference IS NULL;


-- ------------------------------------------------------------
-- FINAL SUMMARY
-- ------------------------------------------------------------

WITH tests AS
(
    SELECT
        (
            SELECT COUNT(*)
            FROM actual_annex_1_1
        ) = 24 AS t1,

        (
            SELECT COUNT(*)
            FROM actual_annex_1_1
            WHERE provision_type = 'DATA_ELEMENT'
        ) = 20 AS t2,

        (
            SELECT COUNT(*)
            FROM actual_annex_1_1
            WHERE provision_type = 'ANNEX_GROUP'
        ) = 4 AS t3,

        (
            SELECT COUNT(*)
            FROM
            (
                SELECT provision_id
                FROM expected_annex_1_1

                EXCEPT

                SELECT provision_id
                FROM actual_annex_1_1
            )
        ) = 0 AS t4,

        (
            SELECT COUNT(*)
            FROM
            (
                SELECT provision_id
                FROM actual_annex_1_1

                EXCEPT

                SELECT provision_id
                FROM expected_annex_1_1
            )
        ) = 0 AS t5,

        (
            SELECT COUNT(*)
            FROM expected_annex_1_1 e
            JOIN actual_annex_1_1 a
              ON e.provision_id = a.provision_id
            WHERE e.section <> a.section
        ) = 0 AS t6,

        (
            SELECT COUNT(*)
            FROM expected_annex_1_1 e
            JOIN actual_annex_1_1 a
              ON e.provision_id = a.provision_id
            WHERE e.provision_type <> a.provision_type
        ) = 0 AS t7,

        (
            SELECT COUNT(*)
            FROM source.provisions
            WHERE document_id = 'EU-REG-2017-1926'
              AND provision_id LIKE 'EU-2017-1926-ANNEX-1.1-%'
              AND source_reference IS NULL
        ) = 0 AS t8
)

SELECT
    'ANNEX_1_1_SOURCE_INTEGRITY' AS test,

    CASE
        WHEN t1 AND t2 AND t3 AND t4
         AND t5 AND t6 AND t7 AND t8
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM tests;
