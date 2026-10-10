# Transit Data Lab — mapa de estado vigente

**Integración pública — 2026-10-10:** fuentes y documentación sanitizada versionadas en el [PR #59](https://github.com/ylemusit/Transit_Data_Lab/pull/59); CI ampliada con fixtures sintéticos portables. Resultados de operadores y entregas completos conservados fuera de Git. El resultado vigente corresponde al SHA final del PR/main; GTFS Explorer conserva sus repositorios independientes.

**Actualizado:** 2026-10-10

**Limpieza verificada — 2026-10-10:** retirados los diez snapshots sustituidos y las cachés inventariadas: 1.623 archivos (74.152.440 bytes). Hashes contrastados antes de cada borrado; 21 JSON históricos archivados y tres marcadores de mypy conservados. 40 pruebas PASS con candidatos inaccesibles; estado Git y trabajo local preservados.

**E2E de fábrica a auditoría — CS Autobuses, cierre 2026-10-10:** runner 1.7.0, ZIP sintético de 32 archivos, R14 `E2E_PASS` y 20/20 controles. G03 FIELD-TYPE 1.1.0 corregido y reproducción 1.0.0 conservada; auditoría `COMPLETED_WITH_LIMITATIONS`, cero hallazgos en el alcance ejecutado. PDF/XLSX/KMZ completos con renderer portátil; inventario exacto y escaneo de contenido PASS. 121 tests, dos libros abiertos en Excel 16.0 y 40 páginas de QA visual. Demo disponible con límites; emisión real requiere fuente autorizada y revisión humana, GIS sigue pendiente. NAP se evalúa aparte de la auditoría previa a publicación; baseline/readiness comercial sin promoción. [Cierre](02_Data_Engineering/GTFS_Lab/docs/CS_AUTOBUSES_REMEDIATION_20261010.md) · [Riesgos](02_Data_Engineering/GTFS_Lab/docs/CS_AUTOBUSES_E2E_RISK_REGISTER_V1.md).

**Contexto jurídico 2026-10-08:** CLOSED_WITH_EVIDENCE_LIMITS. Capturas completas: 17 fuentes + 6 consolidaciones + 10 congeladas; 33/33 hashes y 38/38 tests PASS. PDF privado corregido de 67 páginas, QA y revisión visual completos, paquete de 95 archivos sellado/verificado. Sin tareas técnicas pendientes; aplicabilidad externa y emisión humana no determinadas. Baselines/readiness/C06 preservados. [Detalle](03_Compliance/LEGAL_CONTEXT_UPDATE_20261008.md).

**Doble entrega y calidad 2026-10-08:** estándar V1 documentado; referencia ejecutiva inicial preservada y nueva entrega conjunta portable comprobada en 07/08. Comprensión con clientes, replay independiente y ampliación GTFS/NeTEx aún no demostrados. Readiness y fases Business sin cambios. [Estándar](reports/TDL_AUDIT_QUALITY_STANDARD_V1.md).

**Backlog GTFS/NeTEx 2026-10-09:** 21/24 tareas completadas en sus alcances; 12/13 implementan reglas opt-in estáticas con tests, sin modificar motores V1. 19/20/23 parciales; sigue pendiente validación externa real y perfil/destino NeTEx. No hay generador, conversor ni publicador de feeds reales integrados como capacidad de producto; el puente sintético Frabica_GTFS→TDL no eleva readiness. Dependencias detalladas en la [brecha de capacidad](reports/TDL_STATIC_GTFS_NETEX_CAPABILITY_GAP_20261009.md). No se cambia la fase Business ni el readiness. [Registro](07_Business/03_Market/TDL_GTFS_NETEX_CLAIMS_REGISTER_20261009.md) · [Lista y evidencia técnica](reports/TDL_AUDIT_IMPROVEMENT_BACKLOG_V1.md) · [Cierre 12/13](reports/audit_battery_v1/TDL_AUD_12_13_IMPLEMENTATION_20261009.md).

**Preparación de producción GTFS↔NeTEx — 2026-10-09:** revisión del inventario 0.2.1: 5 runs/43 artefactos, 14 entradas `gtfs-export-*` acotadas por ruta/servicio y un ZIP; payloads no disponibles en el run inspeccionado. `FULL_FEED_PRODUCER = NOT_VERIFIED`, incluida la baseline 0.2.2. Registro de mappings creado como borrador interno; perfil/destino y decisiones del operador pendientes. No se añade generador, conversor o publicación sin esas entradas. [Evidencia](reports/TDL_STATIC_GTFS_NETEX_CAPABILITY_GAP_20261009.md) · [Registro](reports/GTFS_NETEX_MAPPING_REGISTER_V1.md).

**Segundo bloque 2026-10-08:** TDL-AUD-04/05/06 COMPLETADAS en alcance interno: contrato común, seis casos GTFS con poblaciones verificadas, ejemplo NeTEx histórico, dos no evaluables explicados y método de conclusión/prioridad. 20 pruebas focalizadas PASS; prioridad UNASSESSED cuando falta contexto. Sin nueva ejecución del motor. Integrado en nuevas vistas 07/08. [Valoración](reports/audit_assessment_v1/README.md).

**Cuarto bloque 2026-10-09:** TDL-AUD-09/14 COMPLETADAS en alcance interno: 45 fuentes (44 archivos y EPIP ausente), gestión de autoridad/derechos/versiones/cambios, captura GTFS idéntica a referencia fijada. 114 escenarios y 36 controles representados; 114/114 hechos y 458 dependencias XSD PASS; 75/75 pruebas. Referencia sellada, sin motores/HOLDOUT/promoción. Expectativas del agente autor, no revisión humana independiente; no mide precisión ni cobertura exhaustiva. Continuado con 10/11 y 15 en bloque quinto. [Corpus](reports/audit_corpus_v1/README.md) · [Banco](reports/audit_reference_bank_v1/README.md).

**Quinto bloque 2026-10-09:** 10/11 diseño completado (19 propuestas, 36 controles/108 fixtures, 132 campos/32 archivos, sin implementar nuevas reglas); 15 medición delimitada completada (114 escenarios internos + 96 GTFS externos MobilityData 8.0.1/hash verificado). Once abstenciones, tres detecciones cruzadas y diferencias de normalización/contexto/autoridad conservadas; un caso externo con dos errores secundarios. 88/88 pruebas; 114 RAW, 96 informes y 20 entradas protegidas verificados. Sin HOLDOUT, perfil PASS, precisión universal o elevación de readiness. Siguiente: 12/13 y 16/17. [Baterías](reports/audit_battery_v1/README.md) · [Medición](reports/audit_precision_v1/README.md).

**Sexto bloque 2026-10-09:** 16/17 completadas internamente. Replay FINAL_V3 aislado y offline, 108 escenarios ejecutados + seis candidatos preservados = 114/114 equivalentes; 621 entradas/620 originales y 29 módulos verificados; cero intentos de red/lectura original. Misma máquina/base Python, sin clean-machine ni pipeline completo. Seguimiento lateral: seis casos, ocho eventos, dos resueltos/dos persistentes/dos nuevos; REPORTED_CORRECTED separado de resolución, responsables/fechas propuestos y aceptados distintos. Comunicaciones/aceptaciones simuladas, sin productor real o idoneidad del destino. 103/103 pruebas y CLI PASS; fuentes/motores/contratos/RAW/HOLDOUT intactos. [Replay](reports/audit_replay_v1/README.md) · [Seguimiento](reports/audit_lifecycle_v1/README.md).

**Séptimo bloque 2026-10-09:** TDL-AUD-18 cerrada en aplicación documental; lista previa a emisión aplicada a dos paquetes, sin revisión independiente o autorización humana. TDL-AUD-19 parcial: especificación multi-soporte y prototipo listos; navegador bloqueó `file://`, interacción real pendiente. TDL-AUD-20 parcial: protocolo de usuarios preparado, sin sesiones ni participantes; umbral 4/5 por perfil aún no medido. [Revisión, UX y protocolo](reports/audit_quality_gate_v1/README.md).

**Octavo bloque 2026-10-09:** 21 completada como recorrido interno: ocho etapas, responsables propuestos, entradas/salidas/excepciones/mensajes; dos recorridos GTFS/NeTEx con V1/V2 y decisiones de 17 preservadas. API/CLI aditiva, ocho pruebas PASS; un resuelto/un persistente/un nuevo por formato. Acuerdos/respuestas/aceptaciones simulados; sin nueva auditoría, integración de intake/pantallas o cliente real. [Servicio operativo interno](reports/audit_service_v1/README.md).

**TDL-AUD-23/24 2026-10-09:** validación de valor diseñada, sin evidencia primaria; cuadro documental reproducible y pauta periódica preparados. 23 PARCIAL; 24 COMPLETADA en preparación, sin revisiones humanas recurrentes ni medición comercial. [Gestión de calidad](reports/audit_quality_management_v1/README.md).

**TDL-AUD-22 2026-10-09:** diez afirmaciones auditables, con audiencias, madurez, frase permitida, evidencia/fecha, límites y veto de uso externo; evidencia y capacidades conservadoras, sin tocar la baseline Business V1 congelada. [Registro Market interno](07_Business/03_Market/TDL_GTFS_NETEX_CLAIMS_REGISTER_20261009.md).

**Fuente de detalle:** [PROJECT_STATUS.md](PROJECT_STATUS.md).

**Revisión canónica 2026-10-07:** entorno P: `PASS_WITH_LIMITATIONS`; 34 junctions presentes; 0 rutas C: activas encontradas; suites actuales y prueba sintética con limitaciones. HOLDOUT no accedido. Piloto real externo: NO hasta probar backup/restore separado y autorizar operación externa. [Revisión](reports/PROJECT_INTEGRITY_AND_HEALTH_REVIEW_V1.md) · [Matriz](reports/PROJECT_VALIDATION_MATRIX_V1.md) · [Gaps](reports/PROJECT_GAP_ANALYSIS_V1.md).

```text
TRANSIT DATA LAB
│
├── DEDICATED PARTITION MIGRATION V1    ✅ CLOSED_WITH_TEMPORARY_COMPATIBILITY_LINKS; P: canonical; REVIEW=0; C: CLEAN; 34 P-only junctions
│   └── Validación                       50 focal tests + bank E2E + Compliance + Git PASS; MapLibre advisory pendiente separado
├── LOCAL ENVIRONMENT RECONCILIATION V2  ✅ CLOSED_WITH_PROTECTED_RESIDUALS (13.278.198.318 bytes V2; 58 worktrees + 7 copias retirados; datos/evidencia privados protegidos)
├── LOCAL WORKSPACE RECONCILIATION R1  ✅ CLOSED_WITH_PROTECTED_LEGACY_RESIDUALS (~6.40 GB recuperados; política de datos externos establecida)
├── TRUST FOUNDATION                    ✅ CLOSED (gate técnico)
├── GTFS AUDIT ENGINE V1                ✅ CLOSED (alcance técnico documentado)
├── COMPLIANCE V1                       ✅ CLOSED_WITH_DEFERRALS
├── REMEDIATION ENGINE V1               ✅ CLOSED (alcance técnico documentado)
├── PRODUCT READINESS V1                ✅ READY_FOR_CONTROLLED_PILOT_WITH_LIMITATIONS
│   ├── Distribution model               INTERNAL_USE_ONLY; customer/public distribution deferred
│   ├── Client report V1                 ✅ Complete rule matrix + bounded Compliance bridge
│   ├── E2E / Trust / GTFS / Compliance  ✅ Synthetic E2E + current gates PASS
│   ├── Clean-machine validation         ⚠ PARTIAL / BLOCKED_BY_ENVIRONMENT; not rerun
│   └── Market / demand / WTP            ⚪ NOT_VALIDATED
│
├── NÚCLEO DEL PRODUCTO — AÑO 1         🎯 ESPAÑA + GTFS + NeTEx
│   ├── GTFS PRODUCTIZATION              ✅ V1 CLOSED (P01–P09)
│   │   ├── P01–P06, P08                ✅ CLOSED
│   │   ├── P07 recurring                ✅ CLOSED_WITH_DOCUMENTED_LIMITATION
│   │   ├── CI remoto + E2E sintético   ✅ PASS (PR34 + POST-MERGE)
│   │   └── P09 cierre final             ✅ APPROVED; CIERRE TÉCNICO
│   └── NeTEx                             ✅ V1 PASS / CLOSED (alcance documentado)
│
├── REAL DATASET TEST BANK V1             ✅ CLOSED; HUMAN CLOSURE APPROVED
│   ├── Controlled Intake + Case ID      ✅ GTFS; SHA-256 + códigos no reutilizables
│   ├── Short workspace + metadata       ✅ OK / NOT_OK; registros y replay
│   ├── Validación real                  ✅ EMT PALMA LOCAL CASE COMPLETED; LOCAL / CONTROLLED
│   └── Aceptación remota                ✅ PR40 MERGED; CI PR + POST-MERGE PASS
├── REAL DATA HARDENING CAMPAIGN V1       ✅ PASS / CLOSED
│   ├── 7 datasets; 9 intentos / 8 OK     ✅ NOT_OK histórico preservado
│   ├── Replay requerido / fallos        ✅ PASS / 0 abiertos
│   └── PR #43 + CI PR/post-merge        ✅ MERGED / PASS
├── AUDIT INTERPRETATION & CONSOLIDATION V1
│   ├── I01 Contract                     ✅ CLOSED; frozen schema + synthetic contract tests
│   ├── I02–I03                          ✅ CLOSED; deterministic consolidation + evidence-bounded impact
│   ├── I04–I06                          ✅ CLOSED; generic G07 + synthetic battery + JSON/Markdown
│   ├── I07                              ✅ CLOSED; Client Workflow + Test Bank + semantic replay
│   └── I08                              ✅ 279 PASS; 1 documented SKIP; human closure APPROVED
├── AUDIT INTERPRETATION V1              ✅ VALIDATED_WITH_DOCUMENTED_LIMITATIONS
│   ├── DEVELOPMENT                       ✅ 14/14 OK; 14/14 replay; 92 findings / 7 families
│   ├── Interpretation                    ✅ 11 interpreted; 3 partial; 0 unknown / unsupported
│   ├── Dataset 019                       ⚠ 12m43s; ~18.89 GiB; optimization required
│   └── HOLDOUT                           ✅ GENERALIZATION_PASS_WITH_LIMITATIONS; PUBLICATION COMPLETE (PR #47; post-merge CI PASS)
├── AUDIT CASES AND DECISIONS V1          ⚠ IMPLEMENTED LOCALLY; R1 AND R2 CONFORME CON LIMITACIONES
│   ├── Additive contract                  ✅ V1 schema unchanged; source records / reconciled events separated
│   ├── Focused verification               ✅ 32/32 focused tests; RUN02 E2E completed
│   └── Reference package                 ⚠ PRIVATE LOCAL OUTPUT; HUMAN EMISSION REVIEW PENDING
├── WINDOWS SELF-SERVICE CLIENT V1       ✅ W02–W08 PASS_WITH_LIMITATIONS; W08_HUMAN_ACCEPTANCE PASS; PR #51 MERGED (37bd5c5; post-merge CI SUCCESS); sin release
│   ├── W00-R / W00-O / W00-M / W00-P       DIAGNOSTICS COMPLETE / ROOT CAUSE UNKNOWN / SYNTHETIC CAUSE PROBABLE / PASS_WITH_RESOURCE_LIMITATION
│   ├── Streaming JSON S1/S4/S64            BYTE + SEMANTIC EQUIVALENCE PASS
│   ├── Pico privado muestreado             −32,85 % / −72,95 % / −81,41 %
│   ├── Causa raíz sintética                CONFIRMED; no atribución a dataset 019
│   ├── W00-P regresión                     291 total / 290 PASS / 0 FAIL / 1 SKIP documentado; consolidación PASS
│   ├── Outputs sintéticos completos        NOT VERSIONED; retained locally; no cleanup
│   ├── PyInstaller + DuckDB               ONEDIR PASS; DuckDB 1.5.5; clean machine PENDING
│   ├── Hardware mínimo/recomendado        NOT_YET_ESTABLISHED
│   ├── Dataset 019 / soporte feeds extremos DEFERRED / NOT CERTIFIED
│   ├── QGIS                                EXTERNAL AND OPTIONAL; NOT BUNDLED OR REQUIRED
│   ├── PR #49 + post-merge CI              ✅ MERGED / SUCCESS (6271a75; run 37256036471)
│   ├── W01 Application Shell                ✅ HUMAN ACCEPTANCE PASS; 7/7 tests
│   ├── PyInstaller onedir + DuckDB           ✅ PASS; DuckDB bundled
│   ├── W02 Intake                            ✅ PASS; 4 synthetic tests + client regression
│   ├── W03 Audit execution                   ✅ isolated worker, truthful stages, failure/cancel/rerun tests
│   ├── W04 Results                           ✅ read-only result/family viewer; manual visual acceptance PASS
│   ├── W05 GIS export                         ✅ GeoJSON/KML bridge + guide; manually validated; QGIS remains external/optional
│   ├── W06 Reporting/export                   ✅ PDF/Markdown export; PDF visual acceptance PASS
│   ├── W07 Reliability                        ✅ synthetic failure/cancel/collision/restart matrix
│   └── W08 Packaging/release                 ✅ RC 1.0.0-rc.1; manual acceptance, GIS/QGIS, KML/Google Earth PASS; APPLICATION_DEFECT_001 CLOSED_FIXED_AND_VERIFIED; clean-machine parcial; firma/SmartScreen/hardware pendientes
├── COMMERCIAL VALIDATION                ⚪ NOT_ESTABLISHED
├── GIS / QGIS                           ✅ W05 export bridge validated; QGIS external, optional, not bundled or required
│
└── BACKLOG POST-COMERCIALIZACIÓN        💤 FUERA DE LA SIGUIENTE FASE
    ├── SIRI
    ├── GTFS-RT
    ├── Colombia
    └── otros mercados y modos
```

**R1 local:** `LOCAL_WORKSPACE_RECONCILIATION_R1 = CLOSED_WITH_PROTECTED_LEGACY_RESIDUALS`; espacio recuperado ≈ 6.40 GB; `CONTROLLED_EXTERNAL_DATA_POLICY = ESTABLISHED`. No se incluyen rutas locales ni inventarios en el estado público. Detalle sanitizado: [resumen R1](reports/LOCAL_WORKSPACE_RECONCILIATION_R1_SUMMARY.md).

**Antecedente de W00/W01 previo a la campaña W02–W08:** El freeze funcional permanece en `9cafe0703abf47e80f67f80a6b423c938e1979aa`; la validación HOLDOUT no cambió ficheros funcionales versionados. La publicación de evidencia está publicada (PR #47, merge `69567c4a82d65e3017ee74ce64695a6a8334aa46`; CI post-merge `37230388650` PASS). Se preserva la historia del protocolo: `PRISTINE_BLIND_HOLDOUT = NO`; `CONTENT_BLIND_HOLDOUT = YES`. Generalización aprobada con limitaciones: 6/6 replays PASS, 530 findings, 3 familias, y una interpretación parcial (caso 00026; G04 en consolidación genérica). Los seis paquetes de evidencia y sus hashes están registrados en el manifiesto de HOLDOUT. No hay código específico de operador; validación comercial/mercado no establecida; no se reclama cumplimiento legal ni cobertura GTFS completa. `W00 = CLOSED_WITH_RESOURCE_LIMITATION`; PR #49 y el CI post-merge `37256036471` sobre `6271a75399732dfafcaef06ec5fd63ff5835a86b` están completos. `W01_APPLICATION_SHELL = CLOSED_WITH_NONBLOCKING_LIMITATIONS`; aceptación humana PASS, 7/7 tests PASS, onedir PASS y DuckDB incluido. Los estados `CLEAN_MACHINE_VALIDATION = PENDING` y `W02 = NEXT / NOT_STARTED` describen el cierre anterior a packaging y quedaron supersedidos por el estado W02–W08 vigente de arriba. W01 no cambió semántica de motor y no accedió a HOLDOUT. Dataset 019 sigue diferido. Detalles: [PROJECT_STATUS.md](PROJECT_STATUS.md), [informe W01](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_APPLICATION_SHELL.md), [W01-P](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_P_PACKAGED_SHELL_INTEGRATION.md), [W01-F](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W01_F_FINAL_PACKAGED_GUI_ACCEPTANCE.md), [W00-P](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_P_JSON_SERIALIZATION_OPTIMIZATION_PROOF.md) e [informe HOLDOUT](reports/TDL_AUDIT_INTERPRETATION_V1_HOLDOUT_CONTENT_BLIND_20261004.md).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.

## Antecedente de migración V1 — sustituido por el cierre

2026-10-07: nueva pasada completada sobre los 81 temporales antes inaccesibles: 489 archivos, 226 directorios y 635.338.932 bytes lógicos eliminados; MIGRATE_TO_P = NO. DEDICATED_PARTITION_MIGRATION_V1 = REVIEW_REQUIRED_PROTECTED_MATERIAL: la ACL del material privado de firma y la herencia más amplia de P: requieren resolver su política de acceso antes del traslado. Sin cutover ni retiro de raíces; HOLDOUT intacto. Expediente vigente: P:\TransitDataLab\03_Evidence\Historical\migration_v1\resume_report_20261007.md y final_footprint.json. Este estado no cambia los gates de producto.
## Antecedente de descomposición V1 — sustituido por el cierre

2026-10-07: `CANONICAL_WHOLESALE_MIGRATION = PROHIBITED`; `CANONICAL_CUTOVER = NO`. Descomposición completa: 28 hijos directos y 34.742 filas recursivas, sin seguir 15 reparse points y sin errores de acceso. La raíz medida tras retirar el PFX tiene 290.967 archivos, 150.733 directorios y 283.567.279.349 bytes lógicos. 06_Products explica 261,771 GiB. Distribución propuesta: 0,515 GiB para fuentes y metadata de cuatro repositorios independientes; 207,787 GiB de candidatos regenerables; 9,584 GiB de workspaces mixtos por revisar. No se ha efectuado limpieza adicional ni se ha declarado duplicidad por nombre. Checkpoints congelados, paquetes y evidencia se preservan fuera de la fuente.

Proyección conservadora de ingress a P: 105,308 GiB, conservando todas las unidades dudosas y otras raíces legacy y excluyendo regenerables; cabe con presupuesto de reconstrucción de runtime y reserva, pero no acredita transferencia, eliminación ni funcionamiento. Pendientes: reconciliar unidades mixtas y contratos de rutas, sanity checks por unidad, transferencia verificada y validación operacional antes del cutover.

La decisión privada de firma está resuelta: PFX trasladado a P:\TransitDataLab\Private\Signing, SHA-256 de origen/destino coincidentes y ACL de origen capturada; carpeta y PFX sin herencia, con acceso exclusivo para Yeison, SYSTEM y Administradores. Origen retirado tras verificar. El registro permanece restringido y no se publica en Git. HOLDOUT intacto; no se abrió, hasheó ni modificó su contenido. Este estado sustituye el bloqueo anterior por política de acceso al PFX y no cambia los gates de producto.

Expediente completo y columnas solicitadas: P:\TransitDataLab\03_Evidence\Historical\migration_v1\storage_decomposition\STORAGE_DECOMPOSITION.md, direct_children.json/csv, recursive_decomposition.json/csv, category_allocation.json y capacity_projection.json. Los informes y cambios locales previos se conservan. Sin commit, push ni publicación.
