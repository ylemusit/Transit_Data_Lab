$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 2.2
# DYNAMIC DATA - LEVEL OF SERVICE 2
#
# Source:
# CELEX 02017R1926-20240304
# Consolidated version: 04/03/2024
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\007_eu_2017_1926_annex_2_2.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_2_2.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir   | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 2.2" -ForegroundColor Cyan
Write-Host " DYNAMIC DATA - LEVEL OF SERVICE 2" -ForegroundColor Cyan
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
-- 2.2 Level of service 2
--
-- Legal structure:
--
-- (a) terminal element
--
-- (b) availability check and location
--     (i)
--     (ii)
--
-- IMPORTANT:
-- No artificial ANNEX_GROUP is created for 2.2(a).
-- heading/text_content contain normalized Spanish descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 2.2(a)
-- Parking tariff information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-A',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(a)',
    'Información sobre tarifas de estacionamiento',
    'Servicio de información sobre tarifas de estacionamiento para transporte a la demanda y transporte personal.',
    'Annex 2.2(a)',
    'Terminal legal element. Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-A'
);


-- ------------------------------------------------------------
-- 2.2(b)
-- Availability check and location
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '2.2',
    '2.2(b)',
    'Consulta de disponibilidad y localización',
    'Consulta de disponibilidad y localización para transporte a la demanda y transporte personal cuando proceda.',
    'Annex 2.2(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B'
);


-- ------------------------------------------------------------
-- 2.2(b)(i)
-- Shared vehicles
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(b)(i)',
    'Disponibilidad y localización de vehículos compartidos',
    'Disponibilidad y localización de coches compartidos, bicicletas compartidas, patinetes compartidos y otros vehículos compartidos.',
    'Annex 2.2(b)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B-I'
);


-- ------------------------------------------------------------
-- 2.2(b)(ii)
-- Available parking spaces
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(b)(ii)',
    'Plazas de estacionamiento disponibles',
    'Plazas de estacionamiento disponibles, tanto en vía pública como fuera de ella.',
    'Annex 2.2(b)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B-II'
);

COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


# ============================================================
# 2. LOAD SOURCE
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Cargando ANNEX 2.2..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error cargando ANNEX 2.2."
}


# ============================================================
# 3. CREATE STRUCTURAL INTEGRITY TEST
# ============================================================

@'
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
'@ | Set-Content -Path $TestFile -Encoding UTF8


# ============================================================
# 4. RUN TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SOURCE INTEGRITY TEST - ANNEX 2.2" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 2.2."
}


# ============================================================
# 5. ANNEX SUMMARY
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
Write-Host " ANNEX 2.2 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
