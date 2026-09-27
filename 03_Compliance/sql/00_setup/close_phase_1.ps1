$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Database = "$Root\databases\transit_compliance.duckdb"

$HistoricalDir = "$Root\EU\01_Primary_Law\Historical"

$Dir454  = "$HistoricalDir\Regulation_454_2011"
$Dir1305 = "$HistoricalDir\Regulation_1305_2014"

New-Item -ItemType Directory -Force -Path $Dir454  | Out-Null
New-Item -ItemType Directory -Force -Path $Dir1305 | Out-Null

Get-Command duckdb -ErrorAction Stop | Out-Null


Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " TRANSIT DATA LAB" -ForegroundColor Cyan
Write-Host " PHASE 1 - FINAL CORPUS CLOSURE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan


# ============================================================
# 1. HISTORICAL SOURCES
# ============================================================

$File454 =
    "$Dir454\Regulation_454_2011_CONSOLIDATED_2019-06-16_ES.pdf"

$File1305 =
    "$Dir1305\Regulation_1305_2014_CONSOLIDATED_2021-04-18_ES.pdf"


# EUR-Lex CELLAR PDF endpoints for consolidated acts.
# Language = ES

$Url454 =
    "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:02011R0454-20190616"

$Url1305 =
    "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:02014R1305-20210418"


Write-Host ""
Write-Host "[1/6] Descargando fuentes historicas oficiales..." -ForegroundColor Cyan


function Download-OfficialPdf {

    param (
        [Parameter(Mandatory=$true)]
        [string]$Url,

        [Parameter(Mandatory=$true)]
        [string]$Destination
    )

    if (Test-Path $Destination) {

        Write-Host " Ya existe: $Destination" -ForegroundColor Gray
        return
    }

    Write-Host " Descargando:" -ForegroundColor Gray
    Write-Host " $Url" -ForegroundColor DarkGray

    Invoke-WebRequest `
        -Uri $Url `
        -OutFile $Destination `
        -UseBasicParsing

    if (-not (Test-Path $Destination)) {
        throw "No se pudo descargar: $Destination"
    }

    $info = Get-Item $Destination

    if ($info.Length -lt 10000) {
        throw "El fichero descargado parece demasiado pequeno: $Destination"
    }

    # PDF magic header validation
    $bytes = [System.IO.File]::ReadAllBytes($Destination)

    if ($bytes.Length -lt 5) {
        throw "Fichero invalido: $Destination"
    }

    $header =
        [System.Text.Encoding]::ASCII.GetString(
            $bytes[0..4]
        )

    if ($header -ne "%PDF-") {
        throw "EUR-Lex no devolvio un PDF valido: $Destination"
    }

    Write-Host " PDF validado: $($info.Length) bytes" -ForegroundColor Green
}


Download-OfficialPdf `
    -Url $Url454 `
    -Destination $File454

Download-OfficialPdf `
    -Url $Url1305 `
    -Destination $File1305


# ============================================================
# 2. SHA-256 HISTORICAL SOURCES
# ============================================================

Write-Host ""
Write-Host "[2/6] Calculando SHA-256 historicos..." -ForegroundColor Cyan

$Hash454 =
    (Get-FileHash $File454 -Algorithm SHA256).Hash.ToLower()

$Hash1305 =
    (Get-FileHash $File1305 -Algorithm SHA256).Hash.ToLower()


Write-Host " 454/2011  $Hash454" -ForegroundColor Gray
Write-Host " 1305/2014 $Hash1305" -ForegroundColor Gray


# ============================================================
# 3. DATABASE METADATA
# ============================================================

Write-Host ""
Write-Host "[3/6] Actualizando source.documents..." -ForegroundColor Cyan


$Relative454 =
    "EU/01_Primary_Law/Historical/Regulation_454_2011/Regulation_454_2011_CONSOLIDATED_2019-06-16_ES.pdf"

$Relative1305 =
    "EU/01_Primary_Law/Historical/Regulation_1305_2014/Regulation_1305_2014_CONSOLIDATED_2021-04-18_ES.pdf"


$sql = @"

BEGIN TRANSACTION;


UPDATE source.documents
SET
    official_url =
        'https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:02011R0454-20190616',

    local_file =
        '$Relative454',

    source_hash =
        '$Hash454',

    consolidated_date =
        DATE '2019-06-16',

    status =
        'REPEALED'

WHERE document_id =
    'EU-REG-2011-454';


UPDATE source.documents
SET
    official_url =
        'https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:02014R1305-20210418',

    local_file =
        '$Relative1305',

    source_hash =
        '$Hash1305',

    consolidated_date =
        DATE '2021-04-18',

    status =
        'REPEALED'

WHERE document_id =
    'EU-REG-2014-1305';


COMMIT;

"@

& duckdb "$Database" -c $sql

if ($LASTEXITCODE -ne 0) {
    throw "Error actualizando documentos historicos."
}


# ============================================================
# 4. HASH ALL LOCAL SOURCES
# ============================================================

Write-Host ""
Write-Host "[4/6] Sincronizando SHA-256 de todo el corpus..." -ForegroundColor Cyan


$rows = & duckdb "$Database" -csv -noheader -c "
SELECT
    document_id,
    COALESCE(local_file, '')
FROM source.documents
ORDER BY document_id;
"


foreach ($row in $rows) {

    if ([string]::IsNullOrWhiteSpace($row)) {
        continue
    }

    $parts = $row -split ',', 2

    $documentId =
        $parts[0].Trim('"')

    $localFile = ""

    if ($parts.Count -gt 1) {
        $localFile =
            $parts[1].Trim('"')
    }

    if ([string]::IsNullOrWhiteSpace($localFile)) {

        Write-Host " SKIP $documentId - sin local_file" -ForegroundColor Yellow
        continue
    }


    $resolved = $null


    # Absolute path
    if (Test-Path $localFile) {

        $resolved =
            (Resolve-Path $localFile).Path
    }

    # Relative to Compliance root
    elseif (Test-Path (Join-Path $Root $localFile)) {

        $resolved =
            (Resolve-Path (Join-Path $Root $localFile)).Path
    }

    # Search by filename
    else {

        $fileName =
            Split-Path $localFile -Leaf

        $found =
            Get-ChildItem `
                -Path $Root `
                -File `
                -Recurse `
                -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Name -eq $fileName
            } |
            Select-Object -First 1

        if ($found) {
            $resolved = $found.FullName
        }
    }


    if (-not $resolved) {

        Write-Host " MISSING $documentId" -ForegroundColor Red
        continue
    }


    $hash =
        (Get-FileHash `
            -Path $resolved `
            -Algorithm SHA256).Hash.ToLower()


    $safeHash =
        $hash.Replace("'", "''")

    $updateSql = @"

UPDATE source.documents
SET source_hash = '$safeHash'
WHERE document_id = '$documentId';

"@

    & duckdb "$Database" -c $updateSql

    if ($LASTEXITCODE -ne 0) {
        throw "Error actualizando hash de $documentId"
    }


    Write-Host " HASHED $documentId" -ForegroundColor Green
}


# ============================================================
# 5. FINAL DATABASE CHECK
# ============================================================

Write-Host ""
Write-Host "[5/6] Verificacion final del registro..." -ForegroundColor Cyan
Write-Host ""


$validationSql = @"

SELECT
    document_id,

    CASE
        WHEN official_url IS NOT NULL
         AND TRIM(official_url) <> ''
        THEN 'PASS'
        ELSE 'FAIL'
    END AS official_url,

    CASE
        WHEN local_file IS NOT NULL
         AND TRIM(local_file) <> ''
        THEN 'PASS'
        ELSE 'FAIL'
    END AS local_file,

    CASE
        WHEN source_hash IS NOT NULL
         AND LENGTH(source_hash) = 64
         AND regexp_matches(
                source_hash,
                '^[0-9a-fA-F]{64}$'
             )
        THEN 'PASS'
        ELSE 'FAIL'
    END AS sha256

FROM source.documents

ORDER BY document_id;

"@

& duckdb "$Database" -c $validationSql

if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando validacion final."
}


# ============================================================
# 6. RUN EXISTING PHASE 1 MASTER
# ============================================================

Write-Host ""
Write-Host "[6/6] Ejecutando PHASE 1 MASTER..." -ForegroundColor Cyan
Write-Host ""


$Finalize =
    "$Root\sql\00_setup\finalize_phase_1.ps1"


if (-not (Test-Path $Finalize)) {
    throw "No existe finalize_phase_1.ps1"
}


& $Finalize


if ($LASTEXITCODE -ne 0) {
    throw "Error ejecutando finalize_phase_1.ps1"
}


Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " PHASE 1 CLOSURE PROCESS COMPLETED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "La fase solo puede declararse FROZEN si:" -ForegroundColor Yellow
Write-Host ""
Write-Host " PHASE_1_CORPUS_INTEGRITY = PASS"
Write-Host " LOCAL SOURCE FILES       = PASS"
Write-Host " todos los SHA-256        = PASS"
Write-Host ""
