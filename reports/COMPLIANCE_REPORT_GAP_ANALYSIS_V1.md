# Compliance → informe de cliente — análisis de gaps V1

**Estado:** análisis documental basado en el código y los contratos de `origin/main` 9734d800. No modifica Compliance V1, Phase 1/2 congeladas, la base Compliance ni fuentes capturadas.

## Alcance y cadena revisada

Se revisó el flujo persistido `03_Compliance` → `compliance_adapter.inspect_fixed_stop_references` → `pipeline.run` → `g09_reporting.build_engine_report` → `client_workflow._finding_rows` → `report/client_report.md` y PDF. El scope normativo de Compliance V1 permanece `CLOSED_WITH_DEFERRALS`; su estado y límites constan en `03_Compliance/COMPLIANCE_V1_CURRENT_STATE.md` y `03_Compliance/reports/COMPLIANCE_V1_FINAL_CLOSURE_REPORT.md`.

La cadena documental trazable existe en Compliance para sus requisitos revisados: fuente y versión → provision/source fact → requirement → concepto → scope/representación → observación/regla técnica → resultado/evidencia. Para el scope GTFS concreto, el informe maestro ejemplifica `EU-REG-2017-1926` (consolidación fijada) → source fact / requirement A04-P01 → `V1-CPT-GTFS` → capability/mapping → `V1-SCOPE-GTFS` → `V1-REP-GTFS` → fixture/hashes y locator → `V1-OBS-*` → `V1-RULE-GTFS` → resultado técnico. La cadena upstream no implica que todo el detalle se exporte al artefacto de auditoría cliente.

## Hallazgos A–H

| Clase | Resultado verificable | Consecuencia para informe | Tratamiento |
|---|---|---|---|
| A. Producido y reportado | El run conserva identidad/hash del dataset, resultado global Compliance V1, rule/evaluator version y hashes del evaluador/referencia cuando están disponibles; findings por origen conservan locator y evidencia. | El informe actual ya muestra resultado técnico y Compliance y referencia artifacts. | Mantener; incluir esos identificadores con enlaces de artefacto. |
| B. Producido y perdido | G09 serializa por regla estado, versión, autoridad, requirement, cobertura y estado de recomendación. El informe cliente sólo presenta resumen de validation/Compliance y no proyecta filas por regla. La matriz de validaciones ejecutadas se pierde en el límite de presentación. | El cliente no puede distinguir el resultado de cada check ni consultar cobertura completa desde la narrativa. | Gap de puente confirmado. Proyectar la matriz desde artefactos ya producidos. |
| C. Representado ambiguamente | `NOT_EVALUABLE`, `NOT_APPLICABLE`, errores de inspección y fallos técnicos existen en motores, pero el resumen cliente agrupa la evaluación en pocos estados globales; no expone aplicabilidad/evaluabilidad y conteos por regla. Un resultado Compliance técnico puede confundirse con evaluación legal si no se acota. | Se difuminan no aplicable/no evaluable y el límite de una inspección técnica. | Presentar vocabularios explícitos y disclaimer acotado. |
| D. Genuinamente ausente en artefacto de auditoría | El run Compliance no adjunta una relación por finding cliente que materialice los 48 requirements/familias con disposición Phase 3, cita/URL, fecha/versión jurídica y conclusión de aplicabilidad para ese dataset. El adapter expone un scope y una referencia técnica hashada, no un dictamen normativo por requisito. | No se puede crear un inventario de normas aplicables ni asignar `CURRENT/SUPERSEDED/REPEALED` desde el resultado de una auditoría. | Mostrar explícitamente el dato ausente/`VERSION_UNKNOWN`; no construir un segundo motor regulatorio ni inferir vigencia. |
| E. NOT_EVALUABLE intencional | Los evaluadores preservan `NOT_EVALUABLE` y `INSPECTION_ERROR` ante entrada parcial, evidencia insuficiente o fallo seguro del adapter; G09 recoge gaps de etapa/regla. | Ocultarlo como PASS o FAIL alteraría semántica. | Mostrar regla, estado, cobertura conocida y motivo/referencia cuando exista. |
| F. NOT_APPLICABLE | Las reglas por etapa conservan `NOT_APPLICABLE` para condiciones de archivo/feature fuera de la entrada; Compliance diferencia límites de scope. | No debe mezclarse con fallo ni con no evaluable. | Incluir una sección de reglas no aplicables y conservar el estado original. |
| G. Fuente superseded/repealed/version unknown | Compliance conserva identidades/hashes y snapshots, pero la proyección cliente no incluye catálogo de fuente jurídica por resultado ni estado de vigencia aplicable al feed. Una captura/hash técnico no demuestra por sí sola vigencia normativa. | La versión/estado legal de fuente no puede rellenarse con seguridad en el renderer. | Sólo publicar estado demostrado; para artefacto sin versión jurídica asociada, `VERSION_UNKNOWN`. |
| H. Diseño/cosmética, no gap de motor | Jerarquía narrativa, nombres de secciones, etiquetas, tablas e impresión son propiedades de presentación. | No justifican cambios de parser, reglas ni persistencia Compliance. | Resolver en renderer/modelo PDF existente. |

## Contrato de informe

El gap B/C/H justifica ampliar la capa de presentación existente mediante una vista cliente determinista, JSON y Markdown, y usarla en el PDF existente. La especificación está en `02_Data_Engineering/GTFS_Lab/spec/client_report_contract_v1.json`; contiene las 29 secciones, vocabularios y prohibiciones de inferencia. La proyección utiliza manifest, run/engine report, findings, interpretación y Compliance ya persistidos; no muta findings RAW ni reinterpreta decisiones upstream.

La matriz contiene cada regla de G03–G08 y validador legacy observado en los artefactos, más la fila acotada del resultado Compliance. Evidencia se enlaza por ID/ruta al paquete entregado. Los valores no disponibles se mantienen como `VERSION_UNKNOWN`, `NOT_EVALUABLE` o explicación explícita. La recomendación de publicación sólo se emite cuando la matriz es reconocible, no hay gaps del motor y `accounting_gap = 0`; la conclusión sigue limitada al alcance técnico de la ejecución.

## Criterio de cierre y límites

Este análisis **no** concluye cumplimiento jurídico, fuente vigente, aplicabilidad legal para un operador, aceptación NAP, cobertura GTFS universal ni preparación comercial. No cambia requisitos, facts, mappings, filas Compliance, reglas audit.rules, fuentes, hashes, snapshots ni contratos persistentes. El gate humano/regulatorio de Compliance permanece inalterado.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
