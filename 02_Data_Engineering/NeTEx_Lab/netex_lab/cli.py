from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit
from .report import json_report, markdown_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a NeTEx XML or ZIP dataset.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--schema", type=Path)
    args = parser.parse_args()
    result = audit(args.input, args.schema) if args.schema else audit(args.input)
    args.json.write_text(json_report(result), encoding="utf-8")
    if args.markdown:
        args.markdown.write_text(markdown_report(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
