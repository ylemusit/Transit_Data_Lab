# GTFS Audit Engine V1 — cierre G02

Fecha: 2026-09-30
PR: [#22](https://github.com/ylemusit/Transit_Data_Lab/pull/22)
Resultado: `G02_MERGED_AND_VERIFIED`

## Merge

| Campo | Valor comprobado |
| --- | --- |
| Head revisado | `8ca39ab61a7e4c7c80e943d12c2ba328b98a6b82` |
| Base esperada | `d7f4c76ce5c13844ea49303f0434f83d31d95a4c` |
| Merge commit | `8e2b1cac53e96f4000f8be0d9c03da4350edfbee` |
| Parent 1 | `d7f4c76ce5c13844ea49303f0434f83d31d95a4c` |
| Parent 2 | `8ca39ab61a7e4c7c80e943d12c2ba328b98a6b82` |
| `merged_at` | `2026-09-30T01:58:54Z` |
| Main autoritativo | `8e2b1cac53e96f4000f8be0d9c03da4350edfbee` |

La guarda pre-merge verificó PR OPEN, head y base exactos, `MERGEABLE` y `synthetic = SUCCESS` para el head revisado. Se marcó Ready for Review y se reconfirmaron SHA y check. Se fusionó con estrategia normal, protegida por el head esperado. El checkout aislado posterior quedó en `HEAD == origin/main == 8e2b1cac53e96f4000f8be0d9c03da4350edfbee` y `git status --short` vacío.

## Contrato y separación de ejecución

En main se verificaron las enumeraciones completas:

- Rule taxonomy: `STRUCTURE`, `SCHEMA`, `TYPE_FORMAT`, `IDENTITY`, `REFERENTIAL`, `TEMPORAL`, `SEQUENCE`, `SPATIAL`, `DATA_CONSISTENCY`, `QUALITY`.
- Authority: `GTFS_REQUIRED`, `GTFS_CONDITIONAL`, `GTFS_RECOMMENDED`, `TDL_QUALITY`.
- Requirement kinds: `REQUIRED`, `CONDITIONALLY_REQUIRED`, `OPTIONAL`, `RECOMMENDED`, `PROHIBITED_WHEN`.
- Engine-native statuses: `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `NOT_APPLICABLE`, `INSPECTION_ERROR`.

Legacy `WARNING` sigue en `RULE_RESULT_STATUSES` y no forma parte de `ENGINE_RULE_RESULT_STATUSES`; la ruta legacy permanece separada.

`identity.rules.rule_versions` persiste la identidad registrada completa. `registered_rule_ids` y `registered_rule_versions` representan las reglas registradas; `executed_rule_ids` y `executed_rule_versions` solo incluyen evaluadores que efectivamente se ejecutaron. La prueba focalizada verifica esta separación y confirma explícitamente que `NOT_APPLICABLE` no significa ejecución.

ChangeAttribution 1.1 conserva versiones sin cambio y registra `RULE_SEMANTIC_CHANGE`, `RULE_ADDED` y `RULE_REMOVED`; prueba además el cambio semántico cuando el estado es `NOT_APPLICABLE`. La ruta legacy ChangeAttribution 1.0 permanece intacta y cuenta con sus 16 pruebas de contrato.

## Regresión local en main

Ejecutada desde el checkout aislado de main:

| Grupo | Resultado |
| --- | ---: |
| G02 focused | 10 PASS |
| ChangeAttribution 1.0 | 16 PASS |
| Engine preconditions / ChangeAttribution 1.1 | 10 PASS |
| Audit comparison / synthetic pipeline | 23 PASS |
| Corpus split | 23 PASS |
| Lineage | 6 PASS |
| M02 persistence gate | 21/21 checks PASS |
| `compileall` | PASS |
| `git diff --check` | PASS |

Split y lineage inspeccionaron únicamente metadatos versionados. No se reprodujo ningún dataset HOLDOUT ni se abrió su contenido.

## CI remoto

El check `synthetic` terminó SUCCESS sobre el head revisado (run `36657369896`) y sobre el merge commit (run `36657667773`). El workflow remoto ejecuta precondiciones, contratos de corpus, ChangeAttribution y comparación sintética; no incluye `test_g02_rule_registry.py`. Por ello los 10 tests G02 se acreditan con la regresión local y no se infieren de CI.

## Cierre

```ini
G02 = PASS
GTFS_AUDIT_ENGINE_V1_RULE_REGISTRY = CLOSED
GTFS_AUDIT_ENGINE_V1_G03 = READY_TO_START
```

G03 no se inició ni se implementó como parte del merge.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
