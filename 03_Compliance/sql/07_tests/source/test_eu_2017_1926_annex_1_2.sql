-- ============================================================
-- TRANSIT DATA LAB
-- SOURCE INTEGRITY TEST
--
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
-- ANNEX 1.2 - Level of service 2
-- ============================================================

CREATE OR REPLACE TEMP TABLE expected_annex_1_2
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);

INSERT INTO expected_annex_1_2 VALUES

('EU-2017-1926-ANNEX-1.2-A',     'ANNEX_GROUP',  '1.2(a)'),
('EU-2017-1926-ANNEX-1.2-A-I',   'DATA_ELEMENT', '1.2(a)(i)'),
('EU-2017-1926-ANNEX-1.2-A-II',  'DATA_ELEMENT', '1.2(a)(ii)'),
('EU-2017-1926-ANNEX-1.2-A-III', 'DATA_ELEMENT', '1.2(a)(iii)'),
('EU-2017-1926-ANNEX-1.2-A-IV',  'DATA_ELEMENT', '1.2(a)(iv)'),
('EU-2017-1926-ANNEX-1.2-A-V',   'DATA_ELEMENT', '1.2(a)(v)'),
('EU-2017-1926-ANNEX-1.2-A-VI',  'DATA_ELEMENT', '1.2(a)(vi)'),
('EU-2017-1926-ANNEX-1.2-A-VII', 'DATA_ELEMENT', '1.2(a)(vii)'),

('EU-2017-1926-ANNEX-1.2-B',     'ANNEX_GROUP',  '1.2(b)'),
('EU-2017-1926-ANNEX-1.2-B-I',   'DATA_ELEMENT', '1.2(b)(i)'),
('EU-2017-1926-ANNEX-1.2-B-II',  'DATA_ELEMENT', '1.2(b)(ii)'),

('EU-2017-1926-ANNEX-1.2-C',     'ANNEX_GROUP',  '1.2(c)'),
('EU-2017-1926-ANNEX-1.2-C-I',   'DATA_ELEMENT', '1.2(c)(i)'),
('EU-2017-1926-ANNEX-1.2-C-II',  'DATA_ELEMENT', '1.2(c)(ii)');


CREATE OR REPLACE TEMP VIEW actual_annex_1_2 AS

SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.2-%';


-- ============================================================
-- TEST RESULTS
-- ============================================================

WITH test_results AS
(
    SELECT
        '01_EXPECTED_COUNT' AS test,
        14 AS expected,
        COUNT(*) AS actual
    FROM actual_annex_1_2

    UNION ALL

    SELECT
        '02_DATA_ELEMENT_COUNT',
        11,
        COUNT(*)
    FROM actual_annex_1_2
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT
        '03_GROUP_COUNT',
        3,
        COUNT(*)
    FROM actual_annex_1_2
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT
        '04_MISSING_PROVISIONS',
        0,
        COUNT(*)
    FROM
    (
        SELECT provision_id
        FROM expected_annex_1_2

        EXCEPT

        SELECT provision_id
        FROM actual_annex_1_2
    )

    UNION ALL

    SELECT
        '05_UNEXPECTED_PROVISIONS',
        0,
        COUNT(*)
    FROM
    (
        SELECT provision_id
        FROM actual_annex_1_2

        EXCEPT

        SELECT provision_id
        FROM expected_annex_1_2
    )

    UNION ALL

    SELECT
        '06_SECTION_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_1_2 e
    JOIN actual_annex_1_2 a
      ON e.provision_id = a.provision_id
    WHERE e.section <> a.section

    UNION ALL

    SELECT
        '07_TYPE_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_1_2 e
    JOIN actual_annex_1_2 a
      ON e.provision_id = a.provision_id
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT
        '08_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)
    FROM actual_annex_1_2
    WHERE source_reference IS NULL
),

evaluated AS
(
    SELECT
        test,
        expected,
        actual,

        CASE
            WHEN expected = actual
            THEN 'PASS'
            ELSE 'FAIL'
        END AS status

    FROM test_results
)

SELECT
    test,
    status,
    expected,
    actual
FROM evaluated
ORDER BY test;


SELECT
    'ANNEX_1_2_SOURCE_INTEGRITY' AS test,

    CASE
        WHEN
            (SELECT COUNT(*) FROM actual_annex_1_2) = 14

        AND (SELECT COUNT(*)
             FROM actual_annex_1_2
             WHERE provision_type = 'DATA_ELEMENT') = 11

        AND (SELECT COUNT(*)
             FROM actual_annex_1_2
             WHERE provision_type = 'ANNEX_GROUP') = 3

        AND (SELECT COUNT(*)
             FROM
             (
                 SELECT provision_id
                 FROM expected_annex_1_2

                 EXCEPT

                 SELECT provision_id
                 FROM actual_annex_1_2
             )) = 0

        AND (SELECT COUNT(*)
             FROM
             (
                 SELECT provision_id
                 FROM actual_annex_1_2

                 EXCEPT

                 SELECT provision_id
                 FROM expected_annex_1_2
             )) = 0

        AND (SELECT COUNT(*)
             FROM expected_annex_1_2 e
             JOIN actual_annex_1_2 a
               ON e.provision_id = a.provision_id
             WHERE e.section <> a.section) = 0

        AND (SELECT COUNT(*)
             FROM expected_annex_1_2 e
             JOIN actual_annex_1_2 a
               ON e.provision_id = a.provision_id
             WHERE e.provision_type <> a.provision_type) = 0

        AND (SELECT COUNT(*)
             FROM actual_annex_1_2
             WHERE source_reference IS NULL) = 0

        THEN 'PASS'
        ELSE 'FAIL'
    END AS status;
