WITH cap_evidence AS (
    SELECT c.capability_id,
           c.review_status,
           length(trim(coalesce(c.limitations,''))) > 0 AS has_limitation,
           count(s.source_reference_id) AS source_count,
           count(s.source_reference_id) FILTER (WHERE s.source_kind IN ('OFFICIAL_SPECIFICATION','OFFICIAL_PROFILE')) AS authoritative_count,
           count(s.source_reference_id) FILTER (WHERE length(trim(coalesce(s.section,''))) > 0 AND length(trim(s.url_or_document_id)) > 0) AS locator_count
    FROM mapping.phase3_capabilities c
    LEFT JOIN mapping.phase3_source_references s USING (capability_id)
    WHERE c.fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST'
    GROUP BY c.capability_id,c.review_status,c.limitations
), totals AS (
    SELECT count(*) AS capabilities,
           count(*) FILTER (WHERE source_count > 0 AND authoritative_count > 0) AS with_authoritative_source,
           count(*) FILTER (WHERE locator_count > 0) AS with_locator,
           count(*) FILTER (WHERE has_limitation) AS with_limitation,
           count(*) FILTER (WHERE review_status IN ('NEEDS_REVIEW','UNREVIEWED')) AS needs_human_review,
           (SELECT count(*) FROM mapping.phase3_source_references WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS source_references,
           (SELECT count(*) FROM mapping.phase3_representability WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS representability_assertions,
           (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS mappings,
           (SELECT count(*) FROM mapping.phase3_exceptions WHERE fixture_kind IS DISTINCT FROM 'SYNTHETIC_TEST') AS exceptions
    FROM cap_evidence
)
SELECT CASE
         WHEN capabilities=0 OR with_authoritative_source<>capabilities OR with_locator<>capabilities OR with_limitation<>capabilities THEN 'FAIL'
         WHEN needs_human_review>0 THEN 'PARTIAL'
         ELSE 'PASS'
       END AS status,
       capabilities,source_references,with_authoritative_source,with_locator,with_limitation,
       needs_human_review,representability_assertions,mappings,exceptions
FROM totals;
