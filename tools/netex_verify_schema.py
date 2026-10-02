from __future__ import annotations

import argparse
import json
from pathlib import Path

from netex_schema_manifest import build_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream_checkout", type=Path)
    parser.add_argument("--manifest", type=Path, default=Path("01_Research_Standards/NeTEx/schemas/v2.0.0/schema_manifest.json"))
    args = parser.parse_args()
    expected = json.loads(args.manifest.read_text(encoding="utf-8"))
    actual = build_manifest(args.upstream_checkout)
    if actual != expected:
        actual_dependencies = {item["path"]: item for item in actual["dependencies"]}
        expected_dependencies = {item["path"]: item for item in expected.get("dependencies", [])}
        missing = sorted(set(expected_dependencies) - set(actual_dependencies))
        extra = sorted(set(actual_dependencies) - set(expected_dependencies))
        changed = [name for name in sorted(set(actual_dependencies) & set(expected_dependencies))
                   if actual_dependencies[name] != expected_dependencies[name]]
        raise SystemExit(
            "Pinned NeTEx schema snapshot does not match its SHA-256 manifest; "
            f"missing={missing[:3]} extra={extra[:3]} changed={changed[:3]} "
            f"root_expected={expected.get('root_schema_sha256')} root_actual={actual.get('root_schema_sha256')} "
            f"top_level_differences={[(key, expected.get(key), actual.get(key)) for key in sorted(set(expected) | set(actual)) if key != 'dependencies' and expected.get(key) != actual.get(key)]}"
        )
    print(f"schema_snapshot=PASS dependencies={actual['dependency_count']} commit={actual['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
