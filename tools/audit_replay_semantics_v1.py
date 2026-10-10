"""Explicit normalization of execution metadata, never audit findings or statuses."""
import json
import hashlib

VOLATILE_KEYS={'run_id','dataset_id','ingestion_timestamp_utc','started_at_utc','ended_at_utc'}


PATH_METADATA={'input_path','work_dir','source_zip','outputDirectory','source_root','schema_path','report_path','raw_path'}


def semantic(value, roots=(), path=()):
    if isinstance(value,dict):
        audit_envelope='rule_id' in value or 'gtfs_lab_version' in value or 'parser_version' in value
        source_payload=any(k in {'observed_value','observed_identifier_or_reference','fieldValue'} for k in path) or 'observed' in path[1:]
        return {k:semantic(v,roots,path+(k,)) for k,v in value.items()
                if not (k in VOLATILE_KEYS and audit_envelope and not source_payload)}
    if isinstance(value,list):return [semantic(v,roots,path+('*',)) for v in value]
    if isinstance(value,str):
        if path and path[-1] in PATH_METADATA:
            for root in sorted(roots,key=len,reverse=True):
                value=value.replace(root,'<EXECUTION_ROOT>').replace(root.replace('\\','/'),'<EXECUTION_ROOT>')
        return value
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
