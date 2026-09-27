$ErrorActionPreference = 'Stop'

$gtfsLabRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$database = Join-Path $gtfsLabRoot 'databases\gtfs_lab.duckdb'
$sqlFile = Join-Path $PSScriptRoot '20260924_020003_import_consorcio_asturias.sql'

if (-not (Test-Path -LiteralPath $database)) { throw "No existe la base GTFS: $database" }
if (-not (Test-Path -LiteralPath $sqlFile)) { throw "No existe el SQL de importación: $sqlFile" }

$sqlPath = $sqlFile.Replace('\', '/')
Push-Location $gtfsLabRoot
try {
    & duckdb $database -c ".read '$sqlPath'"
    if ($LASTEXITCODE -ne 0) { throw "DuckDB terminó con código $LASTEXITCODE." }
}
finally {
    Pop-Location
}

