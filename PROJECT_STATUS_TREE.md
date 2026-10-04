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
├── AUDIT INTERPRETATION V1              ✅ VALIDATED_WITH_DOCUMENTED_LIMITATIONS
│   ├── DEVELOPMENT                       ✅ 14/14 OK; 14/14 replay; 92 findings / 7 families
│   ├── Interpretation                    ✅ 11 interpreted; 3 partial; 0 unknown / unsupported
│   ├── Dataset 019                       ⚠ 12m43s; ~18.89 GiB; optimization required
│   └── HOLDOUT                           ✅ 6/6; PASS_WITH_LIMITATIONS; content blind
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

El freeze funcional permanece en `9cafe0703abf47e80f67f80a6b423c938e1979aa`; la validación HOLDOUT no cambió ficheros funcionales versionados. Se preserva la historia del protocolo: `PRISTINE_BLIND_HOLDOUT = NO`; `CONTENT_BLIND_HOLDOUT = YES`. Generalización aprobada con limitaciones: 6/6 replays PASS, 530 findings, 3 familias, y una interpretación parcial (caso 00026; G04 en consolidación genérica). Los seis paquetes de evidencia y sus hashes están registrados en el manifiesto de HOLDOUT. Regresión: 279 PASS, 0 FAIL y 1 SKIP documentado. No hay código específico de operador; validación comercial/mercado no establecida; no se reclama cumplimiento legal ni cobertura GTFS completa. Windows Self-Service Client V1 continúa diferido. Los detalles están en [PROJECT_STATUS.md](PROJECT_STATUS.md) y el [informe HOLDOUT](reports/TDL_AUDIT_INTERPRETATION_V1_HOLDOUT_CONTENT_BLIND_20261004.md).

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
