"""Check external notice attribution and avoid unsafe agreement inference."""
import unittest
from tools.audit_external_review_v1 import focal_notices, review_row


class ExternalReviewTests(unittest.TestCase):
    def row(self):
        return {'case_id':'GTFS-REF-TRIP-ROUTE--negative','criterion_id':'GTFS-REF-TRIP-ROUTE','expected_state':'VIOLATED',
                'notices':[],'system_notices':[],'report_sha256':'a'*64,'report_path':'external/report.json'}

    def test_no_notice_never_infers_pass(self):
        result=review_row(self.row(),{'classification':'TP','observed':{'status':'FAIL_TECHNICAL'}})
        self.assertEqual('NO_FOCAL_NOTICE_NOT_PASS',result['external_review'])

    def test_foreign_key_must_match_field_and_table(self):
        row=self.row();sample={'childFilename':'trips.txt','childFieldName':'service_id'}
        row['notices']=[{'code':'foreign_key_violation','sampleNotices':[sample]}]
        self.assertEqual([],focal_notices(row))
        sample['childFieldName']='route_id';self.assertEqual(1,len(focal_notices(row)))

    def test_duplicate_notice_in_other_table_is_not_focal(self):
        row=self.row();row['criterion_id']='GTFS-G06-STOP-SEQUENCE'
        row['notices']=[{'code':'duplicate_key','sampleNotices':[{'filename':'stops.txt'}]}]
        self.assertEqual([],focal_notices(row))

    def test_external_internal_errors_are_retained(self):
        row=self.row();row['system_notices']=[{'code':'runtime_exception_in_validator_error'}]
        result=review_row(row,{'classification':'TP','observed':{'status':'FAIL_TECHNICAL'}})
        self.assertEqual(row['system_notices'],result['system_notices'])
        self.assertIn('exit 0',result['reason'])

    def test_provider_context_difference_not_false_negative(self):
        row=self.row();row['criterion_id']='GTFS-G06-FREQUENCY-OPERATIONS'
        result=review_row(row,{'classification':'TP','observed':{'status':'FAIL_TECHNICAL'}})
        self.assertEqual('CONTEXT_NOT_SHARED',result['external_review'])


if __name__=='__main__':unittest.main()
