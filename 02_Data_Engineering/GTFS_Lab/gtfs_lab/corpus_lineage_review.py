"""Build the M04-A2 lineage evidence matrix from recovered M04-A1 artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ASSESSMENTS = {"SAME_SOURCE_LINEAGE", "LIKELY_SAME_LINEAGE", "NO_LINEAGE_EVIDENCE", "LIKELY_INDEPENDENT_SOURCE", "UNRESOLVED"}
DOMAINS = {"SOURCE_LINEAGE", "NETWORK_STRUCTURE", "IDENTIFIER_COLLISION", "MIXED", "NONE", "UNRESOLVED"}
ALLOWED = {"YES", "NO", "UNRESOLVED"}


def build(provenance: dict[str, Any], relationships: dict[str, Any]) -> dict[str, Any]:
    datasets = {row["dataset_id"]: row for row in provenance["datasets"]}
    pairs = []
    for source in relationships["pairs"]:
        a, b = datasets[source["dataset_a"]], datasets[source["dataset_b"]]
        feed = source["feed_info_comparison"]
        shared_agency_names = source["shared_agency_names"]
        shared_route_names = source["shared_route_short_long_names"]
        shared_stop_names = source["shared_stop_names"]
        shared_trip_ids = source["shared_trip_ids"]
        exact_zip = a["zip_sha256"] == b["zip_sha256"]
        same_source_id = a.get("source_dataset_id") not in (None, "UNKNOWN", "") and a.get("source_dataset_id") == b.get("source_dataset_id")
        same_source_url = a.get("source_url") not in (None, "UNKNOWN", "") and a.get("source_url") == b.get("source_url")
        same_operator = a["operator_declared"].strip().casefold() == b["operator_declared"].strip().casefold()
        same_publisher = feed["publisher_a"] not in ("UNKNOWN", "") and feed["publisher_a"].casefold() == feed["publisher_b"].casefold()
        same_publisher_url = feed["publisher_url_a"] not in ("UNKNOWN", "") and feed["publisher_url_a"].rstrip("/").casefold() == feed["publisher_url_b"].rstrip("/").casefold()
        distinct_operators = a["operator_declared"] not in ("UNKNOWN", "") and b["operator_declared"] not in ("UNKNOWN", "") and not same_operator
        distinct_publishers = feed["publisher_a"] not in ("UNKNOWN", "") and feed["publisher_b"] not in ("UNKNOWN", "") and feed["publisher_a"].casefold() != feed["publisher_b"].casefold()
        distinct_publisher_urls = feed["publisher_url_a"] not in ("UNKNOWN", "") and feed["publisher_url_b"] not in ("UNKNOWN", "") and feed["publisher_url_a"].rstrip("/").casefold() != feed["publisher_url_b"].rstrip("/").casefold()
        source_signals = []
        supporting = []
        network = []
        independence = []
        if exact_zip:
            source_signals.append("IDENTICAL_ZIP_SHA256")
        if same_source_id:
            source_signals.append("SAME_SOURCE_DATASET_ID")
        if same_source_url:
            source_signals.append("SAME_SOURCE_RESOURCE_URL")
        if same_operator and (shared_agency_names or same_publisher or same_publisher_url):
            source_signals.append("SAME_OPERATOR_WITH_IDENTITY_SUPPORT")
        if shared_trip_ids and (shared_route_names or shared_stop_names or source["trip_overlap_ratio"] >= 0.5):
            source_signals.append("SUBSTANTIAL_TRIP_AND_IDENTITY_OVERLAP")
        if shared_trip_ids:
            supporting.append("SHARED_TRIP_IDS")
        if same_publisher:
            supporting.append("SAME_FEED_PUBLISHER")
        if same_publisher_url:
            supporting.append("SAME_PUBLISHER_URL")
        if shared_agency_names:
            supporting.append("SHARED_AGENCY_NAMES")
        if shared_route_names:
            supporting.append("SHARED_ROUTE_NAMES")
        if shared_stop_names:
            supporting.append("SHARED_STOP_NAMES")
        if source["shared_agency_ids"]:
            network.append("SHARED_AGENCY_IDS")
        if source["shared_route_ids"]:
            network.append("SHARED_ROUTE_IDS")
        if source["shared_stop_ids"]:
            network.append("SHARED_STOP_IDS")
        if shared_agency_names:
            network.append("SHARED_AGENCY_IDENTITY")
        if distinct_operators:
            independence.append("DISTINCT_DECLARED_OPERATORS")
        if distinct_publishers:
            independence.append("DISTINCT_FEED_PUBLISHERS")
        if distinct_publisher_urls:
            independence.append("DISTINCT_PUBLISHER_URLS")
        if a["zip_sha256"] != b["zip_sha256"]:
            independence.append("DIFFERENT_ZIP_BYTES")
        if not shared_trip_ids:
            independence.append("NO_SHARED_TRIP_IDS")
        if not shared_route_names:
            independence.append("NO_SHARED_ROUTE_NAME_IDENTITY")
        if not shared_stop_names:
            independence.append("NO_SHARED_STOP_NAME_IDENTITY")

        identifiers_only = bool(network) and not (shared_agency_names or shared_route_names or shared_stop_names or shared_trip_ids)
        shared_identifier_count = sum(len(source[key]) for key in ("shared_agency_ids", "shared_route_ids", "shared_stop_ids"))
        generic_collision = identifiers_only and shared_identifier_count <= 2 and not shared_trip_ids and all(
            (not source["shared_agency_ids"] or set(source["shared_agency_ids"]) <= {"0", "1"})
            and (not source["shared_route_ids"] or all(len(item) <= 2 for item in source["shared_route_ids"]))
            and (not source["shared_stop_ids"] or all(len(item) <= 10 for item in source["shared_stop_ids"]))
            for _ in (0,)
        )
        # Numeric agency ID 1 is generic in this observed corpus; shared stop IDs
        # are network identifiers unless supported by named identity or trip overlap.
        if exact_zip or same_source_id or same_source_url:
            assessment, domain, confidence, allowed = "SAME_SOURCE_LINEAGE", "SOURCE_LINEAGE", "HIGH", "NO"
            reason = "Exact source bytes or a canonical source identifier/resource URL matches."
        elif "SUBSTANTIAL_TRIP_AND_IDENTITY_OVERLAP" in source_signals or (same_operator and (same_publisher or same_publisher_url)):
            assessment, domain, confidence, allowed = "LIKELY_SAME_LINEAGE", "SOURCE_LINEAGE", "HIGH", "NO"
            reason = "A shared operator/source is corroborated by substantial feed identity or trip evidence."
        elif distinct_operators and (distinct_publishers or distinct_publisher_urls) and not shared_trip_ids and not shared_route_names:
            assessment = "LIKELY_INDEPENDENT_SOURCE"
            domain = "NETWORK_STRUCTURE" if source["shared_stop_ids"] or source["shared_route_ids"] else ("IDENTIFIER_COLLISION" if identifiers_only else "NONE")
            confidence, allowed = "HIGH", "YES"
            reason = "Distinct operator identity and publisher resource, different ZIP bytes, and no shared trips or route-name identity; residual stop/route IDs are network structure only."
        elif distinct_operators and not shared_trip_ids and not shared_route_names and not shared_stop_names and (identifiers_only or not network):
            assessment = "LIKELY_INDEPENDENT_SOURCE"
            domain = "IDENTIFIER_COLLISION" if identifiers_only else "NONE"
            confidence, allowed = "MEDIUM", "YES"
            reason = "Distinct declared operators, different ZIP bytes, and no shared trip or named route/stop identity; shared generic IDs do not establish source lineage."
        elif source["shared_trip_ids"] or (shared_route_names and shared_stop_names):
            assessment, domain, confidence, allowed = "UNRESOLVED", "MIXED", "MEDIUM", "UNRESOLVED"
            reason = "Material trip and named route/stop identity overlap could indicate a shared source or derived feed and is not explained by ID reuse alone."
        elif identifiers_only or network:
            assessment = "NO_LINEAGE_EVIDENCE"
            domain = "IDENTIFIER_COLLISION" if generic_collision or source["shared_agency_ids"] or source["shared_route_ids"] else "NETWORK_STRUCTURE"
            confidence, allowed = "MEDIUM", "YES" if distinct_operators and a["zip_sha256"] != b["zip_sha256"] else "UNRESOLVED"
            reason = "Only feed-scoped identifiers or physical/network stop overlap are shared; this is not source lineage."
        else:
            assessment, domain, confidence, allowed = "NO_LINEAGE_EVIDENCE", "NONE", "MEDIUM", "YES" if distinct_operators else "UNRESOLVED"
            reason = "No source-lineage signal is present; distinct declared operator identities and different ZIP bytes support separate source assignments." if allowed == "YES" else "No lineage signal is visible, but positive independence evidence is insufficient."

        pairs.append({
            "pair_id": source["pair_id"], "dataset_a": source["dataset_a"], "dataset_b": source["dataset_b"],
            "lineage_signals": {"strong": source_signals, "supporting": supporting},
            "network_identifier_signals": network,
            "contradictory_independence_signals": independence,
            "shared_network_identifiers": {"agency_ids": source["shared_agency_ids"], "route_ids": source["shared_route_ids"], "stop_ids": source["shared_stop_ids"]},
            "source_identity_differences": {
                "operators": [a["operator_declared"], b["operator_declared"]],
                "publishers": [feed["publisher_a"], feed["publisher_b"]],
                "publisher_urls": [feed["publisher_url_a"], feed["publisher_url_b"]],
                "agency_ids": [[item.get("agency_id", "UNKNOWN") for item in a["agency_identity"]], [item.get("agency_id", "UNKNOWN") for item in b["agency_identity"]]],
                "agency_names": [[item.get("agency_name", "UNKNOWN") for item in a["agency_identity"]], [item.get("agency_name", "UNKNOWN") for item in b["agency_identity"]]],
            },
            "trip_differences": {"shared_trip_ids": shared_trip_ids, "shared_trip_count": len(shared_trip_ids)},
            "route_name_differences": {"shared_route_names": shared_route_names},
            "source_lineage_assessment": assessment, "relationship_domain": domain,
            "confidence": confidence, "can_be_opposite_split_sides": allowed, "reason": reason,
            "generic_id_collision": "GENERIC_ID_COLLISION" if generic_collision else None,
        })
    counts = {value: sum(row["can_be_opposite_split_sides"] == value for row in pairs) for value in sorted(ALLOWED)}
    return {
        "schema_version": "1.0.0", "review": "M04-A2", "pair_count": len(pairs), "pairs": pairs,
        "counts": counts,
        "blocking_pairs": [row["pair_id"] for row in pairs if row["can_be_opposite_split_sides"] != "YES"],
        "policy": {
            "lineage": "same source feed, repeated snapshot, derived feed, same provider/generator with transferable structure-specific adaptation, or explicit operator-specific adaptation can leak between development and holdout.",
            "not_automatically_leakage": "GTFS standards, generic IDs, physical shared stops, and territorially interacting routes do not establish lineage.",
            "system_context": "TDL currently evaluates deterministic rules, not a model trained on examples. Holdout protects against rules designed after inspecting all feeds, operator-specific exceptions, known-dataset heuristics, and false generalization.",
            "split_status": "NOT_CREATED",
        },
    }


def validate(review: dict[str, Any]) -> list[str]:
    errors = []
    if len(review.get("pairs", [])) != 29:
        errors.append("expected 29 reviewed pairs")
    seen = set()
    for row in review.get("pairs", []):
        if row.get("source_lineage_assessment") not in ASSESSMENTS:
            errors.append(f"invalid lineage assessment: {row.get('pair_id')}")
        if row.get("relationship_domain") not in DOMAINS:
            errors.append(f"invalid relationship domain: {row.get('pair_id')}")
        if row.get("can_be_opposite_split_sides") not in ALLOWED:
            errors.append(f"invalid split decision: {row.get('pair_id')}")
        key = tuple(sorted((row.get("dataset_a"), row.get("dataset_b"))))
        if key in seen:
            errors.append(f"duplicate pair: {row.get('pair_id')}")
        seen.add(key)
        if row.get("source_lineage_assessment") == "NO_LINEAGE_EVIDENCE" and row.get("can_be_opposite_split_sides") == "YES" and not row.get("contradictory_independence_signals"):
            errors.append(f"YES lacks positive independence evidence: {row.get('pair_id')}")
        if row.get("source_lineage_assessment") in {"SAME_SOURCE_LINEAGE", "LIKELY_SAME_LINEAGE"} and row.get("can_be_opposite_split_sides") != "NO":
            errors.append(f"lineage not blocked: {row.get('pair_id')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--relationships", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    review = build(json.loads(args.provenance.read_text(encoding="utf-8")), json.loads(args.relationships.read_text(encoding="utf-8")))
    errors = validate(review)
    if errors:
        raise SystemExit("\n".join(errors))
    args.output.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"M04A2_LINEAGE_REVIEW_PASS pairs={review['pair_count']} YES={review['counts']['YES']} NO={review['counts']['NO']} UNRESOLVED={review['counts']['UNRESOLVED']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
