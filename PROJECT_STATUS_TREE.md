# Transit Data Lab — mapa visual del estado

**Actualizado:** 2026-10-01
**Fuente detallada y de verdad:** [PROJECT_STATUS.md](PROJECT_STATUS.md)
**Regla:** este mapa resume el estado vigente; los documentos enlazados contienen evidencia y límites.

```text
TRANSIT DATA LAB
│
├── 1. TRUST FOUNDATION                              ✅ COMPLETADO — PASS TÉCNICO
│   ├── M01 Trust Contract                           ✅ PASS
│   ├── M02 Audit Manifest / Findings Persistence    ✅ PASS
│   ├── M03                                          ✅ PASS
│   ├── M04 Corpus / Holdout / Replay                ✅ CERRADO; HOLDOUT V2 COMPLETADO
│   ├── M05 Change Attribution                       ✅ PASS
│   └── TDL_TRUST_FOUNDATION                         ✅ PASS TÉCNICO
│
├── 2. GTFS AUDIT ENGINE V1                          🚧 ACTIVO — G08 EN REVISIÓN LOCAL
│   ├── G01 Scope / Specification / Gap Matrix       ✅ PASS / CLOSED
│   ├── G02 Rule Registry / Specification Contract   ✅ PASS / CLOSED / DURABLE
│   ├── G03 Structure / Schema / Types               ✅ PASS / CLOSED
│   │   ├── File catalog / CSV structure             ✅ IMPLEMENTADO Y VERIFICADO
│   │   ├── Presence conditions                      🟡 16 RESUELTAS; 15 PENDIENTES
│   │   ├── Capability map                           ✅ 106 ejecutables; 11 parciales; 15 sin resolver
│   │   ├── Field contract                            ✅ VALIDADO CON BRECHAS DE METADATOS
│   │   ├── Header/schema y field type/format         ✅ CERRADOS EN EL ALCANCE IMPLEMENTADO
│   │   ├── Specification metadata / extensions      🟡 BRECHAS Y POLÍTICA DE EXTENSIONES ABIERTAS
│   │   └── Formal closure / PR #24                  ✅ MERGED; CI POST-MERGE PASS
│   ├── G04 Identity / Referential Integrity         ✅ PASS / CLOSED; MERGED Y VERIFICADO
│   ├── G05 Calendar / Temporal                      ✅ PASS / CLOSED; MERGED Y VERIFICADO
│   ├── G06 stop_times / Sequence / Operational      ✅ PASS / CLOSED; MERGED Y VERIFICADO
│   ├── G07 Shapes / Spatial                         ✅ PASS / CLOSED; MERGED Y VERIFICADO
│   ├── G04–G07 PR #26 / CI post-merge               ✅ MERGED / PASS (run 36791698098)
│   ├── G08 Quality                                  🟡 TRABAJO POSTERIOR; LOCAL; NO PUBLICADO NI INTEGRADO
│   ├── G09 Reporting / Evidence Integration         ⏳ PENDIENTE
│   ├── G10 Authorized Development Corpus Evaluation ⏳ PENDIENTE; HOLDOUT NO EJECUTADO
│   └── G11 V1 Closure Gate                          ⏳ PENDIENTE
│       └── GTFS completo / cumplimiento jurídico   ⚪ NO ESTABLECIDO
│
├── 3. REMEDIATION ENGINE / DATA IMPROVEMENT         ⏳ FUTURO; SIN FASE ACTIVA REGISTRADA
├── 4. REGULATORY ALIGNMENT                          🟡 BASE DOCUMENTAL EN COMPLIANCE; SIN CIERRE JURÍDICO
├── 5. NeTEx READINESS                               🟡 TRACK TÉCNICO ACOTADO CON FIXTURES; NO COMPLETO
├── 6. NeTEx AUDIT ENGINE                            ⏳ SIN MOTOR DEDICADO REGISTRADO
├── 7. INTEROPERABILITY                              ⏳ MAPPINGS PENDIENTES
├── 8. COMPLIANCE                                    🟡 V1 CLOSED_WITH_DEFERRALS
│   ├── Phase 1 / 2                                  🧊 FROZEN
│   ├── Phase 3                                      ✅ CLOSED_WITH_DEFERRALS (alcance GTFS/NeTEx V1)
│   ├── GTFS / NeTEx                                 🟡 Scopes reproducibles con fixtures sintéticos
│   └── SIRI / GTFS-RT                               💤 STANDBY
├── 9. GIS / QGIS EVIDENCE WORKBENCH                 🟡 GIS EXISTENTE; REPRODUCIBILIDAD INTEGRAL PENDIENTE
├── 10. CLIENT AUDIT PACKAGING                       ⏳ SIN CIERRE / PAQUETE VIGENTE REGISTRADO
├── 11. MARKET / SERVICE VALIDATION                  🚧 BUSINESS PHASE 3 EN CURSO; MERCADO NO VALIDADO
│   ├── Stage 1                                      ✅ COMPLETE / APPROVED (15/15)
│   ├── Stage 2A                                     ✅ DISEÑO DOCUMENTAL COMPLETO
│   ├── Stage 2B                                     ✅ PREPARACIÓN DOCUMENTAL COMPLETA
│   ├── Contact Gate V2                              🟡 NOT_READY; revisión profesional y canal pendientes
│   └── Contacto externo / entrevistas               ⛔ NO AUTORIZADOS / NO REALIZADOS
├── 12. COLOMBIA MARKET STUDY                        ⚪ SIN ESTADO VIGENTE DOCUMENTADO
├── 13. SIRI / GTFS-RT                               💤 STANDBY
└── 14. FUTURE MULTIMODAL EXPANSION                  ⏳ FUTURO; SIN ALCANCE APROBADO REGISTRADO
```

## Límites que acompañan al mapa

- El cierre G04–G07 acredita integración y verificación técnica del alcance implementado. No se ejecutó HOLDOUT; no acredita resultados HOLDOUT, cumplimiento GTFS completo ni cumplimiento jurídico.
- Los findings G04 no forman actualmente parte de `validation.findings`; M02 no normaliza findings G04–G07. El manifest conoce indirectamente los artefactos del run y legacy sigue productivo donde corresponde.
- Se mantienen los gaps y deferrals, sin declarar persistencia M02 de findings G04–G07, equivalencia total con legacy ni cobertura de features diferidas. `CREATED_LOCAL_UNPUBLISHED` del inventario G04 sigue como deuda contractual conocida.
- G03 conserva brechas de metadatos normativos y política de extensiones. Las condiciones pendientes siguen explícitas.
- Compliance y Business tienen fases y gates propios. Un PASS técnico o documental no equivale a aprobación jurídica, validación de mercado ni autorización de contacto.
- Los estados “sin estado vigente documentado” indican que no se encontró una fuente actual que permita asignar otro estado; no significan que el trabajo no exista.

## Mantenimiento

Al cerrar cada paso que cambie el estado, actualizar este mapa y `PROJECT_STATUS.md` en la misma tarea, después de verificar el resultado. Anotar fecha, evidencia y siguiente paso; conservar los límites y estados de autorización. Si el paso no cambia estado, no tocar el mapa. Las áreas con fuente propia se contrastan con ella antes de editar este resumen.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
