# Gobierno del área Business

## Alcance y aislamiento

Este archivo rige el trabajo dentro de `07_Business`. El área Business está físicamente aislada y se ocupa de su documentación empresarial. No autoriza modificaciones fuera de este directorio.

La fase actual es **BUSINESS PHASE 3 — MARKET EVIDENCE**, **IN_PROGRESS**, con baseline de capacidades V1 FROZEN. El estado operativo se mantiene en BUSINESS_STATUS.md y las autorizaciones en 01_Governance/DECISION_LOG.md. Stage 1 = COMPLETE / APPROVED (BUS-DEC-025); Stage 2A = COMPLETE. La autorización explícita del usuario del 2026-09-27 cubre Stage 2B — auditoría documental, simulaciones sintéticas, identificación de organizaciones/roles/canales públicos y preparación del paquete de gate. No autoriza contacto externo, entrevistas ni envíos: EXTERNAL_CONTACT permanece NOT_AUTHORIZED hasta decisión humana expresa. No iniciar ejecución de entrevistas ni otros gates sin autorización expresa.

## Fuentes técnicas de verdad

Compliance y GTFS_Lab son las fuentes técnicas de verdad. Business no puede modificarlas, sustituirlas ni reinterpretarlas para favorecer objetivos comerciales.

El desarrollo comercial no debe condicionar ni alterar resultados, requisitos, evidencias o conclusiones técnicas de Compliance o GTFS_Lab. La documentación Business debe respetar sus conclusiones y límites.

Ninguna capacidad podrá presentarse comercialmente como existente sin evidencia técnica verificable. En la fase de capacidades, cada afirmación deberá identificar su fuente y evidencia, las condiciones y límites aplicables y su estado de verificación.

Se distinguirán explícitamente los estados **existente**, **en desarrollo** y **planificada**. La condición **pendiente de verificación** se registrará por separado cuando corresponda; nunca equivale a una capacidad demostrada. No inferir capacidades a partir del nombre del proyecto, de objetivos o de ideas.

## Progresión autorizada

La construcción empresarial seguirá esta secuencia:

1. Governance.
2. Capabilities.
3. Market.
4. Offering.
5. Economics.
6. Legal/commercial.
7. Go-to-market.

`02_Capabilities` y `03_Market` ya existen por autorizaciones registradas. Los directorios `04_Offering`, `05_Economics`, `06_Legal_and_Compliance` y `07_Go_to_Market` solo se crearán al iniciar formalmente su fase correspondiente. Los Business Stages no renumeran las Business Phases ni las Compliance Phases.

## Decisiones, hipótesis y evidencias

- Registrar decisiones aprobadas en `01_Governance/DECISION_LOG.md` con identificadores estables. No reutilizar identificadores ni cambiar silenciosamente decisiones aprobadas; registrar posteriores revisiones mediante una nueva entrada con referencia a la anterior.
- Registrar supuestos pendientes en `01_Governance/ASSUMPTIONS_REGISTER.md`. Distinguir decisiones, hipótesis y hechos comprobados.
- No convertir ideas comerciales en hechos ni asignar valores, precios o conclusiones sin respaldo.
- Mantener `BUSINESS_STATUS.md` actualizado con Completed, In progress, Blocked y Next actions, diferenciando trabajo realizado de trabajo futuro.
- Mantener `README.md` como guía de alcance y navegación.

## Nombre provisional y objetivo exploratorio

**Transit Data Lab** se adopta como **WORKING NAME**. No afirmar que sea una marca registrada, un nombre societario definitivo o una denominación jurídicamente disponible. Su disponibilidad deberá verificarse formalmente antes de una decisión definitiva de marca.

El objetivo empresarial inicial es explorar la futura comercialización de servicios/productos relacionados con calidad, validación, auditoría y compliance de datos de transporte público, siempre sujeto a capacidades técnicamente demostradas. Esta intención no acredita capacidades, demanda ni viabilidad comercial.

## Restricciones vigentes

Una tarea exclusivamente Business no autoriza modificaciones fuera de `07_Business`. La revisión global de alineación autorizada por el usuario puede leer documentación técnica y corregir gobierno vigente, preservando baselines y evidencias. No habilita desarrollo técnico ni ejecución de nuevas fases empresariales.

La investigación de mercado previa está registrada. Solo el diseño de customer discovery está autorizado por BUS-DEC-026; no iniciar entrevistas, pilotos, contacto, pricing, oferta o publicación sin autorización específica. No cambiar capacidades congeladas para acomodarlas a documentación nueva. Aplicar 03_Market/RESOURCE_USAGE_POLICY.md para controles de recursos: no hash global ni ejecución automática de verify_market.py. No hacer commit. Las restricciones iniciales de Phase 1 se interpretan como históricas, conforme a las autorizaciones posteriores registradas.

## Autoría

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
