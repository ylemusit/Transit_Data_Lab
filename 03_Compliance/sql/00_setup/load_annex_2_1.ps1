$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 2.1
# DYNAMIC DATA - LEVEL OF SERVICE 1
#
# Source:
# CELEX 02017R1926-20240304
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\006_eu_2017_1926_annex_2_1.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_2_1.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir   | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 2.1" -ForegroundColor Cyan
Write-Host " DYNAMIC DATA - LEVEL OF SERVICE 1" -ForegroundColor Cyan
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
-- 2. TYPES OF DYNAMIC TRAVEL AND TRAFFIC DATA
-- 2.1 Level of service 1
--
-- Heading:
-- Passing times, trip plans and auxiliary information
--
-- Legal structure:
--   (i)
--   (ii)
--   (iii)
--
-- No ANNEX_GROUP nodes exist below 2.1.
--
-- heading/text_content contain normalized Spanish descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 2.1(i)
-- Disruptions
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(i)',
    'Perturbaciones',
    'Perturbaciones, como cierres de redes o desvíos y, cuando sea posible, el motivo de la perturbación.',
    'Annex 2.1(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-I'
);


-- ------------------------------------------------------------
-- 2.1(ii)
-- Real-time status information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(ii)',
    'Información sobre la situación en tiempo real',
    'Información sobre la situación en tiempo real, como horas estimadas de salida y llegada de los servicios, retrasos, anulaciones y seguimiento de correspondencias garantizadas.',
    'Annex 2.1(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-II'
);


-- ------------------------------------------------------------
-- 2.1(iii)
-- Access node feature status
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(iii)',
    'Estado de los servicios en los nodos de acceso',
    'Estado de los servicios en los nodos de acceso, incluida información dinámica sobre andenes, ascensores o escaleras mecánicas en funcionamiento y entradas y salidas cerradas, para los transportes programados.',
    'Annex 2.1(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-III'
);

COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


# ============================================================
# 2. LOAD SOURCE
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Cargando ANNEX 2.1..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error cargando ANNEX 2.1."
}


# ============================================================
# 3. CREATE STRUCTURAL INTEGRITY TEST
# ============================================================

@'
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
'@ | Set-Content -Path $TestFile -Encoding UTF8


# ============================================================
# 4. RUN TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SOURCE INTEGRITY TEST - ANNEX 2.1" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 2.1."
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
    COUNT(*) AS total_document_provisions
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926';
"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " ANNEX 2.1 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
