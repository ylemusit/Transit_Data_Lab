"""Portable complete workbook renderer over the professional presentation model."""
import json
import math
from pathlib import Path

VERSION = "1.1.0"
IDENTITY_HEADERS = ["ID auditoría", "ID ejecución", "SHA-256 origen", "Revisión"]
COVERAGE_LABELS = {"source_record_count":"Registros fuente", "classified_record_count":"Registros clasificados",
    "reconciled_event_count":"Eventos reconciliados", "duplicate_source_reference_count":"Referencias fuente duplicadas",
    "unclassified_record_count":"Registros pendientes de decisión", "accounting_gap":"Brecha de reconciliación",
    "source_origins":"Orígenes de evidencia"}


def text(value):
    if value is None: return ""
    if isinstance(value, (dict, list)): return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def record_rows(records):
    keys = list(dict.fromkeys(key for row in records for key in row))
    serialized = [text(row) for row in records]
    count = max([1, *[math.ceil(len(s) / 15000) for s in serialized]])
    headers = ["N.º registro", *keys, *[f"Registro íntegro (JSON) [parte {i+1}]" for i in range(count)]]
    rows = [[i+1, *[row.get(k) for k in keys], *[serialized[i][j*15000:(j+1)*15000] for j in range(count)]] for i,row in enumerate(records)]
    return headers, rows


def expanded_columns(headers, rows, widths):
    """Split overlong literal fields rather than silently truncate Excel cells."""
    result_headers, result_rows, result_widths = [], [[] for _ in rows], []
    for column, header in enumerate(headers):
        values = [row[column] if column < len(row) else None for row in rows]
        width = widths[column] if column < len(widths) else 28
        chunk_size = max(200, min(1000, int(width * 16)))
        chunks = max([1, *[math.ceil(len(text(v)) / chunk_size) for v in values]])
        for part in range(chunks):
            result_headers.append(header if chunks == 1 else f"{header} [parte {part+1}]")
            result_widths.append(widths[column] if column < len(widths) else 28)
            for index, value in enumerate(values):
                result_rows[index].append(value if chunks == 1 else text(value)[part*chunk_size:(part+1)*chunk_size])
    if len(result_headers) > 16384 or len(result_rows) > 1048575:
        raise ValueError("Workbook exceeds Excel dimensions; no records were truncated")
    return result_headers, result_rows, result_widths


def build_workbook(model, output):
    import xlsxwriter
    output = Path(output)
    if output.exists(): raise FileExistsError("Workbook output already exists")
    identity = model["identity"]
    identity_values = [identity.get(k, "") for k in ("client_audit_id", "audit_execution_id", "source_sha256", "revision")]
    counts = {}
    with xlsxwriter.Workbook(str(output), {"strings_to_formulas": False, "strings_to_urls": False}) as wb:
        wb.set_properties({"title": "Auditoría GTFS", "author": "Yeison Arbey Carrillo Lemus", "comments": "Todos los derechos reservados."})
        header = wb.add_format({"font_name":"Arial","font_size":10,"bold":True,"font_color":"white","bg_color":"#17324D","text_wrap":True,"valign":"vcenter","align":"center"})
        body = wb.add_format({"font_name":"Arial","font_size":10,"text_wrap":True,"valign":"top"})
        number = wb.add_format({"font_name":"Arial","font_size":10,"num_format":"#,##0","valign":"top"})
        editable = wb.add_format({"font_name":"Arial","font_size":10,"bg_color":"#FFF3CE","text_wrap":True,"valign":"top","locked":False})
        title = wb.add_format({"font_name":"Arial","font_size":15,"bold":True,"font_color":"#17324D"})

        def write(sheet, row, column, value, fmt=body):
            if isinstance(value, bool): result=sheet.write_boolean(row,column,value,fmt)
            elif isinstance(value,(int,float)) and math.isfinite(value): result=sheet.write_number(row,column,value,number)
            else: result=sheet.write_string(row,column,text(value),fmt)
            if result: raise ValueError("Workbook value could not be written completely")

        summary = wb.add_worksheet("Resumen")
        summary.hide_gridlines(2); summary.set_tab_color("#17324D")
        summary.set_column(0,0,32); summary.set_column(1,1,95)
        write(summary,1,0,"Auditoría GTFS",title); summary.set_row(1,26)
        summary_rows = [*zip(IDENTITY_HEADERS,identity_values),
            ("Resultado técnico",model["presentation"]["technical_text"]),
            ("Estado para el uso",model["presentation"]["use_text"]),
            ("Base del análisis",model["presentation"]["basis"]),
            *[(COVERAGE_LABELS.get(k,k.replace('_',' ')),v) for k,v in model["coverage"].items()],
            ("Limitaciones","\n".join(model["presentation"]["limitations"]))]
        for row,(label,value) in enumerate(summary_rows,3):
            write(summary,row,0,label); write(summary,row,1,value)
            summary.set_row(row,max(24,min(400,(len(text(value))//85+len(text(value).splitlines()))*14+8)))
        next_row=4+len(summary_rows)
        for step in model["presentation"]["steps"]:
            write(summary,next_row,0,f"{step['order']}. {step['action']}")
            write(summary,next_row,1,step["basis"]+"\nInformación necesaria: "+text(step["missing"]))
            summary.set_row(next_row,80); next_row+=1
        summary.set_landscape(); summary.fit_to_pages(1,0); summary.print_area(0,0,next_row,1)

        def data_sheet(name, headers, rows, widths=None, editable_columns=()):
            rows=[[*r,*identity_values] for r in rows]
            headers=[*headers,*IDENTITY_HEADERS]
            widths=[*(widths or [28]*(len(headers)-4)),22,22,38,16]
            headers,rows,widths=expanded_columns(headers,rows,widths)
            sheet=wb.add_worksheet(name); sheet.hide_gridlines(2); sheet.freeze_panes(1,2)
            for col,width in enumerate(widths): sheet.set_column(col,col,width)
            for col,label in enumerate(headers): write(sheet,0,col,label,header)
            sheet.set_row(0,44)
            for index,row in enumerate(rows,1):
                lines=max([1,*[sum(max(1,math.ceil(len(line)/max(8,widths[c]))) for line in text(v).split('\n')) for c,v in enumerate(row)]])
                sheet.set_row(index,min(400,max(26,lines*14+8)))
                for col,value in enumerate(row): write(sheet,index,col,value,editable if col in editable_columns else body)
            sheet.autofilter(0,0,len(rows),len(headers)-1)
            sheet.set_landscape(); sheet.fit_to_pages(1,0); sheet.repeat_rows(0)
            counts[name]=len(rows)
            return sheet

        clients=model["client_cases"]
        fields=["case_id","title","observation","criterion","action","closure_criteria","impact_known","impact_potential","limitations","entities_text","disposition_text","priority_text","producer_text","reaudit_text"]
        data_sheet("Casos",["ID caso","Caso","Observación","Criterio","Acción propuesta","Criterio de cierre","Impacto conocido","Impacto potencial","Limitaciones","Entidades afectadas","Disposición fuente","Prioridad fuente","Productor fuente","Reauditoría fuente"],
                   [[c[k] for k in fields] for c in clients],[18,28,42,34,42,36,28,28,34,30,22,18,24,26])
        contract=model["case_contract"]
        records=[{"_record_type":"Metadatos del contrato","_contract_metadata":{k:v for k,v in contract.items() if k!='cases'}}]
        for case in contract["cases"]:
            records.append({"_record_type":"Metadatos del caso",**{k:v for k,v in case.items() if k!='occurrences'}})
            for index,occ in enumerate(case.get("occurrences",[]),1):
                records.append({"_record_type":"Ocurrencia","_case_id":case["case_id"],"_occurrence_index":index,**(occ if isinstance(occ,dict) else {"occurrence":occ})})
        records.extend({"_record_type":"Pendiente",**(r if isinstance(r,dict) else {"source_record":r})} for r in model["pending_records"])
        records.extend({"_record_type":"Control técnico",**r} for r in model["matrix"])
        headers,rows=record_rows(records)
        labels={"_record_type":"Tipo de registro","_case_id":"ID caso","_occurrence_index":"N.º ocurrencia","_contract_metadata":"Metadatos del contrato (JSON)"}
        labels_headers=[labels.get(h,h) for h in headers]
        data_sheet("Ocurrencias",labels_headers,rows,[14,*[60 if "JSON" in h else 28 for h in labels_headers[1:]]])
        data_sheet("Seguimiento",["ID caso","Caso","Estado del productor registrado","Respuesta del productor (editable)","Estado del productor (editable)","Responsable productor (editable)","Estado de verificación registrado","Revisión del auditor (editable)","Estado auditor (editable)"],
                   [[c['case_id'],c['title'],c['producer_text'],'','','',c['reaudit_text'],'',''] for c in clients],
                   [18,28,28,40,24,28,28,42,24],(3,4,5,7,8))
        keys=["rule_id","stage","status","applicability","evaluability","finding_count","semantic_version","authority","specification_reference"]
        data_sheet("Matriz",["Regla","Etapa","Resultado","Aplicabilidad","Evaluabilidad","Hallazgos","Versión de regla","Autoridad técnica","Referencia"],
                   [[row.get(k) for k in keys] for row in model["matrix"]],[30,14,24,24,24,14,16,24,50])
        records=[{"case_id":c['case_id'],"title":c['title'],"evidence":e} for c in clients for e in c['evidence']]
        headers,rows=record_rows(records)
        data_sheet("Evidencias",headers,rows)
    return {"renderer":"TDL_PORTABLE_WORKBOOK","version":VERSION,"sheets":counts,"external_strings_as_formulas":False,"native_visual_acceptance":"PENDING"}
