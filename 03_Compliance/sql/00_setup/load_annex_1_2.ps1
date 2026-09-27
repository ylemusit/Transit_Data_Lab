$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 1.2
# LOAD + SOURCE INTEGRITY TEST
#
# Source:
# CELEX 02017R1926-20240304
# Amended by Regulation (EU) 2024/490
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\003_eu_2017_1926_annex_1_2.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_1_2.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir   | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 1.2" -ForegroundColor Cyan
Write-Host " LOAD + SOURCE INTEGRITY TEST" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan


# ============================================================
# 1. CREATE SOURCE SQL
# ============================================================

@'
BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
-- ANNEX 1.2 - Level of service 2
--
-- IMPORTANT:
-- heading/text_content are normalized descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 1.2(a)
-- Location search
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(a)',
    'Búsqueda de ubicación — transporte a demanda y transporte personal',
    'Búsqueda de ubicación para transporte a demanda y transporte personal.',
    'Annex 1.2(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(i)',
    'Ubicación de plazas de estacionamiento',
    'Ubicación de plazas de estacionamiento en vía pública y fuera de ella, incluidas plazas accesibles para personas con discapacidad y movilidad reducida.',
    'Annex 1.2(a)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(ii)',
    'Paradas Park & Ride',
    'Localización de paradas o instalaciones Park & Ride.',
    'Annex 1.2(a)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(iii)',
    'Paradas Park & Drive',
    'Localización de paradas o instalaciones Park & Drive.',
    'Annex 1.2(a)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(iv)',
    'Estaciones de bicicletas compartidas',
    'Localización de estaciones de bicicletas compartidas.',
    'Annex 1.2(a)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-IV'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-V',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(v)',
    'Estaciones de coches compartidos',
    'Localización de estaciones de coches compartidos.',
    'Annex 1.2(a)(v)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-V'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-VI',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(vi)',
    'Estacionamiento seguro para bicicletas',
    'Localización de estacionamiento seguro para bicicletas, como garajes cerrados.',
    'Annex 1.2(a)(vi)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-VI'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-VII',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(vii)',
    'Zonas de estacionamiento de patinetes',
    'Localización de zonas de estacionamiento de patinetes.',
    'Annex 1.2(a)(vii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-VII'
);


-- ------------------------------------------------------------
-- 1.2(b)
-- Information service
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(b)',
    'Servicio de información',
    'Información relativa a adquisición de billetes y pago de estacionamiento.',
    'Annex 1.2(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(b)(i)',
    'Dónde y cómo comprar billetes',
    'Dónde y cómo comprar billetes para transporte programado, incluidos canales de venta, métodos de entrega y métodos de pago.',
    'Annex 1.2(b)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(b)(ii)',
    'Dónde y cómo pagar el estacionamiento',
    'Dónde y cómo pagar el estacionamiento, incluidos canales de venta, métodos de entrega y métodos de pago.',
    'Annex 1.2(b)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B-II'
);


-- ------------------------------------------------------------
-- 1.2(c)
-- Auxiliary information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(c)',
    'Información auxiliar',
    'Información auxiliar para transporte programado y transporte a demanda cuando resulte pertinente.',
    'Annex 1.2(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(c)(i)',
    'Tarifas estándar comunes básicas',
    'Datos de red tarifaria y estructuras tarifarias estándar, incluidas zonas, paradas, etapas tarifarias y tarifas punto a punto, diarias, semanales, zonales o planas.',
    'Annex 1.2(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(c)(ii)',
    'Equipamiento de los vehículos',
    'Equipamiento del vehículo, incluidas clases de transporte, Wi-Fi a bordo, capacidad y condiciones de acceso para bicicletas.',
    'Annex 1.2(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C-II'
);


COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


Write-Host ""
Write-Host "SQL de fuente creado:" -ForegroundColor Green
Write-Host $SourceFile


# ============================================================
# 2. LOAD ANNEX 1.2
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Cargando ANNEX 1.2..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error cargando ANNEX 1.2."
}


# ============================================================
# 3. BASIC VALIDATION
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " VALIDACION DE CARGA" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c "
SELECT
    COUNT(*) AS annex_1_2_records,
    COUNT(*) FILTER (
        WHERE provision_type = 'ANNEX_GROUP'
    ) AS groups,
    COUNT(*) FILTER (
        WHERE provision_type = 'DATA_ELEMENT'
    ) AS data_elements
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.2-%';

SELECT
    COUNT(*) AS total_document_provisions
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926';
"


# ============================================================
# 4. CREATE INTEGRITY TEST
# ============================================================

@'
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
'@ | Set-Content -Path $TestFile -Encoding UTF8


Write-Host ""
Write-Host "Test creado:" -ForegroundColor Green
Write-Host $TestFile


# ============================================================
# 5. RUN INTEGRITY TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SOURCE INTEGRITY TEST - ANNEX 1.2" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 1.2."
}


# ============================================================
# 6. FINAL COUNTS
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ESTADO DEL CORPUS 2017/1926" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c "
SELECT
    section,
    COUNT(*) AS records,
    COUNT(*) FILTER (
        WHERE provision_type = 'ANNEX_GROUP'
    ) AS groups,
    COUNT(*) FILTER (
        WHERE provision_type = 'DATA_ELEMENT'
    ) AS data_elements
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND section IN ('1.1','1.2')
GROUP BY section
ORDER BY section;

SELECT
    COUNT(*) AS total_document_provisions
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926';
"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " ANNEX 1.2 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
