# Transit Data Lab — mapa de estado vigente

**Actualizado:** 2026-10-05
**Fuente de detalle:** [PROJECT_STATUS.md](PROJECT_STATUS.md).

```text
TRANSIT DATA LAB
│
├── TRUST FOUNDATION                    ✅ CLOSED (gate técnico)
├── GTFS AUDIT ENGINE V1                ✅ CLOSED (alcance técnico documentado)
├── COMPLIANCE V1                       ✅ CLOSED_WITH_DEFERRALS
├── REMEDIATION ENGINE V1               ✅ CLOSED (alcance técnico documentado)
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
├── WINDOWS SELF-SERVICE CLIENT V1       🟡 W00 PASS_WITH_RESOURCE_LIMITATION; PUBLICATION PR IN PREPARATION
│   ├── W00-R / W00-O / W00-M / W00-P       DIAGNOSTICS COMPLETE / ROOT CAUSE UNKNOWN / SYNTHETIC CAUSE PROBABLE / PASS WITH LIMITATION
│   ├── Streaming JSON S1/S4/S64            BYTE + SEMANTIC EQUIVALENCE PASS
│   ├── Pico privado muestreado             −32,85 % / −72,95 % / −81,41 %
│   ├── Causa raíz sintética                CONFIRMED; no atribución a dataset 019
│   ├── W00-P regresión                     291 total / 290 PASS / 0 FAIL / 1 SKIP documentado; consolidación PASS
│   ├── Outputs sintéticos completos        NOT VERSIONED; retained locally; no cleanup
│   ├── PyInstaller + DuckDB               ONEDIR PASS; DuckDB 1.5.5; clean machine PENDING
│   ├── Hardware mínimo/recomendado        NOT_YET_ESTABLISHED
│   ├── Dataset 019 / soporte feeds extremos DEFERRED / NOT CERTIFIED
│   ├── QGIS                                EXTERNAL GIS EVIDENCE WORKBENCH; INTEGRATION NOT IMPLEMENTED
│   └── W01                                 NEXT_AFTER_W00_PUBLICATION; NOT STARTED
├── COMMERCIAL VALIDATION                ⚪ NOT_ESTABLISHED
├── GIS / QGIS                           🟡 SOPORTE Y EVIDENCIA CUANDO PROCEDA
│
└── BACKLOG POST-COMERCIALIZACIÓN        💤 FUERA DE LA SIGUIENTE FASE
    ├── SIRI
    ├── GTFS-RT
    ├── Colombia
    └── otros mercados y modos
```

El freeze funcional permanece en `9cafe0703abf47e80f67f80a6b423c938e1979aa`; la validación HOLDOUT no cambió ficheros funcionales versionados. La publicación de evidencia está publicada (PR #47, merge `69567c4a82d65e3017ee74ce64695a6a8334aa46`; CI post-merge `37230388650` PASS). Se preserva la historia del protocolo: `PRISTINE_BLIND_HOLDOUT = NO`; `CONTENT_BLIND_HOLDOUT = YES`. Generalización aprobada con limitaciones: 6/6 replays PASS, 530 findings, 3 familias, y una interpretación parcial (caso 00026; G04 en consolidación genérica). Los seis paquetes de evidencia y sus hashes están registrados en el manifiesto de HOLDOUT. No hay código específico de operador; validación comercial/mercado no establecida; no se reclama cumplimiento legal ni cobertura GTFS completa. W00-P queda listo para revisión humana tras pasar byte equivalence, semántica, replay y regresión; la mejora de memoria se confirma solo en sintético. Dataset 019 sigue diferido, la validación en máquina limpia pendiente y W01 sin iniciar. Los detalles están en [PROJECT_STATUS.md](PROJECT_STATUS.md), el [informe W00-P](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_P_JSON_SERIALIZATION_OPTIMIZATION_PROOF.md), el [informe histórico W00-M](reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_M_MEMORY_ROOT_CAUSE_ISOLATION.md) y el [informe HOLDOUT](reports/TDL_AUDIT_INTERPRETATION_V1_HOLDOUT_CONTENT_BLIND_20261004.md).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
