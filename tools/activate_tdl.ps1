# Activación local de TDL; solo modifica el proceso actual.
# Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
[CmdletBinding()]
param([string]$Root)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$configuration = Get-Content -LiteralPath (Join-Path $PSScriptRoot '..\config\tdl_paths.json') -Raw | ConvertFrom-Json
if (-not $Root) { $Root = $env:TDL_ROOT }
if (-not $Root) { $Root = $configuration.TDL_ROOT }
$Root = [System.IO.Path]::GetFullPath($Root)
$areas = @{ TDL_PROJECT_ROOT='01_Project\Transit Data Lab'; TDL_DATA_ROOT='02_Data'; TDL_EVIDENCE_ROOT='03_Evidence'; TDL_RUNTIME_ROOT='04_Runtime'; TDL_CLIENT_ROOT='05_Client' }
$env:TDL_ROOT = $Root
foreach ($name in $areas.Keys) { [Environment]::SetEnvironmentVariable($name, (Join-Path $Root $areas[$name]), 'Process') }
$env:NETEX_SCHEMA_PATH = Join-Path $env:TDL_DATA_ROOT 'External\netex-schema-v2.0.0\xsd\NeTEx_publication.xsd'
$env:GTFS_EXPLORER_ARTIFACT_STORE = Join-Path $env:TDL_CLIENT_ROOT 'HistoricalPackages\06_Products\GTFS Explorer\GTFS Explorer Artifacts'
$env:Path = (Join-Path $Root '07_Tools\DuckDB') + [IO.Path]::PathSeparator + $env:Path
$env:TEMP = Join-Path $env:TDL_RUNTIME_ROOT 'Temp\Sessions'
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
Write-Output ('TDL_PROJECT_ROOT=' + $env:TDL_PROJECT_ROOT)
