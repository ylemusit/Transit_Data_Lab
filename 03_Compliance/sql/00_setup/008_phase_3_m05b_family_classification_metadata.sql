-- M05B-SI: add planning-only classification metadata to family memberships.
-- Guarded one-time migration. Existing substantive rows cannot be assigned
-- invented classifications, so abort before changing the table if any exist.
BEGIN TRANSACTION;

SELECT CASE WHEN EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema='mapping' AND table_name='phase3_requirement_families'
) THEN 'M05B_TABLE_PRESENT' ELSE error('M05B family membership table missing') END;

SELECT CASE WHEN NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='mapping' AND table_name='phase3_requirement_families'
      AND column_name IN ('classification_reason','classification_confidence')
) THEN 'M05B_SCHEMA_NOT_ALREADY_MIGRATED'
ELSE error('M05B migration already applied; guarded one-time migration') END;

SELECT CASE WHEN NOT EXISTS (
    SELECT 1 FROM mapping.phase3_requirement_families
    WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
) THEN 'M05B_NO_SUBSTANTIVE_ROWS'
ELSE error('M05B unexpected substantive memberships; refusing to invent metadata') END;

CREATE TABLE mapping.phase3_requirement_families_m05b_new (
    requirement_id VARCHAR NOT NULL,
    family_id VARCHAR NOT NULL,
    relation_type VARCHAR NOT NULL CHECK (relation_type IN ('PRIMARY_FAMILY','SECONDARY_CHARACTERISTIC')),
    review_status VARCHAR NOT NULL CHECK (review_status IN ('UNREVIEWED','NEEDS_REVIEW','REVIEWED','APPROVED','REJECTED')),
    fixture_kind VARCHAR CHECK (fixture_kind IS NULL OR fixture_kind='SYNTHETIC_TEST'),
    classification_reason VARCHAR,
    classification_confidence VARCHAR,
    PRIMARY KEY(requirement_id, family_id, relation_type),
    FOREIGN KEY (family_id) REFERENCES mapping.phase3_families(family_id),
    CHECK (coalesce(fixture_kind,'')='SYNTHETIC_TEST' OR length(trim(coalesce(classification_reason,''))) > 0),
    CHECK (coalesce(fixture_kind,'')='SYNTHETIC_TEST' OR classification_confidence IN ('HIGH','MEDIUM','LOW'))
);

INSERT INTO mapping.phase3_requirement_families_m05b_new
    (requirement_id,family_id,relation_type,review_status,fixture_kind,classification_reason,classification_confidence)
SELECT requirement_id,family_id,relation_type,review_status,fixture_kind,NULL,NULL
FROM mapping.phase3_requirement_families;

SELECT CASE WHEN
    (SELECT count(*) FROM mapping.phase3_requirement_families_m05b_new)=
    (SELECT count(*) FROM mapping.phase3_requirement_families)
    AND (SELECT count(*) FROM mapping.phase3_requirement_families_m05b_new)=0
THEN 'M05B_ROW_PRESERVATION_VALIDATED' ELSE error('M05B row preservation validation failed') END;

DROP TABLE mapping.phase3_requirement_families;
ALTER TABLE mapping.phase3_requirement_families_m05b_new RENAME TO phase3_requirement_families;

SELECT CASE WHEN
    (SELECT count(*) FROM information_schema.table_constraints
     WHERE table_schema='mapping' AND table_name='phase3_requirement_families' AND constraint_type='PRIMARY KEY')=1
    AND (SELECT count(*) FROM information_schema.table_constraints
     WHERE table_schema='mapping' AND table_name='phase3_requirement_families' AND constraint_type='FOREIGN KEY')=1
    AND (SELECT count(*) FROM mapping.phase3_requirement_families)=0
THEN 'M05B_POST_RECONSTRUCTION_VALIDATION_PASS'
ELSE error('M05B post-reconstruction validation failed') END;

COMMIT;
