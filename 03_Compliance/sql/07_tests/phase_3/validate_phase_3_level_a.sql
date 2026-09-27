WITH checks AS (
    SELECT 'REQUIREMENT_REFERENCE' AS check_name, count(*)::BIGINT AS invalid_count
    FROM mapping.phase3_requirement_capabilities m LEFT JOIN compliance.requirements r USING (requirement_id)
    WHERE r.requirement_id IS NULL AND m.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
    UNION ALL SELECT 'CAPABILITY_REFERENCE', count(*) FROM mapping.phase3_requirement_capabilities m LEFT JOIN mapping.phase3_capabilities c USING (capability_id) WHERE c.capability_id IS NULL
    UNION ALL SELECT 'STANDARD_REFERENCE', count(*) FROM mapping.phase3_capabilities c LEFT JOIN mapping.phase3_standards s USING (standard_id) WHERE s.standard_id IS NULL
    UNION ALL SELECT 'DUPLICATE_MAPPING', count(*) FROM (SELECT requirement_id, capability_id FROM mapping.phase3_requirement_capabilities GROUP BY 1,2 HAVING count(*) > 1)
    UNION ALL SELECT 'REPRESENTABILITY_REASON', count(*) FROM mapping.phase3_representability WHERE representability_state IN ('PARTIAL','MISSING','UNKNOWN','NOT_APPLICABLE') AND length(trim(coalesce(explanation,'')))=0
    UNION ALL SELECT 'EXCEPTION_JUSTIFICATION', count(*) FROM mapping.phase3_exceptions WHERE length(trim(reason))=0 OR length(trim(justification))=0 OR length(trim(evidence_expectations))=0
    UNION ALL SELECT 'SOURCE_REFERENCE_SHAPE', count(*) FROM mapping.phase3_source_references WHERE length(trim(url_or_document_id))=0 OR capability_id NOT IN (SELECT capability_id FROM mapping.phase3_capabilities)
    UNION ALL SELECT 'CAPABILITY_CONTEXT', count(*) FROM mapping.phase3_capabilities c JOIN mapping.phase3_standards s USING (standard_id) WHERE length(trim(c.semantic_meaning))=0 OR length(trim(s.standard_kind))=0
), totals AS (
    SELECT (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS mappings,
           (SELECT count(*) FROM mapping.phase3_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS capabilities,
           (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS exceptions
)
SELECT CASE WHEN (SELECT coalesce(sum(invalid_count),0) FROM checks)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       mappings, capabilities, exceptions,
       coalesce((SELECT sum(invalid_count) FROM checks WHERE check_name IN ('REQUIREMENT_REFERENCE','CAPABILITY_REFERENCE','STANDARD_REFERENCE')),0) AS invalid_references,
       coalesce((SELECT sum(invalid_count) FROM checks WHERE check_name IN ('DUPLICATE_MAPPING','CAPABILITY_CONTEXT')),0) AS invalid_states,
       coalesce((SELECT sum(invalid_count) FROM checks WHERE check_name IN ('REPRESENTABILITY_REASON','EXCEPTION_JUSTIFICATION','SOURCE_REFERENCE_SHAPE')),0) AS missing_required_reasons
FROM totals;
