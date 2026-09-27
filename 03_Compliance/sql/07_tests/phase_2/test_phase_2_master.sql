WITH checks AS (
    SELECT '01_CANDIDATE_ID_UNIQUE' test, 0 expected,
        (SELECT count(*) FROM (SELECT candidate_id FROM compliance.requirement_candidates GROUP BY candidate_id HAVING count(*) > 1)) actual
    UNION ALL SELECT '02_REQUIREMENT_ID_UNIQUE',0,
        (SELECT count(*) FROM (SELECT requirement_id FROM compliance.requirements GROUP BY requirement_id HAVING count(*) > 1))
    UNION ALL SELECT '03_CANDIDATE_DOCUMENT_EXISTS',0,
        (SELECT count(*) FROM compliance.requirement_candidates c LEFT JOIN source.documents d ON c.source_document_id=d.document_id WHERE d.document_id IS NULL)
    UNION ALL SELECT '04_CANDIDATE_PROVISION_EXISTS',0,
        (SELECT count(*) FROM compliance.requirement_candidates c LEFT JOIN source.provisions p ON c.source_provision_id=p.provision_id WHERE p.provision_id IS NULL)
    UNION ALL SELECT '05_REQUIREMENT_DOCUMENT_EXISTS',0,
        (SELECT count(*) FROM compliance.requirements r LEFT JOIN source.documents d ON r.source_document_id=d.document_id WHERE d.document_id IS NULL)
    UNION ALL SELECT '06_REQUIREMENT_PROVISION_EXISTS',0,
        (SELECT count(*) FROM compliance.requirements r LEFT JOIN source.provisions p ON r.source_provision_id=p.provision_id WHERE r.source_provision_id IS NULL OR p.provision_id IS NULL)
    UNION ALL SELECT '07_CANDIDATE_DESCRIPTION_NOT_NULL',0,
        (SELECT count(*) FROM compliance.requirement_candidates WHERE description IS NULL OR trim(description)='') +
        (SELECT count(*) FROM compliance.requirements WHERE description IS NULL OR trim(description)='')
    UNION ALL SELECT '08_CANDIDATE_SOURCE_FACT_NOT_NULL',0,
        (SELECT count(*) FROM compliance.requirement_candidates c LEFT JOIN compliance.source_facts f USING(source_fact_id) WHERE f.source_fact_id IS NULL OR f.source_fact_text IS NULL OR trim(f.source_fact_text)='' OR f.source_document_id<>c.source_document_id OR f.source_provision_id<>c.source_provision_id)
    UNION ALL SELECT '09_VALID_LEGAL_CLASSIFICATION',0,
        (SELECT count(*) FROM compliance.requirement_candidates WHERE legal_classification NOT IN ('DEFINITION','SCOPE','OBLIGATION','CONDITION','PERMISSION','EXCEPTION','DEADLINE','PROCEDURAL','REFERENCE','OTHER'))
    UNION ALL SELECT '10_VALID_REQUIREMENT_CLASS',0,
        (SELECT count(*) FROM compliance.requirement_candidates WHERE requirement_class NOT IN ('DATA_AVAILABILITY','ACCESS','FORMAT','INTEROPERABILITY','METADATA','UPDATE','QUALITY','DISCOVERY','REUSE','ROUTING','ASSESSMENT','REPORTING','DEADLINE','OTHER'))
    UNION ALL SELECT '11_VALID_REVIEW_STATUS',0,
        (SELECT count(*) FROM compliance.requirement_candidates WHERE review_status NOT IN ('PENDING','APPROVED','REJECTED','NEEDS_REVIEW'))
    UNION ALL SELECT '12_DEADLINE_REQUIREMENT_EXISTS',0,
        (SELECT count(*) FROM compliance.deadlines d LEFT JOIN compliance.requirements r USING(requirement_id) WHERE d.requirement_id IS NULL OR r.requirement_id IS NULL)
    UNION ALL SELECT '13_DEADLINE_SOURCE_EXISTS',0,
        (SELECT count(*) FROM compliance.deadlines d LEFT JOIN source.documents s ON d.source_document_id=s.document_id LEFT JOIN source.provisions p ON d.source_provision_id=p.provision_id WHERE d.source_document_id IS NULL OR d.source_provision_id IS NULL OR s.document_id IS NULL OR p.provision_id IS NULL)
    UNION ALL SELECT '14_ONLY_2017_1926_PROCESSED',0,
        (SELECT count(*) FROM (SELECT source_document_id FROM compliance.provision_classifications UNION SELECT source_document_id FROM compliance.source_facts UNION SELECT source_document_id FROM compliance.requirement_candidates UNION SELECT source_document_id FROM compliance.requirements WHERE source_document_id IN (SELECT document_id FROM source.documents) UNION SELECT source_document_id FROM compliance.deadlines UNION SELECT source_document_id FROM compliance.requirement_candidate_sources) WHERE source_document_id <> 'EU-REG-2017-1926')
    UNION ALL SELECT '15_FORMAT_COVERAGE_EMPTY',0,(SELECT count(*) FROM mapping.format_coverage)
    UNION ALL SELECT '16_AUDIT_RULES_EMPTY',0,(SELECT count(*) FROM audit.rules)
    UNION ALL SELECT '17_PHASE1_DOCUMENTS_UNCHANGED',0,
        (SELECT count(*) FROM ((SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_DOCUMENTS.csv')) EXCEPT ALL (SELECT * FROM source.documents))) +
        (SELECT count(*) FROM ((SELECT * FROM source.documents) EXCEPT ALL (SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_DOCUMENTS.csv'))))
    UNION ALL SELECT '18_PHASE1_PROVISIONS_UNCHANGED',0,
        (SELECT count(*) FROM ((SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_PROVISIONS.csv')) EXCEPT ALL (SELECT * FROM source.provisions))) +
        (SELECT count(*) FROM ((SELECT * FROM source.provisions) EXCEPT ALL (SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_PROVISIONS.csv'))))
    UNION ALL SELECT '19_PHASE1_RELATIONSHIPS_UNCHANGED',0,
        (SELECT count(*) FROM ((SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_RELATIONSHIPS.csv')) EXCEPT ALL (SELECT * FROM source.relationships))) +
        (SELECT count(*) FROM ((SELECT * FROM source.relationships) EXCEPT ALL (SELECT * FROM read_csv_auto('03_Compliance/reports/phase_2/baseline/PHASE_1_SOURCE_RELATIONSHIPS.csv'))))
    UNION ALL SELECT '20_2017_1926_PROVISIONS_REMAIN_92',92,
        (SELECT count(*) FROM source.provisions WHERE document_id='EU-REG-2017-1926')
    UNION ALL SELECT '21_ALL_2017_1926_PROVISIONS_CLASSIFIED',92,
        (SELECT count(*) FROM compliance.provision_classifications WHERE source_document_id='EU-REG-2017-1926')
    UNION ALL SELECT '22_APPROVED_CANDIDATES_MATERIALIZED',0,
        (SELECT count(*) FROM compliance.requirement_candidates c LEFT JOIN compliance.requirements r USING(requirement_id) WHERE c.review_status='APPROVED' AND r.requirement_id IS NULL)
    UNION ALL SELECT '23_REQUIREMENTS_FROM_APPROVED_CANDIDATES_ONLY',0,
        (SELECT count(*) FROM compliance.requirements r LEFT JOIN compliance.requirement_candidates c USING(requirement_id) WHERE c.candidate_id IS NULL OR c.review_status <> 'APPROVED')
    UNION ALL SELECT '24_CANDIDATES_HAVE_EXACTLY_ONE_SOURCE_DOCUMENT',0,
        (SELECT count(*) FROM compliance.requirement_candidates WHERE source_document_id <> 'EU-REG-2017-1926')
    UNION ALL SELECT '25_DEADLINE_HAS_REQUIREMENT_AND_SOURCE',0,
        (SELECT count(*) FROM compliance.deadlines WHERE deadline_date IS NOT NULL AND (requirement_id IS NULL OR source_document_id IS NULL OR source_provision_id IS NULL OR description IS NULL OR trim(description)=''))
    UNION ALL SELECT '26_CLASSIFICATION_COVERS_ONLY_TARGET_DOCUMENT',0,
        (SELECT count(*) FROM compliance.provision_classifications WHERE source_document_id <> 'EU-REG-2017-1926')
    UNION ALL SELECT '27_SOURCE_FACT_VERSION_IS_CONSOLIDATED_2024_03_04',0,
        (SELECT count(*) FROM compliance.source_facts WHERE source_document_id='EU-REG-2017-1926' AND source_version_date <> DATE '2024-03-04')
    UNION ALL SELECT '28_ANNEX_SUPPORT_SOURCE_EXISTS',0,
        (SELECT count(*) FROM compliance.requirement_candidate_sources s LEFT JOIN compliance.requirement_candidates c USING(candidate_id) LEFT JOIN source.provisions p ON s.source_provision_id=p.provision_id WHERE c.candidate_id IS NULL OR p.provision_id IS NULL OR s.source_document_id <> c.source_document_id OR p.document_id <> c.source_document_id)
), evaluated AS (
    SELECT test, CASE WHEN expected=actual THEN 'PASS' ELSE 'FAIL' END status, expected, actual FROM checks
)
SELECT * FROM evaluated ORDER BY test;
