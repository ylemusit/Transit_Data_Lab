# Source census — Viagón (005)

Fuente física censada: `FAMILY_A_SMALL_BASIC/005_viagon/02_sources/gtfs_schedule/extracted`

## Ficheros

| Fichero | Bytes | Filas | Columnas | Encoding | BOM | Saltos | Vacío | Columnas exactas |
|---|---:|---:|---:|---|---|---|---|---|
| `agency.txt` | 175 | 1 | 6 | utf-8-sig | false | LF | false | `agency_id, agency_name, agency_url, agency_timezone, agency_phone, agency_lang` |
| `calendar.txt` | 636 | 11 | 10 | utf-8-sig | false | LF | false | `service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date` |
| `routes.txt` | 871 | 11 | 5 | utf-8-sig | false | LF | false | `route_id, agency_id, route_short_name, route_long_name, route_type` |
| `stop_times.txt` | 14335 | 240 | 16 | utf-8-sig | false | LF | false | `trip_id, arrival_time, departure_time, stop_id, stop_sequence, Unnamed: 5, Unnamed: 6, Unnamed: 7, Unnamed: 8, Unnamed: 9, Unnamed: 10, Unnamed: 11, Unnamed: 12, Unnamed: 13, Unnamed: 14, Unnamed: 15` |
| `stops.txt` | 4054 | 62 | 4 | utf-8-sig | false | LF | false | `stop_id, stop_name, stop_lat, stop_lon` |
| `trips.txt` | 1192 | 22 | 5 | utf-8-sig | false | LF | false | `route_id, service_id, trip_id, trip_headsign, direction_id` |

## Archivos GTFS

Obligatorios presentes: `agency.txt, routes.txt, trips.txt, stop_times.txt, stops.txt`.
Opcionales presentes: `calendar.txt`.
Archivos no estándar adicionales: `ninguno`.

## Campos no estándar

| Fichero | Campo | Ocurrencias no vacías |
|---|---|---:|
| `stop_times.txt` | `Unnamed: 5` | 0 |
| `stop_times.txt` | `Unnamed: 6` | 0 |
| `stop_times.txt` | `Unnamed: 7` | 0 |
| `stop_times.txt` | `Unnamed: 8` | 0 |
| `stop_times.txt` | `Unnamed: 9` | 0 |
| `stop_times.txt` | `Unnamed: 10` | 0 |
| `stop_times.txt` | `Unnamed: 11` | 0 |
| `stop_times.txt` | `Unnamed: 12` | 0 |
| `stop_times.txt` | `Unnamed: 13` | 0 |
| `stop_times.txt` | `Unnamed: 14` | 0 |
| `stop_times.txt` | `Unnamed: 15` | 0 |
