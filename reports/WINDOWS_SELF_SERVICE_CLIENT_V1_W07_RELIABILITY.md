# Windows Self-Service Client V1 — W07 Reliability

**Decisión:** `W07 = PASS_WITH_LIMITATIONS` (2026-10-05).

## SCOPE

Probar de forma determinista las condiciones de fallo seguras y verificar que los archivos fuente y los outputs previos no se pisan.

## IMPLEMENTATION

- La GUI mantiene estados distintos para entrada no válida, fallo de auditoría, fallo de aplicación, cancelación y revisión humana.
- Fallos del workflow conservan `workflow_result.json`, logs y artefactos parciales sin habilitar la entrega como éxito.
- Colisiones de workspace se rechazan antes de escribir; el rerun usa un audit id y workspace nuevos.
- El fallo del generador PDF queda marcado como no bloqueante y el manifest sella lo que sí se produjo.
- No se ejecutaron pruebas extremas de RAM/disk; se mantiene la política de recursos W00.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 25 tests, OK; 2 skips documentados hasta crear el onedir (W08).
- Matriz incluida: ZIP corrupto/no ZIP, tablas/columnas ausentes, fallo real sintético del motor, renderer PDF, ruta/unicode en pruebas empaquetadas, colisión de salida, rerun, cancelación con hijo, mutex de instancia, resultado de revisión y preservación del source.
- `py_compile`: PASS.
- `git diff --check`: PASS.

## EVIDENCE

El fallo técnico probado deja resultado `BLOCKED_TECHNICAL`, SOURCE inmutable y sin `audit_manifest.json` de entrega. La colisión conserva íntegro un marcador previo. La terminación Windows prueba que worker e hijo ya no aparecen activos. W08 ejecutará los tests empaquetados omitidos ahora.

## LIMITATIONS

- No se simuló ACL de destino sin permisos, disco lleno ni ruta superior al límite configurado; dependen de configuración de Windows y entorno.
- QGIS ausente no es fallo del producto porque es externo y opcional.
- Los recursos extremos y dataset 019 siguen fuera de esta campaña.

## DECISION

`PASS_WITH_LIMITATIONS`; las condiciones conocidas conservan fuente/evidencia, no se presentan parciales como éxito y dejan una nueva ejecución posible.

## NEXT PHASE

W08 build onedir, validación aislada Windows, distribución/instalación de usuario, versión RC y documentación de rebuild/rollback.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
