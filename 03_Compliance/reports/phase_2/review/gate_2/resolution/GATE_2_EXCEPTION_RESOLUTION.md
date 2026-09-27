# Gate 2 - resolución de excepciones

GATE_2_EXCEPTION_RESOLUTION = PASS

GATE_2_READY_FOR_FINAL_APPROVAL = YES

Gate 2 permanece abierto. No se materializa, no se inicia Phase 3, no se congela Phase 2. project_baseline.json permanece intacto. No se concluye cumplimiento jurídico.

## Resultado

- SHA antes: `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`
- SHA después: `ef8908038f92abaa6a150859d64b483916822cf266399d54e323c0d8bc8a8668`
- DB unchanged = YES; existing DB rows changed = NO.
- Universo inicial 45; padres superseded 2; hijos 5; universo final 48.
- Elegibles (preparatorio): 47; bloqueados: 1. Incluye tres coincidencias ya materializadas, conservadas sin modificaciones.
- Cola final: 1; cuestiones interpretativas pendientes: 0.
- Siete dependencias PARTIAL conservadas; instrumentos externos no consultados ni interpretados.

## Resoluciones humanas

- G2-017: UNSPECIFIED_IN_PROVISION; operational_subject = API providing access through NAP. Accesibilidad pública y registro previo cuando proceda conservados.
- G2-032: dos hijos DATA_ACCESS_REUSE y REUSE_TIMELINESS, con información sobre calidad y actor UNSPECIFIED_IN_PROVISION. El plazo funcional no es DATE ni SLA.
- G2-036/G2-037/G2-038: UNSPECIFIED_IN_PROVISION. Sujeto gramatical documentado en actor CSV, confianza HIGH en la decisión conservadora (no en identificar un actor ausente).
- G2-037: tres hijos RANKING_TRANSPARENCY, PROHIBITED_RANKING_FACTORS, NON_DISCRIMINATORY_APPLICATION. Identidad, consideración comercial cuando la hubiera y todos los usuarios de datos o finales participantes conservados.
- G2-038: presentación inicial no engañosa, independiente y sin split.
- G2-030: METADATA_CORRECTION; oportunamente; FUNCTIONAL_TIME_REQUIREMENT; deadline_date = NULL.
- Artículo 9(2): PROCEDURAL_POWER no obligatorio. Artículo 9(3): VERIFICATION_DUTY obligatorio.

## Estados humanos

- APPROVED_PENDING_MATERIALIZATION: 31
- APPROVED_WITH_CHANGES_PENDING_MATERIALIZATION: 9
- APPROVED_WITH_EXTERNAL_DEPENDENCY: 7
- READY_PENDING_SOURCE_FACT_PERSISTENCE: 1

HOLD = 0; REJECT = 0.

## Operación de persistencia propuesta para 9(3)

PROPOSED_NOT_PERSISTED. Identificador determinista `EU-2017-1926-SF-A09-P03`, según patrón SF-Axx-Pxx existente, sin colisión. G2-045 = READY_PENDING_SOURCE_FACT_PERSISTENCE, materialization_eligible = FALSE, blocker = SOURCE_FACT_NOT_PERSISTED.

En una ejecución autorizada por separado, insertar exactamente una fila en compliance.source_facts usando las ocho columnas existentes: source_fact_id <- proposed_source_fact_id; source_document_id; source_provision_id; legal_reference; source_fact_text; source_version_date; source_uri; notes. Los valores exactos están en ARTICLE_9_3_SOURCE_FACT_PROPOSAL.csv. article, paragraph, fact_type, normalized_fact y persistence_status son metadatos de propuesta, no columnas nuevas de DB. No se incluye ninguna operación sobre requirements o deadlines. Debe revalidarse ausencia de colisión al autorizar la persistencia.

Corpus local consolidado ES 04/03/2024: páginas 6, 8, 9 y 10 contrastadas. PDF SHA-256: `0a91ab5ffcf0466d588da8a8db7f7e7ed6d97b4d64576c31e083610fcd5b08d5`. El texto de 9(3) se reproduce literalmente con normalización de saltos de línea.

## Codificación

DB_ENCODING_OK = YES. CSV_ENCODING_OK = NO en entradas / YES en nuevos informes. MARKDOWN_ENCODING_OK = NO en review pack original / YES en nuevos informes. ENCODING_REQUIRES_DB_REPAIR = NO. Entradas históricas preservadas.

## Verificación durable

| Comprobación | Resultado |
|---|---|
| Entry DuckDB SHA | PASS |
| Original universe 45, Gate 1 proposals 43 + Article 9(2)/(3) | PASS |
| Entry decision distribution | PASS |
| Entry fidelity/atomicity/actor/exception counts | PASS |
| Input alignment GATE_2_SOURCE_FIDELITY.csv | PASS |
| Input alignment GATE_2_ATOMICITY.csv | PASS |
| Input alignment GATE_2_ACTORS.csv | PASS |
| Input alignment GATE_2_CONDITIONALITY.csv | PASS |
| Input alignment GATE_2_TEMPORAL.csv | PASS |
| Input alignment GATE_2_AUDITABILITY.csv | PASS |
| Seven PARTIAL dependencies at entry | PASS |
| DB encoding correct | PASS |
| Existing 3 requirements and 1 deadline | PASS |
| Persisted source fact traceability | PASS |
| Local corpus literal G2-017 | PASS |
| Local corpus literal G2-030 | PASS |
| Local corpus literal G2-032 | PASS |
| Local corpus literal G2-036 | PASS |
| Local corpus literal G2-037 | PASS |
| Local corpus literal G2-038 | PASS |
| Local corpus literal G2-045 | PASS |
| Local consolidated corpus hash | PASS |
| Child ID no collision G2-032-A | PASS |
| Child ID no collision G2-032-B | PASS |
| Child ID no collision G2-037-A | PASS |
| Child ID no collision G2-037-B | PASS |
| Child ID no collision G2-037-C | PASS |
| Article 9(3) deterministic source fact no collision | PASS |
| G2-032 superseded with exactly two children | PASS |
| G2-037 superseded with exactly three children | PASS |
| Final universe 45 - 2 + 5 = 48, unique IDs | PASS |
| No ambiguous slash actor | PASS |
| G2-017 actor conservative | PASS |
| G2-030 metadata correction | PASS |
| G2-028/029 substantive and temporal metadata unchanged | PASS |
| Functional expressions non-date | PASS |
| Seven PARTIAL preserved | PASS |
| 9(2) procedural power non-mandatory | PASS |
| 9(3) verification mandatory blocked | PASS |
| Eligibility prerequisites | PASS |
| No Annex B-I/D-I introduced | PASS |
| Unaddressed propositions unchanged, no universal format or GTFS compliance inference | PASS |
| No external instrument interpreted: preserved documentary references | PASS |
| Output data encoding clean | PASS |
| Resolution directory empty before authoring | PASS |
| Existing rows unchanged after read-only work | PASS |
| DuckDB hash after identical | PASS |
| Original Gate 2 reports and baseline unchanged | PASS |
| Regenerated CSV roundtrip 48 | PASS |
| New reports encoding UTF-8 clean | PASS |
| Git state preserved without staging/commit/push | PASS |

No se ha reinterpretado el universo completo. La comprobación de trazabilidad no reabre las filas aprobadas sin excepción. No se añadieron dependencias Annex B-I/D-I ni obligaciones universales NeTEx/SIRI/GTFS ni inferencias de incumplimiento basadas en validación GTFS.

## Git

Antes:

```text
?? .gitignore
?? 02_Data_Engineering/
?? 03_Compliance/
?? PROJECT_CURRENT_STATE.md
?? project_baseline.json
?? reports/
```

Después:

```text
?? .gitignore
?? 02_Data_Engineering/
?? 03_Compliance/
?? PROJECT_CURRENT_STATE.md
?? project_baseline.json
?? reports/
```

Sin git add, commit ni push.

## Archivos

- GATE_2_EXCEPTION_RESOLUTION.md
- GATE_2_EXCEPTION_RESOLUTION.csv
- GATE_2_FINAL_ATOMIC_UNIVERSE.csv
- GATE_2_FINAL_ATOMIC_UNIVERSE.md
- ARTICLE_9_3_SOURCE_FACT_PROPOSAL.csv
- GATE_2_ACTOR_RESOLUTION.csv
- GATE_2_SPLIT_RESOLUTION.csv
- GATE_2_TEMPORAL_CORRECTIONS.csv
- GATE_2_ENCODING_CHECK.md
- GATE_2_FINAL_EXCEPTION_QUEUE.csv

Autor del proyecto: Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
