from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("01_Research_Standards/NeTEx")
REQUIREMENTS = [
    {
        "requirement_id": "NETEX-REQ-XML-01", "source_id": "TDL-TECH-01", "authority_level": "L4",
        "citation": "XML 1.0 well-formedness is an intake precondition for the V1 audit runtime",
        "normative_strength": "INFORMATIVE", "scope": "all input XML members",
        "applicability": "ALWAYS", "concepts": ["PublicationDelivery"],
        "condition": "The member parses as XML without DTD/entity declarations",
        "machine_interpretation_status": "MACHINE_EVALUABLE", "notes": "Runtime security/technical precondition, not EPIP or legal compliance.",
    },
    {
        "requirement_id": "NETEX-REQ-REG-01", "source_id": "N02-21", "authority_level": "L1",
        "citation": "Reglamento Delegado (UE) 2017/1926, art. 4(1)(a), (b), texto consolidado 2024-03-04, modificado por 2024/490",
        "normative_strength": "MUST", "scope": "format selection for Annex 1 data by transport mode",
        "applicability": "HUMAN_REVIEW_REQUIRED for regular scheduled bus; road/other-mode category mapping unresolved",
        "concepts": [],
        "condition": "Article 4(1)(a) assigns road transport to a format referenced through Delegated Regulation (EU) 2015/962; Article 4(1)(b) lists NeTEx for other modes. Regulation 2015/962 was repealed from 2025-01-01 by 2022/670.",
        "machine_interpretation_status": "HUMAN_REVIEW_REQUIRED", "notes": "No NeTEx regulatory obligation is inferred for the bus scope. Resolve category applicability and the stale cross-reference through legal review; the runtime is a technical NeTEx evaluator only.",
        "related_source_ids": ["N02-34"],
    },
    {
        "requirement_id": "NETEX-REQ-REG-02", "source_id": "N02-21", "authority_level": "L1",
        "citation": "Reglamento Delegado (UE) 2017/1926, art. 4(2), texto consolidado 2024-03-04",
        "normative_strength": "MUST", "scope": "aplicable categories represented using NeTEx/DATEX II",
        "applicability": "CONDITIONAL; exact Annex 1 categories remain explicit",
        "concepts": [],
        "condition": "Applicable data is to be represented through EU minimum profiles or national profiles",
        "machine_interpretation_status": "HUMAN_REVIEW_REQUIRED", "notes": "This provision does not itself identify EPIP 2026 by name. Whether the listed categories are NeTEx-applicable for the approved bus scope requires review.",
    },
    {
        "requirement_id": "NETEX-REQ-REG-03", "source_id": "N02-21", "authority_level": "L1",
        "citation": "Reglamento Delegado (UE) 2017/1926, art. 4(1)(b), texto consolidado 2024-03-04",
        "normative_strength": "MUST", "scope": "other transport modes, excluding the approved regular scheduled bus scope",
        "applicability": "OUT_OF_SCOPE for this engine",
        "concepts": [],
        "condition": "Other-mode data use one of the specified standards or a proven fully compatible/interoperable machine-readable format; NeTEx CEN/TS 16614 is listed",
        "machine_interpretation_status": "OUT_OF_SCOPE", "notes": "This clause must not be applied to road transport by inference.",
    },
    {
        "requirement_id": "NETEX-REQ-XSD-01", "source_id": "N02-28", "authority_level": "L4",
        "citation": "Pinned upstream v2.0.0 README, production root schema, verified at commit a94e5e1752bcc13aabb8a1f3d018dc08e6978f42",
        "normative_strength": "INFORMATIVE", "scope": "technical audit contract for this V1 build",
        "applicability": "when XSD validation is evaluated",
        "concepts": ["PublicationDelivery", "CompositeFrame", "GeneralFrame"],
        "condition": "Validate with xsd/NeTEx_publication.xsd from the pinned release",
        "machine_interpretation_status": "MACHINE_EVALUABLE", "notes": "Technical baseline choice, not legal or EPIP conformance.",
    },
    {
        "requirement_id": "NETEX-REQ-EPIP-UNKNOWN", "source_id": "N02-26", "authority_level": "L2",
        "citation": "CEN/TS 16614-4:2026; full controlled text not present; public preview is incomplete",
        "normative_strength": "UNKNOWN", "scope": "EPIP constraints for regular scheduled bus",
        "applicability": "UNKNOWN until the full profile is reviewed",
        "concepts": ["StopPlace", "Quay", "Line", "JourneyPattern", "ServiceJourney", "DayType", "OperatingPeriod"],
        "condition": "Requirement assertions and conditions are not inferred from examples or preview snippets",
        "machine_interpretation_status": "UNKNOWN", "notes": "Do not convert this gap to PASS or FAIL.",
    },
    {
        "requirement_id": "NETEX-REQ-NAP-UNKNOWN", "source_id": "N02-20", "authority_level": "L3",
        "citation": "MITRAMS NAP public guidance reviewed on 2026-10-02",
        "normative_strength": "UNKNOWN", "scope": "NAP Spain technical acceptance",
        "applicability": "UNKNOWN; no public technical acceptance contract identified",
        "concepts": ["PublicationDelivery"], "condition": "No technical assertion defined",
        "machine_interpretation_status": "UNKNOWN", "notes": "No contact or authenticated resource access performed.",
    },
]

CONCEPTS = [
    ("PublicationDelivery", "netex_publication.xsd", "DIRECT_XSD"),
    ("CompositeFrame", "netex_framework/netex_frames/netex_compositeFrame_version.xsd", "DIRECT_XSD"),
    ("GeneralFrame", "netex_framework/netex_frames/netex_generalFrame_version.xsd", "DIRECT_XSD"),
    ("Authority", "netex_framework/netex_reusableComponents/netex_transportOrganisation_version.xsd", "DIRECT_XSD"),
    ("Operator", "netex_framework/netex_reusableComponents/netex_transportOrganisation_version.xsd", "DIRECT_XSD"),
    ("StopPlace", "netex_part_1/part1_ifopt/netex_ifopt_stopPlace_version.xsd", "DIRECT_XSD"),
    ("Quay", "netex_part_1/part1_ifopt/netex_ifopt_stopPlace_version.xsd", "DIRECT_XSD"),
    ("ScheduledStopPoint", "netex_part_1/part1_tacticalPlanning/netex_servicePattern_version.xsd", "DIRECT_XSD"),
    ("Line", "netex_part_1/part1_networkDescription/netex_line_version.xsd", "DIRECT_XSD"),
    ("Route", "netex_part_1/part1_networkDescription/netex_route_version.xsd", "DIRECT_XSD"),
    ("RoutePoint", "netex_part_1/part1_networkDescription/netex_route_version.xsd", "DIRECT_XSD"),
    ("JourneyPattern", "netex_part_1/part1_tacticalPlanning/netex_journeyPattern_version.xsd", "DIRECT_XSD"),
    ("ServiceJourney", "netex_part_2/part2_journeyTimes/netex_serviceJourney_version.xsd", "DIRECT_XSD"),
    ("PassingTime", "netex_part_2/part2_journeyTimes/netex_passingTimes_version.xsd", "DIRECT_XSD"),
    ("DayType", "netex_framework/netex_reusableComponents/netex_dayType_version.xsd", "DIRECT_XSD"),
    ("OperatingPeriod", "netex_framework/netex_reusableComponents/netex_serviceCalendar_version.xsd", "DIRECT_XSD"),
    ("DestinationDisplay", "netex_part_1/part1_networkDescription/netex_line_version.xsd", "DIRECT_XSD"),
    ("VehicleMode", "netex_framework/netex_reusableComponents/netex_mode_support.xsd", "DIRECT_XSD"),
    ("TransportSubmode", "netex_framework/netex_reusableComponents/netex_submode_version.xsd", "DIRECT_XSD"),
    ("PassengerStopAssignment", "netex_part_1/part1_tacticalPlanning/netex_stopAssignment_version.xsd", "DIRECT_XSD"),
    ("TariffZone", "netex_framework/netex_genericFramework/netex_zone_version.xsd", "DIRECT_XSD"),
    ("BasicGeometry", "gml/geometryBasic0d1d-extract-v3_2_1.xsd", "DIRECT_XSD"),
    ("VersionFrameRelationships", "netex_framework/netex_frames/", "CROSS_REFERENCE"),
    ("LocalReferences", "NeTEx object reference attributes", "CROSS_REFERENCE"),
]


def build() -> tuple[dict, dict]:
    requirement_doc = {"catalog_version": "1.0.0", "scope": "Spain / regular scheduled bus / static scheduled passenger information",
                       "requirements": REQUIREMENTS, "fabricated_requirements": 0}
    concepts = [{"concept_id": f"NETEX-CONCEPT-{index:02d}", "name": name, "xsd_path": path,
                 "xml_locator_template": f"/netex:PublicationDelivery/netex:dataObjects//netex:{name}",
                 "evaluation_class": evaluation, "representation_status": "REPRESENTABLE_IN_PINNED_MODEL",
                 "evaluation_status": "MACHINE_EVALUABLE" if evaluation == "DIRECT_XSD" else "NOT_EVALUABLE",
                 "evidence_required": "XSD validation result plus source hash",
                 "uncertainty": "Element presence does not assert EPIP applicability or semantic correctness."}
                for index, (name, path, evaluation) in enumerate(CONCEPTS, 1)]
    concept_doc = {"catalog_version": "1.0.0", "scope": requirement_doc["scope"], "concepts": concepts,
                   "known_limits": ["The complete EPIP 2026 text is not available in the corpus.",
                                    "Cross-reference semantics are inventoried but not asserted without a normative target mapping."]}
    matrix = []
    for concept in concepts:
        matrix.append({
            "requirement_ids": [req["requirement_id"] for req in REQUIREMENTS if concept["name"] in req["concepts"]],
            "concept_id": concept["concept_id"], "concept": concept["name"],
            "xml_representation": concept["xml_locator_template"], "schema_path": concept["xsd_path"],
            "xpath_or_locator": concept["xml_locator_template"], "evaluation_class": concept["evaluation_class"],
            "representability": concept["representation_status"], "evaluation_status": concept["evaluation_status"],
            "evidence_required": concept["evidence_required"], "uncertainty": concept["uncertainty"],
        })
    matrix.append({"requirement_ids": ["NETEX-REQ-EPIP-UNKNOWN"], "concept_id": "NETEX-EPIP-ASSERTIONS",
                   "concept": "Profile-specific constraints", "xml_representation": "varies by requirement",
                   "schema_path": "EPIP assertion set not mapped", "xpath_or_locator": None,
                   "evaluation_class": "PROFILE_CONSTRAINT", "representability": "UNKNOWN",
                   "evaluation_status": "HUMAN_REVIEW_REQUIRED", "evidence_required": "controlled normative text and reviewed requirement-to-schema mapping",
                   "uncertainty": "Full text not present; do not infer from examples."})
    matrix.append({"requirement_ids": ["NETEX-REQ-NAP-UNKNOWN"], "concept_id": "NETEX-NAP-ACCEPTANCE",
                   "concept": "NAP acceptance", "xml_representation": None, "schema_path": None, "xpath_or_locator": None,
                   "evaluation_class": "REGULATORY_ALIGNMENT", "representability": "UNKNOWN",
                   "evaluation_status": "NOT_EVALUABLE", "evidence_required": "published technical acceptance contract",
                   "uncertainty": "No public contract identified; not a claim of nonexistence."})
    matrix.append({"requirement_ids": ["NETEX-REQ-REG-01", "NETEX-REQ-REG-02"],
                   "concept_id": "NETEX-ROAD-REGULATORY-MAPPING", "concept": "Road transport applicability and format alignment",
                   "xml_representation": None, "schema_path": None, "xpath_or_locator": None,
                   "evaluation_class": "REGULATORY_ALIGNMENT", "representability": "UNKNOWN",
                   "evaluation_status": "HUMAN_REVIEW_REQUIRED", "evidence_required": "legal category mapping and current cross-reference analysis",
                   "uncertainty": "Article 4(1)(a) points to repealed Regulation 2015/962; do not infer NeTEx from Article 4(1)(b)."})
    matrix_doc = {"matrix_version": "1.0.0", "scope": requirement_doc["scope"], "rows": matrix,
                  "unknowns_explicit": True, "not_representable_count": 0}
    return requirement_doc, concept_doc, matrix_doc


if __name__ == "__main__":
    req, concepts, matrix = build()
    for name, content in (("N03_REQUIREMENTS_20261002.json", req), ("N03_CONCEPTS_20261002.json", concepts),
                          ("N04_REPRESENTABILITY_20261002.json", matrix)):
        (ROOT / name).write_text(json.dumps(content, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
