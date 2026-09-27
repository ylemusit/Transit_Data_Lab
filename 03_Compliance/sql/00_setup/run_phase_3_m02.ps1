param([switch]$ValidateOnly)
$ErrorActionPreference = 'Stop'
$complianceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$repoRoot = Split-Path -Parent (Split-Path -Parent $complianceRoot)
$database = Join-Path $complianceRoot 'databases\transit_compliance.duckdb'
$migration = Join-Path $PSScriptRoot '005_phase_3_m02_mapping_framework.sql'
$validator = Join-Path $complianceRoot 'sql\07_tests\phase_3\validate_phase_3_level_a.sql'
$fixture = Join-Path $complianceRoot 'sql\07_tests\phase_3\test_phase_3_m02_fixture.sql'
$duckdb = (Get-Command duckdb -ErrorAction Stop).Source
function Invoke-DuckDB([string[]]$Arguments) {
    $output = & $duckdb @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "DuckDB falló ($LASTEXITCODE): $output" }
    return $output
}
function Get-Counts {
    $q = "SELECT (SELECT count(*) FROM compliance.requirements) requirements,(SELECT count(*) FROM compliance.deadlines) deadlines,(SELECT count(*) FROM compliance.requirement_candidates) candidates,(SELECT count(*) FROM compliance.source_facts) source_facts,(SELECT count(*) FROM audit.rules) audit_rules;"
    $raw = Invoke-DuckDB @('-readonly','-csv',$database,'-c',$q)
    return ($raw | ConvertFrom-Csv | Select-Object -First 1)
}
$before = Get-Counts
if ($before.requirements -ne '48' -or $before.deadlines -ne '10' -or $before.candidates -ne '34' -or $before.source_facts -ne '36') { throw "Conteos Phase 1/2 iniciales inesperados: $($before | ConvertTo-Json -Compress)" }
if (-not $ValidateOnly) { Invoke-DuckDB @('-bail',$database,'-f',$migration) | Out-Null }
$fixtureOutput = Invoke-DuckDB @('-bail',$database,'-f',$fixture)
if (($fixtureOutput -join "`n") -notmatch 'PASS') { throw "Fixture sintético no pasó: $($fixtureOutput -join ' ')" }
$after = Get-Counts
if (($before | ConvertTo-Json -Compress) -ne ($after | ConvertTo-Json -Compress)) { throw "Protección Phase 1/2 incumplida: before=$($before | ConvertTo-Json -Compress) after=$($after | ConvertTo-Json -Compress)" }
$validation = Invoke-DuckDB @('-readonly','-csv',$database,'-f',$validator)
$result = $validation | ConvertFrom-Csv | Select-Object -First 1
if ($result.status -ne 'PASS') { throw "Level A FAIL: $($validation -join ' ')" }
"LEVEL_A=$($result.status) MAPPINGS=$($result.mappings) CAPABILITIES=$($result.capabilities) EXCEPTIONS=$($result.exceptions) INVALID_REFERENCES=$($result.invalid_references) INVALID_STATES=$($result.invalid_states) MISSING_REQUIRED_REASONS=$($result.missing_required_reasons)"
"TEST_FIXTURES=PASS (SYNTHETIC_TEST; TRANSACTION_ROLLED_BACK)"
"PHASE2_BEFORE=$($before | ConvertTo-Json -Compress)"
"PHASE2_AFTER=$($after | ConvertTo-Json -Compress)"
