"""Check facts in authored fixtures independently of the frozen audit engines.

This checks small focused witnesses, not arbitrary feeds or engine accuracy.
"""
from collections import Counter
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
from lxml import etree
from tools.audit_corpus_v1 import ROOT, SCHEMA, read, write, sha
from tools.audit_reference_definitions_v1 import DEFINITIONS


def seconds(value):
    h,m,s=map(int,value.split(":"))
    if h<0 or not 0<=m<60 or not 0<=s<60: raise ValueError("Invalid witness time")
    return 3600*h+60*m+s


def feed(path):
    tables={}
    with zipfile.ZipFile(path) as archive:
        if len(archive.namelist())>32 or len(set(archive.namelist()))!=len(archive.namelist()):raise ValueError("Fixture inventory unsafe")
        for info in archive.infolist():
            if Path(info.filename).name!=info.filename or info.file_size>1_000_000:raise ValueError("Fixture member unsafe")
            data=archive.read(info.filename).decode("utf-8")
            reader=csv.DictReader(io.StringIO(data,newline=""),strict=True)
            tables[info.filename]={"fields":reader.fieldnames,"rows":list(reader)}
    return tables


def gtfs_state(case,path,family):
    try:data=feed(path)
    except csv.Error:
        if family=="csv":return "VIOLATED"
        raise
    def rows(name):return data.get(name,{"rows":[]})["rows"]
    def fields(name):return data.get(name,{"fields":[]})["fields"]
    def ids(name,field):return {r[field] for r in rows(name)}
    def yes(condition):return "SATISFIED" if condition else "VIOLATED"
    if family=="csv":return "SATISFIED"
    if family=="color":return yes(all(r["route_text_color"]=="" or re.fullmatch(r"[a-fA-F0-9]{6}",r["route_text_color"]) for r in rows("routes.txt")))
    if family=="catalog":return "REVIEW_REQUIRED" if "operator_extension.txt" in data else "SATISFIED"
    if family=="calendar_presence":return yes("calendar.txt" in data or "calendar_dates.txt" in data)
    if family=="networks":return yes(not("networks.txt" in data and "network_id" in fields("routes.txt")))
    if family=="header":
        if case["context"].get("agency_cardinality_evidence_available") is False:return "UNKNOWN"
        return yes(len(rows("agency.txt"))==1 or "agency_id" in fields("routes.txt"))
    if family=="translation":
        if "translations.txt" not in data:return "NOT_APPLICABLE"
        return yes(all(r["record_id"] in ids("stops.txt","stop_id") for r in rows("translations.txt")))
    if family=="service_ref":return yes(all(r["service_id"] in ids("calendar.txt","service_id")|ids("calendar_dates.txt","service_id") for r in rows("trips.txt")))
    if family=="unique":return yes(len(rows("stops.txt"))==len(ids("stops.txt","stop_id")))
    if family=="parent":
        stations={r["stop_id"] for r in rows("stops.txt") if r["location_type"]=="1"}
        return yes(all(not r["parent_station"] or r["parent_station"] in stations for r in rows("stops.txt")))
    if family in {"calendar_range","feed_range"}:
        f="calendar.txt" if family=="calendar_range" else "feed_info.txt";start="start_date" if family=="calendar_range" else "feed_start_date";end="end_date" if family=="calendar_range" else "feed_end_date"
        return yes(all(datetime.strptime(r[start],"%Y%m%d")<=datetime.strptime(r[end],"%Y%m%d") for r in rows(f)))
    if family=="frequency_range":return yes(all(seconds(r["start_time"])<seconds(r["end_time"]) for r in rows("frequencies.txt")))
    if family=="frequency_end":
        last=seconds(case["context"]["last_desired_departure"])
        return yes(all(last<seconds(r["end_time"])<last+int(r["headway_secs"]) for r in rows("frequencies.txt")))
    if family=="service_dates":return "SATISFIED" if any(r["exception_type"]=="1" for r in rows("calendar_dates.txt")) else "REVIEW_REQUIRED"
    if family in {"window_review","time_review"}:
        if family=="window_review" and "start_pickup_drop_off_window" not in fields("stop_times.txt"):return "NOT_APPLICABLE"
        if case["context"].get("approved_criterion_available") is not False:raise ValueError("Review witness has undeclared authority")
        return "UNKNOWN"
    if family in {"coordinate","stop_coordinate"}:
        f="shapes.txt" if family=="coordinate" else "stops.txt";lat="shape_pt_lat" if family=="coordinate" else "stop_lat";lon="shape_pt_lon" if family=="coordinate" else "stop_lon"
        return yes(all(-90<=float(r[lat])<=90 and -180<=float(r[lon])<=180 for r in rows(f)))
    if family=="distance":
        if "shape_dist_traveled" not in fields("shapes.txt"):return "NOT_APPLICABLE"
        values=[float(r["shape_dist_traveled"]) for r in rows("shapes.txt")]
        return yes(all(a<b for a,b in zip(values,values[1:])))
    if family in {"stop_sequence","shape_sequence"}:
        f="stop_times.txt" if family=="stop_sequence" else "shapes.txt";field="stop_sequence" if family=="stop_sequence" else "shape_pt_sequence"
        values=[int(r[field]) for r in rows(f)];return yes(all(a<b for a,b in zip(values,values[1:])))
    if family.startswith("recommend_"):
        field={"recommend_start":"feed_start_date","recommend_end":"feed_end_date","recommend_version":"feed_version"}[family]
        return "SATISFIED" if field in fields("feed_info.txt") else "RECOMMENDATION_UNMET"
    if family=="stop_ref":
        allowed={r["stop_id"] for r in rows("stops.txt") if r["location_type"]=="0"}
        return yes(all(r["stop_id"] in allowed for r in rows("stop_times.txt")))
    if family=="shape_ref":return yes(all(not r["shape_id"] or r["shape_id"] in ids("shapes.txt","shape_id") for r in rows("trips.txt")))
    if family=="route_ref":return yes(all(r["route_id"] in ids("routes.txt","route_id") for r in rows("trips.txt")))
    if family=="agency_presence":return yes("agency.txt" in data)
    raise ValueError("Missing focused witness checker")


def schema_identity():
    manifest=read(ROOT/SCHEMA);root=((ROOT/SCHEMA).parent/manifest["root_schema"]).resolve().parent.parent
    if root!=Path("P:/TransitDataLab/02_Data/External/netex-schema-v2.0.0").resolve():raise ValueError("Unexpected pinned schema root")
    count=0
    for dependency in manifest["dependencies"]:
        path=(root/dependency["path"]).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes().replace(b"\r\n",b"\n")).hexdigest()!=dependency["sha256"]:
            raise ValueError("Pinned schema dependency changed")
        count+=1
    parser=etree.XMLParser(resolve_entities=False,no_network=True,load_dtd=False)
    schema=etree.XMLSchema(etree.parse(str(root/manifest["root_schema"]),parser))
    return schema,{"dependencies_verified":count,"commit":manifest["commit"],"root_schema_sha256":manifest["root_schema_sha256"],"normalization":"LF for pinned schema hashes"}


def netex_state(case,path,schema):
    rule=case["criterion_id"];data=path.read_bytes()
    if rule=="TDL-CAND-NETEX-REFERENCE-CONTEXT":
        obj=json.loads(data)
        if not obj["local_scope_available"]:return "UNKNOWN"
        return "SATISFIED" if obj["object"]==obj["reference"] else "REVIEW_REQUIRED"
    unsafe=b"<!DOCTYPE" in data or b"<!ENTITY" in data
    try:tree=etree.fromstring(data,etree.XMLParser(resolve_entities=False,no_network=True,load_dtd=False)) if not unsafe else None
    except etree.XMLSyntaxError:tree=None
    if rule=="NETEX-XML-001":return "SATISFIED" if tree is not None else "VIOLATED"
    if tree is None:return "UNKNOWN"
    if rule=="NETEX-XSD-001":return "SATISFIED" if schema.validate(tree) else "VIOLATED"
    if rule=="NETEX-PROFILE-001":return "REVIEW_REQUIRED"
    if rule=="NETEX-IDENTITY-001":
        elements=tree.xpath("//*[@id]");counter=Counter(e.attrib["id"] for e in elements)
        if case["variant"]=="boundary":
            versions={e.attrib.get("version") for e in elements}
            if len(versions)<2:raise ValueError("Identity boundary must actually contain differing versions")
        return "REVIEW_REQUIRED" if any(v>1 for v in counter.values()) else "SATISFIED"
    raise ValueError("Missing NeTEx witness checker")


def verify_facts(bank):
    root=Path(bank["fixture_root"]);families={d[0]:d[4] for d in DEFINITIONS};schema,identity=schema_identity();results=[]
    for case in bank["cases"]:
        path=root/case["fixture"]
        if sha(path)!=case["sha256"]:raise ValueError("Fixture changed before fact check")
        if case["format"]=="GTFS_SCHEDULE":
            family=families.get(case["criterion_id"],"header" if case["criterion_id"]=="TDL-CAND-GTFS-CONDITION-RESOLUTION" else None)
            observed=gtfs_state(case,path,family)
        else:observed=netex_state(case,path,schema)
        if observed!=case["expected"]["criterion_state"]:raise ValueError("Expectation does not match authored facts: "+case["case_id"])
        results.append({"case_id":case["case_id"],"focused_fact_check":"PASS","criterion_state":observed})
    return {"contract":"TDL_REFERENCE_FACT_CHECK/1","result":"PASS","cases":len(results),"schema_identity":identity,
            "checks":results,"audit_engine_executed":False,"accuracy_measured":False,"independent_human_review":False}


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument("--bank",type=Path,required=True);parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args();result=verify_facts(read(args.bank));write(args.receipt,result)
    print(json.dumps({k:v for k,v in result.items() if k!="checks"},ensure_ascii=False))
