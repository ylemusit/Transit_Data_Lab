#!/usr/bin/env python3
"""Crea fuentes sintéticas de CS Autobuses y deriva archivos GTFS Schedule.

Uso:
  python generar_cs_autobuses.py --crear-origenes
  python generar_cs_autobuses.py --generar-gtfs

Las fuentes de origen son la fuente de verdad. La segunda operación lee los
orígenes, elimina sus columnas de trazabilidad y escribe solo campos GTFS.
No genera ZIP ni acredita autorización de explotación o cumplimiento legal.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
ORIGINS = ROOT / "origenes"
OUTPUT = ROOT / "gtfs_generado"
DELIVERIES = ROOT / "entregas"
GTFS_ZIP = DELIVERIES / "CS_Autobuses_GTFS_32_archivos_DEMOSTRACION.zip"
SOURCE_META = ["source_record_id", "source_reference", "source_method", "source_note"]

# Encabezados GTFS exactos usados por esta edición. Se incluyen los campos
# efectivamente modelados; los campos opcionales no utilizados se omiten.
SCHEMAS = {
    "agency.txt": ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang"],
    "stops.txt": ["stop_id", "stop_name", "stop_lat", "stop_lon", "location_type", "parent_station", "level_id", "platform_code"],
    "routes.txt": ["route_id", "agency_id", "route_short_name", "route_long_name", "route_type", "route_color", "route_text_color"],
    "trips.txt": ["route_id", "service_id", "trip_id", "trip_headsign", "direction_id", "shape_id", "wheelchair_accessible", "bikes_allowed"],
    "stop_times.txt": ["trip_id", "arrival_time", "departure_time", "stop_id", "location_group_id", "location_id", "stop_sequence", "stop_headsign", "pickup_type", "drop_off_type", "timepoint", "start_pickup_drop_off_window", "end_pickup_drop_off_window", "pickup_booking_rule_id", "drop_off_booking_rule_id"],
    "calendar.txt": ["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "start_date", "end_date"],
    "calendar_dates.txt": ["service_id", "date", "exception_type"],
    "fare_attributes.txt": ["fare_id", "price", "currency_type", "payment_method", "transfers", "agency_id", "transfer_duration"],
    "fare_rules.txt": ["fare_id", "route_id", "origin_id", "destination_id", "contains_id"],
    "timeframes.txt": ["timeframe_group_id", "start_time", "end_time", "service_id"],
    "rider_categories.txt": ["rider_category_id", "rider_category_name", "is_default_fare_category", "eligibility_url"],
    "fare_media.txt": ["fare_media_id", "fare_media_name", "fare_media_type"],
    "fare_products.txt": ["fare_product_id", "fare_product_name", "rider_category_id", "fare_media_id", "amount", "currency"],
    "fare_leg_rules.txt": ["leg_group_id", "network_id", "from_area_id", "to_area_id", "from_timeframe_group_id", "to_timeframe_group_id", "fare_product_id", "rule_priority"],
    "fare_leg_join_rules.txt": ["from_network_id", "to_network_id", "from_stop_id", "to_stop_id"],
    "fare_transfer_rules.txt": ["from_leg_group_id", "to_leg_group_id", "transfer_count", "duration_limit", "duration_limit_type", "fare_transfer_type", "fare_product_id"],
    "areas.txt": ["area_id", "area_name"],
    "stop_areas.txt": ["area_id", "stop_id"],
    "networks.txt": ["network_id", "network_name"],
    "route_networks.txt": ["network_id", "route_id"],
    "shapes.txt": ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence", "shape_dist_traveled"],
    "frequencies.txt": ["trip_id", "start_time", "end_time", "headway_secs", "exact_times"],
    "transfers.txt": ["from_stop_id", "to_stop_id", "from_route_id", "to_route_id", "transfer_type", "min_transfer_time"],
    "pathways.txt": ["pathway_id", "from_stop_id", "to_stop_id", "pathway_mode", "is_bidirectional", "traversal_time", "from_level_id", "to_level_id"],
    "levels.txt": ["level_id", "level_index", "level_name"],
    "location_groups.txt": ["location_group_id", "location_group_name"],
    "location_group_stops.txt": ["location_group_id", "stop_id"],
    "booking_rules.txt": ["booking_rule_id", "booking_type", "prior_notice_last_day", "prior_notice_last_time", "prior_notice_start_day", "prior_notice_start_time", "prior_notice_service_id", "message", "info_url", "booking_url"],
    "translations.txt": ["table_name", "field_name", "language", "translation", "record_id"],
    "feed_info.txt": ["feed_publisher_name", "feed_publisher_url", "feed_lang", "default_lang", "feed_start_date", "feed_end_date", "feed_version", "feed_contact_url"],
    "attributions.txt": ["attribution_id", "organization_name", "is_producer", "is_operator", "is_authority", "attribution_url"],
}

# Fuentes maestras ficticias. Los nombres de campo son normalizados para que
# el transformador pueda seleccionar las columnas GTFS sin perder trazabilidad.
DATA = {
    "agency.txt": [
        {"agency_id": "CSA-001", "agency_name": "CS Autobuses", "agency_url": "https://example.com/cs-autobuses", "agency_timezone": "Europe/Madrid", "agency_lang": "es"},
    ],
    "stops.txt": [
        {"stop_id": "CS-TERM", "stop_name": "CS-01 · Intercambiador", "stop_lat": "39.000000", "stop_lon": "-4.000000", "location_type": "1"},
        {"stop_id": "CS-ENT", "stop_name": "CS-01 · Entrada intercambiador", "stop_lat": "39.000050", "stop_lon": "-4.000050", "location_type": "2", "parent_station": "CS-TERM", "level_id": "LV-0"},
        {"stop_id": "CS-PLAT", "stop_name": "CS-01 · Andén A", "stop_lat": "39.000100", "stop_lon": "-4.000100", "location_type": "0", "parent_station": "CS-TERM", "level_id": "LV-1", "platform_code": "A"},
        {"stop_id": "CS-PLAZA", "stop_name": "CS-01 · Plaza Cívica", "stop_lat": "39.002000", "stop_lon": "-4.002000", "location_type": "0"},
        {"stop_id": "CS-HOSP", "stop_name": "CS-01 · Centro Sanitario", "stop_lat": "39.004000", "stop_lon": "-4.003000", "location_type": "0"},
        {"stop_id": "CS-UNI", "stop_name": "CS-01 · Campus", "stop_lat": "39.006000", "stop_lon": "-4.001000", "location_type": "0"},
        {"stop_id": "CS-MERC", "stop_name": "CS-01 · Mercado", "stop_lat": "39.003000", "stop_lon": "-3.998000", "location_type": "0"},
        {"stop_id": "CS-PARQ", "stop_name": "CS-01 · Parque", "stop_lat": "39.001000", "stop_lon": "-3.997000", "location_type": "0"},
    ],
    "routes.txt": [
        {"route_id": "R-01", "agency_id": "CSA-001", "route_short_name": "01", "route_long_name": "Intercambiador - Campus", "route_type": "3", "route_color": "145A8D", "route_text_color": "FFFFFF"},
        {"route_id": "R-02", "agency_id": "CSA-001", "route_short_name": "02", "route_long_name": "Intercambiador - Mercado", "route_type": "3", "route_color": "27844A", "route_text_color": "FFFFFF"},
        {"route_id": "R-FLEX", "agency_id": "CSA-001", "route_short_name": "D1", "route_long_name": "Servicio flexible CS-01", "route_type": "3", "route_color": "8A4E9B", "route_text_color": "FFFFFF"},
    ],
    "trips.txt": [
        {"route_id": "R-01", "service_id": "SV-ALL", "trip_id": "T-01-AM", "trip_headsign": "Campus", "direction_id": "0", "shape_id": "SH-01"},
        {"route_id": "R-01", "service_id": "SV-ALL", "trip_id": "T-01-PM", "trip_headsign": "Intercambiador", "direction_id": "1", "shape_id": "SH-01"},
        {"route_id": "R-02", "service_id": "SV-ALL", "trip_id": "T-02-AM", "trip_headsign": "Mercado", "direction_id": "0", "shape_id": "SH-02"},
        {"route_id": "R-FLEX", "service_id": "SV-ALL", "trip_id": "T-FLEX-GROUP", "trip_headsign": "Zona de puntos CS-01", "direction_id": "0"},
        {"route_id": "R-FLEX", "service_id": "SV-ALL", "trip_id": "T-FLEX-ZONE", "trip_headsign": "Área flexible CS-01", "direction_id": "0"},
    ],
    "stop_times.txt": [
        {"trip_id": "T-01-AM", "arrival_time": "07:00:00", "departure_time": "07:00:00", "stop_id": "CS-PLAT", "stop_sequence": "1", "timepoint": "1"},
        {"trip_id": "T-01-AM", "arrival_time": "07:12:00", "departure_time": "07:12:00", "stop_id": "CS-PLAZA", "stop_sequence": "2", "timepoint": "1"},
        {"trip_id": "T-01-AM", "arrival_time": "07:25:00", "departure_time": "07:25:00", "stop_id": "CS-UNI", "stop_sequence": "3", "timepoint": "1"},
        {"trip_id": "T-01-PM", "arrival_time": "17:00:00", "departure_time": "17:00:00", "stop_id": "CS-UNI", "stop_sequence": "1", "timepoint": "1"},
        {"trip_id": "T-01-PM", "arrival_time": "17:13:00", "departure_time": "17:13:00", "stop_id": "CS-PLAZA", "stop_sequence": "2", "timepoint": "1"},
        {"trip_id": "T-01-PM", "arrival_time": "17:25:00", "departure_time": "17:25:00", "stop_id": "CS-PLAT", "stop_sequence": "3", "timepoint": "1"},
        {"trip_id": "T-02-AM", "arrival_time": "08:00:00", "departure_time": "08:00:00", "stop_id": "CS-PLAT", "stop_sequence": "1", "timepoint": "1"},
        {"trip_id": "T-02-AM", "arrival_time": "08:10:00", "departure_time": "08:10:00", "stop_id": "CS-PARQ", "stop_sequence": "2", "timepoint": "1"},
        {"trip_id": "T-02-AM", "arrival_time": "08:20:00", "departure_time": "08:20:00", "stop_id": "CS-MERC", "stop_sequence": "3", "timepoint": "1"},
        {"trip_id": "T-FLEX-GROUP", "location_group_id": "LG-CS-CENTRO", "stop_sequence": "1", "start_pickup_drop_off_window": "09:00:00", "end_pickup_drop_off_window": "09:30:00", "pickup_type": "2", "drop_off_type": "2", "pickup_booking_rule_id": "BR-DAY-AHEAD", "drop_off_booking_rule_id": "BR-DAY-AHEAD"},
        {"trip_id": "T-FLEX-GROUP", "location_group_id": "LG-CS-CENTRO", "stop_sequence": "2", "start_pickup_drop_off_window": "09:31:00", "end_pickup_drop_off_window": "10:00:00", "pickup_type": "2", "drop_off_type": "2", "pickup_booking_rule_id": "BR-DAY-AHEAD", "drop_off_booking_rule_id": "BR-DAY-AHEAD"},
        {"trip_id": "T-FLEX-ZONE", "location_id": "ZG-CS-01", "stop_sequence": "1", "start_pickup_drop_off_window": "10:00:00", "end_pickup_drop_off_window": "10:30:00", "pickup_type": "2", "drop_off_type": "2", "pickup_booking_rule_id": "BR-DAY-AHEAD", "drop_off_booking_rule_id": "BR-DAY-AHEAD"},
        {"trip_id": "T-FLEX-ZONE", "location_id": "ZG-CS-01", "stop_sequence": "2", "start_pickup_drop_off_window": "10:31:00", "end_pickup_drop_off_window": "11:00:00", "pickup_type": "2", "drop_off_type": "2", "pickup_booking_rule_id": "BR-DAY-AHEAD", "drop_off_booking_rule_id": "BR-DAY-AHEAD"},
    ],
    "calendar.txt": [
        {"service_id": "SV-ALL", "monday": "1", "tuesday": "1", "wednesday": "1", "thursday": "1", "friday": "1", "saturday": "1", "sunday": "1", "start_date": "20261009", "end_date": "20261231"},
    ],
    "calendar_dates.txt": [
        {"service_id": "SV-ALL", "date": "20261225", "exception_type": "2"},
    ],
    "fare_attributes.txt": [
        {"fare_id": "FARE-URBANA", "price": "1.50", "currency_type": "EUR", "payment_method": "0", "transfers": "1", "agency_id": "CSA-001", "transfer_duration": "3600"},
    ],
    "fare_rules.txt": [
        {"fare_id": "FARE-URBANA", "route_id": "R-01"},
        {"fare_id": "FARE-URBANA", "route_id": "R-02"},
        {"fare_id": "FARE-URBANA", "route_id": "R-FLEX"},
    ],
    "timeframes.txt": [
        {"timeframe_group_id": "TF-DIARIO", "start_time": "00:00:00", "end_time": "24:00:00", "service_id": "SV-ALL"},
    ],
    "rider_categories.txt": [
        {"rider_category_id": "RC-GENERAL", "rider_category_name": "Tarifa general", "is_default_fare_category": "1"},
    ],
    "fare_media.txt": [
        {"fare_media_id": "FM-PAPEL", "fare_media_name": "Billete de papel CS-01", "fare_media_type": "1"},
        {"fare_media_id": "FM-APP", "fare_media_name": "App CS Autobuses (simulada)", "fare_media_type": "4"},
    ],
    "fare_products.txt": [
        {"fare_product_id": "FP-URBANO", "fare_product_name": "Billete sencillo urbano", "rider_category_id": "RC-GENERAL", "fare_media_id": "FM-PAPEL", "amount": "1.50", "currency": "EUR"},
        {"fare_product_id": "FP-URBANO", "fare_product_name": "Billete sencillo urbano", "rider_category_id": "RC-GENERAL", "fare_media_id": "FM-APP", "amount": "1.50", "currency": "EUR"},
    ],
    "fare_leg_rules.txt": [
        {"leg_group_id": "LG-FLAT", "network_id": "NET-CS-01", "from_timeframe_group_id": "TF-DIARIO", "fare_product_id": "FP-URBANO", "rule_priority": "1"},
    ],
    "fare_leg_join_rules.txt": [
        {"from_network_id": "NET-CS-01", "to_network_id": "NET-CS-01"},
    ],
    "fare_transfer_rules.txt": [
        {"from_leg_group_id": "LG-FLAT", "to_leg_group_id": "LG-FLAT", "transfer_count": "1", "duration_limit": "3600", "duration_limit_type": "0", "fare_transfer_type": "0"},
    ],
    "areas.txt": [
        {"area_id": "AREA-CS-CENTRO", "area_name": "Zona central sintética"},
        {"area_id": "AREA-CS-CAMPUS", "area_name": "Zona campus sintética"},
    ],
    "stop_areas.txt": [
        {"area_id": "AREA-CS-CENTRO", "stop_id": "CS-PLAT"},
        {"area_id": "AREA-CS-CENTRO", "stop_id": "CS-PLAZA"},
        {"area_id": "AREA-CS-CENTRO", "stop_id": "CS-HOSP"},
        {"area_id": "AREA-CS-CENTRO", "stop_id": "CS-MERC"},
        {"area_id": "AREA-CS-CENTRO", "stop_id": "CS-PARQ"},
        {"area_id": "AREA-CS-CAMPUS", "stop_id": "CS-UNI"},
    ],
    "networks.txt": [
        {"network_id": "NET-CS-01", "network_name": "Red urbana CS-01"},
    ],
    "route_networks.txt": [
        {"network_id": "NET-CS-01", "route_id": "R-01"},
        {"network_id": "NET-CS-01", "route_id": "R-02"},
        {"network_id": "NET-CS-01", "route_id": "R-FLEX"},
    ],
    "shapes.txt": [
        {"shape_id": "SH-01", "shape_pt_lat": "39.000100", "shape_pt_lon": "-4.000100", "shape_pt_sequence": "1", "shape_dist_traveled": "0"},
        {"shape_id": "SH-01", "shape_pt_lat": "39.002000", "shape_pt_lon": "-4.002000", "shape_pt_sequence": "2", "shape_dist_traveled": "300"},
        {"shape_id": "SH-01", "shape_pt_lat": "39.006000", "shape_pt_lon": "-4.001000", "shape_pt_sequence": "3", "shape_dist_traveled": "800"},
        {"shape_id": "SH-02", "shape_pt_lat": "39.000100", "shape_pt_lon": "-4.000100", "shape_pt_sequence": "1", "shape_dist_traveled": "0"},
        {"shape_id": "SH-02", "shape_pt_lat": "39.001000", "shape_pt_lon": "-3.997000", "shape_pt_sequence": "2", "shape_dist_traveled": "350"},
        {"shape_id": "SH-02", "shape_pt_lat": "39.003000", "shape_pt_lon": "-3.998000", "shape_pt_sequence": "3", "shape_dist_traveled": "600"},
    ],
    "frequencies.txt": [
        {"trip_id": "T-02-AM", "start_time": "08:00:00", "end_time": "09:00:00", "headway_secs": "1200", "exact_times": "0"},
    ],
    "transfers.txt": [
        {"from_stop_id": "CS-PLAT", "to_stop_id": "CS-PLAZA", "transfer_type": "2", "min_transfer_time": "240"},
    ],
    "pathways.txt": [
        {"pathway_id": "PW-ELEV-01", "from_stop_id": "CS-ENT", "to_stop_id": "CS-PLAT", "pathway_mode": "5", "is_bidirectional": "1", "traversal_time": "35", "from_level_id": "LV-0", "to_level_id": "LV-1"},
    ],
    "levels.txt": [
        {"level_id": "LV-0", "level_index": "0", "level_name": "Acceso"},
        {"level_id": "LV-1", "level_index": "1", "level_name": "Andén"},
    ],
    "location_groups.txt": [
        {"location_group_id": "LG-CS-CENTRO", "location_group_name": "Puntos flexibles centro CS-01"},
    ],
    "location_group_stops.txt": [
        {"location_group_id": "LG-CS-CENTRO", "stop_id": "CS-PLAZA"},
        {"location_group_id": "LG-CS-CENTRO", "stop_id": "CS-MERC"},
    ],
    "booking_rules.txt": [
        {"booking_rule_id": "BR-DAY-AHEAD", "booking_type": "2", "prior_notice_last_day": "1", "prior_notice_last_time": "17:00:00", "prior_notice_start_day": "14", "prior_notice_start_time": "00:00:00", "prior_notice_service_id": "SV-ALL", "message": "Servicio ficticio: reserva hasta las 17:00 del día anterior.", "info_url": "https://example.com/cs-autobuses/reservas", "booking_url": "https://example.com/cs-autobuses/reservar"},
    ],
    "translations.txt": [
        {"table_name": "agency", "field_name": "agency_name", "language": "en", "translation": "CS Buses", "record_id": "CSA-001"},
    ],
    "feed_info.txt": [
        {"feed_publisher_name": "CS Autobuses (datos sintéticos)", "feed_publisher_url": "https://example.com/cs-autobuses", "feed_lang": "es", "default_lang": "es", "feed_start_date": "20261009", "feed_end_date": "20261231", "feed_version": "CS-01-SYN-001", "feed_contact_url": "https://example.com/cs-autobuses/datos"},
    ],
    "attributions.txt": [
        {"attribution_id": "ATTR-CS-01", "organization_name": "CS Autobuses (operador ficticio)", "is_producer": "1", "is_operator": "1", "is_authority": "0", "attribution_url": "https://example.com/cs-autobuses"},
    ],
}

CATALOG = {
    "agency.txt": ("Ficha maestra sintética del operador", "Razón social/nombre público, portal y zona horaria definidos para el ejercicio."),
    "stops.txt": ("Inventario sintético de paradas", "Ubicaciones y jerarquía creadas para el municipio demostrativo; no proceden de una concesión real."),
    "routes.txt": ("Catálogo sintético de líneas", "Nombres, modo y presentación de rutas diseñados para el ejercicio."),
    "trips.txt": ("Plan sintético de explotación", "Viajes regulares y flexibles definidos para el periodo demostrativo."),
    "stop_times.txt": ("Cuadro horario sintético", "Tiempos y ventanas de servicio inventados; no son horarios autorizados."),
    "calendar.txt": ("Calendario sintético de servicio", "Vigencia creada para la muestra y compartida por los viajes."),
    "calendar_dates.txt": ("Registro sintético de excepciones", "Excepción ficticia para demostrar la relación con el calendario base."),
    "fare_attributes.txt": ("Tarifario sintético Fares V1", "Importe ficticio de demostración; no representa una tarifa aprobada."),
    "fare_rules.txt": ("Matriz sintética Fares V1", "Regla de aplicación enlazada a rutas ficticias."),
    "timeframes.txt": ("Franjas sintéticas de tarifa", "Ventana diaria ficticia para las reglas Fares V2."),
    "rider_categories.txt": ("Catálogo sintético de categorías", "Categoría general creada para ejemplificar productos tarifarios."),
    "fare_media.txt": ("Catálogo sintético de soportes", "Billete y aplicación simulados; no afirman aceptación comercial real."),
    "fare_products.txt": ("Catálogo sintético Fares V2", "Productos y precios inventados para el ejemplo."),
    "fare_leg_rules.txt": ("Reglas sintéticas de tarifa por tramo", "Reglas de red y franja asociadas al producto sintético."),
    "fare_leg_join_rules.txt": ("Reglas sintéticas de combinación", "Unión de tramos dentro de una red ficticia."),
    "fare_transfer_rules.txt": ("Reglas sintéticas de transbordo tarifario", "Ventana y tratamiento de transferencia de demostración."),
    "areas.txt": ("Zonas tarifarias sintéticas", "Zonas creadas para cubrir la estructura Fares V2."),
    "stop_areas.txt": ("Asignación sintética de paradas a zonas", "Correspondencia inventada de paradas y áreas tarifarias."),
    "networks.txt": ("Red tarifaria sintética", "Red creada para la demostración; se usa con route_networks.txt."),
    "route_networks.txt": ("Matriz sintética ruta-red", "Asociación inventada de las rutas a la red tarifaria."),
    "shapes.txt": ("Trazados sintéticos", "Geometrías inventadas para ilustración; no se han contrastado con calles reales."),
    "frequencies.txt": ("Plan de frecuencias sintético", "Intervalo creado para un viaje de ejemplo."),
    "transfers.txt": ("Regla sintética de conexión", "Tiempo mínimo ilustrativo, sin levantamiento de estación."),
    "pathways.txt": ("Grafo interior sintético", "Conexión de ascensor inventada para ilustrar niveles; no acredita accesibilidad."),
    "levels.txt": ("Niveles sintéticos", "Niveles creados para el ejemplo del intercambiador."),
    "location_groups.txt": ("Grupos sintéticos de demanda", "Grupo ficticio de puntos de recogida y bajada."),
    "location_group_stops.txt": ("Miembros sintéticos de grupo", "Paradas asociadas al grupo flexible de ejemplo."),
    "locations.geojson": ("Zona sintética GeoJSON", "Polígono dibujado para la muestra, sin validación territorial."),
    "booking_rules.txt": ("Condiciones sintéticas de reserva", "Antelación y URLs de ejemplo, no servicio activo."),
    "translations.txt": ("Traducción sintética", "Nombre traducido para ilustrar el mecanismo de traducciones."),
    "feed_info.txt": ("Ficha sintética de publicación", "Editor, periodo y versión identifican la edición de demostración."),
    "attributions.txt": ("Atribución sintética", "Roles atribuidos a una organización ficticia."),
}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_geojson_source() -> dict:
    return {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "id": "ZG-CS-01",
            "properties": {
                "stop_name": "Zona flexible CS-01",
                "stop_desc": "Polígono de demostración; no representa un área de servicio autorizada.",
                "source_record_id": "ORIG-ZONE-001",
                "source_reference": "SYN-GIS-CS-01",
                "source_method": "digitalización sintética",
                "source_note": "Coordenadas de ejemplo en WGS84; requieren sustitución/validación para uso real.",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-4.0060, 38.9980], [-3.9950, 38.9980],
                    [-3.9950, 39.0070], [-4.0060, 39.0070],
                    [-4.0060, 38.9980],
                ]],
            },
        }],
    }


def create_origins() -> None:
    ORIGINS.mkdir(parents=True, exist_ok=True)
    catalog_rows = []
    provenance_rows = []
    for filename, schema in SCHEMAS.items():
        rows = DATA[filename]
        source_rows = []
        for index, record in enumerate(rows, start=1):
            source_id = f"ORIG-{filename.split('.')[0].upper()}-{index:03d}"
            source_ref, note = CATALOG[filename]
            source_rows.append({
                "source_record_id": source_id,
                "source_reference": f"SYN-CS-01-{filename.split('.')[0].upper()}",
                "source_method": "elaboración sintética documentada",
                "source_note": note,
                **record,
            })
            provenance_rows.append({
                "gtfs_file": filename,
                "source_file": f"{filename.split('.')[0]}_origen.csv",
                "source_record_id": source_id,
                "source_reference": f"SYN-CS-01-{filename.split('.')[0].upper()}",
                "source_type": "SINTETICO",
                "creation_method": "elaboración sintética documentada",
                "limitation": note,
            })
        source_name = f"{filename.split('.')[0]}_origen.csv"
        write_csv(ORIGINS / source_name, SOURCE_META + schema, source_rows)
        catalog_rows.append({
            "gtfs_file": filename,
            "origin_artifact": source_name,
            "origin_category": source_ref,
            "owner": "CS Autobuses (ficticia)",
            "origin_status": "SINTETICO_PARA_DEMOSTRACION",
            "transformation": "seleccionar los campos GTFS definidos y descartar columnas source_*",
            "limitation": note,
        })

    geo_source = make_geojson_source()
    (ORIGINS / "locations_origen.geojson").write_text(
        json.dumps(geo_source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    catalog_rows.append({
        "gtfs_file": "locations.geojson",
        "origin_artifact": "locations_origen.geojson",
        "origin_category": "Capa GIS sintética",
        "owner": "CS Autobuses (ficticia)",
        "origin_status": "SINTETICO_PARA_DEMOSTRACION",
        "transformation": "copiar FeatureCollection y retener solo propiedades GTFS admitidas",
        "limitation": "Polígono de ejemplo en WGS84; no representa un área de servicio autorizada.",
    })
    provenance_rows.append({
        "gtfs_file": "locations.geojson",
        "source_file": "locations_origen.geojson",
        "source_record_id": "ORIG-ZONE-001",
        "source_reference": "SYN-GIS-CS-01",
        "source_type": "SINTETICO",
        "creation_method": "digitalización sintética",
        "limitation": "Coordenadas de ejemplo en WGS84; requieren sustitución/validación para uso real.",
    })
    write_csv(
        ORIGINS / "catalogo_fuentes.csv",
        ["gtfs_file", "origin_artifact", "origin_category", "owner", "origin_status", "transformation", "limitation"],
        catalog_rows,
    )
    write_csv(
        ORIGINS / "procedencia.csv",
        ["gtfs_file", "source_file", "source_record_id", "source_reference", "source_type", "creation_method", "limitation"],
        provenance_rows,
    )


def build_gtfs() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, schema in SCHEMAS.items():
        source_path = ORIGINS / f"{filename.split('.')[0]}_origen.csv"
        with source_path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames is None or any(field not in reader.fieldnames for field in schema):
                raise ValueError(f"Origen incompleto para {filename}: faltan campos GTFS.")
            output_rows = [{field: row.get(field, "") or "" for field in schema} for row in reader]
        write_csv(OUTPUT / filename, schema, output_rows)

    source_geo = json.loads((ORIGINS / "locations_origen.geojson").read_text(encoding="utf-8"))
    output_geo = {"type": "FeatureCollection", "features": []}
    for feature in source_geo.get("features", []):
        props = feature.get("properties", {})
        output_geo["features"].append({
            "type": "Feature",
            "id": feature["id"],
            "properties": {key: props[key] for key in ("stop_name", "stop_desc") if key in props},
            "geometry": feature["geometry"],
        })
    (OUTPUT / "locations.geojson").write_text(
        json.dumps(output_geo, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    print(f"Generados {len(SCHEMAS) + 1} archivos en {OUTPUT}")


def package_gtfs() -> None:
    expected = set(SCHEMAS) | {"locations.geojson"}
    actual = {path.name for path in OUTPUT.iterdir() if path.is_file()}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"Contenido GTFS inesperado; faltan={missing}; sobran={extra}")
    DELIVERIES.mkdir(parents=True, exist_ok=True)
    with ZipFile(GTFS_ZIP, "w", compression=ZIP_DEFLATED) as archive:
        for filename in sorted(expected):
            archive.write(OUTPUT / filename, arcname=filename)
    print(f"Creado {GTFS_ZIP}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crear-origenes", action="store_true", help="escribe las fuentes sintéticas")
    parser.add_argument("--generar-gtfs", action="store_true", help="deriva archivos GTFS desde origenes/")
    parser.add_argument("--empaquetar-gtfs", action="store_true", help="empaqueta los 32 archivos GTFS en un ZIP")
    args = parser.parse_args()
    if not args.crear_origenes and not args.generar_gtfs and not args.empaquetar_gtfs:
        parser.error("indica --crear-origenes, --generar-gtfs o --empaquetar-gtfs")
    if args.crear_origenes:
        create_origins()
        print(f"Creados {len(SCHEMAS) + 1} orígenes, catálogo y procedencia en {ORIGINS}")
    if args.generar_gtfs:
        build_gtfs()
    if args.empaquetar_gtfs:
        package_gtfs()


if __name__ == "__main__":
    main()
