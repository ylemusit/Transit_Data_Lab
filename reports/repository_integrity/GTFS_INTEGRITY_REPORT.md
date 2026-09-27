# GTFS Integrity Report

Fecha: 2026-09-27. Resultado global: **WARNING**.

El baseline raw está íntegro y todos los controles de datos ejecutados pasan. El resultado no es PASS global porque las capas `core`, `validation` y `analysis` descritas en la arquitectura no existen.

## Evidencia

- Base abierta con DuckDB 1.5.5 y `-readonly`.
- SHA-256 antes de la auditoría: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- ZIP fuente SHA-256: `f3093ab85d728ee824ba45cd3f247d1d9ea68a4685aaf25b27a8de98ea50b549`.
- Las 7 entradas ZIP coinciden por hash con los 7 ficheros extraídos.
- `calendar.txt` ausente y `calendar_dates.txt` presente.

## Conteos

| Relación | Esperado | Real | Estado |
|---|---:|---:|---|
| `raw.agency` | 41 | 41 | PASS |
| `raw.calendar_dates` | 3.875 | 3.875 | PASS |
| `raw.routes` | 609 | 609 | PASS |
| `raw.shapes` | 774.732 | 774.732 | PASS |
| `raw.stop_times` | 354.287 | 354.287 | PASS |
| `raw.stops` | 6.368 | 6.368 | PASS |
| `raw.trips` | 21.015 | 21.015 | PASS |

## Controles estructurales

Todos dieron 0: duplicados en claves examinadas, FK/referencias huérfanas, coordenadas inválidas, secuencias no numéricas/negativas, secuencias repetidas y secuencias no crecientes. Los formatos de arrival/departure examinados son válidos.

Hay 201 filas con llegada o salida a partir de `24:00:00`. Los campos siguen siendo `VARCHAR`; no se observó casting destructivo. La hora máxima es 24.

## Capas

| Capa | Estado |
|---|---|
| raw | IMPLEMENTED |
| core | NOT_FOUND |
| validation | NOT_FOUND |
| analysis | NOT_FOUND |
| GIS persistido/scripts | NOT_FOUND |
| exports KML | PARTIAL: 3 ficheros existentes sin script reproducible |

`validation.results` no existe. Ninguna familia prevista puede clasificarse como implementada dentro del GTFS_Lab.

## Route 440 / GIS

`route_id=440` continúa disponible: 1 ruta, 2 viajes, 2 shapes y 814 puntos. Los tres KML contienen en conjunto las variantes/sentidos esperados. Sus bounds son coherentes con Asturias, por lo que no se observa la antigua inversión de ejes en los exports actuales.

## Hallazgos

- MEDIUM: faltan las capas esperadas core/validation/analysis.
- MEDIUM: no hay SQL/script GIS reproducible.
- MEDIUM: README del laboratorio vacío.
- LOW: `main.stops` duplica exactamente `raw.stops` sin propósito documentado.
- LOW: el import usa rutas relativas dependientes del cwd.
- INFO: el feed usa correctamente `calendar_dates.txt` sin `calendar.txt`.

## Test creado

`02_Data_Engineering/GTFS_Lab/sql/07_tests/test_gtfs_lab_integrity.sql` contiene solo SELECT y no es un validador GTFS completo.

---

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

