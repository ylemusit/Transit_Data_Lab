# Capacidad estática GTFS y NeTEx en las líneas de auditoría — alcance y brechas

Actualizado: 2026-10-09. Este documento compara las líneas de auditoría GTFS_Lab y NeTEx_Lab con un servicio de generación y despliegue. El alcance considerado aquí es solo GTFS Schedule y NeTEx estáticos; GTFS-RT y SIRI quedan excluidos. El [piloto de Viagón](../02_Data_Engineering/GTFS_Lab/20_clientes_reales/FAMILY_A_SMALL_BASIC/005_viagon/03_gtfs_explorer/README.md) contiene capturas y artefactos exportados por GTFS Explorer Desktop 0.2.1, ejecutado externamente; no se ha verificado ese ejecutable como componente del flujo de auditoría ni como productor integral GTFS↔NeTEx.

| Capacidad | Estado comprobado | Qué falta para ofrecerla como servicio a otro operador |
|---|---|---|
| Auditar GTFS Schedule | Motor técnico G03–G08 y entrega local de informes; se añade un diagnóstico opt-in de condiciones `agency_id`. | Validar el conjunto de reglas contra el alcance y contrato de cada cliente; ejecutar con su fuente identificada y revisión de resultados. |
| Auditar NeTEx | XML seguro, XSD 2.0.0 fijado, identidad y separación explícita del perfil; se añade un candidato opt-in de referencias locales. | Texto controlado del perfil/destino (por ejemplo, el perfil que exija cada NAP), catálogo completo y expectativas revisadas. La validez XSD no basta. |
| Generar GTFS | GTFS_Lab audita feeds; no incluye un productor de feeds de operador. El piloto conserva salidas de un ejecutable de escritorio externo. | Verificar el alcance real del exportador existente si se pretende reutilizarlo; además, definir modelo de entrada, responsable de la fuente, campos, asignación y ciclo de versión para la generación íntegra. |
| Convertir GTFS ↔ NeTEx | No hay un convertidor GTFS↔NeTEx integrado en estas dos líneas ni un modelo canónico de producción. | Correspondencias autorizadas para calendarios, servicios, paradas, recorridos, viajes, horarios, identificadores, zonas horarias y extensiones; reglas explícitas para datos que no se pueden representar en ambos formatos. |
| Desplegar/publicar feeds | No hay publicación remota de feeds. Los ZIP, informes y paquetes actuales son entregas locales/de revisión. | Destino por cliente, protocolo, titularidad, autorización, formato del paquete, validaciones de puerta, rollback, observabilidad y responsabilidades operativas. |
| Operación recurrente | Existe seguimiento interno de versiones y correcciones con recorridos sintéticos; no existe operación periódica con un productor real. | Calendario acordado, recepción de nuevas versiones, comparación, correcciones devueltas por el productor, nueva ejecución y aceptación del operador. |

## Dependencias para iniciar una implementación de producción

1. Un feed o modelo de entrada autorizado y un ejemplo de salida esperado, con su origen, versión, licencia y propietario identificados.
2. Perfil NeTEx y destino de publicación nombrados por el operador. Si se exige conformidad NAP, se necesita el texto y la versión de sus reglas y el catálogo de referencia aplicable.
3. Un contrato GTFS↔NeTEx acordado, incluidos los campos sin correspondencia y quién decide cómo representarlos.
4. Entorno de despliegue, permisos, cadencia, mecanismo de recuperación y criterio de aceptación acordados.

Hasta que se determinen esas entradas y se verifique el alcance del exportador externo, producir una salida GTFS/NeTEx genérica podría ser sintácticamente plausible y aun así no servir al operador. Las líneas de auditoría pueden continuar con ejecución local y evidencia técnica, pero no afirmar capacidad integral de generación, conversión, publicación ni aceptación de destino.

## Evidencia relacionada

- [Estado GTFS_Lab](../02_Data_Engineering/GTFS_Lab/README.md): auditoría, informes locales y exclusiones.
- [Estado NeTEx_Lab](../02_Data_Engineering/NeTEx_Lab/README.md): alcance XSD/perfil y dependencia de texto controlado.
- [Implementación de TDL-AUD-12/13](audit_battery_v1/TDL_AUD_12_13_IMPLEMENTATION_20261009.md): extensiones opt-in y límites.
- [Seguimiento interno de correcciones](audit_lifecycle_v1/README.md): recorridos sintéticos, separados de respuesta/aceptación real del productor.

## Comprobación del exportador disponible

La inspección de solo lectura de `20_clientes_reales/04_audit/pilot_01/gte_output_inventory.json` registra cinco runs, 43 artefactos inventariados y 14 nombres `gtfs-export-*` para GTFS Explorer 0.2.1. Entre estos últimos hay seis JSON más sus manifiestos, un CSV más manifiesto y un ZIP más manifiesto; los nombres observados están acotados por ruta/servicio y el único ZIP inventariado es `gtfs-export-route-...zip` de Bizkaibus.

No se encontró el ZIP ni los JSON/CSV enumerados en el directorio de run de Bizkaibus del checkout activo; allí solo constan tres archivos (captura, manifiesto HTML y `project.json`). Por tanto, la evidencia comprobada permite afirmar que el inventario histórico registra **exportaciones seleccionadas por ruta**, pero no permite inspeccionar su contenido ni confirmar un ZIP GTFS completo, reproducir la exportación, revisar código fuente o transferir esa capacidad a la baseline actual 0.2.2. Estado: `FULL_FEED_PRODUCER = NOT_VERIFIED`; no incorporar este exportador como componente de producción sin una revisión específica de producto y de contenido.

Para preparar el mapping sin fijar decisiones de un cliente, se añade el [registro de correspondencias GTFS↔NeTEx V1](GTFS_NETEX_MAPPING_REGISTER_V1.md). Es un borrador interno: todos los valores de operador/perfil/destino están pendientes y no habilita generación.
