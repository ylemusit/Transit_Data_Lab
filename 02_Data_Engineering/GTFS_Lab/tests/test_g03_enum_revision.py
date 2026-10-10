import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from gtfs_lab.g03_structure import _evaluate_types, _evaluate_types_v1, load_official_catalog, _rule_registry


class EnumRevisionTests(unittest.TestCase):
    def evaluate(self, file, field, values, legacy=False):
        payload=(field+'\n'+'\n'.join(values)+'\n').encode()
        with patch('gtfs_lab.g03_structure._read_zip_member',return_value=payload):
            return (_evaluate_types_v1 if legacy else _evaluate_types)(Path('memory.zip'),{file:zipfile.ZipInfo(file)},load_official_catalog(),[file])

    def test_official_domains_and_invalid_neighbours(self):
        domains=[('stops.txt','location_type',['0','1','2','3','4']),('pathways.txt','is_bidirectional',['0','1']),
                 ('transfers.txt','transfer_type',['0','1','2','3','4','5']),
                 ('translations.txt','table_name',['agency','stops','routes','trips','stop_times','pathways','levels','feed_info','attributions'])]
        for file,field,values in domains:
            with self.subTest(field=field):
                self.assertEqual('PASS',self.evaluate(file,field,values)['status'])
                self.assertEqual('FAIL_TECHNICAL',self.evaluate(file,field,['99','parent_station.1'])['status'])

    def test_calendar_inherited_domains_are_enforced_for_each_day(self):
        for day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            with self.subTest(day=day):
                self.assertEqual('PASS',self.evaluate('calendar.txt',day,['0','1'])['status'])
                self.assertEqual('FAIL_TECHNICAL',self.evaluate('calendar.txt',day,['9','yes'])['status'])

    def test_original_mode_is_preserved_and_rule_versions_are_distinct(self):
        self.assertEqual('FAIL_TECHNICAL',self.evaluate('stops.txt','location_type',['1'],legacy=True)['status'])
        self.assertEqual('PASS',self.evaluate('calendar.txt','tuesday',['9'],legacy=True)['status'])
        for version in ['1.0.0','1.1.0']:
            self.assertEqual(version,_rule_registry(version)['GTFS-G03-FIELD-TYPE'].semantic_version)

    def test_revision_records_reference_hash_and_empty_alias_is_not_rejected(self):
        result=self.evaluate('stops.txt','location_type',['','0'])
        self.assertEqual('PASS',result['status'])
        self.assertEqual('1.1.0',result['field_contract_revision'])
        self.assertEqual(64,len(result['field_contract_sha256']))
