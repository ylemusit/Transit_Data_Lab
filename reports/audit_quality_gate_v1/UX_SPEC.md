# TDL-AUD-19 — navegación y accesibilidad por soporte

Objetivo: que dirección encuentre rápidamente decisión, impacto, límite y siguiente paso; que el equipo productor llegue desde cada conclusión al hallazgo, criterio, localizador y prueba. La vista ejecutiva usa lenguaje cotidiano; el detalle normativo o técnico se explica en su contexto y con fuente/versionado identificados.

## Reglas compartidas

* Identidad y formato visibles; GTFS Schedule y NeTEx se presentan en secciones y cifras separadas.
* Encabezados jerárquicos, orden de lectura lineal, nombres de enlace descriptivos, idioma español declarado, contraste legible y foco de teclado visible.
* Cada estado combina texto y forma; el color nunca es el único indicador. Abreviaturas y escalas se explican junto al dato.
* Un hallazgo tiene ID estable y vínculo bidireccional a resumen, criterio, evidencia y acción. El destino no depende de que el lector interprete códigos internos.
* Mensajes de error explican qué falló, qué parte no pudo comprobarse y el siguiente paso disponible. Sin falso PASS por falta de evidencia.
* Permitir zoom/reflujo donde el soporte lo admita. No fijar información esencial exclusivamente en gráficos o mapas.

## Pantalla / HTML

Navegación principal por Resumen, Hallazgos y Acciones; filtros visibles con etiqueta y estado actual; controles nativos por teclado, orden de tabulación lógico, foco visible, `aria-live` para resultado de filtros, títulos semánticos y ancla para saltar al contenido. Tabla con encabezados asociados y alternativa textual al resumen gráfico. Mensajes de cero resultados y de filtro inválido. Prototipo: prototype/index.html (referencia local no publicada).

## PDF

Orden de lectura y títulos comprobables; tablas con encabezados identificables y sin depender de posición visual; hipervínculos descriptivos; contraste en impresión y zoom; pies, numeración y encabezados que no ocultan el contenido; mapas/gráficos con leyenda y alternativa textual; campos de metadatos e idioma. La renderización página por página detecta geometría, pero no certifica etiquetado/estructura accesible del PDF.

## Libro (XLSX/hoja de cálculo)

Una tabla por conjunto de datos, una fila de encabezado única, nombres de hoja significativos y sin celdas combinadas en tablas de datos; filtros y primera fila/columna congeladas cuando ayuden; filtros con rótulo e instrucciones; formatos de fecha/unidad consistentes; textos alternativos de gráficos; evitar colores solos; orden de hoja y foco comprensibles; fórmulas y celdas protegidas explicadas. La tarea 19 define requisitos; no acredita implementación/QA de libros si no forman parte del paquete evaluado.

## Estado de comprobación

El prototipo incluye estructura semántica, controles nativos etiquetados, foco visible definido, navegación por anclas, mensaje de estado anunciado, tabla con encabezados y vista estrecha con etiquetas. La inspección visual/interactiva real queda pendiente: el navegador disponible rechazó la URL local `file://` por su política (solo admite HTTP/HTTPS), y no se realizó un servidor alternativo ni se sorteó esa restricción. Por tanto TDL-AUD-19 queda **PARCIAL** hasta comprobar navegación, filtro, teclado, foco y ampliación en navegador. No es auditoría WCAG. Los PDF/libros conservan su QA previo y limitaciones.
