# Preparar una nueva ejecución tras un estado terminal

- **CONTEXT:** La GUI instalada había terminado una auditoría y el usuario seleccionaba otra entrada.
- **PROBLEM / ROOT_CAUSE:** La disponibilidad solo aceptaba IDLE/READY; el estado terminal impedía rearmar el flujo.
- **DECISION_OR_SOLUTION:** Preparar el nuevo run liberando referencias GUI previas y deshabilitando resultados antiguos; conservar salidas en disco y generar audit_id al iniciar.
- **EVIDENCE / RELATED_COMMITS_OR_REPORTS:** [Fuente autoritativa](https://github.com/ylemusit/Transit_Data_Lab/blob/cf4e0a30f6837b077e6994305f51fbf2cca8282c/reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W08_PACKAGING_RELEASE.md).
- **IMPACT:** APPLICATION_DEFECT_001 quedó CLOSED_FIXED_AND_VERIFIED tras el retest humano documentado.
- **REUSABLE_LESSON:** Probar secuencias completas éxito→nueva entrada y cancelación→rerun en el paquete real; el arranque aislado no cubre el ciclo de vida.
- **STATUS:** Retenido; alcance y límites de la fuente, sin nueva certificación.
