"""Shape sequence, WGS84 coordinate bounds, and declared distance progression."""
from __future__ import annotations
import csv
import math
from .phase_runtime_contract import build_phase_registry

REVISION="2026-04-27"
RULES=("GTFS-G07-SHAPE-SEQUENCE","GTFS-G07-COORDINATE-BOUNDS","GTFS-G07-DISTANCE-PROGRESSION")
RULE_SPECS=((RULES[0],"SPATIAL","shape point sequence",("shapes.txt",)),
            (RULES[1],"SPATIAL","WGS84 coordinate bounds",("shapes.txt",)),
            (RULES[2],"SPATIAL","shape distance progression",("shapes.txt",)))

def _g03_uncertain(g03):
    if g03 is None:return False
    comp=g03.get("csv_structure")
    inspected=next((x for x in comp.get("inspected",[]) if x.get("file")=="shapes.txt"),None) if isinstance(comp,dict) else None
    if inspected is None or inspected.get("status")!="PASS":return True
    if any(x.get("file")=="shapes.txt" for x in comp.get("findings",[])):return True
    types=g03.get("field_types") or {}
    return any(x.get("file")=="shapes.txt" for key in ("findings","not_evaluable") for x in types.get(key,[]))

def evaluate_g07(ctx,g03_result=None,g04_result=None):
    registry=build_phase_registry(RULE_SPECS,evaluate_g07,"g07_spatial")
    rule_versions=registry.identity_map()["rule_versions"]
    states={r:[] for r in RULES};findings={r:[] for r in RULES}
    def add(rid,state,row,fields,observed,reason):
        states[rid].append(state)
        if state=="FAIL_TECHNICAL":findings[rid].append({"rule_id":rid,"source_file":"shapes.txt","record_locator":f"data_row:{row}","source_fields":fields,"observed":observed,"technical_reason":reason,"specification_reference":"https://gtfs.org/documentation/schedule/reference/#shapestxt"})
    try:
        if g03_result and g03_result.get("status")=="INSPECTION_ERROR":return {"status":"INSPECTION_ERROR","rules":[{"rule_id":r,"status":"INSPECTION_ERROR","findings":[],"evaluator_executed":True} for r in RULES],"findings":[],"rule_versions":rule_versions}
        path=ctx.tables.get("shapes")
        if path is None:
            rules=[{"rule_id":r,"semantic_version":"1.0.0","category":"SPATIAL","status":"NOT_APPLICABLE","evaluator_executed":True,"coverage":{"evaluated":0,"not_evaluable":0,"not_applicable":1,"state":"FEATURE_NOT_PRESENT"},"specification_reference":f"GTFS Schedule Reference {REVISION}","findings":[]} for r in RULES]
            return {"status":"NOT_APPLICABLE","rules":rules,"findings":[],"rule_versions":rule_versions}
        if _g03_uncertain(g03_result):
            rules=[{"rule_id":r,"semantic_version":"1.0.0","category":"SPATIAL","status":"NOT_EVALUABLE","evaluator_executed":True,"coverage":{"evaluated":0,"not_evaluable":1,"not_applicable":0,"state":"PARTIAL"},"specification_reference":f"GTFS Schedule Reference {REVISION}","findings":[]} for r in RULES]
            return {"status":"NOT_EVALUABLE","rules":rules,"findings":[],"rule_versions":rule_versions}
        enc=getattr(ctx.dataset,"files",{}).get("shapes.txt",{}).get("encoding") or "utf-8-sig"
        with path.open(encoding=enc,newline="") as f:
            reader=csv.DictReader(f,strict=True)
            if not reader.fieldnames:raise ValueError("missing shapes header")
            heads=list(reader.fieldnames);rows=list(reader)
        required={"shape_id","shape_pt_sequence","shape_pt_lat","shape_pt_lon"}
        key_rule=next((r for r in (g04_result or {}).get("rules",[]) if r.get("rule_id","").endswith("PRIMARY-KEY-UNIQUENESS")),None)
        duplicate_keys=set()
        if key_rule:
            for finding in key_rule.get("findings",[]):
                if finding.get("source_file")=="shapes.txt":
                    observed=finding.get("observed_identifier_or_reference")
                    if isinstance(observed,list) and len(observed)==2:
                        duplicate_keys.add((str(observed[0]),str(observed[1])))
        if not required.issubset(heads):
            for r in RULES:add(r,"NOT_EVALUABLE",1,sorted(required-set(heads)),None,"required shape fields unavailable")
        else:
            groups={}
            for i,row in enumerate(rows,1):
                shape=row.get("shape_id","")
                if not shape:
                    add(RULES[0],"NOT_EVALUABLE",i,["shape_id"],shape,"shape grouping is unresolved for an empty shape_id")
                    add(RULES[2],"NOT_EVALUABLE",i,["shape_id","shape_dist_traveled"],None,"distance ordering is unresolved for an empty shape_id")
                    shape=""
                try:seq=int(row.get("shape_pt_sequence",""))
                except ValueError:add(RULES[0],"NOT_EVALUABLE",i,["shape_pt_sequence"],row.get("shape_pt_sequence"),"sequence is not interpretable");seq=None
                if seq is not None:
                    if seq<0:add(RULES[0],"FAIL_TECHNICAL",i,["shape_pt_sequence"],seq,"shape_pt_sequence must be non-negative")
                    else:add(RULES[0],"PASS",i,["shape_pt_sequence"],seq,"non-negative sequence; uniqueness is evaluated by G04")
                    if seq>=0 and shape and (shape,row.get("shape_pt_sequence") or "") in duplicate_keys:
                        add(RULES[2],"NOT_EVALUABLE",i,["shape_id","shape_pt_sequence","shape_dist_traveled"],None,"duplicate identity prevents unambiguous distance ordering")
                    elif seq>=0 and shape:
                        groups.setdefault(shape,[]).append((i,seq,row))
                try:
                    lat,lon=float(row.get("shape_pt_lat","")),float(row.get("shape_pt_lon",""))
                    ok=math.isfinite(lat) and math.isfinite(lon) and -90<=lat<=90 and -180<=lon<=180
                    add(RULES[1],"PASS" if ok else "FAIL_TECHNICAL",i,["shape_pt_lat","shape_pt_lon"],[lat,lon],"WGS84 latitude/longitude outside inclusive bounds")
                except ValueError:add(RULES[1],"NOT_EVALUABLE",i,["shape_pt_lat","shape_pt_lon"],None,"coordinate is not interpretable")
                if "shape_dist_traveled" in heads and (row.get("shape_dist_traveled") or ""):
                    try:
                        distance=float(row["shape_dist_traveled"])
                        if not math.isfinite(distance) or distance<0:add(RULES[2],"FAIL_TECHNICAL",i,["shape_dist_traveled"],distance,"shape_dist_traveled must be a finite non-negative value")
                    except ValueError:add(RULES[2],"NOT_EVALUABLE",i,["shape_dist_traveled"],row.get("shape_dist_traveled"),"distance is not interpretable")
            for shape,items in groups.items():
                items.sort(key=lambda x:x[1])
                if "shape_dist_traveled" in heads:
                    prior=None
                    for i,seq,row in items:
                        raw=row.get("shape_dist_traveled") or ""
                        if not raw:continue
                        try:value=float(raw)
                        except ValueError:add(RULES[2],"NOT_EVALUABLE",i,["shape_dist_traveled"],raw,"distance is not interpretable");continue
                        if not math.isfinite(value):continue
                        if prior is not None:
                            add(RULES[2],"PASS" if value>prior[1] else "FAIL_TECHNICAL",i,["shape_id","shape_pt_sequence","shape_dist_traveled"],{"shape_id":shape,"previous":prior[1],"current":value},"declared distance must increase as shape sequence increases")
                        prior=(i,value)
            if "shape_dist_traveled" not in heads:
                add(RULES[2],"NOT_APPLICABLE",1,["shape_dist_traveled"],None,"optional distance field absent")
        rules=[]
        for rid in RULES:
            ss=states[rid];status="FAIL_TECHNICAL" if "FAIL_TECHNICAL" in ss else "NOT_EVALUABLE" if "NOT_EVALUABLE" in ss else "PASS" if "PASS" in ss else "NOT_APPLICABLE"
            rules.append({"rule_id":rid,"semantic_version":"1.0.0","category":"SPATIAL","status":status,"evaluator_executed":True,"coverage":{"evaluated":ss.count("PASS")+ss.count("FAIL_TECHNICAL"),"not_evaluable":ss.count("NOT_EVALUABLE"),"not_applicable":ss.count("NOT_APPLICABLE"),"state":"PARTIAL" if "NOT_EVALUABLE" in ss else "FEATURE_PRESENT_FULLY_AUDITED"},"specification_reference":f"GTFS Schedule Reference {REVISION}","findings":findings[rid]})
        allfind=[f for group in findings.values() for f in group]; ss=[r["status"] for r in rules]
        status="FAIL_TECHNICAL" if "FAIL_TECHNICAL" in ss else "NOT_EVALUABLE" if "NOT_EVALUABLE" in ss else "PASS" if "PASS" in ss else "NOT_APPLICABLE"
        return {"status":status,"rules":rules,"findings":allfind,"rule_versions":rule_versions}
    except Exception as exc:return {"status":"INSPECTION_ERROR","rules":[{"rule_id":r,"status":"INSPECTION_ERROR","findings":[],"evaluator_executed":True} for r in RULES],"findings":[],"rule_versions":rule_versions,"error":f"{type(exc).__name__}: {exc}"}
