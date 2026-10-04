"""Deterministic generic consolidation with exact raw-finding accounting."""
from __future__ import annotations

import base64
import hashlib
import json
from collections import defaultdict
from typing import Any

from . import VERSION
from .analyzers.g07_geometry import RULE_ID as G07_RULE, classify_findings
from .contract import validate_result
from .impact import load_population_and_relationships, propagated_counts

ENTITY_FIELDS = {"shape": ("shape_id",), "trip": ("trip_id",), "route": ("route_id",),
                 "service": ("service_id",), "stop": ("stop_id",), "stop_time": ("stop_id",),
                 "calendar": ("service_id",), "calendar_date": ("service_id",), "frequency": ("trip_id",),
                 "agency": ("agency_id",)}
VALID_ENTITIES = set(ENTITY_FIELDS) | {"feed"}


def _entity(finding: dict[str, Any]) -> tuple[str, str]:
    observed = finding.get("observed") if isinstance(finding.get("observed"), dict) else {}
    fields = finding.get("source_fields") if isinstance(finding.get("source_fields"), dict) else {}
    source_file = str(finding.get("source_file") or finding.get("file") or finding.get("table") or "")
    if source_file == "stop_times.txt":
        trip = observed.get("trip_id", fields.get("trip_id", finding.get("trip_id")))
        sequence = observed.get("stop_sequence", fields.get("stop_sequence", finding.get("stop_sequence")))
        if trip is not None and sequence is not None:
            return "stop_time", f"{trip}:{sequence}"
        return "stop_time", str(finding.get("record_locator", finding.get("row_locator", "unknown")))
    source_entity = {"shapes.txt": "shape", "trips.txt": "trip", "routes.txt": "route",
                     "stops.txt": "stop", "agency.txt": "agency", "calendar.txt": "calendar",
                     "calendar_dates.txt": "calendar_date", "frequencies.txt": "frequency"}.get(source_file)
    if source_entity:
        for name in ENTITY_FIELDS[source_entity]:
            value = observed.get(name, fields.get(name, finding.get(name)))
            if value not in (None, ""):
                return source_entity, str(value)
    for entity_type, names in ENTITY_FIELDS.items():
        for name in names:
            value = observed.get(name, fields.get(name, finding.get(name)))
            if value not in (None, ""):
                return entity_type, str(value)
    locator = finding.get("record_locator", finding.get("row_locator", finding.get("locator")))
    if locator not in (None, ""):
        return "feed", str(locator)
    return "feed", hashlib.sha256(_canonical(finding)).hexdigest()[:16]


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")


def semantic_fingerprint(result: dict[str, Any]) -> str:
    """Replay fingerprint excludes execution IDs and raw evidence provenance."""
    families = []
    for family in result["finding_families"]:
        families.append({key: value for key, value in family.items() if key != "evidence_refs"})
    semantic = {"contract_version": result["contract_version"], "dataset_identity": result["dataset_identity"],
                "families": families, "coverage": result["coverage"]}
    return hashlib.sha256(_canonical(semantic)).hexdigest()


def _family_id(dimensions: dict[str, str]) -> str:
    # URL-safe base64 of canonical JSON is injective, order-independent and
    # collision-free for distinct keys; unlike a digest it needs no collision policy.
    token = base64.urlsafe_b64encode(_canonical(dimensions)).decode("ascii").rstrip("=")
    return "family-v1:" + token


def _pattern_assignment(finding: dict[str, Any], g07_groups: dict[str, list[dict[str, Any]]]) -> str:
    supplied = finding.get("pattern_id")
    if supplied in {"EXACT_DUPLICATE_GEOMETRY", "QUANTIZATION_COMPATIBLE", "DISTANCE_DECREASE", "MIXED_PATTERN", "UNKNOWN_PATTERN"}:
        return supplied
    for pattern_id, values in g07_groups.items():
        if finding in values:
            return pattern_id
    return "TECHNICAL_FINDING" if finding.get("rule_id") else "UNKNOWN_PATTERN"


def build_result(*, dataset_identity: dict[str, Any], audit_execution_id: str, engine_version: str,
                 findings: list[dict[str, Any]], zip_path: str | None = None,
                 tdl_ref: str = "UNKNOWN") -> dict[str, Any]:
    # Add contract identity fields to defensive copies. Every original raw field
    # remains byte-for-value intact; source_findings never aliases caller objects.
    source_findings: list[dict[str, Any]] = []
    duplicates: dict[str, int] = defaultdict(int)
    for original in findings:
        item = dict(original)
        digest = hashlib.sha256(_canonical(original)).hexdigest()
        ordinal = duplicates[digest]
        duplicates[digest] += 1
        entity_type, entity_id = _entity(original)
        # Normalize contract fields even when a producer emitted null, blank,
        # or an unsupported entity label; retain every unrelated raw field.
        item["raw_finding_id"] = str(item.get("raw_finding_id") or f"finding-v1:{digest}:{ordinal}")
        item["rule_id"] = str(item.get("rule_id") or "UNKNOWN_RULE")
        item["stage"] = str(item.get("stage") or original.get("origin") or "UNKNOWN")
        item["source_file"] = str(item.get("source_file") or original.get("file") or original.get("table") or "UNKNOWN")
        item["technical_status"] = str(item.get("technical_status") or original.get("status") or "UNKNOWN")
        item["entity_type"] = entity_type if entity_type in VALID_ENTITIES else "feed"
        item["entity_id"] = str(item.get("entity_id") or entity_id)
        source_findings.append(item)
    findings = source_findings
    populations: dict[str, int | None] = {}
    relationships: dict[str, dict[str, set[str]]] = {}
    if zip_path:
        populations, relationships = load_population_and_relationships(zip_path)
    g07, g07_metrics = classify_findings(findings, zip_path)
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        entity_type, entity_id = _entity(finding)
        rule = str(finding.get("rule_id") or "UNKNOWN_RULE")
        known = (bool(finding.get("rule_id")) and finding.get("origin") in
                 {"AUDIT_ENGINE", "AUDIT_ENGINE_RECOMMENDATION", "COMPLIANCE", "LEGACY"})
        supplied_pattern = finding.get("pattern_id")
        recognized_patterns = {"EXACT_DUPLICATE_GEOMETRY", "QUANTIZATION_COMPATIBLE", "DISTANCE_DECREASE", "MIXED_PATTERN", "UNKNOWN_PATTERN"}
        pattern_id = (_pattern_assignment(finding, g07) if rule == G07_RULE else
                      supplied_pattern if supplied_pattern in recognized_patterns else
                      "TECHNICAL_FINDING" if known else "UNKNOWN_PATTERN")
        stage = str(finding.get("stage") or finding.get("origin") or "UNKNOWN")
        source_file = str(finding.get("source_file") or finding.get("file") or finding.get("table") or "UNKNOWN")
        technical_status = str(finding.get("technical_status") or finding.get("status") or "UNKNOWN")
        grouped[(rule, stage, source_file, technical_status, pattern_id, entity_type)].append(finding)

    families = []
    total_unclassified = 0
    for dimensions_tuple, rows in sorted(grouped.items()):
        rule, stage, source_file, technical_status, pattern_id, entity_type = dimensions_tuple
        entity_ids = {_entity(item)[1] for item in rows}
        unknown = pattern_id == "UNKNOWN_PATTERN"
        unclassified = len(rows) if unknown else 0
        total_unclassified += unclassified
        pattern_status = "UNKNOWN_PATTERN" if unknown else "CONFIRMED_PATTERN" if pattern_id in {"EXACT_DUPLICATE_GEOMETRY", "DISTANCE_DECREASE", "TECHNICAL_FINDING"} else "COMPATIBLE_PATTERN"
        population = populations.get(entity_type)
        pct = round(len(entity_ids) * 100 / population, 8) if population and len(entity_ids) <= population else None
        propagated = propagated_counts(entity_type, entity_ids, relationships)
        impact = {"direct_affected": {"entity_type": entity_type, "entity_count": len(entity_ids)},
                  "propagated_usage": [{"entity_type": key, "entity_count": len(values)} for key, values in sorted(propagated.items())]}
        family_id = _family_id({"rule_id": rule, "stage": stage, "source_file": source_file,
                                "technical_status": technical_status, "pattern_id": pattern_id,
                                "affected_entity_type": entity_type})
        raw_ids = [str(item.get("raw_finding_id") or hashlib.sha256(_canonical(item)).hexdigest()) for item in rows]
        family = {"family_id": family_id, "rule_id": rule, "stage": stage, "source_file": source_file,
                  "technical_status": technical_status, "raw_occurrence_count": len(rows),
                  "affected_entity_type": entity_type, "affected_entity_count": len(entity_ids),
                  "population": {"population_type": entity_type, "population_count": population},
                  "affected_percentage": pct, "observations": [{"kind": "OBSERVED", "statement": f"{len(rows)} findings de origen en el grupo técnico."}],
                  "calculations": [{"kind": "CALCULATED", "statement": f"{len(entity_ids)} entidades directas únicas."}],
                  "inferences": [], "patterns": [{"pattern_id": pattern_id, "status": pattern_status,
                      "occurrence_count": len(rows) - unclassified,
                      "classification": "UNCLASSIFIED" if unknown else pattern_id}],
                  "unclassified_occurrences": unclassified, "operational_impact": impact,
                  "probable_explanations": [], "confidence_basis": None,
                  "remediation_assessment": "NOT_EVALUABLE",
                  "evidence_refs": [{"raw_finding_ids": raw_ids, "source_file": source_file,
                      "row_entity_refs": {"entity_ids": sorted(entity_ids)},
                      "dataset_sha256": dataset_identity["sha256"], "audit_execution_id": audit_execution_id}],
                  "limitations": []}
        if pattern_id == "QUANTIZATION_COMPATIBLE":
            family["inferences"].append({"kind": "INFERRED", "statement": "Distancia declarada igual con coordenadas distintas es compatible con cuantización; no demuestra su causa."})
        if pattern_id == "UNKNOWN_PATTERN":
            family["limitations"].append("No existe un intérprete especializado aplicable; occurrences permanecen sin clasificar.")
        families.append(family)

    raw_count = len(findings)
    consolidated = sum(f["raw_occurrence_count"] - f["unclassified_occurrences"] for f in families)
    gap = raw_count - consolidated - total_unclassified
    g07_families = [f for f in families if f["rule_id"] == G07_RULE]
    if g07_families and g07_metrics["transition_count"]:
        statement = "; ".join(f"{name}={count}" for name, count in g07_metrics["equal_coordinate_movement_buckets_m"].items())
        for family in g07_families:
            transition_pct = round(family["raw_occurrence_count"] * 100 / g07_metrics["transition_count"], 8)
            family["calculations"].append({"kind": "CALCULATED", "statement": f"G07 total_shapes={populations.get('shape') if populations.get('shape') is not None else 'NOT_EVALUABLE'}; affected_shapes={family['affected_entity_count']}; total_transitions={g07_metrics['transition_count']}; affected_transitions={family['raw_occurrence_count']}; affected_transition_percentage={transition_pct}; increase={g07_metrics['increase_count']}; equal={g07_metrics['equal_count']}; decrease={g07_metrics['decrease_count']}; movimiento geográfico por bucket (m): {statement}; precisión shape_dist_traveled={g07_metrics['distance_precision']}."})
            family["limitations"].append("Las métricas G07 se calculan sobre findings G07 y el shapes.txt del mismo SOURCE; el análisis no determina causalidad.")
    result = {"contract_version": VERSION, "interpretation_status": "COMPLETE" if gap == 0 else "INCOMPLETE",
              "dataset_identity": {"dataset_id": str(dataset_identity["dataset_id"]), "sha256": str(dataset_identity["sha256"])},
              "execution_identity": {"audit_execution_id": audit_execution_id, "engine_version": engine_version,
                                     "interpretation_version": VERSION},
              "source_findings": findings, "finding_families": families,
              "coverage": {"raw_finding_count": raw_count, "consolidated_occurrence_count": consolidated,
                           "unclassified_occurrence_count": total_unclassified, "accounting_gap": gap},
              "limitations": ["Interpretación técnica; no determina cumplimiento jurídico.",
                              "Las poblaciones ausentes o no fiables no producen porcentaje evaluable."],
              "provenance": {"schema_version": VERSION,
                  "deterministic_family_id_basis": f"family-v1 + base64url(canonical UTF-8 JSON semantic dimensions); injective encoding, no timestamps or random IDs; tdl_ref={tdl_ref}.",
                  "raw_findings_immutable": True}}
    validate_result(result)
    return result
