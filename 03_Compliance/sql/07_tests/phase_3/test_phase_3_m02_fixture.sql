BEGIN TRANSACTION;
INSERT INTO mapping.phase3_standards VALUES ('M02-FIXTURE-STANDARD','Synthetic framework fixture','GTFS_SCHEDULE',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'IDENTITY_ONLY');
INSERT INTO mapping.phase3_capabilities (capability_id,standard_id,semantic_meaning,review_status,fixture_kind)
VALUES ('M02-FIXTURE-CAPABILITY','M02-FIXTURE-STANDARD','Synthetic capability for schema exercise','UNREVIEWED','SYNTHETIC_TEST');
INSERT INTO mapping.phase3_requirement_capabilities (mapping_id,requirement_id,capability_id,mapping_type,review_status,fixture_kind)
SELECT 'M02-FIXTURE-MAPPING',requirement_id,'M02-FIXTURE-CAPABILITY','DIRECT','UNREVIEWED','SYNTHETIC_TEST'
FROM compliance.requirements ORDER BY requirement_id LIMIT 1;
INSERT INTO mapping.phase3_representability VALUES ('M02-FIXTURE-REPRESENTABILITY','M02-FIXTURE-CAPABILITY','UNKNOWN','Synthetic fixture only',NULL,NULL,'UNREVIEWED','SYNTHETIC_TEST');
INSERT INTO mapping.phase3_exceptions VALUES ('M02-FIXTURE-EXCEPTION',(SELECT requirement_id FROM compliance.requirements ORDER BY requirement_id LIMIT 1),'LEGAL_PROCESS','Synthetic test path','Synthetic fixture only','Synthetic test evidence','UNREVIEWED','SYNTHETIC_TEST');
SELECT CASE WHEN
 (SELECT count(*) FROM mapping.phase3_requirement_capabilities WHERE mapping_id='M02-FIXTURE-MAPPING')=1
 AND (SELECT count(*) FROM mapping.phase3_exceptions WHERE exception_id='M02-FIXTURE-EXCEPTION')=1
 AND (SELECT count(*) FROM mapping.phase3_representability WHERE representability_id='M02-FIXTURE-REPRESENTABILITY')=1
 THEN 'PASS' ELSE error('M02 synthetic fixture failed') END AS fixture_status;
ROLLBACK;
