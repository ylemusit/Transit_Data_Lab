# GTFS Audit Engine V1 — cierre del pack de precondiciones

Base autorizada: `e6c4d39e0032d3dd08cc8cc087a1bdb48275fe4a`. Rama aislada: `feat/gtfs-engine-preconditions-pack`. Ninguna fuente HOLDOUT se abrió. Este informe describe un cambio de desarrollo; no promueve el estado de `main` ni una auditoría de operadores.

| Finding | Before | Resolution | Evidence | Status |
| --- | --- | --- | --- | --- |
| R01 | SQL histórico con diez rutas legales absolutas | Manifiesto legal relativo y SHA-256; gate portable verifica bytes del checkout y sustituye en memoria solo las diez cláusulas de hash antes de ejecutar el gate Compliance completo | `03_Compliance/legal_sources_portable_v1.json`; `tools/compliance_portable_gate.py`; 22 Phase 1 + 377 Phase 2 y replay completo PASS | PASS |
| R02 | Bases ausentes del checkout; fallo tardío y dependencias implícitas | Configuración explícita, estados de recurso, hash, WAL y apertura DuckDB `-readonly` antes del gate | `config/protected_resources.example.json`; `tools/protected_resource_preflight.py`; prueba de ausencia, mismatch, WAL y dos DB externas PASS | PASS |
| R03 | Ningún workflow ni protección de `main` | Job sintético en cada PR, con tests, contratos M01/M03/Golden, split/lineage, Compliance legal portable y compileall; `main` exige `synthetic` actualizado también a administradores | [Run 36646327710](https://github.com/ylemusit/Transit_Data_Lab/actions/runs/36646327710) PASS; protección GitHub API: `contexts=[synthetic]`, `strict=true`, `enforce_admins=true` | PASS |
| R04 | CLI histórico devolvía 0 para `FAIL_TECHNICAL` | Entrada `gtfs_lab.ci_gate`, contrato JSON y salidas 0/2/3; política de findings explícita | `ORPHAN_ROUTE.zip`: `FAIL_TECHNICAL`, exit 2; `VALID_MINIMAL.zip`: `AUDIT_PASS`, exit 0 | PASS |
| R05 | ChangeAttribution 1.0.0 no atribuía mapas por regla | Contrato sucesor 1.1.0, versiones por `rule_id`, altas/bajas/cambios múltiples; nuevas auditorías lo marcan en manifest; comparaciones mixtas fallan cerradas | `change_attribution_v1_1.py`; tests legacy y sucesor; dos nuevos runs 1.1.0 comparados | PASS |
| R13 | Raíz histórica sucia y atrasada | Política de worktree aislado limpio, base ancestral y guard para operaciones autorizadas | `tools/clean_worktree_guard.py`; worktree desde base exacta; raíz intacta | MITIGATED |

## Cadena operativa

1. Crear un worktree aislado desde la base autorizada. Comprobar `git rev-parse HEAD`, `git status --short` y ejecutar `python tools/clean_worktree_guard.py --base <SHA>` en un checkout ya confirmado. La raíz histórica no es entorno autoritativo; nunca se resetea, limpia ni rebasa automáticamente.
2. Declarar las bases externas en una copia local de `config/protected_resources.example.json`. No versionar rutas privadas. `python tools/protected_resource_preflight.py --config <json>` devuelve `RESOURCE_READY`, `RESOURCE_NOT_FOUND`, `RESOURCE_HASH_MISMATCH`, `RESOURCE_WAL_PRESENT`, `RESOURCE_NOT_READABLE` o `RESOURCE_CONFIGURATION_INVALID`. Ningún recurso se copia ni busca de manera implícita.
3. `python tools/compliance_portable_gate.py --legal-root . --db <ruta-db> --db-sha256 <SHA> --gtfs-db <ruta-db-gtfs> --evidence <directorio-nuevo>` verifica fuentes y bases antes del gate Compliance completo. `--sources-only` sirve para CI sin DB y declara ese alcance. `--phase-only` verifica fuentes y Phase 1/2 sin replay completo. Un root legal externo requiere `--allow-external-legal-root`; la ruta utilizada aparece en el JSON. El SQL histórico permanece byte a byte sin cambios.
4. `python -m gtfs_lab.ci_gate <zip> --output <directorio-nuevo> [--findings-policy fail|allow]` interpreta el resultado de auditoría. 0 significa política satisfecha; 2, error técnico, de inspección o recurso; 3, configuración inválida. `AUDIT_WITH_FINDINGS` solo puede salir 0 con `--findings-policy allow`. El CLI V1 anterior conserva su semántica de ejecución.
5. Para reglas futuras, persistir `executed_rule_versions` y `change_attribution_contract_version=1.1.0`. Comparaciones 1.0↔1.0 usan el contrato congelado; 1.1↔1.1 comparan por regla; 1.0↔1.1 es `NOT_COMPARABLE` sin inventar versiones históricas.

## Evidencia local

- Checkout inicial limpio en el SHA base indicado. El remoto `origin/main` coincidía con ese SHA antes de preparar la rama.
- Fuentes legales: diez hashes correctos desde este worktree y desde otro root con idénticos bytes; ausencia y modificación fallaron; root equivocado sin autorización explícita falló. El SQL histórico no aparece en el diff.
- Bases externas iniciales: GTFS `F4186D603C455021B807261BDAC8770F5F5F4D2BED7830214EB98C223EFD99FC`; Compliance `4DB39FA5494C525F339F68BF0B96087B5FF2E1E0CB830EEA882336174BC8048B`. Preflight `RESOURCE_READY` para ambas. Gate Compliance completo `PASS`, con 22 checks Phase 1 y 377 Phase 2 más la excepción histórica `UNCHANGED_COUNT_audit.rules`. Su resumen conservó el hash final de Compliance.
- 101 tests completos PASS al inyectar la DB externa verificada en el único test histórico con ruta fija. Sin esa inyección: 100 PASS y 1 error de recurso ausente, sin falso PASS.
- M01, M02, M03-A, corpus Golden, evaluador Golden, regresión Golden, split y GTFS_Lab V1: PASS con entradas sintéticas y salidas temporales nuevas. Suite CI local: 72 tests PASS. `compileall` y `git diff --check`: PASS.
- El checkpoint M04 V2 `CEEEC24A72211DD0F0B59A663C3AF34C3697820FEACA015384DFDF534392C978` se conserva como referencia histórica; no se reabrió su fuente bajo la restricción «No HOLDOUT». Split, Golden, registros M05 y cierre M04 no se modificaron en el diff.
- Draft PR [#19](https://github.com/ylemusit/Transit_Data_Lab/pull/19) abierto, base `e6c4d39…`; el job remoto `synthetic` pasó. `main` exige el contexto `synthetic` con branch actualizado. PR sin fusionar.

## Riesgos aplazados

R06 registro extensible, R07 recursos/timeout completo, R08 matriz Windows/Linux, R09 restore, R10 `main.stops`, R11 limpieza histórica de tests y R14 retención de evidencia. El CI sin bases protegidas ejecuta la parte sintética y legal-source-only; el gate Compliance completo se probó localmente con recursos externos hash-verificados y no se presenta como PASS del job remoto.

## Veredicto

Q1 Sí: la configuración y manifiestos declaran recursos. Q2 Sí: ausencia falla antes del gate. Q3 Sí: el nuevo gate usa fuentes legales relativas y DB externa explícita. Q4 Sí: el gate de auditoría devuelve 2 para fallo técnico. Q5 Sí: contratos 1.1.0 por regla. Q6 Sí: el workflow pasó en GitHub y `main` exige su check. Q7 No se observa otro P1 que invalide el inicio del desarrollo del motor en esta rama.

`GTFS_AUDIT_ENGINE_V1_PRECONDITIONS = PASS`  
`GTFS_AUDIT_ENGINE_V1_READY_TO_START`

Este veredicto corresponde al pack en el Draft PR; no afirma que esté fusionado en `main`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
