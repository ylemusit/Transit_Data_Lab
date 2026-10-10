from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.audit_corpus_v1 import read,write
from tools.audit_lifecycle_demo_v1 import ref
from tools.audit_lifecycle_v1 import initialize,append,validate,key


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='tdl_lifecycle_');self.root=Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.enterContext(patch('tools.audit_lifecycle_v1.ALLOWED_ROOTS', (self.root,)))
        self.proof=self.root/'statement.txt';self.proof.write_text('SYNTHETIC UNIT TEST STATEMENT')
        self.before=self.snapshot('BEFORE','FAIL_TECHNICAL');self.model=initialize(ref(self.before));self.cid=next(iter(self.model['cases']))

    def snapshot(self,name,status,version='1.0.0',include=True):
        raw=self.root/(name+'-raw.json');write(raw,{'status':status})
        rule={'rule_id':'RULE','version':version,'status':status,'checked_rows':1}
        native_row={'case_id':'C','criterion_id':'RULE','format':'GTFS_SCHEDULE','fixture_sha256':'b'*64,
                    'observed':{'status':status,'raw_rule_result':rule},'raw_path':str(raw),'raw_sha256':ref(raw)['sha256']}
        native=self.root/(name+'-native.json');write(native,{'run_id':name,'rows':[native_row]})
        row={'format':'GTFS_SCHEDULE','logical_dataset_id':'SYNTH','criterion_id':'RULE','rule_version':version,
             'scope_id':'REVIEWED_FOCAL_SCOPE','source_case_id':'C','status':status,'coverage_complete':status in {'PASS','FAIL_TECHNICAL'},
             'fixture_sha256':'b'*64,'raw_evidence':ref(raw)}
        path=self.root/(name+'.json');write(path,{'contract':'TDL_REAUDIT_SNAPSHOT/1','execution_id':name,'execution_evidence':ref(native),'rows':[row] if include else []})
        return path

    def event(self,kind,**values):return {'type':kind,'actor':'unit test author','origin':'SYNTHETIC_SIMULATION',**values}

    def test_reported_corrected_does_not_resolve(self):
        m=append(self.model,self.event('PRODUCER_RESPONSE',case_id=self.cid,reported_state='REPORTED_CORRECTED',statement='reported only',evidence=ref(self.proof)))
        self.assertEqual('OPEN',m['cases'][self.cid]['technical_state']);self.assertEqual('REPORTED_CORRECTED',m['cases'][self.cid]['producer_status'])
        self.assertEqual([],self.model['events'])

    def test_same_execution_cannot_resolve(self):
        with self.assertRaises(ValueError):append(self.model,self.event('REAUDIT',evidence=ref(self.before)))

    def test_distinct_pass_with_proof_resolves(self):
        after=self.snapshot('AFTER','PASS');m=append(self.model,self.event('REAUDIT',evidence=ref(after)))
        self.assertEqual('RESOLVED',m['cases'][self.cid]['technical_state']);self.assertEqual('NOT_ACCEPTED',m['cases'][self.cid]['acceptance'])
        self.assertEqual('AFTER',m['cases'][self.cid]['resolution_evidence']['execution_id'])

    def test_absent_result_cannot_resolve(self):
        after=self.snapshot('AFTER','PASS',include=False);m=append(self.model,self.event('REAUDIT',evidence=ref(after)))
        self.assertEqual('NOT_EVALUATED',m['cases'][self.cid]['technical_state'])

    def test_unknown_and_changed_version_do_not_resolve(self):
        for status in ('NOT_EVALUABLE','NOT_APPLICABLE','INSPECTION_ERROR'):
            after=self.snapshot('AFTER-'+status,status);m=append(self.model,self.event('REAUDIT',evidence=ref(after)))
            self.assertEqual('NOT_EVALUATED',m['cases'][self.cid]['technical_state'])
        after=self.snapshot('VERSION-CHANGE','PASS','2.0.0');m=append(self.model,self.event('REAUDIT',evidence=ref(after)))
        self.assertEqual('NOT_COMPARABLE',m['cases'][self.cid]['technical_state'])

    def test_tampered_snapshot_and_raw_rejected(self):
        after=self.snapshot('AFTER','PASS');data=read(after);data['rows'][0]['status']='FAIL_TECHNICAL';write(after,data)
        with self.assertRaises(ValueError):append(self.model,self.event('REAUDIT',evidence=ref(after)))
        self.proof.write_text('changed')
        with self.assertRaises(ValueError):append(self.model,self.event('PRODUCER_RESPONSE',case_id=self.cid,reported_state='REPORTED_CORRECTED',statement='changed',evidence={'path':str(self.proof),'sha256':'0'*64}))

    def test_assignment_suggestion_is_not_accepted(self):
        m=append(self.model,self.event('PROPOSE_ACTION',case_id=self.cid,action='fix',owner='proposal',date='2026-10-16'))
        self.assertIsNone(m['cases'][self.cid]['owner_accepted']);self.assertIsNone(m['cases'][self.cid]['date_accepted'])
        m=append(m,self.event('ACCEPT_ASSIGNMENT',case_id=self.cid,owner='accepted',date='2026-10-20',evidence=ref(self.proof)))
        self.assertEqual('proposal',m['cases'][self.cid]['owner_proposed']);self.assertEqual('accepted',m['cases'][self.cid]['owner_accepted'])

    def test_risk_acceptance_does_not_resolve(self):
        m=append(self.model,self.event('ACCEPTANCE',case_id=self.cid,decision='ACCEPT_RISK',reviewer='test',rationale='synthetic',evidence=ref(self.proof)))
        self.assertEqual('OPEN',m['cases'][self.cid]['technical_state']);self.assertEqual('ACCEPTED_RISK',m['cases'][self.cid]['acceptance'])
        with self.assertRaises(ValueError):append(self.model,self.event('ACCEPTANCE',case_id=self.cid,decision='ACCEPT_CORRECTION',reviewer='test',rationale='not resolved',evidence=ref(self.proof)))

    def test_reappeared_defect_invalidates_correction_acceptance(self):
        m=append(self.model,self.event('REAUDIT',evidence=ref(self.snapshot('AFTER','PASS'))))
        m=append(m,self.event('ACCEPTANCE',case_id=self.cid,decision='ACCEPT_CORRECTION',reviewer='test',rationale='resolved',evidence=ref(self.proof)))
        m=append(m,self.event('REAUDIT',evidence=ref(self.snapshot('THIRD','FAIL_TECHNICAL'))))
        self.assertEqual('REAPPEARED',m['cases'][self.cid]['technical_state']);self.assertEqual('NOT_ACCEPTED',m['cases'][self.cid]['acceptance'])

    def test_event_history_and_baseline_identity_cannot_be_edited(self):
        m=append(self.model,self.event('PROPOSE_ACTION',case_id=self.cid,action='fix'));bad=deepcopy(m);bad['events'][0]['payload']['action']='forged'
        with self.assertRaises(ValueError):validate(bad)
        bad=deepcopy(m);bad['baseline_execution_id']='forged'
        with self.assertRaises(ValueError):validate(bad)


if __name__=='__main__':unittest.main()
