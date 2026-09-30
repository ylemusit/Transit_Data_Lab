# Radiografía de Transit Data Lab — GTFS primero, NeTEx después

Fecha de corte: 2026-09-28. Diagnóstico documental y del estado local observado; no se han ejecutado nuevas importaciones, gates, auditorías de operadores ni cambios en bases protegidas.

## Decisión de enfoque

1. **GTFS Schedule** es la prioridad 1: consolidar el flujo local, cerrar límites concretos de validación y obtener evidencia atribuible al alcance que se quiera ofrecer.
2. **NeTEx** es la prioridad 2: pasar del fragmento `Line` probado a un flujo propio, con perfil y versión elegidos explícitamente antes de ampliar validaciones.
3. **SIRI y GTFS-RT** permanecen `STANDBY`. Su reapertura requiere GTFS y NeTEx estables y una decisión explícita para el nuevo track. No se planifica trabajo operativo realtime en esta hoja de ruta.

`READY` en Compliance V1 significa reproducibilidad **solo dentro de dos scopes técnicos fijados**. No significa soporte completo del estándar, conformidad jurídica ni auditoría de un operador. La prioridad es una decisión de secuencia, no una modificación de la baseline congelada.

## Fuentes y lectura de las infografías

- [Estado vigente](../PROJECT_STATUS.md), [GTFS_Lab V1](../02_Data_Engineering/GTFS_Lab/GTFS_LAB_V1_CURRENT_STATE.md), [Compliance V1](../03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md), [scope](../03_Compliance/COMPLIANCE_V1_SCOPE.md) y [cierre técnico](../03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md) gobiernan las afirmaciones técnicas.
- [Disposiciones por requisito y familia](../03_Compliance/reports/evidence/compliance_v1_20260928/dispositions.md), [informe de estabilización GTFS](../02_Data_Engineering/GTFS_Lab/reports/GTFS_LAB_V1_STABILIZATION_REPORT.md) y [estado Business](../07_Business/BUSINESS_STATUS.md) detallan límites y pendientes.
- [Infografía del 27/09](../08_infografias/Infografia%20del%20proyecto%20a%20dia%2027092026.png): **histórica**. Sus porcentajes de core, validación, análisis, Phase 2 y mapping, y su flujo genérico GTFS/NeTEx/SIRI, ya no describen el estado operativo. Sus porcentajes no se usan como métricas de avance.
- [Infografía del 28/09](../08_infografias/Infografia%20del%20proyecto%20a%20dia%2028092026.png): resumen visual más cercano al estado vigente. Sus tarjetas `IMPLEMENTADO` son ciertas dentro del alcance V1 indicado en la propia imagen; la prueba NeTEx es un fragmento y la prueba GTFS Compliance tiene límites de tamaño. El ejemplo de rutas es ilustrativo, no un resultado auditado.

## Estado comprobado por área

| Área | Lo que existe | Lo que todavía falta o limita el uso |
| --- | --- | --- |
| GTFS_Lab | Pipeline local reproducible ZIP Schedule → inventario/hash → DuckDB aislada → integridad/reglas → análisis/calendario → GIS GeoJSON/KML → informe. Gate y E2E sintéticos PASS. Dry run Asturias: ingestión, reglas locales, análisis, DuckDB y GIS completados, cero hallazgos locales. | Catálogo de tablas acotado, sin parser completo de todas las entidades Schedule, UI ni auditoría legal. El evaluador Compliance congelado limita cada archivo a 1 MiB y 10.000 filas: Asturias tiene 21.015 `trips`, por lo que devuelve `INSPECTION_ERROR`, sin finding del operador. Un solo feed real no prueba cobertura de tipos de feeds ni desempeño general. |
| Compliance GTFS | Una regla técnica reproducible sobre `stop_times.trip_id → trips.trip_id` y `stop_times.stop_id → stops.stop_id` para paradas fijas. 18 casos sintéticos en el piloto. | No valida horarios, calendarios, tarifas, flex ni feed completo; no hay observaciones de operadores. Una ampliación exige scope, versión/fuente, fixtures y gate nuevos, sin reinterpretar el V1 cerrado. |
| NeTEx | Scope técnico separado: fragmento global `Line` con identidad/`Name`, validado contra XSD EPIP fijado basado en NeTEx 1.3.1; 10 casos sintéticos. Fuente, versión y hashes preservados en Compliance. | `NeTEx_Lab` no tiene pipeline propio. No se ha probado `PublicationDelivery` completa, relaciones entre frames, perfil nacional aplicable, datos reales de operador ni conversión GTFS↔NeTEx. El artefacto EPIP utilizado está declarado no mantenido: su elección futura requiere evaluación explícita. |
| Research & Standards | Referencias y fuentes fijadas dentro de Compliance. | El área `01_Research_Standards` está planificada, sin implementación de catálogo transversal observada. La selección de perfil/versionado para una ampliación NeTEx sigue pendiente. |
| Interoperability | Relaciones semánticas y mappings parciales en Compliance. | `04_Interoperability` conserva estructura planificada; no hay crosswalk operativo ni prueba de conversión, pérdidas, ida/vuelta o equivalencia 1:1. |
| Audits | Evidencia histórica de 20 operadores bajo GTFS_Lab y resultados técnicos de fixtures. | `05_Audits` está planificada. Cero observaciones Compliance sobre operadores; sin auditoría normativa integral ni informe de conformidad. Los datasets históricos no son clientes comerciales. |
| Products | GTFS Explorer Desktop mantiene identidad y repositorio independientes; baseline protegida `v0.2.2`. | Los cambios locales del producto y su aceptación visual/nativa son asunto de su propio repositorio. El estado del contenedor no certifica automáticamente el producto. |
| Business | Baseline V1 congelada; Stage 1 aprobado documentalmente y Stage 2 preparado en documentación. | Phase 3 sigue en curso. Demanda, disposición a pagar y diferenciación siguen sin validar. Contacto externo no autorizado. El inventario Business V1 describe una foto anterior a GTFS_Lab/Compliance V1; sus clasificaciones de capacidades no se actualizan implícitamente. |

Compliance conserva 92 provisions, 36 source facts, 48 requisitos y 10 deadlines en Phase 1/2 congeladas. Phase 3 está `CLOSED_WITH_DEFERRALS` para V1: **0 requisitos completos**, 6 parciales, 12 de revisión humana, 20 diferidos y 10 fuera del scope V1; 9 familias, ninguna completa. Hay 15 mappings y 10 decisiones de coverage (9 `PARTIAL`, 1 `UNRESOLVED`), 2 reglas técnicas y 28 observaciones **sintéticas**. El gate vigente registrado es PASS y mantiene explícito un FAIL histórico de un gate anterior que esperaba `audit.rules=0`.

## Brechas que determinan el orden de trabajo

| Orden | Brecha | Por qué importa | Criterio observable para cerrarla |
| --- | --- | --- | --- |
| G1 | Contrato de GTFS Schedule objetivo y matriz de cobertura | El pipeline V1 funciona en un subconjunto; “validación GTFS completa” excede la evidencia. | Inventario de entidades/reglas soportadas, no soportadas y no evaluables, ligado a versión de referencia y fixtures; resultados por alcance, sin porcentaje global inventado. |
| G2 | Límite del evaluador Compliance GTFS frente a feeds reales | Asturias excede 10.000 `trips`; hoy la regla no puede inspeccionar ese caso. | Decisión explícita de evolución V2 o inspección segmentada con semántica y controles de completitud demostrados; gate nuevo, feed grande de prueba y preservación de V1. Hasta entonces, conservar `INSPECTION_ERROR`. |
| G3 | Evidencia GTFS real, comparable y reproducible | Un dry run y fixtures no demuestran robustez en distintas estructuras ni atribuyen el resultado a un operador. | Muestra autorizada con procedencia, permisos, hashes, versión de evaluador, resultados completos y revisión de falsos positivos; separar hallazgo técnico de conclusión jurídica. |
| N1 | Perfil y artefactos NeTEx aplicables | El XSD EPIP V1 solo prueba `Line` y no acredita un perfil español o entrega completa. | Decisión documentada de caso de uso, perfil, versión, constraints, fuente y aplicabilidad, con artefactos verificables y fixture mínimo representativo. |
| N2 | Pipeline NeTEx propio | La prueba vive en Compliance; no existe la experiencia ZIP/XML → inventario → validación → resultados del laboratorio. | Ingesta segura y trazable de un paquete NeTEx, validación estructural y de referencias en el scope elegido, resultados reproducibles y gate aislado. |
| I1 | Relación GTFS↔NeTEx | Los dos pilotos prueban propiedades diferentes; no hay conversión general. | Crosswalk **por concepto y caso de uso**, pérdidas/ambigüedades documentadas y pruebas de ida o vuelta solo donde tengan sentido; sin prometer equivalencia general. |
| C1 | Contexto normativo/NAP y evidencia de operador | Un formato no prueba publicación, acceso, fecha, institución, calidad ni solicitudes. | Evidencia contextual por requisito, revisión humana cuando corresponda y separación de resultado técnico, legal y comercial. F05–F08 requieren registros de cambios, calidad, reutilización y solicitudes. |
| D1 | Sincronización documental | `PROJECT_STRUCTURE.md` y la baseline Business contienen afirmaciones históricas de componentes pendientes; pueden inducir un plan erróneo si se leen como actuales. | Mantener `PROJECT_STATUS.md` como entrada vigente; revisar esas vistas en tareas documentales específicas, conservando las baselines congeladas. |

## Secuencia propuesta y gates

| Hito | Trabajo concreto | Entregable y salida mínima | Dependencia |
| --- | --- | --- | --- |
| **P1 · GTFS cobertura** | Fijar el caso de uso principal y matriz de archivos, campos, relaciones y reglas; separar GTFS_Lab de Compliance. Priorizar referencias, calendario/horarios y formatos de salida según evidencia de feeds. | Matriz versionada + fixtures positivos, negativos y `NOT_EVALUABLE`; gate focalizado PASS. | Estado V1 preservado. |
| **P2 · GTFS escala y evidencia** | Resolver el límite G2 mediante un contrato nuevo; ejecutar una muestra de feeds autorizados de tamaños y estructuras distintos, con revisión de falsos positivos. | E2E repetible y resultados completos para los casos dentro de scope; errores y límites explícitos; hashes de entradas y build. | P1 y decisión sobre contrato V2. |
| **P3 · NeTEx perfil** | Elegir caso de uso y artefactos normativos/técnicos aplicables; registrar diferencias con EPIP 2021. | Decisión de perfil/versionado, corpus mínimo con procedencia y matriz de entidades/constraints. | GTFS estabilizado en el alcance objetivo. |
| **P4 · NeTEx laboratorio** | Construir ingesta, validación y reporting para el scope elegido; probar publicación y relaciones solo si las cubren los artefactos fijados. | Gate sintético y E2E con paquete representativo; estados `PASS`/`FAIL_TECHNICAL`/`NOT_EVALUABLE`/`INSPECTION_ERROR` trazables. | P3. |
| **P5 · Interoperabilidad acotada** | Comparar conceptos realmente presentes en ambos pipelines y documentar transformaciones o imposibilidad. | Crosswalk con pérdidas y pruebas por caso; ninguna conversión general implícita. | P2 y P4. |
| **P6 · Auditoría y producto** | Definir alcance por operador/requisito, evidencia contextual, revisión jurídica y aceptación del producto en su propio repositorio. | Informe con alcance y limitaciones, evidencia técnica separada de revisión jurídica y validación comercial. | Pipelines y autorizaciones correspondientes. |

Cada hito es una propuesta de trabajo futuro, **no** una declaración de inicio o de autorización para importar nuevos datos, tocar baselines, abrir una fase Business, contactar terceros o publicar. El primer trabajo ejecutable es P1; al cerrarlo habrá una lista medible de reglas y entidades GTFS antes de ampliar el motor. No se asignan porcentajes de avance sin denominador verificable.

## Límites de esta radiografía

Se han inspeccionado los documentos vigentes, la salida guardada del gate Compliance, los dos PNG y la presencia/ausencia de archivos en los laboratorios y áreas planificadas. No se ha reejecutado el gate ni verificado de nuevo el contenido de bases o feeds, la interfaz Desktop, licencias de datasets o requisitos legales actuales. Las cifras de pruebas y de Asturias proceden de informes fechados del 28/09; cualquier ejecución posterior debe registrar su propia evidencia. Los directorios de productos anidados no se han inspeccionado.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
