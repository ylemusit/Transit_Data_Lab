-- Read-only checks for the authorized Article 9(3) source fact.
-- Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
WITH target AS (
    SELECT * FROM compliance.source_facts
    WHERE source_fact_id = 'EU-2017-1926-SF-A09-P03'
), checks AS (
    SELECT 'TARGET_ID_UNIQUE' test, (SELECT count(*)=1 FROM target) ok
    UNION ALL SELECT 'TARGET_PROVISION_VALID',
        (SELECT count(*)=1 FROM target f JOIN source.provisions p
         ON p.provision_id=f.source_provision_id AND p.document_id=f.source_document_id
         WHERE p.provision_id='EU-2017-1926-ART09' AND p.article='9')
    UNION ALL SELECT 'TARGET_DOCUMENT_VALID',
        (SELECT count(*)=1 FROM target f JOIN source.documents d ON d.document_id=f.source_document_id
         WHERE d.document_id='EU-REG-2017-1926')
    UNION ALL SELECT 'TARGET_TEXT_NONEMPTY',
        (SELECT count(*)=1 FROM target WHERE trim(source_fact_text)<>'')
    UNION ALL SELECT 'TARGET_LEGAL_REFERENCE',
        (SELECT count(*)=1 FROM target WHERE legal_reference='Artículo 9, apartado 3')
    UNION ALL SELECT 'TARGET_SOURCE_URI_PRESENT',
        (SELECT count(*)=1 FROM target WHERE trim(source_uri)<>'' AND source_uri LIKE '%02017R1926-20240304%')
    UNION ALL SELECT 'TARGET_VERSION_DATE_PRESENT',
        (SELECT count(*)=1 FROM target WHERE source_version_date=DATE '2024-03-04')
    UNION ALL SELECT 'ALL_EIGHT_VALUES_MATCH_APPROVED_PROPOSAL',
        (SELECT count(*)=1 FROM target f JOIN read_csv(
            '03_Compliance/reports/phase_2/review/gate_2/resolution/ARTICLE_9_3_SOURCE_FACT_PROPOSAL.csv',
            header=true, all_varchar=true) p
         ON f.source_fact_id=p.proposed_source_fact_id
         AND f.source_document_id=p.source_document_id
         AND f.source_provision_id=p.source_provision_id
         AND f.legal_reference=p.legal_reference
         AND f.source_fact_text=p.source_fact_text
         AND f.source_version_date=CAST(p.source_version_date AS DATE)
         AND f.source_uri=p.source_uri
         AND f.notes IS NOT DISTINCT FROM p.notes)
)
SELECT test, CASE WHEN ok THEN 'PASS' ELSE 'FAIL' END status FROM checks ORDER BY test;
