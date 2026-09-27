# Prueba del delta semántico de base

Único delta: +1 compliance.source_facts row `EU-2017-1926-SF-A09-P03`.

| Tabla | Antes | Después | Contenido preexistente |
|---|---:|---:|---|
| audit.evidence | 0 | 0 | Sin cambios |
| audit.results | 0 | 0 | Sin cambios |
| audit.rules | 0 | 0 | Sin cambios |
| audit.runs | 0 | 0 | Sin cambios |
| compliance.deadlines | 1 | 1 | Sin cambios |
| compliance.nap_requirements | 0 | 0 | Sin cambios |
| compliance.provision_classifications | 92 | 92 | Sin cambios |
| compliance.requirement_candidate_sources | 21 | 21 | Sin cambios |
| compliance.requirement_candidates | 34 | 34 | Sin cambios |
| compliance.requirements | 3 | 3 | Sin cambios |
| compliance.source_facts | 35 | 36 | Sin cambios |
| mapping.format_coverage | 0 | 0 | Sin cambios |
| mapping.format_equivalences | 0 | 0 | Sin cambios |
| source.documents | 10 | 10 | Sin cambios |
| source.provisions | 92 | 92 | Sin cambios |
| source.relationships | 6 | 6 | Sin cambios |

DATABASE_BEFORE.json y DATABASE_AFTER.json contienen las filas de todas las tablas persistentes. DATABASE_TABLE_DELTA.csv contiene SHA-256 deterministas sobre JSON por fila (claves ordenadas, Unicode sin escapar, separadores compactos), filas ordenadas lexicográficamente y unidas con LF. Los NULL y tipos JSON se preservan; fechas/timestamps se representan como cadenas DuckDB. Dentro de la transacción se contrastaron conteos y SHA-256 de to_json de cada tabla, excluyendo únicamente el ID nuevo tras INSERT. La comparación posterior completa confirma que no se ha cambiado ninguna fila existente.

Autor: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
