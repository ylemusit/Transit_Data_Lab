# NeTEx Audit Lab V1

Runtime for the approved static passenger information scope: Spanish regular scheduled bus. The audit keeps XML well-formedness, NeTEx XSD validity, profile evaluation, semantics, quality and regulatory alignment as separate layers.

The schema must be prepared separately from an audit and supplied locally. Audits do not download schemas or resolve network references. Fetch the exact upstream snapshot at commit `a94e5e1752bcc13aabb8a1f3d018dc08e6978f42`, verify the SHA-256 manifest in `01_Research_Standards/NeTEx/schemas/v2.0.0/schema_manifest.json`, and point `--schema` to its `xsd/NeTEx_publication.xsd`. The schema is not copied into this repository pending resolution of the source's GPL-3.0 license file and its CEN/Crown Copyright notice.

Install the pinned dependency and run:

```powershell
python -m pip install -r requirements.txt
python -m netex_lab.cli input.xml --schema C:/schemas/NeTEx_publication.xsd --json audit.json --markdown audit.md
```

ZIP intake is in-memory, bounded, and rejects traversal and duplicate normalized member paths. Reports contain only basenames/member-relative names, hashes, findings and normalized evidence. No source file is changed.

The initial rule set is deliberately small. EPIP 2026 conformance remains `HUMAN_REVIEW_REQUIRED` because the full controlled standard is not present and no complete public machine implementation was identified. XSD validity does not imply EPIP conformance, NAP acceptance, regulatory compliance, or high data quality.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
