"""Portable acceptance checks of two disposable synthetic service journeys."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.audit_corpus_v1 import read, write
from tools.audit_service_v1 import STAGES, start, advance, validate, save, reference, build_package
from tools.audit_lifecycle_v1 import initialize, append


class ServiceAcceptance(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='tdl_service_')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.enterContext(patch('tools.audit_service_v1.RUNTIME', self.root))
        self.enterContext(patch('tools.audit_service_v1.ROOTS', (self.root,)))
        self.enterContext(patch('tools.audit_lifecycle_v1.ALLOWED_ROOTS', (self.root,)))
        before = self.snapshot('BEFORE', ['FAIL_TECHNICAL', 'FAIL_TECHNICAL', 'PASS'])
        after = self.snapshot('AFTER', ['PASS', 'FAIL_TECHNICAL', 'FAIL_TECHNICAL'])
        proof = self.root / 'statement.txt'
        proof.write_text('Synthetic response and acceptance, no real client.', encoding='utf-8')
        ledger = initialize(before)
        refs = [self.ledger('LEDGER_00', ledger)]
        for case_id, case in ledger['cases'].items():
            if case['logical_dataset_id'].endswith('-0'):
                ledger = append(ledger, {'type': 'PRODUCER_RESPONSE', 'actor': 'test', 'origin': 'SYNTHETIC_SIMULATION',
                    'case_id': case_id, 'reported_state': 'REPORTED_CORRECTED', 'statement': 'Reported only', 'evidence': reference(proof)})
        refs.append(self.ledger('LEDGER_04', ledger))
        ledger = append(ledger, {'type': 'REAUDIT', 'actor': 'test', 'origin': 'SYNTHETIC_SIMULATION', 'evidence': after})
        refs.append(self.ledger('LEDGER_06', ledger))
        for case_id, case in ledger['cases'].items():
            if case['technical_state'] == 'RESOLVED':
                ledger = append(ledger, {'type': 'ACCEPTANCE', 'actor': 'test', 'origin': 'SYNTHETIC_SIMULATION',
                    'case_id': case_id, 'decision': 'ACCEPT_CORRECTION', 'reviewer': 'test', 'rationale': 'Synthetic verified resolution', 'evidence': reference(proof)})
        refs.append(self.ledger('LEDGER_08', ledger))
        for fmt in ('GTFS_SCHEDULE', 'NETEX'):
            folder = self.root / fmt
            folder.mkdir()
            criteria = sorted({r['criterion_id'] for r in read(Path(before['path']))['rows'] if r['format'] == fmt})
            save(folder / 'PLAN.json', {'format': fmt, 'criteria': criteria, 'agreement_origin': 'INTERNAL_SCENARIO_PLAN', 'profile_claim': 'NOT_EVALUATED'})
            save(folder / 'REVIEW.json', {'format': fmt, 'snapshot': before, 'result': 'PASS_WITH_LIMITATIONS',
                'review_kind': 'AUTHOR_SELF_REVIEW', 'human_emission_approval': False})
            v1 = build_package(folder / 'DELIVERY_V1', before, fmt)
            v2 = build_package(folder / 'DELIVERY_V2', after, fmt)
            evidence = [{'snapshot': before}, {'plan': reference(folder / 'PLAN.json')}, {'snapshot': before},
                {'review': reference(folder / 'REVIEW.json')}, {'package': v1, 'ledger': refs[0]},
                {'ledger': refs[1]}, {'snapshot': after, 'ledger': refs[2], 'package': v2}, {'ledger': refs[3]}]
            model = start('synthetic-test-' + fmt, fmt)
            for step, (stage, entries) in enumerate(zip(STAGES, evidence), 1):
                event = {'stage': stage, 'actor': 'test', 'origin': 'INTERNAL_SYNTHETIC_EXERCISE', 'evidence': entries}
                save(folder / f'EVENT_{step:02}.json', event)
                model = advance(model, event)
                save(folder / f'JOURNEY_{step:02}.json', model)

    def ledger(self, name, model):
        path = self.root / (name + '.json')
        write(path, model)
        return reference(path)

    def snapshot(self, name, statuses):
        rows, native_rows = [], []
        for fmt in ('GTFS_SCHEDULE', 'NETEX'):
            for i, status in enumerate(statuses):
                case_id = fmt + '-' + str(i)
                raw = self.root / f'{name}-{case_id}-raw.json'
                write(raw, {'status': status})
                rule = {'rule_id': 'RULE-' + str(i), 'version': '1.0.0', 'status': status, 'checked_rows': 1}
                native_rows.append({'case_id': case_id, 'criterion_id': rule['rule_id'], 'format': fmt,
                    'fixture_sha256': 'b' * 64, 'observed': {'status': status, 'raw_rule_result': rule},
                    'raw_path': str(raw), 'raw_sha256': reference(raw)['sha256']})
                rows.append({'format': fmt, 'logical_dataset_id': case_id, 'criterion_id': rule['rule_id'],
                    'rule_version': '1.0.0', 'scope_id': 'SYNTHETIC_TEST', 'source_case_id': case_id,
                    'status': status, 'coverage_complete': True, 'fixture_sha256': 'b' * 64, 'raw_evidence': reference(raw)})
        native = self.root / (name + '-native.json')
        write(native, {'run_id': name, 'rows': native_rows})
        snapshot = self.root / (name + '.json')
        write(snapshot, {'contract': 'TDL_REAUDIT_SNAPSHOT/1', 'execution_id': name,
            'execution_evidence': reference(native), 'rows': rows})
        return reference(snapshot)

    def model(self, step=8, fmt='GTFS_SCHEDULE'):
        return read(self.root / fmt / f'JOURNEY_{step:02}.json')

    def event(self, step, fmt='GTFS_SCHEDULE'):
        return read(self.root / fmt / f'EVENT_{step:02}.json')

    def test_complete_two_formats_preserve_open_issues_and_versions(self):
        for fmt in ('GTFS_SCHEDULE', 'NETEX'):
            m = self.model(fmt=fmt); self.assertTrue(validate(m))
            self.assertEqual(len(m['events']), 8)
            self.assertEqual(m['state']['technical_states'], {'RESOLVED': 1, 'PERSISTENT': 1, 'NEW': 1})
            self.assertNotEqual(m['state']['delivery_v1'], m['state']['delivery_v2'])
            self.assertNotEqual(m['state']['baseline_execution_id'], m['state']['reaudit_execution_id'])
            self.assertFalse(m['state']['issues_all_resolved'])
            self.assertEqual(m['client_acceptance'], 'NOT_OBTAINED')

    def test_stage_cannot_be_skipped(self):
        with self.assertRaises(ValueError):
            advance(start('test', 'GTFS_SCHEDULE'), self.event(2))

    def test_prior_decision_cannot_be_silently_rewritten(self):
        m = self.model(); m['events'][2]['payload']['actor'] = 'Other actor'
        with self.assertRaises(ValueError): validate(m)

    def test_delivery_of_wrong_version_rejected(self):
        event = self.event(5)
        event['evidence']['package'] = self.model()['state']['delivery_v2']
        with self.assertRaises(ValueError): advance(self.model(4), event)

    def test_reported_response_cannot_import_future_resolution(self):
        event = self.event(6)
        event['evidence']['ledger'] = self.model()['state']['latest_ledger']
        with self.assertRaises(ValueError): advance(self.model(5), event)

    def test_correction_history_cannot_be_rolled_back(self):
        event = self.event(8)
        event['evidence']['ledger'] = self.model(5)['state']['latest_ledger']
        with self.assertRaises(ValueError): advance(self.model(7), event)

    def test_internal_record_cannot_claim_external_acceptance(self):
        event = self.event(1); event['client_acceptance'] = True
        with self.assertRaises(ValueError): advance(start('test', 'GTFS_SCHEDULE'), event)

    def test_previous_record_cannot_be_overwritten(self):
        path = self.root / 'GTFS_SCHEDULE/JOURNEY_08.json'; before = reference(path)
        with self.assertRaises(FileExistsError): save(path, {})
        self.assertEqual(before, reference(path))


if __name__ == '__main__': unittest.main()
