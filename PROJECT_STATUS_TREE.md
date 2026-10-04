# Transit Data Lab — mapa de estado vigente

**Actualizado:** 2026-10-04
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
├── WINDOWS SELF-SERVICE CLIENT V1       ⏸ DEFERRED
├── COMMERCIAL VALIDATION                ⚪ NOT_ESTABLISHED
├── GIS / QGIS                           🟡 SOPORTE Y EVIDENCIA CUANDO PROCEDA
│
└── BACKLOG POST-COMERCIALIZACIÓN        💤 FUERA DE LA SIGUIENTE FASE
    ├── SIRI
    ├── GTFS-RT
    ├── Colombia
    └── otros mercados y modos
```

El expediente real permanece local y controlado; esta fase usó únicamente fixtures sintéticas. Yeison aprobó el cierre humano I01–I08. I01 se conserva sin cambios (SHA-256: `9AE821BA963849D341F509A74956DEF76C5739BD8175150198EA6A5F99CA7BD4`). La regresión registró 279 PASS, 0 FAIL y 1 SKIP documentado de 280 pruebas. HOLDOUT no se accedió ni se ejecutó el corpus DEVELOPMENT de 14 datasets. No hay código específico de operador; la validación comercial y de mercado no está establecida, y no se reclama cumplimiento legal ni cobertura GTFS completa. Windows Self-Service Client V1 continúa diferido. Los límites constan en [PROJECT_STATUS.md](PROJECT_STATUS.md) y la [revisión I08](reports/TDL_AUDIT_INTERPRETATION_CONSOLIDATION_V1_I08_CLOSURE_REVIEW.md).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
