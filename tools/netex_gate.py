from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("02_Data_Engineering/NeTEx_Lab").resolve()))
from netex_lab.rules import RULES, validate_registry  # noqa: E402


NETEX = Path("01_Research_Standards/NeTEx")


def read(name: str) -> dict:
    return json.loads((NETEX / name).read_text(encoding="utf-8"))


def main() -> int:
    sources = read("N02_SOURCE_MANIFEST_20261002.json")
    requirements = read("N03_REQUIREMENTS_20261002.json")
    concepts = read("N03_CONCEPTS_20261002.json")
    matrix = read("N04_REPRESENTABILITY_20261002.json")
    schema = read("schemas/v2.0.0/schema_manifest.json")
    registry_path = Path("02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    corpus_path = Path("02_Data_Engineering/NeTEx_Lab/tests/fixtures/corpus_manifest.json")
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    validate_registry()
    assert len(sources["sources"]) == 34
    assert len({item["source_id"] for item in sources["sources"]}) == 34
    source_ids = {item["source_id"] for item in sources["sources"]}
    required_source_fields = {"source_id", "title", "authority_level", "publisher", "version", "date", "status",
                              "url", "hash_if_local", "scope", "normative_or_informative", "machine_readable", "notes", "classification"}
    assert all(required_source_fields.issubset(item) for item in sources["sources"])
    assert all(item["classification"] in {"AUTHORITATIVE", "SUPPORTING", "IMPLEMENTATION_REFERENCE", "HISTORICAL", "DEFERRED"}
               for item in sources["sources"])
    assert schema["release"] == "v2.0.0" and schema["commit"] == "a94e5e1752bcc13aabb8a1f3d018dc08e6978f42"
    assert schema["dependency_count"] == len(schema["dependencies"]) == 458
    assert requirements["fabricated_requirements"] == 0
    requirement_ids = {item["requirement_id"] for item in requirements["requirements"]}
    assert all(item["source_id"] in source_ids or item["source_id"] == "TDL-TECH-01"
               for item in requirements["requirements"])
    assert all(set(item.get("related_source_ids", [])) <= source_ids for item in requirements["requirements"])
    assert all(rule["requirement_id"] is None or rule["requirement_id"] in requirement_ids for rule in RULES)
    assert sorted(RULES, key=lambda item: item["rule_id"]) == registry["rules"]
    assert len(concepts["concepts"]) == 24 and len(matrix["rows"]) == 27
    assert matrix["unknowns_explicit"] and corpus["holdout_accessed"] is False
    assert all(row["evaluation_status"] in {"MACHINE_EVALUABLE", "HUMAN_REVIEW_REQUIRED", "NOT_EVALUABLE", "NOT_APPLICABLE", "UNKNOWN"}
               for row in matrix["rows"])
    for case in corpus["cases"]:
        path = Path("02_Data_Engineering/NeTEx_Lab") / case["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == case["sha256"], case["case_id"]
    print("netex_documentation_and_traceability=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
