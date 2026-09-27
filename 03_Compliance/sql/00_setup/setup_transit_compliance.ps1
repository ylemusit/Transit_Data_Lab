$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Database = "$Root\databases\transit_compliance.duckdb"
$SQLFile = "$Root\sql\00_setup\001_create_transit_compliance.sql"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " TRANSIT DATA LAB - COMPLIANCE SETUP" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# ------------------------------------------------------------
# Seguridad
# ------------------------------------------------------------

if (Test-Path $Database) {
    throw "La base ya existe: $Database"
}

# ------------------------------------------------------------
# SQL
# ------------------------------------------------------------

$SQL = @"
CREATE SCHEMA source;
CREATE SCHEMA compliance;
CREATE SCHEMA mapping;
CREATE SCHEMA audit;
CREATE SCHEMA analysis;


CREATE TABLE source.documents (
    document_id VARCHAR PRIMARY KEY,
    jurisdiction VARCHAR NOT NULL,
    authority VARCHAR,
    document_type VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    identifier VARCHAR,
    celex VARCHAR,
    boe_id VARCHAR,
    publication_date DATE,
    effective_date DATE,
    consolidated_date DATE,
    status VARCHAR,
    language VARCHAR DEFAULT 'ES',
    official_url VARCHAR,
    local_file VARCHAR,
    source_hash VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE source.provisions (
    provision_id VARCHAR PRIMARY KEY,
    document_id VARCHAR NOT NULL,
    provision_type VARCHAR,
    article VARCHAR,
    paragraph VARCHAR,
    annex VARCHAR,
    section VARCHAR,
    heading VARCHAR,
    text_content VARCHAR,
    source_reference VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE compliance.requirements (
    requirement_id VARCHAR PRIMARY KEY,
    jurisdiction VARCHAR NOT NULL,
    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR,
    requirement_class VARCHAR,
    requirement_type VARCHAR,
    data_category VARCHAR,
    data_element VARCHAR,
    description VARCHAR,
    transport_modes VARCHAR,
    geographic_scope VARCHAR,
    responsible_party VARCHAR,
    beneficiary_party VARCHAR,
    is_mandatory BOOLEAN,
    is_conditional BOOLEAN,
    condition_text VARCHAR,
    availability_requirement VARCHAR,
    accessibility_requirement VARCHAR,
    update_requirement VARCHAR,
    quality_requirement VARCHAR,
    interoperability_requirement VARCHAR,
    deadline_date DATE,
    effective_from DATE,
    effective_to DATE,
    legal_status VARCHAR,
    is_auditable BOOLEAN,
    validation_method VARCHAR,
    notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE compliance.deadlines (
    deadline_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR,
    jurisdiction VARCHAR,
    deadline_date DATE,
    deadline_type VARCHAR,
    description VARCHAR,
    scope_description VARCHAR,
    source_document_id VARCHAR,
    source_provision_id VARCHAR,
    notes VARCHAR
);


CREATE TABLE compliance.nap_requirements (
    nap_requirement_id VARCHAR PRIMARY KEY,
    source_document_id VARCHAR,
    source_provision_id VARCHAR,
    rule_type VARCHAR,
    category VARCHAR,
    description VARCHAR,
    severity VARCHAR,
    is_mandatory BOOLEAN,
    is_auditable BOOLEAN,
    validation_method VARCHAR,
    notes VARCHAR
);


CREATE TABLE mapping.format_coverage (
    mapping_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR NOT NULL,
    format_name VARCHAR NOT NULL,
    format_version VARCHAR,
    profile_name VARCHAR,
    coverage_status VARCHAR,
    source_file VARCHAR,
    source_entity VARCHAR,
    source_field VARCHAR,
    target_entity VARCHAR,
    target_field VARCHAR,
    transformation_required BOOLEAN,
    enrichment_required BOOLEAN,
    mapping_notes VARCHAR,
    evidence_text VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE mapping.format_equivalences (
    equivalence_id VARCHAR PRIMARY KEY,
    source_format VARCHAR NOT NULL,
    source_version VARCHAR,
    source_entity VARCHAR,
    source_field VARCHAR,
    target_format VARCHAR NOT NULL,
    target_version VARCHAR,
    target_profile VARCHAR,
    target_entity VARCHAR,
    target_field VARCHAR,
    mapping_type VARCHAR,
    information_loss BOOLEAN,
    enrichment_required BOOLEAN,
    notes VARCHAR
);


CREATE TABLE audit.rules (
    rule_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR,
    rule_family VARCHAR,
    rule_name VARCHAR NOT NULL,
    description VARCHAR,
    target_format VARCHAR,
    target_entity VARCHAR,
    target_field VARCHAR,
    severity VARCHAR,
    validation_engine VARCHAR,
    validation_expression VARCHAR,
    is_automatic BOOLEAN,
    legal_conclusion_allowed BOOLEAN DEFAULT FALSE,
    notes VARCHAR
);


CREATE TABLE audit.runs (
    audit_run_id VARCHAR PRIMARY KEY,
    dataset_name VARCHAR,
    operator_name VARCHAR,
    format_name VARCHAR,
    format_version VARCHAR,
    source_url VARCHAR,
    source_file VARCHAR,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR
);


CREATE TABLE audit.results (
    result_id VARCHAR PRIMARY KEY,
    audit_run_id VARCHAR NOT NULL,
    rule_id VARCHAR,
    requirement_id VARCHAR,
    result_status VARCHAR,
    severity VARCHAR,
    entity_id VARCHAR,
    field_name VARCHAR,
    observed_value VARCHAR,
    expected_value VARCHAR,
    message VARCHAR,
    evidence_text VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE audit.evidence (
    evidence_id VARCHAR PRIMARY KEY,
    audit_run_id VARCHAR,
    result_id VARCHAR,
    evidence_type VARCHAR,
    evidence_source VARCHAR,
    reference_text VARCHAR,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR
);


CREATE VIEW analysis.eu_requirements AS
SELECT *
FROM compliance.requirements
WHERE jurisdiction = 'EU';


CREATE VIEW analysis.spain_requirements AS
SELECT *
FROM compliance.requirements
WHERE jurisdiction = 'ES';


CREATE VIEW analysis.static_requirements AS
SELECT *
FROM compliance.requirements
WHERE UPPER(data_category) = 'STATIC';


CREATE VIEW analysis.dynamic_requirements AS
SELECT *
FROM compliance.requirements
WHERE UPPER(data_category) = 'DYNAMIC';


CREATE VIEW analysis.requirement_format_matrix AS
SELECT
    r.requirement_id,
    r.jurisdiction,
    r.data_category,
    r.data_element,
    r.description,

    MAX(CASE
        WHEN f.format_name = 'GTFS'
        THEN f.coverage_status
    END) AS gtfs,

    MAX(CASE
        WHEN f.format_name = 'GTFS-RT'
        THEN f.coverage_status
    END) AS gtfs_rt,

    MAX(CASE
        WHEN f.format_name = 'NeTEx'
        THEN f.coverage_status
    END) AS netex,

    MAX(CASE
        WHEN f.format_name = 'SIRI'
        THEN f.coverage_status
    END) AS siri

FROM compliance.requirements r

LEFT JOIN mapping.format_coverage f
    ON r.requirement_id = f.requirement_id

GROUP BY
    r.requirement_id,
    r.jurisdiction,
    r.data_category,
    r.data_element,
    r.description;


INSERT INTO source.documents (
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    status,
    language,
    local_file
)
VALUES
(
    'EU-DIR-2010-40',
    'EU',
    'European Union',
    'DIRECTIVE',
    'Directive 2010/40/EU',
    '2010/40/EU',
    '02010L0040-20231220',
    'CONSOLIDATED',
    'ES',
    'EU/01_Primary_Law/Directive_2010_40_EU/Directive_2010_40_EU_CONSOLIDATED_2023-12-20_ES.pdf'
),
(
    'EU-DIR-2023-2661',
    'EU',
    'European Union',
    'DIRECTIVE',
    'Directive (EU) 2023/2661',
    '2023/2661',
    '32023L2661',
    'ORIGINAL',
    'ES',
    'EU/01_Primary_Law/Directive_2023_2661/Directive_EU_2023_2661_ES.pdf'
),
(
    'EU-REG-2017-1926',
    'EU',
    'European Commission',
    'DELEGATED_REGULATION',
    'Commission Delegated Regulation (EU) 2017/1926',
    '2017/1926',
    '02017R1926-20240304',
    'CONSOLIDATED',
    'ES',
    'EU/01_Primary_Law/Regulation_2017_1926/Regulation_2017_1926_CONSOLIDATED_2024-03-04_ES.pdf'
),
(
    'EU-REG-2024-490',
    'EU',
    'European Commission',
    'DELEGATED_REGULATION',
    'Commission Delegated Regulation (EU) 2024/490',
    '2024/490',
    '32024R0490',
    'ORIGINAL',
    'ES',
    'EU/01_Primary_Law/Regulation_2024_490/Regulation_2024_490_ES.pdf'
),
(
    'ES-LAW-9-2025',
    'ES',
    'Jefatura del Estado',
    'LAW',
    'Ley 9/2025, de 3 de diciembre, de Movilidad Sostenible',
    'Ley 9/2025',
    NULL,
    'CONSOLIDATED',
    'ES',
    'Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_CONSOLIDATED_2026-03-21.pdf'
);
"@

$SQL | Set-Content -Path $SQLFile -Encoding UTF8

Write-Host ""
Write-Host "SQL creado:" -ForegroundColor Cyan
Write-Host $SQLFile

$DuckPath = $SQLFile.Replace("\", "/")

Write-Host ""
Write-Host "Creando base DuckDB..." -ForegroundColor Cyan

& duckdb $Database -c ".read '$DuckPath'"

if ($LASTEXITCODE -ne 0) {
    throw "DuckDB devolvio codigo de error $LASTEXITCODE"
}

Write-Host ""
Write-Host "Base creada correctamente." -ForegroundColor Green


# ------------------------------------------------------------
# VALIDACIÓN
# ------------------------------------------------------------

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " VALIDACION" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema IN (
    'source',
    'compliance',
    'mapping',
    'audit',
    'analysis'
)
ORDER BY table_schema, table_name;
"

Write-Host ""
Write-Host "DOCUMENTOS:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT
    document_id,
    jurisdiction,
    identifier,
    status
FROM source.documents
ORDER BY document_id;
"

Write-Host ""
Write-Host "CONTADORES:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT 'documents' AS entity, COUNT(*) AS records
FROM source.documents

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
Write-Host "PRUEBA analysis.eu_requirements:" -ForegroundColor Cyan

& duckdb $Database -c "
SELECT COUNT(*) AS eu_requirements
FROM analysis.eu_requirements;
"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host " SETUP COMPLETADO" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green

Write-Host ""
Write-Host "Base:" -ForegroundColor Cyan
Write-Host $Database

Write-Host ""
Write-Host "Para abrirla:" -ForegroundColor Cyan
Write-Host "duckdb `"$Database`""

