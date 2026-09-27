-- ============================================================
-- STRUCTURAL INTEGRITY TEST
-- EU 2017/1926 - ANNEX 2.2
-- ============================================================

CREATE OR REPLACE TEMP TABLE expected_annex_2_2
(
    provision_id   VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section        VARCHAR NOT NULL
);

INSERT INTO expected_annex_2_2 VALUES

(
    'EU-2017-1926-ANNEX-2.2-A',
    'DATA_ELEMENT',
    '2.2(a)'
),

(
    'EU-2017-1926-ANNEX-2.2-B',
    'ANNEX_GROUP',
    '2.2(b)'
),

(
    'EU-2017-1926-ANNEX-2.2-B-I',
    'DATA_ELEMENT',
    '2.2(b)(i)'
),

(
    'EU-2017-1926-ANNEX-2.2-B-II',
    'DATA_ELEMENT',
    '2.2(b)(ii)'
);


CREATE OR REPLACE TEMP VIEW actual_annex_2_2 AS

SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-2.2-%';


-- ============================================================
-- INDIVIDUAL TESTS
-- ============================================================

WITH test_results AS
(
    SELECT
        '01_EXPECTED_COUNT' AS test,
        4 AS expected,
        COUNT(*) AS actual
    FROM actual_annex_2_2

    UNION ALL

    SELECT
        '02_DATA_ELEMENT_COUNT',
        3,
        COUNT(*)
    FROM actual_annex_2_2
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT
        '03_GROUP_COUNT',
        1,
        COUNT(*)
    FROM actual_annex_2_2
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT
        '04_MISSING_PROVISIONS',
        0,
        COUNT(*)
    FROM (
        SELECT provision_id
        FROM expected_annex_2_2

        EXCEPT

        SELECT provision_id
        FROM actual_annex_2_2
    )

    UNION ALL

    SELECT
        '05_UNEXPECTED_PROVISIONS',
        0,
        COUNT(*)
    FROM (
        SELECT provision_id
        FROM actual_annex_2_2

        EXCEPT

        SELECT provision_id
        FROM expected_annex_2_2
    )

    UNION ALL

    SELECT
        '06_SECTION_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_2_2 e
    JOIN actual_annex_2_2 a
      USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT
        '07_TYPE_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_2_2 e
    JOIN actual_annex_2_2 a
      USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT
        '08_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)
    FROM actual_annex_2_2
    WHERE source_reference IS NULL
),

evaluated AS
(
    SELECT
        test,
        CASE
            WHEN expected = actual THEN 'PASS'
            ELSE 'FAIL'
        END AS status,
        expected,
        actual
    FROM test_results
)

SELECT *
FROM evaluated
ORDER BY test;


-- ============================================================
-- GLOBAL TEST
-- ============================================================

WITH checks AS
(
    SELECT 4 expected, COUNT(*) actual
    FROM actual_annex_2_2

    UNION ALL

    SELECT 3, COUNT(*)
    FROM actual_annex_2_2
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 1, COUNT(*)
    FROM actual_annex_2_2
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_2_2
        EXCEPT
        SELECT provision_id FROM actual_annex_2_2
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_2_2
        EXCEPT
        SELECT provision_id FROM expected_annex_2_2
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_2_2 e
    JOIN actual_annex_2_2 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_2_2 e
    JOIN actual_annex_2_2 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_2_2
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_2_2_SOURCE_INTEGRITY' AS test,

    CASE
        WHEN COUNT(*) FILTER (
            WHERE expected <> actual
        ) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM checks;
