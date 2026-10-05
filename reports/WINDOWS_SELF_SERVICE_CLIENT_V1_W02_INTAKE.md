# Windows Self-Service Client V1 — W02 Intake

**Decisión:** `W02 = PASS` (2026-10-05).

## SCOPE

Prevalidar el GTFS ZIP antes de iniciar el worker, mostrar identidad de entrada y conservar intacto el flujo de auditoría existente.

## IMPLEMENTATION

- `client_intake.py` valida extensión y existencia, estructura ZIP e integridad CRC, límites/nombres de miembros aplicados por el inspector del motor, presencia de tablas obligatorias y sus columnas requeridas.
- La GUI muestra filename, SHA-256, `GTFS-<prefijo SHA>`, tamaño, tablas detectadas e instante UTC. Muestra el identificador de auditoría al iniciar y no habilita el inicio hasta disponer de entrada validada y destino.
- La validación previa es de solo lectura. El worker mantiene la autoridad sobre la identidad persistida en `dataset_identity.json`, vuelve a hashear SOURCE y verifica la copia antes de continuar; no se modificó el contrato de identidad.
- Entradas rechazadas muestran `BLOCKED_INPUT_INVALID` y no lanzan worker.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_intake.py'`: 4/4 PASS.
- `python -m unittest discover -s tests -p 'test_client_*.py'`: 16 tests, OK; 2 skips documentados en el conjunto existente.
- `python -m py_compile gtfs_lab/client_app.py gtfs_lab/client_intake.py gtfs_lab/client_workflow.py`: PASS.
- `git diff --check`: PASS.

## EVIDENCE

Fixtures enteramente sintéticos cubren identidad/hash reproducible, inmutabilidad, tabla requerida ausente, columna requerida ausente, extensión incorrecta y ZIP malformado. La regresión cliente existente cubre generación de una entrega con source freeze y verificación de hashes.

## LIMITATIONS

- El resumen completo de metadatos de tablas se muestra en la GUI; no se infieren agencia/operador.
- Una validación inicial puede tardar proporcionalmente al tamaño comprimido porque verifica integridad ZIP completa; la interfaz no muestra progreso durante esa comprobación previa.
- La identidad autoritativa del audit sigue siendo la persistida por el worker al empezar; la GUI valida y muestra la identidad previa y el worker vuelve a calcularla.

## DECISION

`PASS`. Validación de entrada, error clasificado, identidad visible/reproducible e inmutabilidad quedan cubiertos sin cambios semánticos del motor.

## NEXT PHASE

Continuar W03; añadir lectura de marcadores de etapa en la GUI y cerrar la regresión de cancelación, fallo y rerun antes de declarar PASS.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
