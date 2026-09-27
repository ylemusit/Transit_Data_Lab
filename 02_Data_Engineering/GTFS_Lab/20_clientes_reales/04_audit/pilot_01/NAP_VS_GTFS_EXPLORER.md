# NAP vs GTFS Explorer 0.2.1 — Pilot Audit 01

La comparación de reglas solo se clasifica como correspondencia cuando existe evidencia de ambos lados. El baseline NAP disponible aporta conteos agregados y estado, pero no rule IDs; por eso no se fuerza una equivalencia de reglas.

## 002 — Ancebus

### NAP

- Errores: `0`.
- Warnings: `0`.
- Estado: `VALID_WITHOUT_WARNINGS`.

### GTFS Explorer

- Estado: `INVALID`; detectadas: `12`; persistidas: `12`; detalle completo: `true`.
- Severity counts persistidos: ERROR `6`, WARNING `0`, NOTICE `6`, BEST_PRACTICE `6`.

| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |
|---|---|---:|---:|---|---|
| `GTFS_BP_TRIP_WITHOUT_SHAPE` | NOTICE | 6 | 6 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_SHAPE_GEOMETRY_INVALID` | ERROR | 6 | 6 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |

Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.

## 005 — Viagón

### NAP

- Errores: `0`.
- Warnings: `22`.
- Estado: `VALID_WITH_WARNINGS`.

### GTFS Explorer

- Estado: `INVALID`; detectadas: `56`; persistidas: `56`; detalle completo: `true`.
- Severity counts persistidos: ERROR `22`, WARNING `0`, NOTICE `34`, BEST_PRACTICE `23`.

| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |
|---|---|---:|---:|---|---|
| `GTFS_BP_STOP_WITHOUT_STOP_TIMES` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_BP_TRIP_WITHOUT_SHAPE` | NOTICE | 22 | 22 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_EXTRA_HEADER` | NOTICE | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_SHAPE_GEOMETRY_INVALID` | ERROR | 22 | 22 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |

Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.

## 014 — Gilsanz

### NAP

- Errores: `1`.
- Warnings: `1`.
- Estado: `INVALID_WITH_ERRORS`.

### GTFS Explorer

- Estado: `INVALID`; detectadas: `1`; persistidas: `1`; detalle completo: `true`.
- Severity counts persistidos: ERROR `1`, WARNING `0`, NOTICE `0`, BEST_PRACTICE `0`.

| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |
|---|---|---:|---:|---|---|
| `GTFS_AGENCY_TXT_AGENCY_URL_REQUIRED` | ERROR | 1 | 1 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |

Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.

## 019 — Bizkaibus

### NAP

- Errores: `0`.
- Warnings: `0`.
- Estado: `VALID_WITHOUT_WARNINGS`.

### GTFS Explorer

- Estado: `INVALID`; detectadas: `1040852`; persistidas: `100000`; detalle completo: `false`.
- Severity counts persistidos: ERROR `100000`, WARNING `0`, NOTICE `0`, BEST_PRACTICE `0`.

| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |
|---|---|---:|---:|---|---|
| `GTFS_ROUTES_TXT_CONTINUOUS_DROP_OFF_CONDITIONALLY_FORBIDDEN` | ERROR | 99 | 99 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_ROUTES_TXT_CONTINUOUS_PICKUP_CONDITIONALLY_FORBIDDEN` | ERROR | 99 | 99 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_STOPS_TXT_WHEELCHAIR_BOARDING_OPTIONAL` | ERROR | 1360 | 1360 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_STOP_TIMES_TXT_CONTINUOUS_PICKUP_CONDITIONALLY_FORBIDDEN` | ERROR | 98442 | 98442 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |

Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.

## 020 — Kbus

### NAP

- Errores: `0`.
- Warnings: `317`.
- Estado: `VALID_WITH_WARNINGS`.

### GTFS Explorer

- Estado: `INVALID`; detectadas: `644`; persistidas: `644`; detalle completo: `true`.
- Severity counts persistidos: ERROR `644`, WARNING `0`, NOTICE `0`, BEST_PRACTICE `0`.

| Rule ID | Severity | Occurrences | Detail rows | Classification | Evidence |
|---|---|---:|---:|---|---|
| `GTFS_STOPS_TXT_WHEELCHAIR_BOARDING_OPTIONAL` | ERROR | 88 | 88 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_TRIPS_TXT_BIKES_ALLOWED_OPTIONAL` | ERROR | 278 | 278 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |
| `GTFS_TRIPS_TXT_WHEELCHAIR_ACCESSIBLE_OPTIONAL` | ERROR | 278 | 278 | `UNKNOWN` | `GTE informe-validacion.html`; NAP sin rule_id comparable |

Conclusión de operador: los agregados NAP y GTE no son equivalentes por sí solos; las reglas quedan `UNKNOWN` al no existir detalle NAP por regla.
