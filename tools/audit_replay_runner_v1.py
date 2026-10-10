"""Executed inside a fresh isolated venv and copied evaluator/source tree."""
import argparse
import json
from pathlib import Path
import sys
import socket
import importlib.metadata


def execute(root):
    root=Path(root).resolve();source=root/'source'
    if not Path(sys.prefix).resolve().is_relative_to(root):raise ValueError('Not using the fresh replay venv')
    sys.path[:0]=[str(source),str(source/'02_Data_Engineering/GTFS_Lab'),str(source/'02_Data_Engineering/NeTEx_Lab')]
    network={'blocked':0}
    def offline(event,args):
        if event in {'socket.connect','socket.getaddrinfo','socket.bind'}:
            network['blocked']+=1;raise PermissionError('TDL_REPLAY_OFFLINE_NETWORK_BLOCKED')
    sys.addaudithook(offline)
    try:socket.create_connection(('127.0.0.1',9),timeout=1)
    except PermissionError:pass
    else:raise ValueError('Offline guard failed')
    from tools.audit_corpus_v1 import read,write,sha
    from tools.audit_precision_v1 import gtfs_observation,netex_observation,classify,investigate
    from tools.audit_replay_semantics_v1 import semantic,digest
    manifest=read(root/'REPLAY_INPUT_MANIFEST.json')
    for name,expected in manifest['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root) or sha(path)!=expected:raise ValueError('Replay input drift: '+name)
    baseline=read(root/'BASELINE.json');results=[]
    original_roots=[Path(p).resolve() for p in baseline['normalization_roots']]+[
        Path('P:/TransitDataLab/02_Data').resolve(),Path('P:/TransitDataLab/03_Evidence').resolve(),
        Path('P:/TransitDataLab/05_Client').resolve(),Path('P:/TransitDataLab/04_Runtime/Current/TDL').resolve()]
    source_access={'blocked':0}
    def separate_inputs(event,args):
        if event=='open' and isinstance(args[0],(str,bytes)):
            path=Path(__import__('os').fsdecode(args[0])).resolve()
            if any(path.is_relative_to(p) for p in original_roots):
                source_access['blocked']+=1;raise PermissionError('TDL_REPLAY_ORIGINAL_INPUT_ROOT_BLOCKED')
    sys.addaudithook(separate_inputs)
    try:open(original_roots[0]/'README.md','rb')
    except PermissionError:pass
    else:raise ValueError('Original input access guard failed')
    output=root/'execution'
    if output.exists():raise ValueError('Use a fresh execution directory')
    output.mkdir()
    for case in baseline['cases']:
        path=root/'fixtures'/case['fixture']
        if case['scope']!='CURRENT_RULE_ILLUSTRATION':obs={'status':'UNIMPLEMENTED','reason':'Candidate family, no approved evaluator'};raw={}
        elif case['format']=='GTFS_SCHEDULE':obs,raw=gtfs_observation(path,case,output/'ingestion')
        else:obs,raw=netex_observation(path,case)
        review=investigate(case,obs,raw);initial=classify(case['expected'],obs)
        classification=review['category'] if review['category'] in {'DETECTED_OTHER_RULE','STATUS_SCOPE_DIFFERENCE'} else initial
        new={'observed':obs,'raw':raw,'classification':classification,'investigation':review}
        old=baseline['results'][case['case_id']]
        old_norm=semantic(old,baseline['normalization_roots']);new_norm=semantic(new,[str(root),str(source)])
        raw_path=output/'raw'/(case['case_id']+'.json');write(raw_path,raw)
        results.append({'case_id':case['case_id'],'criterion_id':case['criterion_id'],'format':case['format'],
                        'fixture_sha256':sha(path),'observed':obs,'classification':classification,
                        'raw_path':str(raw_path),'raw_sha256':sha(raw_path),'baseline_semantic_sha256':digest(old_norm),
                        'replay_semantic_sha256':digest(new_norm),'semantic_equivalent':old_norm==new_norm})
    loaded=[]
    for name,module in sorted(sys.modules.items()):
        if name.startswith(('gtfs_lab','netex_lab','tools.audit_','transit_data_lab_compliance')) and getattr(module,'__file__',None):
            path=Path(module.__file__).resolve()
            if not path.is_relative_to(source):raise ValueError('Evaluator imported from outside copied source: '+name)
            relative=path.relative_to(root).as_posix()
            if manifest['files'].get(relative)!=sha(path):raise ValueError('Imported module is not a declared input: '+name)
            loaded.append({'module':name,'path':str(path),'sha256':sha(path)})
    if network['blocked']!=1:raise ValueError('Evaluator attempted a network operation')
    if source_access['blocked']!=1:raise ValueError('Evaluator attempted to read an original input root')
    for name,expected in manifest['files'].items():
        if sha(root/name)!=expected:raise ValueError('Replay modified an input')
    receipt={'contract':'TDL_OFFLINE_REPLAY/1','execution_id':root.name+'-EXECUTION','baseline_execution_id':baseline['execution_id'],
        'rows':results,'counts':{'scenarios':len(results),'equivalent':sum(r['semantic_equivalent'] for r in results),
                                'different':sum(not r['semantic_equivalent'] for r in results)},
        'environment':{'python':sys.version,'prefix':sys.prefix,'base_prefix':sys.base_prefix,'executable':sys.executable,
            'lxml':importlib.metadata.version('lxml'),'fresh_venv':True,'isolated_mode':bool(sys.flags.isolated),'loaded_evaluator_modules':loaded},
        'network_guard':{'self_test_blocked':True,'evaluator_network_attempts':network['blocked']-1},
        'original_input_guard':{'self_test_blocked':True,'evaluator_read_attempts':source_access['blocked']-1,
                                'blocked_roots':[str(p) for p in original_roots]},
        'normalization':{'removed_keys':sorted(__import__('tools.audit_replay_semantics_v1',fromlist=['VOLATILE_KEYS']).VOLATILE_KEYS),
                         'root_substitution':'Explicit execution path metadata only; source payload and evidence SHA values retained',
                         'metadata_key_rule':'Remove volatile keys only from audit envelopes, never nested source payload.'},
        'inputs_verified_before_after':True,'holdout_accessed':False,'same_windows_host':True,
        'limits':['Evaluator replay only; not PDF/GIS/DB pipeline or external-validator replay.','Same host and base Python; not clean-machine or second-OS acceptance.',
                 'Existing unknown/profile/review states must remain unchanged.','Schema copied solely for private internal replay; no redistribution approval.']}
    write(root/'REPLAY_RESULT.json',receipt)
    return receipt['counts']


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(execute(args.root)))
