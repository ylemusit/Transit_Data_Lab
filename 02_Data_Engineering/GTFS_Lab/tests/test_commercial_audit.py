from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from gtfs_lab.commercial_audit import load_catalogue, load_legal_context, prepare_atlas, row_for, validation_matrix
from gtfs_lab.commercial_content import LEGAL


class CommercialAuditTests(unittest.TestCase):
    def test_legal_context_integrity_and_failure_boundaries(self):
        root = Path(__file__).resolve().parents[3]
        path = root / '03_Compliance/reports/legal_update_20261008/source_registry.json'
        document = load_legal_context(path, root)
        self.assertFalse(document['legal_conclusion_allowed'])
        with tempfile.TemporaryDirectory() as tmp:
            changed = Path(tmp) / 'context.json'
            for mutation, expected in (
                ('hash', 'hash mismatch'), ('path', 'Invalid legal context path'),
                ('boundary', 'boundary'), ('uncaptured', 'Uncaptured'),
            ):
                bad = copy.deepcopy(document)
                if mutation == 'hash': bad['sources'][0]['sha256'] = '0' * 64
                if mutation == 'path': bad['sources'][0]['local_path'] = '../outside.xml'
                if mutation == 'boundary': bad['legal_conclusion_allowed'] = True
                if mutation == 'uncaptured': bad['sources'][0]['capture_status'] = 'REFERENCE_ONLY'
                changed.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, expected): load_legal_context(changed, root)

    def test_context_review_keeps_external_applicability_undetermined(self):
        self.assertTrue({'PRIV-01', 'SPAT-01', 'REUSE-01', 'NAP-01'}.issubset({e['id'] for e in LEGAL}))
        for entry in LEGAL:
            self.assertFalse(entry['legal_conclusion_allowed'])
            self.assertEqual(entry['applicability'], 'UNDETERMINED')
            self.assertTrue(entry['authority_types'])

    def test_current_its_context_uses_successor_without_legal_verdict(self):
        entry = next(e for e in LEGAL if e['id'] == 'ES-02')
        self.assertIn('450/2026', entry['source'])
        self.assertIn('BOE-A-2026-12035', entry['url'])
        self.assertIn('Deroga', entry['analysis'])
        self.assertEqual(entry['mapping'], 'CONTEXT_ONLY')
        self.assertEqual(entry['rules'], [])

    def fixture(self):
        tables=dict(routes=[dict(route_id='A',route_short_name='1'),dict(route_id='B',route_short_name='2')],
                    trips=[dict(trip_id='T1',route_id='A',shape_id='S'),dict(trip_id='T2',route_id='B',shape_id='S')],
                    stops=[],stop_times=[],frequencies=[],
                    shapes=[dict(shape_id='S',shape_pt_sequence='1',shape_pt_lon='2.65',shape_pt_lat='39.57',shape_dist_traveled='10'),
                            dict(shape_id='S',shape_pt_sequence='2',shape_pt_lon='2.65',shape_pt_lat='39.57',shape_dist_traveled='10'),
                            dict(shape_id='UNLINKED',shape_pt_sequence='1',shape_pt_lon='2.66',shape_pt_lat='39.58',shape_dist_traveled='20'),
                            dict(shape_id='UNLINKED',shape_pt_sequence='2',shape_pt_lon='2.66',shape_pt_lat='39.58',shape_dist_traveled='20')])
        occurrences=[dict(normalized_locator='shapes.txt:data_row:2',source_record_id='engine:1'),
                     dict(normalized_locator='shapes.txt:data_row:2',source_record_id='legacy:1'),
                     dict(normalized_locator='shapes.txt:data_row:4',source_record_id='engine:2')]
        model=dict(cases=[dict(case_id='PAL-G07-DUP',occurrences=occurrences,reconciled_event_count=2)])
        return model,tables

    def test_shared_shape_counts_events_once_and_keeps_all_routes(self):
        model,tables=self.fixture();atlas=prepare_atlas(model,tables)
        self.assertEqual(atlas['case_details'][0]['event_count'],2)
        self.assertEqual(atlas['case_details'][0]['route_ids'],['A','B'])
        self.assertEqual([r['cases']['PAL-G07-DUP'] for r in atlas['routes']],[1,1])
        self.assertEqual(len(atlas['points']['features']),3)

    def test_unlinked_shape_is_drawn_without_inventing_route(self):
        model,tables=self.fixture();atlas=prepare_atlas(model,tables)
        self.assertEqual(atlas['unassigned_shapes'][0]['shape_id'],'UNLINKED')
        self.assertEqual(atlas['case_details'][0]['events_without_route'],1)
        self.assertTrue(any(f['properties']==dict(route_id='',shape_id='UNLINKED') for f in atlas['lines']['features']))

    def test_predecessor_follows_sequence_not_file_order(self):
        model,tables=self.fixture()
        tables['shapes'][0],tables['shapes'][1]=tables['shapes'][1],tables['shapes'][0]
        model['cases'][0]['occurrences'][0]['normalized_locator']='shapes.txt:data_row:1'
        model['cases'][0]['occurrences'][1]['normalized_locator']='shapes.txt:data_row:1'
        atlas=prepare_atlas(model,tables)
        self.assertEqual(atlas['case_details'][0]['example']['previous']['data_row'],2)

    def test_rejects_geometry_that_disagrees_with_reviewed_case(self):
        model,tables=self.fixture();tables['shapes'][1]['shape_pt_lon']='2.67'
        with self.assertRaisesRegex(ValueError,'classification'):prepare_atlas(model,tables)

    def test_rejects_changed_distance_and_event_count(self):
        model,tables=self.fixture();tables['shapes'][1]['shape_dist_traveled']='11'
        with self.assertRaisesRegex(ValueError,'repeated distance'):prepare_atlas(model,tables)
        model,tables=self.fixture();model['cases'][0]['reconciled_event_count']=3
        with self.assertRaisesRegex(ValueError,'accounting'):prepare_atlas(model,tables)

    def test_rejects_ambiguous_sequence_and_invalid_locator(self):
        model,tables=self.fixture();tables['shapes'][1]['shape_pt_sequence']='1'
        with self.assertRaisesRegex(ValueError,'sequence'):prepare_atlas(model,tables)
        with self.assertRaisesRegex(ValueError,'outside'):row_for(tables,dict(normalized_locator='shapes.txt:data_row:0'))

    def test_pass_and_no_evaluation_do_not_turn_into_legal_compliance(self):
        rule=dict(rule_id='GTFS-G03-HEADER-SCHEMA',finding_count=0,status='NOT_EVALUABLE',coverage=None,
                  specification_reference='synthetic')
        compliance=dict(rule_id='V1-RULE-GTFS',reason='synthetic',result='PASS',legal_conclusion_allowed=False)
        checks=validation_matrix(dict(matrix=[rule],cases=[]),compliance)
        self.assertEqual(checks[0]['status'],'NOT_EVALUABLE')
        self.assertEqual(checks[0]['legal_mapping'],'NO_DIRECT_LEGAL_MAPPING_DOCUMENTED')
        self.assertEqual(checks[1]['legal_mapping'],'DOCUMENTED_PARTIAL')
        self.assertTrue(all(e['mapping']!='FULL' for e in LEGAL))
        bad=copy.deepcopy(compliance);bad['legal_conclusion_allowed']=True
        with self.assertRaisesRegex(ValueError,'legal boundary'):validation_matrix(dict(matrix=[],cases=[]),bad)

    def test_unknown_rule_requires_its_own_explanation(self):
        with self.assertRaisesRegex(ValueError,'Missing client explanation'):
            validation_matrix(dict(cases=[],matrix=[dict(rule_id='GTFS-G99-UNKNOWN')]),{})

    def test_full_matrix_retains_legacy_and_reconciles_duplicate_compliance(self):
        model=dict(cases=[],matrix=[])
        compliance=dict(rule_id='V1-RULE-GTFS',reason='synthetic',result='PASS',legal_conclusion_allowed=False)
        source=[dict(stage='LEGACY',rule_id='GTFS-REF-SERVICE',finding_count=0,result='PASS'),
                dict(stage='LEGACY',rule_id='V1-RULE-GTFS',result='PASS'),
                dict(stage='COMPLIANCE',rule_id='V1-RULE-GTFS',result='PASS')]
        checks=validation_matrix(model,compliance,source)
        self.assertEqual(len(checks),2)
        self.assertEqual(checks[0]['source_matrix_row_count'],2)
        self.assertEqual(checks[1]['rule_id'],'GTFS-REF-SERVICE')
        source[2]['result']='FAIL_TECHNICAL'
        with self.assertRaisesRegex(ValueError,'status mismatch'):validation_matrix(model,compliance,source)

    def test_full_matrix_cannot_silently_omit_source_rule(self):
        compliance=dict(rule_id='V1-RULE-GTFS',reason='synthetic',result='PASS',legal_conclusion_allowed=False)
        with self.assertRaisesRegex(ValueError,'omits or adds'):
            validation_matrix(dict(cases=[],matrix=[]),compliance,[dict(stage='G99',rule_id='GTFS-G99-X',result='PASS')])

    def test_rejects_superseded_reconciliation_catalogue(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'catalogue.json';path.write_text('[]',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'earlier reconciliation'):load_catalogue(path)

    def test_final_catalogue_retains_all_descriptions_and_dispositions(self):
        rows=[]
        for state,count in dict(PARTIAL=6,HUMAN_REVIEW_REQUIRED=12,DEFERRED=20,OUT_OF_SCOPE_V1=10).items():
            rows.extend(dict(requirement_id=f'R-{len(rows)}-{i}',description='Synthetic requirement',disposition=state) for i in range(count))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'catalogue.json';path.write_text(json.dumps(dict(requirements=rows)),encoding='utf-8')
            self.assertEqual(load_catalogue(path),rows)
            rows[0]['description']='';path.write_text(json.dumps(dict(requirements=rows)),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'descriptions'):load_catalogue(path)


if __name__=='__main__':unittest.main()
