BEGIN TRANSACTION;

-- ============================================================
-- SOURCE RELATIONSHIPS
-- ============================================================

CREATE TABLE IF NOT EXISTS source.relationships
(
    relationship_id VARCHAR PRIMARY KEY,

    source_document_id VARCHAR NOT NULL,
    source_provision_id VARCHAR,

    target_document_id VARCHAR NOT NULL,
    target_provision_id VARCHAR,

    relationship_type VARCHAR NOT NULL,

    description VARCHAR,
    notes VARCHAR,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- NEW CURRENT DOCUMENTS
-- ============================================================

INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-2024-1679',
    'EU',
    'European Parliament and Council',
    'REGULATION',
    'Regulation (EU) 2024/1679 on Union guidelines for the development of the trans-European transport network',
    '2024/1679',
    '32024R1679',
    DATE '2024-06-28',
    DATE '2024-07-18',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2024/1679/oj',
    'EU/01_Primary_Law/Regulation_2024_1679/Regulation_EU_2024_1679_ES.pdf',
    '73B34F389D4493B62F553D28C740EE499B8FEB1D7534DD1356EFD9502D669C15',
    'TEN-T framework. Relevant to urban nodes and urban mobility data.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2024-1679'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-IMPL-2026-1554',
    'EU',
    'European Commission',
    'IMPLEMENTING_REGULATION',
    'Commission Implementing Regulation (EU) 2026/1554 on collection and submission of urban mobility data per urban node',
    '2026/1554',
    '32026R1554',
    DATE '2026-07-10',
    DATE '2026-07-30',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg_impl/2026/1554/oj',
    'EU/01_Primary_Law/Regulation_2026_1554/Implementing_Regulation_EU_2026_1554_ES.pdf',
    '873BD419EBC3769F1D93E466767E971FD25C40CAFF2C768F98093654F70334E0',
    'Urban mobility data: sustainability, safety and accessibility. Implements Regulation (EU) 2024/1679.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-IMPL-2026-1554'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    publication_date,
    effective_date,
    consolidated_date,
    status,
    language,
    official_url,
    local_file,
    source_hash,
    notes
)
SELECT
    'EU-REG-IMPL-2026-253',
    'EU',
    'European Commission',
    'IMPLEMENTING_REGULATION',
    'Commission Implementing Regulation (EU) 2026/253 on interoperability of data sharing in rail transport (TEL TSI)',
    '2026/253',
    '32026R0253',
    DATE '2026-02-10',
    DATE '2026-03-01',
    NULL,
    'IN_FORCE',
    'ES',
    'https://eur-lex.europa.eu/eli/reg_impl/2026/253/oj',
    'EU/01_Primary_Law/Regulation_2026_253/Implementing_Regulation_EU_2026_253_ES.pdf',
    'EB6BFD69199D226758F6940896E0DD5C68CA15B1BF1F18F069827FA1D73DE42F',
    'TEL TSI. Rail telematics and interoperability of data sharing.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-IMPL-2026-253'
);


-- ============================================================
-- HISTORICAL / REPEALED DOCUMENT REFERENCES
-- Metadata only for now. No local PDF downloaded.
-- ============================================================

INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    status,
    language,
    official_url,
    notes
)
SELECT
    'EU-REG-2011-454',
    'EU',
    'European Commission',
    'REGULATION',
    'Commission Regulation (EU) No 454/2011 - TAP TSI',
    '454/2011',
    '32011R0454',
    'REPEALED',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2011/454/oj',
    'Historical reference. Repealed by Implementing Regulation (EU) 2026/253.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2011-454'
);


INSERT INTO source.documents
(
    document_id,
    jurisdiction,
    authority,
    document_type,
    title,
    identifier,
    celex,
    status,
    language,
    official_url,
    notes
)
SELECT
    'EU-REG-2014-1305',
    'EU',
    'European Commission',
    'REGULATION',
    'Commission Regulation (EU) No 1305/2014 - TAF TSI',
    '1305/2014',
    '32014R1305',
    'REPEALED',
    'ES',
    'https://eur-lex.europa.eu/eli/reg/2014/1305/oj',
    'Historical reference. Repealed by Implementing Regulation (EU) 2026/253.'
WHERE NOT EXISTS
(
    SELECT 1
    FROM source.documents
    WHERE document_id = 'EU-REG-2014-1305'
);


-- ============================================================
-- RELATIONSHIPS
-- ============================================================

INSERT INTO source.relationships
SELECT
    'REL-EU-2023-2661-AMENDS-2010-40',
    'EU-DIR-2023-2661',
    NULL,
    'EU-DIR-2010-40',
    NULL,
    'AMENDS',
    'Directive (EU) 2023/2661 amends Directive 2010/40/EU.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2023-2661-AMENDS-2010-40'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2024-490-AMENDS-2017-1926',
    'EU-REG-2024-490',
    NULL,
    'EU-REG-2017-1926',
    NULL,
    'AMENDS',
    'Delegated Regulation (EU) 2024/490 amends Delegated Regulation (EU) 2017/1926.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2024-490-AMENDS-2017-1926'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-1554-IMPLEMENTS-2024-1679',
    'EU-REG-IMPL-2026-1554',
    NULL,
    'EU-REG-2024-1679',
    NULL,
    'IMPLEMENTS',
    'Implementing Regulation (EU) 2026/1554 lays down rules for the application of Regulation (EU) 2024/1679 regarding urban mobility data.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-1554-IMPLEMENTS-2024-1679'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-1554-REFERENCES-2017-1926',
    'EU-REG-IMPL-2026-1554',
    NULL,
    'EU-REG-2017-1926',
    NULL,
    'REFERENCES',
    'Regulation (EU) 2026/1554 refers to data collection methods under Delegated Regulation (EU) 2017/1926 for relevant urban mobility indicators.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-1554-REFERENCES-2017-1926'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-253-REPEALS-2011-454',
    'EU-REG-IMPL-2026-253',
    NULL,
    'EU-REG-2011-454',
    NULL,
    'REPEALS',
    'Implementing Regulation (EU) 2026/253 repeals Regulation (EU) No 454/2011.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-253-REPEALS-2011-454'
);


INSERT INTO source.relationships
SELECT
    'REL-EU-2026-253-REPEALS-2014-1305',
    'EU-REG-IMPL-2026-253',
    NULL,
    'EU-REG-2014-1305',
    NULL,
    'REPEALS',
    'Implementing Regulation (EU) 2026/253 repeals Regulation (EU) No 1305/2014.',
    NULL,
    CURRENT_TIMESTAMP
WHERE NOT EXISTS
(
    SELECT 1 FROM source.relationships
    WHERE relationship_id = 'REL-EU-2026-253-REPEALS-2014-1305'
);


COMMIT;

