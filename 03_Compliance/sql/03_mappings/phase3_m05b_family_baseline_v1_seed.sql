-- M05B-C: reviewed planning/navigation baseline for the frozen 48 requirements.
-- Classification is independent of legal conclusions, technical mappings,
-- representability, requirement coverage, and audit outcomes.
BEGIN TRANSACTION;

CREATE TEMP TABLE m05b_expected_families AS SELECT * FROM (VALUES
 ('F01','NAP access and discovery','Planning work to establish, expose, and locate the national access point and its data. FALSE: this is the reviewed current planning taxonomy, not an unreviewed proposal.','HIGH'),
 ('F02','Availability and format representation','Planning work to make data available in the required exchange formats, standards, or profiles; this does not assert representability. FALSE: this is the reviewed current planning taxonomy, not an unreviewed proposal.','HIGH'),
 ('F03','Temporal coverage and deadlines','Planning work concerning staged availability, geographic rollout, temporal coverage, and explicit dates.','HIGH'),
 ('F04','Metadata and provenance','Planning work concerning metadata requirements, source attribution, and update-interval metadata.','HIGH'),
 ('F05','Update and correction','Planning work to propagate changes, provide advance updates, and correct inaccuracies.','HIGH'),
 ('F06','Quality and notification','Planning work concerning accuracy, freshness, minimum quality requirements, and reporting defects.','HIGH'),
 ('F07','Reuse and journey presentation','Planning work concerning neutral reuse, ranking criteria, and the way journey options are presented.','HIGH'),
 ('F08','Routing-result exchange','Planning work concerning provider-to-provider communication of routing results.','HIGH'),
 ('F09','Governance, evaluation, and process duties','Planning work concerning privacy constraints, institutional evaluation and verification, procedural powers, and reports.','HIGH')
) AS t(family_id,family_name,description,confidence);

CREATE TEMP TABLE m05b_expected_primary AS
SELECT requirement_id,
 CASE
  WHEN requirement_class IN ('ACCESS','DISCOVERY','DATA_AVAILABILITY') THEN 'F01'
  WHEN requirement_class IN ('FORMAT','INTEROPERABILITY') THEN 'F02'
  WHEN requirement_class='DEADLINE' THEN 'F03'
  WHEN requirement_class='METADATA' THEN 'F04'
  WHEN requirement_class='UPDATE' THEN 'F05'
  WHEN requirement_class='QUALITY' THEN 'F06'
  WHEN requirement_class='REUSE' THEN 'F07'
  WHEN requirement_class='ROUTING' THEN 'F08'
  ELSE 'F09'
 END AS family_id,
 CASE
  WHEN requirement_class IN ('ACCESS','DISCOVERY','DATA_AVAILABILITY') THEN 'The principal work is establishing, exposing, or locating the national access point and its data.'
  WHEN requirement_class IN ('FORMAT','INTEROPERABILITY') THEN 'The principal work is reviewing the required exchange format, standard, interoperability, or profile boundary; no representability conclusion is made.'
  WHEN requirement_class='DEADLINE' THEN 'The principal work is sequencing a dated availability obligation across its stated geography and data scope.'
  WHEN requirement_class='METADATA' THEN 'The principal work is agreeing, supplying, or disclosing metadata and provenance information.'
  WHEN requirement_class='UPDATE' THEN 'The principal work is updating or correcting data when changes or inaccuracies arise.'
  WHEN requirement_class='QUALITY' THEN 'The principal work is defining, maintaining, or communicating data quality.'
  WHEN requirement_class='REUSE' THEN 'The principal work is governing neutral reuse or presenting ranked journey options.'
  WHEN requirement_class='ROUTING' THEN 'The principal work is exchanging a routing result between service providers.'
  ELSE 'The principal work is an institutional, procedural, reporting, privacy, evaluation, or verification duty rather than a transport-format capability.'
 END AS classification_reason,
 CASE WHEN requirement_class IN ('ACCESS','DATA_AVAILABILITY','FORMAT','INTEROPERABILITY','DEADLINE','METADATA','UPDATE','QUALITY','REUSE','ROUTING') THEN 'HIGH' ELSE 'MEDIUM' END AS confidence
FROM compliance.requirements;

SELECT CASE WHEN (SELECT count(*) FROM compliance.requirements)=48
 AND (SELECT count(*) FROM m05b_expected_primary)=48
 AND (SELECT count(DISTINCT requirement_id) FROM m05b_expected_primary)=48
 AND (SELECT count(*) FROM m05b_expected_families)=9
THEN 'M05B_CLASSIFICATION_PREWRITE_PASS'
ELSE error('M05B pre-write classification gate failed') END;

-- Existing data is accepted only when it is already the exact same baseline.
SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_families)=0 OR (
 (SELECT count(*) FROM mapping.phase3_families)=9 AND
 NOT EXISTS (SELECT 1 FROM m05b_expected_families e LEFT JOIN mapping.phase3_families f USING(family_id)
  WHERE f.family_id IS NULL OR f.family_name<>e.family_name OR f.description<>e.description OR f.provisional<>FALSE)
) THEN 'M05B_FAMILY_STATE_COMPATIBLE'
ELSE error('Incompatible substantive family state; refusing overwrite') END;
SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_requirement_families)=0 OR (
 (SELECT count(*) FROM mapping.phase3_requirement_families)=48 AND
 NOT EXISTS (SELECT 1 FROM m05b_expected_primary e LEFT JOIN mapping.phase3_requirement_families m
  ON m.requirement_id=e.requirement_id AND m.family_id=e.family_id AND m.relation_type='PRIMARY_FAMILY'
  WHERE m.requirement_id IS NULL OR m.review_status<>'REVIEWED' OR m.classification_reason<>e.classification_reason OR m.classification_confidence<>e.confidence) AND
 NOT EXISTS (SELECT 1 FROM mapping.phase3_requirement_families m LEFT JOIN m05b_expected_primary e
  ON e.requirement_id=m.requirement_id AND e.family_id=m.family_id
  WHERE e.requirement_id IS NULL OR m.relation_type<>'PRIMARY_FAMILY')
) THEN 'M05B_MEMBERSHIP_STATE_COMPATIBLE'
ELSE error('Incompatible substantive membership state; refusing overwrite') END;

INSERT INTO mapping.phase3_families(family_id,family_name,description,provisional)
SELECT family_id,family_name,description,FALSE FROM m05b_expected_families
ON CONFLICT(family_id) DO NOTHING;
INSERT INTO mapping.phase3_requirement_families
 (requirement_id,family_id,relation_type,review_status,fixture_kind,classification_reason,classification_confidence)
SELECT requirement_id,family_id,'PRIMARY_FAMILY','REVIEWED',NULL,classification_reason,confidence
FROM m05b_expected_primary
ON CONFLICT(requirement_id,family_id,relation_type) DO NOTHING;

SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_families)=9
 AND (SELECT count(*) FROM mapping.phase3_requirement_families)=48
THEN 'M05B_FAMILY_BASELINE_SEEDED' ELSE error('M05B seed postcondition failed') END;
COMMIT;
