"""Evidence-bounded finding, coverage and priority projections (TDL-AUD-04..06).

Reads existing results and the identified source to count populations; does not
execute audit rules, change producer data or assign unsupported service impacts.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CASE_FIELDS = {
    "PAL-G03-COLOR": ("routes.txt", "route_text_color", "OPTIONAL_VALID_IF_SUPPLIED"),
    "PAL-G04-PARENT": ("stops.txt", "parent_station", "OPTIONAL_FOR_OBSERVED_STOP_TYPES_VALID_IF_SUPPLIED"),
    "PAL-G04-SHAPE": ("trips.txt", "shape_id", "CONDITIONAL_REQUIREDNESS_NOT_TRIGGERED_IN_REFERENCE_VALID_IF_SUPPLIED"),
    "PAL-G06-FREQUENCY": ("frequencies.txt", "exact_times", "EXACT_TIMES_1_INTERVAL_BOUND"),
    "PAL-G07-DUP": ("shapes.txt", "shape_dist_traveled", "OPTIONAL_DISTANCE_PROGRESSION_IF_SUPPLIED"),
    "PAL-G07-EQUAL": ("shapes.txt", "shape_dist_traveled", "OPTIONAL_DISTANCE_PROGRESSION_IF_SUPPLIED"),
}
STATUSES = {"PASS", "FAIL_TECHNICAL", "NOT_EVALUABLE", "NOT_APPLICABLE", "INSPECTION_ERROR", "HUMAN_REVIEW_REQUIRED"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def priority(context):
    """Assign a proposed work priority only from a documented destination impact.

    References identify evidence for a reviewer; this function cannot authenticate
    external statements or substitute for that review.
    """
    required = ("destination", "acceptance_criteria_ref", "target_date", "consequence_evidence_ref")
    missing = [k for k in required if not context.get(k)]
    consequence = context.get("consequence_kind")
    if missing or consequence in (None, "NOT_VERIFIED"):
        return {"value": "UNASSESSED", "missing": missing,
                "basis": "Destination, timing or consequences are not documented; counts alone do not establish priority."}
    try:
        date.fromisoformat(context["target_date"])
    except (ValueError, TypeError):
        raise ValueError("Priority target_date must be an ISO date")
    levels = {"SERVICE_UNAVAILABLE": "HIGH", "FUNCTIONAL_FAILURE": "HIGH",
              "DEGRADATION": "MEDIUM", "PRESENTATION_DEFECT": "LOW"}
    if consequence not in levels:
        raise ValueError("Unknown documented consequence category")
    level = levels[consequence]
    if consequence == "SERVICE_UNAVAILABLE" and context.get("urgent_no_workaround"):
        if not context.get("urgency_evidence_ref"):
            raise ValueError("Critical priority needs evidence of urgency and absence of workaround")
        level = "CRITICAL"
    return {"value": level, "missing": [], "basis": "TDL proposed rubric for a documented consequence in the stated destination.",
            "evidence_ref": context["consequence_evidence_ref"], "human_validation": "REQUIRED_BEFORE_EXTERNAL_USE"}


def validate_finding(finding):
    required = ("contract", "case_id", "format", "condition", "criterion", "exposure", "evidence",
                "observed_impact", "potential_impact", "cause", "action", "closure", "priority", "destination_blocking")
    if any(k not in finding for k in required):
        raise ValueError("Incomplete finding contract")
    if finding["contract"] != "TDL_ASSESSED_FINDING/1" or finding["format"] not in {"GTFS_SCHEDULE", "NETEX"}:
        raise ValueError("Unsupported finding contract or format")
    exposure = finding["exposure"]
    count, denominator = exposure["affected_count"], exposure["eligible_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError("Invalid affected population")
    if denominator is not None and (not isinstance(denominator, int) or isinstance(denominator, bool) or denominator < count):
        raise ValueError("Denominator cannot be smaller than affected units")
    if denominator is None and not exposure.get("denominator_unknown_reason"):
        raise ValueError("Unknown denominator requires a reason")
    if not exposure.get("unit") or not exposure.get("basis"):
        raise ValueError("Population needs units and evidence basis")
    if not finding["evidence"] or not finding["criterion"].get("reference"):
        raise ValueError("Finding needs source evidence and an identified criterion")
    if finding["potential_impact"].get("state") not in {"POTENTIAL_ONLY", "NOT_ASSESSED"}:
        raise ValueError("Potential impact must not be presented as verified")
    cause = finding["cause"]
    if cause["state"] not in {"UNKNOWN", "HYPOTHESIS", "CONFIRMED"}:
        raise ValueError("Unknown cause state")
    if cause["state"] == "CONFIRMED" and not cause.get("evidence_ref"):
        raise ValueError("Confirmed cause requires evidence")
    impact = finding["observed_impact"]
    if impact["state"] not in {"NOT_VERIFIED", "VERIFIED"}:
        raise ValueError("Unknown observed-impact state")
    if impact["state"] == "VERIFIED" and not impact.get("evidence_ref"):
        raise ValueError("Observed impact requires evidence")
    blocking = finding["destination_blocking"]
    if blocking["state"] not in {"NOT_DETERMINED", "CONFIRMED", "NOT_BLOCKING"}:
        raise ValueError("Unknown destination blocking state")
    if blocking["state"] != "NOT_DETERMINED" and not blocking.get("evidence_ref"):
        raise ValueError("Destination decision requires evidence")
    if finding["priority"]["value"] not in {"UNASSESSED", "LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError("Unknown priority level")
    if finding["priority"]["value"] != "UNASSESSED":
        if impact["state"] != "VERIFIED" or not finding["priority"].get("evidence_ref"):
            raise ValueError("Assessed priority requires a verified consequence")
    if not finding["action"] or not finding["closure"]:
        raise ValueError("Action and closure criteria are required")


def source_populations(source):
    populations = {}
    with zipfile.ZipFile(source) as archive:
        for filename, field in {(v[0], v[1]) for v in CASE_FIELDS.values()}:
            total = supplied = eligible = 0
            shape_groups = Counter()
            with archive.open(filename) as raw:
                reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
                if field not in (reader.fieldnames or []):
                    raise ValueError("Reference source field is unavailable")
                for row in reader:
                    total += 1
                    supplied += row.get(field, "") != ""
                    if filename == "frequencies.txt":
                        eligible += row.get(field) == "1"
                    if filename == "shapes.txt":
                        shape_groups[row["shape_id"]] += 1
            if filename == "shapes.txt":
                if supplied != total:
                    raise ValueError("Review pair eligibility: some shape distances are missing")
                eligible = sum(max(n - 1, 0) for n in shape_groups.values())
            elif filename != "frequencies.txt":
                eligible = supplied
            populations[filename] = {"total_rows": total, "supplied_values": supplied,
                                      "eligible": eligible, "shape_groups": len(shape_groups) if shape_groups else None}
    return populations


def project_findings(model, source, context):
    if sha(source) != model["identity"]["source_sha256"]:
        raise ValueError("Source differs from the audited identity")
    if {c["case_id"] for c in model["cases"]} != set(CASE_FIELDS):
        raise ValueError("This population projection is scoped to the reviewed Palma cases")
    populations = source_populations(source)
    findings = []
    for index, case in enumerate(model["cases"]):
        filename, field, presence = CASE_FIELDS[case["case_id"]]
        p = populations[filename]
        for occurrence in case["occurrences"]:
            match = re.fullmatch(re.escape(filename) + r":(?:ROW|data_row):(\d+)", occurrence["normalized_locator"])
            if not match or not 1 <= int(match[1]) <= p["total_rows"]:
                raise ValueError("Occurrence locator is outside its identified source")
        unit = "SHAPE_TRANSITION" if filename == "shapes.txt" else "EXACT_TIMES_1_INTERVAL" if filename == "frequencies.txt" else "SUPPLIED_FIELD_VALUE"
        count = case["reconciled_event_count"]
        finding = {"contract": "TDL_ASSESSED_FINDING/1", "case_id": case["case_id"], "format": "GTFS_SCHEDULE",
            "condition": case["observation"],
            "criterion": {"text": case["criterion"], "reference": case["evidence"], "field_presence": presence,
                          "source_metadata_limitations": case["limitations"]},
            "exposure": {"affected_count": count, "eligible_count": p["eligible"], "total_source_rows": p["total_rows"],
                         "unit": unit, "field": field, "basis": "Named source population counted after SHA-256 match; findings retained from source model.",
                         "percentage": round(100 * count / p["eligible"], 2) if p["eligible"] else None,
                         "percentage_meaning": "Affected units in this criterion, not passengers, risk or whole-feed quality."},
            "evidence": [{"source_ref": f"PRESENTATION_MODEL.json#/cases/{index}/occurrences",
                          "source_sha256": model["identity"]["source_sha256"], "record_count": case["occurrence_count"],
                          "locator_convention": "ONE_BASED_DATA_ROWS; original and normalized locators remain in the source model."}],
            "technical_state": "NONCONFORMITY_DOCUMENTED", "service_evidence_confidence": "NOT_VERIFIED",
            "observed_impact": {"state": "NOT_VERIFIED", "text": case["impact_known"], "evidence_ref": None},
            "potential_impact": {"state": "POTENTIAL_ONLY", "text": case["impact_potential"]},
            "cause": {"state": "UNKNOWN", "text": "The recorded condition does not establish its cause.", "evidence_ref": None},
            "action": case["action"], "closure": case["closure_criteria"], "disposition": case["disposition"],
            "priority": priority(context), "destination_blocking": {"state": "NOT_DETERMINED", "evidence_ref": None},
            "producer_status": case["producer_status"], "reaudit": case["reaudit"]}
        validate_finding(finding)
        findings.append(finding)
    return findings, populations


def project_coverage(model, run, g06):
    header = run["g03"]["header_schema"]
    gaps = header["not_evaluable"]
    group_counts = Counter((r["file"], r.get("field"), r["reason"]) for r in gaps)
    if header["status"] != "NOT_EVALUABLE" or not gaps:
        raise ValueError("Review changed header evaluability before projecting reasons")
    time_rule = next(r for r in model["matrix"] if r["rule_id"] == "TDL-G06-TRIP-TIME-ORDER-REVIEW")
    reviews = [r for r in g06["deferred_rule_reviews"] if r["rule_id"] == time_rule["rule_id"]]
    if time_rule["status"] != "NOT_EVALUABLE" or not reviews:
        raise ValueError("Trip-time review reason is missing or has changed")
    return {"contract": "TDL_COVERAGE_EXPLANATION/1", "new_operator_findings": 0,
        "non_evaluable_controls": [
            {"rule_id": "GTFS-G03-HEADER-SCHEMA", "status": header["status"],
             "reason": "Conditional-presence signals, unresolved metadata and extension policy leave part of the header evaluation unknown.",
             "provenance": "R3 engine_run/run.json#/g03/header_schema",
             "annotations": len(gaps), "reason_counts": dict(Counter(r["reason"] for r in gaps)),
             "groups": [{"file": f, "field": field, "reason": reason, "annotations": count} for (f, field, reason), count in sorted(group_counts.items())],
             "scope_not_covered": "Conditions whose signals are UNKNOWN; unresolved conditional headers and custom fields. This is not a blanket absence of all header checks.",
             "missing_or_unresolved": "Runtime handling of absent conditional fields and unresolved presence/extension criteria; not automatically missing producer data.",
             "available_partial_checks": {"recorded_header_decisions": len(header["decisions"]),
                  "resolved_conditional_row_evaluations": header["conditional_rows_total"],
                  "conditional_sample_truncated": header["conditional_rows_truncated"],
                  "limits": "Counts use different units; resolved checks are not a complete denominator and sampling does not represent full evidence."},
             "alternative": "Review absent-vs-empty signal semantics against captured criteria and classify the specific extensions; retain existing CSV, field-type and reference checks within their scope.",
             "alternative_status": "PROPOSED_NOT_EXECUTED", "owner_of_followup": "TDL rule/corpus review plus producer clarification for intended custom fields"},
            {"rule_id": time_rule["rule_id"], "status": time_rule["status"], "reason": reviews[0]["reason"],
             "provenance": "R3 engine_run/g06.json#/deferred_rule_reviews", "coverage": time_rule["coverage"],
             "scope_not_covered": "Cross-stop arrival/departure ordering as a binding requirement; the counter is a review item, not a trip population.",
             "missing_or_unresolved": "Reviewed authority decision and intended service-time semantics; adding a MUST cannot be inferred from the runtime result.",
             "alternative": "Agree a non-normative diagnostic with explicit midnight/extended-hour and frequency-service semantics; compare with an independent timetable when available.",
             "alternative_status": "PROPOSED_NOT_EXECUTED", "owner_of_followup": "TDL methodology review and service planner"}],
        "aggregation_policy": "Do not add annotations to defects, mix check units or calculate a global PASS percentage."}


def conclusion(controls, context):
    if any(r["status"] not in STATUSES for r in controls):
        raise ValueError("Unknown result status")
    if len({r["rule_id"] for r in controls}) != len(controls):
        raise ValueError("Conclusion requires unique controls, not duplicated projections")
    counts = Counter(r["status"] for r in controls)
    gaps = any(counts[s] for s in ("NOT_EVALUABLE", "INSPECTION_ERROR", "HUMAN_REVIEW_REQUIRED"))
    if counts["FAIL_TECHNICAL"]:
        result = "NONCONFORMITIES_DETECTED_WITH_COVERAGE_LIMITS" if gaps else "NONCONFORMITIES_DETECTED_IN_DEFINED_SCOPE"
    elif gaps:
        result = "NO_NONCONFORMITY_DETECTED_WITH_COVERAGE_LIMITS"
    elif counts["PASS"]:
        result = "NO_NONCONFORMITY_DETECTED_IN_DEFINED_SCOPE"
    else:
        result = "NO_APPLICABLE_CONTROL_RESULT"
    return {"contract": "TDL_TECHNICAL_CONCLUSION/1", "technical_result": result, "unique_control_counts": dict(counts),
            "priority": priority(context), "destination_suitability": "NOT_DETERMINED_BY_TECHNICAL_COUNTS",
            "legal_compliance": "NOT_EVALUATED", "service_truth": "NOT_VERIFIED",
            "scope_limit": "Result limited to the implemented controls and supplied evidence; no certification or universal format coverage."}


def generate(r3, source, foundation, output):
    if any(p.resolve() == output.resolve() or p.resolve() in output.resolve().parents for p in (r3, foundation)):
        raise ValueError("Output must be outside source packages and accepted foundation")
    paths = {"model": r3 / "02_EVIDENCIAS/PRESENTATION_MODEL.json", "run": r3 / "03_SOURCE_DELIVERY/engine_run/run.json",
             "g06": r3 / "03_SOURCE_DELIVERY/engine_run/g06.json", "crosswalk": foundation / "CONTROL_CROSSWALK.json", "source_zip": source,
             "foundation_receipt": foundation / "GENERATION_RECEIPT.json"}
    binding = read(paths["foundation_receipt"])
    if binding["inputs"]["model"]["sha256"] != sha(paths["model"]) or binding["outputs"]["CONTROL_CROSSWALK.json"] != sha(paths["crosswalk"]):
        raise ValueError("Foundation crosswalk is not bound to this model")
    model, run, g06, crosswalk = (read(paths[k]) for k in ("model", "run", "g06", "crosswalk"))
    context = {"destination": None, "acceptance_criteria_ref": None, "target_date": None,
               "consequence_kind": "NOT_VERIFIED", "consequence_evidence_ref": None}
    findings, populations = project_findings(model, source, context)
    coverage = project_coverage(model, run, g06)
    result = conclusion(crosswalk["controls"], context)
    output.mkdir(parents=True, exist_ok=False)
    for name, body in (("ASSESSED_FINDINGS.json", findings), ("SOURCE_POPULATIONS.json", populations),
                       ("COVERAGE_EXPLANATION.json", coverage), ("TECHNICAL_CONCLUSION.json", result)):
        (output / name).write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"contract": "TDL_ASSESSMENT_RECEIPT/1", "generator_sha256": sha(Path(__file__)),
               "audit_identity": model["identity"], "inputs": {k: {"path": str(p), "sha256": sha(p)} for k, p in paths.items()},
               "outputs": {p.name: sha(p) for p in output.iterdir()}, "new_engine_run": False,
               "source_population_counted": True, "source_modified": False, "result": "PASS",
               "cases": len(findings), "non_evaluable_controls": len(coverage["non_evaluable_controls"])}
    (output / "GENERATION_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("r3", "source", "foundation", "output"):
        parser.add_argument("--" + arg, required=True, type=Path)
    args = parser.parse_args()
    receipt = generate(args.r3, args.source, args.foundation, args.output)
    print(json.dumps({k: receipt[k] for k in ("result", "cases", "non_evaluable_controls")}))
