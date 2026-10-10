"""Guard against misleading precision, attribution and coverage claims."""
from copy import deepcopy
import unittest
from tools.audit_precision_v1 import classify, metrics, investigate
from tools.audit_battery_plan_v1 import validate


class PrecisionTests(unittest.TestCase):
    def test_abstention_never_becomes_true_negative(self):
        for state in ('SATISFIED','VIOLATED'):
            for status in ('NOT_EVALUABLE','INSPECTION_ERROR','NOT_APPLICABLE'):
                self.assertEqual('ABSTENTION',classify({'criterion_state':state},{'status':status}))

    def test_unrelated_family_failure_is_not_false_positive(self):
        self.assertEqual('CONFOUNDED_REVIEW',classify({'criterion_state':'SATISFIED'}, {'status':'FAIL_TECHNICAL','confounded':True}))

    def test_conditional_and_recommendation_are_not_binary(self):
        self.assertEqual('RECOMMENDATION_MATCH',classify({'criterion_state':'RECOMMENDATION_UNMET'},{'status':'PASS','recommendation_met':False}))
        self.assertEqual('UNSUPPORTED_DETERMINATION_REVIEW',classify({'criterion_state':'UNKNOWN'},{'status':'PASS'}))

    def test_denominators_include_undetected_abstentions(self):
        rows=[{'criterion_id':'R','classification':c,'expected':{'criterion_state':s}} for c,s in
              [('TP','VIOLATED'),('ABSTENTION','VIOLATED'),('TN','SATISFIED'),('CONFOUNDED_REVIEW','SATISFIED')]]
        m=metrics(rows)[0]
        self.assertEqual(4,m['scenarios']);self.assertEqual(2,m['binary_decisions'])
        self.assertEqual(0.5,m['violation_detection_yield']);self.assertEqual(1,m['violation_abstentions'])

    def test_missing_binary_denominator_is_unknown(self):
        m=metrics([{'criterion_id':'R','classification':'UNIMPLEMENTED','expected':{'criterion_state':'UNKNOWN'}}])[0]
        self.assertIsNone(m['false_negative_rate_decided']);self.assertIsNone(m['false_positive_rate_decided'])

    def test_cross_rule_detection_requires_matching_table_and_rule(self):
        case={'criterion_id':'GTFS-G06-STOP-SEQUENCE','variant':'negative'}
        obs={'status':'PASS'}
        finding={'rule_id':'GTFS-G04-PRIMARY-KEY-UNIQUENESS','source_file':'shapes.txt'}
        self.assertNotEqual('DETECTED_OTHER_RULE',investigate(case,obs,{'g04':{'findings':[finding]}})['category'])
        finding['source_file']='stop_times.txt'
        self.assertEqual('DETECTED_OTHER_RULE',investigate(case,obs,{'g04':{'findings':[finding]}})['category'])

    def test_profile_gap_cannot_be_suppressed(self):
        plan={'proposals':[{'proposal_id':'N','format':'NETEX','area':'PROFILE','blocking_reason':None,
              'fixtures':dict(positive='review',negative='review',boundary='unknown'),'implementation_status':'DESIGNED_NOT_IMPLEMENTED'}],
              'engine_modified':False,'holdout_accessed':False,'full_coverage_claim':False}
        with self.assertRaises(ValueError):validate(plan)
        plan['proposals'][0]['blocking_reason']='Missing text';validate(plan)

    def test_plan_cannot_claim_exhaustive_coverage(self):
        plan={'proposals':[],'engine_modified':False,'holdout_accessed':False,'full_coverage_claim':True}
        with self.assertRaises(ValueError):validate(plan)


if __name__=='__main__':unittest.main()
