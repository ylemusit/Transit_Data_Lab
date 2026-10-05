# Windows Self-Service Client V1 — W05 GIS / QGIS Bridge

**Decisión:** `W05 = PASS_WITH_LIMITATIONS` (2026-10-05).

## SCOPE

Hacer las exportaciones espaciales existentes accesibles desde la entrega y documentar su uso en QGIS como herramienta externa.

## IMPLEMENTATION

- La entrega ya incluye el directorio `engine_run/exports` con los GeoJSON/KML producidos por el motor; la campaña no duplica capas ni altera findings.
- Se añade `GIS_QGIS_GUIDE.md` a la entrega antes de calcular `audit_manifest.json`; el archivo queda cubierto por SHA-256 y `delivery_seal.json`.
- La GUI ofrece acceso a la carpeta GIS cuando hay capas GeoJSON o KML.
- QGIS permanece opcional y externo; la guía explica ausencia de capas y su límite probatorio.

## TESTS

- `python -m unittest discover -s tests -p 'test_client_*.py'`: 24 tests, OK; 2 skips documentados.
- La prueba E2E de entrega verifica que la guía GIS existe y está incluida en el manifest sellado.
- `py_compile`: PASS.
- `git diff --check`: PASS.

## EVIDENCE

`gtfs_lab.gis` genera GeoJSON/KML en las exportaciones del engine run. El workflow existente copia íntegramente el directorio de run a la entrega; la guía se añade como artefacto versionado y sellado.

## LIMITATIONS

- GeoPackage no se genera: no existe una dependencia GIS equivalente en el runtime actual y añadirla no es necesario para que QGIS consuma las capas existentes.
- No se instaló ni ejecutó QGIS para una prueba visual del proyecto/capas; el puente documentado es mediante apertura de formatos interoperables existentes.
- La presencia y cobertura espacial varían según el contenido de cada fuente.

## DECISION

`PASS_WITH_LIMITATIONS`; bridge GIS/QGIS disponible sin dependencia ni afirmación de cobertura GIS adicional.

## NEXT PHASE

W06 reporting profesional PDF y paquete de exportación.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
