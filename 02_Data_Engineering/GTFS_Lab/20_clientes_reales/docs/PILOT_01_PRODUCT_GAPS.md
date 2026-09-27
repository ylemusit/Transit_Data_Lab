# Pilot Audit 01 — product gaps observed

Solo hechos demostrables en los artefactos existentes. No contiene propuestas de implementación ni interpretación jurídica.

## OBSERVED FACT

- Los cinco outputs contienen informes de validación GTFS Explorer 0.2.1 con filtros nulos (`severities=null`, `categories=null`), por lo que el informe declara alcance sin filtro de severidad/categoría.
- El baseline NAP contiene estado y conteos agregados, pero no rule IDs ni filas de detalle equivalentes; por ello no permite mapear cada regla GTE a NAP.
- GTE produce rule IDs, severidad, categoría, localización, message_key y ocurrencias por detalle; esta granularidad no está presente en el baseline NAP.
- Ancebus, Viagón, Gilsanz y Kbus conservan todos los detalles declarados por sus informes (`omitted_issue_count=0`).
- Bizkaibus declara `1.040.852` incidencias detectadas, conserva `100.000` detalles y omite `940.852`; su detalle no es completo.
- El número total y la severidad no son intercambiables: por ejemplo, Kbus tiene NAP `317` warnings y `0` errores, mientras que GTE conserva `644` errores y `0` warnings.
- El baseline NAP declara recursos externos o capas adicionales (GTFS-RT, NeTEx, SIRI) para Kbus y Bizkaibus que no aparecen como findings del informe GTFS Schedule inspeccionado.
- La información NAP sobre accesibilidad, tarifas y recursos externos no se convierte automáticamente en una regla GTE: el informe GTE solo demuestra los findings contenidos en su payload.

## FUTURE HYPOTHESIS

- No se registra ninguna hipótesis de implementación en esta fase.
