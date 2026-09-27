[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$compliance = Join-Path $root '03_Compliance'
$db = Join-Path $compliance 'databases\transit_compliance.duckdb'
$baselineDir = Join-Path $compliance 'reports\phase_2\baseline'
$reportDir = Join-Path $compliance 'reports\phase_2'
$duckdbCommand = Get-Command duckdb -ErrorAction Stop
$duckdb = $duckdbCommand.Source

function Invoke-DuckDB {
    param([string[]]$Arguments)
    & $duckdb @Arguments
    if ($LASTEXITCODE -ne 0) { throw "DuckDB falló con exit code ${LASTEXITCODE}: $($Arguments -join ' ')" }
}

function Invoke-QueryCsv {
    param([string]$Query)
    $result = & $duckdb -readonly $db -csv -header -c $Query
    if ($LASTEXITCODE -ne 0) { throw "Falló la consulta DuckDB: $Query" }
    return @($result | ConvertFrom-Csv)
}

function Export-QueryCsv {
    param([string]$Query, [string]$Path)
    $safePath = $Path.Replace('\','/').Replace("'", "''")
    Invoke-DuckDB @($db,'-bail','-c',"COPY ($Query) TO '$safePath' (HEADER, DELIMITER ',');")
}

if (!(Test-Path -LiteralPath $db -PathType Leaf)) { throw "No existe la base de Compliance: $db" }
foreach ($required in @(
    'reports\phase_2\baseline\PHASE_1_SOURCE_DOCUMENTS.csv',
    'reports\phase_2\baseline\PHASE_1_SOURCE_PROVISIONS.csv',
    'reports\phase_2\baseline\PHASE_1_SOURCE_RELATIONSHIPS.csv',
    'sql\00_setup\003_phase_2_engine_schema.sql',
    'sql\00_setup\004_phase_2_2017_1926_seed.sql',
    'sql\07_tests\phase_2\test_phase_2_master.sql'
)) {
    $path = Join-Path $compliance $required
    if (!(Test-Path -LiteralPath $path -PathType Leaf)) { throw "Falta prerequisito: $path" }
}

$version = (& $duckdb --version | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $version -notmatch 'v?1\.5\.5') { throw "Se requiere DuckDB 1.5.5; detectado: $version" }

$engineTable = Invoke-QueryCsv "SELECT count(*) AS n FROM information_schema.tables WHERE table_schema='compliance' AND table_name='requirement_candidates';"
$engineExists = $engineTable[0].n -eq '1'
$baselineChecks = Invoke-QueryCsv "SELECT (SELECT count(*) FROM source.documents) docs,(SELECT count(*) FROM source.relationships) rels,(SELECT count(*) FROM source.provisions WHERE document_id='EU-REG-2017-1926') provisions,(SELECT count(*) FROM compliance.requirements) requirements,(SELECT count(*) FROM mapping.format_coverage) mappings,(SELECT count(*) FROM audit.rules) rules;"
$b = $baselineChecks[0]
if ($b.docs -ne '10' -or $b.rels -ne '6' -or $b.provisions -ne '92' -or (!$engineExists -and $b.requirements -ne '0') -or $b.mappings -ne '0' -or $b.rules -ne '0') {
    throw "Baseline detenido: docs=$($b.docs), relationships=$($b.rels), provisions=$($b.provisions), requirements=$($b.requirements), mappings=$($b.mappings), rules=$($b.rules). No se ha ejecutado la migración."
}

$workDir = Join-Path $env:TEMP ('phase_2_baseline_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $workDir | Out-Null
Push-Location $root
try {
    $tableQueries = [ordered]@{
        'PHASE_1_SOURCE_DOCUMENTS.csv' = 'SELECT * FROM source.documents ORDER BY document_id'
        'PHASE_1_SOURCE_PROVISIONS.csv' = 'SELECT * FROM source.provisions ORDER BY provision_id'
        'PHASE_1_SOURCE_RELATIONSHIPS.csv' = 'SELECT * FROM source.relationships ORDER BY relationship_id'
    }
    foreach ($name in $tableQueries.Keys) {
        $expected = Join-Path $baselineDir $name
        $actual = Join-Path $workDir $name
        Export-QueryCsv $tableQueries[$name] $actual
        $expectedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $expected).Hash
        $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $actual).Hash
        if ($expectedHash -ne $actualHash) { throw "Phase 1 baseline mismatch en $name; se detiene antes de migrar." }
    }

    $sourceRows = Invoke-QueryCsv "SELECT document_id,local_file,source_hash FROM source.documents WHERE source_hash IS NOT NULL ORDER BY document_id;"
    $sourcePass = 0
    foreach ($source in $sourceRows) {
        $sourcePath = if ([IO.Path]::IsPathRooted($source.local_file)) { $source.local_file } else { Join-Path $compliance $source.local_file }
        if (!(Test-Path -LiteralPath $sourcePath -PathType Leaf)) { throw "No existe la fuente legal $($source.document_id): $sourcePath" }
        $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash.ToLowerInvariant()
        if ($actualHash -ne $source.source_hash.ToLowerInvariant()) { throw "SHA-256 distinto para $($source.document_id); se detiene antes de migrar." }
        $sourcePass++
    }
    if ($sourcePass -ne 10) { throw "Esperadas 10 fuentes legales con hash; verificadas $sourcePass." }

    $scriptDir = Join-Path $compliance 'sql\00_setup'
    Invoke-DuckDB @($db,'-bail','-f',(Join-Path $scriptDir '003_phase_2_engine_schema.sql'))
    Invoke-DuckDB @($db,'-bail','-f',(Join-Path $scriptDir '004_phase_2_2017_1926_seed.sql'))

    $testOutput = & $duckdb -readonly $db -csv -header -f (Join-Path $compliance 'sql\07_tests\phase_2\test_phase_2_master.sql')
    if ($LASTEXITCODE -ne 0) { throw "El master Phase 2 terminó con exit code $LASTEXITCODE." }
    $testCsv = @($testOutput | ConvertFrom-Csv)
    $failed = @($testCsv | Where-Object status -ne 'PASS')
    if ($failed.Count -gt 0) { throw "Tests Phase 2 fallaron: $(($failed.test -join ', '))" }
    $sourceHashStatus = if ($sourcePass -eq 10) { 'PASS' } else { 'FAIL' }
    $testCsv += [pscustomobject]@{test='PHASE1_LEGAL_SOURCE_FILE_SHA256';status=$sourceHashStatus;expected=10;actual=$sourcePass}
    $failed = @($testCsv | Where-Object status -ne 'PASS')
    if ($failed.Count -gt 0) { throw "Tests Phase 2 o hashes externos fallaron: $(($failed.test -join ', '))" }
    $testCsv | Export-Csv -LiteralPath (Join-Path $reportDir 'PHASE_2_TEST_RESULTS.csv') -NoTypeInformation -Encoding utf8

    Export-QueryCsv "SELECT c.*,f.legal_reference,f.source_fact_text,f.source_version_date,f.source_uri,s.supporting_source_provision_ids FROM compliance.requirement_candidates c JOIN compliance.source_facts f USING(source_fact_id) LEFT JOIN (SELECT candidate_id,string_agg(source_provision_id,'; ' ORDER BY source_provision_id) supporting_source_provision_ids FROM compliance.requirement_candidate_sources GROUP BY candidate_id) s USING(candidate_id) ORDER BY c.candidate_id" (Join-Path $reportDir 'PHASE_2_CANDIDATES.csv')
    Export-QueryCsv "SELECT r.*,c.candidate_id,c.review_status,c.source_fact_id,f.legal_reference,f.source_fact_text,f.source_version_date FROM compliance.requirements r JOIN compliance.requirement_candidates c USING(requirement_id) JOIN compliance.source_facts f USING(source_fact_id) ORDER BY r.requirement_id" (Join-Path $reportDir 'PHASE_2_REQUIREMENTS.csv')
    Export-QueryCsv "SELECT * FROM compliance.deadlines ORDER BY deadline_id" (Join-Path $reportDir 'PHASE_2_DEADLINES.csv')
    Export-QueryCsv "SELECT p.provision_id,p.source_reference,p.heading,p.text_content,p.notes,'Preservada: el ID termina en -I pero source_reference es Annex 1.3(b)/(d), sin subinciso romano; Phase 2 no corrige Phase 1.' AS anomaly_note FROM source.provisions p WHERE p.document_id='EU-REG-2017-1926' AND p.provision_id IN ('EU-2017-1926-ANNEX-1.3-B-I','EU-2017-1926-ANNEX-1.3-D-I') ORDER BY p.provision_id" (Join-Path $reportDir 'PHASE_2_SOURCE_ANOMALIES.csv')

    $counts = Invoke-QueryCsv "SELECT (SELECT count(*) FROM source.provisions WHERE document_id='EU-REG-2017-1926') provisions_analysed,(SELECT count(*) FROM compliance.provision_classifications WHERE source_document_id='EU-REG-2017-1926') provisions_classified,(SELECT count(*) FROM compliance.requirement_candidates WHERE source_document_id='EU-REG-2017-1926') candidates,(SELECT count(*) FROM compliance.requirement_candidates WHERE source_document_id='EU-REG-2017-1926' AND review_status='APPROVED') approved,(SELECT count(*) FROM compliance.requirement_candidates WHERE source_document_id='EU-REG-2017-1926' AND review_status='NEEDS_REVIEW') needs_review,(SELECT count(*) FROM compliance.requirement_candidates WHERE source_document_id='EU-REG-2017-1926' AND review_status='REJECTED') rejected,(SELECT count(*) FROM compliance.deadlines WHERE source_document_id='EU-REG-2017-1926' AND deadline_date IS NOT NULL) deadlines,(SELECT count(*) FROM source.provisions WHERE provision_id IN ('EU-2017-1926-ANNEX-1.3-B-I','EU-2017-1926-ANNEX-1.3-D-I')) anomalies,(SELECT count(*) FROM compliance.requirements) requirements,(SELECT count(*) FROM mapping.format_coverage) mappings,(SELECT count(*) FROM audit.rules) rules;"
    $c = $counts[0]
    $phase1Status = if ($testCsv.Where({$_.test -match '^1[789]_PHASE1_' -and $_.status -ne 'PASS'}).Count -eq 0 -and $sourcePass -eq 10) { 'PASS' } else { 'FAIL' }
    $testPass = @($testCsv | Where-Object status -eq 'PASS').Count
    $summary = @"
# Phase 2 — Legal Requirements Engine (2017/1926)

- Fecha de ejecución: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')
- Versión fuente: EU-REG-2017-1926 consolidada 2024-03-04; 10/10 hashes de fuentes legales verificados.
- Provisions analizadas/clasificadas: $($c.provisions_analysed) / $($c.provisions_classified)
- Candidates: $($c.candidates); APPROVED: $($c.approved); NEEDS_REVIEW: $($c.needs_review); REJECTED: $($c.rejected)
- Requirements materializados: $($c.requirements)
- Deadlines definitivas: $($c.deadlines)
- Anomalías Phase 1 registradas y preservadas: $($c.anomalies)
- Tests del master SQL y SHA-256 de ficheros fuente: $testPass/$($testCsv.Count) PASS, $($failed.Count) FAIL
- Protección Phase 1: $phase1Status (snapshots de documents/provisions/relationships iguales; 10/10 SHA-256 jurídicos iguales; 2017/1926 = 92 provisions)
- Fuera de alcance preservado: mapping.format_coverage=$($c.mappings), audit.rules=$($c.rules)

## Decisiones de extracción

- La clasificación de las 92 provisions no las convierte automáticamente en obligaciones.
- Solo se materializan deberes cuya cita indica directamente actor y acción (NAP del artículo 3(1) e informe del artículo 10(1)). El informe mantiene su fecha histórica vencida sin concluir incumplimiento.
- Los calendarios de artículos 4 y 5 quedan en revisión por excepciones, categorías y alcance de red/modos. Sus fechas solo se guardan como datos de candidatos.
- Requisitos de formato sujetos a otras normas, condiciones técnicas, alcance del artículo 5(4), calidad y atomicidad, reutilización neutral, corrección de datos y evaluación requieren revisión humana.
- Los extractos fuente y descripciones normalizadas están separados. No se modifica `source.provisions`.

## Revisión humana pendiente

1. Verificar las excepciones por datos y modo de transporte de cada fecha del artículo 4(3), y las categorías/redes del artículo 5(3).
2. Resolver responsabilidades, condiciones y granularidad de metadatos, acceso API, calidad, actualización, encaminamiento y reutilización.
3. Interpretar las remisiones a los actos externos listados en `PHASE_2_CANDIDATES.csv` sin ampliar aquí el corpus.
4. Revisar si las dos obligaciones aprobadas deben conservar su granularidad propuesta.
5. Mantener visibles los IDs Annex 1.3 B-I/D-I y confirmar su correspondencia jurídica en una tarea separada; no se corrigieron.

La extracción no afirma cumplimiento jurídico. Un error GTFS no es una conclusión de incumplimiento.

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"@
    Set-Content -LiteralPath (Join-Path $reportDir 'PHASE_2_SUMMARY.md') -Value $summary -Encoding utf8
    $summary
}
finally {
    Pop-Location
    Remove-Item -LiteralPath $workDir -Recurse -Force -ErrorAction SilentlyContinue
}
