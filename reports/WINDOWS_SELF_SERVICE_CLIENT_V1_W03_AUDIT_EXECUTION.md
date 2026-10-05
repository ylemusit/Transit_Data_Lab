# Windows Self-Service Client V1 — W03 Audit Execution

**Decisión:** `W03 = PASS_WITH_LIMITATIONS` (2026-10-05).

## SCOPE

Clarificar ejecución y resultados del worker conservando el subprocess aislado, cancelación y contratos de entrega existentes.

## IMPLEMENTATION

- La GUI sigue lanzando `gtfs_lab.client_workflow` o `tdl-worker.exe`; el motor no se importa en el hilo de interfaz.
- La GUI lee marcadores de etapa ya emitidos por el workflow y muestra etapas reales sin porcentaje inventado. La barra permanece indeterminada.
- Se distinguen cancelación, entrada bloqueada, fallo del motor, fallo de aplicación, éxito y resultado que requiere revisión humana.
- La cancelación Windows conserva `taskkill /T /F` y se añade cobertura de un worker con proceso descendiente.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 24 tests, OK; 2 skips documentados.
- Coberturas añadidas: etapas, resultados, cancelación de árbol de procesos, fallo sintético del motor sin entrega exitosa, rerun E2E con source freeze y artefactos sellados.
- `py_compile`: PASS.
- `git diff --check`: PASS.

## EVIDENCE

Las pruebas de cliente incluyen el motor parcheado con fallo técnico y verifican `BLOCKED_TECHNICAL`, hash SOURCE preservado y ausencia de manifest de entrega exitosa. El caso de rerun ejecuta dos auditorías sintéticas independientes y confirma `source_immutable` y hashes verificados. El test Windows de terminación inicia worker e hijo propios y verifica su cierre.

## LIMITATIONS

- No se realizó aceptación visual manual de la nueva etiqueta de etapa en GUI compilada. El comportamiento de cancelación original ya estaba aceptado en W01; esta fase suma prueba automatizada real del árbol de procesos.
- La validación en máquina limpia permanece reservada a W08.

## DECISION

`PASS_WITH_LIMITATIONS`; subprocess, estados, información de etapa, cancelación y rerun quedan cubiertos por pruebas específicas.

## NEXT PHASE

W04 resultados entendibles sobre los artefactos autoritativos, sin duplicar su semántica.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
