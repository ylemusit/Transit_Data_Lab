# GTFS Client Audit Workflow V1 — diseño y contrato

**Estado:** implementación técnica P01–P08 con evidencia E2E sintética; P09 cierre humano pendiente. Este documento registra el design review desde `origin/main` `455b5e4cc9b3b716f5edfb27b3c69182f52316bf`.

## Design review: capacidades reutilizables

| Capacidad | Fuente existente | Uso V1 / límite |
|---|---|---|
| Intake ZIP, límites y CSV | `gtfs_lab.ingestion` | Reutilizar `load_dataset` y sus límites; no duplicar parser. |
| Identidad y SHA del input | `core.DatasetIdentity`, `audit_contract` | Registrar identidad cliente adicional en el nuevo contrato; preservar manifest M01 1.1.2. |
| SOURCE freeze | `audit_persistence.persist_audit` | Reutilizar verificación hash antes/después; añadir copia de zona inmutable. |
| Audit Engine G03–G08 y findings | `pipeline.run`, `g09_reporting` | Orquestar reporte técnico; preservar G03–G08 como origen independiente. |
| Compliance | `pipeline.run`, `compliance_adapter` | Ya ejecutado por el pipeline; extraer salida separada, no inferir conclusión jurídica. |
| Findings legacy | `validation` y normalización M02 | Mantener `LEGACY` separado del Audit Engine y Compliance. No afirmar equivalencia. |
| Remediación | `remediation.create_proposal` | Evaluación humana; el adaptador existente es específico del caso DEVELOPMENT 010 y no es un remedidor genérico. |
| Re-audit / comparación | `audit_comparison` + ChangeAttribution 1.1 | Usar dos runs aceptados; distinguir incomparabilidad de cambio de datos. |
| Reporting | `g09_reporting`, `pipeline.render_report` | Añadir informe cliente, conservar límites y no inventar score. |
| GIS | `gis` dentro de `pipeline.run` | Evidencia opcional útil; no gate universal. |
| Evidence, manifests, provenance | `audit_persistence`, `corpus_provenance`, manifests existentes | Manifests separados por contrato; artefactos de delivery con hash. |
| Replay determinista | pipeline y gates sintéticos/G10 | Fijar hashes/versions; comprobar estabilidad en P08. |

El flujo no cambia Trust Foundation, Audit Engine V1, Compliance V1 ni Remediation Engine V1. `SOURCE`, `WORKING`, `DERIVED`, `AUDIT` y `DELIVERY` quedan físicamente separados. No se persisten rutas locales en DELIVERY; no se usa servicio externo.

## Contrato de entrada

Entrada inicial: un `GTFS.zip` local válido. No requiere backend ni cuenta. Campos obligatorios y vocabularios: [client_audit_contract_v1.schema.json](../spec/client_audit_contract_v1.schema.json). `client_project_id` y `audit_id` son identificadores locales, nunca ramas de código específicas por operador. Metadata adicional es opcional y no debe incluir secretos.

`dataset_id` se deriva del SHA-256 (`GTFS-` + 16 primeros hex); `source_filename`, timestamp UTC, tamaño y provenance se registran en ingestión. SOURCE es una copia verificada de los bytes recibidos y se vuelve a hashear al terminar. El input externo original no se reescribe.

## Zonas y etapas

| Etapa | Input → output | Estados / fallo | Evidencia y replay |
|---|---|---|---|
| 1 Intake | ZIP → identidad | aceptado / `BLOCKED_INPUT_INVALID` | nombre, tamaño, SHA, provenance; reintento con nuevo audit_id. |
| 2 Freeze | bytes recibidos → `SOURCE/` | verificado / `BLOCKED_TECHNICAL` | hash y tamaño antes/después; no se modifica SOURCE. |
| 3 Identity | fuente congelada → `dataset_identity.json` | registrado / bloqueado | contract v1 y timestamp UTC. |
| 4 Preconditions | SOURCE copiado a WORKING → parser checks | válido / input inválido | límites y errores de ingestion; no omitir `NOT_EVALUABLE`. |
| 5 Audit Engine | WORKING → run + evidence G03–G08 | estado nativo por regla | versión, rules, findings, cobertura y gaps. |
| 6 Compliance | mismo run → Compliance V1 | `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `INSPECTION_ERROR` | evaluator y hashes referenciados por salida existente. |
| 7 Consolidation | Engine + Compliance + legacy → `findings.json` | consolidado / revisión humana | cada fila mantiene `origin`; no colapsar semánticas. |
| 8 Remediation assessment | findings → `remediation.json` | `AUTO_SAFE`, `HUMAN_REVIEW`, `NOT_REMEDIABLE`, `OUT_OF_SCOPE` | V1 por defecto no ejecuta propuestas genéricas; autorización y evidence case-specific requeridas. |
| 9 Safe remediation | propuesta humana aprobada → DERIVED | aplicado / no elegible | solo mecanismo autorizado existente; SOURCE intacto. |
| 10 Re-audit | DERIVED + baseline → comparación | comparable / no comparable | dos runs completos; comparación separa hash de datos y versiones. |
| 11 GIS | resultado + pregunta geográfica → artefactos GIS | útil / no aplica | salida heredada; GIS no bloquea findings no espaciales. |
| 12 Report | evidence → Markdown cliente | generado / bloqueado | catorce secciones mínimas; claims jurídicos excluidos. |
| 13 Evidence package | manifests y salidas → DELIVERY | hashes verificados / error técnico | no duplica copias de la fuente. |
| 14 Delivery manifest | artefactos → manifest + seal | completo / incompleto | SHA-256, tamaños, versions, gaps, deferrals. El seal externo resuelve el hash autorreferencial del manifest. |
| 15 Archive/baseline | paquete sellado → conservación | elegible / diferido | comparación futura por audit_id; sin promoción automática. |

Estructura de workspace: `SOURCE/<zip>`, `WORKING/<zip>`, `DERIVED/`, `AUDIT/` (runs, identity, findings, Compliance, decision/comparison) y `DELIVERY/` (manifest, informe, evidencias). Ningún archivo temporal se presenta como evidencia salvo que el manifest lo incluya.

## Estados y findings

Estados globales: `COMPLETED`, `COMPLETED_WITH_FINDINGS`, `COMPLETED_WITH_LIMITATIONS`, `BLOCKED_INPUT_INVALID`, `BLOCKED_TECHNICAL`, `HUMAN_REVIEW_REQUIRED`. Los estados nativos por regla se preservan. El finding cliente incluye origen, regla/versión, autoridad, severidad, requisito, estado técnico, archivo/locator/campo, evidencia observada, recomendación, elegibilidad de remediación y hash/provenance disponible. La presentación no reasigna severidad ni produce score global.

## Reporte cliente

El reporte incluye: resumen, identidad, alcance, metodología, findings técnicos, calidad, alineación Compliance, remediación, before/after, evidencia geográfica cuando aplique, limitaciones, diferimientos, recomendaciones y apéndice reproducible. No declara certificación, cumplimiento jurídico definitivo, conformidad GTFS total ni garantía operacional.

## Delivery y reproducibilidad

`audit_manifest.json` contiene audit/client IDs, hash fuente, versiones de workflow/motor/Compliance/Remediation, mapa de versiones de reglas ejecutadas, timestamps, artefactos y sus SHA/tamaños, gaps y diferimientos. `delivery_seal.json` fija el hash del manifest final. El auditor puede ligar informe y evidence a un input y ejecutar comparación de dos runs aceptados.

El runtime actual no expone una única identidad serializada del RuleRegistry G02 para G03–G08. Por ello el delivery identifica los mapas de versiones realmente ejecutados y su hash canónico; Compliance conserva por separado rule, evaluator y reference SHA. No se inventa un hash de registry ausente.

## Gates propuestos

| Gate | Condición de cierre |
|---|---|
| P01 CONTRACT | Contrato versionado y estados/zonas aprobados técnicamente. |
| P02 INTAKE / FREEZE | ZIP válido, hash y tamaño estables; invalidación explícita. |
| P03 ORCHESTRATION | Engine y Compliance ejecutados sin cambios a sus contratos. |
| P04 FINDINGS | Findings tipados con origen intacto y `NOT_EVALUABLE` visible. |
| P05 REPORTING | 14 secciones, claims permitidos y local paths ausentes. |
| P06 DELIVERY | Manifest, sello y verificación de hashes completos. |
| P07 RECURRING AUDIT | Datos, motor y reglas atribuibles por separado o `NOT_COMPARABLE`. |
| P08 DEVELOPMENT E2E | UNKNOWN sintético/DEVELOPMENT reproducible; SOURCE intacto, sin operator-specific code. |
| P09 CLOSURE | Evidencia de P01–P08 y decisión humana de cierre. |

No se accede a HOLDOUT ni a feeds reales para esta misión. P08 inicial usa exclusivamente synthetic/DEVELOPMENT. No implica readiness comercial.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
