"""Bounded technical inspectors. No legal or whole-feed conclusions.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
from lxml import etree

VERSION = 'compliance-v1/1'
MAX_BYTES = 1024 * 1024
MAX_ROWS = 10000
NS = 'http://www.netex.org.uk/netex'
RESULTS = {'PASS', 'FAIL_TECHNICAL', 'NOT_EVALUABLE', 'INSPECTION_ERROR'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dataset_hash(files):
    return digest(json.dumps({k: digest(v) for k, v in sorted(files.items())},
                             sort_keys=True, separators=(',', ':')).encode())


def result(status, reason, locator, observed=None):
    assert status in RESULTS
    return dict(result=status, reason=reason, locator=locator,
                observed=observed or ('PRESENT' if status == 'PASS' else 'INDETERMINATE'),
                legal_conclusion_allowed=False)


def csv_rows(data):
    if len(data) > MAX_BYTES or b'\x00' in data:
        raise ValueError('SIZE_OR_NUL')
    reader = csv.reader(io.StringIO(data.decode('utf-8-sig'), newline=''), strict=True)
    rows = list(reader)
    if not rows or len(rows) > MAX_ROWS + 1:
        raise ValueError('EMPTY_OR_ROW_LIMIT')
    header = rows[0]
    if len(set(header)) != len(header) or any(not x for x in header):
        raise ValueError('AMBIGUOUS_HEADER')
    if any(len(row) != len(header) for row in rows[1:]):
        raise ValueError('RAGGED_CSV')
    return header, [dict(zip(header, row)) for row in rows[1:]]


def inspect_gtfs(files, version, expected_version, complete=True):
    """Fixed-stop stop_times -> trips/stops foreign keys and platform type only.

    An inspection adapter for the GTFS raw VARCHAR contract, not an ingestion
    stack. Flexible locations are outside this committed technical scope.
    """
    loc = 'stop_times.txt#rows[*]/trip_id,stop_id -> trips.txt,stops.txt'
    if version != expected_version or not complete:
        return result('NOT_EVALUABLE', 'VERSION_OR_PARTIAL_INSPECTION', loc)
    names = {'trips.txt': {'trip_id'}, 'stops.txt': {'stop_id'},
             'stop_times.txt': {'trip_id', 'stop_id'}}
    if not names.keys() <= files.keys():
        return result('NOT_EVALUABLE', 'MISSING_INSPECTION_INPUT', loc)
    try:
        parsed = {name: csv_rows(files[name]) for name in names}
    except (ValueError, UnicodeError, csv.Error) as exc:
        return result('INSPECTION_ERROR', type(exc).__name__ + ':' + str(exc), loc)
    # No claim on a mixed/partial flex dataset, including a missing stop_id header.
    times = parsed['stop_times.txt'][1]
    if any(row.get('location_id') or row.get('location_group_id') for row in times):
        return result('NOT_EVALUABLE', 'FLEX_OUTSIDE_COMMITTED_SCOPE', loc)
    if any(not cols <= set(parsed[name][0]) for name, cols in names.items()):
        return result('NOT_EVALUABLE', 'SCHEMA_MISMATCH', loc)
    if not times:
        return result('NOT_EVALUABLE', 'NO_TARGET_ROWS', loc)
    trips = parsed['trips.txt'][1]
    stops = parsed['stops.txt'][1]
    for rows, key in [(trips, 'trip_id'), (stops, 'stop_id')]:
        ids = [r[key] for r in rows]
        if any(not x for x in ids) or len(set(ids)) != len(ids):
            return result('NOT_EVALUABLE', 'AMBIGUOUS_PARENT_IDENTITY', loc)
    trip_ids = {r['trip_id'] for r in trips}
    stop_ids = {r['stop_id']: r for r in stops}
    # Validate complete target scope before returning any finding.
    for index, row in enumerate(times, 2):
        rowloc = f'stop_times.txt#csv-record={index};trip_id={row["trip_id"]};stop_id={row["stop_id"]}'
        if not row['trip_id'] or not row['stop_id']:
            return result('FAIL_TECHNICAL', 'MISSING_FIXED_STOP_REFERENCE', rowloc, 'ABSENCE_CONFIRMED')
        if row['trip_id'] not in trip_ids or row['stop_id'] not in stop_ids:
            return result('FAIL_TECHNICAL', 'BROKEN_FOREIGN_REFERENCE', rowloc, 'ABSENCE_CONFIRMED')
        location_type = stop_ids[row['stop_id']].get('location_type', '')
        if location_type not in ('', '0'):
            return result('FAIL_TECHNICAL', 'REFERENCED_LOCATION_IS_NOT_PLATFORM', rowloc, 'PRESENT')
    return result('PASS', 'FIXED_STOP_REFERENCES_RESOLVE_TO_TRIP_AND_PLATFORM', loc)


def inspect_netex(data, version, expected_version, schema_path, complete=True):
    """Validate a standalone EPIP Line fragment, not a PublicationDelivery."""
    loc = '/n:Line[@id]/n:Name; n=' + NS
    if version != expected_version or not complete:
        return result('NOT_EVALUABLE', 'PROFILE_VERSION_OR_PARTIAL_INSPECTION', loc)
    if len(data) > MAX_BYTES or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        return result('INSPECTION_ERROR', 'UNSAFE_OR_OVERSIZED_XML', loc)
    parser = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True,
                             huge_tree=False, recover=False)
    try:
        root = etree.fromstring(data, parser)
    except (etree.XMLSyntaxError, ValueError) as exc:
        return result('INSPECTION_ERROR', type(exc).__name__, loc)
    if root.getroottree().docinfo.doctype:
        return result('INSPECTION_ERROR', 'DTD_FORBIDDEN_IN_ANY_ENCODING', loc)
    if root.tag != '{' + NS + '}Line':
        return result('NOT_EVALUABLE', 'FRAGMENT_SCOPE_OR_NAMESPACE_MISMATCH', loc)
    try:
        schema = etree.XMLSchema(etree.parse(str(schema_path), parser))
    except (OSError, etree.XMLSchemaParseError, etree.XMLSyntaxError):
        return result('INSPECTION_ERROR', 'TRUSTED_SCHEMA_LOAD_FAILURE', loc)
    if not schema.validate(root):
        # Stable machine codes; diagnostics do not execute or resolve feed URLs.
        codes = sorted({e.type_name for e in schema.error_log})
        missing = root.find('{' + NS + '}Name') is None
        return result('FAIL_TECHNICAL', 'XSD:' + ','.join(codes), loc,
                      'ABSENCE_CONFIRMED' if missing else 'PRESENT')
    return result('PASS', 'EPIP_XSD_LINE_FRAGMENT_VALID', loc)


def evaluate(case, sources, gtfs_version, netex_version):
    if case['standard'] == 'GTFS':
        files = {name: (case['directory'] / name).read_bytes() for name in case['files']}
        answer = inspect_gtfs(files, case['version'], gtfs_version, case['complete'])
        data_hash = dataset_hash(files)
    else:
        data = (case['directory'] / 'fragment.xml').read_bytes()
        answer = inspect_netex(data, case['version'], netex_version,
                               sources / 'NeTEx_publication_EPIP.xsd', case['complete'])
        data_hash = digest(data)
    return dict(answer, dataset_sha256=data_hash, evaluator_version=VERSION,
                evaluator_sha256=digest(Path(__file__).read_bytes()), dataset_id=case['id'])


def read_bounded(path):
    with path.open('rb') as handle:
        data=handle.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES:
        raise ValueError('INPUT_SIZE_LIMIT')
    return data


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--standard',choices=['GTFS','NETEX'],required=True)
    p.add_argument('--dataset',type=Path,required=True)
    p.add_argument('--version',required=True,help='Exact artifact identity in the V1 fixture manifest')
    p.add_argument('--partial',action='store_true')
    a=p.parse_args()
    root=Path(__file__).resolve().parents[1]
    sources=root/'03_Compliance/reports/evidence/compliance_v1_20260928/sources'
    manifest=json.loads((sources.parent/'source_manifest.json').read_text())
    # A corrupted evaluator installation is an inspection error, never a finding.
    try:
        for entry in manifest['sources']:
            if digest((sources/entry['path']).read_bytes())!=entry['sha256']:
                raise ValueError('TRUSTED_SOURCE_HASH_MISMATCH')
        if a.standard=='GTFS':
            files={n:read_bounded(a.dataset/n) for n in ['trips.txt','stops.txt','stop_times.txt'] if (a.dataset/n).exists()}
            answer=inspect_gtfs(files,a.version,'GTFS-SNAPSHOT-SHA256:'+digest((sources/'gtfs_reference.md').read_bytes()),not a.partial)
            identity=dataset_hash(files)
        else:
            data=read_bounded(a.dataset)
            answer=inspect_netex(data,a.version,'EPIP-XSD-NeTEx-1.3.1:'+manifest['netex_commit'],sources/'NeTEx_publication_EPIP.xsd',not a.partial)
            identity=digest(data)
    except (OSError, ValueError) as exc:
        answer=result('INSPECTION_ERROR',type(exc).__name__+':'+str(exc),'input')
        identity=None
    print(json.dumps(dict(answer,evaluator_version=VERSION,evaluator_sha256=digest(Path(__file__).read_bytes()),
                          dataset_sha256=identity),sort_keys=True))


if __name__=='__main__':
    main()
