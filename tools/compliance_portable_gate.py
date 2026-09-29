"""Portable legal-source and read-only Compliance phase gate.

Historical SQL is read unchanged; its machine-specific legal hash clauses are
replaced in memory after independent byte verification against this checkout.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from protected_resource_preflight import check_resource

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "03_Compliance/legal_sources_portable_v1.json"
SQL = ROOT / "03_Compliance/sql/07_tests/phase_2/test_phase_2_post_materialization_gate.sql"


def sources(root: Path) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    historical = []
    for identity, absolute, digest in re.findall(
        r"SELECT 'LEGAL_HASH_([^']+)'.*?read_blob\('([^']+)'\).*?sha256\(content\)='([0-9a-f]{64})'",
        SQL.read_text(encoding="utf-8-sig"), re.S,
    ):
        if "/03_Compliance/" not in absolute:
            return {"status": "CONFIGURATION_ERROR", "reason": "historical legal path is unexpected"}
        historical.append({"identity": identity, "path": "03_Compliance/" + absolute.split("/03_Compliance/", 1)[1], "sha256": digest})
    if historical != manifest.get("sources"):
        return {"status": "CONFIGURATION_ERROR", "reason": "portable manifest differs from historical legal identities"}
    rows = []
    for spec in manifest["sources"]:
        relative = Path(spec["path"])
        if relative.is_absolute() or ".." in relative.parts or not spec.get("identity"):
            return {"status": "CONFIGURATION_ERROR", "sources": rows}
        path = root / relative
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError:
            return {"status": "CONFIGURATION_ERROR", "reason": "legal source escapes configured root", "sources": rows}
        row = check_resource({"name": spec["identity"], "path": str(path.resolve()), "sha256": spec["sha256"]})
        row["relative_path"] = spec["path"]
        rows.append(row)
    return {"status": "PASS" if len(rows) == 10 and all(row["status"] == "RESOURCE_READY" for row in rows) else "RESOURCE_ERROR", "sources": rows}


def portable_sql() -> str:
    sql = SQL.read_text(encoding="utf-8-sig")
    pattern = r"\nUNION ALL\nSELECT 'LEGAL_HASH_[^\n]+"
    rewritten, count = re.subn(pattern, "", sql)
    if count != 10:
        raise ValueError(f"expected 10 historical legal SQL clauses, found {count}")
    return rewritten


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legal-root", type=Path, required=True)
    parser.add_argument("--allow-external-legal-root", action="store_true")
    parser.add_argument("--db", type=Path)
    parser.add_argument("--db-sha256")
    parser.add_argument("--gtfs-db", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--phase-only", action="store_true")
    parser.add_argument("--sources-only", action="store_true")
    args = parser.parse_args()
    if not args.legal_root.is_dir() or (not args.sources_only and (args.db is None or not args.db_sha256)) or (not args.sources_only and not args.phase_only and (args.gtfs_db is None or args.evidence is None)):
        print(json.dumps({"status": "CONFIGURATION_ERROR", "reason": "legal root or DB configuration unavailable"}))
        return 3
    if args.legal_root.resolve() != ROOT.resolve() and not args.allow_external_legal_root:
        print(json.dumps({"status": "CONFIGURATION_ERROR", "reason": "legal root is a different checkout; pass --allow-external-legal-root explicitly"}))
        return 3
    try:
        legal = sources(args.legal_root.resolve())
        if legal["status"] != "PASS":
            print(json.dumps(legal, ensure_ascii=False, indent=2))
            return 2 if legal["status"] == "RESOURCE_ERROR" else 3
        if args.sources_only:
            print(json.dumps({"status": "PASS", "scope": "LEGAL_SOURCES_ONLY", **legal}, ensure_ascii=False))
            return 0
        db = check_resource({"name": "compliance_db", "path": str(args.db.resolve()), "sha256": args.db_sha256, "kind": "duckdb"})
        if db["status"] != "RESOURCE_READY":
            print(json.dumps({"status": "RESOURCE_ERROR", "database": db}, ensure_ascii=False))
            return 2
        if not args.phase_only:
            command = [sys.executable, str(ROOT / "tools/compliance_v1_current_gate.py"), "--evidence", str(args.evidence),
                       "--portable", "--legal-root", str(args.legal_root.resolve()), "--db", str(args.db.resolve()),
                       "--gtfs-db", str(args.gtfs_db.resolve())]
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            summary_path = args.evidence.resolve() / "summary.json"
            if summary_path.is_file():
                print(summary_path.read_text(encoding="utf-8"))
            else:
                print(json.dumps({"status": "FAIL_TECHNICAL", "error": completed.stderr[-1000:]}))
            return 0 if completed.returncode == 0 else 2
        before = db["sha256"]
        checks = {}
        for phase, sql_path in (("phase1", ROOT / "03_Compliance/sql/07_tests/phase_1/test_phase_1_invariants.sql"), ("phase2", SQL)):
            sql = portable_sql() if phase == "phase2" else sql_path.read_text(encoding="utf-8-sig")
            run = subprocess.run(["duckdb", "-batch", "-bail", "-json", "-readonly", str(args.db.resolve())], input=sql, text=True, capture_output=True, cwd=ROOT, encoding="utf-8", errors="replace")
            if run.returncode:
                raise RuntimeError(f"{phase}: {run.stderr[-800:]}")
            decoder = json.JSONDecoder()
            output = run.stdout.strip()
            rows = []
            while output:
                block, end = decoder.raw_decode(output)
                rows.extend(row for row in block if isinstance(row, dict) and "test" in row and "status" in row)
                output = output[end:].strip()
            failures = [row for row in rows if row.get("status") != "PASS"]
            allowed = [{"test": "UNCHANGED_COUNT_audit.rules", "status": "FAIL", "expected": 0, "actual": 2}] if phase == "phase2" else []
            if len(rows) != (22 if phase == "phase1" else 377) or failures != allowed:
                raise RuntimeError(f"{phase}: count or invariant failure: {failures[:3]}")
            checks[phase] = {"checks": len(rows), "historical_exception": allowed}
        after = hashlib.sha256(args.db.read_bytes()).hexdigest()
        if before.lower() != after:
            raise RuntimeError("READONLY_DRIFT")
        print(json.dumps({"status": "PASS", "scope": "PORTABLE_PHASE_1_2_AND_LEGAL_SOURCES", "checks": checks, "database_sha256": after}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "FAIL_TECHNICAL", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
