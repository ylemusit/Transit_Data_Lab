import tempfile
from pathlib import Path
import unittest
from tools.audit_replay_semantics_v1 import semantic,digest
from tools.audit_replay_prepare_v1 import module_closure


class ReplayTests(unittest.TestCase):
    def test_execution_metadata_may_change_but_status_must_not(self):
        a={'rule_id':'R','dataset_id':'A','status':'FAIL_TECHNICAL'}
        b={**a,'dataset_id':'B'}
        self.assertEqual(semantic(a),semantic(b))
        b['status']='PASS';self.assertNotEqual(digest(semantic(a)),digest(semantic(b)))

    def test_source_payload_dataset_id_is_not_discarded(self):
        a={'rule_id':'R','observed_value':{'dataset_id':'A','rule_id':'producer-field'}}
        b={'rule_id':'R','observed_value':{'dataset_id':'B','rule_id':'producer-field'}}
        self.assertNotEqual(semantic(a),semantic(b))

    def test_source_root_in_observed_value_is_not_rewritten(self):
        value={'rule_id':'R','observed_value':'P:/root/input'}
        self.assertEqual(value,semantic(value,['P:/root']))
        self.assertEqual('<EXECUTION_ROOT>/input',semantic({'input_path':'P:/root/input'},['P:/root'])['input_path'])

    def test_coverage_and_findings_are_semantic(self):
        a={'rule_id':'R','coverage':{'state':'FULL'},'findings':[]}
        b={**a,'coverage':{'state':'PARTIAL'}}
        self.assertNotEqual(semantic(a),semantic(b))
        b={**a,'findings':[{'observed_value':'missing'}]};self.assertNotEqual(semantic(a),semantic(b))

    def test_relative_import_closure_includes_nested_function_import(self):
        with tempfile.TemporaryDirectory(prefix='tdl_replay_') as name:
            folder=Path(name)
            (folder/'__init__.py').write_text('');(folder/'a.py').write_text('def f():\n from .b import x\n')
            (folder/'b.py').write_text('from .c import y\nx=1\n');(folder/'c.py').write_text('y=2\n')
            self.assertEqual({'__init__.py','a.py','b.py','c.py'},{p.name for p in module_closure('test',folder,['a'])})


if __name__=='__main__':unittest.main()
