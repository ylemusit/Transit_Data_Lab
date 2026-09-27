-- Read-only cumulative-database regression. Run from repository root.
-- Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
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

    UNION ALL SELECT '29_SOURCE_FACTS_CURRENT', 36, (SELECT count(*) FROM compliance.source_facts)
    UNION ALL SELECT '30_ARTICLE_9_3_EXACTLY_ONCE', 1, (SELECT count(*) FROM compliance.source_facts WHERE source_fact_id='EU-2017-1926-SF-A09-P03')
    UNION ALL SELECT '31_REQUIREMENTS_CURRENT', 3, (SELECT count(*) FROM compliance.requirements)
    UNION ALL SELECT '32_DEADLINES_CURRENT', 1, (SELECT count(*) FROM compliance.deadlines)
    UNION ALL SELECT '33_FINAL_ATOMIC_UNIVERSE', 48, (SELECT count(DISTINCT final_review_id) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true))
    UNION ALL SELECT '34_EXCEPTION_QUEUE', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_EXCEPTION_QUEUE.csv',header=true,all_varchar=true))
    UNION ALL SELECT '35_MECHANICAL_BLOCKERS', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE materialization_eligible IS DISTINCT FROM 'TRUE' OR coalesce(materialization_blocker,'')<>'')
    UNION ALL SELECT '36_UNRESOLVED_HUMAN_DECISIONS', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE human_status IS NULL OR human_status IN ('HOLD','REJECT'))
    UNION ALL SELECT '37_EXTERNAL_DEPENDENCIES', 7, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/GATE_2_EXTERNAL_DEPENDENCIES.csv',header=true,all_varchar=true) WHERE external_dependency='TRUE' AND dependency_blocking_level='PARTIAL')
    UNION ALL SELECT '38_UNIVERSE_EXTERNAL_DEPENDENCIES', 7, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE external_dependency='TRUE' AND dependency_blocking_level='PARTIAL')
    UNION ALL SELECT '39_SOURCE_ANOMALY_DEPENDENCIES', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE source_anomaly_dependency IS DISTINCT FROM 'FALSE')
    UNION ALL SELECT '40_UNIVERSE_FACT_TRACEABILITY', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) u LEFT JOIN compliance.source_facts f ON u.source_fact_id=f.source_fact_id WHERE f.source_fact_id IS NULL OR u.source_document_id IS DISTINCT FROM f.source_document_id OR u.source_provision_id IS DISTINCT FROM f.source_provision_id OR u.source_fact_text IS DISTINCT FROM f.source_fact_text)
    UNION ALL SELECT '41_ANNEX_ANOMALY_RECORDS_RETAINED', 2, (SELECT count(*) FROM source.provisions WHERE provision_id IN ('EU-2017-1926-ANNEX-1.3-B-I','EU-2017-1926-ANNEX-1.3-D-I'))
    UNION ALL SELECT 'LEGAL_HASH_EU-DIR-2010-40', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Directive_2010_40_EU/Directive_2010_40_EU_CONSOLIDATED_2023-12-20_ES.pdf') WHERE sha256(content)='832deb51ce828b65c6e1b951bdae57194769838d47a0cd3013cc28f1bd420e58')
    UNION ALL SELECT 'LEGAL_HASH_EU-DIR-2023-2661', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Directive_2023_2661/Directive_EU_2023_2661_ES.pdf') WHERE sha256(content)='d9a1a3fb35ae1db13861f8f9c32085bd2f9375d55eb74f979f0c912f86e133ab')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-2017-1926', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Regulation_2017_1926/Regulation_2017_1926_CONSOLIDATED_2024-03-04_ES.pdf') WHERE sha256(content)='0a91ab5ffcf0466d588da8a8db7f7e7ed6d97b4d64576c31e083610fcd5b08d5')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-2024-490', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Regulation_2024_490/Regulation_2024_490_ES.pdf') WHERE sha256(content)='853f3cacdb5c5d4751c36b3938cdd20929a33c83cfe195679c3309fdbbd31eaf')
    UNION ALL SELECT 'LEGAL_HASH_ES-LAW-9-2025', 1, (SELECT count(*) FROM read_blob('03_Compliance/Spain/01_Primary_Law/Ley_9_2025/Ley_9_2025_CONSOLIDATED_2026-03-21.pdf') WHERE sha256(content)='ba40df196ab7bf2ad74b840784b268cd8e75d213533d6aafdcd8c72c0386048c')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-2024-1679', 1, (SELECT count(*) FROM read_blob('C:/Users/yeiso/Desktop/Folder/VSCode/Proyectos/Transit Data Lab/03_Compliance/EU/01_Primary_Law/Regulation_2024_1679/Regulation_EU_2024_1679_ES.pdf') WHERE sha256(content)='73b34f389d4493b62f553d28c740ee499b8feb1d7534dd1356efd9502d669c15')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-IMPL-2026-1554', 1, (SELECT count(*) FROM read_blob('C:/Users/yeiso/Desktop/Folder/VSCode/Proyectos/Transit Data Lab/03_Compliance/EU/01_Primary_Law/Regulation_2026_1554/Implementing_Regulation_EU_2026_1554_ES.pdf') WHERE sha256(content)='873bd419ebc3769f1d93e466767e971fd25c40caff2c768f98093654f70334e0')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-IMPL-2026-253', 1, (SELECT count(*) FROM read_blob('C:/Users/yeiso/Desktop/Folder/VSCode/Proyectos/Transit Data Lab/03_Compliance/EU/01_Primary_Law/Regulation_2026_253/Implementing_Regulation_EU_2026_253_ES.pdf') WHERE sha256(content)='eb6bfd69199d226758f6940896e0dd5c68ca15b1bf1f18f069827fa1d73de42f')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-2011-454', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Historical/Regulation_454_2011/Regulation_454_2011_CONSOLIDATED_2019-06-16_ES.pdf') WHERE sha256(content)='8daa0f6f9aa6adc52f3b335d551ee2bf5d3c4572b51a9eb69bbad245f8847f14')
    UNION ALL SELECT 'LEGAL_HASH_EU-REG-2014-1305', 1, (SELECT count(*) FROM read_blob('03_Compliance/EU/01_Primary_Law/Historical/Regulation_1305_2014/Regulation_1305_2014_CONSOLIDATED_2021-04-18_ES.pdf') WHERE sha256(content)='0ab0d946f518cc486a3dc2740865eedd5e616048f5ca674fe1b5de18f6137264')
    UNION ALL SELECT '42_INTERPRETIVE_ISSUES', 0, (SELECT CASE WHEN contains(content, 'cuestiones interpretativas pendientes: 0') THEN 0 ELSE 1 END FROM read_text('03_Compliance/reports/phase_2/review/gate_2/resolution/GATE_2_EXCEPTION_RESOLUTION.md'))
    UNION ALL SELECT '43_NO_GTFS_OBLIGATION_INFERENCE', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE contains(upper(normalized_description),'GTFS'))
    UNION ALL SELECT '44_NO_UNIVERSAL_NETEX', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE contains(upper(normalized_description),'NETEX') AND (is_conditional IS DISTINCT FROM 'TRUE' OR coalesce(condition_text,'')='' OR NOT (contains(lower(normalized_description),' o ') OR contains(lower(normalized_description),'compatible'))))
    UNION ALL SELECT '44_NO_UNIVERSAL_SIRI', 0, (SELECT count(*) FROM read_csv('03_Compliance/reports/phase_2/review/gate_2/materialization/GATE_2_POST_SOURCE_FACT_ATOMIC_UNIVERSE.csv',header=true,all_varchar=true) WHERE contains(upper(normalized_description),'SIRI') AND (is_conditional IS DISTINCT FROM 'TRUE' OR coalesce(condition_text,'')='' OR NOT (contains(lower(normalized_description),' o ') OR contains(lower(normalized_description),'compatible'))))
), evaluated AS (
    SELECT test, CASE WHEN expected=actual THEN 'PASS' ELSE 'FAIL' END status, expected, actual FROM checks
)
SELECT * FROM evaluated ORDER BY test;
