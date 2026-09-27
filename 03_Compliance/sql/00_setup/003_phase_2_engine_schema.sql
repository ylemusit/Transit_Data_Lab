-- Phase 2 additions. Phase 1 source tables are read-only inputs.
CREATE TABLE IF NOT EXISTS compliance.provision_classifications (
    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR NOT NULL,
    legal_classification VARCHAR NOT NULL CHECK (legal_classification IN
        ('DEFINITION','SCOPE','OBLIGATION','CONDITION','PERMISSION','EXCEPTION','DEADLINE','PROCEDURAL','REFERENCE','OTHER')),
    classification_notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_document_id, source_provision_id)
);

CREATE TABLE IF NOT EXISTS compliance.source_facts (
    source_fact_id VARCHAR PRIMARY KEY,
    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR NOT NULL,
    legal_reference VARCHAR NOT NULL,
    source_fact_text VARCHAR NOT NULL,
    source_version_date DATE NOT NULL,
    source_uri VARCHAR NOT NULL,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS compliance.requirement_candidates (
    candidate_id VARCHAR PRIMARY KEY,
    requirement_id VARCHAR UNIQUE,
    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR NOT NULL,
    source_fact_id VARCHAR NOT NULL,
    supporting_source_provision_id VARCHAR,
    legal_classification VARCHAR NOT NULL CHECK (legal_classification IN
        ('DEFINITION','SCOPE','OBLIGATION','CONDITION','PERMISSION','EXCEPTION','DEADLINE','PROCEDURAL','REFERENCE','OTHER')),
    requirement_class VARCHAR NOT NULL CHECK (requirement_class IN
        ('DATA_AVAILABILITY','ACCESS','FORMAT','INTEROPERABILITY','METADATA','UPDATE','QUALITY','DISCOVERY','REUSE','ROUTING','ASSESSMENT','REPORTING','DEADLINE','OTHER')),
    requirement_type VARCHAR,
    data_category VARCHAR,
    data_element VARCHAR,
    description VARCHAR NOT NULL,
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
    legal_status VARCHAR,
    review_status VARCHAR NOT NULL CHECK (review_status IN ('PENDING','APPROVED','REJECTED','NEEDS_REVIEW')),
    review_notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_fact_id) REFERENCES compliance.source_facts(source_fact_id)
);

CREATE INDEX IF NOT EXISTS idx_requirement_candidates_review
    ON compliance.requirement_candidates(review_status);
CREATE INDEX IF NOT EXISTS idx_requirement_candidates_source
    ON compliance.requirement_candidates(source_document_id, source_provision_id);

CREATE TABLE IF NOT EXISTS compliance.requirement_candidate_sources (
    candidate_id VARCHAR NOT NULL,
    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR NOT NULL,
    source_role VARCHAR NOT NULL CHECK (source_role IN ('ANNEX_SCOPE_SUPPORT','ADDITIONAL_SOURCE')),
    notes VARCHAR,
    PRIMARY KEY (candidate_id, source_provision_id),
    FOREIGN KEY (candidate_id) REFERENCES compliance.requirement_candidates(candidate_id)
);
