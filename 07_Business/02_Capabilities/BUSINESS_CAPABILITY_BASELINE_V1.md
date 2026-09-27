# BUSINESS_CAPABILITY_BASELINE_V1

Baseline ID: **BUSINESS_CAPABILITY_BASELINE_V1**

Fecha: **2026-09-27** (Europe/Madrid). Estado: **FROZEN**.

BUSINESS_PHASE_2_BASELINE_REVIEW = **PASS**. Business Phase 3: **NOT STARTED**.

## Alcance y exclusiones

“El conjunto de capacidades que Transit Data Lab puede sostener, a esta fecha, exclusivamente mediante evidencia técnica identificada.”

Representa evidencia disponible y capacidades estrictamente acotadas en la fecha indicada. Las demostraciones históricas siguen siendo históricas; no acreditan operación actual universal. No representa catálogo comercial, certificación, homologación, garantía jurídica, producto terminado, readiness comercial ni cumplimiento normativo integral. No evalúa mercado, pricing, licencias/reutilización o viabilidad. Transit Data Lab es WORKING NAME.

## Distribución final

| Estado | Número |
| --- | ---: |
| EXISTING | 11 |
| IN_DEVELOPMENT | 2 |
| PLANNED | 4 |
| PENDING_VERIFICATION | 3 |
| TOTAL | 20 |

28 evidencias técnicas; 76 rutas únicas registradas y verificadas. Sin degradaciones adicionales durante esta revisión final; las clasificaciones conservadoras previas permanecen.

## Capacidades EXISTING

- **TDL-CAP-001**: Ingestión raw de Asturias.
- **TDL-CAP-002**: Integridad y procedencia binaria GTFS.
- **TDL-CAP-003**: Controles de integridad específicos de Asturias.
- **TDL-CAP-004**: Consultas SQL exploratorias read-only.
- **TDL-CAP-009**: Corpus normativo con trazabilidad binaria.
- **TDL-CAP-010**: Requirements engine materializado de 2017/1926.
- **TDL-CAP-011**: Revisión humana con Gate 1 y Gate 2.
- **TDL-CAP-012**: Gates de regresión del baseline Compliance.
- **TDL-CAP-016**: Censo físico de cinco datasets piloto.
- **TDL-CAP-018**: Exportación de datos GTE conservada con manifiesto.
- **TDL-CAP-019**: Comparación descriptiva NAP / GTE del piloto.

Descripciones, evidencias, dependencias y límites completos en [CAPABILITY_REGISTER.md](CAPABILITY_REGISTER.md). La matriz A–H de las 11 EXISTING, la coherencia de las 20 capacidades y la clasificación de las 28 evidencias están en [BASELINE_REVIEW_V1.md](BASELINE_REVIEW_V1.md).

## Documentos integrantes y SHA-256

Las huellas se calculan sobre los bytes de archivo, sin normalizar contenido ni saltos de línea. Orden obligatorio: CAPABILITY_REGISTER.md, EVIDENCE_INDEX.md, CAPABILITY_GAPS.md.

| Orden | Documento | SHA-256 |
| --- | --- | --- |
| 1 | [CAPABILITY_REGISTER.md](CAPABILITY_REGISTER.md) | `39506abb74cf0437802603c7915d90ba62fce29ff38f6c21277cdabc577a4c15` |
| 2 | [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) | `f8bdcf9a49f09352fe754decc1c87881091c56c23edec4cff344c9eb2c691b41` |
| 3 | [CAPABILITY_GAPS.md](CAPABILITY_GAPS.md) | `2b33a86971f8f860039a9f2a0144da14a67867ef0c26ccb801a94ce96264e01d` |

**BASELINE SHA-256:** `5e0635956f40c6fbf27d6c6b16fcac8d4762f3fc1c93793d628c7df24dea30c2`

Algoritmo determinista: para cada documento en el orden anterior, concatenar `nombre + espacio ASCII + sha256 hexadecimal minúsculo + LF`. Codificar UTF-8 sin BOM, incluyendo LF final; calcular SHA-256 sobre esa concatenación. Entrada exacta persistida en [baseline_hash_input.txt](review_v1/baseline_hash_input.txt). El descriptor V1 no se incluye en su propio hash; evita autorreferencia. BUSINESS_STATUS y DECISION_LOG son registros de gobierno, no integrantes del agregado.

## Limitaciones generales

- Sentinel Asturias: **42 PASS / 4 FAIL**, exit 0 y global **WARNING**. Capas ausentes: analysis, core, validation y validation.results. Solo controles estructurales seleccionados y conteos de esa baseline; **no es un validador GTFS completo**. No se ocultaron ni convirtieron los cuatro FAIL en éxito técnico completo.
- Ingestión de un feed Asturias conservado; importación no replayada, core/analysis/motor GTFS propios ausentes, sin universalidad o portabilidad integral acreditada.
- Compliance: replay integral no demostrado; interpretación y aprobación humanas; siete dependencias PARTIAL, anomalías Annex 1.3 B-I/D-I, fidelidad textual no certificada y rutas absolutas no portables. Fuente consolidada 2024-03-04; no se verifica vigencia jurídica.
- Mapping sin resultados consolidados: coverage/equivalences=0. Audit limitado a DDL/tablas: rules/runs/results=0. Infraestructura no acredita auditoría normativa completa ni cumplimiento.
- GIS **PENDING_VERIFICATION**: KML experimentales sin generador reproducible suficiente.
- Piloto histórico de cinco datasets; veinte entradas de investigación no son clientes comerciales. GTFS Explorer vigente atribuible a build permanece **PENDING_VERIFICATION**. Comparación NAP/GTE sin equivalencia de reglas ni superioridad. Hallazgos enum históricos Bizkaibus invalidados; no se presentan como errores reales actuales.
- Export Kbus histórico con manifiesto; routes contiene AH/H/L2 mientras la selección incluye L3. No acredita completitud, round-trip, pipeline vigente ni exportación de findings.
- Git padre sin commits y artefactos ignorados: congelación documental por hash; no es release portable/versionada del conjunto técnico. No hay autorización comercial de reutilización inferida.

Los 13 gaps permanecen abiertos en [CAPABILITY_GAPS.md](CAPABILITY_GAPS.md). El baseline congelado no obliga a corregirlos ni autoriza trabajo técnico.

## Respaldo de la decisión

[Revisión final](BASELINE_REVIEW_V1.md) y [final_summary.json](review_v1/final_summary.json): 221 controles satisfechos tras corregir únicamente comparación case-sensitive de cinco SHA hexadecimales. Se conserva el resultado inicial FAIL del comparador y la recomprobación binaria; esto no modifica los cuatro FAIL técnicos del sentinel. Resultados completos read-only y exit codes guardados en review_v1; diez suites Compliance revisadas desde evidencia persistida, sin rerun. Inventarios antes/después de 899 archivos técnicos idénticos.

## Inmutabilidad y criterio de modificación

V1 y sus tres documentos integrantes no se modificarán silenciosamente. Conservar esta versión y sus huellas. Una corrección o ampliación futura exige nueva revisión Business documentada con motivo, evidencia, impacto y nuevas huellas; un cambio de estados, alcance, capacidades o evidencia sustancial producirá BUSINESS_CAPABILITY_BASELINE_V2. Una revisión documental menor debe conservar V1 e identificar expresamente su nueva revisión y relación con V1.

La evolución técnica **no actualiza automáticamente la capacidad comercial**. Nuevos resultados requieren verificación Business explícita de A–H y de las afirmaciones permitidas/prohibidas. Una discrepancia futura de huellas suspende la utilización de V1 hasta aclarar procedencia mediante revisión; no se regenera el hash para ocultarla. No se inicia Phase 3 sin autorización expresa.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
