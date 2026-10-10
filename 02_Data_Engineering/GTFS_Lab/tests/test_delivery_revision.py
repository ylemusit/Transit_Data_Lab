import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from gtfs_lab.client_workflow import _sanitize_delivery, _redact_path_text
from gtfs_lab.delivery_integrity import verify_inventory, contained
from gtfs_lab.delivery_privacy import inspect_delivery_content


class DeliveryRevisionTests(unittest.TestCase):
    def test_sanitizer_preserves_input_bytes_urls_and_observed_values(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); inp=root/'engine_run/input'; inp.mkdir(parents=True)
            raw=b'stop_url,stop_name\nhttps://example.org/ruta?next=/horarios,C:\\producer\\name\n'
            (inp/'stops.txt').write_bytes(raw)
            doc={'database':str(root/'private.duckdb'),'observed':'C:\\producer\\name','url':'https://example.org/ruta?next=/horarios'}
            p=root/'result.json'; p.write_text(json.dumps(doc),encoding='utf-8')
            _sanitize_delivery(root)
            result=json.loads(p.read_text(encoding='utf-8'))
            self.assertEqual(raw,(inp/'stops.txt').read_bytes())
            self.assertEqual(doc['observed'],result['observed']); self.assertEqual(doc['url'],result['url'])
            self.assertEqual('[LOCAL_PATH_REDACTED]',result['database'])
            self.assertEqual(doc['url'],_redact_path_text(doc['url']))

    def test_streamed_json_preserves_observations_and_redacts_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); p=root/'result.json'
            p.write_text(json.dumps({'artifact':str(root/'private'),'observed':'C:\\producer\\value','url':'https://example.org/a?next=/x'}),encoding='utf-8')
            with patch('gtfs_lab.client_workflow._LARGE_JSON_STREAM_THRESHOLD',1): _sanitize_delivery(root)
            value=json.loads(p.read_text(encoding='utf-8'))
            self.assertEqual('C:\\producer\\value',value['observed']); self.assertEqual('[LOCAL_PATH_REDACTED]',value['artifact'])

    def test_inventory_rejects_empty_extra_missing_changed_and_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); p=root/'evidence.txt'; p.write_bytes(b'original')
            records={'evidence.txt':{'size_bytes':8,'sha256':hashlib.sha256(b'original').hexdigest()}}
            self.assertEqual(1,verify_inventory(root,records,set()))
            with self.assertRaises(ValueError):verify_inventory(root,{},set())
            extra=root/'extra.txt'; extra.write_bytes(b'extra')
            with self.assertRaises(ValueError):verify_inventory(root,records,set())
            self.assertEqual(1,verify_inventory(root,records,{'extra.txt'}))
            p.write_bytes(b'changed!')
            with self.assertRaises(ValueError):verify_inventory(root,records,{'extra.txt'})
            with self.assertRaises(ValueError):verify_inventory(root,{'missing.txt':records['evidence.txt']},{'extra.txt'})
            for name in ['../outside','C:/outside','/absolute','a\\b']:
                with self.assertRaises(ValueError):contained(root,name)

    def test_archive_content_and_opaque_files_have_explicit_coverage(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with zipfile.ZipFile(root/'book.xlsx','w') as z:z.writestr('xl/sharedStrings.xml',r'<t>C:\private\feed.zip</t>')
            result=inspect_delivery_content(root)
            self.assertEqual('FAIL_PATH_FOUND',result['status'])
            with zipfile.ZipFile(root/'book.xlsx','w') as z:
                z.writestr('xl/sharedStrings.xml','<t>https://example.org/a?next=/home/x</t>')
                z.writestr('_rels/.rels','<Relationships/>')
            self.assertEqual('PASS',inspect_delivery_content(root)['status'])
            (root/'opaque.bin').write_bytes(b'opaque')
            result=inspect_delivery_content(root)
            self.assertEqual('PARTIAL_UNSCANNED_CONTENT',result['status']); self.assertEqual(['opaque.bin'],result['unscanned_files'])
