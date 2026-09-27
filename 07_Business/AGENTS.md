# Gobierno del área Business

## Alcance y aislamiento

Este archivo rige el trabajo dentro de `07_Business`. El área Business está físicamente aislada y se ocupa de su documentación empresarial. No autoriza modificaciones fuera de este directorio.

La fase actual es **BUSINESS PHASE 1 — DOCUMENT GOVERNANCE**. Su alcance se limita a la infraestructura mínima de gobierno documental. No se debe iniciar otra fase sin autorización expresa.

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

Los directorios `02_Capabilities`, `03_Market`, `04_Offering`, `05_Economics`, `06_Legal_and_Compliance` y `07_Go_to_Market` solo se crearán al iniciar formalmente su fase correspondiente.

## Decisiones, hipótesis y evidencias

- Registrar decisiones aprobadas en `01_Governance/DECISION_LOG.md` con identificadores estables. No reutilizar identificadores ni cambiar silenciosamente decisiones aprobadas; registrar posteriores revisiones mediante una nueva entrada con referencia a la anterior.
- Registrar supuestos pendientes en `01_Governance/ASSUMPTIONS_REGISTER.md`. Distinguir decisiones, hipótesis y hechos comprobados.
- No convertir ideas comerciales en hechos ni asignar valores, precios o conclusiones sin respaldo.
- Mantener `BUSINESS_STATUS.md` actualizado con Completed, In progress, Blocked y Next actions, diferenciando trabajo realizado de trabajo futuro.
- Mantener `README.md` como guía de alcance y navegación.

## Nombre provisional y objetivo exploratorio

**Transit Data Lab** se adopta como **WORKING NAME**. No afirmar que sea una marca registrada, un nombre societario definitivo o una denominación jurídicamente disponible. Su disponibilidad deberá verificarse formalmente antes de una decisión definitiva de marca.

El objetivo empresarial inicial es explorar la futura comercialización de servicios/productos relacionados con calidad, validación, auditoría y compliance de datos de transporte público, siempre sujeto a capacidades técnicamente demostradas. Esta intención no acredita capacidades, demanda ni viabilidad comercial.

## Restricciones de la Fase 1

No inspeccionar otras carpetas ni modificar archivos fuera de `07_Business`. No investigar mercado, competidores o marcas; establecer pricing; crear landing pages, material comercial o paquetes de servicios; realizar afirmaciones sobre capacidades técnicas; ni contactar terceros.

La verificación final se limitará a la documentación de este directorio y a `git diff`/`git status` para comprobar el alcance. No hacer commit. Esperar autorización para Business Phase 2.

## Autoría

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
