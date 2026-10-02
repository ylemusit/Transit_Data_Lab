# NeTEx N05 — schema y modelo estructural

**Gate técnico local:** runtime operativo; schema baseline pinned; inventario reproducible.
**Schema:** `v2.0.0`, commit `a94e5e1752bcc13aabb8a1f3d018dc08e6978f42`, raíz `xsd/NeTEx_publication.xsd`, 458 dependencias XSD identificadas por SHA-256.

## Intake y seguridad

XML y ZIP se identifican por SHA-256 sin escribir sobre la entrada. ZIP se lee en memoria, limita miembros a 256, miembro XML a 256 MiB y total XML a 512 MiB; valida rutas normalizadas, nombres repetidos y errores de CRC/compresión antes de evaluar. El parser lxml desactiva resolución de entidades, DTD, red y árboles enormes; los documentos con DTD o nodos entity se rechazan. No se siguen `schemaLocation` del documento de entrada.

## Identidad y validación

`schema_manifest.json` fija release, commit, root, y hash/tamaño para cada XSD. El runtime vuelve a verificar todos los hashes locales antes de compilar la raíz. Cualquier dependencia ausente o distinta detiene la evaluación XSD como `INSPECTION_ERROR`. El schema se carga solo desde ruta local; fetching es una operación explícita de setup/CI, fuera de una auditoría.

Resultados separados en manifest: `WELL_FORMED`/`NOT_WELL_FORMED` y `XSD_VALID`, `XSD_INVALID`, `XSD_NOT_EVALUABLE`, `INSPECTION_ERROR`. Los findings usan el vocabulario nativo `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, etc. Cada XML de ZIP se informa por miembro. `iterparse` hace una pasada para well-formedness/inventario y otra con el XSD pinned para validar, borrando elementos terminados para limitar memoria de árbol. El inventario incluye namespace/counts de elementos, IDs repetidos y hasta 1.000 muestras de referencias con tipo/ID de origen cuando está disponible; no declara resolución semántica de referencias sin mapping de tipos.

## Rendimiento conocido

El intake lee el ZIP comprimido y mantiene los miembros XML acotados en memoria; los límites duros actuales son 512 MiB de archivo, 256 MiB por miembro y 512 MiB XML total. `iterparse` evita retener un DOM completo durante inventario y validación. La memoria sigue dependiendo del contenido en buffers ZIP, estado de identidad/referencias y estructuras de validación XSD; inputs por encima de los límites devuelven error de inspección.

El árbol de schema se descarga directamente desde su repositorio público durante preparación local/CI, no se distribuye aquí hasta revisar los avisos GPL-3.0 y CEN/Crown Copyright. Toda auditoría normal permanece offline.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
