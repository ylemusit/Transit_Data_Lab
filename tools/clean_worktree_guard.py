"""Guard for authoritative gate and release orchestration only."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    try:
        root = Path(git("rev-parse", "--show-toplevel"))
        head = git("rev-parse", "HEAD")
        base = git("rev-parse", args.base + "^{commit}")
        clean = not git("status", "--porcelain")
        isolated = (root / ".git").is_file()
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", base, head]).returncode == 0
        result = {"status": "PASS" if clean and isolated and ancestor else "FAIL",
                  "head": head, "base": base, "clean": clean, "isolated": isolated, "base_is_ancestor": ancestor}
    except (OSError, subprocess.CalledProcessError) as exc:
        result = {"status": "FAIL", "error": str(exc)}
    print(json.dumps(result))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
