$ErrorActionPreference = 'Stop'
$complianceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$database = Join-Path $complianceRoot 'databases\transit_compliance.duckdb'
$duckdb = (Get-Command duckdb -ErrorAction Stop).Source

function Invoke-DuckDB([string[]]$Arguments, [switch]$ExpectFailure) {
    $output = & $duckdb @Arguments 2>&1
    $code = $LASTEXITCODE
    if ($ExpectFailure) {
        if ($code -eq 0) { throw "Se aceptó una inserción inválida: $($Arguments -join ' ')" }
    } elseif ($code -ne 0) { throw "DuckDB falló ($code): $output" }
    return $output
}

$schemaSql = "SELECT column_name,data_type,is_nullable FROM information_schema.columns WHERE table_schema='mapping' AND table_name='phase3_requirement_families' AND column_name IN ('classification_reason','classification_confidence') ORDER BY column_name;"
$schema = Invoke-DuckDB @('-readonly','-csv',$database,'-c',$schemaSql) | ConvertFrom-Csv
if ($schema.Count -ne 2 -or ($schema | Where-Object column_name -eq 'classification_reason').data_type -ne 'VARCHAR' -or ($schema | Where-Object column_name -eq 'classification_confidence').data_type -ne 'VARCHAR') { throw 'Columnas M05B no disponibles con tipo esperado.' }

$constraints = Invoke-DuckDB @('-readonly','-csv',$database,'-c',"SELECT constraint_type FROM information_schema.table_constraints WHERE table_schema='mapping' AND table_name='phase3_requirement_families';") | ConvertFrom-Csv
if (@($constraints | Where-Object constraint_type -eq 'PRIMARY KEY').Count -ne 1 -or @($constraints | Where-Object constraint_type -eq 'FOREIGN KEY').Count -ne 1) { throw 'PK/FK de membresías no preservadas.' }

$id='M05B-SYNTHETIC-FAMILY'
$rid='M05B-SYNTHETIC-REQUIREMENT'
$seed="INSERT INTO mapping.phase3_families(family_id,family_name,description,provisional) VALUES ('$id','$id','rolled back M05B test',TRUE);"
$base="INSERT INTO mapping.phase3_requirement_families(requirement_id,family_id,relation_type,review_status,fixture_kind,classification_reason,classification_confidence) VALUES ('$rid','$id','PRIMARY_FAMILY','UNREVIEWED',NULL,'reason','HIGH');"
Invoke-DuckDB @('-bail',$database,'-c',"BEGIN TRANSACTION; $seed INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','$id','PRIMARY_FAMILY','UNREVIEWED',NULL,'','HIGH'); ROLLBACK;") -ExpectFailure | Out-Null
Invoke-DuckDB @('-bail',$database,'-c',"BEGIN TRANSACTION; $seed INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','$id','PRIMARY_FAMILY','UNREVIEWED',NULL,'reason','INVALID'); ROLLBACK;") -ExpectFailure | Out-Null
Invoke-DuckDB @('-bail',$database,'-c',"BEGIN TRANSACTION; $seed INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','$id','INVALID_RELATION','UNREVIEWED',NULL,'reason','HIGH'); ROLLBACK;") -ExpectFailure | Out-Null
Invoke-DuckDB @('-bail',$database,'-c',"BEGIN TRANSACTION; $seed INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','$id','PRIMARY_FAMILY','INVALID_REVIEW',NULL,'reason','HIGH'); ROLLBACK;") -ExpectFailure | Out-Null
Invoke-DuckDB @('-bail',$database,'-c',"BEGIN TRANSACTION; INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','M05B-NO-SUCH-FAMILY','PRIMARY_FAMILY','UNREVIEWED',NULL,'reason','HIGH'); ROLLBACK;") -ExpectFailure | Out-Null

$validSql = @"
BEGIN TRANSACTION;
$seed
$base
INSERT INTO mapping.phase3_requirement_families VALUES ('$rid','$id','SECONDARY_CHARACTERISTIC','UNREVIEWED',NULL,'planning reason','MEDIUM');
INSERT INTO mapping.phase3_requirement_families VALUES ('M05B-FIXTURE-NULL','$id','PRIMARY_FAMILY','UNREVIEWED','SYNTHETIC_TEST',NULL,NULL);
INSERT INTO mapping.phase3_requirement_families VALUES ('M05B-LOW','$id','PRIMARY_FAMILY','UNREVIEWED','SYNTHETIC_TEST','planning reason','LOW');
ROLLBACK;
"@
Invoke-DuckDB @('-bail',$database,'-c',$validSql) | Out-Null
$left = Invoke-DuckDB @('-readonly','-csv',$database,'-c',"SELECT (SELECT count(*) FROM mapping.phase3_requirement_families WHERE fixture_kind='SYNTHETIC_TEST') synthetic_memberships,(SELECT count(*) FROM mapping.phase3_requirement_families WHERE requirement_id LIKE 'M05B-%') m05b_memberships,(SELECT count(*) FROM mapping.phase3_families WHERE family_id='$id') synthetic_families;") | ConvertFrom-Csv | Select-Object -First 1
if ($left.synthetic_memberships -ne '0' -or $left.m05b_memberships -ne '0' -or $left.synthetic_families -ne '0') { throw "Fixture no revirtió completamente: $($left | ConvertTo-Json -Compress)" }

$future = Invoke-DuckDB @('-readonly','-csv',$database,'-c',@"
WITH totals AS (
 SELECT count(*) total_requirements,
   (SELECT count(*) FROM mapping.phase3_requirement_families WHERE relation_type='PRIMARY_FAMILY' AND fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') primary_assignments,
   (SELECT count(*) FROM mapping.phase3_requirement_families m WHERE relation_type='PRIMARY_FAMILY' AND fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND NOT EXISTS (SELECT 1 FROM compliance.requirements r WHERE r.requirement_id=m.requirement_id)) unknown_requirement_ids,
   (SELECT count(*) FROM compliance.requirements r WHERE (SELECT count(*) FROM mapping.phase3_requirement_families m WHERE m.requirement_id=r.requirement_id AND m.relation_type='PRIMARY_FAMILY' AND m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST')=0) records_without_primary,
   (SELECT count(*) FROM (SELECT requirement_id FROM mapping.phase3_requirement_families WHERE relation_type='PRIMARY_FAMILY' AND fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' GROUP BY requirement_id HAVING count(*)>1)) records_with_multiple_primary,
   (SELECT count(*) FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND coalesce(classification_confidence,'') NOT IN ('HIGH','MEDIUM','LOW')) invalid_confidence,
   (SELECT count(*) FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' AND length(trim(coalesce(classification_reason,'')))=0) missing_reason,
   (SELECT count(*) FROM (SELECT requirement_id,family_id,relation_type FROM mapping.phase3_requirement_families WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST' GROUP BY 1,2,3 HAVING count(*)>1)) duplicate_membership
 FROM compliance.requirements
)
SELECT *, CASE WHEN total_requirements=48 AND primary_assignments=48 AND records_without_primary=0 AND records_with_multiple_primary=0 AND unknown_requirement_ids=0 AND invalid_confidence=0 AND missing_reason=0 AND duplicate_membership=0 THEN 'YES' ELSE 'NO' END family_baseline_complete
FROM totals;
"@) | ConvertFrom-Csv | Select-Object -First 1
if ($future.total_requirements -ne '48' -or $future.family_baseline_complete -ne 'YES') { throw "Baseline M05B no completa tras la clasificación: $($future | ConvertTo-Json -Compress)" }

'SCHEMA_READY=YES'
'FAMILY_BASELINE_COMPLETE=YES'
"TOTAL_REQUIREMENTS=$($future.total_requirements)"
"PRIMARY_ASSIGNMENTS=$($future.primary_assignments)"
"RECORDS_WITHOUT_PRIMARY=$($future.records_without_primary)"
"RECORDS_WITH_MULTIPLE_PRIMARY=$($future.records_with_multiple_primary)"
"UNKNOWN_REQUIREMENT_IDS=$($future.unknown_requirement_ids)"
"INVALID_CONFIDENCE=$($future.invalid_confidence)"
"MISSING_REASON=$($future.missing_reason)"
"DUPLICATE_MEMBERSHIP=$($future.duplicate_membership)"
'INVALID_CONFIDENCE_REJECTED=YES'
'BLANK_REASON_REJECTED=YES'
'HIGH_ACCEPTED=YES'
'MEDIUM_ACCEPTED=YES'
'LOW_ACCEPTED=YES'
'PRIMARY_SYNTHETIC_ACCEPTED=YES'
'SECONDARY_SYNTHETIC_ACCEPTED=YES'
'FIXTURE_KIND_NULL_METADATA_ACCEPTED=YES'
'SYNTHETIC_ROWS_AFTER_ROLLBACK=0'
'EXISTING_PK_PRESERVED=YES'
'EXISTING_FK_PRESERVED=YES'
'RELATION_VOCABULARY_PRESERVED=YES'
'REVIEW_STATUS_VOCABULARY_PRESERVED=YES'
'FIXTURE_KIND_PRESERVED=YES'
