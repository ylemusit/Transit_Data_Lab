"""Opt-in NeTEx local reference diagnostics; not an EPIP or NAP conformance rule."""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from lxml import etree

from .intake import IntakeError, MAX_XML_MEMBER_BYTES, read_sources


CONTRACT = "TDL_NETEX_REFERENCE_CONTEXT_V1"
RULE_ID = "TDL-CAND-NETEX-REFERENCE-CONTEXT"
RULE_VERSION = "candidate/1"
AUTHORITY = "PROPOSED_TDL_DIAGNOSTIC_NOT_PROFILE_ASSERTION"
MAX_REFERENCES = 1_000_000
MAX_OBJECTS = 2_000_000


def _local_attr(element: etree._Element, expected: str) -> str | None:
    for key, value in element.attrib.items():
        if etree.QName(key).localname.casefold() == expected.casefold():
            return value
    return None


def _inspect_member(name: str, data: bytes) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(data) > MAX_XML_MEMBER_BYTES:
        raise IntakeError("XML member exceeds configured size limit")
    object_rows: list[dict[str, Any]] = []
    reference_rows: list[dict[str, Any]] = []
    object_stack: list[tuple[etree._Element, str, str]] = []
    etree.clear_error_log()
    try:
        context = etree.iterparse(BytesIO(data), events=("start", "end"), resolve_entities=False,
                                  no_network=True, load_dtd=False, huge_tree=False, recover=False)
        for event, element in context:
            if not isinstance(element.tag, str):
                continue
            local_name = etree.QName(element).localname
            if event == "start":
                object_id = _local_attr(element, "id")
                if object_id and not local_name.casefold().endswith("ref"):
                    if len(object_rows) >= MAX_OBJECTS:
                        raise IntakeError("NeTEx candidate object limit exceeded")
                    object_type = local_name
                    version = _local_attr(element, "version")
                    object_rows.append({"file": name, "type": object_type, "id": object_id,
                                        "version": version})
                    object_stack.append((element, object_type, object_id))
                continue

            if local_name.casefold().endswith("ref"):
                target_id = _local_attr(element, "ref")
                if target_id:
                    if len(reference_rows) >= MAX_REFERENCES:
                        raise IntakeError("NeTEx candidate reference limit exceeded")
                    source_type, source_id = (object_stack[-1][1], object_stack[-1][2]) if object_stack else (None, None)
                    target_type = local_name[:-3]
                    reference_rows.append({
                        "file": name,
                        "line": element.sourceline,
                        "source_type": source_type,
                        "source_id": source_id,
                        "target_type": target_type,
                        "target_id": target_id,
                        "target_version": _local_attr(element, "versionRef"),
                    })
            if object_stack and object_stack[-1][0] is element:
                object_stack.pop()
            parent = element.getparent()
            element.clear()
            if parent is not None:
                while element.getprevious() is not None:
                    del parent[0]
        if context.root is None:
            raise IntakeError("XML has no document element")
        if context.root.getroottree().docinfo.doctype:
            raise IntakeError("DTD and entity declarations are not accepted")
    except IntakeError:
        raise
    except (etree.XMLSyntaxError, etree.LxmlError, OSError, ValueError) as exc:
        raise IntakeError("XML member could not be parsed for candidate reference diagnostics") from exc
    return object_rows, reference_rows


def _finding(source_hash: str, ref: dict[str, Any], status: str, reason: str) -> dict[str, Any]:
    locator = f"//{ref['target_type']}Ref[line={ref['line']}]"
    identity = "|".join((source_hash, ref["file"], locator, ref["target_type"],
                         ref["target_id"], str(ref["target_version"]), status))
    return {
        "finding_id": hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20],
        "rule_id": RULE_ID,
        "rule_version": RULE_VERSION,
        "authority": AUTHORITY,
        "status": status,
        "source_file": ref["file"],
        "locator": locator,
        "source_object": {"type": ref["source_type"], "id": ref["source_id"]},
        "target_reference": {"type": ref["target_type"], "id": ref["target_id"],
                             "version": ref["target_version"]},
        "reason": reason,
        "evidence": {"source_sha256": source_hash},
    }


def audit_reference_context(input_path: str | Path, *, closed_scope: bool = False) -> dict[str, Any]:
    """Resolve simple typed ``*Ref/@ref`` links within the supplied XML scope.

    ``closed_scope`` is an explicit operator assertion that the supplied input
    contains the complete target catalogue for this diagnostic. Missing links
    remain NOT_EVALUABLE when that assertion is absent.
    """
    path = Path(input_path).resolve(strict=True)
    try:
        source_kind, sources, source_hash = read_sources(path)
    except (OSError, IntakeError) as exc:
        raise IntakeError("Input could not be read for the candidate diagnostic") from exc

    objects: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    member_results: list[dict[str, str]] = []
    for source in sources:
        try:
            member_objects, member_references = _inspect_member(source.name, source.data)
            objects.extend(member_objects)
            references.extend(member_references)
            member_results.append({"source_file": source.name, "status": "PARSED"})
        except IntakeError as exc:
            member_results.append({"source_file": source.name, "status": "NOT_EVALUABLE",
                                  "reason": str(exc)})

    effective_closed = closed_scope and all(row["status"] == "PARSED" for row in member_results)
    parse_complete = all(row["status"] == "PARSED" for row in member_results)
    by_identity: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for obj in objects:
        by_identity[(obj["type"], obj["id"])].append(obj)
        by_id[obj["id"]].append(obj)

    findings: list[dict[str, Any]] = []
    for ref in references:
        if not parse_complete:
            findings.append(_finding(source_hash, ref, "NOT_EVALUABLE",
                                      "At least one supplied XML member could not be parsed; the local reference inventory is incomplete."))
            continue
        candidates = by_identity.get((ref["target_type"], ref["target_id"]), [])
        if ref["target_version"] is not None:
            exact = [item for item in candidates if item["version"] == ref["target_version"]]
            if len(exact) == 1:
                status, reason = "PASS", "One exact local type/id/version target was found."
            elif len(exact) > 1:
                status, reason = "HUMAN_REVIEW_REQUIRED", "More than one exact local type/id/version target was found."
            elif candidates:
                status, reason = "HUMAN_REVIEW_REQUIRED", "A local type/id exists, but its version does not match the reference."
            elif by_id.get(ref["target_id"]):
                status, reason = "HUMAN_REVIEW_REQUIRED", "The local identifier exists under a different object type."
            elif effective_closed:
                status, reason = "HUMAN_REVIEW_REQUIRED", "No target exists in the explicitly declared closed local scope."
            else:
                status, reason = "NOT_EVALUABLE", "No local target was found; scope completeness or external targets are unknown."
        else:
            if len(candidates) == 1 and candidates[0]["version"] is None:
                status, reason = "PASS", "One local type/id target without version context was found."
            elif len(candidates) == 1:
                status, reason = "HUMAN_REVIEW_REQUIRED", "A versioned local target exists, but the reference omits version context."
            elif len(candidates) > 1:
                status, reason = "HUMAN_REVIEW_REQUIRED", "Multiple local versions or targets match this type/id."
            elif by_id.get(ref["target_id"]):
                status, reason = "HUMAN_REVIEW_REQUIRED", "The local identifier exists under a different object type."
            elif effective_closed:
                status, reason = "HUMAN_REVIEW_REQUIRED", "No target exists in the explicitly declared closed local scope."
            else:
                status, reason = "NOT_EVALUABLE", "No local target was found; scope completeness or external targets are unknown."
        findings.append(_finding(source_hash, ref, status, reason))

    if not references:
        overall = "NOT_EVALUABLE"
        limitation = "No references in the supported *Ref/@ref shape were found."
    elif any(item["status"] == "HUMAN_REVIEW_REQUIRED" for item in findings):
        overall = "HUMAN_REVIEW_REQUIRED"
        limitation = "Candidate diagnostics need review; they do not assert NeTEx profile failure."
    elif any(item["status"] == "NOT_EVALUABLE" for item in findings):
        overall = "NOT_EVALUABLE"
        limitation = "One or more references cannot be resolved without a complete local scope."
    else:
        overall = "PASS"
        limitation = "All recognized references resolved in the local graph; profile conformance is not evaluated."

    if not effective_closed:
        closed_note = "Input is treated as a partial scope; unresolved targets remain NOT_EVALUABLE."
    else:
        closed_note = "Caller declared the supplied XML set complete for this local diagnostic."
    return {
        "contract": CONTRACT,
        "version": "1.0.0",
        "dataset_identity": {"source_kind": source_kind, "input_sha256": source_hash,
                             "member_count": len(sources)},
        "rule": {"rule_id": RULE_ID, "rule_version": RULE_VERSION, "authority": AUTHORITY,
                 "status": overall, "object_count": len(objects), "reference_count": len(references),
                 "closed_scope_declared": closed_scope, "closed_scope_effective": effective_closed,
                 "scope_note": closed_note},
        "member_results": member_results,
        "findings": sorted(findings, key=lambda item: (item["source_file"], item["locator"], item["finding_id"])),
        "limitations": [limitation,
                        "Only attributes named ref/versionRef on elements ending in Ref are interpreted.",
                        "Object type is inferred from the Ref element name; aliases and profile-specific type mappings are not inferred.",
                        "This addendum does not validate the XSD, EPIP, Spanish profile, NAP acceptance, or legal compliance."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the opt-in NeTEx local-reference diagnostic V1.")
    parser.add_argument("input", type=Path, help="NeTEx XML or ZIP")
    parser.add_argument("--json", type=Path, required=True, help="Output JSON path")
    parser.add_argument("--closed-scope", action="store_true",
                        help="Declare supplied XML members the complete local reference scope")
    args = parser.parse_args()
    result = audit_reference_context(args.input, closed_scope=args.closed_scope)
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
