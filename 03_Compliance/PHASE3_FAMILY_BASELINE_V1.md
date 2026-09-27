# Phase 3 family planning baseline V1

BASELINE_NAME = `PHASE3_FAMILY_BASELINE_V1`

M01_STATUS = `M01_NOT_RECOVERABLE`

FAMILY_CLASSIFICATION_ROLE = `PLANNING_METADATA`

Estado: baseline de planificación revisada para las 48 filas actuales de `compliance.requirements`. Esta taxonomía facilita navegación y planificación; no es clasificación ni interpretación jurídica, validación de cumplimiento, representabilidad, aceptación de mappings, cobertura o resultado de auditoría. Se deriva del universo vigente y es independiente de M01, cuyo estado es `M01_NOT_RECOVERABLE`.

`mapping.phase3_families.provisional = FALSE` expresa que esta taxonomía fue revisada y aceptada como baseline de planificación actual. No expresa aprobación legal o técnica. Las membresías usan `REVIEWED`, nunca `APPROVED`. Confianza `LOW` no se usa como sustituto de incertidumbre jurídica.

## Taxonomía y límites de clasificación

| ID | Familia | Inclusión | Exclusión y límite |
|---|---|---|---|
| F01 | NAP access and discovery | Establecer el NAP, hacerlo punto único, publicar/acceder a datos por él, API pública y localizar datos. | No incluye formato/perfil ni los metadatos de procedencia; el simple hecho de mencionar el NAP no basta si el trabajo principal es otro. |
| F02 | Availability and format representation | Revisar formatos, normas, interoperabilidad y perfiles de intercambio exigidos para representar/intercambiar datos. | No concluye que un estándar represente plenamente un requisito ni que haya cobertura o cumplimiento. |
| F03 | Temporal coverage and deadlines | Fechas explícitas, etapas, alcance geográfico de disponibilidad y ventanas de despliegue. | No incluye actualización ordinaria por cambios del feed; fechas no crean mappings. |
| F04 | Metadata and provenance | Acordar y facilitar metadatos, atribución de fuente e intervalo de actualización. | No incluye las obligaciones sustantivas de calidad ni los datos de transporte subyacentes. |
| F05 | Update and correction | Propagar actualizaciones ante cambios conocidos y corregir inexactitudes. | No incluye el estándar general de exactitud/frescura ni plazos legales de despliegue. |
| F06 | Quality and notification | Exactitud, frescura, requisitos mínimos de calidad y comunicación de errores. | No incluye el acto posterior de corregir datos ni el metadata interval. |
| F07 | Reuse and journey presentation | Neutralidad/no discriminación en reutilización, criterios de ordenación y presentación de itinerarios. | No incluye el intercambio entre proveedores del resultado de encaminamiento. |
| F08 | Routing-result exchange | Comunicación, a petición, de resultados de encaminamiento entre proveedores. | No clasifica neutralidad, ranking o presentación al usuario. |
| F09 | Governance, evaluation, and process duties | Privacidad, evaluación/controles institucionales, poderes procedimentales e informes. | No absorbe obligaciones operativas de datos solo por su importancia jurídica. |

Regla repetible aplicada: se asignó una familia primaria según la preocupación de trabajo dominante en la fila materializada, usando `requirement_class` junto con su descripción. ACCESS, DISCOVERY y DATA_AVAILABILITY → F01; FORMAT e INTEROPERABILITY → F02; DEADLINE → F03; METADATA → F04; UPDATE → F05; QUALITY → F06; REUSE → F07; ROUTING → F08; clases restantes → F09. No se añadieron secundarias porque no aportaban valor suficiente para planificar otro trabajo paralelo.

## Conteos y límites de la comparación con M05

| ID | Total primaria | Pilotos | Restantes | M05 provisional restante | Diferencia |
|---|---:|---:|---:|---:|---:|
| F01 | 8 | 1 | 7 | 5 | +2 |
| F02 | 8 | 1 | 7 | 7 | 0 |
| F03 | 9 | 1 | 8 | 8 | 0 |
| F04 | 4 | 1 | 3 | 2 | +1 |
| F05 | 3 | 0 | 3 | 4 | -1 |
| F06 | 4 | 0 | 4 | 2 | +2 |
| F07 | 5 | 0 | 5 | 5 | 0 |
| F08 | 1 | 0 | 1 | 1 | 0 |
| F09 | 6 | 1 | 5 | 9 | -4 |

El dato M05 conservado para este trabajo solo aporta conteos agregados, no asignaciones por `requirement_id`. Por ello no permite afirmar qué filas concretas fueron movidas desde/hacia M05. Como trazabilidad de cada diferencia, los IDs actuales que componen las familias afectadas son:

- F01 restante (7): `EU-2017-1926-REQ-A03-P01-001`, `EU-2017-1926-REQ-A03-P01-002`, `EU-2017-1926-REQ-A03-P03-001`, `EU-2017-1926-REQ-A04-P04-001`, `EU-2017-1926-REQ-A05-P01-001`, `EU-2017-1926-REQ-A08-P01-001-01-A`, `EU-2017-1926-REQ-A08-P01-001-01-B`. El criterio agrupa establishment/discovery y disponibilidad por NAP; el agregado M05 no permite atribuir los dos registros de diferencia a una pareja histórica concreta.
- F04 restante (3): `EU-2017-1926-REQ-A03-P04-001-01`, `EU-2017-1926-REQ-A03-P04-001-02`, `EU-2017-1926-REQ-A08-P03-001-02`. Incluye los acuerdos y provisión de metadatos y el intervalo de actualización declarado como metadato; M05 no identifica cuál fila explica el +1.
- F05 restante (3): `EU-2017-1926-REQ-A06-P02-001-01`, `EU-2017-1926-REQ-A06-P02-001-02`, `EU-2017-1926-REQ-A06-P02-001-03`. La clasificación separa actualización/corrección de calidad; el total M05 excedía este grupo en uno sin preservar su ID.
- F06 restante (4): `EU-2017-1926-REQ-A04-P05-001`, `EU-2017-1926-REQ-A08-P01-001-02`, `EU-2017-1926-REQ-A08-P01-001-03`, `EU-2017-1926-REQ-A08-P01-001-04`. Incluye aviso de inexactitud, exactitud/frescura y requisitos mínimos de calidad; M05 no permite identificar qué dos filas causan el +2.
- F09 restante (5): `EU-2017-1926-REQ-A04-P06-001`, `EU-2017-1926-REQ-A09-P01-001`, `EU-2017-1926-REQ-A09-P02-DOCUMENT_REQUEST`, `EU-2017-1926-REQ-A10-P01-001`, `EU-2017-1926-REQ-A10-P02-001`. La familia se acota a privacidad, evaluación/proceso e informes; los 4 registros de diferencia no pueden desglosarse sin las membresías históricas por ID.

Estas diferencias se conservan; no se modificaron familias para reproducir M05. M01 no se reconcilia.

## Pilotos y B01

| Registro | Primaria | Confianza |
|---|---|---|
| `EU-2017-1926-REQ-A04-P01-001` | F01 | HIGH |
| `EU-2017-1926-REQ-A04-P02-001` | F02 | HIGH |
| `EU-2017-1926-REQ-A08-P03-001-01` | F04 | HIGH |
| `EU-2017-1926-REQ-A05-P03-001` | F03 | HIGH |
| `EU-2017-1926-REQ-A09-P03-RANDOM_CHECKS` | F09 | MEDIUM |

B01: `EU-2017-1926-REQ-A03-P01-001`, `EU-2017-1926-REQ-A03-P01-002` y `EU-2017-1926-REQ-A03-P03-001` pertenecen a F01. Son un lote coherente para revisar establecimiento del punto, acceso único y descubrimiento/localización. B01 sigue siendo una primera expansión recomendable por su delimitación temática. No requiere investigar perfiles de formatos antes de empezar, pues no es una clasificación F02. Esta conclusión de planificación no aprueba mappings.

## Reproducibilidad y validación

La migración `sql/00_setup/008_phase_3_m05b_family_classification_metadata.sql` es una migración transaccional de única ejecución: exige que el esquema aún no tenga las columnas nuevas y que la tabla familiar esté vacía, reconstruye la tabla preservando PK/FK y aborta con rollback si los prechecks o postchecks fallan. La migración se aplica antes del seed; repetirla después falla deliberadamente para evitar una reconstrucción accidental. La base local ya presenta el esquema migrado. El seed posterior sí es idempotente y valida el estado previo antes de insertar.

El seed `sql/03_mappings/phase3_m05b_family_baseline_v1_seed.sql` deriva IDs de la tabla de requisitos vigente, exige exactamente 48 registros y nueve familias, y aborta ante datos previos incompatibles. Inserta solo nueve familias y 48 membresías primarias. Repetirlo conserva conteos y filas; no crea secundarias. El validator `sql/07_tests/phase_3/validate_phase_3_m05b_family_baseline_v1.sql` revisa cobertura, vocabularios, referencias, pilotos, B01 y límites de estado.

Conteo validado: 9 familias; 48 membresías primarias; 0 secundarias; 0 sin primaria, con múltiples primarias, IDs desconocidos, duplicados, motivos ausentes o confianza inválida. Confianza: HIGH = 41, MEDIUM = 7, LOW = 0. Mapping semantics unchanged; coverage semantics unchanged. B01 coherente y recomendado como primer lote; profile research no es necesario antes de B01. Sus tres requisitos son F01. No se crean mappings.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
