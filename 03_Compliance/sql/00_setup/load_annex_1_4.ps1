$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 1.4
# LOAD + SOURCE INTEGRITY TEST
#
# Official source:
# CELEX 02017R1926-20240304
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\005_eu_2017_1926_annex_1_4.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_1_4.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 1.4" -ForegroundColor Cyan
Write-Host " HISTORIC + OBSERVED DATA" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan


# ============================================================
# 1. CREATE SOURCE SQL
# ============================================================

@'
BEGIN TRANSACTION;

-- ============================================================
-- ANNEX 1.4 - LEVEL OF SERVICE 4
--
-- Consolidated Regulation (EU) 2017/1926
-- Version: 04/03/2024
--
-- IMPORTANT:
-- 1.4(a) and 1.4(d) are terminal legal elements.
-- Only (b) and (c) are represented as ANNEX_GROUP.
-- ============================================================


-- ------------------------------------------------------------
-- 1.4(a)
-- Historic travel and traffic data
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-A',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(a)',
    'Datos históricos de desplazamientos y tráfico sobre retrasos',
    'Datos históricos de desplazamientos y tráfico sobre retrasos para transporte programado y transporte a la demanda cuando proceda.',
    'Annex 1.4(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-A'
);


-- ------------------------------------------------------------
-- 1.4(b)
-- Observed delays and passing times
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.4',
    '1.4(b)',
    'Datos observados sobre retrasos y tiempos de paso',
    'Datos observados sobre retrasos y tiempos de paso para transporte programado.',
    'Annex 1.4(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(i)',
    'Retrasos ferroviarios de al menos 60 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos de al menos 60 minutos en servicios ferroviarios de viajeros.',
    'Annex 1.4(b)(i)',
    'Threshold linked by the Regulation to Regulation (EU) 2021/782.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(ii)',
    'Retrasos marítimos y por vías navegables superiores a 90 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos en la salida superiores a 90 minutos en servicios de pasajeros por mar y vías navegables interiores.',
    'Annex 1.4(b)(ii)',
    'Threshold linked by the Regulation to Regulation (EU) No 1177/2010.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(iii)',
    'Retrasos de autobús y autocar superiores a 120 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos en la salida desde una terminal superiores a 120 minutos para servicios regulares de autobús y autocar con distancia programada de 250 km o más.',
    'Annex 1.4(b)(iii)',
    'Threshold linked by the Regulation to Regulation (EU) No 181/2011.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(iv)',
    'Retrasos de vuelos',
    'Duración y, cuando sea posible, motivo de retrasos de vuelos en salida de al menos 120 minutos y en llegada de al menos 180 minutos.',
    'Annex 1.4(b)(iv)',
    'Threshold linked by the Regulation to Regulation (EC) No 261/2004.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-IV'
);


-- ------------------------------------------------------------
-- 1.4(c)
-- Observed cancellations
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.4',
    '1.4(c)',
    'Datos observados sobre cancelaciones',
    'Datos observados sobre cancelaciones para transporte programado.',
    'Annex 1.4(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(i)',
    'Cancelaciones ferroviarias',
    'Cancelaciones y, cuando sea posible, motivo de la cancelación de servicios ferroviarios de viajeros.',
    'Annex 1.4(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(ii)',
    'Cancelaciones marítimas y por vías navegables',
    'Cancelaciones y, cuando sea posible, motivo de servicios de pasajeros por mar y vías navegables interiores.',
    'Annex 1.4(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(iii)',
    'Cancelaciones de autobús y autocar',
    'Cancelaciones y, cuando sea posible, motivo de servicios regulares de autobús y autocar con distancia programada de 250 km o más.',
    'Annex 1.4(c)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(iv)',
    'Cancelaciones de vuelos',
    'Cancelaciones y, cuando sea posible, motivo de cancelación de vuelos.',
    'Annex 1.4(c)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-IV'
);


-- ------------------------------------------------------------
-- 1.4(d)
-- Parking tariffs
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-D',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(d)',
    'Información sobre tarifas de estacionamiento',
    'Información sobre tarifas de estacionamiento.',
    'Annex 1.4(d)',
    'Terminal legal element.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-D'
);


COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


# ============================================================
# 2. LOAD SOURCE
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Cargando ANNEX 1.4..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error cargando ANNEX 1.4."
}


# ============================================================
# 3. CREATE INTEGRITY TEST
# ============================================================

@'
CREATE OR REPLACE TEMP TABLE expected_annex_1_4
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);

INSERT INTO expected_annex_1_4 VALUES

('EU-2017-1926-ANNEX-1.4-A',     'DATA_ELEMENT', '1.4(a)'),

('EU-2017-1926-ANNEX-1.4-B',     'ANNEX_GROUP',  '1.4(b)'),
('EU-2017-1926-ANNEX-1.4-B-I',   'DATA_ELEMENT', '1.4(b)(i)'),
('EU-2017-1926-ANNEX-1.4-B-II',  'DATA_ELEMENT', '1.4(b)(ii)'),
('EU-2017-1926-ANNEX-1.4-B-III', 'DATA_ELEMENT', '1.4(b)(iii)'),
('EU-2017-1926-ANNEX-1.4-B-IV',  'DATA_ELEMENT', '1.4(b)(iv)'),

('EU-2017-1926-ANNEX-1.4-C',     'ANNEX_GROUP',  '1.4(c)'),
('EU-2017-1926-ANNEX-1.4-C-I',   'DATA_ELEMENT', '1.4(c)(i)'),
('EU-2017-1926-ANNEX-1.4-C-II',  'DATA_ELEMENT', '1.4(c)(ii)'),
('EU-2017-1926-ANNEX-1.4-C-III', 'DATA_ELEMENT', '1.4(c)(iii)'),
('EU-2017-1926-ANNEX-1.4-C-IV',  'DATA_ELEMENT', '1.4(c)(iv)'),

('EU-2017-1926-ANNEX-1.4-D',     'DATA_ELEMENT', '1.4(d)');


CREATE OR REPLACE TEMP VIEW actual_annex_1_4 AS
SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.4-%';


WITH test_results AS
(
    SELECT '01_EXPECTED_COUNT' test, 12 expected, COUNT(*) actual
    FROM actual_annex_1_4

    UNION ALL

    SELECT '02_DATA_ELEMENT_COUNT', 10, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT '03_GROUP_COUNT', 2, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT '04_MISSING_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_4
        EXCEPT
        SELECT provision_id FROM actual_annex_1_4
    )

    UNION ALL

    SELECT '05_UNEXPECTED_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_4
        EXCEPT
        SELECT provision_id FROM expected_annex_1_4
    )

    UNION ALL

    SELECT '06_SECTION_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT '07_TYPE_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT '08_SOURCE_REFERENCE_NULL', 0, COUNT(*)
    FROM actual_annex_1_4
    WHERE source_reference IS NULL
),

evaluated AS
(
    SELECT
        test,
        CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END status,
        expected,
        actual
    FROM test_results
)

SELECT *
FROM evaluated
ORDER BY test;


WITH checks AS
(
    SELECT 12 expected, COUNT(*) actual
    FROM actual_annex_1_4

    UNION ALL

    SELECT 10, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 2, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_4
        EXCEPT
        SELECT provision_id FROM actual_annex_1_4
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_4
        EXCEPT
        SELECT provision_id FROM expected_annex_1_4
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_1_4
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_1_4_SOURCE_INTEGRITY' AS test,
    CASE
        WHEN COUNT(*) FILTER (WHERE expected <> actual) = 0
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
Write-Host " SOURCE INTEGRITY TEST - ANNEX 1.4" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 1.4."
}


# ============================================================
# 5. CORPUS SUMMARY
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " STATIC / HISTORIC / OBSERVED CORPUS" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c "
WITH levels(level) AS (
    VALUES ('1.1'), ('1.2'), ('1.3'), ('1.4')
)
SELECT
    l.level,
    COUNT(p.provision_id) FILTER (
        WHERE p.provision_type IN ('ANNEX_GROUP','DATA_ELEMENT')
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
Write-Host " ANNEX 1.4 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
