"""Read-only inspection of parent documentation and explicitly protected files.

Does not traverse nested repositories, datasets, environments or backups.
Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = [
    "PROJECT_CURRENT_STATE.md", "project_baseline.json",
    "07_Business/02_Capabilities/CAPABILITY_REGISTER.md",
    "07_Business/02_Capabilities/EVIDENCE_INDEX.md",
    "07_Business/02_Capabilities/CAPABILITY_GAPS.md",
    "07_Business/02_Capabilities/BUSINESS_CAPABILITY_BASELINE_V1.md",
    "02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb",
    "03_Compliance/databases/transit_compliance.duckdb",
]
NESTED = [
    "06_Products/GTFS Explorer/GTFS Explorer Desktop",
    "06_Products/GTFS Explorer/GTFS Explorer Engineering",
    "06_Products/GTFS Explorer/GTFS Explorer Artifacts",
    "06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02",
]


def command(*args: str, cwd: Path = ROOT) -> dict:
    result = subprocess.run(args, cwd=cwd, capture_output=True)
    return {"exit_code": result.returncode,
            "stdout": result.stdout.decode("utf-8", errors="replace").strip(),
            "stderr": result.stderr.decode("utf-8", errors="replace").strip()}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inspect() -> dict:
    listing = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, check=True,
    )
    paths = sorted(set(p.decode("utf-8") for p in listing.stdout.split(b"\0") if p))
    docs, missing, syntax_errors, text_defects = [], [], [], []
    for name in paths:
        if name.startswith("06_Products/"):
            continue
        path = ROOT / name
        if path.suffix not in {".md", ".py"} or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8-sig")
        if path.suffix == ".py":
            try:
                ast.parse(content, filename=name)
            except SyntaxError as exc:
                syntax_errors.append({"file": name, "line": exc.lineno, "error": exc.msg})
            continue
        historical = ("/reports/" in name or name.startswith("reports/")
                      or "/evidence/" in name or "/03_gtfs_explorer/" in name
                      or name in PROTECTED or name == "PROJECT_SNAPSHOT_V0.1.md"
                      or name in {
                          "02_Data_Engineering/GTFS_Lab/20_clientes_reales/README.md",
                          "02_Data_Engineering/GTFS_Lab/20_clientes_reales/CHANGELOG.md",
                      })
        docs.append({"path": name, "bytes": path.stat().st_size,
                     "classification": "historical_or_frozen" if historical else "documentation",
                     "empty": not content.strip()})
        # Inline Markdown links; anchors and reference-style links are outside this check.
        fence = False
        for number, line in enumerate(content.splitlines(), 1):
            defects = []
            if any(ord(char) < 32 and char != "\t" for char in line):
                defects.append("control_character")
            if "$(System.Collections.Hashtable." in line:
                defects.append("unresolved_metadata_placeholder")
            if re.search(r"Ã.|Â.|â[€†]", line):
                defects.append("possible_encoding_corruption")
            if defects:
                text_defects.append({"file": name, "line": number,
                                     "defects": defects, "historical": historical})
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
            if fence:
                continue
            for match in re.finditer(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)", line):
                target = match.group(1).strip().strip("<>")
                if re.match(r"^[a-zA-Z][\w+.-]*:", target) or target.startswith("#"):
                    continue
                target = unquote(target.split("#", 1)[0])
                if not (path.parent / target).exists():
                    missing.append({"file": name, "line": number, "target": target,
                                    "historical": historical})
    nested = {name: {"head": command("git", "rev-parse", "HEAD", cwd=ROOT / name),
                     "status": command("git", "status", "--porcelain=v1", cwd=ROOT / name)}
              for name in NESTED}
    desktop = ROOT / NESTED[0]
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "parent Markdown and Python; explicit frozen files; nested Git metadata only",
        "root_head": command("git", "rev-parse", "HEAD"),
        "root_tag": command("git", "rev-parse", "tdl-baseline-v0.1^{commit}"),
        "origin": command("git", "remote", "get-url", "origin"),
        "cached_origin_main": command("git", "rev-parse", "origin/main"),
        "merge_base": command("git", "merge-base", "HEAD", "origin/main"),
        "desktop_tag": command("git", "rev-parse", "v0.2.2^{commit}", cwd=desktop),
        "nested": nested,
        "protected_sha256": {name: digest(ROOT / name) for name in PROTECTED},
        "markdown_files": docs,
        "markdown_count": len(docs),
        "markdown_bytes": sum(doc["bytes"] for doc in docs),
        "missing_local_links": missing,
        "python_syntax_errors": syntax_errors,
        "text_defects": text_defects,
        "limitations": ["No nested worktree content inspection or product runtime tests",
                        "No remote fetch, legal interpretation or technical gate rerun",
                        "Link check excludes anchors, reference-style links and external URLs"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    result = inspect()
    if args.compare:
        before = json.loads(args.compare.read_text(encoding="utf-8"))
        result["preservation"] = {
            key: result[key] == before[key]
            for key in ("protected_sha256", "nested", "root_head", "root_tag", "desktop_tag")
        }
    result["verification_ok"] = (
        not result["python_syntax_errors"]
        and not any(not link["historical"] for link in result["missing_local_links"])
        and not any(not defect["historical"] for defect in result["text_defects"])
        and all(result.get("preservation", {}).values())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in
                     ("markdown_count", "markdown_bytes", "missing_local_links",
                      "python_syntax_errors", "verification_ok")}, ensure_ascii=True))
    return 0 if result["verification_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
