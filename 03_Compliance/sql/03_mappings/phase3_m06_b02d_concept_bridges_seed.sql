-- FINAL SEED — NOT AUTHORIZED FOR EXECUTION
SELECT CASE WHEN (SELECT count(*) FROM mapping.phase3_concept_mappings WHERE mapping_id LIKE 'M06-B02-MAP-A05-%')=0
 THEN 'PREFLIGHT_OK' ELSE error('ABORT_CONFLICT: B02 concept bridges exist; compare complete rows before execution') END;
INSERT INTO mapping.phase3_concept_mappings(concept_id,mapping_id,relation_note)
VALUES
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-4-SN-A','C01 partial technical relation: RTTI 670/2022 RRP 4-SN-A road closures.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-4-SN-B','C01 partial technical relation: RTTI 670/2022 RRP 4-SN-B lane closures.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-4-SN-C','C01 partial technical relation: RTTI 670/2022 RRP 4-SN-C roadworks.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-4-SN-D','C01 partial technical relation: RTTI 670/2022 RRP 4-SN-D temporary traffic management.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-5-SN-A','C01 partial technical relation: RTTI 670/2022 RRP 5-SN-A bridge closures.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-5-SN-B','C01 partial technical relation: RTTI 670/2022 RRP 5-SN-B accidents and incidents.'),
('M06-B02-CPT-A05-P01-002-ROAD-STATUS-DISRUPTION','M06-B02-MAP-A05-P01-002-DATEX-5-SN-C','C01 partial technical relation: RTTI 670/2022 RRP 5-SN-C poor road conditions.'),
('M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','M06-B02-MAP-A05-P02-001-SIRI-ET','C07 partial technical relation: EPIP-RT ET journey delay/cancellation.'),
('M06-B02-CPT-A05-P02-001-PASSENGER-RT-STATUS-DISRUPTION','M06-B02-MAP-A05-P02-001-SIRI-SX','C07 partial technical relation: EPIP-RT SX passenger disruption notice.');
