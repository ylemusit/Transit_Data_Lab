"""Reproduce presentation workflow with reviewed, empty and partially uncovered evidence.

This creates synthetic sealed inputs, not an engine audit or a producer correction.
Run from GTFS_Lab; outputs must be outside the source tree.
"""
from __future__ import annotations

import argparse
import copy
import zipfile
from pathlib import Path
from collections import Counter

from gtfs_lab.professional_audit import digest, generate, read, write
from gtfs_lab.interpretation.cases import sha256_json
from tests.test_professional_audit import ProfessionalAuditTests


def run(root, workbook_command=None):
    root.mkdir(parents=True, exist_ok=False)
    receipts = []
    for scenario in ("reviewed", "empty", "pending"):
        zone = root / scenario; zone.mkdir()
        source = zone / "source.zip"
        with zipfile.ZipFile(source, "w") as z:
            z.writestr("stops.txt", "stop_id,stop_name,stop_lat,stop_lon\nS1,Parada sintética,41,-3\n")
            z.writestr("shapes.txt", "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\nX,41,-3,0,0\nX,41.001,-3.001,1,100\n")
        sha = digest(source)
        manifest, interpretation, decisions = ProfessionalAuditTests().fixture()
        manifest["audit_id"] = "SYNTHETIC-" + scenario.upper()
        manifest["dataset_identity"]["source_sha256"] = sha
        interpretation["dataset_identity"] = {"dataset_id": "SYNTHETIC-STRUCTURE", "sha256": sha}
        interpretation["execution_identity"]["audit_execution_id"] = "ENGINE-" + scenario.upper()
        case_model = decisions["case_contract"]
        case_model["dataset_identity"] = copy.deepcopy(interpretation["dataset_identity"])
        case_model["execution_identity"].update(client_audit_id=manifest["audit_id"], audit_execution_id=interpretation["execution_identity"]["audit_execution_id"])
        if scenario == "empty":
            interpretation["source_findings"] = []
            manifest["technical_status"] = "PASS"
        if scenario == "pending":
            new = {"raw_finding_id": "uncovered-C", "origin": "AUDIT_ENGINE", "rule_id": "UNKNOWN-FAMILY", "source_file": "custom.txt", "observed": "preserve exactly"}
            interpretation["source_findings"].append(new)
            case_model["coverage"].update(source_record_count=3, unclassified_record_count=1, source_origins={"AUDIT_ENGINE": 2, "LEGACY": 1})
            case_model["unclassified_source_record_ids"] = [new["raw_finding_id"]]
        case_model["source_interpretation"]["sha256"] = sha256_json(interpretation)
        delivery = zone / "delivery"; delivery.mkdir()
        write(delivery / "AUDIT_CONSOLIDATED.json", interpretation)
        write(delivery / "engine_run" / "engine_report.json", {"technical_evaluation": {"stages": [{"stage": "SYNTHETIC", "status": manifest["technical_status"], "rules": [{"rule_id": "SYNTHETIC-CRITERION", "status": manifest["technical_status"]}]}]}})
        write(delivery / "compliance.json", {"result": "NOT_EVALUABLE"})
        manifest["delivery_artifacts"] = {p.relative_to(delivery).as_posix(): {"sha256": digest(p), "size_bytes": p.stat().st_size} for p in delivery.rglob("*") if p.is_file()}
        write(delivery / "audit_manifest.json", manifest)
        manifest_sha = digest(delivery / "audit_manifest.json")
        write(delivery / "delivery_seal.json", {"audit_manifest_sha256": manifest_sha})
        case_model["execution_identity"]["manifest_sha256"] = manifest_sha
        decision_file = None
        if scenario != "empty":
            decision_file = zone / "decisions.json"; write(decision_file, decisions)
        receipt = generate(delivery, zone / "presentation", "SYNTHETIC-PRESENTATION-" + scenario.upper(), source, decision_file, workbook_command)
        model = read(zone / "presentation/02_EVIDENCIAS/PRESENTATION_MODEL.json")
        assert len(model["pending_records"]) == (1 if scenario == "pending" else 0)
        assert len(model["cases"]) == (0 if scenario == "empty" else 1)
        assert digest(source) == sha
        assert model["case_contract"]["use_readiness"]["status"] != "APTO"
        receipts.append(receipt)
    write(root / "SYNTHETIC_RECEIPTS.json", receipts)
    return receipts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--node")
    parser.add_argument("--workbook-script")
    args = parser.parse_args()
    if bool(args.node) != bool(args.workbook_script): parser.error("--node and --workbook-script must be provided together")
    print(run(args.output, [args.node, args.workbook_script] if args.node else None))
