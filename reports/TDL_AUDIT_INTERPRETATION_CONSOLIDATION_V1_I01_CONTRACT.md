# Audit Interpretation & Consolidation V1 — contrato I01

**Estado:** contrato definido para I01. No se implementan analizadores ni se inicia I02.

## Alcance

I01 fija estructura, vocabulario, invariantes y límites para añadir interpretación derivada a una auditoría GTFS. `source_findings` conserva los findings de entrada como evidencia primaria e inmutable. La capa derivada no puede borrarlos, reemplazarlos, reescribirlos ni ocultarlos. Este contrato no implementa una consolidación de runtime.

El esquema machine-readable está en [`audit_interpretation_contract_v1.schema.json`](../02_Data_Engineering/GTFS_Lab/spec/audit_interpretation_contract_v1.schema.json). La fixture sintética usada para el contrato está en [`audit_interpretation_v1_synthetic.json`](../02_Data_Engineering/GTFS_Lab/tests/fixtures/audit_interpretation_v1_synthetic.json).

## Modelo

`AuditInterpretationResult` incluye `dataset_identity`, `execution_identity`, `source_findings`, `finding_families`, `coverage`, `limitations` y `provenance`. Cada familia identifica regla, etapa, archivo y estado técnico; cuenta occurrences raw y entidades afectadas; expresa población y porcentaje cuando es evaluable; separa observaciones, cálculos e inferencias; contiene patrones, impacto, explicaciones, base de confianza, evaluación de remediación, referencias de evidencia y limitaciones.

Una entidad directa usa el vocabulario GTFS `agency`, `route`, `trip`, `service`, `stop`, `shape`, `stop_time`, `calendar`, `calendar_date`, `frequency` o `feed`. `operational_impact.direct_affected` y `propagated_usage` son campos separados: el uso propagado por viajes o rutas no aumenta el número de findings.

## Vocabulario epistemológico

- `OBSERVED`: dato o finding directamente observado.
- `CALCULATED`: resultado matemático reproducible a partir de evidencia identificable.
- `INFERRED`: interpretación plausible; nunca se convierte en hecho observado.
- `NOT_EVALUABLE`: evidencia o capacidad insuficiente para evaluar.

Los arrays separados `observations`, `calculations` e `inferences` exigen la clase epistemológica correspondiente. El estado `NOT_EVALUABLE` puede usarse en declaraciones cuando no se dispone de base suficiente.

Estados de patrón: `CONFIRMED_PATTERN`, `COMPATIBLE_PATTERN`, `MIXED_PATTERN`, `UNKNOWN_PATTERN`, `NOT_EVALUABLE`. Coincidencia exacta de coordenadas y distancia permite describir duplicación exacta confirmada. Distancia igual con coordenadas cambiadas puede ser compatible con cuantización, pero no prueba la causa.

## Invariantes y límites

Para cada grupo raw, las occurrences asignadas a patrones más las no clasificadas deben ser iguales al número raw. `coverage.accounting_gap` se define como la diferencia entre ambos lados; solo `0` permite `interpretation_status = COMPLETE`. Si no cierra, el resultado es `INCOMPLETE`. Una familia especializada puede subdividir un grupo, siempre preservando esa cardinalidad.

Los objetos raw originales se transportan íntegros en `source_findings`; el schema permite propiedades adicionales para no recortar extensiones o campos del emisor. Los `evidence_refs` enlazan IDs raw, archivo fuente, referencias de fila/entidad, SHA-256 del dataset e identidad de ejecución. La procedencia declara `raw_findings_immutable = true`.

No hay score global de calidad, cumplimiento legal, operador ni semáforo. No se define severidad por defecto. `TECHNICAL_FINDING` no implica `LEGAL_NONCOMPLIANCE`; `XSD_VALID` tampoco implica conformidad de perfil, aceptación NAP, cumplimiento regulatorio ni alta calidad de datos.

Remediación solo admite `SAFE_DETERMINISTIC`, `HUMAN_REVIEW`, `NOT_RECOMMENDED` o `NOT_EVALUABLE`. El contrato de interpretación no autoriza cambios y no sustituye los contratos del Remediation Engine.

I01 no fija todavía un algoritmo binario/hash de `family_id`. La identidad lógica determinista es la clave semántica `(rule_id, pattern_id, affected_entity_type)`; antes de runtime se debe cerrar su serialización sin ambigüedad ni colisiones. No se usan UUID aleatorios ni timestamps semánticos. `confidence_basis` permite registrar la justificación; no se asigna nivel ni porcentaje de confianza mientras no exista regla objetiva documentada.

## Fixture y contabilidad

El ejemplo no usa Tuvisa ni datos de operador: incluye 10 findings sintéticos de shapes. Ocho presentan distancia consecutiva igual con coordenadas cambiadas y quedan como `COMPATIBLE_PATTERN / QUANTIZATION_COMPATIBLE`; dos presentan coordenadas y distancia iguales y quedan como `CONFIRMED_PATTERN / EXACT_DUPLICATE_GEOMETRY`.

| Grupo | Findings raw | Shapes directos | Viajes propagados | Rutas propagadas |
| --- | ---: | ---: | ---: | ---: |
| Cuantización compatible | 8 | 4 | 15 | 3 |
| Geometría duplicada exacta | 2 | 1 | 2 | 1 |
| Total contable | 10 | — | — | — |

`raw_finding_count = 10`, `consolidated_occurrence_count = 10`, `unclassified_occurrence_count = 0`, `accounting_gap = 0`. Los conteos de impacto son sintéticos y deliberadamente distintos del conteo de findings.

## Compatibilidad y verificación

I01 es un contrato separado: no cambia GTFS Audit Engine V1, Compliance V1, Remediation Engine V1, Client Audit Workflow V1, Test Bank V1, replay ni delivery. No contiene código específico de operador. No accede a HOLDOUT ni ejecuta los 14 datasets DEVELOPMENT.

Los tests de contrato cubren inmutabilidad de entrada, conservación de cardinalidad, gap cero, unknown no clasificado, separación de impactos, etiquetas de inferencia, ausencia de score global y conclusión legal implícita, clave de familia estable y ajuste de la fixture al contrato. El test usa `jsonschema` Draft 2020-12 si está disponible; su fallback estándar cubre las palabras clave declaradas sin añadir dependencia al proyecto. La validación formal ejecutada en esta tarea usó `jsonschema` temporal fuera del repositorio. No se ejecutan analizadores ni suites de datasets.

Verificación registrada: `tests.test_audit_interpretation_contract` + `tests.test_audit_comparison`: **33 PASS**; `tests.test_remediation` + `tests.test_client_workflow` + `tests.test_test_bank`: **25 PASS**; fallos: **0**; omitidos: **0**. `Draft202012Validator.check_schema` pasó y la fixture obtuvo **0 errores**. `python -m json.tool` pasó para schema y fixture; `git diff --check` pasó. Las suites usaron fixtures y temporales de tests; no corrieron los 14 datasets DEVELOPMENT.

## Límites de I01

- No hay runtime de consolidación, análisis de patrones o cálculo de impacto.
- El proyecto no declara una dependencia JSON Schema validator; el test mantiene un fallback acotado en biblioteca estándar y la validación oficial Draft 2020-12 se ejecutó con un paquete temporal.
- La metodología para definir poblaciones GTFS, resolver impactos propagados, confianza cualitativa y serialización final sin colisiones de `family_id` requiere decisiones de fases posteriores.
- No se infiere validez legal, perfil, aceptación NAP, calidad integral, severidad o recomendación automática.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
