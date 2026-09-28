# TDL Trust Foundation — M01

Fecha: 2026-09-28.

## Alcance

Primer bloque ejecutable del Programa 1 definido en `SERVICE_AUDIT_ALIGNMENT_MATRIX.md`.

Este checkpoint **no promueve** `TDL_TRUST_FOUNDATION = PASS` y no modifica la baseline GTFS_Lab V1. Introduce únicamente un contrato aditivo para preparar la trazabilidad de futuras auditorías.

## Implementado

- `gtfs_lab/audit_contract.py`
  - `AuditManifest` versionado.
  - validación de campos mínimos e integridad SHA-256 de la fuente.
  - contrato `original_preserved=true`.
  - estados normalizados de `RuleResult`.
  - lifecycle inicial de findings.
  - `finding_id` determinista basado en fuente, regla y localización/evidencia.
  - normalización de payloads de validación existentes sin cambiar las reglas V1.
- `gtfs_lab/trust_gate.py`
  - manifiesto válido.
  - rechazo de SHA-256 inválido.
  - determinismo de `finding_id`.
  - normalización de `RuleResult` y recálculo de `finding_count`.
  - rechazo de estados no contractuales.

## Verificación realizada

Se reprodujeron ambos módulos en un entorno Python aislado y se ejecutó:

```text
python -m gtfs_lab.trust_gate
python -m py_compile gtfs_lab/audit_contract.py gtfs_lab/trust_gate.py
```

Resultado observado del gate sintético: `PASS`, 5/5 checks.

No se pudo clonar el repositorio desde el entorno de ejecución por falta de resolución de red, por lo que **no se ha ejecutado todavía el gate dentro del checkout completo**, ni GTFS_Lab V1, ni Compliance V1, ni feeds reales.

## No implementado todavía

- integración de `audit_manifest.json` en `pipeline.py`;
- persistencia del lifecycle en outputs V1;
- golden cases del repositorio;
- partición formal `development/holdout` del corpus;
- gate completo `TDL_TRUST_FOUNDATION`;
- modificación de reglas GTFS o Compliance;
- auditorías nuevas de operadores.

## Siguiente criterio de aceptación

Antes de integrar el contrato en el pipeline vigente:

1. ejecutar `python -m gtfs_lab.trust_gate` dentro del checkout real;
2. ejecutar `py_compile` del paquete;
3. reejecutar el gate GTFS_Lab V1 vigente;
4. confirmar que el contrato no reinterpreta ni cambia resultados históricos;
5. integrar `audit_manifest.json` de forma aditiva y repetir los gates.

Hasta completar estos pasos, M01 es `IMPLEMENTED_PENDING_REPO_VALIDATION`.
