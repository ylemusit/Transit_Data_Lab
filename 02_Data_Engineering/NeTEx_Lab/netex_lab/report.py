from __future__ import annotations

import json
from typing import Any


def json_report(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def markdown_report(result: dict[str, Any]) -> str:
    identity = result["dataset_identity"]
    lines = [
        "# NeTEx audit report", "",
        f"- Input: `{identity['source_kind']}` ({identity['member_count']} XML member(s))",
        f"- Dataset SHA-256: `{identity['input_sha256']}`",
        f"- XSD: NeTEx `{result['schema_identity']['release']}`",
        f"- XSD root SHA-256: `{result['schema_identity']['root_schema_sha256']}`", "",
        "## Result layers", "",
        "- XML well-formedness and XSD validity are reported independently.",
        "- Profile evaluation is not established by XSD validity.",
        "- NAP acceptance, regulatory compliance and overall data quality are not certified.", "",
        "## Findings", "",
        "| Status | Rule | File | Locator | Severity |", "|---|---|---|---|---|",
    ]
    for finding in result["findings"]:
        lines.append("| {status} | {rule_id} | {source_file} | {locator} | {severity} |".format(**finding))
    lines.extend(["", "## Gaps", ""])
    lines.extend(f"- {gap}" for gap in result["gaps"])
    lines.extend(["", "## Reproducibility", "",
                   "The normalized report excludes wall-clock timestamps and absolute input paths.",
                   "", "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""])
    return "\n".join(lines)
