"""Prepare a bounded private offline recipe without modifying source baselines."""
import argparse
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tools.audit_corpus_v1 import ROOT,read,write,sha,SCHEMA
from tools.audit_precision_v1 import REFERENCE
from tools.audit_reference_integrity_v1 import verify


def module_closure(package, directory, seeds):
    pending=list(seeds);found=set()
    while pending:
        module=pending.pop();path=directory/((module.replace('.', '/'))+'.py')
        if not path.exists() or path in found:continue
        found.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            if isinstance(node,ast.ImportFrom) and node.level:
                prefix=module.split('.')[:-node.level]
                target='.'.join(prefix+([node.module] if node.module else []))
                if target:pending.append(target)
                for alias in node.names:pending.append('.'.join(filter(None,[target,alias.name])))
    found.add(directory/'__init__.py')
    return found


def prepare(root,wheelhouse,output):
    root=Path(root).resolve();wheelhouse=Path(wheelhouse);output=Path(output)
    if root.exists() or output.exists():raise ValueError('Use new replay roots and receipt')
    if not root.is_relative_to(Path('P:/TransitDataLab/04_Runtime/AuditQuality').resolve()):raise ValueError('Replay outside named runtime root')
    ref=verify(REFERENCE);bank=read(REFERENCE/'REFERENCE_BANK.json')
    measurement_path=ROOT/'reports/audit_precision_v1/run_20261009_final_v1/MEASUREMENT.json'
    measurement=read(measurement_path);files={};originals={}
    for name,digest in measurement['engine_inputs'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Evaluator drift')
    root.mkdir()
    def copy(src,relative):
        src=Path(src);dest=root/relative
        if src.is_symlink():raise ValueError('Do not copy source symlink')
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        if sha(src)!=sha(dest):raise ValueError('Copy mismatch')
        files[dest.relative_to(root).as_posix()]=sha(dest);originals[str(src)]=sha(src)
    for pkg,seeds in [('GTFS_Lab',['g03_structure','ingestion','validation','compliance_adapter','g04_identity','g05_temporal','g06_operations','g07_spatial','g08_quality']),('NeTEx_Lab',['audit'])]:
        name='gtfs_lab' if pkg=='GTFS_Lab' else 'netex_lab';directory=ROOT/'02_Data_Engineering'/pkg/name
        for path in sorted(module_closure(name,directory,seeds)):
            copy(path,Path('source')/path.relative_to(ROOT))
        for path in sorted((ROOT/'02_Data_Engineering'/pkg/'spec').glob('*.json')):
            copy(path,Path('source')/path.relative_to(ROOT))
    for name in ['audit_precision_v1.py','audit_corpus_v1.py','audit_reference_integrity_v1.py','audit_reference_bank_v1.py','audit_reference_definitions_v1.py','audit_replay_semantics_v1.py']:
        copy(ROOT/'tools'/name,Path('source/tools')/name)
    for name in ['tools/compliance_v1_engine.py','03_Compliance/reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md','03_Compliance/reports/evidence/compliance_v1_20260928/source_manifest.json']:
        copy(ROOT/name,Path('source')/name)
    copy(ROOT/SCHEMA,Path('source')/SCHEMA)
    schema=read(ROOT/SCHEMA);schema_root=((ROOT/SCHEMA).parent/schema['root_schema']).resolve().parent.parent
    for dependency in schema['dependencies']:
        path=schema_root/dependency['path']
        import hashlib
        if hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=dependency['sha256']:raise ValueError('Schema identity mismatch')
        copy(path,Path('source/01_Research_Standards/NeTEx/schemas/v2.0.0')/dependency['path'])
    for case in bank['cases']:copy(Path(bank['fixture_root'])/case['fixture'],Path('fixtures')/case['fixture'])
    wheels=list(wheelhouse.glob('lxml-6.1.3-cp312-cp312-win_amd64.whl'))
    if len(wheels)!=1:raise ValueError('Need the exact local lxml wheel')
    copy(wheels[0],Path('wheelhouse')/wheels[0].name)
    copy(ROOT/'tools/audit_replay_runner_v1.py','runner.py')
    baseline={'execution_id':measurement['run_id'],'reference_manifest_sha256':ref['manifest_sha256'],
              'measurement_sha256':sha(measurement_path),'cases':bank['cases'],'normalization_roots':[
                  str(ROOT),str(Path(bank['fixture_root'])),str(Path('P:/TransitDataLab/04_Runtime/AuditQuality/Precision_20261009_FINAL_V1'))], 'results':{}}
    for row in measurement['rows']:
        raw_path=Path(row['raw_path'])
        if sha(raw_path)!=row['raw_sha256']:raise ValueError('Baseline RAW drift')
        baseline['results'][row['case_id']]={'observed':row['observed'],'raw':read(raw_path),'classification':row['classification'],'investigation':row['investigation']}
    write(root/'BASELINE.json',baseline);files['BASELINE.json']=sha(root/'BASELINE.json')
    write(root/'REPLAY_INPUT_MANIFEST.json',{'contract':'TDL_REPLAY_INPUT/1','files':files,'original_files':originals,
          'reference_manifest_sha256':ref['manifest_sha256'],'private_internal_only':True,'hashes_authenticate_author':False})
    # Script is portable within this prepared Windows/Python 3.12 bundle.
    recipe="""param([string]$BasePython = 'python')
$ErrorActionPreference = 'Stop'
$ReplayRoot = $PSScriptRoot
$ReplayPython = Join-Path $ReplayRoot 'venv/Scripts/python.exe'
if (Test-Path -LiteralPath (Join-Path $ReplayRoot 'venv')) { throw 'Use a new replay directory; environment already exists.' }
& $BasePython -m venv (Join-Path $ReplayRoot 'venv')
if ($LASTEXITCODE -ne 0) { throw 'venv failed' }
& $ReplayPython -m pip --disable-pip-version-check install --no-index --no-deps --find-links (Join-Path $ReplayRoot 'wheelhouse') lxml==6.1.3
if ($LASTEXITCODE -ne 0) { throw 'offline dependency install failed' }
& $ReplayPython -I (Join-Path $ReplayRoot 'runner.py') --root $ReplayRoot
if ($LASTEXITCODE -ne 0) { throw 'offline replay failed' }
"""
    (root/'RUN_OFFLINE.ps1').write_text(recipe,encoding='utf8')
    env=dict(os.environ)
    for key in ('PYTHONPATH','PYTHONHOME','NETEX_SCHEMA_PATH','TDL_RESOURCE_STAGE_FILE'):env.pop(key,None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    command=['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'RUN_OFFLINE.ps1'),'-BasePython',sys.executable]
    proc=subprocess.run(command,capture_output=True,env=env,timeout=240)
    (root/'recipe.stdout.log').write_bytes(proc.stdout);(root/'recipe.stderr.log').write_bytes(proc.stderr)
    if proc.returncode:raise RuntimeError('Offline recipe failed; inspect '+str(root/'recipe.stderr.log'))
    result=read(root/'REPLAY_RESULT.json')
    for name,digest in originals.items():
        if sha(Path(name))!=digest:raise ValueError('Original changed')
    if verify(REFERENCE)!=ref:raise ValueError('Reference changed')
    receipt={'contract':'TDL_REPLAY_PREPARATION/1','root':str(root),'command':command,'recipe_sha256':sha(root/'RUN_OFFLINE.ps1'),
             'input_manifest_sha256':sha(root/'REPLAY_INPUT_MANIFEST.json'),'result_path':str(root/'REPLAY_RESULT.json'),
             'result_sha256':sha(root/'REPLAY_RESULT.json'),'counts':result['counts'],'original_files_verified':len(originals),
             'prepared_files':len(files),'offline_install':'pip --no-index --no-deps from pinned local wheel',
             'source_root_isolated':True,'same_host':True,'scope':'G03-G08, legacy, Compliance adapter, NeTEx XML/XSD/diagnostics; 114 synthetic witnesses',
             'task_16_state':'COMPLETADA_REPLAY_DELIMITADO' if not result['counts']['different'] else 'DIFERENCIAS_REQUIEREN_REVISION'}
    write(output,receipt);return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True);parser.add_argument('--wheelhouse',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(prepare(args.root,args.wheelhouse,args.output),ensure_ascii=False))
