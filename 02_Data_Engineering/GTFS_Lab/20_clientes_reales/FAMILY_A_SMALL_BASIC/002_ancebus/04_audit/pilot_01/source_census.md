# Source census — Ancebus (002)

Fuente física censada: `FAMILY_A_SMALL_BASIC/002_ancebus/02_sources/gtfs_schedule/extracted`

## Ficheros

| Fichero | Bytes | Filas | Columnas | Encoding | BOM | Saltos | Vacío | Columnas exactas |
|---|---:|---:|---:|---|---|---|---|---|
| `agency.txt` | 164 | 1 | 6 | utf-8-sig | false | LF | false | `agency_id, agency_name, agency_url, agency_timezone, agency_phone, agency_lang` |
| `calendar.txt` | 225 | 3 | 10 | utf-8-sig | false | LF | false | `service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date` |
| `routes.txt` | 217 | 2 | 5 | utf-8-sig | false | LF | false | `route_id, agency_id, route_short_name, route_long_name, route_type` |
| `stop_times.txt` | 2214 | 52 | 5 | utf-8-sig | false | LF | false | `trip_id, arrival_time, departure_time, stop_id, stop_sequence` |
| `stops.txt` | 1107 | 26 | 4 | utf-8-sig | false | LF | false | `stop_id, stop_name, stop_lat, stop_lon` |
| `trips.txt` | 331 | 6 | 5 | utf-8-sig | false | LF | false | `route_id, service_id, trip_id, trip_headsign, direction_id` |

## Archivos GTFS

Obligatorios presentes: `agency.txt, routes.txt, trips.txt, stop_times.txt, stops.txt`.
Opcionales presentes: `calendar.txt`.
Archivos no estándar adicionales: `ninguno`.

## Campos no estándar

Ninguno detectado con el baseline de campos estándar usado en este censo.
