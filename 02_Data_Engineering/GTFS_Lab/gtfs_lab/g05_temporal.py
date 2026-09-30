"""Conservative temporal comparisons for GTFS Schedule revision 2026-04-27."""
from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path
from .phase_runtime_contract import build_phase_registry

REVISION = "2026-04-27"
RULES = ("GTFS-G05-CALENDAR-RANGE", "GTFS-G05-FEED-RANGE", "GTFS-G05-FREQUENCY-TIME-RANGE", "TDL-G05-PICKUP-WINDOW-ORDER-REVIEW", "GTFS-G05-SERVICE-DATE-SET")
RULE_SPECS = (
    (RULES[0],"TEMPORAL","calendar date range",("calendar.txt",)),
    (RULES[1],"TEMPORAL","feed date range",("feed_info.txt",)),
    (RULES[2],"TEMPORAL","frequency time range",("frequencies.txt",)),
    (RULES[3],"QUALITY","unconfirmed pickup/drop-off window ordering",("stop_times.txt",),"TDL_QUALITY","INFO","RECOMMENDED"),
    (RULES[4],"TEMPORAL","service date set",("calendar.txt","calendar_dates.txt")),
)

def _read(ctx, name):
    path = ctx.tables.get(name.removesuffix(".txt"))
    if path is None: return None
    encoding = getattr(ctx.dataset, "files", {}).get(name, {}).get("encoding") or "utf-8-sig"
    with path.open(encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, strict=True)
        if not reader.fieldnames: raise ValueError(f"missing header: {name}")
        return list(reader.fieldnames), list(reader)

def _date(value): return datetime.strptime(value, "%Y%m%d").date()
def _time(value):
    parts = value.split(":")
    if len(parts) != 3: raise ValueError(value)
    h, m, s = map(int, parts)
    if h < 0 or not 0 <= m < 60 or not 0 <= s < 60: raise ValueError(value)
    return h * 3600 + m * 60 + s

def _g03_uncertain(g03, file_name):
    if g03 is None: return False
    comp=g03.get("csv_structure")
    inspected=next((x for x in comp.get("inspected",[]) if x.get("file")==file_name),None) if isinstance(comp,dict) else None
    if inspected is None or inspected.get("status")!="PASS": return True
    if any(x.get("file")==file_name for x in comp.get("findings",[])): return True
    types=g03.get("field_types") or {}
    return any(x.get("file")==file_name for key in ("findings","not_evaluable") for x in types.get(key,[]))

def evaluate_g05(ctx, g03_result=None, g04_result=None):
    registry=build_phase_registry(RULE_SPECS,evaluate_g05,"g05_temporal")
    rule_versions=registry.identity_map()["rule_versions"]
    rules = {rid: {"rule_id": rid, "semantic_version": "1.0.0", "status": "NOT_APPLICABLE",
        "coverage": {"evaluated": 0, "not_evaluable": 0, "not_applicable": 0, "state": "FULL"},
        "specification_reference": f"GTFS Schedule Reference {REVISION}", "findings": []} for rid in RULES}
    findings=[]
    def mark(rid, state, file=None, row=None, fields=None, observed=None, reason=None):
        r=rules[rid]
        old=r["status"]
        if state=="FAIL_TECHNICAL" or old not in {"FAIL_TECHNICAL","INSPECTION_ERROR"} and (state=="NOT_EVALUABLE" or old=="NOT_APPLICABLE"):
            r["status"]=state
        key={"PASS":"evaluated", "FAIL_TECHNICAL":"evaluated", "NOT_EVALUABLE":"not_evaluable", "NOT_APPLICABLE":"not_applicable"}.get(state,"not_evaluable")
        r["coverage"][key]+=1
        if state=="NOT_EVALUABLE": r["coverage"]["state"]="PARTIAL"
        if state=="FAIL_TECHNICAL":
            ref={RULES[0]:"https://gtfs.org/documentation/schedule/reference/#calendartxt",
                RULES[1]:"https://gtfs.org/documentation/schedule/reference/#feed_infotxt",
                RULES[2]:"https://gtfs.org/documentation/schedule/reference/#frequenciestxt",
                RULES[3]:"https://gtfs.org/documentation/schedule/reference/#stop_timestxt",
                RULES[4]:"https://gtfs.org/documentation/schedule/reference/#calendar_datestxt"}[rid]
            f={"rule_id":rid,"source_file":file,"record_locator":f"data_row:{row}","source_fields":fields,"observed":observed,"technical_reason":reason,"specification_reference":ref};r["findings"].append(f);findings.append(f)
    try:
        if g03_result and g03_result.get("status")=="INSPECTION_ERROR":
            for rid,r in rules.items(): r["status"]="INSPECTION_ERROR";r["category"]="QUALITY" if rid==RULES[3] else "TEMPORAL";r["evaluator_executed"]=True
            return {"status":"INSPECTION_ERROR","rules":list(rules.values()),"findings":[],"rule_versions":rule_versions}
        for name, rid, start, end in (("calendar.txt",RULES[0],"start_date","end_date"),("feed_info.txt",RULES[1],"feed_start_date","feed_end_date")):
            data=_read(ctx,name)
            if data is None: continue
            if _g03_uncertain(g03_result,name): mark(rid,"NOT_EVALUABLE");continue
            heads, rows=data
            if start not in heads or end not in heads: mark(rid,"NOT_EVALUABLE");continue
            for i,row in enumerate(rows,1):
                a,b=row.get(start) or "",row.get(end) or ""
                if not a or not b: mark(rid,"NOT_EVALUABLE");continue
                try: ok=_date(a)<=_date(b)
                except ValueError: mark(rid,"NOT_EVALUABLE");continue
                mark(rid,"PASS" if ok else "FAIL_TECHNICAL",name,i,[start,end],[a,b],"date range start must not follow end")
        # Intrarecord windows only; trip grouping and stop chronology belong to G06.
        for name, fields, rule in (("frequencies.txt",("start_time","end_time"),RULES[2]),("stop_times.txt",("start_pickup_drop_off_window","end_pickup_drop_off_window"),RULES[3])):
            data=_read(ctx,name)
            if data is None: continue
            if _g03_uncertain(g03_result,name): mark(rule,"NOT_EVALUABLE");continue
            heads,rows=data
            if not set(fields).issubset(heads): continue
            for i,row in enumerate(rows,1):
                a,b=(row.get(x) or "" for x in fields)
                if not a and not b: continue
                if not a or not b: mark(rule,"NOT_EVALUABLE");continue
                try: ok=_time(a)<=_time(b)
                except ValueError: mark(rule,"NOT_EVALUABLE");continue
                if rule==RULES[3]:
                    mark(rule,"NOT_EVALUABLE",name,i,list(fields),[a,b],"ordering of pickup/drop-off windows remains a TDL review item; the pinned reference does not define this comparison as a MUST")
                else:
                    mark(rule,"PASS" if ok else "FAIL_TECHNICAL",name,i,list(fields),[a,b],"temporal interval start must not follow end")
        service_dates={}
        calendar=_read(ctx,"calendar.txt")
        dates=_read(ctx,"calendar_dates.txt")
        if calendar is None and dates is None:
            mark(RULES[4],"NOT_APPLICABLE")
        else:
            uncertain=(calendar is not None and _g03_uncertain(g03_result,"calendar.txt")) or (dates is not None and _g03_uncertain(g03_result,"calendar_dates.txt"))
            g04_domain=next((r for r in (g04_result or {}).get("rules",[]) if r.get("rule_id","" ).endswith("IDENTITY-DOMAIN")),None)
            if g04_result and g04_domain and g04_domain.get("status") not in {"PASS","NOT_APPLICABLE"}: uncertain=True
            g04_keys=next((r for r in (g04_result or {}).get("rules",[]) if r.get("rule_id","" ).endswith("PRIMARY-KEY-UNIQUENESS")),None)
            if g04_result and g04_keys:
                service_key_findings=[f for f in g04_keys.get("findings",[]) if f.get("source_file") in {"calendar.txt","calendar_dates.txt"}]
                if service_key_findings or g04_keys.get("status")=="NOT_EVALUABLE":uncertain=True
            if uncertain:
                mark(RULES[4],"NOT_EVALUABLE")
            else:
                weekdays=("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
                if calendar is not None:
                    heads,rows=calendar
                    if not {"service_id","start_date","end_date",*weekdays}.issubset(heads):
                        mark(RULES[4],"NOT_EVALUABLE")
                    else:
                        for rownum,row in enumerate(rows,1):
                            try:
                                if not row.get("service_id"): raise ValueError("empty service_id")
                                start,end=_date(row["start_date"]),_date(row["end_date"])
                                if start>end: mark(RULES[4],"NOT_EVALUABLE");continue
                                if any(row.get(day) not in {"0","1"} for day in weekdays):
                                    mark(RULES[4],"NOT_EVALUABLE");continue
                                weekly=tuple(index for index,name in enumerate(weekdays) if row.get(name)=="1")
                                service_dates.setdefault(row["service_id"],{"weekly_periods":[],"exceptions":{}})["weekly_periods"].append({"start_date":start.isoformat(),"end_date":end.isoformat(),"weekdays":list(weekly)})
                            except (ValueError,KeyError): mark(RULES[4],"NOT_EVALUABLE")
                if dates is not None:
                    heads,rows=dates
                    if not {"service_id","date","exception_type"}.issubset(heads):
                        mark(RULES[4],"NOT_EVALUABLE")
                    else:
                        for rownum,row in enumerate(rows,1):
                            try:
                                service=row["service_id"]
                                if not service:raise ValueError("empty service_id")
                                day=_date(row["date"]).isoformat()
                                kind=row["exception_type"]
                                if kind in {"1","2"}:
                                    service_dates.setdefault(service,{"weekly_periods":[],"exceptions":{}})["exceptions"][day]=(kind=="1")
                                else:mark(RULES[4],"NOT_EVALUABLE")
                            except (ValueError,KeyError):mark(RULES[4],"NOT_EVALUABLE")
                if rules[RULES[4]]["status"]!="NOT_EVALUABLE": mark(RULES[4],"PASS")
                if rules[RULES[4]]["status"]!="PASS": service_dates={}
        for r in rules.values():
            if r["status"]=="NOT_APPLICABLE" and not r["coverage"]["not_applicable"]: r["coverage"]["not_applicable"]=1
            if r["status"] not in {"NOT_APPLICABLE","FAIL_TECHNICAL","INSPECTION_ERROR"} and r["coverage"]["not_evaluable"]: r["status"]="NOT_EVALUABLE"
            r["category"]="QUALITY" if r["rule_id"]==RULES[3] else "TEMPORAL"
            r["evaluator_executed"]=True
        statuses=[r["status"] for r in rules.values()]
        status="FAIL_TECHNICAL" if "FAIL_TECHNICAL" in statuses else "INSPECTION_ERROR" if "INSPECTION_ERROR" in statuses else "NOT_EVALUABLE" if "NOT_EVALUABLE" in statuses else "PASS" if "PASS" in statuses else "NOT_APPLICABLE"
        return {"status":status,"rules":list(rules.values()),"findings":findings,"rule_versions":rule_versions,
            "service_dates_by_service_id":{key:{"weekly_periods":value["weekly_periods"],"exceptions":dict(sorted(value["exceptions"].items()))} for key,value in sorted(service_dates.items())}}
    except Exception as exc:
        for rid,r in rules.items():r["status"]="INSPECTION_ERROR";r["category"]="QUALITY" if rid==RULES[3] else "TEMPORAL";r["evaluator_executed"]=True
        return {"status":"INSPECTION_ERROR","rules":list(rules.values()),"findings":[],"rule_versions":rule_versions,"error":f"{type(exc).__name__}: {exc}"}
