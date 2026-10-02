from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("02_Data_Engineering/NeTEx_Lab").resolve()))
from netex_lab.rules import RULES, validate_registry  # noqa: E402


def main() -> int:
    validate_registry()
    output = {"registry_version": "1.0.0", "rules": sorted(RULES, key=lambda item: item["rule_id"])}
    target = Path("02_Data_Engineering/NeTEx_Lab/spec/netex_rule_registry_v1.json")
    target.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
