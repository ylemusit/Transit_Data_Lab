"""Cross-row trip ordering and frequency interval checks."""
from __future__ import annotations
import csv
from .phase_runtime_contract import build_phase_registry

REVISION="2026-04-27"
RULES=("GTFS-G06-STOP-SEQUENCE","TDL-G06-TRIP-TIME-ORDER-REVIEW","GTFS-G06-FREQUENCY-OPERATIONS")
RULE_SPECS=((RULES[0],"SEQUENCE","stop sequence",("stop_times.txt",)),
            (RULES[1],"QUALITY","unconfirmed trip time ordering",("stop_times.txt",),"TDL_QUALITY","INFO","RECOMMENDED"),
            (RULES[2],"DATA_CONSISTENCY","frequency operations",("frequencies.txt",)))

def _read(ctx,name):
    path=ctx.tables.get(name.removesuffix(".txt"))
    if path is None:return None
    enc=getattr(ctx.dataset,"files",{}).get(name,{}).get("encoding") or "utf-8-sig"
    with path.open(encoding=enc,newline="") as f:
        reader=csv.DictReader(f,strict=True)
        if not reader.fieldnames:raise ValueError(f"missing header: {name}")
        return list(reader.fieldnames),list(reader)

def _seconds(text):
    h,m,s=map(int,text.split(":"))
    if h<0 or not 0<=m<60 or not 0<=s<60:raise ValueError(text)
    return h*3600+m*60+s

def _g03_uncertain(g03,name):
    if g03 is None:return False
    comp=g03.get("csv_structure")
    inspected=next((x for x in comp.get("inspected",[]) if x.get("file")==name),None) if isinstance(comp,dict) else None
    if inspected is None or inspected.get("status")!="PASS":return True
    if any(x.get("file")==name for x in comp.get("findings",[])):return True
    types=g03.get("field_types") or {}
    return any(x.get("file")==name for key in ("findings","not_evaluable") for x in types.get(key,[]))

def evaluate_g06(ctx,g03_result=None,g04_result=None,g05_result=None):
    registry=build_phase_registry(RULE_SPECS,evaluate_g06,"g06_operations")
    rule_versions=registry.identity_map()["rule_versions"]
    result={"status":"NOT_APPLICABLE","rules":[],"findings":[],"rule_versions":rule_versions}
    specs=tuple((spec[0],spec[1]) for spec in RULE_SPECS)
    states={rid:[] for rid,_ in specs}; finds={rid:[] for rid,_ in specs}
    frequency_interval_review=False
    def add(rid,state,file,row,fields,observed,reason):
        states[rid].append(state)
        if state=="FAIL_TECHNICAL":
            ref="https://gtfs.org/documentation/schedule/reference/#frequenciestxt" if file=="frequencies.txt" else "https://gtfs.org/documentation/schedule/reference/#stop_timestxt"
            finds[rid].append({"rule_id":rid,"source_file":file,"record_locator":f"data_row:{row}","source_fields":fields,"observed":observed,"technical_reason":reason,"specification_reference":ref})
    try:
        if g03_result and g03_result.get("status")=="INSPECTION_ERROR":return {"status":"INSPECTION_ERROR","rules":[{"rule_id":r,"status":"INSPECTION_ERROR","findings":[],"evaluator_executed":True} for r,_ in specs],"findings":[],"rule_versions":rule_versions}
        st=_read(ctx,"stop_times.txt")
        if st:
            if _g03_uncertain(g03_result,"stop_times.txt"):
                add(RULES[0],"NOT_EVALUABLE","stop_times.txt",1,[],None,"G03 structural or field coverage is incomplete")
                add(RULES[1],"NOT_EVALUABLE","stop_times.txt",1,[],None,"G03 structural or field coverage is incomplete")
                st=None
        if st:
            heads,rows=st
            if not {"trip_id","stop_sequence"}.issubset(heads):add(RULES[0],"NOT_EVALUABLE","stop_times.txt",1,["trip_id","stop_sequence"],None,"required identity fields unavailable")
            else:
                groups={}
                for i,row in enumerate(rows,1):
                    if not row.get("trip_id"):
                        add(RULES[0],"NOT_EVALUABLE","stop_times.txt",i,["trip_id"],row.get("trip_id"),"trip grouping is unresolved for an empty trip_id")
                        continue
                    try: seq=int(row.get("stop_sequence",""))
                    except ValueError: add(RULES[0],"NOT_EVALUABLE","stop_times.txt",i,["stop_sequence"],row.get("stop_sequence"),"sequence is not interpretable");continue
                    if seq<0:
                        add(RULES[0],"FAIL_TECHNICAL","stop_times.txt",i,["stop_sequence"],seq,"stop_sequence must be non-negative")
                        continue
                    add(RULES[0],"PASS","stop_times.txt",i,["stop_sequence"],seq,"non-negative stop sequence; uniqueness is evaluated by G04")
                    groups.setdefault(row.get("trip_id",""),[]).append((i,seq,row))
                for trip,items in groups.items():
                    if len(items)<2:continue
                if {"arrival_time","departure_time"}.issubset(heads) and any(row.get("arrival_time") or row.get("departure_time") for row in rows):
                    add(RULES[1],"NOT_EVALUABLE","stop_times.txt",1,["arrival_time","departure_time"],None,"the fixed GTFS reference does not state a MUST-level monotonicity relation; retained as a TDL review item")
        freq=_read(ctx,"frequencies.txt")
        if freq:
            temporal_rule=next((r for r in (g05_result or {}).get("rules",[]) if r.get("rule_id")=="GTFS-G05-FREQUENCY-TIME-RANGE"),None)
            if temporal_rule is None or temporal_rule.get("status") in {"NOT_EVALUABLE","INSPECTION_ERROR"}:
                add(RULES[2],"NOT_EVALUABLE","frequencies.txt",1,[],None,"G05 time interpretation is incomplete")
                freq=None
            elif _g03_uncertain(g03_result,"frequencies.txt"):
                add(RULES[2],"NOT_EVALUABLE","frequencies.txt",1,[],None,"G03 structural or field coverage is incomplete")
                freq=None
        if freq:
            heads,rows=freq
            if not {"trip_id","start_time","end_time","headway_secs"}.issubset(heads):add(RULES[2],"NOT_EVALUABLE","frequencies.txt",1,[],None,"frequency fields unavailable")
            else:
                groups={}
                g05_bad_rows=set()
                for finding in temporal_rule.get("findings",[]):
                    locator=str(finding.get("record_locator",""))
                    if finding.get("source_file")=="frequencies.txt" and locator.startswith("data_row:") and locator[9:].isdigit():
                        g05_bad_rows.add(int(locator[9:]))
                for i,row in enumerate(rows,1):
                    trip=row.get("trip_id","")
                    if not trip:
                        add(RULES[2],"NOT_EVALUABLE","frequencies.txt",i,["trip_id"],trip,"frequency grouping is unresolved for an empty trip_id")
                        continue
                    if i in g05_bad_rows:
                        add(RULES[2],"NOT_EVALUABLE","frequencies.txt",i,["start_time","end_time"],None,"G05 already reports this row's temporal range; G06 does not duplicate it")
                        try:head=int(row.get("headway_secs",""))
                        except ValueError:continue
                        if head<=0:add(RULES[2],"FAIL_TECHNICAL","frequencies.txt",i,["headway_secs"],head,"headway_secs must be positive")
                        continue
                    try:
                        start,end=_seconds(row.get("start_time","")),_seconds(row.get("end_time",""))
                        head=int(row.get("headway_secs",""))
                    except ValueError:add(RULES[2],"NOT_EVALUABLE","frequencies.txt",i,["start_time","end_time","headway_secs"],None,"temporal value not interpretable");continue
                    interval_valid=True
                    if head<=0:
                        add(RULES[2],"FAIL_TECHNICAL","frequencies.txt",i,["headway_secs"],head,"headway_secs must be positive")
                        interval_valid=False
                    exact=row.get("exact_times") or "0"
                    if exact not in {"0","1"}:
                        add(RULES[2],"NOT_EVALUABLE","frequencies.txt",i,["exact_times"],exact,"exact_times is not interpretable")
                    elif exact=="1" and head>0:
                        if start>=end:
                            add(RULES[2],"FAIL_TECHNICAL","frequencies.txt",i,["start_time","end_time","headway_secs","exact_times"],{"start":start,"end":end,"headway":head},"exact_times=1 end_time must be greater than the last desired trip start")
                            interval_valid=False
                        else:
                            last=start+((end-start-1)//head)*head
                            valid=last<end<last+head
                            if not valid:add(RULES[2],"FAIL_TECHNICAL","frequencies.txt",i,["start_time","end_time","headway_secs","exact_times"],{"start":start,"end":end,"headway":head,"last_trip_start":last},"exact_times=1 end_time must fall after the last scheduled trip start and before that start plus one headway")
                            else:add(RULES[2],"PASS","frequencies.txt",i,["start_time","end_time","headway_secs","exact_times"],{"start":start,"end":end,"headway":head,"last_trip_start":last},"exact_times=1 end_time bounds the last desired trip")
                    if start==end and exact!="1":
                        add(RULES[2],"NOT_EVALUABLE","frequencies.txt",i,["start_time","end_time"],{"start":start,"end":end},"a positive frequency interval is required by the candidate scope; the pinned reference does not state an explicit MUST for this case")
                        frequency_interval_review=True
                        interval_valid=False
                    if interval_valid:groups.setdefault(trip,[]).append((i,start,end))
                for trip,items in groups.items():
                    ordered=sorted(items,key=lambda x:x[1])
                    for prev,cur in zip(ordered,ordered[1:]):
                        if cur[1]<prev[2]:add(RULES[2],"FAIL_TECHNICAL","frequencies.txt",cur[0],["trip_id","start_time","end_time"],{"trip_id":trip,"previous_end":prev[2],"current_start":cur[1]},"frequency intervals for a trip must not overlap")
                        else:add(RULES[2],"PASS","frequencies.txt",cur[0],["trip_id","start_time","end_time"],{"trip_id":trip,"previous_end":prev[2],"current_start":cur[1]},"frequency intervals do not overlap")
        for rid,category in specs:
            ss=states[rid]
            status="FAIL_TECHNICAL" if "FAIL_TECHNICAL" in ss else "NOT_EVALUABLE" if "NOT_EVALUABLE" in ss else "PASS" if "PASS" in ss else "NOT_APPLICABLE"
            result["rules"].append({"rule_id":rid,"semantic_version":"1.0.0","category":category,"status":status,"evaluator_executed":True,"coverage":{"evaluated":ss.count("PASS")+ss.count("FAIL_TECHNICAL"),"not_evaluable":ss.count("NOT_EVALUABLE"),"not_applicable":int(not ss),"state":"PARTIAL" if "NOT_EVALUABLE" in ss else "FULL"},"specification_reference":f"GTFS Schedule Reference {REVISION}","findings":finds[rid]})
        result["findings"]=[f for arr in finds.values() for f in arr]
        if states[RULES[1]]:
            result["deferred_rule_reviews"]=[{"rule_id":RULES[1],"authority":"TDL_QUALITY","reason":"The pinned specification defines times per stop but does not state an explicit cross-stop monotonicity MUST; do not classify an operator finding without a reviewed authority decision."}]
        if frequency_interval_review:
            result.setdefault("deferred_rule_reviews",[]).append({"rule_id":RULES[2],"authority":"TDL_QUALITY","reason":"Zero-length frequency intervals are not treated as valid; the pinned reference does not establish a separate MUST-level start-before-end comparison when exact_times is not 1."})
        statuses=[x["status"] for x in result["rules"]]
        result["status"]="FAIL_TECHNICAL" if "FAIL_TECHNICAL" in statuses else "NOT_EVALUABLE" if "NOT_EVALUABLE" in statuses else "PASS" if "PASS" in statuses else "NOT_APPLICABLE"
        return result
    except Exception as exc:return {"status":"INSPECTION_ERROR","rules":[{"rule_id":r,"status":"INSPECTION_ERROR","findings":[],"evaluator_executed":True} for r,_ in specs],"findings":[],"rule_versions":rule_versions,"error":f"{type(exc).__name__}: {exc}"}
