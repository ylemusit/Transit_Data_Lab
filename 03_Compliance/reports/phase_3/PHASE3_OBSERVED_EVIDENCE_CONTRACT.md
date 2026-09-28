# Phase 3 — contrato observado v1

Fecha: 2026-09-28. Estado: **PASS de almacenamiento aislado**, sin observaciones autoritativas ni regla de auditoría.

Se inspeccionaron columnas y constraints actuales antes de diseñar el contrato. La tabla `mapping.phase3_observed_evidence` permite conservar la envolvente JSON versionada en `notes VARCHAR`; no hace falta una tabla nueva ni migración. El contrato se aplica mediante `tools/phase3_observation_contract.py`. El esquema SQL por sí solo no obliga a respetarlo: futuros escritores deberán llamar al validador y verificar las relaciones. No se autoriza aquí un escritor de producción.

| Necesidad | Almacenamiento existente / contrato |
|---|---|
| Identidad/version/hash de dataset | `notes.dataset_id`, `dataset_version`, `dataset_sha256` (SHA-256 de los bytes) |
| Run y versión evaluador | `notes.inspection_run`, `evaluator_version`; hash del ejecutable en evidencia del run |
| Localizador y fecha | Columnas `locator`, `observed_on` |
| Scope | `notes.scope_unit_id`; comprobar que su mapping coincide con `mapping_id` y su capability con `capability_id` |
| Estado de inspección | `notes.inspection_status` |
| Resultado observado | `notes.observed_result`; copia idéntica en `observed_value` |
| Errores y límites | Arrays `notes.errors`, `limitations`; extensión inspeccionada en `inspection_extent` |
| Provenance sintética | `notes.synthetic=true` y `fixture_kind=SYNTHETIC_TEST` |

Pares permitidos: COMPLETED/PRESENT, COMPLETED/ABSENCE_CONFIRMED, COMPLETED/INDETERMINATE, NOT_INSPECTED/INDETERMINATE, FAILED/INDETERMINATE. ABSENCE_CONFIRMED exige inspección completa del locator declarado; nunca expresa ausencia en todo un operador. FAILED exige error; INDETERMINATE exige limitación. Valores desconocidos y versiones incompatibles se rechazan.

El hash identifica el artefacto, no acredita que se haya inspeccionado. NOT_INSPECTED puede conservar el hash de bytes preparados sin inspección. Un fallo de lectura sin hash verificable no produce esta observación: se conserva en el log del run. No se inventa hash vacío ni resultado de ausencia.

Prueba reproducible desde raíz (directorio nuevo):

```powershell
python tools/phase3_operational_checks.py --evidence <directorio_nuevo>
```

Requiere Python stdlib, DuckDB CLI, la DB local en el hash de cierre B02 y los módulos existentes de `tools`. Copia la DB a ese directorio y escribe exclusivamente en la copia. No descarga fuentes ni depende de una cuenta externa. Usa el esquema real, sus FK/CHECK, igualdad de todas las tablas restantes y un error transaccional inyectado para verificar rollback. Conserva cinco filas sintéticas de prueba en la copia, no en la base autoritativa.

Evidencia: [summary](evidence/phase3_operational_closure_20260928/contract_test/summary.json), [casos](evidence/phase3_operational_closure_20260928/contract_test/contract_cases.json), [rechazos](evidence/phase3_operational_closure_20260928/contract_test/rejected_cases.json), [filas](evidence/phase3_operational_closure_20260928/contract_test/isolated_rows.json). Cinco roundtrips exactos y deterministas, diez rechazos esperados, protección exacta y rollback PASS.

Estos casos son envolventes construidas para comprobar almacenamiento. `contract_payload.json` **no es un fixture SIRI**, los resultados no proceden de un parser y no prueban representabilidad. La demostración operativa sigue pendiente del contrato técnico del perfil. No se extrapola este PASS a etapas E–H o M.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
