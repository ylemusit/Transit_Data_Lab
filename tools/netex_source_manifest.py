from __future__ import annotations

import json
import re
from pathlib import Path


SOURCE_TABLE = Path("01_Research_Standards/NeTEx/N02_SOURCE_REGISTER_INITIAL_20261002.md")
OUTPUT = Path("01_Research_Standards/NeTEx/N02_SOURCE_MANIFEST_20261002.json")

LEVELS = {
    **{f"N02-{number:02d}": "L1" for number in (1, 2, 13, 14, 21)},
    **{f"N02-{number:02d}": "L2" for number in (26, 27, 29)},
    **{f"N02-{number:02d}": "L3" for number in (3, 6, 7, 8, 9, 10, 11, 12, 16, 19, 20, 22, 23, 31)},
    **{f"N02-{number:02d}": "L4" for number in (4, 5, 15, 17, 18, 24, 28, 30)},
    "N02-25": "L1",
    "N02-32": "L1",
    "N02-33": "L1",
    "N02-34": "L1",
}
CLASSIFICATION = {
    **{f"N02-{number:02d}": "AUTHORITATIVE" for number in (1, 2, 13, 14, 21, 25, 26, 32, 33, 34)},
    **{f"N02-{number:02d}": "SUPPORTING" for number in (3, 8, 9, 10, 11, 12, 19, 20, 22, 23, 24, 29)},
    **{f"N02-{number:02d}": "IMPLEMENTATION_REFERENCE" for number in (4, 5, 6, 7, 16, 17, 18, 27, 28, 30)},
    **{f"N02-{number:02d}": "HISTORICAL" for number in (15,)},
    "N02-31": "SUPPORTING",
}
NORMATIVE_IDS = {"N02-01", "N02-02", "N02-13", "N02-14", "N02-21", "N02-32", "N02-33", "N02-34"}


def fields(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def title_from(cell: str) -> str:
    match = re.search(r"\[([^\]]+)\]", cell)
    if match:
        return match.group(1)
    return re.sub(r"`", "", cell).split(" — ", 1)[0].strip()


def build() -> dict:
    records = []
    for line in SOURCE_TABLE.read_text(encoding="utf-8").splitlines():
        id_match = re.match(r"\|\s*`?(N02-\d{2})`?\s*\|", line)
        if not id_match:
            continue
        row = fields(line)
        source_id = id_match.group(1)
        title_authority = row[1]
        purpose, finding, limitation = row[2:5]
        urls = re.findall(r"https?://[^\s)]+", title_authority + " " + finding + " " + limitation)
        if source_id not in LEVELS or source_id not in CLASSIFICATION:
            raise ValueError(f"Unclassified source: {source_id}")
        level = LEVELS[source_id]
        publisher_match = re.search(r"—\s*([^|]+)$", title_authority)
        publisher = publisher_match.group(1).strip() if publisher_match else title_authority
        raw = " ".join(row[2:5])
        dates = re.findall(r"20\d{2}(?:-\d{2}(?:-\d{2})?)?", raw)
        version_hits = re.findall(r"\bv?\d+\.\d+(?:\.\d+)?\b|CEN/TS 16614(?:-\d)?:?\d{0,4}", raw)
        classification = CLASSIFICATION[source_id]
        records.append({
            "source_id": source_id,
            "title": title_from(title_authority),
            "authority_level": level,
            "publisher": publisher,
            "version": version_hits[0] if version_hits else "NOT_IDENTIFIED_IN_REGISTER",
            "date": dates[0] if dates else "PUBLICATION_DATE_NOT_IDENTIFIED; REVIEWED_2026-10-02",
            "status": "HISTORICAL_REFERENCE" if classification == "HISTORICAL" else "REVIEWED_AT_CUTOFF",
            "classification": classification,
            "url": urls,
            "hash_if_local": None,
            "scope": purpose,
            "normative_or_informative": "NORMATIVE_SOURCE" if source_id in NORMATIVE_IDS else "INFORMATIVE_OR_IMPLEMENTATION",
            "machine_readable": any(token in (title_authority + purpose).lower() for token in ("xsd", "schema", "feed", "xml", "zip")),
            "notes": f"Finding: {finding} Limitation: {limitation}",
            "source_register_row": row[2:],
        })
    records.extend([
        {
            "source_id": "N02-32", "title": "Corrigendum to Delegated Regulation (EU) 2024/490 (2025/90135)",
            "authority_level": "L1", "publisher": "European Union / EUR-Lex", "version": "2025/90135",
            "date": "2025-02-13", "status": "REVIEWED_AT_CUTOFF", "classification": "AUTHORITATIVE",
            "url": ["https://eur-lex.europa.eu/eli/reg_del/2024/490/corrigendum/2025-02-13/oj"],
            "hash_if_local": None, "scope": "corrigendum to Annex 1 categories, French language edition",
            "normative_or_informative": "NORMATIVE_SOURCE", "machine_readable": False,
            "notes": "French-language corrections to Annex 1.2 terminology; no Spanish edition identified in this record. Retained for legal provenance, not used to derive a bus requirement.",
            "source_register_row": [],
        },
        {
            "source_id": "N02-33", "title": "Corrigendum to Delegated Regulation (EU) 2024/490 (2026/90193)",
            "authority_level": "L1", "publisher": "European Union / EUR-Lex", "version": "2026/90193",
            "date": "2026-03-12", "status": "REVIEWED_AT_CUTOFF", "classification": "AUTHORITATIVE",
            "url": ["https://eur-lex.europa.eu/eli/reg_del/2024/490/corrigendum/2026-03-12/oj"],
            "hash_if_local": None, "scope": "corrigendum to Annex 1.1(d)(v) and (vii), French language edition",
            "normative_or_informative": "NORMATIVE_SOURCE", "machine_readable": False,
            "notes": "EUR-Lex metadata states the correction does not concern the English version; the French corrections change Annex category wording. No Spanish-language correction was identified in this review. Applicability to the approved Spain/bus scope remains for human legal-language review.",
            "source_register_row": [],
        },
        {
            "source_id": "N02-34", "title": "Commission Delegated Regulation (EU) 2022/670 on real-time traffic information",
            "authority_level": "L1", "publisher": "European Union / EUR-Lex", "version": "2022/670",
            "date": "2022-02-02", "status": "IN_FORCE; REVIEWED_AT_CUTOFF", "classification": "AUTHORITATIVE",
            "url": ["https://eur-lex.europa.eu/eli/reg_del/2022/670/oj/eng"],
            "hash_if_local": None, "scope": "road transport data context and repeal of Delegated Regulation (EU) 2015/962",
            "normative_or_informative": "NORMATIVE_SOURCE", "machine_readable": False,
            "notes": "EUR-Lex states 2015/962 was repealed from 2025-01-01. Included to flag the 2024/490 Article 4(1)(a) cross-reference for legal review; no NeTEx obligation for the approved bus scope is inferred.",
            "source_register_row": [],
        },
    ])
    if len(records) != 34:
        raise ValueError(f"Expected 34 source records, found {len(records)}")
    return {
        "manifest_version": "1.0.0",
        "cutoff_date": "2026-10-02",
        "authority_hierarchy": {"L1": "EU and Spanish law/regulation", "L2": "CEN/NeTEx normative specifications",
                                "L3": "EPIP/profile/NAP guidance", "L4": "implementation references/examples/TDL recommendation"},
        "sources": records,
        "unresolved_topics": ["full controlled EPIP 2026 text and requirement mapping", "Spanish additional profile",
                              "NAP Spain technical acceptance contract", "current public location/status of captured NAP policies",
                              "redistribution terms for CEN/Crown Copyright XSD artifacts"],
        "schema_artifact": "schemas/v2.0.0/schema_manifest.json",
        "notes": ["No CEN controlled text is included.", "URLs are discovery/provenance only; schema artifacts are pinned by commit and per-file SHA-256.",
                  "NAP technical acceptance and any additional Spanish profile remain not identified in reviewed public sources.",
                  "Legal status is not determined by this source register."],
    }


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
