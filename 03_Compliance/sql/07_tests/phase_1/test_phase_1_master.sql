CREATE OR REPLACE TEMP TABLE phase1_expected_documents
(
    document_id VARCHAR PRIMARY KEY,
    expected_status VARCHAR,
    corpus_role VARCHAR
);

INSERT INTO phase1_expected_documents VALUES

('EU-DIR-2010-40',
 'ACTIVE',
 'EU_FRAMEWORK'),

('EU-DIR-2023-2661',
 'ACTIVE',
 'EU_AMENDMENT'),

('EU-REG-2017-1926',
 'ACTIVE',
 'MMTIS_CORE'),

('EU-REG-2024-490',
 'ACTIVE',
 'MMTIS_AMENDMENT'),

('EU-REG-2024-1679',
 'ACTIVE',
 'TEN_T_URBAN_MOBILITY'),

('EU-REG-IMPL-2026-1554',
 'ACTIVE',
 'URBAN_MOBILITY_DATA'),

('EU-REG-IMPL-2026-253',
 'ACTIVE',
 'RAIL_DATA_INTEROPERABILITY'),

('EU-REG-2011-454',
 'HISTORICAL',
 'RAIL_HISTORICAL'),

('EU-REG-2014-1305',
 'HISTORICAL',
 'RAIL_HISTORICAL'),

('ES-LAW-9-2025',
 'ACTIVE',
 'SPAIN_MOBILITY_FRAMEWORK');


-- ============================================================
-- EXPECTED LEGAL RELATIONSHIPS
-- ============================================================

CREATE OR REPLACE TEMP TABLE phase1_expected_relationships
(
    relationship_id VARCHAR PRIMARY KEY
);

INSERT INTO phase1_expected_relationships VALUES

('REL-EU-2023-2661-AMENDS-2010-40'),

('REL-EU-2024-490-AMENDS-2017-1926'),

('REL-EU-2026-1554-IMPLEMENTS-2024-1679'),

('REL-EU-2026-1554-REFERENCES-2017-1926'),

('REL-EU-2026-253-REPEALS-2011-454'),

('REL-EU-2026-253-REPEALS-2014-1305');


-- ============================================================
-- MASTER TESTS
-- ============================================================

WITH tests AS
(

    SELECT
        '01_EXPECTED_DOCUMENTS_PRESENT' AS test,
        0 AS expected,
        COUNT(*) AS actual

    FROM
    (
        SELECT document_id
        FROM phase1_expected_documents

        EXCEPT

        SELECT document_id
        FROM source.documents
    )


    UNION ALL


    SELECT
        '02_EXPECTED_DOCUMENT_COUNT',
        10,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )


    UNION ALL


    SELECT
        '03_DOCUMENT_ID_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND document_id IS NULL


    UNION ALL


    SELECT
        '04_DOCUMENT_TITLE_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND (
          title IS NULL
          OR TRIM(title) = ''
      )


    UNION ALL


    SELECT
        '05_DOCUMENT_TYPE_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND (
          document_type IS NULL
          OR TRIM(document_type) = ''
      )


    UNION ALL


    SELECT
        '06_JURISDICTION_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND (
          jurisdiction IS NULL
          OR TRIM(jurisdiction) = ''
      )


    UNION ALL


    SELECT
        '07_OFFICIAL_URL_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND (
          official_url IS NULL
          OR TRIM(official_url) = ''
      )


    UNION ALL


    SELECT
        '08_LOCAL_FILE_NULL',
        0,
        COUNT(*)

    FROM source.documents

    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
      AND (
          local_file IS NULL
          OR TRIM(local_file) = ''
      )


    UNION ALL


    SELECT
        '09_EXPECTED_RELATIONSHIPS_MISSING',
        0,
        COUNT(*)

    FROM
    (
        SELECT relationship_id
        FROM phase1_expected_relationships

        EXCEPT

        SELECT relationship_id
        FROM source.relationships
    )


    UNION ALL


    SELECT
        '10_EXPECTED_RELATIONSHIP_COUNT',
        6,
        COUNT(*)

    FROM source.relationships

    WHERE relationship_id IN (
        SELECT relationship_id
        FROM phase1_expected_relationships
    )


    UNION ALL


    SELECT
        '11_RELATIONSHIP_SOURCE_MISSING',
        0,
        COUNT(*)

    FROM source.relationships r

    LEFT JOIN source.documents d
      ON r.source_document_id = d.document_id

    WHERE r.relationship_id IN (
        SELECT relationship_id
        FROM phase1_expected_relationships
    )
      AND d.document_id IS NULL


    UNION ALL


    SELECT
        '12_RELATIONSHIP_TARGET_MISSING',
        0,
        COUNT(*)

    FROM source.relationships r

    LEFT JOIN source.documents d
      ON r.target_document_id = d.document_id

    WHERE r.relationship_id IN (
        SELECT relationship_id
        FROM phase1_expected_relationships
    )
      AND d.document_id IS NULL


    UNION ALL


    -- 2017/1926 frozen structural baseline

    SELECT
        '13_2017_1926_PROVISION_COUNT',
        92,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'


    UNION ALL


    SELECT
        '14_2017_1926_ARTICLES',
        11,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ARTICLE'


    UNION ALL


    SELECT
        '15_2017_1926_ANNEX_LEVELS',
        7,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX_LEVEL'


    UNION ALL


    SELECT
        '16_2017_1926_ANNEX_GROUPS',
        14,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'ANNEX_GROUP'


    UNION ALL


    SELECT
        '17_2017_1926_DATA_ELEMENTS',
        57,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
      AND provision_type = 'DATA_ELEMENT'


    UNION ALL


    SELECT
        '18_2017_1926_SOURCE_REFERENCE_NULL',
        0,
        COUNT(*)

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'

      AND provision_type IN (
          'ANNEX',
          'ANNEX_SECTION',
          'ANNEX_LEVEL',
          'ANNEX_GROUP',
          'DATA_ELEMENT'
      )

      AND (
          source_reference IS NULL
          OR TRIM(source_reference) = ''
      )


    UNION ALL


    SELECT
        '19_DUPLICATE_DOCUMENT_IDS',
        0,
        COUNT(*)

    FROM
    (
        SELECT document_id
        FROM source.documents
        GROUP BY document_id
        HAVING COUNT(*) > 1
    )


    UNION ALL


    SELECT
        '20_DUPLICATE_RELATIONSHIP_IDS',
        0,
        COUNT(*)

    FROM
    (
        SELECT relationship_id
        FROM source.relationships
        GROUP BY relationship_id
        HAVING COUNT(*) > 1
    )


    UNION ALL


    SELECT
        '21_DUPLICATE_PROVISION_IDS',
        0,
        COUNT(*)

    FROM
    (
        SELECT provision_id
        FROM source.provisions
        GROUP BY provision_id
        HAVING COUNT(*) > 1
    )


    UNION ALL


    -- Phase 1 must NOT contain derived compliance logic yet

    SELECT
        '22_REQUIREMENTS_NOT_DERIVED_YET',
        0,
        COUNT(*)

    FROM compliance.requirements


    UNION ALL


    SELECT
        '23_FORMAT_MAPPING_NOT_DERIVED_YET',
        0,
        COUNT(*)

    FROM mapping.format_coverage


    UNION ALL


    SELECT
        '24_AUDIT_RULES_NOT_CREATED_YET',
        0,
        COUNT(*)

    FROM audit.rules
),

evaluated AS
(
    SELECT
        test,

        CASE
            WHEN expected = actual
            THEN 'PASS'
            ELSE 'FAIL'
        END AS status,

        expected,
        actual

    FROM tests
)

SELECT *
FROM evaluated
ORDER BY test;


-- ============================================================
-- GLOBAL PHASE 1 RESULT
-- ============================================================

WITH tests AS
(
    SELECT
        COUNT(*) AS missing_documents
    FROM
    (
        SELECT document_id
        FROM phase1_expected_documents
        EXCEPT
        SELECT document_id
        FROM source.documents
    )
),

relationships AS
(
    SELECT
        COUNT(*) AS missing_relationships
    FROM
    (
        SELECT relationship_id
        FROM phase1_expected_relationships
        EXCEPT
        SELECT relationship_id
        FROM source.relationships
    )
),

doc_quality AS
(
    SELECT
        COUNT(*) AS errors
    FROM source.documents
    WHERE document_id IN (
        SELECT document_id
        FROM phase1_expected_documents
    )
    AND (
        title IS NULL
        OR TRIM(title) = ''
        OR document_type IS NULL
        OR TRIM(document_type) = ''
        OR jurisdiction IS NULL
        OR TRIM(jurisdiction) = ''
        OR official_url IS NULL
        OR TRIM(official_url) = ''
        OR local_file IS NULL
        OR TRIM(local_file) = ''
    )
),

r1926 AS
(
    SELECT
        COUNT(*) AS total,

        COUNT(*) FILTER (
            WHERE provision_type = 'ARTICLE'
        ) AS articles,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX'
        ) AS annex_root,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_SECTION'
        ) AS annex_sections,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_LEVEL'
        ) AS annex_levels,

        COUNT(*) FILTER (
            WHERE provision_type = 'ANNEX_GROUP'
        ) AS annex_groups,

        COUNT(*) FILTER (
            WHERE provision_type = 'DATA_ELEMENT'
        ) AS data_elements

    FROM source.provisions

    WHERE document_id = 'EU-REG-2017-1926'
)

SELECT
    'PHASE_1_CORPUS_INTEGRITY' AS test,

    CASE
        WHEN
            t.missing_documents = 0
            AND r.missing_relationships = 0
            AND q.errors = 0

            AND x.total = 92
            AND x.articles = 11
            AND x.annex_root = 1
            AND x.annex_sections = 2
            AND x.annex_levels = 7
            AND x.annex_groups = 14
            AND x.data_elements = 57

            AND (SELECT COUNT(*) FROM compliance.requirements) = 0
            AND (SELECT COUNT(*) FROM mapping.format_coverage) = 0
            AND (SELECT COUNT(*) FROM audit.rules) = 0

        THEN 'PASS'
        ELSE 'FAIL'
    END AS status

FROM tests t
CROSS JOIN relationships r
CROSS JOIN doc_quality q
CROSS JOIN r1926 x;


-- ============================================================
-- DOCUMENT MANIFEST
-- ============================================================

SELECT
    e.document_id,
    d.jurisdiction,
    d.document_type,
    d.identifier,
    d.celex,
    d.boe_id,
    d.publication_date,
    d.effective_date,
    d.consolidated_date,
    d.status,
    e.corpus_role,
    d.local_file,
    d.source_hash

FROM phase1_expected_documents e

LEFT JOIN source.documents d
  USING (document_id)

ORDER BY e.document_id;


-- ============================================================
-- RELATIONSHIP MANIFEST
-- ============================================================

SELECT
    relationship_id,
    source_document_id,
    target_document_id,
    relationship_type,
    description

FROM source.relationships

WHERE relationship_id IN (
    SELECT relationship_id
    FROM phase1_expected_relationships
)

ORDER BY relationship_id;
