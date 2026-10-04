"""Machine and human reports generated from the same interpretation result."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_markdown(result: dict[str, Any]) -> str:
    dataset = result["dataset_identity"]
    execution = result["execution_identity"]
    coverage = result["coverage"]
    lines = ["# Audit Interpretation & Consolidation V1", "",
             "## 1. Dataset Identity", "", f"- Dataset: `{dataset['dataset_id']}`",
             f"- SOURCE SHA-256: `{dataset['sha256']}`", "",
             "## 2. Execution Identity", "", f"- Audit execution: `{execution['audit_execution_id']}`",
             f"- GTFS_Lab: `{execution['engine_version']}`", f"- Interpretation contract: `{execution['interpretation_version']}`",
             f"- TDL ref: `{result['provenance']['deterministic_family_id_basis'].split('tdl_ref=', 1)[-1]}`", "",
             "## 3. Audit Result", "", f"Interpretation status: **{result['interpretation_status']}**.", "",
             "## 4. Coverage", "", f"- Raw occurrences: {coverage['raw_finding_count']}",
             f"- Classified occurrences: {coverage['consolidated_occurrence_count']}",
             f"- Unclassified occurrences: {coverage['unclassified_occurrence_count']}",
             f"- Accounting gap: {coverage['accounting_gap']}", "",
             "## 5. Raw Finding Summary", "", f"`source_findings` contiene {len(result['source_findings'])} findings de origen, preservados en el artefacto JSON.", "",
             "## 6. Consolidated Finding Families", ""]
    if result["finding_families"]:
        lines.extend(["| Rule | Pattern | Status | Raw | Direct entities | Population | Affected % |",
                      "| --- | --- | --- | ---: | ---: | ---: | ---: |"])
        for family in result["finding_families"]:
            pattern = family["patterns"][0]
            pct = "NOT_EVALUABLE" if family["affected_percentage"] is None else f"{family['affected_percentage']:.4f}%"
            population = family["population"]["population_count"]
            lines.append(f"| {family['rule_id']} | {pattern['classification']} | {family['technical_status']} | {family['raw_occurrence_count']} | {family['affected_entity_count']} | {population if population is not None else 'NOT_EVALUABLE'} | {pct} |")
    else:
        lines.append("No se generaron familias porque no hay findings raw.")
    lines.extend(["", "## 7. Pattern Analysis", ""])
    for family in result["finding_families"]:
        for statement in family["calculations"] + family["inferences"]:
            lines.append(f"- `{family['rule_id']}` ({statement['kind']}): {statement['statement']}")
    lines.extend(["", "## 8. Direct Impact", ""])
    for family in result["finding_families"]:
        direct = family["operational_impact"]["direct_affected"]
        lines.append(f"- `{family['rule_id']}`: {direct['entity_count']} {direct['entity_type']} directos afectados.")
    lines.extend(["", "## 9. Operational Propagation", ""])
    for family in result["finding_families"]:
        propagated = family["operational_impact"]["propagated_usage"]
        lines.append(f"- `{family['rule_id']}`: " + (", ".join(f"{item['entity_count']} {item['entity_type']}" for item in propagated) if propagated else "sin relaciones propagadas evaluables"))
    lines.extend(["", "## 10. Probable Explanations", ""])
    explanations = [f"- {item['statement']} ({item['kind']})" for family in result["finding_families"] for item in family["probable_explanations"]]
    lines.extend(explanations or ["- No se emitieron explicaciones causales."])
    lines.extend(["", "## 11. Remediation Assessment", ""])
    for family in result["finding_families"]:
        lines.append(f"- `{family['rule_id']}`: `{family['remediation_assessment']}`.")
    lines.extend(["", "## 12. Compliance Boundary", "",
                  "Los findings son técnicos. Este informe no declara incumplimiento legal, conformidad de perfil ni aceptación NAP.", "",
                  "## 13. Limitations", ""])
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(["", "## 14. Evidence References", ""])
    for family in result["finding_families"]:
        for ref in family["evidence_refs"]:
            lines.append(f"- `{family['rule_id']}`: {len(ref['raw_finding_ids'])} raw IDs; fichero `{ref['source_file']}`; ejecución `{ref['audit_execution_id']}`.")
    lines.extend(["", "Yeison Arbey Carrillo Lemus. Todos los derechos reservados.", ""])
    return "\n".join(lines)


def write_reports(directory: Path, result: dict[str, Any]) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    json_path, markdown_path = directory / "AUDIT_CONSOLIDATED.json", directory / "AUDIT_CONSOLIDATED.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(result), encoding="utf-8")
    return json_path, markdown_path
