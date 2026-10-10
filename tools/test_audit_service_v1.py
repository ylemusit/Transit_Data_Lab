"""Bounded acceptance checks of two preserved internal service journeys."""
from copy import deepcopy
import unittest
from tools.audit_corpus_v1 import read
from tools.audit_service_v1 import RUNTIME, start, advance, validate, save, reference

RUN = RUNTIME / 'Service_20261009_FINAL_V1'


class ServiceAcceptance(unittest.TestCase):
    def model(self, step=8, fmt='GTFS_SCHEDULE'):
        return read(RUN / fmt / f'JOURNEY_{step:02}.json')

    def event(self, step, fmt='GTFS_SCHEDULE'):
        return read(RUN / fmt / f'EVENT_{step:02}.json')

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
        path = RUN / 'GTFS_SCHEDULE/JOURNEY_08.json'; before = reference(path)
        with self.assertRaises(FileExistsError): save(path, {})
        self.assertEqual(before, reference(path))


if __name__ == '__main__': unittest.main()
