$ErrorActionPreference = 'Stop'
$complianceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$database = Join-Path $complianceRoot 'databases\transit_compliance.duckdb'
$setupRoot = Join-Path $complianceRoot 'sql\00_setup'
$testRoot = Join-Path $complianceRoot 'sql\07_tests\phase_3'
$migration = Join-Path $setupRoot '009_phase_3_m06_b01_unbound_capabilities.sql'
$duckdb = (Get-Command duckdb -ErrorAction Stop).Source

function Invoke-DuckDB([string[]]$Arguments, [switch]$ExpectFailure) {
    $output = & $duckdb @Arguments 2>&1
    $code = $LASTEXITCODE
    if ($ExpectFailure) {
        if ($code -eq 0) { throw "DuckDB aceptó una operación que debía rechazar: $($Arguments -join ' ')" }
    } elseif ($code -ne 0) { throw "DuckDB falló ($code): $output" }
    return $output
}
function Query([string]$Sql) {
    return (Invoke-DuckDB @('-readonly','-csv',$database,'-c',$Sql) | ConvertFrom-Csv | Select-Object -First 1)
}
function Run-Validator([string]$File, [string]$Column) {
    $path = Join-Path $testRoot $File
    $rows = Invoke-DuckDB @('-readonly','-csv',$database,'-f',$path) | ConvertFrom-Csv
    $row = $rows | Where-Object { $_.$Column } | Select-Object -First 1
    if (-not $row -or $row.$Column -ne 'PASS') { throw "$File no pasó: $($rows | ConvertTo-Json -Compress -Depth 4)" }
    return $row
}

$branch = git -C (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))) branch --show-current
$head = git -C (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))) rev-parse HEAD
$remote = git -C (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))) rev-parse origin/main
if ($branch -ne 'main' -or $head -ne 'd994b9b4975634072050cb8e1c094a038505016d' -or $remote -ne $head) {
    throw "Precondición Git no satisfecha: branch=$branch HEAD=$head origin/main=$remote"
}

$before = Query @"
SELECT (SELECT count(*) FROM compliance.requirements) requirements,
 (SELECT count(*) FROM compliance.deadlines) deadlines,
 (SELECT count(*) FROM compliance.requirement_candidates) candidates,
 (SELECT count(*) FROM compliance.source_facts) source_facts,
 (SELECT count(*) FROM mapping.phase3_standards) standards,
 (SELECT count(*) FROM mapping.phase3_capabilities) capabilities,
 (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id<>'NAP_DATA_DISCOVERY' AND standard_id IS NOT NULL) original_bound_capabilities,
 (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY' AND standard_id IS NULL) nap_unbound_capability,
 (SELECT count(*) FROM mapping.phase3_source_references) source_references,
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') substantive_mappings,
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities) all_mappings,
 (SELECT count(*) FROM mapping.phase3_mapping_reviews) mapping_reviews,
 (SELECT count(*) FROM mapping.phase3_requirement_coverage) coverage_decisions,
 (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') exceptions,
 (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') representability,
 (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') observed_evidence,
 (SELECT count(*) FROM audit.rules) audit_rules,
 (SELECT count(*) FROM mapping.phase3_families) families,
 (SELECT count(*) FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') family_memberships;
"@
$expected = @{requirements='48';deadlines='10';candidates='34';source_facts='36';standards='3';capabilities='6';original_bound_capabilities='5';nap_unbound_capability='1';source_references='8';substantive_mappings='6';all_mappings='6';mapping_reviews='6';coverage_decisions='8';exceptions='6';representability='0';observed_evidence='0';audit_rules='0';families='9';family_memberships='48'}
foreach ($key in $expected.Keys) { if ($before.$key -ne $expected[$key]) { throw "Conteo protegido previo inesperado: $key=$($before.$key), esperado $($expected[$key])" } }

$schema = Query "SELECT (SELECT is_nullable FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND column_name='standard_id') nullable,(SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND constraint_type='FOREIGN KEY') fk_count,(SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='SOURCE_KIND' AND value='OFFICIAL_LEGAL_SOURCE') legal_vocab;"
$shaBefore = (Get-FileHash $database -Algorithm SHA256).Hash
$alreadyMigrated = $schema.nullable -eq 'YES' -and $schema.legal_vocab -eq '1'
if (-not $alreadyMigrated) {
    $migrationOutput = Invoke-DuckDB @('-bail',$database,'-f',$migration)
    if (($migrationOutput -join "`n") -notmatch 'M06B01_ROW_AND_CONSTRAINT_PRESERVATION_PASS') { throw 'La migración no confirmó preservación de filas y estructura.' }
}
$shaAfter = (Get-FileHash $database -Algorithm SHA256).Hash
$schema = Query "SELECT (SELECT is_nullable FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND column_name='standard_id') nullable,(SELECT count(*) FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_capabilities' AND constraint_type='FOREIGN KEY') fk_count,(SELECT count(*) FROM mapping.phase3_vocabularies WHERE vocabulary='SOURCE_KIND' AND value='OFFICIAL_LEGAL_SOURCE') legal_vocab;"
if ($schema.nullable -ne 'YES' -or $schema.fk_count -ne '1' -or $schema.legal_vocab -ne '1') { throw "Esquema migrado inesperado: $($schema | ConvertTo-Json -Compress)" }

$cap='M06B01-SYNTHETIC-UNBOUND'
$map='M06B01-SYNTHETIC-MAPPING'
$src='M06B01-SYNTHETIC-LEGAL-SOURCE'
$fixture=@"
BEGIN TRANSACTION;
INSERT INTO mapping.phase3_capabilities(capability_id,standard_id,domain,entity,field_or_element,semantic_meaning,review_status,fixture_kind)
 VALUES ('$cap',NULL,'functional','test_entity','test_field','Synthetic unbound functional capability','NEEDS_REVIEW','SYNTHETIC_TEST');
INSERT INTO mapping.phase3_requirement_capabilities(mapping_id,requirement_id,capability_id,mapping_type,limitations,review_status,fixture_kind)
 VALUES ('$map','SYNTHETIC-REQUIREMENT','$cap','PARTIAL','Synthetic test only','NEEDS_REVIEW','SYNTHETIC_TEST');
INSERT INTO mapping.phase3_automatability(automatability_id,mapping_id,automatability_state,explanation,review_status,fixture_kind)
 VALUES ('M06B01-SYNTHETIC-AUTO','$map','PARTIAL','Synthetic test only','NEEDS_REVIEW','SYNTHETIC_TEST');
INSERT INTO mapping.phase3_source_references(source_reference_id,capability_id,source_kind,url_or_document_id,fixture_kind)
 VALUES ('$src','$cap','OFFICIAL_LEGAL_SOURCE','synthetic://legal-source','SYNTHETIC_TEST');
SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='$cap' AND standard_id IS NULL)=1
 AND (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE mapping_id='$map')=1
 AND (SELECT count(*) FROM mapping.phase3_automatability WHERE mapping_id='$map' AND automatability_state='PARTIAL')=1
 AND (SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id='$src' AND source_kind='OFFICIAL_LEGAL_SOURCE')=1
 THEN 'M06B01_SYNTHETIC_CAPABILITY_MAPPING_AUTOMATABILITY_AND_SOURCE_PASS' ELSE error('Synthetic unbound capability path failed') END;
ROLLBACK;
"@
$fixtureOutput = Invoke-DuckDB @('-bail',$database,'-c',$fixture)
if (($fixtureOutput -join "`n") -notmatch 'M06B01_SYNTHETIC_CAPABILITY_MAPPING_AUTOMATABILITY_AND_SOURCE_PASS') { throw 'Fixture unbound/legal source no pasó.' }

$unknown="BEGIN TRANSACTION; INSERT INTO mapping.phase3_capabilities(capability_id,standard_id,semantic_meaning,review_status,fixture_kind) VALUES ('M06B01-UNKNOWN-STANDARD','NO-SUCH-STANDARD','Synthetic invalid binding','NEEDS_REVIEW','SYNTHETIC_TEST'); ROLLBACK;"
Invoke-DuckDB @('-bail',$database,'-c',$unknown) -ExpectFailure | Out-Null
$remaining=Query "SELECT (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id LIKE 'M06B01-%') capabilities,(SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE mapping_id LIKE 'M06B01-%') mappings,(SELECT count(*) FROM mapping.phase3_automatability WHERE automatability_id LIKE 'M06B01-%') automatability,(SELECT count(*) FROM mapping.phase3_source_references WHERE source_reference_id LIKE 'M06B01-%') sources;"
if ($remaining.capabilities -ne '0' -or $remaining.mappings -ne '0' -or $remaining.automatability -ne '0' -or $remaining.sources -ne '0') { throw "Quedaron fixtures tras rollback: $($remaining | ConvertTo-Json -Compress)" }

$after=Query @"
SELECT (SELECT count(*) FROM compliance.requirements) requirements,
 (SELECT count(*) FROM compliance.deadlines) deadlines,
 (SELECT count(*) FROM compliance.requirement_candidates) candidates,
 (SELECT count(*) FROM compliance.source_facts) source_facts,
 (SELECT count(*) FROM mapping.phase3_standards) standards,
 (SELECT count(*) FROM mapping.phase3_capabilities) capabilities,
 (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id<>'NAP_DATA_DISCOVERY' AND standard_id IS NOT NULL) original_bound_capabilities,
 (SELECT count(*) FROM mapping.phase3_capabilities WHERE capability_id='NAP_DATA_DISCOVERY' AND standard_id IS NULL) nap_unbound_capability,
 (SELECT count(*) FROM mapping.phase3_source_references) source_references,
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') substantive_mappings,
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities) all_mappings,
 (SELECT count(*) FROM mapping.phase3_mapping_reviews) mapping_reviews,
 (SELECT count(*) FROM mapping.phase3_requirement_coverage) coverage_decisions,
 (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') exceptions,
 (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') representability,
 (SELECT count(*) FROM mapping.phase3_observed_evidence WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') observed_evidence,
 (SELECT count(*) FROM audit.rules) audit_rules,
 (SELECT count(*) FROM mapping.phase3_families) families,
 (SELECT count(*) FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') family_memberships;
"@
foreach ($key in $expected.Keys) { if ($after.$key -ne $expected[$key]) { throw "Conteo protegido posterior inesperado: $key=$($after.$key)" } }

$levelA=Run-Validator 'validate_phase_3_level_a.sql' 'status'
$m04=Run-Validator 'validate_phase_3_m04_pilot.sql' 'm04_pilot_structural_validation'
$m04b=Run-Validator 'validate_phase_3_m04b_semantic_coverage.sql' 'status'
$m05Schema=Query "SELECT count(*) cnt FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_requirement_families' AND column_name IN ('classification_reason','classification_confidence');"
if ($m05Schema.cnt -ne '2') { throw 'M05B schema regression failed.' }
$m05Family=Run-Validator 'validate_phase_3_m05b_family_baseline_v1.sql' 'family_baseline_validation'
$b01=Run-Validator 'validate_phase_3_m06_b01_candidates.sql' 'b01_structural_validation'
$accounting=Run-Validator 'validate_phase_3_exception_accounting.sql' 'global_exception_accounting'
$shaBeforeSecondRun=(Get-FileHash $database -Algorithm SHA256).Hash
Invoke-DuckDB @('-bail',$database,'-f',$migration) -ExpectFailure | Out-Null
$shaAfterSecondRun=(Get-FileHash $database -Algorithm SHA256).Hash
if ($shaBeforeSecondRun -ne $shaAfterSecondRun) { throw 'La segunda aplicación alteró la base.' }
if (-not $alreadyMigrated -and $shaBefore -eq $shaAfter) { throw 'Hash de base sin cambio tras migración de esquema.' }

"COMPLIANCE_PHASE3_M06_B01_MODEL_MIGRATION=PASS"
"BRANCH=$branch"; "HEAD=$head"; "REMOTE_MAIN=$remote"
"DB_SHA_BEFORE=$shaBefore"; "DB_SHA_AFTER=$shaAfter"
"STANDARD_BINDING_NULLABLE=$($schema.nullable)"; "NON_NULL_STANDARD_FK_ENFORCED=YES"
"CAPABILITY_KIND_ADDED=NO"; "N_TO_M_BINDING_ADDED=NO"; "FAKE_NAP_STANDARD_ADDED=NO"
"OFFICIAL_LEGAL_SOURCE_SUPPORTED=YES"; "SUBSTANTIVE_SOURCE_ROWS_ADDED=0"
"COUNTS_BEFORE=$($before | ConvertTo-Json -Compress)"; "COUNTS_AFTER=$($after | ConvertTo-Json -Compress)"
"NULL_STANDARD_FUNCTIONAL_CAPABILITY=PASS"; "UNKNOWN_NON_NULL_STANDARD=REJECTED"
"OFFICIAL_LEGAL_SOURCE_FIXTURE=PASS"; "REQUIREMENT_MAPPING_TO_UNBOUND_CAPABILITY=PASS"
"PARTIAL_AUTOMATABILITY_FOR_UNBOUND_MAPPING=PASS"; "ROLLBACK_CONFIRMED=YES"; "SYNTHETIC_ROWS_REMAINING=0"
"LEVEL_A=$($levelA.status)"; "M04=$($m04.m04_pilot_structural_validation)"; "M04B=$($m04b.status)"
"M05B_SCHEMA=PASS"; "M05B_FAMILY=$($m05Family.family_baseline_validation)"
"B01_REVIEWED=$($b01.b01_structural_validation)"; "GLOBAL_EXCEPTION_ACCOUNTING=$($accounting.global_exception_accounting)"
"MIGRATION_REPRODUCIBLE=YES (guarded one-time migration; second application refused without writes; runner repeatable)"
"SECOND_RUN_CHANGED_SUBSTANTIVE_COUNTS=NO"
"GIT_DIFF_CHECK=Run separately after runner output"
