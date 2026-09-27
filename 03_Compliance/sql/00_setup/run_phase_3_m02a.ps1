$ErrorActionPreference = 'Stop'
$complianceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$database = Join-Path $complianceRoot 'databases\transit_compliance.duckdb'
$migration = Join-Path $PSScriptRoot '006_phase_3_m02a_generalize_standard_registry.sql'
$validator = Join-Path $complianceRoot 'sql\07_tests\phase_3\validate_phase_3_level_a.sql'
$extensibilityTest = Join-Path $complianceRoot 'sql\07_tests\phase_3\test_phase_3_m02a_extensible_registry.sql'
$m03Seed = Join-Path $complianceRoot 'sql\03_mappings\phase3_m03_seed.sql'
$m03Validator = Join-Path $complianceRoot 'sql\07_tests\phase_3\validate_phase_3_m03_evidence.sql'
$duckdb = (Get-Command duckdb -ErrorAction Stop).Source
function Invoke-DuckDB([string[]]$Arguments) {
    $output = & $duckdb @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) { throw "DuckDB falló ($LASTEXITCODE): $output" }
    return $output
}
function Get-Counts {
    $q = "SELECT (SELECT count(*) FROM compliance.requirements) requirements,(SELECT count(*) FROM compliance.deadlines) deadlines,(SELECT count(*) FROM compliance.requirement_candidates) candidates,(SELECT count(*) FROM compliance.source_facts) source_facts,(SELECT count(*) FROM audit.rules) audit_rules,(SELECT count(*) FROM mapping.phase3_standards) standards,(SELECT count(*) FROM mapping.phase3_capabilities) capabilities,(SELECT count(*) FROM mapping.phase3_source_references) source_references,(SELECT count(*) FROM mapping.phase3_exceptions) exceptions,(SELECT count(*) FROM mapping.phase3_requirement_capabilities) mappings,(SELECT count(*) FROM mapping.phase3_representability) representability;"
    $raw = Invoke-DuckDB @('-readonly','-csv',$database,'-c',$q)
    return ($raw | ConvertFrom-Csv | Select-Object -First 1)
}
$before = Get-Counts
if ($before.requirements -ne '48' -or $before.deadlines -ne '10' -or $before.candidates -ne '34' -or $before.source_facts -ne '36' -or $before.audit_rules -ne '0') { throw "Conteos protegidos iniciales inesperados: $($before | ConvertTo-Json -Compress)" }
if ($before.standards -ne '3' -or $before.capabilities -ne '5' -or $before.source_references -ne '7' -or $before.exceptions -ne '3' -or $before.mappings -ne '0' -or $before.representability -ne '0') { throw "Estado M03 inicial inesperado: $($before | ConvertTo-Json -Compress)" }
$migrationOutput = Invoke-DuckDB @('-bail',$database,'-f',$migration)
if (($migrationOutput -join "`n") -notmatch 'M02A_COPY_VALIDATION_PASS') { throw "Migración sin validación completa: $($migrationOutput -join ' ')" }
$syntheticOutput = Invoke-DuckDB @('-bail',$database,'-f',$extensibilityTest)
if (($syntheticOutput -join "`n") -notmatch 'SYNTHETIC_INSERT_PASS' -or ($syntheticOutput -join "`n") -notmatch 'SYNTHETIC_ROLLBACK_PASS') { throw "Prueba de extensibilidad fallida: $($syntheticOutput -join ' ')" }
$m03SeedOutput = Invoke-DuckDB @('-bail',$database,'-f',$m03Seed)
$after = Get-Counts
if (($before | ConvertTo-Json -Compress) -ne ($after | ConvertTo-Json -Compress)) { throw "Conteos protegidos o M03 cambiaron: before=$($before | ConvertTo-Json -Compress) after=$($after | ConvertTo-Json -Compress)" }
$timer = [System.Diagnostics.Stopwatch]::StartNew()
$levelAOutput = Invoke-DuckDB @('-readonly','-csv',$database,'-f',$validator)
$timer.Stop()
$levelA = $levelAOutput | ConvertFrom-Csv | Select-Object -First 1
if ($levelA.status -ne 'PASS') { throw "Level A FAIL: $($levelAOutput -join ' ')" }
$m03Output = Invoke-DuckDB @('-readonly','-csv',$database,'-f',$m03Validator)
$m03 = $m03Output | ConvertFrom-Csv | Select-Object -First 1
if ($m03.status -notin @('PASS','PARTIAL')) { throw "Validación M03 fallida: $($m03Output -join ' ')" }
"MIGRATION=PASS (transaction committed after row-for-row and FK validation)"
"SYNTHETIC_EXTENSIBILITY=PASS; ROLLBACK=PASS; ROWS_AFTER=0"
"M03_SEED=PASS (idempotent execution; substantive counts preserved)"
"LEVEL_A=$($levelA.status); RUNTIME_MS=$([int]$timer.Elapsed.TotalMilliseconds)"
"M03_EVIDENCE_VALIDATION=$($m03.status)"
"COUNTS_BEFORE=$($before | ConvertTo-Json -Compress)"
"COUNTS_AFTER=$($after | ConvertTo-Json -Compress)"
