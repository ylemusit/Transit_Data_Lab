# M06-B02 — requirement concept schema migration

Fecha: 2026-09-28. Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Decisión y alcance

```text
REQUIREMENT_CONCEPT_DESIGN = APPROVED
SCHEMA_MIGRATION = AUTHORIZED
B02_DATA_PERSISTENCE = NOT_AUTHORIZED
```

Se activó únicamente el esquema aditivo para concepts por requirement y su puente a mappings. No se insertaron concepts, mappings, coverage, representability ni evidence de B02; `audit.rules` no se modificó. Coverage permanece a nivel requirement. M06-B02 sigue `IN_PROGRESS`.

## Diseño aplicado

Migración: `sql/00_setup/010_phase_3_m06_b02_requirement_concepts.sql`.

- `mapping.phase3_requirement_concepts`: identidad estable, requirement/code únicos, alcance, source basis, review y provenance metadata.
- `mapping.phase3_concept_mappings`: puente explícito con FKs a concept y mapping, nota de relación y PK compuesta `(concept_id, mapping_id)`.
- Cardinalidad N:M: no hay `UNIQUE(mapping_id)`. El borrador proponía esa restricción, pero no se halló una razón arquitectónica demostrable para limitar la relación; se aplicó la preferencia aprobada `UNIQUE(concept_id, mapping_id)` equivalente mediante PK compuesta.
- Vocabulario añadido: `REQUIREMENT_CONCEPT_SCOPE` con `IN_SCOPE`, `PARTIAL`, `UNRESOLVED`, `OUT_OF_SCOPE`. Los vocabularios de review/outcome existentes se reutilizan.
- No se reconstruyó ni alteró `phase3_requirement_capabilities`; el requisito del concept se valida lógicamente porque no existe FK cross-schema apropiada.

## Prechecks y transacción

Rama `main`. Había cambios locales y ficheros no versionados preexistentes; se conservaron. Hash SHA-256 de la DB antes: `DD5256494A682618F8F10C46396F96806FDE90B79E88BBFCA9DFABEABB68F1E4`.

Prechecks antes de DDL: requirements 48; mappings sustantivos 6; reviews 6; coverage 8; automatability 6; exceptions sustantivas 6; representability 0; observed evidence 0; `audit.rules` 0; objetos objetivo ausentes. Phase 1: 92 provisions y 36 source facts. Phase 2: 48 requirements y 10 deadlines.

La migración usa una transacción explícita, guarda snapshots temporales de mappings, reviews, coverage, exceptions, source references, automatability, representability y observed evidence, y verifica igualdad bidireccional antes de `COMMIT`. Una guarda o postcheck fallido ejecuta `error()` dentro de la transacción, que aborta el lote; una repetición falla antes del DDL al detectar los objetos ya existentes. No depende de `IF NOT EXISTS`.

## Tratamiento legacy y conteos

Los seis mappings siguen presentes con sus IDs y filas intactas. El puente está vacío: cero asociaciones legacy y cero concepts. No hay backfill textual ni concept artificial.

| Dato | Antes | Después |
|---|---:|---:|
| Requirements | 48 | 48 |
| Mappings sustantivos | 6 | 6 |
| Asociaciones concept/mapping legacy | 0 | 0 |
| Coverage decisions | 8 | 8 |
| Mapping reviews | 6 | 6 |
| Observed evidence | 0 | 0 |
| Representability | 0 | 0 |
| `audit.rules` | 0 | 0 |
| Concepts / bridge rows | no existen | 0 / 0 |

Hash SHA-256 posterior: `E1CA1603D2300B90726F50C65092DB1E923B76F1F35A70E9F57CBB05E35A7BDE`. El cambio de hash corresponde a la migración de esquema y sus cuatro vocabularios, sin persistencia B02.

## Validación

| Validator | Resultado |
|---|---|
| M06-B02 schema validator (25 checks) | PASS |
| Level A | PASS; 6 mappings/capabilities, 6 exceptions, 0 referencias/estados/reasons inválidos |
| M04 | PASS; exit code 0 |
| M04B | PASS; 8 coverage y 6 reviews |
| M05B | PASS; 0 fallos; 41 HIGH, 7 MEDIUM, 0 LOW |
| M06-B01 | PASS; exit code 0 |
| Global exception accounting | PASS; M04 3, B01 3, sin excepciones sin contabilizar |
| `quick_validate` | No disponible en el proyecto; no ejecutado |

Los validators se ejecutaron con DuckDB `-readonly`. Los gates M04/M05B/B01 se usaron en su alcance vigente sin cambiar sus expectativas.

## Integridad, limitaciones y siguiente paso

Phase 1 y Phase 2 conservaron sus conteos protegidos. Los snapshots dentro de la transacción confirman sin diferencias los mappings, reviews, coverage, exceptions, source references, automatability, representability y observed evidence. No se creó una FK física para requirement porque la relación cruza esquemas; el validator detecta huérfanos y mismatch requirement↔mapping. El esquema acepta concepts independientes de mapping y no implementa coverage por concept ni puente a exceptions.

Antes de autorizar persistencia B02 faltan completar y aprobar la revisión de los concepts/candidatos C01/C04/C07/C08 y U01/U02/U03, resolver sus fuentes y límites de alcance, revisar mappings y cobertura por separado, y emitir una autorización humana explícita de persistencia B02. No persistir esos datos hasta ese gate.

```text
REQUIREMENT_CONCEPT_MIGRATION = PASS
REQUIREMENT_CONCEPT_SCHEMA = ACTIVE
LEGACY_MAPPINGS_PRESERVED = YES
B02_DATA_PERSISTENCE = NOT_AUTHORIZED
M06_B02 = IN_PROGRESS
```
