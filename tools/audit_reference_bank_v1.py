"""Build an authored, source-bound synthetic bank without importing audit engines."""
from collections import Counter
from copy import deepcopy
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

from tools.audit_corpus_v1 import (ROOT, DATE, CAPTURE_ROOT, SCHEMA, build_sources,
                                  read, write, sha, verify_sources, change_impact, resolve)
from tools.audit_reference_definitions_v1 import DEFINITIONS, RATIONALES, case_data, expectation

BANK_ROOT = Path("P:/TransitDataLab/02_Data/Development/AuditQuality/ReferenceBank_V1_20261009")
VARIANTS = ("positive", "negative", "boundary")


def archive_feed(path, data, raw):
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED) as archive:
        bodies = dict(raw)
        for name, rows in data.items():
            if name in bodies: continue
            fields = list(dict.fromkeys(k for row in rows for k in row))
            stream=io.StringIO(newline=""); writer=csv.DictWriter(stream,fieldnames=fields,lineterminator="\n")
            writer.writeheader();writer.writerows(rows);bodies[name]=stream.getvalue()
        for name, text in sorted(bodies.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,text.encode("utf-8"))


def criterion(rule, locator, authority, text, source_ids, version):
    return {"criterion_id":rule,"rule_id":rule,"rule_version":version,"authority":authority,"text":text,
            "source_ids":source_ids,"source_locator":locator,"review":{"reviewer":"Codex authoring agent","date":DATE,
                "basis":"Source criterion and authored fixture facts; no engine output used", "independent":False},
            "claim_gate":"NO_LEGAL_OR_DESTINATION_CLAIM"}


def build(output, bank_root=BANK_ROOT):
    output=Path(output);bank_root=Path(bank_root)
    if output.exists() or bank_root.exists():raise ValueError("Use new reference directories")
    inventory_path=ROOT/"reports/audit_foundation_v1/accepted_reference_20261008/CONTROL_INVENTORY.json"
    inventory=read(inventory_path);rules={r["rule_id"]:r for r in inventory["GTFS"]}
    if {r[0] for r in DEFINITIONS}!=set(rules):raise ValueError("GTFS rule inventory differs")
    captures=read(CAPTURE_ROOT/"CAPTURE_RECEIPT.json")["records"]
    registry={"contract":"TDL_SOURCE_GOVERNANCE/1","revision":"TDL-CORPUS-REFERENCE-20261009-V1",
              "sources":build_sources(captures),"engine_baselines_modified":False}
    integrity=verify_sources(registry)
    source_map={s["source_id"]:s for s in registry["sources"]}
    spec=resolve(source_map["GTFS-FIXED"]).read_text(encoding="utf-8")
    criteria=[];cases=[]
    # All input implementation identities are checked against the inventory; no evaluators execute.
    implementation_checks={}
    for r in inventory["GTFS"]+inventory["NETEX"]:
        for record in [r["implementation"]]+r.get("test_sources",[]):
            if sha(ROOT/record["path"])!=record["sha256"]:raise ValueError("Inventory input drift: "+record["path"])
            implementation_checks[record["path"]]=record["sha256"]
    original_fixture_root=ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures"
    original_fixture_manifest=read(original_fixture_root/"corpus_manifest.json")
    original_fixture_checks={}
    for record in original_fixture_manifest["cases"]:
        path=ROOT/"02_Data_Engineering/NeTEx_Lab"/record["path"]
        if sha(path)!=record["sha256"]:raise ValueError("Historical synthetic fixture changed")
        original_fixture_checks[path.relative_to(ROOT).as_posix()]=record["sha256"]
    bank_root.mkdir(parents=True,exist_ok=False);output.mkdir(parents=True,exist_ok=False)
    for rule, locator, authority, text, family in DEFINITIONS:
        if locator not in spec:raise ValueError("Missing criterion selector: "+locator)
        sources=["GTFS-FIXED"]
        if authority.startswith("TDL_"):sources.append("TDL-GTFS-SCOPE")
        if rule=="V1-RULE-GTFS":sources.extend(["COMPLIANCE-SCOPE","EU-REG-2017-1926-FROZEN"])
        criteria.append(criterion(rule,locator,authority,text,sources,rules[rule]["version"]))
        for i, variant in enumerate(VARIANTS):
            data, raw, context=case_data(family,variant);case_id=rule+"--"+variant
            path=bank_root/(case_id+".zip");archive_feed(path,data,raw)
            expected=expectation(family,variant)
            expected["rationale"]=RATIONALES[family][i]
            classification="AMBIGUOUS" if expected["criterion_state"] in {"UNKNOWN","REVIEW_REQUIRED"} else "CONDITIONAL" if variant=="boundary" and family in {"header","calendar_presence","parent","shape_ref"} else "BOUNDARY" if variant=="boundary" else "INVALID" if expected["criterion_state"]=="VIOLATED" else "VALID"
            cases.append({"case_id":case_id,"format":"GTFS_SCHEDULE","criterion_id":rule,"scope":"CURRENT_RULE_ILLUSTRATION",
                "classification":classification,"variant":variant,"fixture":path.name,"sha256":sha(path),"context":context,
                "expected":expected,"source_type":"SYNTHETIC_AUTHORED","producer":"TDL reference authoring agent",
                "review":"INTERNAL_SOURCE_AND_FACT_REVIEW_NOT_INDEPENDENT_AUDIT","unit":"FOCUSED_SCENARIO_NOT_WHOLE_FEED"})
    netex_registry=read(ROOT/"02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json")
    versions={r["rule_id"]:r["version"] for r in netex_registry["rules"]}
    minimal=(ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures/valid_minimal.xml").read_bytes()
    malformed=(ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures/malformed.xml").read_bytes()
    invalid=(ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures/xsd_invalid.xml").read_bytes()
    duplicate=(ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures/duplicate_id_candidate.xml").read_bytes()
    dtd=(ROOT/"02_Data_Engineering/NeTEx_Lab/tests/fixtures/dtd_external.xml").read_bytes()
    netex = {
      "NETEX-XML-001":("ALWAYS","TDL_SECURE_XML_POLICY","XML bien formado y sin DTD/entidades en este alcance.",[minimal,malformed,dtd],["PASS","FAIL_TECHNICAL","FAIL_TECHNICAL"],
                       ["PublicationDelivery bien formado.","Etiquetas no balanceadas impiden interpretación XML.","DTD/entidad externa: rechazo de política segura TDL, no afirmar que todo DTD sea XML inválido."]),
      "NETEX-XSD-001":("WELL_FORMED_XML","PINNED_XSD_ARTIFACT","Validez frente al artefacto XSD 2.0.0 identificado; no es perfil.",[minimal,invalid,malformed],["PASS","FAIL_TECHNICAL","NOT_EVALUABLE"],
                       ["Raíz/namespace y elementos mínimos se contrastan con el XSD fijado.","Documento bien formado cuya estructura no satisface el XSD.","XML no interpretable: la capa XSD no puede emitir conformidad."]),
      "NETEX-IDENTITY-001":("IDENTIFIED_OBJECTS","TDL_DIAGNOSTIC","Revisar identidad duplicada sin declarar fallo normativo de perfil.",[minimal,duplicate,duplicate.replace(b'id="duplicate" version="1.0"',b'id="duplicate" version="2.0"',1)],["PASS","HUMAN_REVIEW_REQUIRED","HUMAN_REVIEW_REQUIRED"],
                       ["No hay identificadores duplicados inventariados; no es conformidad de todos los objetos.","Identificador repetido exige contexto de tipos y versiones.","Cambiar versión no permite dictamen de unicidad global sin alcance revisado."]),
      "NETEX-PROFILE-001":("REGULAR_SCHEDULED_BUS","CONTROLLED_PROFILE_NOT_AVAILABLE","No evaluar EPIP completo sin texto autorizado y aserciones mapeadas.",[minimal,invalid,malformed],["HUMAN_REVIEW_REQUIRED","HUMAN_REVIEW_REQUIRED","NOT_EVALUABLE"],
                       ["XSD válido no acredita EPIP.","XSD inválido no proporciona por sí solo evaluación completa de EPIP.","XML mal formado impide seguir a una evaluación de perfil."])
    }
    for rule, (locator,authority,text,fixtures,statuses,reasons) in netex.items():
        sources=["NETEX-REGISTRY"]
        if rule=="NETEX-XSD-001":sources.append("NETEX-XSD-MANIFEST")
        if rule=="NETEX-PROFILE-001":sources.append("NETEX-EPIP-2026")
        criteria.append(criterion(rule,locator,authority,text,sources,versions[rule]))
        for i,variant in enumerate(VARIANTS):
            case_id=rule+"--"+variant;path=bank_root/(case_id+".xml");path.write_bytes(fixtures[i])
            status=statuses[i];state="SATISFIED" if status=="PASS" else "VIOLATED" if status=="FAIL_TECHNICAL" else "UNKNOWN" if status=="NOT_EVALUABLE" else "REVIEW_REQUIRED"
            cases.append({"case_id":case_id,"format":"NETEX","criterion_id":rule,"scope":"CURRENT_RULE_ILLUSTRATION",
                "classification":"AMBIGUOUS" if state in {"UNKNOWN","REVIEW_REQUIRED"} else "BOUNDARY" if variant=="boundary" else "INVALID" if state=="VIOLATED" else "VALID",
                "variant":variant,"fixture":path.name,"sha256":sha(path),"context":{"schema_identity":"v2.0.0 pinned snapshot", "profile_full_text_available":False},
                "expected":{"criterion_state":state,"criterion_status":status,"rationale":reasons[i],"explanation":"Expectativa de capa, no del documento completo.",
                            "details":{},"aggregate_feed_status":"NOT_PREDICTED","engine_observed_status":None},
                "source_type":"SYNTHETIC_AUTHORED_OR_ALLOWED_LOCAL_FIXTURE","review":"INTERNAL_SOURCE_AND_FACT_REVIEW_NOT_INDEPENDENT_AUDIT","unit":"XML_FILE"})
    # Candidate families are reference material for 10/11; no new rule is implemented or selected.
    candidate="TDL-CAND-GTFS-CONDITION-RESOLUTION"
    criteria.append(criterion(candidate,"### routes.txt","PROPOSED_FORMAT_CONDITION_REFERENCE","Resolver condición de agency_id con cardinalidad de agencias conocida o desconocida.",["GTFS-FIXED"],"candidate/1"))
    for variant in VARIANTS:
        data,raw,ctx=case_data("header",variant);case_id=candidate+"--"+variant
        if variant=="boundary":ctx["agency_cardinality_evidence_available"]=False
        path=bank_root/(case_id+".zip");archive_feed(path,data,raw)
        expected=expectation("header",variant);expected["rationale"]=RATIONALES["header"][VARIANTS.index(variant)]
        if variant=="boundary":expected.update(criterion_state="UNKNOWN",criterion_status="NOT_EVALUABLE",rationale="El consumidor de la condición no recibe evidencia de cardinalidad; no inventar falso ni verdadero.")
        cases.append({"case_id":case_id,"format":"GTFS_SCHEDULE","criterion_id":candidate,"scope":"PROPOSED_REFERENCE_NOT_ENGINE_RULE",
                      "classification":"CONDITIONAL","variant":variant,"fixture":path.name,"sha256":sha(path),"context":ctx,"expected":expected,
                      "source_type":"SYNTHETIC_AUTHORED","review":"INTERNAL_SOURCE_AND_FACT_REVIEW_NOT_INDEPENDENT_AUDIT","unit":"FOCUSED_SCENARIO"})
    candidate="TDL-CAND-NETEX-REFERENCE-CONTEXT"
    criteria.append(criterion(candidate,"Pinned rule scope; candidate local reference graph","PROPOSED_TDL_DIAGNOSTIC_NOT_PROFILE_ASSERTION",
        "Contrastar grafo local solo si tipo, versión y ámbito están definidos; no declarar obligación EPIP ausente.",["NETEX-REGISTRY"],"candidate/1"))
    for i,variant in enumerate(VARIANTS):
        case_id=candidate+"--"+variant;path=bank_root/(case_id+".json")
        payload={"object":{"type":"Line","id":"L","version":"1"},"reference":{"type":"Line","id":"MISSING" if i==1 else "L","version":"1"},"local_scope_available":i!=2}
        write(path,payload);status=["PASS","HUMAN_REVIEW_REQUIRED","NOT_EVALUABLE"][i]
        cases.append({"case_id":case_id,"format":"NETEX","criterion_id":candidate,"scope":"PROPOSED_REFERENCE_NOT_ENGINE_RULE",
            "classification":"CONDITIONAL" if i<2 else "AMBIGUOUS","variant":variant,"fixture":path.name,"sha256":sha(path),"context":{"representation":"LOCAL_GRAPH_FRAGMENT_NOT_PUBLICATIONDELIVERY"},
            "expected":{"criterion_state":["SATISFIED","REVIEW_REQUIRED","UNKNOWN"][i],"criterion_status":status,
                        "rationale":["Tipo/id/versión coinciden en el ámbito local declarado.","Destino local ausente: diagnóstico pendiente de criterio de perfil autorizado.","Sin ámbito local no se puede decidir resolución de referencia."][i],
                        "explanation":"Material candidato para diseño 11, no capacidad del motor.","details":{},"aggregate_feed_status":"NOT_PREDICTED","engine_observed_status":None},
            "source_type":"SYNTHETIC_AUTHORED","review":"INTERNAL_SOURCE_AND_FACT_REVIEW_NOT_INDEPENDENT_AUDIT","unit":"LOCAL_REFERENCE_GRAPH"})
    for case in cases:
        if case["format"]=="NETEX" and case["scope"]=="CURRENT_RULE_ILLUSTRATION":
            names={"NETEX-XML-001":["valid_minimal.xml","malformed.xml","dtd_external.xml"],
                   "NETEX-XSD-001":["valid_minimal.xml","xsd_invalid.xml","malformed.xml"],
                   "NETEX-IDENTITY-001":["valid_minimal.xml","duplicate_id_candidate.xml","duplicate_id_candidate.xml"],
                   "NETEX-PROFILE-001":["valid_minimal.xml","xsd_invalid.xml","malformed.xml"]}
            origin=original_fixture_root/names[case["criterion_id"]][VARIANTS.index(case["variant"])]
            case["origin"]={"kind":"EXISTING_SYNTHETIC_FIXTURE", "path":origin.relative_to(ROOT).as_posix(),"sha256":sha(origin),
                            "mutation":"FIRST_OBJECT_VERSION_1.0_TO_2.0" if case["criterion_id"]=="NETEX-IDENTITY-001" and case["variant"]=="boundary" else "BYTE_PRESERVING_COPY"}
        else:
            definition="tools/audit_reference_definitions_v1.py" if case["format"]=="GTFS_SCHEDULE" else "tools/audit_reference_bank_v1.py"
            case["origin"]={"kind":"AUTHORED_SYNTHETIC", "definition_path":definition,"definition_sha256":sha(ROOT/definition),
                            "permitted_use":"INTERNAL_REFERENCE_NO_OPERATOR_DATA"}
    bank={"contract":"TDL_REFERENCE_BANK/1","revision":"TDL-REFERENCE-20261009-V1","fixture_root":str(bank_root),
          "current_rule_ids":sorted(set(rules)|set(versions)),"cases":cases,"engine_executed":False,"holdout_accessed":False,
          "review_independence":"AUTHORING_AGENT_SOURCE_REVIEW_ONLY","operator_generalization":False,
          "scope_limit":"One focused family with three scenarios per current control; not exhaustive field/branch or full-format coverage."}
    write(output/"SOURCE_REGISTRY.json",registry);write(output/"CRITERIA.json",criteria);write(output/"REFERENCE_BANK.json",bank)
    regulatory=deepcopy(inventory["compliance_requirements"]["requirements"])
    for row in regulatory:
        row["source_ids"]=["EU-REG-2017-1926-FROZEN","COMPLIANCE-SCOPE"]
        row["direct_normative_assertion_review"]="NOT_PERFORMED_BY_THIS_TASK"
        row["catalogue_provenance"]="CONTROL_INVENTORY.json#/compliance_requirements/requirements"
    write(output/"REGULATORY_SCOPE_INDEX.json",{"requirements":regulatory,"legal_conclusion_allowed":False})
    fixed=next(s for s in registry["sources"] if s["source_id"]=="GTFS-FIXED")
    candidate_source=next(s for s in registry["sources"] if s["source_id"]=="GTFS-CANDIDATE")
    candidate_registry=deepcopy(registry)
    next(s for s in candidate_registry["sources"] if s["source_id"]=="GTFS-FIXED")["sha256"]=candidate_source["sha256"]
    actual_change=change_impact(registry,candidate_registry,criteria)
    write(output/"SOURCE_COMPARISON.json",{"frozen_sha256":fixed["sha256"],"new_capture_sha256":candidate_source["sha256"],
        "comparison":"IDENTICAL_BYTES" if fixed["sha256"]==candidate_source["sha256"] else "REVIEW_REQUIRED", "impact":actual_change,"promotion":False})
    receipt={"contract":"TDL_REFERENCE_GENERATION_RECEIPT/1","date":DATE,"input_inventory_sha256":sha(inventory_path),
        "authoring_definition_sha256":sha(ROOT/"tools/audit_reference_definitions_v1.py"),"generator_sha256":sha(Path(__file__)),
        "implementation_identity_checks":implementation_checks,"historical_fixture_identity_checks":original_fixture_checks,
        "source_governance_sha256":sha(ROOT/"tools/audit_corpus_v1.py"),"schema_manifest_sha256":sha(ROOT/SCHEMA),
        "source_integrity":integrity,"cases":len(cases),
        "case_classes":dict(Counter(c["classification"] for c in cases)),"artifact_sha256":{p.name:sha(p) for p in output.glob("*.json")}}
    write(output/"GENERATION_RECEIPT.json",receipt)
    return {"output":str(output),"bank_root":str(bank_root),"cases":len(cases),"current_rules":len(bank["current_rule_ids"]),"sources":len(registry["sources"])}


def validate_bank(bank, criteria, registry, root=None):
    if bank["contract"]!="TDL_REFERENCE_BANK/1" or bank["engine_executed"] or bank["holdout_accessed"]:raise ValueError("Invalid reference bank scope")
    root=Path(root or bank["fixture_root"]);source_ids={s["source_id"] for s in registry["sources"]}
    cmap={c["criterion_id"]:c for c in criteria}
    if len(cmap)!=len(criteria):raise ValueError("Duplicate criterion")
    case_ids=set(); covered=set(); classes=set()
    for criterion in criteria:
        if not set(criterion["source_ids"])<=source_ids or not criterion["source_locator"]:raise ValueError("Unsourced criterion")
    for case in bank["cases"]:
        if case["case_id"] in case_ids:raise ValueError("Duplicate reference case")
        case_ids.add(case["case_id"]);classes.add(case["classification"])
        if case["criterion_id"] not in cmap:raise ValueError("Orphan case")
        expected=case["expected"]
        if not case.get("origin"):raise ValueError("Missing permitted fixture origin")
        if not expected.get("rationale") or expected.get("engine_observed_status") is not None or expected["aggregate_feed_status"]!="NOT_PREDICTED":raise ValueError("Unreviewed or engine-derived expectation")
        if expected["criterion_state"] not in {"SATISFIED","VIOLATED","UNKNOWN","REVIEW_REQUIRED","NOT_APPLICABLE","RECOMMENDATION_UNMET"}:raise ValueError("Unknown expected criterion state")
        state_status={"SATISFIED":"PASS","VIOLATED":"FAIL_TECHNICAL","UNKNOWN":"NOT_EVALUABLE","REVIEW_REQUIRED":"HUMAN_REVIEW_REQUIRED","NOT_APPLICABLE":"NOT_APPLICABLE","RECOMMENDATION_UNMET":"PASS"}
        if expected["criterion_status"]!=state_status[expected["criterion_state"]]:raise ValueError("Expected state/status mismatch")
        if expected["criterion_state"] in {"UNKNOWN","REVIEW_REQUIRED"} and expected["criterion_status"] not in {"NOT_EVALUABLE","HUMAN_REVIEW_REQUIRED"}:raise ValueError("Unsupported positive unknown")
        if cmap[case["criterion_id"]]["authority"]=="RECOMMENDATION" and expected["criterion_status"]=="FAIL_TECHNICAL":raise ValueError("Recommendation converted into failure")
        if "NETEX-EPIP-2026" in cmap[case["criterion_id"]]["source_ids"] and expected["criterion_status"]=="PASS":raise ValueError("Unsupported profile claim")
        name=Path(case["fixture"])
        if name.is_absolute() or len(name.parts)!=1 or name.name in {".",".."}:raise ValueError("Unsafe fixture path")
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or sha(path)!=case["sha256"]:raise ValueError("Fixture changed")
        if case["scope"]=="CURRENT_RULE_ILLUSTRATION":covered.add(case["criterion_id"])
    if covered!=set(bank["current_rule_ids"]):raise ValueError("Current rule coverage differs")
    if not {"VALID","INVALID","CONDITIONAL","BOUNDARY","AMBIGUOUS"}<=classes:raise ValueError("Missing reference classes")
    return {"result":"PASS","cases":len(case_ids),"current_rules_represented":len(covered),"class_counts":dict(Counter(c["classification"] for c in bank["cases"])),
            "engine_accuracy_measured":False,"independent_review":False}


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,required=True);parser.add_argument("--bank-root",type=Path,default=BANK_ROOT);parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    result=validate_bank(read(args.output/"REFERENCE_BANK.json"),read(args.output/"CRITERIA.json"),read(args.output/"SOURCE_REGISTRY.json")) if args.verify else build(args.output,args.bank_root)
    print(json.dumps(result,ensure_ascii=False))
