$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926
# MASTER STRUCTURE INTEGRITY TEST
#
# Corpus baseline:
# Consolidated version 04/03/2024
#
# READ-ONLY TEST
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_master_structure.sql"

New-Item -ItemType Directory -Force -Path $TestDir | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null


Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - MASTER STRUCTURE INTEGRITY TEST" -ForegroundColor Cyan
Write-Host " Consolidated version: 04/03/2024" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan


# ============================================================
# CREATE MASTER TEST
# ============================================================

@'
-- ============================================================
-- TRANSIT DATA LAB
--
-- EU 2017/1926
-- MASTER STRUCTURE INTEGRITY TEST
--
-- Reference corpus:
-- Consolidated version 04/03/2024
--
-- IMPORTANT:
--
-- This test certifies STRUCTURAL integrity only.
--
-- It does NOT certify:
--   - literal textual fidelity
--   - legal interpretation
--   - legal compliance
--   - completeness of derived requirements
--
-- ============================================================


-- ============================================================
-- EXPECTED ANNEX LEVELS
-- ============================================================

CREATE OR REPLACE TEMP TABLE expected_annex_levels
(
    provision_id VARCHAR PRIMARY KEY,
    section      VARCHAR NOT NULL
);

INSERT INTO expected_annex_levels VALUES
('EU-2017-1926-ANNEX-1.1', '1.1'),
('EU-2017-1926-ANNEX-1.2', '1.2'),
('EU-2017-1926-ANNEX-1.3', '1.3'),
('EU-2017-1926-ANNEX-1.4', '1.4'),
('EU-2017-1926-ANNEX-2.1', '2.1'),
('EU-2017-1926-ANNEX-2.2', '2.2'),
('EU-2017-1926-ANNEX-2.3', '2.3');


-- ============================================================
-- EXPECTED CHILD CARDINALITY
-- ============================================================

CREATE OR REPLACE TEMP TABLE expected_level_counts
(
    level         VARCHAR PRIMARY KEY,
    child_records INTEGER NOT NULL,
    groups        INTEGER NOT NULL,
    data_elements INTEGER NOT NULL
);

INSERT INTO expected_level_counts VALUES

('1.1', 24, 4, 20),
('1.2', 14, 3, 11),
('1.3', 14, 4, 10),
('1.4', 12, 2, 10),

('2.1',  3, 0,  3),
('2.2',  4, 1,  3),

-- 2.3 is a terminal ANNEX_LEVEL.
-- It contains its semantic content directly.
('2.3',  0, 0,  0);


-- ============================================================
-- ACTUAL CHILD COUNTS
-- ============================================================

CREATE OR REPLACE TEMP VIEW actual_level_counts AS

SELECT
    e.level,

    COUNT(p.provision_id) FILTER (
        WHERE p.provision_type IN (
            'ANNEX_GROUP',
            'DATA_ELEMENT'
        )
    ) AS child_records,

    COUNT(p.provision_id) FILTER (
        WHERE p.provision_type = 'ANNEX_GROUP'
    ) AS groups,

    COUNT(p.provision_id) FILTER (
        WHERE p.provision_type = 'DATA_ELEMENT'
    ) AS data_elements

FROM expected_level_counts e

LEFT JOIN source.provisions p
  ON p.document_id = 'EU-REG-2017-1926'
 AND p.section LIKE e.level || '(%'

GROUP BY e.level;


-- ============================================================
-- MASTER TESTS
-- ============================================================

WITH test_results AS
(

    -- --------------------------------------------------------
    -- DOCUMENT
    -- --------------------------------------------------------

    SELECT
        '01_DOCUMENT_EXISTS' AS test,
        1 AS expected,
        COUNT(*) AS actual

    FROM source.documents

    WHERE document_id = 'EU-REG-2017-1926'


    UNION ALL


    -- --------------------------------------------------------
    -- TOTAL DOCUMENT PROVISIONS
    -- Current frozen baseline = 92
    -- --------------------------------------------------------

    SELECT
        '02_TOTAL_DOCUMENT_PROVISIONS',
        92,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'


    UNION ALL


    -- --------------------------------------------------------
    -- ARTICLES
    -- --------------------------------------------------------

    SELECT
        '03_ARTICLE_COUNT',
        11,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ARTICLE'


    UNION ALL


    -- --------------------------------------------------------
    -- ANNEX ROOT
    -- --------------------------------------------------------

    SELECT
        '04_ANNEX_ROOT_COUNT',
        1,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX'


    UNION ALL


    -- --------------------------------------------------------
    -- ANNEX SECTIONS
    -- Expected:
    --   1
    --   2
    -- --------------------------------------------------------

    SELECT
        '05_ANNEX_SECTION_COUNT',
        2,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX_SECTION'


    UNION ALL


    -- --------------------------------------------------------
    -- ANNEX LEVELS
    -- --------------------------------------------------------

    SELECT
        '06_ANNEX_LEVEL_COUNT',
        7,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX_LEVEL'


    UNION ALL


    -- --------------------------------------------------------
    -- MISSING EXPECTED LEVELS
    -- --------------------------------------------------------

    SELECT
        '07_MISSING_ANNEX_LEVELS',
        0,
        COUNT(*)

    FROM
    (
        SELECT provision_id
        FROM expected_annex_levels

        EXCEPT

        SELECT provision_id
        FROM source.provisions
        WHERE document_id = 'EU-REG-2017-1926'
          AND provision_type = 'ANNEX_LEVEL'
    )


    UNION ALL


    -- --------------------------------------------------------
    -- UNEXPECTED ANNEX LEVELS
    -- --------------------------------------------------------

    SELECT
        '08_UNEXPECTED_ANNEX_LEVELS',
        0,
        COUNT(*)

    FROM
    (
        SELECT provision_id
        FROM source.provisions
        WHERE document_id = 'EU-REG-2017-1926'
          AND provision_type = 'ANNEX_LEVEL'

        EXCEPT

        SELECT provision_id
        FROM expected_annex_levels
    )


    UNION ALL


    -- --------------------------------------------------------
    -- LEVEL SECTION MISMATCH
    -- --------------------------------------------------------

    SELECT
        '09_ANNEX_LEVEL_SECTION_MISMATCH',
        0,
        COUNT(*)

    FROM expected_annex_levels e

    JOIN source.provisions p
      USING (provision_id)

    WHERE e.section <> p.section


    UNION ALL


    -- --------------------------------------------------------
    -- CHILD CARDINALITY MISMATCH
    -- --------------------------------------------------------

    SELECT
        '10_LEVEL_CHILD_COUNT_MISMATCH',
        0,
        COUNT(*)

    FROM expected_level_counts e

    JOIN actual_level_counts a
      USING (level)

    WHERE e.child_records <> a.child_records


    UNION ALL


    -- --------------------------------------------------------
    -- GROUP CARDINALITY MISMATCH
    -- --------------------------------------------------------

    SELECT
        '11_LEVEL_GROUP_COUNT_MISMATCH',
        0,
        COUNT(*)

    FROM expected_level_counts e

    JOIN actual_level_counts a
      USING (level)

    WHERE e.groups <> a.groups


    UNION ALL


    -- --------------------------------------------------------
    -- DATA ELEMENT CARDINALITY MISMATCH
    -- --------------------------------------------------------

    SELECT
        '12_LEVEL_DATA_ELEMENT_COUNT_MISMATCH',
        0,
        COUNT(*)

    FROM expected_level_counts e

    JOIN actual_level_counts a
      USING (level)

    WHERE e.data_elements <> a.data_elements


    UNION ALL


    -- --------------------------------------------------------
    -- TOTAL ANNEX GROUPS
    --
    -- 1.1 = 4
    -- 1.2 = 3
    -- 1.3 = 4
    -- 1.4 = 2
    -- 2.1 = 0
    -- 2.2 = 1
    -- 2.3 = 0
    --
    -- TOTAL = 14
    -- --------------------------------------------------------

    SELECT
        '13_TOTAL_ANNEX_GROUPS',
        14,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX_GROUP'


    UNION ALL


    -- --------------------------------------------------------
    -- TOTAL DATA ELEMENTS
    --
    -- 20 + 11 + 10 + 10 + 3 + 3 = 57
    -- --------------------------------------------------------

    SELECT
        '14_TOTAL_DATA_ELEMENTS',
        57,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'DATA_ELEMENT'


    UNION ALL


    -- --------------------------------------------------------
    -- NULL SOURCE REFERENCES IN STRUCTURED ANNEX
    -- --------------------------------------------------------

    SELECT
        '15_ANNEX_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type IN (
          'ANNEX',
          'ANNEX_SECTION',
          'ANNEX_LEVEL',
          'ANNEX_GROUP',
          'DATA_ELEMENT'
      )

      AND (
          source_reference IS NULL
          OR TRIM(source_reference) = ''
      )


    UNION ALL


    -- --------------------------------------------------------
    -- NULL HEADINGS IN STRUCTURED ANNEX
    -- --------------------------------------------------------

    SELECT
        '16_ANNEX_HEADING_NULL',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type IN (
          'ANNEX',
          'ANNEX_SECTION',
          'ANNEX_LEVEL',
          'ANNEX_GROUP',
          'DATA_ELEMENT'
      )

      AND (
          heading IS NULL
          OR TRIM(heading) = ''
      )


    UNION ALL


    -- --------------------------------------------------------
    -- TERMINAL DATA ELEMENTS MUST HAVE SEMANTIC CONTENT
    -- --------------------------------------------------------

    SELECT
        '17_DATA_ELEMENT_TEXT_NULL',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'DATA_ELEMENT'

      AND (
          text_content IS NULL
          OR TRIM(text_content) = ''
      )


    UNION ALL


    -- --------------------------------------------------------
    -- 2.3 MUST REMAIN TERMINAL ANNEX_LEVEL
    -- --------------------------------------------------------

    SELECT
        '18_ANNEX_2_3_TYPE',
        1,
        COUNT(*)

    FROM source.provisions

    WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
      AND provision_type = 'ANNEX_LEVEL'


    UNION ALL


    -- --------------------------------------------------------
    -- NO SYNTHETIC CHILDREN BELOW 2.3
    -- --------------------------------------------------------

    SELECT
        '19_ANNEX_2_3_SYNTHETIC_CHILDREN',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_id LIKE 'EU-2017-1926-ANNEX-2.3-%'


    UNION ALL


    -- --------------------------------------------------------
    -- DUPLICATE PROVISION IDs
    -- Defensive test even though provision_id is PK.
    -- --------------------------------------------------------

    SELECT
        '20_DUPLICATE_PROVISION_IDS',
        0,
        COUNT(*)

    FROM
    (
        SELECT provision_id

        FROM source.provisions

        WHERE document_id = 'EU-REG-2017-1926'

        GROUP BY provision_id

        HAVING COUNT(*) > 1
    )


    UNION ALL


    -- --------------------------------------------------------
    -- ALLOWED PROVISION TYPES
    -- --------------------------------------------------------

    SELECT
        '21_UNEXPECTED_PROVISION_TYPES',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type NOT IN (
          'ARTICLE',
          'ANNEX',
          'ANNEX_SECTION',
          'ANNEX_LEVEL',
          'ANNEX_GROUP',
          'DATA_ELEMENT'
      )
),

evaluated AS
(
    SELECT
        test,

        CASE
            WHEN expected = actual
            THEN 'PASS'
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
-- MASTER RESULT
-- ============================================================

WITH expected AS
(
    SELECT
        92 AS total_provisions,
        11 AS articles,
        1  AS annex_root,
        2  AS annex_sections,
        7  AS annex_levels,
        14 AS annex_groups,
        57 AS data_elements
),

actual AS
(
    SELECT
        COUNT(*) AS total_provisions,

        COUNT(*) FILTER (
            WHERE provision_type = 'ARTICLE'
        ) AS articles,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX'
        ) AS annex_root,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_SECTION'
        ) AS annex_sections,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_LEVEL'
        ) AS annex_levels,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_GROUP'
        ) AS annex_groups,

        COUNT(*) FILTER (
            WHERE provision_type = 'DATA_ELEMENT'
        ) AS data_elements

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
),

structural_errors AS
(
    SELECT COUNT(*) AS errors

    FROM expected_level_counts e

    JOIN actual_level_counts a
      USING (level)

    WHERE
        e.child_records <> a.child_records
        OR e.groups <> a.groups
        OR e.data_elements <> a.data_elements
),

reference_errors AS
(
    SELECT COUNT(*) AS errors

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type IN (
          'ANNEX',
          'ANNEX_SECTION',
          'ANNEX_LEVEL',
          'ANNEX_GROUP',
          'DATA_ELEMENT'
      )

      AND (
          source_reference IS NULL
          OR TRIM(source_reference) = ''
      )
),

semantic_errors AS
(
    SELECT COUNT(*) AS errors

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type = 'DATA_ELEMENT'

      AND (
          text_content IS NULL
          OR TRIM(text_content) = ''
      )
)

SELECT
    'EU_2017_1926_MASTER_STRUCTURE_INTEGRITY' AS test,

    CASE

        WHEN
            a.total_provisions = e.total_provisions
            AND a.articles = e.articles
            AND a.annex_root = e.annex_root
            AND a.annex_sections = e.annex_sections
            AND a.annex_levels = e.annex_levels
            AND a.annex_groups = e.annex_groups
            AND a.data_elements = e.data_elements

            AND s.errors = 0
            AND r.errors = 0
            AND m.errors = 0

            AND EXISTS (
                SELECT 1
                FROM source.provisions
                WHERE provision_id =
                    'EU-2017-1926-ANNEX-2.3'
                  AND provision_type =
                    'ANNEX_LEVEL'
            )

            AND NOT EXISTS (
                SELECT 1
                FROM source.provisions
                WHERE document_id =
                    'EU-REG-2017-1926'
                  AND provision_id LIKE
                    'EU-2017-1926-ANNEX-2.3-%'
            )

        THEN 'PASS'

        ELSE 'FAIL'

    END AS status

FROM expected e
CROSS JOIN actual a
CROSS JOIN structural_errors s
CROSS JOIN reference_errors r
CROSS JOIN semantic_errors m;


-- ============================================================
-- CORPUS MANIFEST
-- ============================================================

SELECT
    provision_type,
    COUNT(*) AS records

FROM source.provisions

WHERE document_id = 'EU-REG-2017-1926'

GROUP BY provision_type

ORDER BY
    CASE provision_type
        WHEN 'ARTICLE'      THEN 1
        WHEN 'ANNEX'        THEN 2
        WHEN 'ANNEX_SECTION'THEN 3
        WHEN 'ANNEX_LEVEL'  THEN 4
        WHEN 'ANNEX_GROUP'  THEN 5
        WHEN 'DATA_ELEMENT' THEN 6
        ELSE 99
    END;


-- ============================================================
-- LEVEL MANIFEST
-- ============================================================

SELECT
    e.level,
    a.child_records,
    a.groups,
    a.data_elements,

    CASE
        WHEN
            e.child_records = a.child_records
            AND e.groups = a.groups
            AND e.data_elements = a.data_elements

        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM expected_level_counts e

JOIN actual_level_counts a
  USING (level)

ORDER BY e.level;
'@ | Set-Content -Path $TestFile -Encoding UTF8


# ============================================================
# RUN MASTER TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "Ejecutando MASTER STRUCTURE INTEGRITY TEST..." -ForegroundColor Cyan
Write-Host ""

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando MASTER STRUCTURE INTEGRITY TEST."
}


Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host " IMPORTANTE" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "PASS certifica integridad ESTRUCTURAL del corpus." -ForegroundColor Yellow
Write-Host "NO certifica fidelidad textual literal ni cumplimiento juridico." -ForegroundColor Yellow

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " MASTER TEST FINALIZADO" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
