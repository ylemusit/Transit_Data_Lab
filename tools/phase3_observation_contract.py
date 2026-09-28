"""Bounded observation envelope in existing notes VARCHAR; no audit rule.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import hashlib
import json
import re

VERSION = 'phase3-observation-envelope/1'
PAIRS = {
    ('COMPLETED', 'PRESENT'), ('COMPLETED', 'ABSENCE_CONFIRMED'),
    ('COMPLETED', 'INDETERMINATE'), ('NOT_INSPECTED', 'INDETERMINATE'),
    ('FAILED', 'INDETERMINATE'),
}


def validate(record, scopes):
    required = {'contract_version', 'dataset_id', 'dataset_version', 'dataset_sha256',
                'inspection_run', 'evaluator_version', 'scope_unit_id',
                'inspection_status', 'observed_result', 'errors', 'limitations',
                'inspection_extent', 'synthetic'}
    if set(record) != required or record['contract_version'] != VERSION:
        raise ValueError('CONTRACT_VERSION_OR_FIELDS')
    for key in required - {'errors', 'limitations', 'synthetic'}:
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError('REQUIRED_TEXT:' + key)
    if not re.fullmatch('[0-9a-f]{64}', record['dataset_sha256']):
        raise ValueError('DATASET_HASH')
    if record['scope_unit_id'] not in scopes:
        raise ValueError('UNKNOWN_SCOPE')
    if (record['inspection_status'], record['observed_result']) not in PAIRS:
        raise ValueError('STATUS_RESULT_COLLISION')
    if type(record['synthetic']) is not bool:
        raise ValueError('SYNTHETIC_TYPE')
    for key in ('errors', 'limitations'):
        if not isinstance(record[key], list) or any(not isinstance(v, str) or not v.strip() for v in record[key]):
            raise ValueError('ERRORS_LIMITATIONS_TYPE')
    if record['inspection_status'] == 'FAILED' and not record['errors']:
        raise ValueError('FAILURE_REASON_REQUIRED')
    if record['inspection_status'] != 'FAILED' and record['errors']:
        raise ValueError('ERROR_REQUIRES_FAILED')
    if record['observed_result'] == 'ABSENCE_CONFIRMED' and record['inspection_extent'] != 'COMPLETE_DECLARED_LOCATOR':
        raise ValueError('ABSENCE_REQUIRES_COMPLETE_INSPECTION')
    if record['observed_result'] == 'INDETERMINATE' and not record['limitations']:
        raise ValueError('INDETERMINATE_REASON_REQUIRED')
    return record


def encode(record, scopes):
    return json.dumps(validate(record, scopes), sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def decode(value, scopes):
    return validate(json.loads(value), scopes)


def content_hash(value):
    return hashlib.sha256(value).hexdigest()
