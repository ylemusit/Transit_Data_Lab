# Phase 2 — Legal Requirements Engine (2017/1926)

- Fecha de ejecución: 2026-09-27 01:26:01 +02:00
- Versión fuente: EU-REG-2017-1926 consolidada 2024-03-04; 10/10 hashes de fuentes legales verificados.
- Provisions analizadas/clasificadas: 92 / 92
- Candidates: 34; APPROVED: 3; NEEDS_REVIEW: 31; REJECTED: 0
- Requirements materializados: 3
- Deadlines definitivas: 1
- Anomalías Phase 1 registradas y preservadas: 2
- Tests del master SQL y SHA-256 de ficheros fuente: 29/29 PASS, 0 FAIL
- Protección Phase 1: PASS (snapshots de documents/provisions/relationships iguales; 10/10 SHA-256 jurídicos iguales; 2017/1926 = 92 provisions)
- Fuera de alcance preservado: mapping.format_coverage=0, audit.rules=0

## Decisiones de extracción

- La clasificación de las 92 provisions no las convierte automáticamente en obligaciones.
- Solo se materializan deberes cuya cita indica directamente actor y acción (NAP del artículo 3(1) e informe del artículo 10(1)). El informe mantiene su fecha histórica vencida sin concluir incumplimiento.
- Los calendarios de artículos 4 y 5 quedan en revisión por excepciones, categorías y alcance de red/modos. Sus fechas solo se guardan como datos de candidatos.
- Requisitos de formato sujetos a otras normas, condiciones técnicas, alcance del artículo 5(4), calidad y atomicidad, reutilización neutral, corrección de datos y evaluación requieren revisión humana.
- Los extractos fuente y descripciones normalizadas están separados. No se modifica source.provisions.

## Revisión humana pendiente

1. Verificar las excepciones por datos y modo de transporte de cada fecha del artículo 4(3), y las categorías/redes del artículo 5(3).
2. Resolver responsabilidades, condiciones y granularidad de metadatos, acceso API, calidad, actualización, encaminamiento y reutilización.
3. Interpretar las remisiones a los actos externos listados en PHASE_2_CANDIDATES.csv sin ampliar aquí el corpus.
4. Revisar si las dos obligaciones aprobadas deben conservar su granularidad propuesta.
5. Mantener visibles los IDs Annex 1.3 B-I/D-I y confirmar su correspondencia jurídica en una tarea separada; no se corrigieron.

La extracción no afirma cumplimiento jurídico. Un error GTFS no es una conclusión de incumplimiento.

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
