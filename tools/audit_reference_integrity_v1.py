"""Seal and verify the named internal reference version and its synthetic files."""
import argparse
import json
import os
from pathlib import Path
import stat
import shutil
from tools.audit_corpus_v1 import ROOT, read, write, sha, verify_sources
from tools.audit_reference_bank_v1 import validate_bank

NAMES={"REFERENCE_MANIFEST.json","REFERENCE_SEAL.json"}


def inventory(root):
    root=Path(root);pending=[root];paths={}
    while pending:
        current=pending.pop()
        if current.is_symlink() or getattr(current.stat(),"st_file_attributes",0)&stat.FILE_ATTRIBUTE_REPARSE_POINT:raise ValueError("Reference reparse root")
        with os.scandir(current) as entries:
            for entry in entries:
                if entry.is_symlink() or getattr(entry.stat(follow_symlinks=False),"st_file_attributes",0)&stat.FILE_ATTRIBUTE_REPARSE_POINT:raise ValueError("Reference reparse entry")
                path=Path(entry.path)
                if entry.is_dir(follow_symlinks=False):pending.append(path)
                elif entry.is_file(follow_symlinks=False):paths[path.relative_to(root).as_posix()]={"sha256":sha(path),"bytes":path.stat().st_size}
    return paths


def seal(output):
    output=Path(output)
    if (output/"REFERENCE_SEAL.json").exists():raise ValueError("Reference already sealed; create a new version")
    fact=read(output.parent/"FACT_CHECK_FINAL.json")
    if fact["result"]!="PASS" or fact["cases"]!=114:raise ValueError("Missing fact acceptance")
    bank=read(output/"REFERENCE_BANK.json");registry=read(output/"SOURCE_REGISTRY.json")
    checks=validate_bank(bank,read(output/"CRITERIA.json"),registry)
    sources=verify_sources(registry)
    identities={}
    for name in ("audit_corpus_v1.py","audit_reference_definitions_v1.py","audit_reference_bank_v1.py",
                 "audit_reference_facts_v1.py","audit_reference_integrity_v1.py","test_audit_corpus_reference_v1.py"):
        source=ROOT/"tools"/name;target=output/"authoring_sources"/name;target.parent.mkdir(exist_ok=True)
        if target.exists():raise ValueError("Authoring snapshot already exists")
        shutil.copyfile(source,target);identities[name]={"sha256":sha(target),"original":"tools/"+name}
    shutil.copyfile(output.parent/"FACT_CHECK_FINAL.json",output/"FACT_CHECK.json")
    write(output/"FINAL_ACCEPTANCE.json",{"contract":"TDL_REFERENCE_ACCEPTANCE/1","sources":sources,"bank":checks,
        "authoring_snapshots":identities,"tests":75,"fact_check_sha256":sha(output/"FACT_CHECK.json"),
        "independent_human_review":False,"readiness_changed":False,"baseline_promoted":False})
    artifacts=inventory(output)
    write(output/"REFERENCE_MANIFEST.json",{"contract":"TDL_REFERENCE_MANIFEST/1","metadata_artifacts":artifacts,
        "fixture_root":bank["fixture_root"],"fixture_artifacts":inventory(Path(bank["fixture_root"]))})
    write(output/"REFERENCE_SEAL.json",{"manifest_sha256":sha(output/"REFERENCE_MANIFEST.json"),"authentication":"INTEGRITY_ONLY_NOT_SIGNED"})
    return verify(output)


def verify(output):
    output=Path(output);manifest=read(output/"REFERENCE_MANIFEST.json")
    if sha(output/"REFERENCE_MANIFEST.json")!=read(output/"REFERENCE_SEAL.json")["manifest_sha256"]:raise ValueError("Reference seal mismatch")
    artifacts={k:v for k,v in inventory(output).items() if k not in NAMES}
    if artifacts!=manifest["metadata_artifacts"]:raise ValueError("Reference metadata altered")
    bank=read(output/"REFERENCE_BANK.json");registry=read(output/"SOURCE_REGISTRY.json")
    if manifest["fixture_root"]!=bank["fixture_root"] or inventory(Path(bank["fixture_root"]))!=manifest["fixture_artifacts"]:raise ValueError("Reference fixtures altered")
    result=validate_bank(bank,read(output/"CRITERIA.json"),registry);sources=verify_sources(registry)
    return {"result":"PASS","metadata_artifacts":len(artifacts),"fixtures":len(manifest["fixture_artifacts"]),"cases":result["cases"],
            "identified_source_files":sources["identified_files"],"missing_sources":sources["missing_sources"],"manifest_sha256":sha(output/"REFERENCE_MANIFEST.json")}


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,required=True);parser.add_argument("--seal",action="store_true")
    args=parser.parse_args();print(json.dumps(seal(args.output) if args.seal else verify(args.output),ensure_ascii=False))
