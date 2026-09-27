$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# EU 2017/1926 - ANNEX 1.3
# LOAD + SOURCE INTEGRITY TEST
#
# Official source:
# CELEX 02017R1926-20240304
# Consolidated version: 04/03/2024
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"

$SourceDir  = "$Root\sql\01_sources"
$SourceFile = "$SourceDir\004_eu_2017_1926_annex_1_3.sql"

$TestDir  = "$Root\sql\07_tests\source"
$TestFile = "$TestDir\test_eu_2017_1926_annex_1_3.sql"

New-Item -ItemType Directory -Force -Path $SourceDir | Out-Null
New-Item -ItemType Directory -Force -Path $TestDir   | Out-Null

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " EU 2017/1926 - ANNEX 1.3" -ForegroundColor Cyan
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
-- ANNEX 1.3 - Level of service 3
--
-- heading/text_content are normalized descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 1.3(a)
-- Detailed fare query
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(a)',
    'Consulta detallada de tarifas normales comunes y tarifas especiales',
    'Consulta detallada de tarifas normales comunes y tarifas especiales para transporte programado y transporte a la demanda cuando proceda.',
    'Annex 1.3(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(i)',
    'Clases de pasajeros',
    'Clases de pasajeros, condiciones de cualificación y clases de viaje.',
    'Annex 1.3(a)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-I'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(ii)',
    'Productos tarifarios comunes',
    'Productos tarifarios comunes: derechos de acceso, elegibilidad, condiciones básicas de uso y precios estándar.',
    'Annex 1.3(a)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-II'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(iii)',
    'Productos tarifarios especiales',
    'Productos tarifarios con condiciones especiales, como promociones, grupos, abonos, productos agregados y productos suplementarios.',
    'Annex 1.3(a)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-III'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(iv)',
    'Condiciones comerciales básicas',
    'Condiciones comerciales básicas, como reembolso, sustitución, cambio o transferencia.',
    'Annex 1.3(a)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-IV'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-V',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(v)',
    'Condiciones básicas de reserva',
    'Condiciones básicas de reserva: ventanas de compra, períodos de validez, restricciones de itinerario, secuencias zonales y estancia mínima.',
    'Annex 1.3(a)(v)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-V'
);


-- ------------------------------------------------------------
-- 1.3(b)
-- Demand-responsive transport booking
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(b)',
    'Servicio de información para transporte a la demanda',
    'Información sobre cómo reservar servicios de transporte a la demanda.',
    'Annex 1.3(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-B'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(b)(i)',
    'Reserva de transporte a la demanda',
    'Cómo reservar servicios de transporte a la demanda, incluidos canales minoristas, métodos de ejecución y métodos de pago.',
    'Annex 1.3(b)',
    'Normalized terminal data element. The legal Annex expresses this content directly under point (b), without a numbered subpoint.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-B-I'
);


-- ------------------------------------------------------------
-- 1.3(c)
-- Trip plans
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(c)',
    'Planes de viaje',
    'Datos adicionales utilizados en planes de viaje.',
    'Annex 1.3(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(i)',
    'Características detalladas de la red ciclista',
    'Características detalladas de la red ciclista, como firme, circulación en paralelo, superficies compartidas y restricciones de giro o acceso.',
    'Annex 1.3(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-I'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(ii)',
    'Parámetros para calcular factores medioambientales',
    'Parámetros necesarios para calcular factores medioambientales, como emisiones de gases de efecto invernadero.',
    'Annex 1.3(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-II'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(iii)',
    'Parámetros para calcular el consumo de combustible',
    'Parámetros necesarios para calcular el consumo de combustibles convencionales y alternativos.',
    'Annex 1.3(c)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-III'
);


-- ------------------------------------------------------------
-- 1.3(d)
-- Trip plan computation
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-D',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(d)',
    'Cálculo de planes de viaje',
    'Cálculo de planes de viaje mediante tiempos de viaje estimados.',
    'Annex 1.3(d)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-D'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-D-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(d)(i)',
    'Tiempos de viaje estimados',
    'Tiempos de viaje estimados por tipo de día, franja horaria y modo o combinación de modos de transporte.',
    'Annex 1.3(d)',
    'Normalized terminal data element. The legal Annex expresses this content directly under point (d), without a numbered subpoint.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-D-I'
);

COMMIT;
'@ | Set-Content -Path $SourceFile -Encoding UTF8


# ============================================================
# 2. LOAD
# ============================================================

$DuckSource = $SourceFile.Replace("\", "/")

Write-Host ""
Write-Host "Cargando ANNEX 1.3..." -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckSource'"

if ($LASTEXITCODE -ne 0) {
    throw "Error cargando ANNEX 1.3."
}


# ============================================================
# 3. CREATE TEST
# ============================================================

@'
CREATE OR REPLACE TEMP TABLE expected_annex_1_3
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);

INSERT INTO expected_annex_1_3 VALUES
('EU-2017-1926-ANNEX-1.3-A',     'ANNEX_GROUP',  '1.3(a)'),
('EU-2017-1926-ANNEX-1.3-A-I',   'DATA_ELEMENT', '1.3(a)(i)'),
('EU-2017-1926-ANNEX-1.3-A-II',  'DATA_ELEMENT', '1.3(a)(ii)'),
('EU-2017-1926-ANNEX-1.3-A-III', 'DATA_ELEMENT', '1.3(a)(iii)'),
('EU-2017-1926-ANNEX-1.3-A-IV',  'DATA_ELEMENT', '1.3(a)(iv)'),
('EU-2017-1926-ANNEX-1.3-A-V',   'DATA_ELEMENT', '1.3(a)(v)'),

('EU-2017-1926-ANNEX-1.3-B',     'ANNEX_GROUP',  '1.3(b)'),
('EU-2017-1926-ANNEX-1.3-B-I',   'DATA_ELEMENT', '1.3(b)(i)'),

('EU-2017-1926-ANNEX-1.3-C',     'ANNEX_GROUP',  '1.3(c)'),
('EU-2017-1926-ANNEX-1.3-C-I',   'DATA_ELEMENT', '1.3(c)(i)'),
('EU-2017-1926-ANNEX-1.3-C-II',  'DATA_ELEMENT', '1.3(c)(ii)'),
('EU-2017-1926-ANNEX-1.3-C-III', 'DATA_ELEMENT', '1.3(c)(iii)'),

('EU-2017-1926-ANNEX-1.3-D',     'ANNEX_GROUP',  '1.3(d)'),
('EU-2017-1926-ANNEX-1.3-D-I',   'DATA_ELEMENT', '1.3(d)(i)');


CREATE OR REPLACE TEMP VIEW actual_annex_1_3 AS
SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.3-%';


WITH test_results AS
(
    SELECT '01_EXPECTED_COUNT' test, 14 expected, COUNT(*) actual
    FROM actual_annex_1_3

    UNION ALL

    SELECT '02_DATA_ELEMENT_COUNT', 10, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT '03_GROUP_COUNT', 4, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT '04_MISSING_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_3
        EXCEPT
        SELECT provision_id FROM actual_annex_1_3
    )

    UNION ALL

    SELECT '05_UNEXPECTED_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_3
        EXCEPT
        SELECT provision_id FROM expected_annex_1_3
    )

    UNION ALL

    SELECT '06_SECTION_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT '07_TYPE_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT '08_SOURCE_REFERENCE_NULL', 0, COUNT(*)
    FROM actual_annex_1_3
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


WITH test_results AS
(
    SELECT 14 expected, COUNT(*) actual
    FROM actual_annex_1_3

    UNION ALL

    SELECT 10, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 4, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_3
        EXCEPT
        SELECT provision_id FROM actual_annex_1_3
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_3
        EXCEPT
        SELECT provision_id FROM expected_annex_1_3
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_1_3
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_1_3_SOURCE_INTEGRITY' AS test,
    CASE
        WHEN COUNT(*) FILTER (WHERE expected <> actual) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM test_results;
'@ | Set-Content -Path $TestFile -Encoding UTF8


# ============================================================
# 4. RUN TEST
# ============================================================

$DuckTest = $TestFile.Replace("\", "/")

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SOURCE INTEGRITY TEST - ANNEX 1.3" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c ".read '$DuckTest'"

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando test ANNEX 1.3."
}


# ============================================================
# 5. CORRECT HIERARCHICAL SUMMARY
# ============================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ESTADO DEL CORPUS 2017/1926" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

& duckdb "$Database" -c "
WITH levels(level) AS (
    VALUES ('1.1'), ('1.2'), ('1.3')
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
Write-Host " ANNEX 1.3 - PROCESO FINALIZADO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
