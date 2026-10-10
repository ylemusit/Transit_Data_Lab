import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET
from gtfs_lab.professional_audit import build_model, preflight, generate
from gtfs_lab.professional_workbook import build_workbook, record_rows, expanded_columns
from tests import test_professional_audit as fixtures

NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class PortableWorkbookTests(unittest.TestCase):
    def test_workbook_has_complete_sheets_typed_counts_and_literal_external_strings(self):
        manifest,interpretation,decisions=fixtures.ProfessionalAuditTests().fixture()
        model=build_model(manifest,interpretation,'b'*64,'PORTABLE-TEST',decisions)
        model['client_cases'][0]['title']='=HYPERLINK("https://example.org")'
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'book.xlsx'; receipt=build_workbook(model,path)
            with zipfile.ZipFile(path) as z:
                workbook=ET.fromstring(z.read('xl/workbook.xml'))
                names=[x.attrib['name'] for x in workbook.findall('s:sheets/s:sheet',NS)]
                self.assertEqual(['Resumen','Casos','Ocurrencias','Seguimiento','Matriz','Evidencias'],names)
                strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
                self.assertIn(model['client_cases'][0]['title'],strings)
                for member in z.namelist():
                    if member.startswith('xl/worksheets/sheet') and member.endswith('.xml'):
                        sheet=ET.fromstring(z.read(member)); self.assertEqual([],sheet.findall('.//s:f',NS))
                summary=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
                self.assertTrue(any(c.attrib.get('t','n')=='n' for c in summary.findall('.//s:c',NS)))
                cases=ET.fromstring(z.read('xl/worksheets/sheet2.xml'))
                self.assertEqual(2,len(cases.findall('s:sheetData/s:row',NS)))
            self.assertEqual(1,receipt['sheets']['Casos'])

    def test_long_raw_json_can_be_reconstructed_without_truncation(self):
        source={'case_id':'C-LONG','observed':'á'*40000,'nested':{'id':'00001'}}
        headers,rows=record_rows([source])
        raw=''.join(rows[0][i] for i,h in enumerate(headers) if h.startswith('Registro íntegro'))
        self.assertEqual(source,json.loads(raw))
        expanded,values,widths=expanded_columns(headers,rows,[60]*len(headers))
        chunks=[values[0][i] for i,h in enumerate(expanded) if h.startswith('Registro íntegro')]
        self.assertEqual(source,json.loads(''.join(chunks)))
        self.assertLessEqual(max(len(s) for s in chunks),1000)

    def test_complete_matrix_records_are_retained_in_occurrences(self):
        manifest,interpretation,decisions=fixtures.ProfessionalAuditTests().fixture()
        manifest['rule_matrix']=[{'rule_id':'RULE-1','stage':'G03','status':'PASS','custom_detail':{'literal':'00001'}}]
        model=build_model(manifest,interpretation,'b'*64,'MATRIX-TEST',decisions)
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'book.xlsx'; build_workbook(model,p)
            with zipfile.ZipFile(p) as z:
                strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
            self.assertTrue(any('custom_detail' in s and '00001' in s for s in strings))

    def test_demo_label_is_additive_and_historical_projection_remains_available(self):
        manifest,interpretation,decisions=fixtures.ProfessionalAuditTests().fixture()
        manifest['dataset_identity']['source_provenance']='SYNTHETIC'
        old=build_model(manifest,interpretation,'b'*64,'REV',decisions)
        current=build_model(manifest,interpretation,'b'*64,'REV',decisions,include_source_scope=True)
        self.assertNotIn('DEMO.',old['presentation']['basis'])
        self.assertIn('DEMO.',current['presentation']['basis'])

    def test_missing_runtime_is_rejected_before_output_exists(self):
        import importlib.metadata
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'output'
            with patch('importlib.metadata.version',side_effect=importlib.metadata.PackageNotFoundError('missing')):
                with self.assertRaisesRegex(ValueError,'Missing professional runtime'):
                    generate(Path('unused'),output,'REV',Path('unused.zip'))
            self.assertFalse(output.exists()); self.assertFalse(output.with_name('output.partial').exists())

    def test_legacy_renderer_requires_existing_command_and_script(self):
        with self.assertRaisesRegex(ValueError,'unavailable'):
            preflight(['nonexistent_node_executable','absent_script.mjs'])
