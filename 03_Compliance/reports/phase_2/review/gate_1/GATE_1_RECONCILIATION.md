# Gate 1 Reconciliation — EU-REG-2017-1926

## Alcance y evidencia

Reconciliación exclusivamente documental de las inconsistencias de Human Review Gate 1. La base `03_Compliance/databases/transit_compliance.duckdb` se consultó en modo read-only. SHA-256 de entrada esperado y observado: `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`. El corpus empleado es el local consolidado a 04/03/2024. Para el texto de 9(3) se verificó el PDF consolidado local, página 10.

## Issue 1 — HUMAN_DECISION_CONFLICT

**Evidencia:** La matriz indicaba `HOLD_EXTERNAL` para `EU-2017-1926-CAND-A04-P01-004` y un flag `HUMAN_DECISION_CONFLICT`; el resumen ya afirmaba que no había conflictos. El SOURCE FACT remite al artículo 7 de la Directiva 2007/2/CE.

**Decisión humana:** Mantener `HOLD_EXTERNAL`. La dependencia es `PARTIAL`: la obligación/remisión principal es reconocible en EU-2017-1926, mientras que el contenido material completo exige contexto externo.

**Resolución:** Se quitó únicamente el flag de conflicto de la matriz CSV y su representación Markdown. `HUMAN_DECISION_CONFLICTS = 0`. No se alteró el candidato en DuckDB.

## Issue 2 — referencias temporales

**Evidencia:** El dossier inicial contabilizaba 12 candidatos. El SOURCE FACT de A08-P01-001 contiene «en un plazo que permita la reutilización fiable y efectiva».

**Decisión y resolución:** Baseline reconciliado: 13 candidatos con referencia temporal (10 fechas explícitas; 3 candidatos con 5 expresiones temporales funcionales). La referencia externa de calendario en A10-P02-001 se cuenta separadamente (1). Las expresiones funcionales no se convierten en DATE. No es un fallo de integridad. El resumen distingue claramente 12 como conteo inicial y 13 como reconciliado.

## Issues 3 y 4 — propuestas faltantes del artículo 9

**9(1):** Se conserva el candidato existente: Estado miembro, obligación de evaluación del cumplimiento.

**9(2):** Se propone documentalmente `PROCEDURAL_POWER`: autoridades competentes de los Estados miembros podrán solicitar documentos para evaluar 9(1). `is_mandatory=false`; no se representa como deber universal de titulares/proveedores. Se conservan las cuatro categorías consolidadas: (a) datos accesibles por NAP, calidad y reutilización; (b) servicios disponibles y conexiones cuando proceda; (c) declaración y justificantes de cumplimiento de artículos 3–8; (d) licencia o acuerdos con proveedores.

**9(3):** Se propone documentalmente `VERIFICATION`: obligación de los Estados miembros de efectuar comprobaciones aleatorias sobre la exactitud de las declaraciones de 9(2)(c). Se selecciona VERIFICATION porque el objeto expreso es verificar declaraciones; scope limitado a esa letra. No se infieren frecuencia, porcentaje, método, sanciones ni documentación adicional. No es una regla automática GTFS.

Ambas propuestas constan en `MISSING_CANDIDATES_V2.csv`, `WAITING_GATE_2`, sin filas nuevas en DuckDB. `MISSING_CANDIDATES_V1.csv` se conserva sin cambios como evidencia histórica. No se creó `audit.rules`.

## Issue 5 — SHA de project baseline

`project_baseline.json` contiene `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`, correspondiente a Phase 1. La DB Phase 2 tenía al inicio SHA `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`, igual al esperado. Se mantiene pendiente promover el baseline hasta que Phase 2 se cierre formalmente. Esta discrepancia documental no es un fallo de integridad de DB; el JSON no se modificó.

## Impacto

- **Gate 1:** conteos de decisiones y propuestas existentes conservados; flag conflictivo retirado; dos propuestas del artículo 9 documentadas; Gate 1 cerrado.
- **DuckDB:** ninguna fila añadida o modificada. No se materializaron requirements/deadlines, no se crearon mappings ni `audit.rules`, no se modificó `source.provisions`.
- **Annex 1.3 B-I / D-I:** sin cambios.
- **Git:** no se ejecutaron `git add`, commit ni push.

## Validación documental y read-only

- 34 candidatos originales presentes; 43 propuestas atómicas y 14 hijos split sin cambios.
- Decisiones sin cambios: 13 `APPROVE_AS_IS`, 9 `APPROVE_WITH_CHANGES`, 5 `SPLIT`, 7 `HOLD_EXTERNAL`, 0 `REJECT`.
- `HUMAN_DECISION_CONFLICTS = 0`.
- Temporales reconciliados = 13; fechas explícitas = 10; expresiones funcionales = 5 en 3 candidatos; referencia externa de calendario = 1.
- Propuestas faltantes = 2: artículo 9(2), 9(3).
- SHA-256 DB antes = `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`; después = `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`; idéntico.
- `project_baseline.json` conservado. Los conteos preexistentes de DB se mantienen: candidates 34, requirements 3, deadlines 1, source.provisions 92, source_facts del documento 35; mapping.format_coverage 0, mapping.format_equivalences 0 y audit.rules/evidence/results/runs 0. No se añadió ni modificó fila; ninguna materialización nueva.

## Estado final

`GATE_1_RECONCILIATION = PASS`

`HUMAN_REVIEW_GATE_1 = CLOSED`

`READY_FOR_HUMAN_REVIEW_GATE_2 = YES`

Esto no significa que Phase 2 esté frozen, que haya requisitos materializados, que se haya evaluado cumplimiento legal, realizado format mapping o creado audit rules. Gate 2 no se inició.

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
