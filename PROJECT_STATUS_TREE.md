# Transit Data Lab — mapa de estado vigente

**Actualizado:** 2026-10-07
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
