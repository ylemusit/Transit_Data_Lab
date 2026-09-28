# TDL Trust Foundation — M01

Fecha: 2026-09-28.

## Estado

`ACCEPTED_FOR_M02`

M01 queda aceptado como contrato base para iniciar M02. Este estado **no** declara `TDL_TRUST_FOUNDATION = PASS`, no integra todavía el manifest en `pipeline.py` y no modifica la baseline GTFS_Lab V1.

## Alcance

Primer bloque ejecutable del Programa 1 definido en `SERVICE_AUDIT_ALIGNMENT_MATRIX.md`.

Introduce un contrato aditivo para preparar la trazabilidad y defensa de futuras auditorías, sin reinterpretar reglas, resultados históricos, feeds ni Compliance V1.

## Implementado

- `gtfs_lab/audit_contract.py`
  - `AuditManifest` versionado (`1.1.2`).
  - los campos repetidos de identidad se derivan del dataset/run existente;
  - `source_sha256` obligatorio para una auditoría aceptada;
  - `original_preserved=true` solo se acepta con evidencia verificada y hash coincidente;
  - estados normalizados de `RuleResult`;
  - lifecycle de findings con transiciones permitidas y estados terminales;
  - estados `DATA_AMBIGUITY`, `REQUIRES_CONTEXT`, `REVIEWED`, `CONFIRMED` y `REPORTED` exigen `review_required=true`, `reviewed_by` no vacío y `review_evidence` con `reviewed_at_utc` y `basis`;
  - `review_evidence.reviewed_at_utc` debe ser ISO-8601 válido con UTC efectivo (offset cero); se rechazan cadenas inválidas, timestamps naive y offsets no UTC;
  - `finding_id` determinista, sensible al hash del dataset y compatible con Unicode;
  - rechazo de findings sin hash de fuente o sin localizador estable mínimo;
  - normalización de payloads existentes con deduplicación explícita;
  - rechazo de duplicados con el mismo `finding_id` pero contenido conflictivo.
- `gtfs_lab/trust_gate.py`
  - derivación del manifest desde identidad de dataset;
  - rechazo de hash ausente y preservación no verificada;
  - determinismo, Unicode y sensibilidad al dataset del `finding_id`;
  - validación de transiciones del lifecycle;
  - cobertura de todos los estados que requieren revisión humana;
  - rechazo de `review_required=false`, ausencia de `reviewed_by`, ausencia o incompletitud de `review_evidence`;
  - rechazo de `reviewed_at_utc` inválido, sin timezone o con offset distinto de UTC;
  - aceptación explícita de representaciones UTC `Z` y `+00:00`;
  - roundtrip real `RuleResult` dataclass → `result_dict` → normalización;
  - deduplicación explícita de findings repetidos entre regla y nivel superior;
  - rechazo de duplicados conflictivos y estados no contractuales.

## Evidencia de aceptación

Revisión ejecutada sobre el HEAD `32529f7517cea580e72618fa8d7caa2380b8c382`:

- `python -m gtfs_lab.trust_gate`: **PASS, 12/12**;
- `py_compile`: **PASS** con los 13 módulos GTFS_Lab enumerados explícitamente;
- gate GTFS_Lab V1: **PASS**;
- hashes protegidos GTFS_Lab antes/después: **sin cambios**;
- gate Compliance V1: **PASS**;
- hash Compliance inicial/final: **idéntico** (`4DB39F…788E0F`), conservando el FAIL histórico previsto;
- `git diff --check`: **PASS**;
- revisión adicional de timestamps UTC: **sin brecha material**;
- los cambios del SHA revisado se limitan a los tres archivos de M01.

El gate de Compliance se ejecutó desde `main` porque el checkout temporal no contiene las bases locales ignoradas. Se verificó que las fuentes del gate no difieren entre `main` y el SHA revisado.

## Criterios de cierre

Los criterios definidos para M01 se consideran satisfechos:

1. trust gate PASS en checkout real;
2. `py_compile`, GTFS_Lab V1 y Compliance V1 permanecen PASS según sus contratos vigentes;
3. `git diff --check` limpio;
4. sin cambios de baseline, feeds, bases protegidas ni evidencia histórica;
5. estados de revisión humana protegidos por identidad y evidencia explícita;
6. `reviewed_at_utc` limitado a timestamps ISO-8601 con UTC efectivo;
7. transiciones sin salto de detección a reporte;
8. roundtrip de `RuleResult` y política de duplicados validados.

## No implementado todavía

Corresponde a M02 o hitos posteriores:

- integración de `audit_manifest.json` en `pipeline.py`;
- evidencia real de preservación producida por el pipeline;
- persistencia del lifecycle en outputs de ejecución;
- golden cases del repositorio;
- partición formal `development/holdout` del corpus;
- gate completo `TDL_TRUST_FOUNDATION`;
- modificación de reglas GTFS o Compliance;
- auditorías nuevas de operadores.

## Autorización de siguiente hito

M01 queda `ACCEPTED_FOR_M02`.

M02 puede diseñar e integrar de forma **aditiva** `audit_manifest.json` y la normalización persistente de findings, preservando los contratos y gates V1. Cualquier integración deberá volver a ejecutar los gates de confianza, GTFS_Lab y Compliance antes de promover el siguiente estado.
