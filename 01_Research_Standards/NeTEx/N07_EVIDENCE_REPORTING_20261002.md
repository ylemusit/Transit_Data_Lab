# NeTEx N07 — evidencia y reporting

El CLI genera un JSON que actúa como findings machine-readable y audit manifest, y un informe Markdown determinista. Incluye identidad/hash del dataset y schema, versión del registry, finding con regla/autoridad/requisito, localizador, observado/esperado, estado/severidad/evidencia/recomendación/provenance, resumen de estados, inventario estructural y gaps. Los paths absolutos y la hora de ejecución no se serializan.

Capas separadas: XML/XSD, perfil, semántica, calidad y alineación regulatoria. El perfil EPIP conserva revisión humana. No se emite `LEGAL_NON_COMPLIANCE`, no se infiere aceptación NAP ni certificación legal.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
