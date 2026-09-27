$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 2.3
# DYNAMIC DATA - LEVEL OF SERVICE 3
#
# Source:
# CELEX 02017R1926-20240304
# Consolidated version: 04/03/2024
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\008_eu_2017_1926_annex_2_3.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_2_3.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir   | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 2.3" -ForegroundColor Cyan
Write-Host " DYNAMIC DATA - LEVEL OF SERVICE 3" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan


# ============================================================
# 1. CREATE SOURCE SQL
# ============================================================

@'
BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
--
-- ANNEX
-- 2.3 Level of service 3
--
-- IMPORTANT MODELING DECISION
--
-- The legal source contains no child paragraph below 2.3.
-- The substantive data category is expressed directly at 2.3.
--
-- Therefore:
--
--   NO synthetic 2.3(i)
--   NO synthetic DATA_ELEMENT child
--
-- The existing ANNEX_LEVEL provision is enriched directly.
-- ============================================================

UPDATE source.provisions

SET
    heading =
        'Nivel de servicio 3 - Información sobre ocupación del vehículo',

    text_content =
        'Información sobre la ocupación del vehículo para el transporte programado y el transporte a la demanda, cuando proceda.',

    source_reference =
        'Annex 2.3',

    notes =
        'Terminal ANNEX_LEVEL: the legal source contains the substantive data category directly at point 2.3 and has no child subparagraphs.'

WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
  AND document_id = 'EU-REG-2017-1926';

COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


# ============================================================
# 2. LOAD SOURCE
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Actualizando ANNEX 2.3..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error actualizando ANNEX 2.3."
}


# ============================================================
# 3. CREATE SOURCE INTEGRITY TEST
# ============================================================

@'
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
'@ | Set-Content -Path $TestFile -Encoding UTF8


# ============================================================
# 4. RUN TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SOURCE INTEGRITY TEST - ANNEX 2.3" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 2.3."
}


# ============================================================
# 5. COMPLETE ANNEX SUMMARY
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ESTADO DEL ANEXO 2017/1926" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c "
WITH levels(level) AS (
    VALUES
        ('1.1'),
        ('1.2'),
        ('1.3'),
        ('1.4'),
        ('2.1'),
        ('2.2'),
        ('2.3')
)

SELECT
    l.level,

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

FROM levels l

LEFT JOIN source.provisions p
  ON p.document_id = 'EU-REG-2017-1926'
 AND p.section LIKE l.level || '(%'

GROUP BY l.level
ORDER BY l.level;


SELECT
    provision_id,
    provision_type,
    section,
    heading,
    source_reference
FROM source.provisions
WHERE provision_id = 'EU-2017-1926-ANNEX-2.3';


SELECT
    COUNT(*) AS total_document_provisions
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926';
"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " ANNEX 2.3 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
