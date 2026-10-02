from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from lxml import etree

from .contracts import Finding
from .intake import IntakeError, inspect_xml_stream, read_sources
from .rules import RULES, validate_registry
from .schema import SCHEMA_PATH, load_schema, verify_schema_snapshot


def _finding(
    *, rule_id: str, file_name: str, source_hash: str, status: str,
    locator: str, observed: Any, expected: Any, severity: str,
    object_type: str | None = None, object_id: str | None = None,
    recommendation: str = "", provenance: str = "",
) -> Finding:
    rule = next(item for item in RULES if item["rule_id"] == rule_id)
    body = "|".join((rule_id, file_name, locator, str(observed), status))
    return Finding(
        finding_id=hashlib.sha256(body.encode("utf-8")).hexdigest()[:20],
        rule_id=rule_id, rule_version=rule["version"], authority=rule["authority"],
        requirement_id=rule["requirement_id"], source_file=file_name,
        object_type=object_type, object_id=object_id, locator=locator,
        observed=observed, expected=expected, status=status, severity=severity,
        evidence={"source_sha256": source_hash}, recommendation=recommendation,
        provenance=provenance,
    )


def audit(input_path: str | Path, schema_path: str | Path = SCHEMA_PATH) -> dict[str, Any]:
    validate_registry()
    source_kind, sources, dataset_sha = read_sources(input_path)
    schema_path = Path(schema_path).resolve()
    try:
        schema_identity = verify_schema_snapshot(schema_path)
        schema = load_schema(schema_path)
        schema_load_error = None
    except (OSError, ValueError, etree.XMLSchemaParseError) as exc:
        schema_identity = {"release": "2.0.0", "commit": "a94e5e1752bcc13aabb8a1f3d018dc08e6978f42",
                           "root_schema": "xsd/NeTEx_publication.xsd", "root_schema_sha256": None}
        schema = None
        schema_load_error = type(exc).__name__
    findings: list[Finding] = []
    records: list[dict[str, Any]] = []

    for source in sources:
        try:
            inspection = inspect_xml_stream(source.data, schema)
        except IntakeError:
            findings.append(_finding(
                rule_id="NETEX-XML-001", file_name=source.name, source_hash=source.sha256,
                status="FAIL_TECHNICAL", locator="/", observed="MALFORMED_OR_UNSAFE_XML",
                expected="Well-formed XML without DTD/entity declarations", severity="ERROR",
                recommendation="Correct the XML syntax and remove DTD/entity declarations.",
            ))
            findings.append(_finding(
                rule_id="NETEX-XSD-001", file_name=source.name, source_hash=source.sha256,
                status="NOT_EVALUABLE", locator="/", observed="XSD_NOT_EVALUABLE",
                expected="Valid against pinned NeTEx v2.0.0 XSD", severity="REVIEW",
                recommendation="Correct the XML or unsafe declaration before schema validation.",
            ))
            records.append({"source_file": source.name, "source_sha256": source.sha256,
                            "well_formedness": "NOT_WELL_FORMED", "xsd_validation": "XSD_NOT_EVALUABLE",
                            "structural_inventory": None})
            continue

        findings.append(_finding(
            rule_id="NETEX-XML-001", file_name=source.name, source_hash=source.sha256,
            status="PASS", locator="/", observed="WELL_FORMED", expected="Well-formed XML",
            severity="INFO",
        ))
        errors = list(inspection.errors)
        valid = inspection.xsd_valid
        xsd_status = "PASS" if valid is True else "FAIL_TECHNICAL" if valid is False else "INSPECTION_ERROR"
        xsd_state = "XSD_VALID" if valid is True else "XSD_INVALID" if valid is False else "INSPECTION_ERROR"
        findings.append(_finding(
            rule_id="NETEX-XSD-001", file_name=source.name, source_hash=source.sha256,
            status=xsd_status, locator="/", observed=xsd_state, expected="XSD_VALID against pinned NeTEx v2.0.0",
            severity="INFO" if valid else "ERROR",
            recommendation=("" if valid else "Resolve the reported XSD validation errors.") if schema is not None else "Restore the exact pinned local schema snapshot before evaluating XSD.",
            provenance=("; ".join(errors[:50]) if schema is not None else f"Schema loading failed: {schema_load_error}"),
        ))
        inventory = inspection.inventory
        for identifier, types in inventory["duplicate_ids"].items():
            findings.append(_finding(
                rule_id="NETEX-IDENTITY-001", file_name=source.name, source_hash=source.sha256,
                status="HUMAN_REVIEW_REQUIRED", locator="//*[@id='…']", observed={"id": identifier, "types": types},
                expected="Unique object identity should be reviewed in the dataset context",
                severity="ADVISORY", object_id=identifier,
                recommendation="Review identifier scope and uniqueness; this TDL diagnostic is not a normative profile conclusion.",
                provenance="L4 recommendation; duplicate id values are inventoried without asserting legal or EPIP failure.",
            ))
        findings.append(_finding(
            rule_id="NETEX-PROFILE-001", file_name=source.name, source_hash=source.sha256,
            status="HUMAN_REVIEW_REQUIRED", locator="/PublicationDelivery",
            observed="XSD evaluated; full EPIP 2026 assertions are not implemented",
            expected="Requirement-by-requirement EPIP evaluation from controlled normative text",
            severity="REVIEW",
            recommendation="Do not interpret XSD validity as EPIP conformance. Complete a controlled-text requirement mapping before profile claims.",
            provenance="CEN/TS 16614-4:2026 full text and exact v2 constraint mapping remain unavailable in this corpus.",
        ))
        records.append({"source_file": source.name, "source_sha256": source.sha256,
                        "well_formedness": "WELL_FORMED", "xsd_validation": xsd_state,
                        "xsd_errors": errors[:50], "structural_inventory": inventory})

    findings.sort(key=lambda item: (item.source_file, item.rule_id, item.finding_id))
    counts = Counter(item.status for item in findings)
    return {
        "manifest_version": "1.0.0",
        "dataset_identity": {"source_kind": source_kind, "input_sha256": dataset_sha,
                             "member_count": len(sources)},
        "schema_identity": schema_identity,
        "rule_registry_version": "1.0.0",
        "rule_registry": sorted(RULES, key=lambda item: item["rule_id"]),
        "records": records,
        "findings": [item.to_dict() for item in findings],
        "rule_execution_summary": dict(sorted(counts.items())),
        "gaps": ["EPIP 2026 full-text requirement mapping not available",
                 "Spanish additional profile and NAP acceptance contract not identified in reviewed public sources",
                 "NAP acceptance and regulatory compliance are not evaluated by this runtime"],
        "reproducibility": {"deterministic_normalized_output": True,
                            "excluded_runtime_metadata": ["wall-clock timestamp", "absolute input path"]},
    }
