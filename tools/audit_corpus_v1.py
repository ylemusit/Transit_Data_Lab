"""Additive source governance: integrity, authority, rights and change impact.

No engine execution, imports, promotion, source overwrite or HOLDOUT access.
"""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-09"
CAPTURE_ROOT = Path("P:/TransitDataLab/03_Evidence/AuditQuality/Corpus_V1_20261009")
GTFS = "03_Compliance/reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md"
SCHEMA = "01_Research_Standards/NeTEx/schemas/v2.0.0/schema_manifest.json"


def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def resolve(record):
    path = Path(record["path"])
    if path.is_absolute():
        if not path.resolve().is_relative_to(CAPTURE_ROOT.resolve()): raise ValueError("Capture outside named evidence root")
    else:
        resolved = (ROOT/path).resolve()
        if ".." in path.parts or not (resolved.is_relative_to(ROOT.resolve()) or resolved.is_relative_to(Path("P:/TransitDataLab/03_Evidence").resolve())):
            raise ValueError("Source escapes authorized project/evidence roots")
        path = ROOT/path
    return path


def capture():
    urls = {"GTFS_CURRENT.md": "https://raw.githubusercontent.com/google/transit/master/gtfs/spec/en/reference.md",
            "GTFS_LICENSE.txt": "https://raw.githubusercontent.com/google/transit/master/LICENSE",
            "NETEX_LICENSE.txt": "https://raw.githubusercontent.com/TransmodelEcosystem/NeTEx/a94e5e1752bcc13aabb8a1f3d018dc08e6978f42/LICENSE"}
    CAPTURE_ROOT.mkdir(parents=True, exist_ok=False)
    records = []
    for name, url in urls.items():
        with urlopen(Request(url, headers={"User-Agent": "TDL-source-review/1"}), timeout=30) as response:
            data = response.read(2_000_001)
            if len(data)>2_000_000 or response.status != 200: raise ValueError("Capture unavailable or too large")
            resolved_url = response.geturl()
        path = CAPTURE_ROOT/name; path.write_bytes(data)
        records.append({"name": name, "path": str(path), "sha256": sha(path), "url": url,
                        "resolved_url": resolved_url, "retrieved_on": DATE, "bytes": len(data)})
    write(CAPTURE_ROOT/"CAPTURE_RECEIPT.json", {"records": records, "promotion": "NONE", "date": DATE})
    return records


def source(identity, title, path, authority, version, url=None, **extra):
    return {"source_id": identity, "title": title, "path": str(path), "sha256": sha(resolve({"path": str(path)})),
        "authority": authority, "version": version, "official_url": url,
        "capture": {"state": "LOCAL_BYTES_IDENTIFIED", "verified_on": DATE, "retrieved_on": None},
        "validity": {"state": "PINNED_REFERENCE_NOT_CURRENT_LEGAL_ASSURANCE", "knowledge_as_of": None},
        "rights": {"state": "UNKNOWN", "evidence_source_ids": [], "distribution": "NOT_AUTHORIZED_BY_THIS_REGISTER"},
        "review": {"state": "INTERNAL_METADATA_REVIEW", "reviewer": "Codex authoring agent", "independent": False,
                   "date": DATE, "next_review_trigger": "Source, version, rights, profile or destination changes"},
        "use": "INTERNAL_REFERENCE_ONLY", **extra}


def build_sources(captures):
    entries = []
    frozen = read(ROOT/"03_Compliance/reports/evidence/compliance_v1_20260928/source_manifest.json")
    original = next(r for r in frozen["sources"] if r["path"] == "gtfs_reference.md")
    entries.append(source("GTFS-FIXED", "GTFS Schedule Reference", GTFS, "FORMAT_SPECIFICATION", "2026-04-27", original["url"],
        capture={"state": "EXISTING_CAPTURE", "retrieved_on": frozen["retrieved_on"], "verified_on": DATE}))
    if entries[-1]["sha256"] != original["sha256"]: raise ValueError("Frozen GTFS source changed")
    for record in captures:
        identity = {"GTFS_CURRENT.md": "GTFS-CANDIDATE", "GTFS_LICENSE.txt": "GTFS-LICENSE", "NETEX_LICENSE.txt": "NETEX-LICENSE"}[record["name"]]
        if sha(record["path"]) != record["sha256"]: raise ValueError("Capture changed")
        version = "2026-04-27" if identity == "GTFS-CANDIDATE" else "Apache-2.0" if identity == "GTFS-LICENSE" else "GPL-3.0"
        entries.append(source(identity, record["name"], record["path"], "FORMAT_SPECIFICATION" if identity=="GTFS-CANDIDATE" else "LICENSE_DOCUMENT", version,
            record["url"], capture={"state": "NEW_CAPTURE_NOT_PROMOTED", "retrieved_on": DATE, "verified_on": DATE}))
    license_text = resolve(next(s for s in entries if s["source_id"]=="GTFS-LICENSE")).read_text()
    if "Apache License" not in license_text: raise ValueError("Unexpected GTFS license")
    for entry in entries:
        if entry["source_id"] in {"GTFS-FIXED", "GTFS-CANDIDATE"}:
            text = resolve(entry).read_text(encoding="utf-8")
            if "Revised April 27, 2026" not in text: raise ValueError("GTFS revision requires review")
            entry["rights"] = {"state": "APACHE_2_0_NOTICE_IDENTIFIED", "evidence_source_ids": ["GTFS-LICENSE"],
                              "distribution": "REQUIRES_LICENSE_AND_NOTICES_REVIEW_BEFORE_EXTERNAL_DISTRIBUTION"}
    manifest = read(ROOT/SCHEMA)
    entries.append(source("NETEX-XSD-MANIFEST", "NeTEx pinned schema manifest", SCHEMA, "PINNED_SCHEMA_ARTIFACT", manifest["release"], manifest["source"],
        upstream_commit=manifest["commit"], root_schema_sha256=manifest["root_schema_sha256"],
        rights={"state": "GPL_CEN_CROWN_NOTICES_UNRESOLVED", "evidence_source_ids": ["NETEX-LICENSE"], "distribution": "BLOCKED_PENDING_RIGHTS_REVIEW"}))
    entries.append(source("NETEX-REGISTRY", "NeTEx Lab rule scope", "02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json", "TDL_SCOPE_AND_POLICY", "1.0.0"))
    entries.append(source("TDL-GTFS-SCOPE", "TDL bounded quality and review policy", "reports/audit_assessment_v1/PRIORITY_AND_CONCLUSION_METHOD.md", "TDL_POLICY_NOT_FORMAT_REQUIREMENT", "1.0.0"))
    entries.append(source("COMPLIANCE-SCOPE", "Compliance V1 scope", "03_Compliance/COMPLIANCE_V1_SCOPE.md", "TDL_SCOPE_NOT_LEGAL_ASSURANCE", "compliance-v1"))
    entries.append({"source_id": "NETEX-EPIP-2026", "title": "EPIP 2026 controlled text", "path": None, "sha256": None,
        "authority": "CONTROLLED_PROFILE_NOT_AVAILABLE", "version": "2026", "official_url": None,
        "capture": {"state": "NOT_AVAILABLE", "retrieved_on": None, "verified_on": DATE},
        "validity": {"state": "NOT_ESTABLISHED", "knowledge_as_of": None},
        "rights": {"state": "NOT_ESTABLISHED", "evidence_source_ids": [], "distribution": "BLOCKED"},
        "review": {"state": "MISSING_EVIDENCE", "reviewer": "Codex authoring agent", "independent": False, "date": DATE,
                   "next_review_trigger": "Authorized controlled text and mapped profile assertions available"},
        "use": "REVIEW_MARKER_ONLY_NO_CONFORMANCE_CLAIM"})
    legal = read(ROOT/"03_Compliance/reports/legal_update_20261008/source_registry.json")
    for record in legal["sources"]:
        entry = source(record["source_id"], record["title"], record["local_path"], record["authority_type"],
                       "Capture/context " + legal["date"], record.get("official_url") or record.get("capture_url"),
                       validity={"state": record["status"], "knowledge_as_of": record.get("checked_on", legal["date"]),
                                 "fresh_legal_verification_in_this_task": False})
        if entry["sha256"] != record["sha256"]: raise ValueError("Existing legal capture changed")
        entry["capture"]["retrieved_on"] = legal["date"]
        entry["context_metadata"] = {k: record[k] for k in ("effective_from", "effective_to", "repeals", "repealed_by", "use", "applicability") if k in record}
        entries.append(entry)
        consolidated = record.get("consolidated_capture")
        if consolidated:
            entries.append(source(record["source_id"]+"-CONSOLIDATED", record["title"]+" consolidated informational text", consolidated["local_path"],
                "INFORMATIONAL_CONSOLIDATION", consolidated["selection"], consolidated["url"]))
            if entries[-1]["sha256"] != consolidated["sha256"]: raise ValueError("Consolidation changed")
    for record in legal["frozen_sources"]:
        entries.append(source(record["identity"]+"-FROZEN", record["identity"], record["path"], "FROZEN_LEGAL_CONTEXT", "Frozen existing capture"))
        if entries[-1]["sha256"] != record["sha256"]: raise ValueError("Frozen legal source changed")
    # An isolated EPIP schema used by Compliance is a distinct source and scope.
    for record in frozen["sources"]:
        if record["path"].endswith(".xsd"):
            entries.append(source("COMPLIANCE-EPIP-"+record["path"], record["path"],
                "03_Compliance/reports/evidence/compliance_v1_20260928/sources/"+record["path"], "PUBLIC_PROFILE_ARTIFACT_NOT_CONTROLLED_STANDARD", "Pinned EPIP 2021 / XSD 1.3.1", record["url"]))
            if entries[-1]["sha256"] != record["sha256"]: raise ValueError("Frozen public profile source changed")
    return entries


def verify_sources(registry):
    if registry["contract"] != "TDL_SOURCE_GOVERNANCE/1": raise ValueError("Unknown source contract")
    if registry.get("engine_baselines_modified") is not False or not registry.get("revision"):
        raise ValueError("Source register cannot assert baseline promotion")
    ids = [s["source_id"] for s in registry["sources"]]
    if len(ids)!=len(set(ids)): raise ValueError("Duplicate source identity")
    verified = 0; gaps = []
    for record in registry["sources"]:
        for field in ("authority", "version", "capture", "validity", "rights", "review", "use"):
            if not record.get(field): raise ValueError("Missing source governance field")
        if not set(record["rights"]["evidence_source_ids"])<=set(ids): raise ValueError("Orphan license evidence")
        if record["path"] is None:
            if record["sha256"] is not None or record["capture"]["state"]!="NOT_AVAILABLE": raise ValueError("Invented missing source")
            gaps.append(record["source_id"]); continue
        if not re.fullmatch(r"[a-f0-9]{64}", record["sha256"]): raise ValueError("Invalid SHA-256")
        if sha(resolve(record))!=record["sha256"]: raise ValueError("Source changed: "+record["source_id"])
        verified += 1
    return {"integrity": "PASS", "identified_files": verified, "missing_sources": gaps,
            "external_distribution_approved": False, "legal_compliance_asserted": False}


def change_impact(previous, candidate, criteria):
    """Conservative impact set; an unchanged hash alone cannot hide rights/version drift."""
    old = {s["source_id"]:s for s in previous["sources"]}; new = {s["source_id"]:s for s in candidate["sources"]}
    changed = set(old)^set(new)
    for identity in set(old)&set(new):
        if any(old[identity].get(k)!=new[identity].get(k) for k in ("sha256", "version", "authority", "validity", "rights", "path", "official_url", "upstream_commit", "root_schema_sha256")):
            changed.add(identity)
    # Changes to a licence also affect sources depending on that licence.
    affected_sources = set(changed)
    while True:
        dependent = {s["source_id"] for s in list(old.values())+list(new.values()) if set(s["rights"]["evidence_source_ids"]) & affected_sources}
        if dependent<=affected_sources: break
        affected_sources |= dependent
    affected = sorted(c["criterion_id"] for c in criteria if set(c["source_ids"]) & affected_sources)
    return {"contract": "TDL_CORPUS_CHANGE_IMPACT/1", "changed_source_ids": sorted(changed), "affected_source_ids": sorted(affected_sources),
            "affected_criterion_ids": affected, "decision": "REVIEW_REQUIRED" if changed else "NO_CHANGE_IDENTIFIED",
            "baseline_promoted": False, "engine_changes": False}


def reviewed_revision(previous, candidate, criteria, review):
    verify_sources(candidate)
    impact = change_impact(previous, candidate, criteria)
    if not impact["changed_source_ids"]: raise ValueError("No revision change")
    if (not review.get("reviewer") or not review.get("rationale") or not review.get("evidence_ref") or not review.get("evidence_sha256")
        or set(review.get("criterion_ids", []))!=set(impact["affected_criterion_ids"]) or review.get("decision")!="APPROVED_INTERNAL_REFERENCE"):
        raise ValueError("Complete scoped review required")
    if sha(resolve({"path":review["evidence_ref"]}))!=review["evidence_sha256"]:
        raise ValueError("Review evidence identity differs")
    if candidate["revision"] == previous["revision"]: raise ValueError("A new revision identity is required")
    result = deepcopy(candidate); result["predecessor_revision"] = previous["revision"]
    result["change_review"] = {**review, "impact": impact}
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--capture", action="store_true"); parser.add_argument("--verify", type=Path)
    args=parser.parse_args()
    print(json.dumps(capture() if args.capture else verify_sources(read(args.verify)), ensure_ascii=False))
