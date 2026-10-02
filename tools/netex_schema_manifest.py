from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


PINNED_COMMIT = "a94e5e1752bcc13aabb8a1f3d018dc08e6978f42"
EXPECTED_ROOT = "xsd/NeTEx_publication.xsd"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(schema_root: Path) -> dict:
    git_root = schema_root.resolve(strict=True)
    commit = subprocess.run(
        ["git", "-C", str(git_root), "rev-parse", "HEAD"], check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if commit != PINNED_COMMIT:
        raise ValueError(f"Schema source commit mismatch: {commit}")
    xsd_root = git_root / "xsd"
    files = [
        {"path": path.relative_to(git_root).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in sorted(xsd_root.rglob("*.xsd"))
    ]
    root = next(item for item in files if item["path"] == EXPECTED_ROOT)
    return {
        "manifest_version": "1.0.0",
        "source": "https://github.com/TransmodelEcosystem/NeTEx",
        "release": "v2.0.0",
        "commit": commit,
        "root_schema": EXPECTED_ROOT,
        "root_schema_sha256": root["sha256"],
        "dependency_count": len(files),
        "dependencies": files,
        "distribution_note": "XSD bytes are not included in this repository pending review of GPL-3.0 and CEN/Crown Copyright notices.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema_root", type=Path, help="root of pinned upstream checkout")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_manifest(args.schema_root)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
