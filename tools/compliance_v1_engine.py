"""Bounded technical inspectors. No legal or whole-feed conclusions.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
from contextlib import contextmanager
from lxml import etree

VERSION = 'compliance-v1/2'
MAX_BYTES = 1024 * 1024
MAX_ROWS = 1_000_000
MAX_RECORD_BYTES = 4 * 1024 * 1024
MAX_COLUMNS = 256
MAX_FIELD_BYTES = 128 * 1024
MAX_GTFS_FILE_BYTES = 512 * 1024 * 1024
NS = 'http://www.netex.org.uk/netex'
RESULTS = {'PASS', 'FAIL_TECHNICAL', 'NOT_EVALUABLE', 'INSPECTION_ERROR'}


class _SchemaMismatch(Exception):
    pass


class _AmbiguousIdentity(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dataset_hash(files):
    return digest(json.dumps({k: digest(v) for k, v in sorted(files.items())},
                             sort_keys=True, separators=(',', ':')).encode())


def dataset_hash_paths(files):
    hashes = {}
    for name, path in sorted(files.items()):
        h = hashlib.sha256()
        with Path(path).open('rb') as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b''):
                h.update(block)
        hashes[name] = h.hexdigest()
    return digest(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode())


@contextmanager
def _open_input(value):
    if isinstance(value, (bytes, bytearray)):
        with io.BytesIO(value) as handle:
            yield handle
    else:
        with Path(value).open('rb') as handle:
            yield handle


def result(status, reason, locator, observed=None):
    assert status in RESULTS
    return dict(result=status, reason=reason, locator=locator,
                observed=observed or ('PRESENT' if status == 'PASS' else 'INDETERMINATE'),
                legal_conclusion_allowed=False)


class _BoundedLines:
    """Decode physical CSV lines while bounding individual and logical records."""
    def __init__(self, binary):
        self.binary = binary
        self.total_bytes = 0
        self.record_start_bytes = 0
        self.line_number = 0
        self.record_is_whitespace = True

    def __iter__(self):
        first = True
        while True:
            raw = self.binary.readline(MAX_RECORD_BYTES + 1)
            if not raw:
                return
            if len(raw) > MAX_RECORD_BYTES:
                raise ValueError('RECORD_SIZE_LIMIT')
            if b'\x00' in raw:
                raise ValueError('SIZE_OR_NUL')
            self.total_bytes += len(raw)
            if raw.strip(b' \t\r\n\v\f'):
                self.record_is_whitespace = False
            if self.total_bytes - self.record_start_bytes > MAX_RECORD_BYTES:
                raise ValueError('RECORD_SIZE_LIMIT')
            try:
                line = raw.decode('utf-8-sig' if first else 'utf-8')
            except UnicodeError as exc:
                raise ValueError('UNSUPPORTED_ENCODING') from exc
            first = False
            self.line_number += 1
            yield line

    def finish_record(self):
        size = self.total_bytes - self.record_start_bytes
        if size > MAX_RECORD_BYTES:
            raise ValueError('RECORD_SIZE_LIMIT')
        whitespace_only = self.record_is_whitespace
        self.record_is_whitespace = True
        self.record_start_bytes = self.total_bytes
        return size, whitespace_only


def _table_rows(handle):
    lines = _BoundedLines(handle)
    reader = csv.reader(lines, strict=True)
    header = next(reader, None)
    lines.finish_record()
    if not header or len(header) > MAX_COLUMNS or len(set(header)) != len(header) or any(not x for x in header) or any(len(x.encode('utf-8')) > MAX_FIELD_BYTES for x in header):
        raise ValueError('AMBIGUOUS_HEADER')
    return header, lines, reader


def _stream_table(binary, on_row, required=()):
    header, lines, reader = _table_rows(binary)
    if not set(required) <= set(header):
        raise _SchemaMismatch()
    count = 0
    for row in reader:
        _, whitespace_only = lines.finish_record()
        if row == [] or whitespace_only:
            continue
        if len(row) != len(header):
            raise ValueError('RAGGED_CSV')
        if any(len(value.encode('utf-8')) > MAX_FIELD_BYTES for value in row):
            raise ValueError('FIELD_SIZE_LIMIT')
        count += 1
        if count > MAX_ROWS:
            raise ValueError('ROW_LIMIT')
        on_row(count + 1, header, dict(zip(header, row)))
    return header, count


def csv_rows(data):
    """Compatibility parser API; the Compliance GTFS rule uses streaming tables."""
    if len(data) > MAX_GTFS_FILE_BYTES:
        raise ValueError('INPUT_SIZE_LIMIT')
    rows = []
    header, _ = _stream_table(io.BytesIO(data), lambda _index, _header, row: rows.append(row))
    return header, rows


def _stream_file(value, on_row, required=()):
    with _open_input(value) as handle:
        return _stream_table(handle, on_row, required)


def _input_size(value):
    return len(value) if isinstance(value, (bytes, bytearray)) else Path(value).stat().st_size


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
        if any(_input_size(files[name]) > MAX_GTFS_FILE_BYTES for name in names):
            raise ValueError('INPUT_SIZE_LIMIT')
        trips = set()
        stops = {}
        flex = False
        for name, required in (('trips.txt', {'trip_id'}), ('stops.txt', {'stop_id'})):
            def collect(_index, _header, row):
                key = 'trip_id' if name == 'trips.txt' else 'stop_id'
                if row.get(key):
                    if name == 'trips.txt':
                        trips.add(row[key])
                    else:
                        stops[row[key]] = row.get('location_type', '')
            header, _ = _stream_file(files[name], collect, required)
            if not required <= set(header):
                return result('NOT_EVALUABLE', 'SCHEMA_MISMATCH', loc)
        if any(not value for value in trips) or len(trips) == 0 or len(stops) == 0:
            return result('NOT_EVALUABLE', 'AMBIGUOUS_PARENT_IDENTITY', loc)
        seen_trips, seen_stops = set(), set()
        # Duplicate and missing parent IDs make references ambiguous.
        for name, key, seen in (('trips.txt', 'trip_id', seen_trips), ('stops.txt', 'stop_id', seen_stops)):
            def check_ids(_index, _header, row):
                value = row.get(key, '')
                if not value or value in seen:
                    raise _AmbiguousIdentity()
                seen.add(value)
            _stream_file(files[name], check_ids, {key})
        first_finding = None
        target_count = 0
        def inspect_time(index, header, row):
            nonlocal flex, first_finding, target_count
            target_count += 1
            if row.get('location_id') or row.get('location_group_id'):
                flex = True
            if first_finding is not None:
                return
            rowloc = f'stop_times.txt#csv-record={index};trip_id={row["trip_id"]};stop_id={row["stop_id"]}'
            if not row['trip_id'] or not row['stop_id']:
                first_finding = result('FAIL_TECHNICAL', 'MISSING_FIXED_STOP_REFERENCE', rowloc, 'ABSENCE_CONFIRMED')
            elif row['trip_id'] not in trips or row['stop_id'] not in stops:
                first_finding = result('FAIL_TECHNICAL', 'BROKEN_FOREIGN_REFERENCE', rowloc, 'ABSENCE_CONFIRMED')
            elif stops[row['stop_id']] not in ('', '0'):
                first_finding = result('FAIL_TECHNICAL', 'REFERENCED_LOCATION_IS_NOT_PLATFORM', rowloc, 'PRESENT')
        times_header, target_count = _stream_file(files['stop_times.txt'], inspect_time, {'trip_id', 'stop_id'})
        if not {'trip_id', 'stop_id'} <= set(times_header):
            return result('NOT_EVALUABLE', 'SCHEMA_MISMATCH', loc)
        if flex:
            return result('NOT_EVALUABLE', 'FLEX_OUTSIDE_COMMITTED_SCOPE', loc)
        if target_count == 0:
            return result('NOT_EVALUABLE', 'NO_TARGET_ROWS', loc)
        if first_finding:
            return first_finding
        return result('PASS', 'FIXED_STOP_REFERENCES_RESOLVE_TO_TRIP_AND_PLATFORM', loc)
    except _SchemaMismatch:
        return result('NOT_EVALUABLE', 'SCHEMA_MISMATCH', loc)
    except _AmbiguousIdentity:
        return result('NOT_EVALUABLE', 'AMBIGUOUS_PARENT_IDENTITY', loc)
    except (ValueError, UnicodeError, csv.Error) as exc:
        return result('INSPECTION_ERROR', type(exc).__name__ + ':' + str(exc), loc)


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
        files = {name: case['directory'] / name for name in case['files']}
        if any(path.stat().st_size > MAX_GTFS_FILE_BYTES for path in files.values()):
            answer = result('INSPECTION_ERROR', 'INPUT_SIZE_LIMIT', 'input')
            data_hash = None
            return dict(answer, dataset_sha256=data_hash, evaluator_version=VERSION,
                        evaluator_sha256=digest(Path(__file__).read_bytes()), dataset_id=case['id'])
        answer = inspect_gtfs(files, case['version'], gtfs_version, case['complete'])
        data_hash = dataset_hash_paths(files)
    else:
        data = (case['directory'] / 'fragment.xml').read_bytes()
        answer = inspect_netex(data, case['version'], netex_version,
                               sources / 'NeTEx_publication_EPIP.xsd', case['complete'])
        data_hash = digest(data)
    return dict(answer, dataset_sha256=data_hash, evaluator_version=VERSION,
                evaluator_sha256=digest(Path(__file__).read_bytes()), dataset_id=case['id'])


def read_bounded(path, maximum=MAX_BYTES):
    with path.open('rb') as handle:
        data=handle.read(maximum+1)
    if len(data)>maximum:
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
            files={n:a.dataset/n for n in ['trips.txt','stops.txt','stop_times.txt'] if (a.dataset/n).exists()}
            if any(path.stat().st_size > MAX_GTFS_FILE_BYTES for path in files.values()):
                raise ValueError('INPUT_SIZE_LIMIT')
            answer=inspect_gtfs(files,a.version,'GTFS-SNAPSHOT-SHA256:'+digest((sources/'gtfs_reference.md').read_bytes()),not a.partial)
            identity=dataset_hash_paths(files)
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
