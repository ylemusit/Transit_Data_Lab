# TDL Trust Foundation — M01

Fecha: 2026-09-28.

## Alcance

Primer bloque ejecutable del Programa 1 definido en `SERVICE_AUDIT_ALIGNMENT_MATRIX.md`.

Este checkpoint **no promueve** `TDL_TRUST_FOUNDATION = PASS` y no modifica la baseline GTFS_Lab V1. Introduce únicamente un contrato aditivo para preparar la trazabilidad de futuras auditorías.

## Implementado

- `gtfs_lab/audit_contract.py`
  - `AuditManifest` versionado (`1.1.0`).
  - los campos repetidos de identidad se derivan del dataset/run existente en lugar de declararse de forma independiente;
  - `source_sha256` obligatorio para una auditoría aceptada;
  - `original_preserved=true` solo se acepta acompañado de `preservation_evidence.verified=true` y del mismo SHA-256 de fuente;
  - estados normalizados de `RuleResult`;
  - lifecycle de findings con transiciones permitidas y estados terminales;
  - revisión humana obligatoria para estados ambiguos/contextuales y para findings reportados;
  - `finding_id` determinista y sensible al hash del dataset, con soporte Unicode;
  - rechazo de findings sin hash de fuente o sin localizador estable mínimo;
  - normalización de payloads existentes con deduplicación explícita;
  - rechazo de duplicados con el mismo `finding_id` pero contenido conflictivo.
- `gtfs_lab/trust_gate.py`
  - derivación del manifest desde identidad de dataset;
  - rechazo de hash ausente;
  - rechazo de preservación no verificada;
  - determinismo, Unicode y sensibilidad al dataset del `finding_id`;
  - rechazo de identidad de finding sin hash;
  - validación de transiciones del lifecycle;
  - revisión humana obligatoria para `DATA_AMBIGUITY`;
  - roundtrip real `RuleResult` dataclass → `result_dict` → normalización;
  - deduplicación explícita de findings repetidos entre regla y nivel superior;
  - rechazo de duplicados conflictivos;
  - rechazo de estados no contractuales.

## Verificación previa del checkout

La revisión de Codex sobre la primera versión de M01 ejecutó en el checkout completo:

- `python -m gtfs_lab.trust_gate`: PASS, 5/5;
- `py_compile` de GTFS_Lab: PASS en Python 3.12.10;
- gate GTFS_Lab V1: PASS, 14 casos, incluido E2E sintético y GIS direccional;
- gate Compliance V1: PASS, preservando su FAIL histórico declarado;
- hashes de la base Compliance sin cambios;
- `git diff --check`: PASS.

Esa revisión detectó cinco lagunas contractuales: identidad repetida, hash/preservación permisivos, cobertura insuficiente del finding ID, lifecycle sin transiciones y gate sin recorrido real de `RuleResult`. La versión actual de M01 las aborda sin integrar todavía el contrato en `pipeline.py`.

## Verificación pendiente tras el hardening

Debe repetirse sobre el checkout completo de la rama:

```text
python -m gtfs_lab.trust_gate
python -m py_compile gtfs_lab/*.py
# gate vigente GTFS_Lab V1
# gate vigente Compliance V1
git diff --check
```

La evidencia anterior no se reutiliza como PASS de la versión endurecida hasta ejecutar estos checks sobre el nuevo HEAD.

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

1. el gate endurecido pasa en el checkout real;
2. `py_compile`, GTFS_Lab V1 y Compliance V1 permanecen PASS según sus contratos vigentes;
3. `git diff --check` permanece limpio;
4. no cambia ninguna baseline, feed, base protegida ni evidencia histórica;
5. la revisión confirma que el manifest no puede aceptar hash ausente ni preservación autoafirmada;
6. las transiciones y obligaciones de revisión humana no permiten saltar de detección a reporte;
7. el roundtrip de `RuleResult` real y la política de duplicados se comportan según el contrato.

Hasta entonces, M01 es `PENDING_CONTRACT_REVIEW`. No se inicia M02 ni se declara `TDL_TRUST_FOUNDATION = PASS`.
