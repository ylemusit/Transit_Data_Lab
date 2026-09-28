"""Deterministic, synthetic fixture builder; only writes a NEW directory.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
import argparse
import json
from pathlib import Path
from compliance_v1_engine import digest


def build(out, gtfs_version, netex_version):
    out.mkdir(parents=True, exist_ok=False)
    base = {
        'agency.txt': b'agency_id,agency_name,agency_url,agency_timezone\nA,Synthetic,https://example.org,Europe/Madrid\n',
        'routes.txt': b'route_id,agency_id,route_short_name,route_long_name,route_type\nR,A,1,Synthetic,3\n',
        'trips.txt': b'route_id,service_id,trip_id\nR,D,T\n',
        'stops.txt': b'stop_id,stop_name,stop_lat,stop_lon,location_type\nS,Synthetic A,40,-3,0\nZ,Synthetic B,40.1,-3.1,0\n',
        'stop_times.txt': b'trip_id,arrival_time,departure_time,stop_id,stop_sequence\nT,25:00:00,25:00:00,S,1\nT,25:01:00,25:01:00,Z,2\n',
        'calendar_dates.txt': b'service_id,date,exception_type\nD,20260928,1\n',
    }
    cases = []
    def add(standard, name, files, expected, version=None, complete=True):
        case_id = standard.lower() + '-' + name
        d = out / case_id
        d.mkdir()
        for file, data in files.items():
            (d/file).write_bytes(data)
        cases.append(dict(id=case_id, standard=standard, files=sorted(files),
                          hashes={n:digest(b) for n,b in sorted(files.items())},
                          version=version or (gtfs_version if standard=='GTFS' else netex_version),
                          complete=complete, expected=expected, synthetic=True))
    add('GTFS', 'valid', base, 'PASS')
    add('GTFS', 'missing-value', dict(base, **{'stop_times.txt':base['stop_times.txt'].replace(b',S,1',b',,1')}), 'FAIL_TECHNICAL')
    add('GTFS', 'broken-stop', dict(base, **{'stop_times.txt':base['stop_times.txt'].replace(b',S,1',b',MISSING,1')}), 'FAIL_TECHNICAL')
    add('GTFS', 'broken-trip', dict(base, **{'trips.txt':base['trips.txt'].replace(b',T\n',b',OTHER\n')}), 'FAIL_TECHNICAL')
    add('GTFS', 'boundary', dict(base, **{'stops.txt':base['stops.txt'].replace(b',0\n',b',\n')}), 'PASS')
    add('GTFS', 'unexpected-enum', dict(base, **{'stops.txt':base['stops.txt'].replace(b',0\n',b',9\n')}), 'FAIL_TECHNICAL')
    add('GTFS', 'station-reference', dict(base, **{'stops.txt':base['stops.txt'].replace(b',0\n',b',1\n')}), 'FAIL_TECHNICAL')
    add('GTFS', 'malformed', dict(base, **{'stop_times.txt':b'trip_id,stop_id\n"unterminated,S\n'}), 'INSPECTION_ERROR')
    add('GTFS', 'parser-failure', dict(base, **{'stops.txt':b'\xff\xfe\x00'}), 'INSPECTION_ERROR')
    add('GTFS', 'schema-mismatch', dict(base, **{'stop_times.txt':b'wrong,columns\nT,S\n'}), 'NOT_EVALUABLE')
    add('GTFS', 'missing-file', {k:v for k,v in base.items() if k!='stops.txt'}, 'NOT_EVALUABLE')
    add('GTFS', 'wrong-version', base, 'NOT_EVALUABLE', 'unknown')
    add('GTFS', 'partial-inspection', base, 'NOT_EVALUABLE', complete=False)
    add('GTFS', 'flex', dict(base, **{'stop_times.txt':b'trip_id,stop_id,location_id\nT,,AREA\n'}), 'NOT_EVALUABLE')
    add('GTFS', 'duplicate-parent', dict(base, **{'trips.txt':b'trip_id\nT\nT\n'}), 'NOT_EVALUABLE')
    add('GTFS', 'empty-target', dict(base, **{'stop_times.txt':b'trip_id,stop_id\n'}), 'NOT_EVALUABLE')
    add('GTFS', 'duplicate-header', dict(base, **{'stop_times.txt':b'trip_id,stop_id,stop_id\nT,S,S\n'}), 'INSPECTION_ERROR')
    add('GTFS', 'ragged', dict(base, **{'stop_times.txt':b'trip_id,stop_id\nT,S,extra\n'}), 'INSPECTION_ERROR')
    xml = b'<Line xmlns="http://www.netex.org.uk/netex" id="tdl:Line:1" version="1"><Name>Synthetic line</Name></Line>'
    add('NETEX','valid',{'fragment.xml':xml},'PASS')
    add('NETEX','missing-name',{'fragment.xml':xml.replace(b'<Name>Synthetic line</Name>',b'')},'FAIL_TECHNICAL')
    # Empty multilingual text is permitted by this XSD. Do not invent a nonempty rule.
    add('NETEX','boundary',{'fragment.xml':xml.replace(b'Synthetic line',b'')},'PASS')
    add('NETEX','unknown-enum',{'fragment.xml':xml.replace(b'</Line>',b'<TransportMode>not-a-mode</TransportMode></Line>')},'FAIL_TECHNICAL')
    add('NETEX','malformed',{'fragment.xml':xml[:-7]},'INSPECTION_ERROR')
    add('NETEX','unknown-profile',{'fragment.xml':xml},'NOT_EVALUABLE','unknown')
    add('NETEX','partial-inspection',{'fragment.xml':xml},'NOT_EVALUABLE',complete=False)
    add('NETEX','namespace',{'fragment.xml':xml.replace(b'http://www.netex.org.uk/netex',b'https://invalid.example')},'NOT_EVALUABLE')
    add('NETEX','external-entity',{'fragment.xml':b'<!DOCTYPE Line [<!ENTITY x SYSTEM "file:///not-read">]>'+xml},'INSPECTION_ERROR')
    add('NETEX','missing-id',{'fragment.xml':xml.replace(b' id="tdl:Line:1"',b'')},'FAIL_TECHNICAL')
    manifest=(json.dumps(cases,indent=2)+'\n').encode('utf-8')
    (out/'manifest.json').write_bytes(manifest)
    return cases


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--sources',required=True,type=Path)
    a=p.parse_args()
    manifest=json.loads((a.sources.parent/'source_manifest.json').read_text())
    gv='GTFS-SNAPSHOT-SHA256:'+digest((a.sources/'gtfs_reference.md').read_bytes())
    nv='EPIP-XSD-NeTEx-1.3.1:'+manifest['netex_commit']
    print(len(build(a.output,gv,nv)))
