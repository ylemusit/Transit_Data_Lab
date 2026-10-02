# NeTEx N01 — seguimiento de perfil español y feeds públicos

**Fecha de corte:** 2026-10-02
**Estado:** `IN_PROGRESS / SCOPE_NOT_DECIDED`
**Tipo:** investigación documental y lectura estructural de muestras públicas; no es una validación de conformidad.

## Resultado

1. **No se ha identificado un perfil nacional español publicado** en las fuentes públicas consultadas. El inventario de perfiles nacionales de DATA4PT, actualizado el 2024-12-11, no incluye España. El propio inventario es informativo y no exhaustivo; por tanto, esto acredita una laguna de evidencia pública, no la inexistencia de un documento fuera de ese inventario.
2. **Sí hay publicaciones NeTEx españolas de autobús regular**, entre ellas ofertas públicas de Bizkaibus, KBus y LeioaBus en el catálogo abierto del Consorcio de Transportes de Bizkaia. El Gobierno Vasco publica además un índice NeTEx para la red multimodal de Euskadi. Esto acredita práctica/publicación regional; no equivale a un perfil nacional español ni demuestra que cada recurso se ingiera actualmente en el NAP.
3. **Las tres muestras no declaran la versión de NeTEx ni un perfil.** Todas las XML examinadas son bien formadas y usan `PublicationDelivery` con `http://www.netex.org.uk/netex`. `ParticipantRef` es `enRoute`. Ninguno de estos hechos, por sí solo, permite atribuir una edición de CEN/TS, EPIP, un perfil regional formal ni conformidad XSD.
4. **Hay una discrepancia temporal en los metadatos del catálogo:** las páginas CKAN indican última actualización en abril de 2023, mientras que los XML descargados incluyen `PublicationTimestamp` de junio de 2024 (LeioaBus/KBus) y enero de 2025 (Bizkaibus). Se conservan hashes de los ZIP examinados. La ficha de metadatos no debe usarse como fecha del contenido XML.
5. La página pública del NAP lista NeTEx entre sus formatos y muestra conjuntos como Metro Bilbao/Euskotren con NeTEx, pero los detalles encontrados requieren iniciar sesión para descargar. No se accedió a endpoints protegidos ni se obtuvo el payload de ingesta del NAP. Los ejemplos de esta nota proceden del catálogo público CTB/proveedores y no deben presentarse como copia verificada del payload del NAP.

## Muestras examinadas

Descarga pública del recurso ZIP, anunciada como NeTEx y bajo CC BY 4.0 en el catálogo CTB. Inspección en un área temporal local; se omite la ruta del dispositivo en esta copia para evitar publicar información del entorno. Los archivos no se incorporaron al repositorio.

| Dataset | XML | Estructura observada | Timestamp(s) interno(s) | SHA-256 del ZIP |
|---|---:|---|---|---|
| [LeioaBus](https://data.ctb.eus/dataset/horarios-lejoanbusa) | 5 | `stops.xml`, 3 ficheros de línea y `common.xml`; 30 `StopPlace`, 163 `ServiceJourney` | 2024-06-13 04:32:04.4–04:32:05.4 UTC | `f84e9f40adbadc37919d4269b0bfe401c874f49645992406afa70e864312b313` |
| [KBus / Barakaldo](https://data.ctb.eus/dataset/kbus) | 6 | `stops.xml`, 4 ficheros de línea y `common.xml`; 88 `StopPlace`, 282 `ServiceJourney` | 2024-06-13 04:31:53.8–04:31:55.8 UTC | `161045d043b66096b6a06037a04423bdcb407d23882232e71d37bf5b3e260432` |
| [Bizkaibus](https://data.ctb.eus/dataset/horarios-lineas-bizkaibus) | 97 | `stops.xml` y 96 ficheros de línea; 2.263 `StopPlace`, 17.979 `ServiceJourney` | 2025-01-24 13:09:21–13:11:52 UTC | `21abc1a62647bb0b1f0e8bc20e03076b1ade32ccdc98782ef9ddbf8c52ab69c7` |

Los conteos corresponden a elementos XML de las copias descargadas, no a estadísticas actuales de servicio. La estructura observada incluye referencias de parada, puntos de ruta, patrones de viaje, servicios y horas de paso (`ScheduledStopPoint`, `RoutePoint`, `ServiceJourney`, `TimetabledPassingTime`). Es evidencia de contenido estático de red/horarios; no se evaluó integridad referencial ni semántica.

## Evidencia sobre perfil español y regulación

- [Inventario DATA4PT de perfiles nacionales](https://data4pt.org/wiki/National_Implementations): enumera los perfiles nacionales/transnacionales que documenta; España no figura en la tabla de perfiles publicados ni en su lista de implementaciones. Fecha de edición que declara la página: 2024-12-11.
- [Moveuskadi — datos de la red de transporte público de Euskadi](https://www.euskadi.eus/contenidos/ds_movilidad/md_ideeu_moveuskadi/es_def/index.shtml): portal institucional con índice de descarga `NETEX`, cobertura de autobuses, trenes, metro, tranvía, funiculares y otros modos. Declara actualización de datos 2026-09-27 y relaciona la publicación con el Reglamento Delegado 2017/1926. No publica allí una especificación de perfil NeTEx versionada.
- [Open Data Euskadi — BizkaiBus](https://opendata.euskadi.eus/catalogo/-/bizkaibus/): ofrece recursos NeTEx de paradas, líneas y horarios. Es evidencia institucional/regional de publicación, no de un perfil nacional.
- [NAP España — listado](https://nap.transportes.gob.es/Files/List?filterTT=2&orderby=Recientes&page=1&showFilterR=False&showFilterTF=False&showFilterTT=True&showfilterAU=False) y [detalle Metro Bilbao](https://nap.transportes.gob.es/Files/Detail/1066): el listado clasifica NeTEx como formato disponible; el detalle separa NeTEx estático de otras fuentes y exige sesión para descargar. En la ficha consultada, el bloque de metadatos general identifica modelo GTFS, no una versión/perfil de NeTEx. No se infiere que todas las fichas funcionen igual.
- [FAQ del NAP](https://nap.transportes.gob.es/faqs): indica GTFS o NeTEx como formatos preferidos y describe URL de publicación, pero no identifica perfil, versión ni reglas de validación NeTEx.
- [Reglamento Delegado (UE) 2024/490](https://eur-lex.europa.eu/eli/reg_del/2024/490/oj/eng): sigue siendo necesario leer junto al texto consolidado 2017/1926 para mapear perfiles mínimos UE o nacionales a las categorías aplicables. La muestra no determina ese alcance legal.

## Evaluación de las preguntas N01

| Pregunta | Resultado de esta investigación | Estado |
|---|---|---|
| ¿Perfil NeTEx español oficial o semioficial para el NAP? | No identificado en fuentes públicas examinadas. El listado DATA4PT no incluye España; puede haber documentación no indexada. | `UNRESOLVED` |
| ¿Qué versión/profile declaran feeds españoles reales? | Ninguna de las tres muestras declara versión ni perfil; solo namespace, estructura, participante y timestamps. | `UNRESOLVED` |
| ¿Hay datos reales españoles NeTEx de bus regular? | Sí: recursos de LeioaBus, KBus y Bizkaibus del catálogo CTB, con licencia CC BY 4.0. | `CONFIRMED_FOR_PUBLIC_SAMPLES` |
| ¿Son esos bytes exactamente los que NAP recibe ahora? | No se pudo comprobar; no se obtuvo copia del payload NAP autenticado ni un vínculo de identidad/hash entre catálogo CTB y NAP. | `UNRESOLVED` |
| ¿Se probó XSD, EPIP, EPIAP, perfil regional o aceptación NAP? | No. Se comprobó buena formación XML y se hizo un inventario estructural acotado. | `NOT_EVALUATED` |
| ¿Existe guía/validador NAP público específico de NeTEx? | No encontrado en FAQ/documentos públicos consultados; no prueba que no exista un canal técnico no publicado. | `NOT_IDENTIFIED` |

## Efecto sobre la propuesta provisional

La hipótesis de autobús regular estática gana evidencia práctica: hay publicaciones públicas de distintas escalas (servicio urbano y red interurbana) con estructuras NeTEx. No obstante, el inventario muestreado está centrado en Bizkaia, usa artefactos cuyo catálogo lleva metadatos de 2023 y no declara perfiles/versiones. No basta para cerrar la selección de `NeTEx 2.0.0`, elegir EPIP como perfil objetivo, afirmar un perfil español ni definir aceptación NAP.

**Recomendación para el gate:** mantener N01 `IN_PROGRESS / SCOPE_NOT_DECIDED`. Solicitar o localizar documentación técnica oficial de MITRAMS/NAP que indique perfil/versión/validador y obtener, mediante el flujo público autorizado del NAP, muestras descargables con artefacto y fecha de captura trazables. Después, comparar esas muestras con los archivos CTB únicamente si se establece su procedencia/identidad. Cualquier contacto institucional queda fuera de esta investigación documental.

## Procedimiento y límites

- Se inspeccionaron metadatos públicos y se descargaron tres ZIP públicos CC BY 4.0 en directorio temporal.
- Se calcularon SHA-256 y se recorrieron todos los miembros `.xml` de los tres ZIP con `xml.etree.ElementTree`; los XML se pudieron parsear.
- No se incorporaron datasets/XSD al repositorio, no se usaron credenciales, no se intentó sortear el login del NAP y no se hizo validación contra XSD ni contra perfil.
- Las URLs vivas y la disponibilidad de los recursos pueden cambiar. Los hashes identifican solamente las copias locales de esta captura.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
