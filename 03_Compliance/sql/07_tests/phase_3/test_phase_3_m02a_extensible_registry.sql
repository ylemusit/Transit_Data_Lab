BEGIN TRANSACTION;
INSERT INTO mapping.phase3_standards
    (standard_id, standard_name, standard_kind, registry_status)
VALUES
    ('TEST_STANDARD_DO_NOT_PERSIST', 'Synthetic future standard', 'FUTURE_DATA_STANDARD', 'IDENTITY_ONLY');
SELECT CASE WHEN count(*)=1 AND min(standard_name)='Synthetic future standard'
    THEN 'SYNTHETIC_INSERT_PASS' ELSE error('Unknown standard identity was rejected or altered') END
FROM mapping.phase3_standards WHERE standard_id='TEST_STANDARD_DO_NOT_PERSIST';
ROLLBACK;
SELECT CASE WHEN count(*)=0 THEN 'SYNTHETIC_ROLLBACK_PASS'
    ELSE error('Synthetic standard remained after rollback') END
FROM mapping.phase3_standards WHERE standard_id='TEST_STANDARD_DO_NOT_PERSIST';
