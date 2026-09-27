-- ============================================================
-- SOURCE INTEGRITY TEST
-- EU 2017/1926 - ANNEX 2.3
-- ============================================================


-- ------------------------------------------------------------
-- Individual tests
-- ------------------------------------------------------------

WITH test_results AS
(
    -- Exactly one legal node for 2.3
    SELECT
        '01_LEVEL_COUNT' AS test,
        1 AS expected,
        COUNT(*) AS actual
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND document_id = 'EU-REG-2017-1926'

    UNION ALL

    -- Must remain ANNEX_LEVEL
    SELECT
        '02_LEVEL_TYPE',
        1,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND provision_type = 'ANNEX_LEVEL'

    UNION ALL

    -- No artificial children
    SELECT
        '03_CHILD_COUNT',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND section LIKE '2.3(%'

    UNION ALL

    -- No artificial DATA_ELEMENT children
    SELECT
        '04_DATA_ELEMENT_CHILD_COUNT',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND section LIKE '2.3(%'
      AND provision_type = 'DATA_ELEMENT'

    UNION ALL

    -- Source reference required
    SELECT
        '05_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND source_reference IS NULL

    UNION ALL

    -- Semantic content required
    SELECT
        '06_TEXT_CONTENT_NULL',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND (
            text_content IS NULL
            OR TRIM(text_content) = ''
          )

    UNION ALL

    -- Correct legal section
    SELECT
        '07_SECTION_MISMATCH',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND section <> '2.3'

    UNION ALL

    -- No synthetic 2.3 provision IDs
    SELECT
        '08_SYNTHETIC_CHILD_IDS',
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_id LIKE 'EU-2017-1926-ANNEX-2.3-%'
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
    SELECT
        1 AS expected,
        COUNT(*) AS actual
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND document_id = 'EU-REG-2017-1926'

    UNION ALL

    SELECT
        1,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND provision_type = 'ANNEX_LEVEL'

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND section LIKE '2.3(%'

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND section LIKE '2.3(%'
      AND provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND source_reference IS NULL

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND (
            text_content IS NULL
            OR TRIM(text_content) = ''
          )

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND section <> '2.3'

    UNION ALL

    SELECT
        0,
        COUNT(*)
    FROM source.provisions
    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_id LIKE 'EU-2017-1926-ANNEX-2.3-%'
)

SELECT
    'ANNEX_2_3_SOURCE_INTEGRITY' AS test,

    CASE
        WHEN COUNT(*) FILTER (
            WHERE expected <> actual
        ) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM checks;
