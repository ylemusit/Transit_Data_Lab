"""Run a hash-pinned local external validator on current GTFS witnesses."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import subprocess
from pathlib import Path
import json
from collections import Counter
from tools.audit_corpus_v1 import ROOT, read, write, sha
from tools.audit_precision_v1 import REFERENCE
from tools.audit_reference_integrity_v1 import verify

JAR_SHA='19293ddd9b6f954f216d4f12054bd8a3232921751c4484339e339764a91000e2'


def run(root,output):
    root=Path(root);output=Path(output)
    if output.exists():raise ValueError('Use a new comparison receipt')
    download=read(root/'DOWNLOAD_RECEIPT.json');jar=Path(download['asset'])
    if sha(jar)!=JAR_SHA or download['sha256']!=JAR_SHA:raise ValueError('External binary identity mismatch')
    before=verify(REFERENCE);bank=read(REFERENCE/'REFERENCE_BANK.json')
    cases=[c for c in bank['cases'] if c['format']=='GTFS_SCHEDULE' and c['scope']=='CURRENT_RULE_ILLUSTRATION']
    java=subprocess.run(['java','-version'],capture_output=True,text=True,check=True)
    java_path=__import__('shutil').which('java')
    def execute(case):
        fixture=Path(bank['fixture_root'])/case['fixture'];dest=root/'cases'/case['case_id']
        if dest.exists() or sha(fixture)!=case['sha256']:raise ValueError('Fixture drift or reused execution')
        dest.mkdir(parents=True)
        command=['java','-Xmx512m','-jar',str(jar),'-i',str(fixture),'-o',str(dest),'-t','1','-d','2026-10-09','-svu']
        proc=subprocess.run(command,capture_output=True,timeout=90)
        (dest/'stdout.log').write_bytes(proc.stdout);(dest/'stderr.log').write_bytes(proc.stderr)
        report=read(dest/'report.json') if (dest/'report.json').exists() else None
        system=read(dest/'system_errors.json') if (dest/'system_errors.json').exists() else None
        if report and report['summary']['validatorVersion']!='8.0.1':raise ValueError('External report version mismatch')
        return {'case_id':case['case_id'],'criterion_id':case['criterion_id'],'expected_state':case['expected']['criterion_state'],
                'fixture_sha256':case['sha256'],'exit_code':proc.returncode,'command':command,
                'report_path':str(dest/'report.json'),'report_sha256':sha(dest/'report.json') if report else None,
                'system_errors_path':str(dest/'system_errors.json'),'system_errors_sha256':sha(dest/'system_errors.json') if system is not None else None,
                'system_notices':system.get('notices') if system is not None else None,
                'notices':report['notices'] if report else [],
                'logs':{name:sha(dest/name) for name in ('stdout.log','stderr.log')},
                'focal_status':'NOT_DERIVED_FROM_NOTICE_ABSENCE'}
    with ThreadPoolExecutor(max_workers=2) as executor:rows=list(executor.map(execute,cases))
    after=verify(REFERENCE)
    if before!=after:raise ValueError('Reference modified')
    receipt={'contract':'TDL_EXTERNAL_COMPARISON/1','version':'8.0.1','download':download,'java_version':java.stderr.strip(),
             'java_path':java_path,'java_launcher_sha256':sha(Path(java_path)),'execution_parameters':{'heap':'512m','threads':1,'date':'2026-10-09','skip_validator_update':True,'local_input_only':True},
             'reference_manifest_sha256':before['manifest_sha256'],'rows':rows,'scenarios':len(rows),
             'code_counts':dict(Counter(n['code'] for r in rows for n in r['notices'])),
             'tool_sha256':sha(Path(__file__)),'holdout_accessed':False,'operator_data_sent':False,
             'limits':['External absence of notice is not criterion PASS.', 'Notices require code/table/field mapping and review, not severity-only agreement.',
                       'GTFS external tool does not audit NeTEx. lxml is not an independent NeTEx comparison.']}
    write(output,receipt)
    return {'scenarios':len(rows),'reports':sum(r['report_sha256'] is not None for r in rows),'exit_codes':dict(Counter(r['exit_code'] for r in rows)),'notice_codes':len(receipt['code_counts'])}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(run(args.root,args.output)))
