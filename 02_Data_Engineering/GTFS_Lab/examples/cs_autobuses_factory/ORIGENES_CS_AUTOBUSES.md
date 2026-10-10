# Fuentes y generación de CS Autobuses

## Estado de esta entrega

Se han creado 32 artefactos de origen, uno por cada tipo de archivo definido en GTFS Schedule, y se han generado los 32 archivos GTFS correspondientes leyendo esos orígenes.

- Fuentes editables: carpeta origenes.
- Catálogo de procedencia por tipo de archivo: origenes/catalogo_fuentes.csv.
- Procedencia por registro de origen: origenes/procedencia.csv.
- Conversor reproducible: generar_cs_autobuses.py.
- Archivos GTFS derivados: carpeta gtfs_generado.
- ZIP de demostración con los 32 archivos en la raíz: entregas/CS_Autobuses_GTFS_32_archivos_DEMOSTRACION.zip.
- Guía del formato: GUIA_ARCHIVOS_GTFS.md.

La carpeta gtfs_generado y el ZIP contienen solo los 31 TXT y locations.geojson de salida; el ZIP no añade carpetas internas ni metadatos de procedencia.

## Supuesto de demostración

CS Autobuses opera en el municipio inventado CS-01. El conjunto combina dos líneas de autobús urbano programado y una modalidad flexible complementaria. Esta última permite poblar con datos de ejemplo location_groups.txt, location_group_stops.txt, locations.geojson y booking_rules.txt.

Los nombres, horarios, tarifas, reservas, red, polígonos y coordenadas son sintéticos. Las coordenadas sirven para demostrar tipos numéricos y relaciones espaciales; no se han contrastado con cartografía oficial, calles, nomenclátores ni una autorización de servicio. Las URLs bajo example.com son direcciones de ejemplo. Nada de lo generado acredita que CS Autobuses exista, tenga concesión, cobre esas tarifas o preste los servicios descritos.

## Cómo se representa la procedencia

Cada CSV de origen contiene los campos de negocio que se transforman y cuatro columnas adicionales:

- source_record_id identifica el registro de origen para poder rastrearlo.
- source_reference identifica la ficha o fuente sintética asociada.
- source_method describe cómo se creó el dato.
- source_note explica límites o supuestos importantes.

El transformador emite únicamente las columnas oficiales de cada archivo GTFS. En el origen GeoJSON, las propiedades de trazabilidad se eliminan al generar locations.geojson. La procedencia completa se conserva fuera del paquete en catalogo_fuentes.csv y procedencia.csv; no se agregan columnas privadas a los archivos normalizados GTFS.

## Reproducción

Desde la raíz del proyecto:

1. python generar_cs_autobuses.py --crear-origenes crea o restablece los orígenes sintéticos.
2. python generar_cs_autobuses.py --generar-gtfs deriva la carpeta gtfs_generado a partir de los CSV y GeoJSON de origen.
3. python generar_cs_autobuses.py --empaquetar-gtfs crea el ZIP a partir de los archivos derivados y comprueba que están los 32 esperados.

Si se editan los orígenes, se ejecuta solo la segunda operación para regenerar GTFS con esos cambios. La primera operación restablece las fuentes de demostración.

## Límites y siguiente fase

Esta salida sigue siendo una demostración ficticia: el ZIP se ha comprobado estructuralmente (32 entradas en la raíz, 31 TXT y un GeoJSON, sin errores CRC), pero no equivale a la aceptación de un operador ni a una publicación legal u operativa.

### Criterio de los futuros ZIP por ámbito

- **España:** el Anexo I.1.g de la Ley 9/2025 incluye expresamente GTFS entre los formatos aplicables a servicios de transporte programados, junto con NeTEx, SIRI, DATEX II y GTFS Realtime, según corresponda. Para autobús, el paquete deberá cubrir los datos aplicables de rutas, paradas, horarios, tarifas, accesibilidad y demás información exigida; usar toponimia oficial y castellano; y ofrecer una URL descargable por protocolo estándar, mantenida y actualizada. El NAP pide que el proveedor sea titular de los datos o esté autorizado y que estos sean fiables. Por ser CS Autobuses ficticia, solo podremos producir un **candidato de presentación**, no afirmar que el NAP lo ha aceptado.
- **Unión Europea:** el artículo 4.1.b del Reglamento Delegado (UE) 2017/1926, en su versión consolidada tras el Reglamento (UE) 2024/490, permite para los modos a los que aplica esa letra NeTEx u otro formato digital legible por máquina cuya compatibilidad e interoperabilidad completas puedan demostrarse; cita como ejemplos conversores y validadores automáticos. No menciona GTFS por nombre como excepción automática. Por tanto, el GTFS europeo solo se emitirá como candidato si la matriz confirma que esa vía aplica al servicio de autobús y se documenta una correspondencia semántica completa con el perfil NeTEx aplicable, demostrada mediante conversión y validación sin pérdidas de datos obligatorios. La aceptación final depende del NAP competente.

Fuentes consultadas el 9 de octubre de 2026: [Ley 9/2025, Anexo I](https://www.boe.es/buscar/act.php?id=BOE-A-2025-24545&p=20260321&tn=1), [FAQ del NAP español](https://nap.transportes.gob.es/faqs), [Reglamento Delegado (UE) 2017/1926 consolidado](https://eur-lex.europa.eu/eli/reg_del/2017/1926/2024-03-04/eng) y [Reglamento (UE) 2024/490](https://eur-lex.europa.eu/eli/reg_del/2024/490/oj/eng).

El ZIP existente conserva el nombre `DEMO` y no se presentará como ZIP aceptado en España o la UE. Primero se preparará el candidato español; en paralelo se evaluará la equivalencia GTFS–NeTEx. Si esa equivalencia no cubre íntegramente los requisitos aplicables, el resultado europeo se cerrará como no viable en GTFS y el alcance de publicación quedará en España.

La tabla GTFS completa contiene archivos opcionales y condicionales: esta demostración los rellena para ilustrar sus relaciones. La inclusión de los 32 archivos no significa que todas las empresas estén obligadas a publicar cada uno.
