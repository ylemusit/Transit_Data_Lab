$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Database = "$Root\databases\transit_compliance.duckdb"

Get-Command duckdb -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " TRANSIT DATA LAB - PHASE 1" -ForegroundColor Cyan
Write-Host " METADATA REPAIR" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$sql = @"

BEGIN TRANSACTION;

UPDATE source.documents
SET official_url =
'https://www.boe.es/eli/es/l/2025/12/03/9/con'
WHERE document_id = 'ES-LAW-9-2025';


UPDATE source.documents
SET official_url =
'https://eur-lex.europa.eu/eli/dir/2010/40/2023-12-20'
WHERE document_id = 'EU-DIR-2010-40';


UPDATE source.documents
SET official_url =
'https://eur-lex.europa.eu/eli/dir/2023/2661/oj'
WHERE document_id = 'EU-DIR-2023-2661';


UPDATE source.documents
SET official_url =
'https://eur-lex.europa.eu/eli/reg_del/2017/1926/2024-03-04'
WHERE document_id = 'EU-REG-2017-1926';


UPDATE source.documents
SET official_url =
'https://eur-lex.europa.eu/eli/reg_del/2024/490/oj'
WHERE document_id = 'EU-REG-2024-490';

COMMIT;


SELECT
    document_id,
    identifier,
    official_url

FROM source.documents

WHERE document_id IN (
    'ES-LAW-9-2025',
    'EU-DIR-2010-40',
    'EU-DIR-2023-2661',
    'EU-REG-2017-1926',
    'EU-REG-2024-490'
)

ORDER BY document_id;

"@

& duckdb "$Database" -c $sql

if ($LASTEXITCODE -ne 0) {
    throw "Error actualizando metadata."
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " METADATA REPAIR COMPLETED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
