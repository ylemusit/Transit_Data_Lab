# Phase 2 — Legal Requirements Engine

## Alcance actual

La primera extracción trata únicamente `EU-REG-2017-1926`, versión consolidada de 4 de marzo de 2024. La fuente de referencia es el HTML español de EUR-Lex (CELEX `02017R1926-20240304`). No se procesan las normas relacionadas ni se deducen obligaciones de formatos, validaciones GTFS, NAP o auditoría.

Phase 1 permanece congelada. Sus tablas `source.documents`, `source.provisions` y `source.relationships` son entradas de solo lectura. Las filas que ya existen, incluidas las normalizaciones y anomalías de Annex 1.3, no se corrigen en Phase 2.

## Arquitectura

```text
source.provisions (Phase 1, solo lectura)
  -> compliance.provision_classifications (clasificación conceptual)
  -> compliance.source_facts (citas/extractos fuente con versión y referencia)
  -> compliance.requirement_candidates (normalización y revisión)
       + compliance.requirement_candidate_sources (soporte adicional, incluido el anexo)
  -> compliance.requirements (solo candidatos aprobados)
  -> compliance.deadlines (fechas justificadas y vinculadas a requisito)
```

`compliance.requirements` y `compliance.deadlines` ya existían y se reutilizan. Las tablas nuevas son `compliance.provision_classifications`, `compliance.source_facts`, `compliance.requirement_candidates` y `compliance.requirement_candidate_sources`. El `source_fact_text` conserva el hecho fuente separado de `description`, que expresa la interpretación normalizada. La referencia y los identificadores de documento/provision conservan la trazabilidad; la tabla de soporte permite asociar varios puntos del anexo a un candidato sin sustituir su artículo principal.

Las provisions se clasifican con `DEFINITION`, `SCOPE`, `OBLIGATION`, `CONDITION`, `PERMISSION`, `EXCEPTION`, `DEADLINE`, `PROCEDURAL`, `REFERENCE` u `OTHER`. En artículos que contienen varios tipos, la clasificación a nivel de artículo es orientativa; cada candidato lleva su propia clasificación más específica. Una entrada del anexo describe categoría de datos y no crea por sí sola una obligación.

## Flujo de revisión y atomicidad

Los estados son `PENDING`, `APPROVED`, `REJECTED` y `NEEDS_REVIEW`. El seed solo propone aprobados para dos deberes del artículo 3, apartado 1, y el deber histórico de informe del artículo 10, apartado 1, cuya acción, actor y alcance aparecen expresamente en la fuente. El resto de los candidatos quedan `NEEDS_REVIEW`. Una clasificación no genera automáticamente un requisito.

Cada candidato representa un deber o una regla revisable con su cita de origen. Los apartados de calendario del artículo 4 se mantienen en candidatos separados por letra; sus exclusiones y ámbitos se conservan como notas de revisión. No se fijan plazos funcionales como fechas. El deber de informar de 2019 es un requisito histórico con deadline explícita; no se interpreta su vencimiento como conclusión de incumplimiento.

Las clases controladas justificadas por los candidatos de esta extracción son `DATA_AVAILABILITY`, `ACCESS`, `FORMAT`, `INTEROPERABILITY`, `METADATA`, `UPDATE`, `QUALITY`, `DISCOVERY`, `REUSE`, `ROUTING`, `ASSESSMENT`, `REPORTING`, `DEADLINE` y `OTHER`. `OTHER` se usa para la exclusión de datos personales del artículo 4(6), cuya definición remite al Reglamento (UE) 2016/679 y queda pendiente de revisión. GTFS no se incorpora como formato obligatorio. Las referencias a 2015/962, 454/2011, 2007/2/CE, 2016/679 y Directiva 2010/40/UE quedan identificadas como dependencias que pueden requerir revisión; no se amplía la extracción a esos actos.

Los identificadores de candidato y requisito son deterministas y expresan norma, artículo, apartado y secuencia. La secuencia no altera ni inventa numeración legal. Los identificadores principales no son UUID.

## Deadlines y límites

Una deadline definitiva requiere un requisito aprobado y contiene `requirement_id`, fecha, tipo, descripción, documento y provision fuente. Las fechas explícitas de candidatos pendientes permanecen en staging, sin materializarse en `compliance.deadlines`. No se calculan fechas a partir de otras normas o de la entrada en vigor.

La fuente primaria de Phase 1 no almacena el texto completo de los artículos. Por eso `compliance.source_facts` guarda extractos literales de la versión consolidada española, junto con la referencia jurídica y URL, sin rellenar ni sobrescribir `source.provisions`. `description` es la normalización y no sustituye el hecho fuente.

La pareja `EU-2017-1926-ANNEX-1.3-B-I` / `...-D-I` se registra como anomalía preservada: sus referencias fuente son `Annex 1.3(b)` y `Annex 1.3(d)`, sin subinciso romano en esas referencias. El contenido existente no se ha alterado.

## Pruebas y ejecución

Ejecutar desde cualquier directorio:

```powershell
& '<ruta-del-repositorio>\03_Compliance\sql\00_setup\run_phase_2_2017_1926.ps1'
```

El orquestador comprueba versión y baselines, compara los snapshots pre-Phase 2 de documentos/provisions/relaciones, verifica los SHA-256 del corpus legal, aplica migración y seed idempotentes, materializa candidatos `APPROVED`, ejecuta `sql/07_tests/phase_2/test_phase_2_master.sql`, exporta los informes y vuelve a verificar Phase 1. La base DuckDB cambia legítimamente; su hash completo no es una protección aplicable.

Los resultados se guardan en `reports/phase_2/`. Los tests prueban trazabilidad, vocabularios, materialización, alcance, fechas, que `mapping.format_coverage` y `audit.rules` sigan vacíos y que las tablas congeladas sigan idénticas a sus snapshots. La comprobación del SHA-256 físico de los documentos jurídicos la realiza el orquestador.

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
