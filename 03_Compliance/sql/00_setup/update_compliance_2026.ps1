$ErrorActionPreference = "Stop"

# ============================================================
# TRANSIT DATA LAB
# COMPLIANCE UPDATE - 2026
#
# Adds:
#   - Regulation (EU) 2024/1679
#   - Implementing Regulation (EU) 2026/1554
#   - Implementing Regulation (EU) 2026/253
#   - Historical references 454/2011 and 1305/2014
#   - source.relationships
#   - Official EUR-Lex PDFs
#   - SOURCE_MANIFEST entries
#
# Does NOT modify existing 2017/1926 provisions.
# ============================================================

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

$Database = "$Root\databases\transit_compliance.duckdb"
$SqlDir   = "$Root\sql\00_setup"
$SqlFile  = "$SqlDir\002_update_compliance_2026.sql"

$EuRoot   = "$Root\EU\01_Primary_Law"
$Manifest = "$Root\_Sources\SOURCE_MANIFEST.txt"

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " TRANSIT DATA LAB - COMPLIANCE UPDATE 2026" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# 1. PRECHECKS
# ------------------------------------------------------------

if (-not (Test-Path $Database)) {
    throw "No existe la base DuckDB: $Database"
}

$Duck = Get-Command duckdb -ErrorAction Stop

Write-Host "DuckDB encontrado: $($Duck.Source)" -ForegroundColor Green
Write-Host "Base encontrada:   $Database" -ForegroundColor Green

# ------------------------------------------------------------
# 2. DIRECTORIES
# ------------------------------------------------------------

$Dirs = @(
    "$EuRoot\Regulation_2024_1679",
    "$EuRoot\Regulation_2026_1554",
    "$EuRoot\Regulation_2026_253",
    "$EuRoot\Historical\Regulation_454_2011",
    "$EuRoot\Historical\Regulation_1305_2014"
)

foreach ($Dir in $Dirs) {
    New-Item -ItemType Directory -Force -Path $Dir | Out-Null
}

Write-Host ""
Write-Host "Directorios preparados." -ForegroundColor Green

# ------------------------------------------------------------
# 3. DOWNLOAD OFFICIAL EUR-LEX DOCUMENTS
# ------------------------------------------------------------

$Downloads = @(
    @{
        Name = "Regulation (EU) 2024/1679"
        Url  = "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32024R1679"
        Out  = "$EuRoot\Regulation_2024_1679\Regulation_EU_2024_1679_ES.pdf"
    },
    @{
        Name = "Implementing Regulation (EU) 2026/1554"
        Url  = "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32026R1554"
        Out  = "$EuRoot\Regulation_2026_1554\Implementing_Regulation_EU_2026_1554_ES.pdf"
    },
    @{
        Name = "Implementing Regulation (EU) 2026/253"
        Url  = "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32026R0253"
        Out  = "$EuRoot\Regulation_2026_253\Implementing_Regulation_EU_2026_253_ES.pdf"
    }
)

Write-Host ""
Write-Host "Descargando documentos oficiales EUR-Lex..." -ForegroundColor Cyan

foreach ($Item in $Downloads) {

    if (Test-Path $Item.Out) {
        Write-Host "YA EXISTE: $($Item.Name)" -ForegroundColor Yellow
    }
    else {
        Write-Host "DESCARGANDO: $($Item.Name)"

        Invoke-WebRequest `
            -Uri $Item.Url `
            -OutFile $Item.Out

        if (-not (Test-Path $Item.Out)) {
            throw "No se pudo descargar: $($Item.Name)"
        }

        if ((Get-Item $Item.Out).Length -lt 1000) {
            throw "El fichero descargado parece incorrecto: $($Item.Out)"
        }

        Write-Host "OK: $($Item.Out)" -ForegroundColor Green
    }
}

# ------------------------------------------------------------
# 4. HASH OFFICIAL FILES
# ------------------------------------------------------------

$Hash1679 = (Get-FileHash `
    "$EuRoot\Regulation_2024_1679\Regulation_EU_2024_1679_ES.pdf" `
    -Algorithm SHA256).Hash

$Hash1554 = (Get-FileHash `
    "$EuRoot\Regulation_2026_1554\Implementing_Regulation_EU_2026_1554_ES.pdf" `
    -Algorithm SHA256).Hash

$Hash0253 = (Get-FileHash `
    "$EuRoot\Regulation_2026_253\Implementing_Regulation_EU_2026_253_ES.pdf" `
    -Algorithm SHA256).Hash

Write-Host ""
Write-Host "SHA-256 calculados." -ForegroundColor Green

# ------------------------------------------------------------
# 5. NORMALIZE PATHS FOR DUCKDB
# ------------------------------------------------------------

$Local1679 = "$EuRoot\Regulation_2024_1679\Regulation_EU_2024_1679_ES.pdf".Replace("\", "/")
$Local1554 = "$EuRoot\Regulation_2026_1554\Implementing_Regulation_EU_2026_1554_ES.pdf".Replace("\", "/")
$Local0253 = "$EuRoot\Regulation_2026_253\Implementing_Regulation_EU_2026_253_ES.pdf".Replace("\", "/")

# ------------------------------------------------------------
# 6. GENERATE SQL MIGRATION
# ------------------------------------------------------------

$Sql = @"
BEGIN TRANSACTION;

-- ============================================================
-- SOURCE RELATIONSHIPS
-- ============================================================

CREATE TABLE IF NOT EXISTS source.relationships
(
    relationship_id VARCHAR PRIMARY KEY,

    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR,

    target_document_id VARCHAR NOT NULL,
    target_provision_id VARCHAR,

    relationship_type VARCHAR NOT NULL,

    description VARCHAR,
    notes VARCHAR,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- NEW CURRENT DOCUMENTS
-- ============================================================

INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-2024-1679',
    'EU',
    'European Parliament and Council',
    'REGULATION',
    'Regulation (EU) 2024/1679 on Union guidelines for the development of the trans-European transport network',
    '2024/1679',
    '32024R1679',
    DATE '2024-06-28',
    DATE '2024-07-18',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2024/1679/oj',
    '$Local1679',
    '$Hash1679',
    'TEN-T framework. Relevant to urban nodes and urban mobility data.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2024-1679'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-IMPL-2026-1554',
    'EU',
    'European Commission',
    'IMPLEMENTING_REGULATION',
    'Commission Implementing Regulation (EU) 2026/1554 on collection and submission of urban mobility data per urban node',
    '2026/1554',
    '32026R1554',
    DATE '2026-07-10',
    DATE '2026-07-30',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg_impl/2026/1554/oj',
    '$Local1554',
    '$Hash1554',
    'Urban mobility data: sustainability, safety and accessibility. Implements Regulation (EU) 2024/1679.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-IMPL-2026-1554'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-IMPL-2026-253',
    'EU',
    'European Commission',
    'IMPLEMENTING_REGULATION',
    'Commission Implementing Regulation (EU) 2026/253 on interoperability of data sharing in rail transport (TEL TSI)',
    '2026/253',
    '32026R0253',
    DATE '2026-02-10',
    DATE '2026-03-01',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg_impl/2026/253/oj',
    '$Local0253',
    '$Hash0253',
    'TEL TSI. Rail telematics and interoperability of data sharing.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-IMPL-2026-253'
);


-- ============================================================
-- HISTORICAL / REPEALED DOCUMENT REFERENCES
-- Metadata only for now. No local PDF downloaded.
-- ============================================================

INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    status,
    language,
    official_url,
    notes
)
SELECT
    'EU-REG-2011-454',
    'EU',
    'European Commission',
    'REGULATION',
    'Commission Regulation (EU) No 454/2011 - TAP TSI',
    '454/2011',
    '32011R0454',
    'REPEALED',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2011/454/oj',
    'Historical reference. Repealed by Implementing Regulation (EU) 2026/253.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2011-454'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    status,
    language,
    official_url,
    notes
)
SELECT
    'EU-REG-2014-1305',
    'EU',
    'European Commission',
    'REGULATION',
    'Commission Regulation (EU) No 1305/2014 - TAF TSI',
    '1305/2014',
    '32014R1305',
    'REPEALED',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2014/1305/oj',
    'Historical reference. Repealed by Implementing Regulation (EU) 2026/253.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2014-1305'
);


-- ============================================================
-- RELATIONSHIPS
-- ============================================================

INSERT INTO source.relationships
SELECT
    'REL-EU-2023-2661-AMENDS-2010-40',
    'EU-DIR-2023-2661',
    NULL,
    'EU-DIR-2010-40',
    NULL,
    'AMENDS',
    'Directive (EU) 2023/2661 amends Directive 2010/40/EU.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2023-2661-AMENDS-2010-40'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2024-490-AMENDS-2017-1926',
    'EU-REG-2024-490',
    NULL,
    'EU-REG-2017-1926',
    NULL,
    'AMENDS',
    'Delegated Regulation (EU) 2024/490 amends Delegated Regulation (EU) 2017/1926.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2024-490-AMENDS-2017-1926'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-1554-IMPLEMENTS-2024-1679',
    'EU-REG-IMPL-2026-1554',
    NULL,
    'EU-REG-2024-1679',
    NULL,
    'IMPLEMENTS',
    'Implementing Regulation (EU) 2026/1554 lays down rules for the application of Regulation (EU) 2024/1679 regarding urban mobility data.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-1554-IMPLEMENTS-2024-1679'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-1554-REFERENCES-2017-1926',
    'EU-REG-IMPL-2026-1554',
    NULL,
    'EU-REG-2017-1926',
    NULL,
    'REFERENCES',
    'Regulation (EU) 2026/1554 refers to data collection methods under Delegated Regulation (EU) 2017/1926 for relevant urban mobility indicators.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-1554-REFERENCES-2017-1926'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-253-REPEALS-2011-454',
    'EU-REG-IMPL-2026-253',
    NULL,
    'EU-REG-2011-454',
    NULL,
    'REPEALS',
    'Implementing Regulation (EU) 2026/253 repeals Regulation (EU) No 454/2011.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-253-REPEALS-2011-454'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-253-REPEALS-2014-1305',
    'EU-REG-IMPL-2026-253',
    NULL,
    'EU-REG-2014-1305',
    NULL,
    'REPEALS',
    'Implementing Regulation (EU) 2026/253 repeals Regulation (EU) No 1305/2014.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-253-REPEALS-2014-1305'
);


COMMIT;
"@

Set-Content `
    -Path $SqlFile `
    -Value $Sql `
    -Encoding UTF8

Write-Host ""
Write-Host "Migracion SQL creada:" -ForegroundColor Cyan
Write-Host $SqlFile

# ------------------------------------------------------------
# 7. EXECUTE MIGRATION
# ------------------------------------------------------------

$DuckSqlPath = $SqlFile.Replace("\", "/")

Write-Host ""
Write-Host "Actualizando DuckDB..." -ForegroundColor Cyan

& duckdb $Database -c ".read '$DuckSqlPath'"

if ($LASTEXITCODE -ne 0) {
    throw "DuckDB devolvio codigo de error: $LASTEXITCODE"
}

Write-Host "DuckDB actualizado correctamente." -ForegroundColor Green

# ------------------------------------------------------------
# 8. UPDATE SOURCE MANIFEST
# ------------------------------------------------------------

$ManifestBlock = @"

============================================================
TRANSIT DATA LAB - COMPLIANCE CORPUS UPDATE
Update date: 2026-09-26
============================================================

[EU-REG-2024-1679]
CLASSIFICATION=REGULATION
STATUS=IN_FORCE
CELEX=32024R1679
TOPIC=TEN-T / URBAN NODES
OFFICIAL_SOURCE=https://eur-lex.europa.eu/eli/reg/2024/1679/oj
LOCAL_FILE=EU/01_Primary_Law/Regulation_2024_1679/Regulation_EU_2024_1679_ES.pdf
SHA256=$Hash1679

[EU-REG-IMPL-2026-1554]
CLASSIFICATION=IMPLEMENTING_REGULATION
STATUS=IN_FORCE
CELEX=32026R1554
TOPIC=URBAN_MOBILITY_DATA
OFFICIAL_SOURCE=https://eur-lex.europa.eu/eli/reg_impl/2026/1554/oj
LOCAL_FILE=EU/01_Primary_Law/Regulation_2026_1554/Implementing_Regulation_EU_2026_1554_ES.pdf
SHA256=$Hash1554

[EU-REG-IMPL-2026-253]
CLASSIFICATION=IMPLEMENTING_REGULATION
STATUS=IN_FORCE
CELEX=32026R0253
TOPIC=RAIL_TELEMATICS / TEL_TSI
OFFICIAL_SOURCE=https://eur-lex.europa.eu/eli/reg_impl/2026/253/oj
LOCAL_FILE=EU/01_Primary_Law/Regulation_2026_253/Implementing_Regulation_EU_2026_253_ES.pdf
SHA256=$Hash0253

[EU-REG-2011-454]
CLASSIFICATION=REGULATION
STATUS=REPEALED
CELEX=32011R0454
TOPIC=RAIL_TELEMATICS / TAP_TSI
REPEALED_BY=EU-REG-IMPL-2026-253
LOCAL_FILE=NOT_DOWNLOADED

[EU-REG-2014-1305]
CLASSIFICATION=REGULATION
STATUS=REPEALED
CELEX=32014R1305
TOPIC=RAIL_TELEMATICS / TAF_TSI
REPEALED_BY=EU-REG-IMPL-2026-253
LOCAL_FILE=NOT_DOWNLOADED

"@

if (-not (Test-Path $Manifest)) {
    New-Item -ItemType File -Force -Path $Manifest | Out-Null
}

$CurrentManifest = Get-Content $Manifest -Raw

if ($CurrentManifest -notmatch "EU-REG-IMPL-2026-1554") {

    Add-Content `
        -Path $Manifest `
        -Value $ManifestBlock `
        -Encoding UTF8

    Write-Host "SOURCE_MANIFEST actualizado." -ForegroundColor Green
}
else {
    Write-Host "SOURCE_MANIFEST ya contiene esta actualizacion." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# 9. VALIDATION
# ------------------------------------------------------------

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " VALIDACION" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "DOCUMENTOS:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT
    document_id,
    identifier,
    document_type,
    status
FROM source.documents
ORDER BY document_id;
"

Write-Host ""
Write-Host "RELACIONES:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT
    relationship_id,
    source_document_id,
    relationship_type,
    target_document_id
FROM source.relationships
ORDER BY relationship_id;
"

Write-Host ""
Write-Host "CONTADORES:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT 'documents' AS entity, COUNT(*) AS records
FROM source.documents

UNION ALL

SELECT 'relationships', COUNT(*)
FROM source.relationships

UNION ALL

SELECT 'provisions', COUNT(*)
FROM source.provisions

UNION ALL

SELECT 'requirements', COUNT(*)
FROM compliance.requirements

UNION ALL

SELECT 'format_mappings', COUNT(*)
FROM mapping.format_coverage

UNION ALL

SELECT 'audit_rules', COUNT(*)
FROM audit.rules;
"

Write-Host ""
Write-Host "FICHEROS OFICIALES:" -ForegroundColor Cyan

Get-Item `
    "$EuRoot\Regulation_2024_1679\Regulation_EU_2024_1679_ES.pdf",
    "$EuRoot\Regulation_2026_1554\Implementing_Regulation_EU_2026_1554_ES.pdf",
    "$EuRoot\Regulation_2026_253\Implementing_Regulation_EU_2026_253_ES.pdf" |
    Select-Object Name, Length, LastWriteTime

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " ACTUALIZACION COMPLETADA" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
