-- ============================================================
-- STRUCTURAL INTEGRITY TEST
-- EU 2017/1926 - ANNEX 2.1
-- ============================================================

CREATE OR REPLACE TEMP TABLE expected_annex_2_1
(
    provision_id   VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section        VARCHAR NOT NULL
);

INSERT INTO expected_annex_2_1 VALUES

(
    'EU-2017-1926-ANNEX-2.1-I',
    'DATA_ELEMENT',
    '2.1(i)'
),

(
    'EU-2017-1926-ANNEX-2.1-II',
    'DATA_ELEMENT',
    '2.1(ii)'
),

(
    'EU-2017-1926-ANNEX-2.1-III',
    'DATA_ELEMENT',
    '2.1(iii)'
);


CREATE OR REPLACE TEMP VIEW actual_annex_2_1 AS

SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-2.1-%';


-- ============================================================
-- INDIVIDUAL TESTS
-- ============================================================

WITH test_results AS
(
    SELECT
        '01_EXPECTED_COUNT' AS test,
        3 AS expected,
        COUNT(*) AS actual
    FROM actual_annex_2_1

    UNION ALL

    SELECT
        '02_DATA_ELEMENT_COUNT',
        3,
        COUNT(*)
    FROM actual_annex_2_1
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT
        '03_GROUP_COUNT',
        0,
        COUNT(*)
    FROM actual_annex_2_1
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT
        '04_MISSING_PROVISIONS',
        0,
        COUNT(*)
    FROM
    (
        SELECT provision_id
        FROM expected_annex_2_1

        EXCEPT

        SELECT provision_id
        FROM actual_annex_2_1
    )

    UNION ALL

    SELECT
        '05_UNEXPECTED_PROVISIONS',
        0,
        COUNT(*)
    FROM
    (
        SELECT provision_id
        FROM actual_annex_2_1

        EXCEPT

        SELECT provision_id
        FROM expected_annex_2_1
    )

    UNION ALL

    SELECT
        '06_SECTION_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_2_1 e
    JOIN actual_annex_2_1 a
      USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT
        '07_TYPE_MISMATCH',
        0,
        COUNT(*)
    FROM expected_annex_2_1 e
    JOIN actual_annex_2_1 a
      USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT
        '08_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)
    FROM actual_annex_2_1
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
-- GLOBAL RESULT
-- ============================================================

WITH checks AS
(
    SELECT 3 expected, COUNT(*) actual
    FROM actual_annex_2_1

    UNION ALL

    SELECT 3, COUNT(*)
    FROM actual_annex_2_1
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_2_1
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM
    (
        SELECT provision_id FROM expected_annex_2_1
        EXCEPT
        SELECT provision_id FROM actual_annex_2_1
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM
    (
        SELECT provision_id FROM actual_annex_2_1
        EXCEPT
        SELECT provision_id FROM expected_annex_2_1
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_2_1 e
    JOIN actual_annex_2_1 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_2_1 e
    JOIN actual_annex_2_1 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_2_1
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_2_1_SOURCE_INTEGRITY' AS test,

    CASE
        WHEN COUNT(*) FILTER (
            WHERE expected <> actual
        ) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM checks;
