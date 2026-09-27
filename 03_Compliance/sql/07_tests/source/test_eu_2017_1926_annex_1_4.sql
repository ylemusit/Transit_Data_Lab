CREATE OR REPLACE TEMP TABLE expected_annex_1_4
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);

INSERT INTO expected_annex_1_4 VALUES

('EU-2017-1926-ANNEX-1.4-A',     'DATA_ELEMENT', '1.4(a)'),

('EU-2017-1926-ANNEX-1.4-B',     'ANNEX_GROUP',  '1.4(b)'),
('EU-2017-1926-ANNEX-1.4-B-I',   'DATA_ELEMENT', '1.4(b)(i)'),
('EU-2017-1926-ANNEX-1.4-B-II',  'DATA_ELEMENT', '1.4(b)(ii)'),
('EU-2017-1926-ANNEX-1.4-B-III', 'DATA_ELEMENT', '1.4(b)(iii)'),
('EU-2017-1926-ANNEX-1.4-B-IV',  'DATA_ELEMENT', '1.4(b)(iv)'),

('EU-2017-1926-ANNEX-1.4-C',     'ANNEX_GROUP',  '1.4(c)'),
('EU-2017-1926-ANNEX-1.4-C-I',   'DATA_ELEMENT', '1.4(c)(i)'),
('EU-2017-1926-ANNEX-1.4-C-II',  'DATA_ELEMENT', '1.4(c)(ii)'),
('EU-2017-1926-ANNEX-1.4-C-III', 'DATA_ELEMENT', '1.4(c)(iii)'),
('EU-2017-1926-ANNEX-1.4-C-IV',  'DATA_ELEMENT', '1.4(c)(iv)'),

('EU-2017-1926-ANNEX-1.4-D',     'DATA_ELEMENT', '1.4(d)');


CREATE OR REPLACE TEMP VIEW actual_annex_1_4 AS
SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.4-%';


WITH test_results AS
(
    SELECT '01_EXPECTED_COUNT' test, 12 expected, COUNT(*) actual
    FROM actual_annex_1_4

    UNION ALL

    SELECT '02_DATA_ELEMENT_COUNT', 10, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT '03_GROUP_COUNT', 2, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT '04_MISSING_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_4
        EXCEPT
        SELECT provision_id FROM actual_annex_1_4
    )

    UNION ALL

    SELECT '05_UNEXPECTED_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_4
        EXCEPT
        SELECT provision_id FROM expected_annex_1_4
    )

    UNION ALL

    SELECT '06_SECTION_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT '07_TYPE_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT '08_SOURCE_REFERENCE_NULL', 0, COUNT(*)
    FROM actual_annex_1_4
    WHERE source_reference IS NULL
),

evaluated AS
(
    SELECT
        test,
        CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END status,
        expected,
        actual
    FROM test_results
)

SELECT *
FROM evaluated
ORDER BY test;


WITH checks AS
(
    SELECT 12 expected, COUNT(*) actual
    FROM actual_annex_1_4

    UNION ALL

    SELECT 10, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 2, COUNT(*)
    FROM actual_annex_1_4
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_4
        EXCEPT
        SELECT provision_id FROM actual_annex_1_4
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_4
        EXCEPT
        SELECT provision_id FROM expected_annex_1_4
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_4 e
    JOIN actual_annex_1_4 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_1_4
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_1_4_SOURCE_INTEGRITY' AS test,
    CASE
        WHEN COUNT(*) FILTER (WHERE expected <> actual) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM checks;
