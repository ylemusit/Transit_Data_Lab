# Source census — Gilsanz (014)

Fuente física censada: `FAMILY_C_COMPLEX_REGIONAL/014_gilsanz/02_sources/gtfs_schedule/extracted`

## Ficheros

| Fichero | Bytes | Filas | Columnas | Encoding | BOM | Saltos | Vacío | Columnas exactas |
|---|---:|---:|---:|---|---|---|---|---|
| `agency.txt` | 136 | 1 | 7 | utf-8-sig | false | CRLF | false | `agency_id, agency_name, agency_url, agency_timezone, agency_phone, agency_lang, agency_fare_url` |
| `calendar.txt` | 3246 | 82 | 10 | utf-8-sig | false | CRLF | false | `service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date` |
| `calendar_dates.txt` | 83077 | 4799 | 3 | utf-8-sig | false | CRLF | false | `service_id, date, exception_type` |
| `fare_attributes.txt` | 80 | 0 | 7 | utf-8-sig | false | NONE | true | `fare_id, price, currency_type, payment_method, transfers, agency_id, transfer_duration` |
| `fare_rules.txt` | 41 | 0 | 4 | utf-8-sig | false | NONE | true | `fare_id, route_id, origin_id, destination_id` |
| `routes.txt` | 10042 | 144 | 7 | utf-8-sig | false | CRLF | false | `route_id, agency_id, route_short_name, route_long_name, route_type, route_color, route_text_color` |
| `shapes.txt` | 188646 | 4991 | 5 | utf-8-sig | false | CRLF | false | `shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled` |
| `stop_times.txt` | 916412 | 16529 | 7 | utf-8-sig | false | CRLF | false | `trip_id, arrival_time, departure_time, stop_id, stop_sequence, shape_dist_traveled, timepoint` |
| `stops.txt` | 72724 | 1244 | 6 | utf-8-sig | false | CRLF | false | `stop_id, stop_code, stop_name, stop_lat, stop_lon, zone_id` |
| `trips.txt` | 65221 | 788 | 7 | utf-8-sig | false | CRLF | false | `route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id` |

## Archivos GTFS

Obligatorios presentes: `agency.txt, routes.txt, trips.txt, stop_times.txt, stops.txt`.
Opcionales presentes: `calendar.txt, calendar_dates.txt, shapes.txt, fare_attributes.txt, fare_rules.txt`.
Archivos no estándar adicionales: `fare_attributes.txt, fare_rules.txt, shapes.txt`.

## Campos no estándar

| Fichero | Campo | Ocurrencias no vacías |
|---|---|---:|
| `fare_attributes.txt` | `fare_id` | 0 |
| `fare_attributes.txt` | `price` | 0 |
| `fare_attributes.txt` | `currency_type` | 0 |
| `fare_attributes.txt` | `payment_method` | 0 |
| `fare_attributes.txt` | `transfers` | 0 |
| `fare_attributes.txt` | `agency_id` | 0 |
| `fare_attributes.txt` | `transfer_duration` | 0 |
| `fare_rules.txt` | `fare_id` | 0 |
| `fare_rules.txt` | `route_id` | 0 |
| `fare_rules.txt` | `origin_id` | 0 |
| `fare_rules.txt` | `destination_id` | 0 |
| `shapes.txt` | `shape_id` | 4991 |
| `shapes.txt` | `shape_pt_lat` | 4991 |
| `shapes.txt` | `shape_pt_lon` | 4991 |
| `shapes.txt` | `shape_pt_sequence` | 4991 |
| `shapes.txt` | `shape_dist_traveled` | 4991 |
