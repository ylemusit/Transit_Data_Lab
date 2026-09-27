# Capability gaps

Fecha de revisión: 2026-09-27. Visión Business de obstáculos probatorios. No es backlog técnico: no se asignan responsables, plazos, prioridades de implementación ni cambios a GTFS_Lab/Compliance. Las condiciones siguientes describen qué evidencia falta para ampliar una afirmación, sin autorizar su obtención ni corregir el producto.

| Gap | Capability IDs | Evidencia | Obstáculo observado | Efecto sobre lo defendible / evidencia que falta |
| --- | --- | --- | --- | --- |
| G-01 | TDL-CAP-001/002/003/004 | TDL-EVD-001/006/008 | Un baseline Asturias, sin cobertura representativa; importación no replayada. | Acotar la demostración a esta fuente; falta ejecución independiente de ingestión y cobertura de otras estructuras. |
| G-02 | TDL-CAP-006/007/008 | TDL-EVD-001/002/006/008 | core, validation y analysis ausentes; 4 FAIL de ausencia en sentinel. | No afirmar motor tipado, validador integral ni análisis persistido; faltan implementación y resultados identificables. |
| G-03 | TDL-CAP-005 | TDL-EVD-009/008 | KML conservados sin generador GIS. | Solo existencia de artefactos; falta método reproducible y validación geométrica regenerable. |
| G-04 | TDL-CAP-001/004/013 | TDL-EVD-005/008/016 | README Lab vacío, rutas relativas/históricas y tres local_file absolutos en Compliance; main.stops sin finalidad documentada. | Operación/portabilidad parcial; faltan contrato operativo y demostración fuera del entorno actual. No cambiar los paths protegidos. |
| G-05 | TDL-CAP-009/010 | TDL-EVD-011/012/013 | Anomalías Annex 1.3 B-I/D-I y textual_fidelity_certified=false. | Hash válido acredita binario, no fidelidad del corpus normalizado; falta evaluación de fidelidad. |
| G-06 | TDL-CAP-010/011/013 | TDL-EVD-011/016/018/019 | Siete dependencias externas PARTIAL; decisiones humanas y generadores de Gate 1/2 no independientes. | No extractor jurídico autónomo ni replay automático; falta demostración integral con inputs históricos y decisiones explícitas. |
| G-07 | TDL-CAP-014/015 | TDL-EVD-010/011/020 | Mapping vacío, cero reglas/runs/resultados; legal_compliance_assessed=false. | Solo infraestructura iniciada; faltan mappings, motor y resultados trazables. Sin conformidad, garantía ni certificación. |
| G-08 | TDL-CAP-012/013 | TDL-EVD-015/017 | Tests históricos tienen assertions de fase que no corresponden a la base posterior. | Las suites deben atribuirse al estado adecuado; no usar un mismatch histórico como fallo actual ni exigir PASS de un estado superado. |
| G-09 | TDL-CAP-016/019 | TDL-EVD-021/022/024 | 20 entradas de investigación, solo cinco casos del piloto; NAP sin rule IDs suficientes. | Sin clientes comerciales ni equivalencia/superioridad de validadores demostrada; faltan denominadores y comparabilidad regla a regla. |
| G-10 | TDL-CAP-017/019 | TDL-EVD-024/025/027 | Outputs de distintas versiones/procedencias; rc002 no canónico, hallazgos enum invalidados; aceptación run_004 declarada sin forense revalidado dentro del alcance. | No extrapolar comportamiento actual ni calidad de Bizkaibus a partir de 1.040.852 falsos positivos. Falta cadena probatoria independiente de build vigente dentro de un alcance autorizado. |
| G-11 | TDL-CAP-018/020 | TDL-EVD-024/026 | Export de datos no export de findings; selección JSON Kbus AH/H/L2/L3 con solo AH/H/L2 en routes, sin completitud demostrada; grandes runs históricos no prueban totales completos por regla; modelo Audit/Quality conceptual. | Falta contrato implementado de poblaciones, agregados y completitud. El truncado histórico no se atribuye al producto vigente. |
| G-12 | TDL-CAP-001/009/010/012/013 | TDL-EVD-001/011/016 | Git padre sin commits; DB/feeds ignorados; congelación por registros y hashes. | Reproducibilidad local acotada, no entrega versionada integral/portable ni baseline de ejecución end-to-end del contenedor. |
| G-13 | TDL-CAP-001/016/018/019 | TDL-EVD-003/021/022/026 | Presencia de datos/snapshots no demuestra permisos de redistribución o explotación. | No se afirma autorización comercial de reutilización. Evaluación jurídica/comercial fuera de esta fase. |

## Degradaciones explícitas

GIS reproducible (TDL-CAP-005), replay integral Compliance (TDL-CAP-013) y validación vigente atribuible a build (TDL-CAP-017) permanecen PENDING_VERIFICATION. El validador propio GTFS_Lab y el análisis persistido son PLANNED (TDL-CAP-007/008). Mapping y auditoría operativos son IN_DEVELOPMENT (TDL-CAP-014/015), con avance limitado a DDL/tablas. Un directorio, un test parcial, un KML o una tabla vacía no acreditan esas capacidades.

El corpus, los requisitos materializados y sus gates sí se clasifican EXISTING en su alcance técnico acotado. Ningún estado de capacidad constituye evaluación jurídica, homologación o garantía de cumplimiento.

## Límite de continuidad

El inventario y sus gaps se integran en BUSINESS_CAPABILITY_BASELINE_V1, congelada tras revisión final autorizada de 2026-09-27. La congelación mantiene abiertos estos gaps y no amplía afirmaciones. No se inicia Business Phase 3, no se define oferta y no se abre trabajo técnico derivado de estos gaps.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

