# Source census — Kbus (020)

Fuente física censada: `FAMILY_D_MATURE_BENCHMARK/020_kbus/02_sources/gtfs_schedule/extracted`

## Ficheros

| Fichero | Bytes | Filas | Columnas | Encoding | BOM | Saltos | Vacío | Columnas exactas |
|---|---:|---:|---:|---|---|---|---|---|
| `agency.txt` | 157 | 1 | 8 | utf-8-sig | false | CRLF | false | `agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone, agency_fare_url, agency_email` |
| `calendar.txt` | 264 | 5 | 10 | utf-8-sig | false | CRLF | false | `service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date` |
| `calendar_dates.txt` | 816 | 56 | 3 | utf-8-sig | false | CRLF | false | `service_id, date, exception_type` |
| `fare_attributes.txt` | 126 | 1 | 7 | utf-8-sig | false | CRLF | false | `fare_id, price, currency_type, payment_method, transfers, agency_id, transfer_duration` |
| `fare_rules.txt` | 162 | 4 | 5 | utf-8-sig | false | CRLF | false | `fare_id, route_id, origin_id, destination_id, contains_id` |
| `feed_info.txt` | 253 | 1 | 9 | utf-8-sig | false | CRLF | false | `feed_publisher_name, feed_publisher_url, feed_lang, default_lang, feed_start_date, feed_end_date, feed_version, feed_contact_email, feed_contact_url` |
| `routes.txt` | 509 | 4 | 9 | utf-8-sig | false | CRLF | false | `route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color` |
| `shapes.txt` | 78506 | 1442 | 5 | utf-8-sig | false | CRLF | false | `shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled` |
| `stop_times.txt` | 598844 | 6142 | 10 | utf-8-sig | false | CRLF | false | `trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_headsign, pickup_type, drop_off_type, shape_dist_traveled, timepoint` |
| `stops.txt` | 7917 | 88 | 12 | utf-8-sig | false | CRLF | false | `stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station, stop_timezone, wheelchair_boarding` |
| `trips.txt` | 29642 | 278 | 10 | utf-8-sig | false | CRLF | false | `route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed` |

## Archivos GTFS

Obligatorios presentes: `agency.txt, routes.txt, trips.txt, stop_times.txt, stops.txt`.
Opcionales presentes: `calendar.txt, calendar_dates.txt, shapes.txt, feed_info.txt, fare_attributes.txt, fare_rules.txt`.
Archivos no estándar adicionales: `fare_attributes.txt, fare_rules.txt, feed_info.txt, shapes.txt`.

## Campos no estándar

| Fichero | Campo | Ocurrencias no vacías |
|---|---|---:|
| `fare_attributes.txt` | `fare_id` | 1 |
| `fare_attributes.txt` | `price` | 1 |
| `fare_attributes.txt` | `currency_type` | 1 |
| `fare_attributes.txt` | `payment_method` | 1 |
| `fare_attributes.txt` | `transfers` | 1 |
| `fare_attributes.txt` | `agency_id` | 1 |
| `fare_attributes.txt` | `transfer_duration` | 1 |
| `fare_rules.txt` | `fare_id` | 4 |
| `fare_rules.txt` | `route_id` | 4 |
| `fare_rules.txt` | `origin_id` | 4 |
| `fare_rules.txt` | `destination_id` | 4 |
| `fare_rules.txt` | `contains_id` | 0 |
| `feed_info.txt` | `feed_publisher_name` | 1 |
| `feed_info.txt` | `feed_publisher_url` | 1 |
| `feed_info.txt` | `feed_lang` | 1 |
| `feed_info.txt` | `default_lang` | 1 |
| `feed_info.txt` | `feed_start_date` | 1 |
| `feed_info.txt` | `feed_end_date` | 1 |
| `feed_info.txt` | `feed_version` | 1 |
| `feed_info.txt` | `feed_contact_email` | 1 |
| `feed_info.txt` | `feed_contact_url` | 1 |
| `shapes.txt` | `shape_id` | 1442 |
| `shapes.txt` | `shape_pt_lat` | 1442 |
| `shapes.txt` | `shape_pt_lon` | 1442 |
| `shapes.txt` | `shape_pt_sequence` | 1442 |
| `shapes.txt` | `shape_dist_traveled` | 1442 |
