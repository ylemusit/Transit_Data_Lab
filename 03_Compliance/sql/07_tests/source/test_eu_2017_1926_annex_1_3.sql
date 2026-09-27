CREATE OR REPLACE TEMP TABLE expected_annex_1_3
(
    provision_id VARCHAR PRIMARY KEY,
    provision_type VARCHAR NOT NULL,
    section VARCHAR NOT NULL
);

INSERT INTO expected_annex_1_3 VALUES
('EU-2017-1926-ANNEX-1.3-A',     'ANNEX_GROUP',  '1.3(a)'),
('EU-2017-1926-ANNEX-1.3-A-I',   'DATA_ELEMENT', '1.3(a)(i)'),
('EU-2017-1926-ANNEX-1.3-A-II',  'DATA_ELEMENT', '1.3(a)(ii)'),
('EU-2017-1926-ANNEX-1.3-A-III', 'DATA_ELEMENT', '1.3(a)(iii)'),
('EU-2017-1926-ANNEX-1.3-A-IV',  'DATA_ELEMENT', '1.3(a)(iv)'),
('EU-2017-1926-ANNEX-1.3-A-V',   'DATA_ELEMENT', '1.3(a)(v)'),

('EU-2017-1926-ANNEX-1.3-B',     'ANNEX_GROUP',  '1.3(b)'),
('EU-2017-1926-ANNEX-1.3-B-I',   'DATA_ELEMENT', '1.3(b)(i)'),

('EU-2017-1926-ANNEX-1.3-C',     'ANNEX_GROUP',  '1.3(c)'),
('EU-2017-1926-ANNEX-1.3-C-I',   'DATA_ELEMENT', '1.3(c)(i)'),
('EU-2017-1926-ANNEX-1.3-C-II',  'DATA_ELEMENT', '1.3(c)(ii)'),
('EU-2017-1926-ANNEX-1.3-C-III', 'DATA_ELEMENT', '1.3(c)(iii)'),

('EU-2017-1926-ANNEX-1.3-D',     'ANNEX_GROUP',  '1.3(d)'),
('EU-2017-1926-ANNEX-1.3-D-I',   'DATA_ELEMENT', '1.3(d)(i)');


CREATE OR REPLACE TEMP VIEW actual_annex_1_3 AS
SELECT
    provision_id,
    provision_type,
    section,
    source_reference
FROM source.provisions
WHERE document_id = 'EU-REG-2017-1926'
  AND provision_id LIKE 'EU-2017-1926-ANNEX-1.3-%';


WITH test_results AS
(
    SELECT '01_EXPECTED_COUNT' test, 14 expected, COUNT(*) actual
    FROM actual_annex_1_3

    UNION ALL

    SELECT '02_DATA_ELEMENT_COUNT', 10, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT '03_GROUP_COUNT', 4, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT '04_MISSING_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_3
        EXCEPT
        SELECT provision_id FROM actual_annex_1_3
    )

    UNION ALL

    SELECT '05_UNEXPECTED_PROVISIONS', 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_3
        EXCEPT
        SELECT provision_id FROM expected_annex_1_3
    )

    UNION ALL

    SELECT '06_SECTION_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT '07_TYPE_MISMATCH', 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT '08_SOURCE_REFERENCE_NULL', 0, COUNT(*)
    FROM actual_annex_1_3
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


WITH test_results AS
(
    SELECT 14 expected, COUNT(*) actual
    FROM actual_annex_1_3

    UNION ALL

    SELECT 10, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'DATA_ELEMENT'

    UNION ALL

    SELECT 4, COUNT(*)
    FROM actual_annex_1_3
    WHERE provision_type = 'ANNEX_GROUP'

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM expected_annex_1_3
        EXCEPT
        SELECT provision_id FROM actual_annex_1_3
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM (
        SELECT provision_id FROM actual_annex_1_3
        EXCEPT
        SELECT provision_id FROM expected_annex_1_3
    )

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.section <> a.section

    UNION ALL

    SELECT 0, COUNT(*)
    FROM expected_annex_1_3 e
    JOIN actual_annex_1_3 a USING (provision_id)
    WHERE e.provision_type <> a.provision_type

    UNION ALL

    SELECT 0, COUNT(*)
    FROM actual_annex_1_3
    WHERE source_reference IS NULL
)

SELECT
    'ANNEX_1_3_SOURCE_INTEGRITY' AS test,
    CASE
        WHEN COUNT(*) FILTER (WHERE expected <> actual) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS status
FROM test_results;
