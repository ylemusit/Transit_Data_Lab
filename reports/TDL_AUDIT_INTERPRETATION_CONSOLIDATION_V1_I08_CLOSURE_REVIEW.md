# Audit Interpretation & Consolidation V1 — I08 cierre humano

**Decisión humana final:** `APPROVED`
**Estado:** `AUDIT_INTERPRETATION_AND_CONSOLIDATION_V1 = PASS / CLOSED`
**Fecha:** 2026-10-04
**Rama de trabajo:** `feat/audit-interpretation-i02-i08`
**Base:** `62224c13246bb0cda5cb4fc48b1409789abfcc1f`

Yeison aprueba el cierre técnico de Audit Interpretation & Consolidation V1. I01–I07 quedan `CLOSED`; I08 queda `PASS / CLOSED`. Esta decisión cierra el alcance técnico documentado y no amplía sus afirmaciones de conformidad, cobertura o validación.

## Resultado

I01–I08 pasan en el alcance técnico implementado. El resultado queda preparado para revisión y decisión de cierre humano; este informe no declara aprobado ese gate.

| Gate | Resultado técnico | Evidencia de alcance |
|---|---|---|
| I01 — Contrato | CLOSED | Contrato y esquema congelado verificados por pruebas sintéticas; SHA-256 `9AE821BA963849D341F509A74956DEF76C5739BD8175150198EA6A5F99CA7BD4`. |
| I02 — Consolidación | CLOSED | IDs de familia deterministas con codificación inyectiva de dimensiones canónicas; cardinalidad de origen y conciliación exacta, `accounting_gap = 0`. Los patrones sin clasificador aplicable quedan sin clasificar. |
| I03 — Impacto | CLOSED | Se distinguen entidades afectadas directamente del uso propagado por relaciones presentes en el SOURCE. Relaciones ausentes o colgantes no se presentan como uso existente. |
| I04 — G07 | CLOSED | Clasificación sintética de geometría, duplicados exactos, compatibilidad con cuantización, descensos y patrones mixtos. Igualdad de distancia con coordenadas distintas se expresa como inferencia compatible, sin atribuir causa. |
| I05 — Batería sintética | CLOSED | Casos de aumento, igualdad entera y fraccionaria, precisión mixta, duplicidad, descenso, varias formas, entidades compartidas, contexto y referencias incompletos o malformados, unknown, determinismo y conciliación. |
| I06 — Informes | CLOSED | JSON y Markdown derivados del mismo resultado y validados contra el esquema I01, que permanece sin cambios. |
| I07 — Integración | CLOSED | Client Workflow entrega los informes y su estado; Test Bank comprueba artefactos, estado y replay semántico. Un fallo derivado de interpretación queda explícito y no se convierte en aceptación del caso. |
| I08 — Regresión | PASS / CLOSED | 280 pruebas: 279 PASS, 0 FAIL, 1 SKIP documentado. |

El único `SKIP` corresponde a una prueba que requiere una copia protegida y separada de la base Compliance V1. Esa base no está presente en este worktree y no se abrió ni creó para esta validación.

```ini
TESTS = 280
PASS = 279
FAIL = 0
SKIP = 1 DOCUMENTED
I01_SCHEMA_SHA256 = 9AE821BA963849D341F509A74956DEF76C5739BD8175150198EA6A5F99CA7BD4
OPERATOR_SPECIFIC_CODE = 0
HOLDOUT_ACCESSED = NO
DEVELOPMENT_CORPUS_EXECUTED = NO
COMMERCIAL_VALIDATION = NOT_ESTABLISHED
MARKET_VALIDATION = NOT_ESTABLISHED
LEGAL_COMPLIANCE = NOT_CLAIMED
FULL_GTFS_COVERAGE = NOT_CLAIMED
```

## Límites preservados

- Solo G07 dispone de interpretación geométrica especializada; las demás reglas conocidas se agrupan como hallazgos técnicos y los patrones desconocidos quedan sin clasificar.
- Porcentajes y propagación dependen de las tablas y relaciones que existan en el SOURCE. Sin población fiable, el porcentaje es `null`.
- El esquema I01 congelado representa las métricas detalladas G07 como declaraciones `CALCULATED`; no se amplió el contrato.
- No se evaluó un SLA de rendimiento ni feeds grandes; el grafo y las tablas relevantes se cargan para análisis en memoria.
- La referencia TDL usa el HEAD del checkout y marca el árbol como `+WORKTREE_DIRTY`; sin metadatos Git disponibles, la referencia de runtime es `UNKNOWN`.
- No se ejecutó ningún dataset DEVELOPMENT (el corpus previsto contiene 14 datasets) ni se accedió a HOLDOUT. No se analizaron corpus completos ni feeds reales de operadores y no se añadió lógica específica de operador.
- El PASS técnico y esta aprobación de cierre no declaran conformidad legal, aceptación NAP, calidad global del feed, cobertura GTFS completa ni validación comercial o de mercado.

## Archivos de esta entrega

El runtime de interpretación, analizador G07, pruebas unitarias y de integración, workflow, Test Bank y estados del proyecto están en la rama `feat/audit-interpretation-i02-i08`. El contrato I01 y sus artefactos se conservaron; el esquema no cambió. Esta revisión registra la decisión de cierre humano aprobada por Yeison.
