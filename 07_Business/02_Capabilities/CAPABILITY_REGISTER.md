# Capability register

Fecha de revisión: 2026-09-27. BUSINESS PHASE 2 — CAPABILITY BASELINE.

Inventario técnico basado exclusivamente en artefactos locales. No define servicios ni autoriza oferta comercial. Las afirmaciones permitidas son límites de lo defendible técnicamente, no material de marketing ni autorización de publicación. Transit Data Lab continúa como WORKING NAME.

La autorización expresa de Fase 2 sustituye para este trabajo la restricción de Fase 1 aún escrita en AGENTS.md/README.md. Se conservan esos archivos: el alcance de escritura se limita a los tres documentos de capacidades, BUSINESS_STATUS y los registros de gobierno cuando corresponde. Fase 1 completada según declaración del usuario.

## Criterio de clasificación

- **EXISTING**: evidencia de resultado técnico suficiente para el alcance exacto descrito; no implica disponibilidad de servicio ni capacidad universal.
- **IN_DEVELOPMENT**: implementación iniciada, sin resultado suficiente. Para mapping/audit el trabajo observado se limita a infraestructura DDL.
- **PLANNED**: intención/diseño sin implementación demostrable suficiente.
- **PENDING_VERIFICATION**: indicios/resultados aislados sin cadena probatoria suficiente para la capacidad enunciada.

Orden probatorio: baseline congelada y resultados completos ligados a hashes/estado > tests y gates > scripts > documentación > experimentos/diseño. Un hash no demuestra semántica; un exit 0 no demuestra todos los checks PASS. No se extrapola evidencia de GTFS Explorer al motor GTFS_Lab ni de requirements a cumplimiento jurídico.

## Resumen

| Estado | Capacidades |
| --- | ---: |
| EXISTING | 11 |
| IN_DEVELOPMENT | 2 |
| PLANNED | 4 |
| PENDING_VERIFICATION | 3 |
| TOTAL | 20 |

| ID | Nombre | Estado |
| --- | --- | --- |
| TDL-CAP-001 | Ingestión raw de Asturias | EXISTING |
| TDL-CAP-002 | Integridad y procedencia binaria GTFS | EXISTING |
| TDL-CAP-003 | Controles de integridad específicos de Asturias | EXISTING |
| TDL-CAP-004 | Consultas SQL exploratorias read-only | EXISTING |
| TDL-CAP-005 | Generación GIS/KML reproducible | PENDING_VERIFICATION |
| TDL-CAP-006 | Capa GTFS core tipada | PLANNED |
| TDL-CAP-007 | Motor propio de validación GTFS_Lab | PLANNED |
| TDL-CAP-008 | Capa analítica GTFS persistida | PLANNED |
| TDL-CAP-009 | Corpus normativo con trazabilidad binaria | EXISTING |
| TDL-CAP-010 | Requirements engine materializado de 2017/1926 | EXISTING |
| TDL-CAP-011 | Revisión humana con Gate 1 y Gate 2 | EXISTING |
| TDL-CAP-012 | Gates de regresión del baseline Compliance | EXISTING |
| TDL-CAP-013 | Replay integral independiente de Compliance | PENDING_VERIFICATION |
| TDL-CAP-014 | Mapping de requisitos a formatos | IN_DEVELOPMENT |
| TDL-CAP-015 | Motor de auditoría Compliance | IN_DEVELOPMENT |
| TDL-CAP-016 | Censo físico de cinco datasets piloto | EXISTING |
| TDL-CAP-017 | Validación GTFS Explorer vigente atribuible a build | PENDING_VERIFICATION |
| TDL-CAP-018 | Exportación de datos GTE conservada con manifiesto | EXISTING |
| TDL-CAP-019 | Comparación descriptiva NAP / GTE del piloto | EXISTING |
| TDL-CAP-020 | Modelo Audit/Quality de findings y evidencias | PLANNED |

## Baselines y límites de la revisión

Asturias: feed 20260924_020003, base SHA-256 `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`. Compliance Phase 2 FROZEN el 2026-09-27T01:18:24.849175+00:00, fuente consolidada 2024-03-04, base SHA-256 `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`. Phase 1 SHA `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5` es histórico, no la base física activa. Piloto: outputs históricos GTE 0.2.1 y aceptación declarada de candidato GTFS-023; no se inspecciona producto en 06_Products.

No se ha navegado ni interpretado legislación para afirmar vigencia, obligaciones o cumplimiento. GTFS-RT/NeTEx/SIRI no se acreditan como capacidades por referencias a recursos externos en snapshots. Inventario acotado a GTFS_Lab, Compliance y documentación técnica relacionada; no es auditoría de todas las áreas ni del producto actual.

## TDL-CAP-001 — Ingestión raw de Asturias

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-001 |
| Nombre | Ingestión raw de Asturias |
| Descripción técnica | Importación de los siete TXT del feed Asturias a tablas raw VARCHAR. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001), [TDL-EVD-002](EVIDENCE_INDEX.md#tdl-evd-002), [TDL-EVD-003](EVIDENCE_INDEX.md#tdl-evd-003), [TDL-EVD-004](EVIDENCE_INDEX.md#tdl-evd-004), [TDL-EVD-005](EVIDENCE_INDEX.md#tdl-evd-005), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | Base persistida y SQL concordantes; agency 41, calendar_dates 3.875, routes 609, shapes 774.732, stop_times 354.287, stops 6.368, trips 21.015. |
| Limitaciones | Feed único; runner no replayado; no extracción ZIP ni adquisición automática demostradas. |
| Dependencias | DuckDB 1.5.5, feed extraído y cwd resuelto por runner. |
| Nivel de automatización observado | SQL transaccional y runner implementados; adquisición/extracción no observadas como automatizadas. |
| Reproducibilidad observada | Datos y hashes contrastados; importación no repetida porque reemplaza tablas. |
| Afirmación comercial permitida | Se conserva una ingestión raw verificable del feed Asturias de 24-09-2026. |
| Afirmaciones NO permitidas | Ingestión universal, normalización tipada, importación desatendida de cualquier feed. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-002 — Integridad y procedencia binaria GTFS

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-002 |
| Nombre | Integridad y procedencia binaria GTFS |
| Descripción técnica | Vinculación de fuente ZIP, extracción y baseline DuckDB mediante SHA-256. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001), [TDL-EVD-002](EVIDENCE_INDEX.md#tdl-evd-002), [TDL-EVD-003](EVIDENCE_INDEX.md#tdl-evd-003), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | Hash de la base coincide; siete entradas ZIP coinciden byte a byte con extracción. |
| Limitaciones | SHA-256 prueba identidad, no calidad, semántica ni licencias. |
| Dependencias | ZIP fuente, siete TXT y baseline local. |
| Nivel de automatización observado | Comprobación local programática de hashes; sin monitor continuo observado. |
| Reproducibilidad observada | 7/7 pares recomprobados en esta fase; base coincide con baseline. |
| Afirmación comercial permitida | Se puede verificar la identidad binaria de la fuente y extracción de Asturias conservadas. |
| Afirmaciones NO permitidas | Autenticidad jurídica, licencia de reutilización o calidad garantizada por hashes. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-003 — Controles de integridad específicos de Asturias

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-003 |
| Nombre | Controles de integridad específicos de Asturias |
| Descripción técnica | Sentinel SQL read-only para baseline, referencias y propiedades estructurales seleccionadas. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-002](EVIDENCE_INDEX.md#tdl-evd-002), [TDL-EVD-006](EVIDENCE_INDEX.md#tdl-evd-006), [TDL-EVD-007](EVIDENCE_INDEX.md#tdl-evd-007), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | 46 resultados: 42 PASS; 4 FAIL por core/analysis/validation y validation.results ausentes; 201 filas >=24h conservadas. |
| Limitaciones | Resultado global WARNING, no PASS; controles y conteos específicos, cobertura parcial. |
| Dependencias | DuckDB, esquema raw y main.stops de esta baseline. |
| Nivel de automatización observado | SELECT automatizados invocados manualmente; no scheduling observado. |
| Reproducibilidad observada | Sentinel ejecutado aquí read-only, exit 0; exit 0 no equivale a ausencia de FAIL. |
| Afirmación comercial permitida | Se ejecutan controles reproducibles sobre propiedades estructurales seleccionadas del baseline Asturias. |
| Afirmaciones NO permitidas | Validador GTFS completo, cumplimiento de toda la especificación o ausencia de errores en todo feed. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-004 — Consultas SQL exploratorias read-only

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-004 |
| Nombre | Consultas SQL exploratorias read-only |
| Descripción técnica | Inspección de catálogo, conteos y subconjuntos del baseline mediante DuckDB. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-002](EVIDENCE_INDEX.md#tdl-evd-002), [TDL-EVD-006](EVIDENCE_INDEX.md#tdl-evd-006), [TDL-EVD-007](EVIDENCE_INDEX.md#tdl-evd-007), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | Tablas consultables; consultas persistidas de ruta 440: 1 ruta, 2 viajes, 2 shapes y 814 puntos. |
| Limitaciones | sql/02_exploration vacío; no biblioteca de consultas ni informes analíticos generales. |
| Dependencias | DuckDB y base local disponible. |
| Nivel de automatización observado | Consultas ad hoc y SELECT del sentinel; operación manual. |
| Reproducibilidad observada | Catálogo consultado aquí; consultas de subconjunto persistidas en sentinel. |
| Afirmación comercial permitida | El baseline raw conservado permite consultas SQL y comprobaciones puntuales. |
| Afirmaciones NO permitidas | Motor analítico consolidado, dashboards o análisis automático general. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-005 — Generación GIS/KML reproducible

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-005 |
| Nombre | Generación GIS/KML reproducible |
| Descripción técnica | Regeneración de geometrías de rutas como KML. |
| Estado | PENDING_VERIFICATION |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-009](EVIDENCE_INDEX.md#tdl-evd-009), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008), [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | Existen tres KML para ruta 440; informes describen 814 puntos y bounds de Asturias. |
| Limitaciones | No hay fuente ejecutable GIS; artefactos no prueban cómo se generaron. |
| Dependencias | Fuente raw, definición de joins/ordenación y herramienta de generación no identificada. |
| Nivel de automatización observado | Generación no observada; no atribuir automatización. |
| Reproducibilidad observada | Sin replay ni script; se inspeccionan archivos existentes. |
| Afirmación comercial permitida | Se conservan tres exportaciones KML experimentales de la ruta 440. |
| Afirmaciones NO permitidas | Pipeline GIS automatizado, cobertura de todas las rutas, precisión geográfica garantizada. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-006 — Capa GTFS core tipada

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-006 |
| Nombre | Capa GTFS core tipada |
| Descripción técnica | Transformación del raw a entidades tipadas persistidas. |
| Estado | PLANNED |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001), [TDL-EVD-006](EVIDENCE_INDEX.md#tdl-evd-006), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | La arquitectura prevé core; el catálogo vigente y sentinel confirman su ausencia. |
| Limitaciones | Sin esquema core ni SQL de construcción observado. |
| Dependencias | Diseño de tipos/contratos y fuentes raw. |
| Nivel de automatización observado | No observada. |
| Reproducibilidad observada | No hay implementación que reproducir. |
| Afirmación comercial permitida | La capa core figura como prevista; no está disponible. |
| Afirmaciones NO permitidas | Normalización o core ya implementados. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-007 — Motor propio de validación GTFS_Lab

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-007 |
| Nombre | Motor propio de validación GTFS_Lab |
| Descripción técnica | Validación general y persistencia de resultados GTFS dentro del laboratorio. |
| Estado | PLANNED |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001), [TDL-EVD-006](EVIDENCE_INDEX.md#tdl-evd-006), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | sql/03_validation vacío; validation.results y esquema validation ausentes. |
| Limitaciones | El sentinel y reportes externos de Explorer no sustituyen este motor. |
| Dependencias | Reglas, cobertura, ejecución y persistencia no implementadas. |
| Nivel de automatización observado | No observada. |
| Reproducibilidad observada | No hay motor reproducible. |
| Afirmación comercial permitida | El motor de validación propio del laboratorio está previsto. |
| Afirmaciones NO permitidas | Validación integral operativa del GTFS_Lab. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-008 — Capa analítica GTFS persistida

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-008 |
| Nombre | Capa analítica GTFS persistida |
| Descripción técnica | Análisis persistido por encima de raw. |
| Estado | PLANNED |
| Componente origen | GTFS_Lab |
| Evidencia exacta | [TDL-EVD-001](EVIDENCE_INDEX.md#tdl-evd-001), [TDL-EVD-006](EVIDENCE_INDEX.md#tdl-evd-006), [TDL-EVD-008](EVIDENCE_INDEX.md#tdl-evd-008); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Asturias 20260924_020003; baseline verificado 2026-09-27. |
| Qué demuestra exactamente | sql/04_analysis vacío y esquema analysis GTFS ausente. |
| Limitaciones | Consultas manuales no son pipeline; las vistas analysis de Compliance son otro componente. |
| Dependencias | Core/contratos y consultas analíticas futuras. |
| Nivel de automatización observado | No observada. |
| Reproducibilidad observada | Sin pipeline. |
| Afirmación comercial permitida | La capa de análisis GTFS persistida está prevista. |
| Afirmaciones NO permitidas | Análisis automatizado de oferta, cobertura o calidad ya disponible. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-009 — Corpus normativo con trazabilidad binaria

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-009 |
| Nombre | Corpus normativo con trazabilidad binaria |
| Descripción técnica | Registro de documentos, relaciones y provisions con fuentes locales y hashes. |
| Estado | EXISTING |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-010](EVIDENCE_INDEX.md#tdl-evd-010), [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-012](EVIDENCE_INDEX.md#tdl-evd-012), [TDL-EVD-015](EVIDENCE_INDEX.md#tdl-evd-015), [TDL-EVD-017](EVIDENCE_INDEX.md#tdl-evd-017); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | Diez fuentes jurídicas con hash válido, seis relaciones y 92 provisions 2017/1926 preservadas; invariantes 22/22. |
| Limitaciones | Fidelidad textual no acreditada; anomalías Annex 1.3 B-I/D-I; tres rutas absolutas. |
| Dependencias | Corpus local, DuckDB y manifiesto de fuentes. |
| Nivel de automatización observado | Persistencia y checks automatizados; selección/normalización no autónomas. |
| Reproducibilidad observada | 10/10 hashes recomprobados; resultados de invariantes completos contrastados. |
| Afirmación comercial permitida | Se conserva un corpus normativo trazable por fuentes y hashes, con controles de integridad estructural. |
| Afirmaciones NO permitidas | Corpus exhaustivo o actualizado automáticamente; fidelidad jurídica garantizada. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-010 — Requirements engine materializado de 2017/1926

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-010 |
| Nombre | Requirements engine materializado de 2017/1926 |
| Descripción técnica | Persistencia de requisitos revisados con facts, citas y deadlines. |
| Estado | EXISTING |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-010](EVIDENCE_INDEX.md#tdl-evd-010), [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-013](EVIDENCE_INDEX.md#tdl-evd-013), [TDL-EVD-014](EVIDENCE_INDEX.md#tdl-evd-014), [TDL-EVD-015](EVIDENCE_INDEX.md#tdl-evd-015), [TDL-EVD-018](EVIDENCE_INDEX.md#tdl-evd-018), [TDL-EVD-019](EVIDENCE_INDEX.md#tdl-evd-019), [TDL-EVD-028](EVIDENCE_INDEX.md#tdl-evd-028); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | 48 requisitos aprobados/materializados, 36 facts, 10 deadlines; 387/387 checks finales; fuente consolidada 2024-03-04. |
| Limitaciones | Siete dependencias PARTIAL; no interpreta automáticamente otras normas, no evalúa datasets ni cumplimiento. |
| Dependencias | Corpus Phase 1, decisiones humanas y estado aprobado de Phase 2. |
| Nivel de automatización observado | Materialización automatizada desde inputs revisados; interpretación y aprobación humanas. |
| Reproducibilidad observada | Counts actuales read-only coinciden; evidencia completa y hashes SQL contrastados; replay de escritura no ejecutado. |
| Afirmación comercial permitida | Hay un baseline congelado de 48 requisitos revisados y trazables para la fuente 2017/1926 indicada. |
| Afirmaciones NO permitidas | Extractor jurídico autónomo, todos los requisitos UE/España cubiertos, conformidad de operadores. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-011 — Revisión humana con Gate 1 y Gate 2

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-011 |
| Nombre | Revisión humana con Gate 1 y Gate 2 |
| Descripción técnica | Trazabilidad documental de revisión, atomicidad y resolución previa a materialización. |
| Estado | EXISTING |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-018](EVIDENCE_INDEX.md#tdl-evd-018), [TDL-EVD-019](EVIDENCE_INDEX.md#tdl-evd-019), [TDL-EVD-016](EVIDENCE_INDEX.md#tdl-evd-016); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | Gate 1/2 CLOSED, matrices y universo aprobado conservados. |
| Limitaciones | Sin generador independiente de dossiers; evaluación humana no equivale a acreditación jurídica externa. |
| Dependencias | Revisor humano, facts y decisiones registradas. |
| Nivel de automatización observado | Manual con soporte documental y checks. |
| Reproducibilidad observada | Decisiones preservadas; regeneración requiere replay humano. |
| Afirmación comercial permitida | El baseline registra revisión humana y decisiones trazables antes de materializar requisitos. |
| Afirmaciones NO permitidas | Aprobación automática o independiente de toda interpretación jurídica. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-012 — Gates de regresión del baseline Compliance

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-012 |
| Nombre | Gates de regresión del baseline Compliance |
| Descripción técnica | Comprobación técnica de invariantes, anexos y universo materializado. |
| Estado | EXISTING |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-010](EVIDENCE_INDEX.md#tdl-evd-010), [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-015](EVIDENCE_INDEX.md#tdl-evd-015), [TDL-EVD-017](EVIDENCE_INDEX.md#tdl-evd-017); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | 22 invariantes +22 estructura +63 anexos +387 post-materialización, todos PASS guardados; diez exit codes 0 y hashes SQL coincidentes. |
| Limitaciones | Gates técnicos, no auditoría normativa; assertions históricos no aplicables al estado posterior. |
| Dependencias | SQL exacto, DuckDB, snapshots y estado de fase adecuado. |
| Nivel de automatización observado | Tests SQL automatizados; lanzamiento/control de fase manual. |
| Reproducibilidad observada | Se validaron las salidas completas guardadas; no rerun de diez suites en esta fase. |
| Afirmación comercial permitida | El baseline Compliance conserva gates técnicos reproducibles de integridad y trazabilidad. |
| Afirmaciones NO permitidas | Gates prueban cumplimiento jurídico, fidelidad textual o exhaustividad normativa. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-013 — Replay integral independiente de Compliance

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-013 |
| Nombre | Replay integral independiente de Compliance |
| Descripción técnica | Reconstrucción end-to-end de Phase 2 desde inputs de Phase 1. |
| Estado | PENDING_VERIFICATION |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-014](EVIDENCE_INDEX.md#tdl-evd-014), [TDL-EVD-016](EVIDENCE_INDEX.md#tdl-evd-016), [TDL-EVD-017](EVIDENCE_INDEX.md#tdl-evd-017), [TDL-EVD-018](EVIDENCE_INDEX.md#tdl-evd-018), [TDL-EVD-019](EVIDENCE_INDEX.md#tdl-evd-019); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | Hay scripts y matriz de replay controlado; decisiones manuales explícitas. |
| Limitaciones | No replay integral observado; execution_performed=NO en matriz; estado histórico requerido. |
| Dependencias | Copia aislada del estado histórico, corpus local, decisiones humanas y pre-write SHA. |
| Nivel de automatización observado | Mixta: seed/persistencia programados, decisiones manuales. |
| Reproducibilidad observada | No observado end-to-end ni en otra máquina; no ejecutar sobre base congelada activa. |
| Afirmación comercial permitida | Hay componentes de replay documentados sujetos a inputs históricos y decisiones humanas. |
| Afirmaciones NO permitidas | Reconstrucción automática integral, portable o ya comprobada de extremo a extremo. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-014 — Mapping de requisitos a formatos

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-014 |
| Nombre | Mapping de requisitos a formatos |
| Descripción técnica | Cobertura/equivalencia de requisitos respecto a formatos de transporte. |
| Estado | IN_DEVELOPMENT |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-010](EVIDENCE_INDEX.md#tdl-evd-010), [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-020](EVIDENCE_INDEX.md#tdl-evd-020), [TDL-EVD-028](EVIDENCE_INDEX.md#tdl-evd-028); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | Trabajo iniciado únicamente en DDL/tablas; format_coverage=0 y format_equivalences=0 observados. |
| Limitaciones | No mapping poblado ni motor demostrado; no inferir equivalencia GTFS/NeTEx. |
| Dependencias | Requisitos aprobados, reglas y trazabilidad por formato pendientes. |
| Nivel de automatización observado | Infraestructura persistida; mapping automatizado no observado. |
| Reproducibilidad observada | Solo catálogo y cero filas verificados. |
| Afirmación comercial permitida | Existe estructura de datos inicial para futuros mappings; no hay cobertura evaluada. |
| Afirmaciones NO permitidas | GTFS satisface requisitos legales, conversiones 1:1 o equivalencias demostradas. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-015 — Motor de auditoría Compliance

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-015 |
| Nombre | Motor de auditoría Compliance |
| Descripción técnica | Evaluación de reglas contra evidencias y persistencia de runs/resultados. |
| Estado | IN_DEVELOPMENT |
| Componente origen | Compliance |
| Evidencia exacta | [TDL-EVD-010](EVIDENCE_INDEX.md#tdl-evd-010), [TDL-EVD-011](EVIDENCE_INDEX.md#tdl-evd-011), [TDL-EVD-020](EVIDENCE_INDEX.md#tdl-evd-020), [TDL-EVD-028](EVIDENCE_INDEX.md#tdl-evd-028); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Compliance Phase 2 congelada 2026-09-27, fuente 2024-03-04; historial Phase 1 preservado. |
| Qué demuestra exactamente | Trabajo iniciado en tablas audit.rules/runs/results/evidence; rules/runs/results=0. |
| Limitaciones | Infraestructura no es motor operativo; no reglas ni resultados de cumplimiento. |
| Dependencias | Mappings, reglas, datasets, evidencia y contratos aún no demostrados. |
| Nivel de automatización observado | No ejecución de auditoría observada. |
| Reproducibilidad observada | Sin run reproducible. |
| Afirmación comercial permitida | Existe infraestructura inicial de auditoría; todavía no se acredita un motor operativo. |
| Afirmaciones NO permitidas | Auditoría normativa automatizada, certificación, homologación o garantía de cumplimiento. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-016 — Censo físico de cinco datasets piloto

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-016 |
| Nombre | Censo físico de cinco datasets piloto |
| Descripción técnica | Inventario físico de archivos, filas, columnas y hashes del piloto. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab / 20_clientes_reales |
| Evidencia exacta | [TDL-EVD-021](EVIDENCE_INDEX.md#tdl-evd-021), [TDL-EVD-022](EVIDENCE_INDEX.md#tdl-evd-022), [TDL-EVD-023](EVIDENCE_INDEX.md#tdl-evd-023); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Piloto histórico 0.2.1; revisión/procedencia posterior según EVD-027 cuando aplica; fecha de inspección 2026-09-27. |
| Qué demuestra exactamente | Resultados conservados para Ancebus, Viagón, Gilsanz, Kbus y Bizkaibus; scripts de censo. |
| Limitaciones | Histórico; no semántica ni representatividad del mercado; 20 entradas no son 20 auditorías ni clientes. |
| Dependencias | ZIPs/extracciones originales y scripts de inventario. |
| Nivel de automatización observado | Censo generado con Python; adquisición/preparación no acreditadas como desatendidas. |
| Reproducibilidad observada | Código y outputs existentes; generadores no ejecutados porque escriben fuera de scope. |
| Afirmación comercial permitida | Se dispone de un censo físico documentado de cinco datasets piloto. |
| Afirmaciones NO permitidas | Veinte clientes auditados, calidad legal demostrada o cobertura representativa del mercado. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-017 — Validación GTFS Explorer vigente atribuible a build

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-017 |
| Nombre | Validación GTFS Explorer vigente atribuible a build |
| Descripción técnica | Ejecutar validación con procedencia canónica y cobertura identificada. |
| Estado | PENDING_VERIFICATION |
| Componente origen | GTFS Explorer / outputs recibidos en GTFS_Lab |
| Evidencia exacta | [TDL-EVD-024](EVIDENCE_INDEX.md#tdl-evd-024), [TDL-EVD-025](EVIDENCE_INDEX.md#tdl-evd-025), [TDL-EVD-027](EVIDENCE_INDEX.md#tdl-evd-027); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Piloto histórico 0.2.1; revisión/procedencia posterior según EVD-027 cuando aplica; fecha de inspección 2026-09-27. |
| Qué demuestra exactamente | Hay informes históricos 0.2.1 y registro de run_004 GTFS023_ACCEPTED; no se toma rc002 por su nombre. |
| Limitaciones | No se inspeccionaron runtime/forense en Products; README de aceptación no basta para verificar aquí build vigente. Enum findings históricos invalidados. |
| Dependencias | Producto externo, executable SHA, schema, feed y procedencia de proceso. |
| Nivel de automatización observado | Informes indican ejecución del producto; interacción y automatización actuales no observadas. |
| Reproducibilidad observada | Hash HTML Kbus confirmado; validación actual/build y replay no comprobados. |
| Afirmación comercial permitida | El laboratorio conserva informes de validación de ejecuciones concretas de GTFS Explorer y un registro de aceptación Bizkaibus. |
| Afirmaciones NO permitidas | Motor propio del Lab, validador universal vigente verificado; 1.040.852 errores reales de Bizkaibus o defecto vigente de truncado. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-018 — Exportación de datos GTE conservada con manifiesto

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-018 |
| Nombre | Exportación de datos GTE conservada con manifiesto |
| Descripción técnica | Salida JSON de datos seleccionados con integridad verificable. |
| Estado | EXISTING |
| Componente origen | GTFS Explorer / outputs recibidos en GTFS_Lab |
| Evidencia exacta | [TDL-EVD-026](EVIDENCE_INDEX.md#tdl-evd-026), [TDL-EVD-025](EVIDENCE_INDEX.md#tdl-evd-025), [TDL-EVD-024](EVIDENCE_INDEX.md#tdl-evd-024); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Piloto histórico 0.2.1; revisión/procedencia posterior según EVD-027 cuando aplica; fecha de inspección 2026-09-27. |
| Qué demuestra exactamente | JSON Kbus rutas AH-H-L2-L3 y servicios 1-2 conservado; SHA-256 coincide con manifiesto. |
| Limitaciones | Capacidad demostrada histórica y acotada a artefacto recibido; no pipeline vigente ni export de findings. La selección registra AH/H/L2/L3, pero el array routes contiene AH/H/L2: no se acredita completitud de la selección ni presencia de L3. |
| Dependencias | Datos/proyecto de la ejecución externa y selección manual. |
| Nivel de automatización observado | Serialización por producto; flujo de exportación no observado aquí. |
| Reproducibilidad observada | Identidad del JSON recomprobada; no replay ni round-trip. |
| Afirmación comercial permitida | Se conserva una exportación JSON verificable de datos seleccionados de Kbus producida en una ejecución de GTFS Explorer. |
| Afirmaciones NO permitidas | Export universal vigente, round-trip íntegro o export completo de evidencia de auditoría. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-019 — Comparación descriptiva NAP / GTE del piloto

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-019 |
| Nombre | Comparación descriptiva NAP / GTE del piloto |
| Descripción técnica | Contraste de agregados NAP y hallazgos GTE con categorías de comparabilidad. |
| Estado | EXISTING |
| Componente origen | GTFS_Lab / piloto |
| Evidencia exacta | [TDL-EVD-022](EVIDENCE_INDEX.md#tdl-evd-022), [TDL-EVD-023](EVIDENCE_INDEX.md#tdl-evd-023), [TDL-EVD-024](EVIDENCE_INDEX.md#tdl-evd-024), [TDL-EVD-027](EVIDENCE_INDEX.md#tdl-evd-027); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Piloto histórico 0.2.1; revisión/procedencia posterior según EVD-027 cuando aplica; fecha de inspección 2026-09-27. |
| Qué demuestra exactamente | Matriz e informes de cinco operadores; UNKNOWN/NOT_COMPARABLE preservados, sin exclusividades concluyentes. |
| Limitaciones | NAP sin rule IDs suficientes; conclusiones históricas Bizkaibus corregidas por registro posterior; no equivalencia de detectores. |
| Dependencias | Snapshots NAP, reports GTE y reglas de comparación. |
| Nivel de automatización observado | Parsing y agregación Python con interpretación documental. |
| Reproducibilidad observada | Código y resultados conservados; no rerun ni equivalencia regla a regla. |
| Afirmación comercial permitida | Existe comparación descriptiva documentada de los outputs NAP y GTE disponibles para cinco datasets. |
| Afirmaciones NO permitidas | Superioridad de un validador, detección exclusiva, incumplimiento normativo o enum findings históricos válidos. |
| Fecha de revisión | 2026-09-27 |

## TDL-CAP-020 — Modelo Audit/Quality de findings y evidencias

| Campo | Valor |
| --- | --- |
| ID | TDL-CAP-020 |
| Nombre | Modelo Audit/Quality de findings y evidencias |
| Descripción técnica | Separación conceptual entre ocurrencias, findings, muestras y cobertura. |
| Estado | PLANNED |
| Componente origen | GTFS_Lab / piloto |
| Evidencia exacta | [TDL-EVD-024](EVIDENCE_INDEX.md#tdl-evd-024); rutas exactas y hashes en EVIDENCE_INDEX. |
| Versión / baseline / fecha | Piloto histórico 0.2.1; revisión/procedencia posterior según EVD-027 cuando aplica; fecha de inspección 2026-09-27. |
| Qué demuestra exactamente | Documento conceptual propone poblaciones y completitud; no implementación de modelo auditado. |
| Limitaciones | No acredita agregados completos por regla ni resultados normativos. |
| Dependencias | Arquitectura de detalle, denominadores y trazabilidad futura. |
| Nivel de automatización observado | No implementación observada. |
| Reproducibilidad observada | Diseño documental, sin replay ejecutable. |
| Afirmación comercial permitida | Se ha documentado un diseño conceptual de findings y completitud de evidencias. |
| Afirmaciones NO permitidas | Modelo operativo o escalabilidad/completitud por regla ya demostradas. |
| Fecha de revisión | 2026-09-27 |

## Capacidades aparentes degradadas tras inspección

- GIS reproducible → TDL-CAP-005 PENDING_VERIFICATION: KML sin generador.
- Validador GTFS_Lab completo → TDL-CAP-007 PLANNED: sentinel parcial, sin motor/validation.results.
- Análisis GTFS consolidado → TDL-CAP-008 PLANNED: queries manuales y capa ausente.
- Replay Compliance completamente automático → TDL-CAP-013 PENDING_VERIFICATION: decisiones humanas y sin replay integral ejecutado.
- Mappings/auditoría operativos → TDL-CAP-014/015 IN_DEVELOPMENT: existen tablas, pero cero cobertura/reglas/runs/results.
- Validación vigente atribuible al producto → TDL-CAP-017 PENDING_VERIFICATION: informes y registro de aceptación no sustituyen la cadena forense fuera del alcance. No se invalida la aceptación registrada de run_004; aquí no se revalida independientemente.

Ninguna de estas degradaciones modifica la conclusión técnica original ni convierte una limitación Business en trabajo asignado a otro componente. Los 1.040.852 hallazgos enum históricos Bizkaibus están invalidados; no se usan como calidad real del feed.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.


## Revisión final de congelación V1

2026-09-27: las 11 capacidades EXISTING superan A–H exclusivamente para sus descripciones y afirmaciones acotadas. Sin degradaciones adicionales. La matriz individual y la revisión de las 20 capacidades están en [BASELINE_REVIEW_V1.md](BASELINE_REVIEW_V1.md); controles técnicos persistidos en [review_v1/final_summary.json](review_v1/final_summary.json). No se equipara evidencia histórica a operación actual universal.

El inventario se integra en BUSINESS_CAPABILITY_BASELINE_V1. Cualquier cambio posterior requiere nueva revisión Business documentada y nueva huella, o V2; no se modificará silenciosamente esta versión congelada.
