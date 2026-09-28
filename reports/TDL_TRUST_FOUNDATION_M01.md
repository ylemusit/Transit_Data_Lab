# TDL Trust Foundation — M01

Fecha: 2026-09-28.

## Alcance

Primer bloque ejecutable del Programa 1 definido en `SERVICE_AUDIT_ALIGNMENT_MATRIX.md`.

Este checkpoint **no promueve** `TDL_TRUST_FOUNDATION = PASS` y no modifica la baseline GTFS_Lab V1. Introduce únicamente un contrato aditivo para preparar la trazabilidad de futuras auditorías.

## Implementado

- `gtfs_lab/audit_contract.py`
  - `AuditManifest` versionado (`1.1.1`).
  - los campos repetidos de identidad se derivan del dataset/run existente;
  - `source_sha256` obligatorio para una auditoría aceptada;
  - `original_preserved=true` solo se acepta con evidencia verificada y hash coincidente;
  - estados normalizados de `RuleResult`;
  - lifecycle de findings con transiciones permitidas y estados terminales;
  - estados `DATA_AMBIGUITY`, `REQUIRES_CONTEXT`, `REVIEWED`, `CONFIRMED` y `REPORTED` exigen `review_required=true`, `reviewed_by` no vacío y `review_evidence` con `reviewed_at_utc` y `basis`;
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
  - aceptación de un estado revisado solo con identidad y evidencia de revisión completas;
  - roundtrip real `RuleResult` dataclass → `result_dict` → normalización;
  - deduplicación explícita de findings repetidos entre regla y nivel superior;
  - rechazo de duplicados conflictivos y estados no contractuales.

## Evidencia de revisión previa

Codex ejecutó sobre el HEAD anterior `2025ca75a9981c602042c8ad7a5602a62577407d`:

- trust gate PASS 10/10;
- `py_compile` PASS usando enumeración explícita de módulos en PowerShell;
- GTFS_Lab V1 gate PASS;
- Compliance V1 gate PASS, con hash inicial/final idéntico y FAIL histórico preservado;
- `git diff --check` PASS.

La revisión encontró que varios estados de revisión humana podían normalizarse sin `reviewed_by` ni evidencia de revisión. El contrato `1.1.1` corrige esa brecha. La evidencia anterior **no se reutiliza como PASS del nuevo HEAD**.

## Verificación pendiente tras este hardening

Repetir sobre el checkout completo de la rama:

```text
python -m gtfs_lab.trust_gate
# py_compile con enumeración explícita de módulos en PowerShell
# gate vigente GTFS_Lab V1
# gate vigente Compliance V1
git diff --check
```

## No implementado todavía

- integración de `audit_manifest.json` en `pipeline.py`;
- evidencia real de preservación producida por el pipeline;
- persistencia del lifecycle en outputs V1;
- golden cases del repositorio;
- partición formal `development/holdout` del corpus;
- gate completo `TDL_TRUST_FOUNDATION`;
- modificación de reglas GTFS o Compliance;
- auditorías nuevas de operadores.

## Criterio de cierre de M01

M01 puede pasar de `PENDING_CONTRACT_REVIEW` a `ACCEPTED_FOR_M02` solo si:

1. el gate actual pasa en el checkout real;
2. `py_compile`, GTFS_Lab V1 y Compliance V1 permanecen PASS según sus contratos vigentes;
3. `git diff --check` permanece limpio;
4. no cambia ninguna baseline, feed, base protegida ni evidencia histórica;
5. los estados que implican revisión humana no pueden aceptarse sin revisor y evidencia explícita;
6. las transiciones no permiten saltar de detección a reporte;
7. el roundtrip de `RuleResult` real y la política de duplicados se comportan según el contrato.

Hasta entonces, M01 es `PENDING_CONTRACT_REVIEW`. No se inicia M02 ni se declara `TDL_TRUST_FOUNDATION = PASS`.
