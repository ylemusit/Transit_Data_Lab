# Alineación de fuentes y publicación sanitizada — 2026-10-10

La integración reúne código y tests existentes de auditoría profesional, reglas opt-in, contexto NeTEx, seguimiento, replay y método de calidad. Añade una captura verificable de la fábrica sintética CS Autobuses y CI portable. No absorbe los repositorios independientes de GTFS Explorer.

Los informes aplicados a operadores, paquetes cliente, capturas privadas y recibos completos quedan fuera de Git. Los originales de los documentos sanitizados se conservan en una copia preintegración verificada. Los ejemplos públicos de encargo son sintéticos. Las fuentes jurídicas oficiales seleccionadas conservan sus bytes y sus hashes; las excepciones de whitespace se limitan a tres capturas HTML con líneas originales de tabuladores.

Se retiran dependencias de P: de dos tests mediante temporales y una sustitución acotada del guard durante la prueba. Las raíces autorizadas de producción siguen vigentes. La suite `tools.test_audit_corpus_reference_v1` requiere capturas y fixtures locales: está separada del gate portable, sin declarar su resultado a partir de CI.

Comprobaciones locales de esta integración: 83 tests de contratos/método, 73 regresiones GTFS/presentación y 16 tests NeTEx, todos PASS. Los 37 archivos originales de fábrica coinciden con su manifest tanto en disco como en los blobs preparados para Git; generación aislada de un ZIP DEMO con 32 miembros únicos, raíz plana y CRC correcto. El escaneo de candidatos no encuentra patrones de claves privadas o tokens conocidos; no constituye una auditoría universal de secretos.

La limpieza previamente autorizada retiró 1.623 archivos y 74.152.440 bytes, conservando 21 JSON históricos y tres marcadores de caché. Sus manifests y recibos completos permanecen en el expediente local. No se vuelve a ejecutar esa limpieza.

CI y estado de publicación deben contrastarse con el SHA final del PR. Estos resultados no acreditan aceptación GIS/NAP, conformidad jurídica, revisión humana, lanzamiento público ni validación comercial.
