"""Explicit, read-only preflight for protected external files.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

STATUSES = {"RESOURCE_READY", "RESOURCE_NOT_FOUND", "RESOURCE_HASH_MISMATCH",
            "RESOURCE_WAL_PRESENT", "RESOURCE_NOT_READABLE", "RESOURCE_CONFIGURATION_INVALID"}


def check_resource(spec: dict) -> dict:
    name = spec.get("name") if isinstance(spec, dict) else None
    result = {"name": name, "status": "RESOURCE_CONFIGURATION_INVALID"}
    if not isinstance(spec, dict) or not isinstance(name, str) or not name:
        return result
    path, expected, kind = spec.get("path"), spec.get("sha256"), spec.get("kind", "file")
    if not isinstance(path, str) or not Path(path).is_absolute() or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected) or kind not in ("file", "duckdb"):
        return result
    target = Path(path)
    result["path"] = str(target)
    if not target.is_file():
        result["status"] = "RESOURCE_NOT_FOUND"
        return result
    if kind == "duckdb" and any(Path(str(target) + suffix).exists() for suffix in (".wal", "-wal")):
        result["status"] = "RESOURCE_WAL_PRESENT"
        return result
    try:
        digest = hashlib.sha256()
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        result["sha256"] = digest.hexdigest()
        if digest.hexdigest().lower() != expected.lower():
            result["status"] = "RESOURCE_HASH_MISMATCH"
            return result
        if kind == "duckdb":
            probe = subprocess.run(["duckdb", "-readonly", str(target), "-c", "SELECT 1"],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
            if probe.returncode:
                raise OSError(probe.stderr[-300:])
    except (OSError, subprocess.SubprocessError) as exc:
        result["status"] = "RESOURCE_NOT_READABLE"
        result["error"] = type(exc).__name__
        return result
    result["status"] = "RESOURCE_READY"
    return result


def check_config(config: dict) -> dict:
    if not isinstance(config, dict) or not isinstance(config.get("resources"), list):
        return {"status": "RESOURCE_CONFIGURATION_INVALID", "resources": []}
    rows = [check_resource(spec) for spec in config["resources"]]
    names = [row["name"] for row in rows]
    if not rows or any(not isinstance(name, str) or not name for name in names) or len(names) != len(set(names)):
        return {"status": "RESOURCE_CONFIGURATION_INVALID", "resources": rows}
    return {"status": "RESOURCE_READY" if all(row["status"] == "RESOURCE_READY" for row in rows) else "RESOURCE_ERROR", "resources": rows}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "RESOURCE_CONFIGURATION_INVALID", "error": str(exc)}))
        return 3
    result = check_config(config)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "RESOURCE_READY" else 3 if result["status"] == "RESOURCE_CONFIGURATION_INVALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
