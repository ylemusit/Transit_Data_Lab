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
        raise SystemExit("Pinned NeTEx schema snapshot does not match its SHA-256 manifest")
    print(f"schema_snapshot=PASS dependencies={actual['dependency_count']} commit={actual['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
