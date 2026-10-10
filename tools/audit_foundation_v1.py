"""Additive engagement gates, control inventory and Palma crosswalk (TDL-AUD-01..03).

Reads named snapshots and source files only; never runs an auditor or mutates inputs.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
GTFS = "02_Data_Engineering/GTFS_Lab"
NETEX = "02_Data_Engineering/NeTEx_Lab"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def engagement_gate(engagement):
    """Return eligible claim categories, never a positive audit conclusion."""
    if engagement.get("contract") != "TDL_AUDIT_ENGAGEMENT/1":
        raise ValueError("Unknown engagement contract")
    if engagement.get("format") not in {"GTFS_SCHEDULE", "NETEX"}:
        raise ValueError("Only GTFS Schedule and NeTEx are supported")
    for key in ("engagement_id", "purpose", "source", "reference", "destination",
                "period", "included_controls", "exclusions", "service_reference", "requested_claims"):
        if key not in engagement:
            raise ValueError(f"Missing engagement field: {key}")
    if not isinstance(engagement["included_controls"], list) or not isinstance(engagement["exclusions"], list):
        raise ValueError("Controls and exclusions must be lists")
    if engagement["format"] == "NETEX":
        known_controls = {r["rule_id"] for r in read(ROOT / NETEX / "spec/netex_rule_registry_v1.json")["rules"]}
    else:
        modules = ["g03_structure.py", "g04_identity.py", "g05_temporal.py", "g06_operations.py", "g07_spatial.py", "g08_quality.py"]
        known_controls = set().union(*(declared_ids(ROOT / GTFS / "gtfs_lab" / p) for p in modules))
        known_controls |= {"V1-RULE-GTFS", "GTFS-STRUCT-REQUIRED", "GTFS-STRUCT-SERVICE-CALENDAR", "GTFS-REF-TRIP-ROUTE",
                           "GTFS-REF-SERVICE", "GTFS-REF-SHAPE", "GTFS-UNIQUE-PRIMARY-ID", "GTFS-COORDINATE-RANGE"}
    requested_controls = engagement["included_controls"]
    if any(not isinstance(r, str) for r in requested_controls) or len(requested_controls) != len(set(requested_controls)):
        raise ValueError("Invalid or duplicate included controls")
    if set(requested_controls) - known_controls:
        raise ValueError("Engagement includes unknown controls for this format")
    source = engagement["source"]
    digest = source.get("sha256")
    if digest is not None and not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError("Invalid source SHA-256")
    bound = bool(digest and source.get("identity") and engagement["included_controls"])
    ref = engagement["reference"]
    if ref.get("schema_sha256") is not None and not re.fullmatch(r"[a-f0-9]{64}", ref["schema_sha256"]):
        raise ValueError("Invalid schema SHA-256")
    known_spec = bool(ref.get("specification") and ref.get("version"))
    destination = engagement["destination"]
    eligible = {
        "TECHNICAL_RESULTS": bound and known_spec,
        "SCHEMA_RESULTS": bound and engagement["format"] == "NETEX" and bool(ref.get("schema_sha256")),
        "PROFILE_RESULTS": bound and engagement["format"] == "NETEX" and bool(ref.get("profile") and ref.get("profile_criteria_evidence")),
        "DESTINATION_SUITABILITY": bound and known_spec and bool(destination.get("name") and destination.get("acceptance_criteria_evidence")),
        "SERVICE_TRUTH": bound and bool(engagement["service_reference"].get("independent_evidence")),
        "LEGAL_COMPLIANCE": False,
        "CERTIFICATION": False,
    }
    if not engagement["requested_claims"] or not isinstance(engagement["requested_claims"], list):
        raise ValueError("At least one claim category must be requested")
    unknown = set(engagement["requested_claims"]) - set(eligible)
    if unknown:
        raise ValueError(f"Unknown claim categories: {sorted(unknown)}")
    blocked = [key for key in engagement["requested_claims"] if not eligible[key]]
    return {"eligible_categories": [k for k, v in eligible.items() if v], "blocked_requested_categories": blocked,
            "gate": "PASS" if not blocked else "BLOCKED_CLAIMS",
            "positive_conclusion": False,
            "note": "Eligibility requires subsequent execution and evidence; it is not a result or acceptance."}


def build_crosswalk(model, source_rows, validations, regulatory):
    """Join every source projection to a unique control and reviewed case."""
    main = model["matrix"]
    cases = model["cases"]
    main_ids = [row["rule_id"] for row in main]
    ids = [row["rule_id"] for row in validations]
    case_ids = [c["case_id"] for c in cases]
    if len(set(ids)) != len(ids) or len(set(main_ids)) != len(main_ids) or len(set(case_ids)) != len(case_ids):
        raise ValueError("Duplicate control or case identity")
    source_ids = {r["rule_id"] for r in source_rows}
    if source_ids != set(ids) or not set(main_ids) <= source_ids:
        raise ValueError("Orphan or missing source/control projection")
    mappings = {rid: [] for rid in ids}
    for case in cases:
        rules = {o["rule_id"] for o in case["occurrences"]}
        if not rules or not rules <= source_ids:
            raise ValueError("Case has an orphan occurrence rule")
        for rid in rules:
            mappings[rid].append(case["case_id"])
    legal = {rid: [] for rid in ids}
    for entry in regulatory["entries"]:
        for rid in entry.get("rules", []):
            if rid not in legal:
                raise ValueError("Regulatory entry references an orphan rule")
            legal[rid].append(entry["id"])
    out = []
    for i, control in enumerate(validations):
        rid = control["rule_id"]
        indexes = [j for j, row in enumerate(source_rows) if row["rule_id"] == rid]
        statuses = {source_rows[j]["result"] for j in indexes}
        if statuses != {control["status"]}:
            raise ValueError("Control status differs from its source projections")
        if set(control.get("case_ids", [])) != set(mappings[rid]):
            raise ValueError("Commercial case mapping differs from occurrences")
        if rid in main_ids and main[main_ids.index(rid)]["status"] != control["status"]:
            raise ValueError("Main matrix status differs")
        if len(indexes) > 1 and rid != "V1-RULE-GTFS":
            raise ValueError("Unreviewed duplicate source projection")
        out.append({"rule_id": rid, "status": control["status"],
                    "layer": "ENGINE" if rid in main_ids else "COMPLIANCE" if rid == "V1-RULE-GTFS" else "LEGACY",
                    "main_matrix_index": main_ids.index(rid) if rid in main_ids else None,
                    "source_matrix_indexes": indexes, "commercial_index": i,
                    "case_ids": mappings[rid], "regulatory_entry_ids": legal[rid],
                    "executive_case_groups": mappings[rid],
                    "executive_projection": "CASE_SUMMARY" if mappings[rid] else "TECHNICAL_DETAIL_ONLY",
                    "source_reference": control["source"],
                    "duplicate_reason": "COMPLIANCE_PROJECTED_IN_TWO_SOURCE_LAYERS" if len(indexes) > 1 else None})
    return {"contract": "TDL_CONTROL_CROSSWALK/1", "index_convention": "ZERO_BASED_JSON_ARRAY_INDEX",
            "summary": {"main_controls": len(main), "unique_controls": len(out), "source_rows": len(source_rows),
                        "layers": dict(Counter(r["layer"] for r in out)), "cases": len(cases),
                        "source_records": model["coverage"]["source_record_count"],
                        "reconciled_events": model["coverage"]["reconciled_event_count"]},
            "controls": out, "legal_conclusion_allowed": False}


def source_ref(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}


def declared_ids(path):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    return {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and re.fullmatch(r"(?:GTFS|TDL)-G\d{2}-[A-Z-]+", n.value)}


def inventory(model, source_rows, validations, regulatory):
    paths = {
        "G03": ("g03_structure.py", ["test_g03_file_catalog.py", "test_g03_field_contract.py", "test_g03_condition_runtime.py"]),
        "G04": ("g04_identity.py", ["test_g04_identity.py"]),
        "G05": ("g05_temporal.py", ["test_g05_g07_runtimes.py"]),
        "G06": ("g06_operations.py", ["test_g05_g07_runtimes.py"]),
        "G07": ("g07_spatial.py", ["test_g05_g07_runtimes.py"]),
        "G08": ("g08_quality.py", ["test_g08_quality.py"]),
        "LEGACY": ("validation.py", ["test_client_report.py", "test_client_workflow.py"]),
        "COMPLIANCE": ("compliance_adapter.py", ["test_compliance_v1_transition.py"]),
    }
    main_ids = {r["rule_id"] for r in model["matrix"]}
    runtime_ids = set().union(*(declared_ids(ROOT / GTFS / "gtfs_lab" / paths[s][0]) for s in paths if s.startswith("G")))
    if runtime_ids != main_ids:
        raise ValueError("Current GTFS runtime declarations differ from the reference inventory")
    rows = []
    for control in validations:
        rid = control["rule_id"]
        layer = rid.split("-")[1] if rid in main_ids else "COMPLIANCE" if rid == "V1-RULE-GTFS" else "LEGACY"
        code, tests = paths[layer]
        codepath = ROOT / GTFS / "gtfs_lab" / code
        if rid not in codepath.read_text(encoding="utf-8-sig"):
            raise ValueError(f"Rule not declared in implementation: {rid}")
        raw = next((row for row in model["matrix"] if row["rule_id"] == rid),
                   next(row for row in source_rows if row["rule_id"] == rid))
        rows.append({"rule_id": rid, "layer": layer, "title": control["title"],
                     "specification_reference": control.get("technical_reference"),
                     "version": raw.get("semantic_version"), "authority": raw.get("authority"),
                     "applicability": raw.get("applicability"), "requirement": raw.get("requirement"),
                     "metadata_limit": "Missing fields remain unknown; do not infer applicability from PASS.",
                     "implementation": source_ref(codepath),
                     "test_sources": [source_ref(ROOT / GTFS / "tests" / t) for t in tests],
                     "test_scope": "FAMILY_TEST_SOURCE_LOCATED_NOT_EXECUTED_BY_THIS_INVENTORY",
                     "reference_case_result": control["status"], "coverage": raw.get("coverage"),
                     "evidence": "PALMA_R3_R4_REFERENCE", "legal_conclusion_allowed": False})
    registry_path = ROOT / NETEX / "spec/netex_rule_registry_v1.json"
    registry = read(registry_path)
    runtime = (ROOT / NETEX / "netex_lab/rules.py").read_text(encoding="utf-8")
    netex = []
    for rule in registry["rules"]:
        if rule["rule_id"] not in runtime:
            raise ValueError("NeTEx registry declaration differs from implementation")
        netex.append({**rule, "implementation": source_ref(ROOT / NETEX / "netex_lab/audit.py"),
                      "registry": source_ref(registry_path),
                      "test_sources": [source_ref(ROOT / NETEX / "tests/test_netex_audit.py")],
                      "test_scope": "FAMILY_TEST_SOURCE_LOCATED_NOT_EXECUTED_BY_THIS_INVENTORY",
                      "implementation_kind": "REVIEW_MARKER" if rule["family"] == "PROFILE" else "DIAGNOSTIC" if rule["family"] == "IDENTITY" else "AUTOMATED_CHECK",
                      "legal_conclusion_allowed": False})
    capability_path = ROOT / GTFS / "spec/gtfs_schedule_field_capability_map_2026_04_27.json"
    capability = read(capability_path)
    fields_path = ROOT / GTFS / "spec/gtfs_schedule_fields_2026_04_27.json"
    fields = read(fields_path)
    file_catalog_path = ROOT / GTFS / "spec/gtfs_schedule_2026_04_27.json"
    requirements = regulatory["catalogue"]
    if len(requirements) != 48 or Counter(r["disposition"] for r in requirements) != {
        "PARTIAL": 6, "HUMAN_REVIEW_REQUIRED": 12, "DEFERRED": 20, "OUT_OF_SCOPE_V1": 10
    }:
        raise ValueError("Review changed final Compliance catalogue before inventory generation")
    return {"contract": "TDL_CONTROL_INVENTORY/1", "GTFS": rows, "NETEX": netex,
            "scope": "GTFS_LAB_AND_NETEX_LAB_CURRENT_CONTROLS_WITH_GTFS_COMPLIANCE_ADAPTER",
            "separate_compliance_scope": "Compliance NeTEx V1 is a separate frozen lab scope, not a NeTEx_Lab rule or an automatic profile validation.",
            "separate_compliance_NETEX": {"scope": "Isolated named Line fragment; not a complete PublicationDelivery",
                "evaluator_version": "compliance-v1/2", "technical_schema": "EPIP public artifact 2021 / XSD 1.3.1",
                "semantic_context": "CEN/TS 16614-4:2017; not the schema artifact version",
                "implementation": source_ref(ROOT / "tools/compliance_v1_engine.py"),
                "scope_evidence": source_ref(ROOT / "03_Compliance/COMPLIANCE_V1_SCOPE.md"),
                "not_in_NETEX_LAB_registry": True, "legal_conclusion_allowed": False},
            "GTFS_file_catalog": {"source": source_ref(file_catalog_path), "files": read(file_catalog_path)["files"],
                                  "note": "File presence/support inventory is not complete semantic coverage."},
            "GTFS_field_capability": {"source": source_ref(capability_path), "fields": deepcopy(capability["fields"]),
                                      "counts": capability["primary_assessment_counts"],
                                      "deferred_files": fields["FIELD_METADATA_DEFERRED"],
                                      "note": "132 field assessments are not 132 independent controls or proof of complete coverage."},
            "compliance_requirements": {"source": "R4_REGULATORY_REVIEW.json#catalogue (input hash in receipt)", "requirements": requirements,
                                        "note": "Frozen disposition inventory, not operator-specific applicability or new legal evaluation."},
            "NETEX_gaps": ["Full controlled EPIP criteria unavailable", "National/destination profile not identified",
                            "Broken references and temporal consistency have no automatic semantic rules in this registry",
                            "Duplicate identifiers require context review", "XSD needs pinned local dependencies"],
            "universal_coverage_claim": False}


def generate(r3, r4, output, executive=None):
    if any(root.resolve() == output.resolve() or root.resolve() in output.resolve().parents for root in (r3, r4)):
        raise ValueError("Output must be outside source packages")
    inputs = {"model": r3 / "02_EVIDENCIAS/PRESENTATION_MODEL.json",
              "source_report": r3 / "03_SOURCE_DELIVERY/report/client_report.json",
              "validations": r4 / "02_EVIDENCIAS/VALIDATIONS.json",
              "regulatory": r4 / "02_EVIDENCIAS/REGULATORY_REVIEW.json"}
    data = {k: read(p) for k, p in inputs.items()}
    model, source = data["model"], data["source_report"]["validation_matrix"]
    crosswalk = build_crosswalk(model, source, data["validations"], data["regulatory"])
    if executive is not None:
        executive_receipt_path = executive / "GENERATION_RECEIPT.json"
        executive_receipt = read(executive_receipt_path)
        if executive_receipt["source_model_sha256"] != sha(inputs["model"]):
            raise ValueError("Executive reference is bound to a different source model")
        if executive_receipt["audit_identity"] != model["identity"]:
            raise ValueError("Executive audit identity differs")
        for name, digest in executive_receipt["files"].items():
            if Path(name).name != name or sha(executive / name) != digest:
                raise ValueError("Executive file identity or integrity differs")
        crosswalk["executive_binding"] = {"receipt_path": str(executive_receipt_path),
            "receipt_sha256": sha(executive_receipt_path), "model_sha256": executive_receipt["source_model_sha256"],
            "files": executive_receipt["files"], "customer_comprehension": executive_receipt["customer_comprehension"]}
        inputs["executive_receipt"] = executive_receipt_path
    controls = inventory(model, source, data["validations"], data["regulatory"])
    output.mkdir(parents=True, exist_ok=False)
    for name, value in (("CONTROL_CROSSWALK.json", crosswalk), ("CONTROL_INVENTORY.json", controls)):
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"contract": "TDL_AUDIT_FOUNDATION_RECEIPT/1", "source_audit": model["identity"],
               "generator_sha256": sha(Path(__file__)),
               "inputs": {k: {"path": str(p), "sha256": sha(p)} for k, p in inputs.items()},
               "outputs": {p.name: sha(p) for p in output.iterdir()},
               "new_audit": False, "input_package_integrity": "NAMED_INPUT_HASHES_ONLY_NOT_FULL_PACKAGE_REVERIFICATION",
               "result": "PASS", "summary": crosswalk["summary"]}
    (output / "GENERATION_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r3", type=Path, required=True)
    parser.add_argument("--r4", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="A new output directory")
    parser.add_argument("--executive", type=Path, help="Existing executive reference to verify against the model")
    args = parser.parse_args()
    print(json.dumps(generate(args.r3, args.r4, args.output, args.executive)["summary"], ensure_ascii=False))
