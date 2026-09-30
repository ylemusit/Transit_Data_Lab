# SERVICE_AUDIT_ALIGNMENT_MATRIX

**Proyecto:** Transit Data Lab  
**Fecha base:** 2026-09-28  
**Propósito:** Traducir el estado técnico actual del proyecto en capacidades de servicio verificables, sin duplicar trabajo, reabrir baselines congeladas ni presentar como comerciales capacidades aún no demostradas.

---

## 1. Principio rector

Transit Data Lab no se presenta como organismo certificador ni como validador genérico de “cumplimiento total”.

Su objetivo es ofrecer **Transport Data Assurance**:

- verificación técnica reproducible;
- evaluación de calidad de datos;
- revisión geoespacial;
- trazabilidad de requisitos aplicables;
- gestión de evidencias;
- corrección controlada;
- comparación entre versiones;
- preparación para mantenimiento recurrente;
- interoperabilidad progresiva GTFS ↔ NeTEx.

Cada entrega debe declarar explícitamente:

1. qué se evaluó;
2. contra qué versión, estándar, requisito o criterio;
3. qué quedó fuera de alcance;
4. qué no pudo evaluarse;
5. qué requiere revisión humana;
6. qué hallazgos son técnicos, de calidad, regulatorios o de interoperabilidad;
7. qué versión de dataset, motor y reglas produjo el resultado.

---

## 2. Niveles de autoridad

| Nivel | Tipo | Uso |
|---|---|---|
| L1 | Obligación legal o regulatoria aplicable | Evidencia de alineación normativa; puede requerir revisión humana/jurídica |
| L2 | Requisito del estándar | Conformidad técnica GTFS / NeTEx |
| L3 | Perfil, requisito NAP o condición contractual | Reglas específicas del contexto de publicación |
| L4 | Recomendación Transit Data Lab | Mejora de calidad, mantenibilidad, operación o interoperabilidad |

Una recomendación TDL nunca debe presentarse como obligación normativa.

---

## 3. Estados de resultado normalizados

### Resultado técnico
- `PASS`
- `FAIL_TECHNICAL`
- `WARNING`
- `NOT_EVALUABLE`
- `INSPECTION_ERROR`

### Estado de revisión del hallazgo
- `DETECTED`
- `REPRODUCED`
- `EVIDENCE_ATTACHED`
- `REVIEWED`
- `CONFIRMED`
- `REPORTED`
- `FALSE_POSITIVE`
- `TOOL_DEFECT`
- `DATA_AMBIGUITY`
- `REQUIRES_CONTEXT`

### Severidad
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `INFO`

La severidad y el estado de conformidad son dimensiones distintas.

---

# 4. Matriz de alineación del servicio

| ID | Capacidad de servicio | Necesidad del cliente | Activo existente | Evidencia actual | Limitación actual | Riesgo de falso positivo | Revisión humana | Trabajo pendiente | Criterio de aceptación | ¿Comercial? |
|---|---|---|---|---|---|---|---|---|---|---|
| SA-001 | Preservación del dataset original | Garantizar trazabilidad e integridad de la entrada | Política de gobernanza, hashes e identidad por ejecución | GTFS_Lab registra identidad, hash y contexto; bases y originales protegidos | No existe aún contrato único de auditoría de extremo a extremo | Bajo | No, salvo incidencias de procedencia | Unificar manifiesto de auditoría y política de originales/copia de trabajo | Toda auditoría produce hash, origen, fecha, versión y copia inmutable | **Casi** |
| SA-002 | Ingestión GTFS reproducible | Procesar un feed sin modificar el original | Pipeline ZIP → inventario/hash → DuckDB aislada | Gate y E2E sintético PASS; dry run Asturias completado | Catálogo de tablas acotado; no cubre todo GTFS Schedule | Bajo/Medio | No | Fijar contrato GTFS objetivo y matriz soportada/no soportada | Un feed dentro del scope se ingiere de forma repetible y trazable | **Sí, dentro de scope** |
| SA-003 | Conformidad estructural GTFS | Detectar errores de estructura, claves y referencias | Reglas locales + Compliance GTFS V1 | Regla técnica reproducible sobre referencias `stop_times` y fixtures sintéticos | Cobertura muy limitada; no valida todo el estándar | Medio | No para reglas deterministas | Ampliar familias de reglas con fixtures y gates propios | Cada regla tiene ID, versión, fundamento, fixtures y evidencia | **No todavía como auditoría amplia** |
| SA-004 | Escalabilidad GTFS | Auditar feeds reales grandes | DuckDB por ejecución + pipeline actual | Asturias supera 10.000 `trips`; el laboratorio procesa, Compliance V1 no completa esa inspección | Límite fijo 10.000 filas / 1 MiB en evaluador Compliance V1 | Alto si se interpreta `INSPECTION_ERROR` como hallazgo | No | Nuevo contrato V2 o inspección segmentada con completitud demostrada | Feed grande evaluado sin pérdida semántica y con gate específico | **No** |
| SA-005 | Calidad de datos GTFS | Detectar datos válidos pero deficientes | Análisis local, calendario, GIS, resultados históricos | GTFS_Lab genera análisis e informes; GIS GeoJSON/KML reproducible | Catálogo de checks de calidad aún no cerrado | Medio/Alto | Sí para checks heurísticos | Definir reglas de calidad separadas de requisitos del estándar | Cada check indica fundamento, umbral y riesgo de falso positivo | **Piloto** |
| SA-006 | Auditoría geográfica | Detectar paradas desplazadas, discontinuidades y anomalías espaciales | Exportación GeoJSON/KML; QGIS disponible como entorno externo | GIS ya generado por run | QGIS no está integrado ni se han fijado CRS, unidades, umbrales ni workflow | Alto para conclusiones automáticas | Sí | Crear proyecto/modelo QGIS reproducible vinculado a finding IDs | Un hallazgo espacial puede reproducirse desde datos originales y parámetros fijados | **Piloto** |
| SA-007 | Trazabilidad normativa | Relacionar requisitos con evidencia técnica | Compliance V1: provisions, source facts, requirements, mappings, coverage | 92 provisions, 36 source facts, 48 requirements, 15 mappings; 2 reglas técnicas | 0 requisitos completos; 6 parciales; 12 revisión humana; 20 diferidos; 10 fuera de scope | Medio/Alto | Sí | Extender por contratos nuevos sin reinterpretar V1 | Requirement → applicability → rule/evidence → disposition trazable | **No como “cumplimiento total”** |
| SA-008 | Informe ejecutivo de auditoría | Dar a dirección una visión accionable | Reporting actual de GTFS_Lab | Pipeline genera informe | Aún no existe paquete comercial estandarizado de auditoría | Bajo | Sí, revisión editorial | Diseñar executive report + resumen de alcance + limitaciones + acciones | Informe comprensible, reproducible y vinculado a evidencia técnica | **Piloto** |
| SA-009 | Anexo técnico | Permitir a IT/proveedor corregir problemas | Findings y resultados existentes | Regla/resultados ya contienen status, severity, versión, scope y referencias | Taxonomía no unificada entre componentes | Medio | Sí para confirmar findings ambiguos | Normalizar `RuleResult` y ciclo de vida del hallazgo | Cada finding se localiza en original y puede reproducirse | **Piloto** |
| SA-010 | Control de falsos positivos | Evitar conclusiones erróneas como las históricas de Bizkaibus | Evidencia histórica + fixtures + gates | Existe antecedente de hallazgos invalidados por defecto del producto | No hay aún lifecycle formal del hallazgo ni golden corpus transversal | Alto | Sí | Golden cases, holdout feeds, clasificación `TOOL_DEFECT/FALSE_POSITIVE` | Ningún finding comercial se reporta sin reproducción y evidencia | **Obligatorio antes de vender** |
| SA-011 | Corpus real NAP | Probar robustez contra implementaciones reales | `20_clientes_reales`, manifiesto de 20 datasets, 4 familias | Corpus organizado y con snapshots/metadatos parciales | Procedencia incompleta en algunos casos; un feed real no demuestra generalización | Medio | Sí para licencia/procedencia | Completar metadatos sin reescribir historia; dividir dev/holdout | Corpus con hashes, procedencia, formato, licencia y rol dev/holdout | **Interno** |
| SA-012 | Generalización a operadores desconocidos | Evitar reglas adaptadas a casos concretos | Corpus real + futuros holdouts | No demostrada aún | Riesgo de sobreajuste al corpus conocido | Alto | Sí | Reservar feeds holdout y prohibir ajustes específicos previos | Dataset no visto genera resultados reproducibles sin cambio específico de código | **Gate comercial clave** |
| SA-013 | Corrección sobre copia de trabajo | Ayudar al operador a resolver findings | Gobernanza de originales/copia de trabajo prevista | Principio documentado | Flujo operativo completo todavía no demostrado | Medio | Sí | Definir remediation workspace y trazabilidad de cambios | Original intacto; cada corrección tiene causa, autor, fecha y diff | **Piloto** |
| SA-014 | Diff entre versiones | Distinguir cambios del dataset | Arquitectura y hashes existentes; no hay motor completo de diff demostrado | Capacidad conceptual y elementos de identidad disponibles | No existe aún contrato de diff por entidad/semántica | Medio | Sí para cambios ambiguos | Construir Diff Engine por archivo, entidad y semántica | Dataset A/B produce altas, bajas, cambios y entidades afectadas reproducibles | **No todavía** |
| SA-015 | Regresión tras corrección | Confirmar que una mejora no introduce nuevos problemas | Gates actuales + futuro diff | Gates aislados existentes | No hay ciclo formal intake → fix → regression → release | Medio | Sí | Workflow de segunda entrega y regression audit | Misma versión de motor/ruleset permite atribuir mejora al dataset | **No todavía** |
| SA-016 | Release Candidate previo a NAP | Entregar un paquete listo para aprobación humana | Pipeline + reporting + gobernanza | No demostrado extremo a extremo | Sin workflow comercial de aceptación | Bajo/Medio | **Sí obligatoria** | Crear release manifest y human approval gate | Ninguna publicación se considera lista sin aprobación humana registrada | **No todavía** |
| SA-017 | Mantenimiento recurrente GTFS | Reducir errores en futuras actualizaciones | Identidad, hashes, reglas, futuro diff/regression | Base técnica parcial | Aún no hay segunda entrega real controlada | Medio | Sí | Demostrar un ciclo completo de actualización | v1 → corrección → v2 → diff → regression → release reproducible | **Después de SA-014/015** |
| SA-018 | NeTEx readiness | Saber qué información GTFS existe y qué falta para NeTEx | Fragmento `Line` + mappings parciales | 10 casos sintéticos; XSD EPIP fijado | No hay perfil español/aplicable elegido ni PublicationDelivery completa | Alto | Sí | Elegir perfil/versionado/caso de uso y registrar concepts/gaps | Informe de conceptos `AVAILABLE / PARTIAL / MISSING / AMBIGUOUS` | **No** |
| SA-019 | Ingestión y auditoría NeTEx | Validar un paquete NeTEx real | Prueba técnica de fragmento `Line` | Alcance técnico reproducible muy acotado | No existe `NeTEx_Lab` | Alto | Sí inicialmente | Pipeline XML seguro → XSD → referencias → findings → report | E2E con paquete representativo + gates | **No** |
| SA-020 | Interoperabilidad GTFS ↔ NeTEx | Migrar preservando información y declarando pérdidas | Mappings parciales en Compliance | Relaciones semánticas parciales | No existe crosswalk operativo ni conversión demostrada | Alto | Sí | Concept Registry incremental y mappings `EXACT/PARTIAL/LOSSY/...` | Conversión solo donde el caso de uso y pérdida estén demostrados | **No** |
| SA-021 | Solicitud de información faltante | Evitar inventar datos no presentes | Principio de no inferencia + futura readiness | No formalizado como contrato operativo | Riesgo de derivar información no soportada | Alto | Sí | Estado `REQUIRES_OPERATOR_INPUT` y formulario de carencias | Ningún dato ausente se fabrica silenciosamente | **Sí como principio** |
| SA-022 | Comparación cambios de datos vs motor | Saber si bajan findings por mejora real o por cambio de evaluador | Versionado disponible parcialmente | Versiones y contexto ya se registran en varios componentes | No hay diff de evaluador/ruleset formal | Medio | Sí | Guardar dataset version + engine version + ruleset version en cada run | Toda comparación declara qué variable cambió | **Obligatorio** |
| SA-023 | Paquete de evidencias | Entregar un trabajo defendible y portable | Informes, hashes, GeoJSON/KML y outputs actuales | Outputs reproducibles parciales | No existe estructura comercial estándar | Bajo | Sí | Estandarizar Evidence Pack | Un tercero puede revisar findings sin depender de la memoria del analista | **Piloto** |
| SA-024 | Auditoría de la propia herramienta | Poder defender que el motor no introduce el error | Gates, fixtures, py_compile, evidencia histórica | Ya existen gates y regresiones parciales | No hay assurance transversal del evaluador | Alto | Sí | Golden tests + metamorphic/negative tests + holdouts + integrity checks | Release del motor solo si pasa suite de confianza | **Obligatorio** |

---

# 5. Orden de implementación recomendado

## Programa 1 — TDL Trust Foundation

**Objetivo:** garantizar que la herramienta sea auditable antes de ampliar su oferta.

Cerrar primero:

- SA-001 Preservación;
- SA-009 Anexo técnico;
- SA-010 Control de falsos positivos;
- SA-011 Corpus;
- SA-012 Generalización;
- SA-022 Cambios dataset vs motor;
- SA-024 Auditoría del propio evaluador.

### Entregables

- `AUDIT_MANIFEST_SCHEMA`
- contrato normalizado de `RuleResult`
- lifecycle de finding
- golden cases
- feeds holdout
- versionado obligatorio de engine/ruleset/dataset
- regla de no adaptación silenciosa por operador

### Gate

`TDL_TRUST_FOUNDATION = PASS`

---

## Programa 2 — GTFS Audit Engine V1

Cerrar:

- SA-002 Ingestión;
- SA-003 Conformidad;
- SA-004 Escala;
- SA-005 Calidad;
- SA-006 Geografía;
- SA-008 Informe ejecutivo;
- SA-023 Evidence Pack.

### Gate

`GTFS_AUDIT_V1 = PASS`

Este es el primer punto donde puede existir un **servicio de auditoría GTFS con alcance explícito**.

---

## Programa 3 — Remediation & Maintenance

Cerrar:

- SA-013 Corrección controlada;
- SA-014 Diff;
- SA-015 Regresión;
- SA-016 Release Candidate;
- SA-017 Mantenimiento recurrente.

### Gate

`GTFS_MAINTENANCE_V1 = PASS`

Este es el primer punto donde aparece el **servicio recurrente**.

---

## Programa 4 — Regulatory Assurance

Cerrar:

- SA-007 Trazabilidad normativa.

Construir la cadena:

`source → provision → requirement → applicability → technical evidence → human evidence → disposition`

### Gate

`REGULATORY_ASSURANCE_V1 = PASS`

Nunca implica certificación oficial.

---

## Programa 5 — NeTEx Readiness

Cerrar:

- SA-018 Readiness;
- SA-021 Información faltante.

### Gate

`NETEX_READINESS_V1 = PASS`

Primer producto NeTEx potencial: **readiness assessment**, no conversión completa.

---

## Programa 6 — NeTEx Audit Engine

Cerrar:

- SA-019.

### Gate

`NETEX_AUDIT_V1 = PASS`

---

## Programa 7 — Interoperability

Cerrar:

- SA-020.

Empezar con `Concept Registry`, no con un modelo canónico global.

### Gate

`GTFS_NETEX_INTEROP_V1 = PASS`

---

# 6. Primer paquete de auditoría objetivo

La primera auditoría piloto profesional debe producir:

```text
TDL_AUDIT_<id>/
├── audit_manifest.yaml
├── executive_report.pdf
├── technical_report.pdf
├── findings/
│   ├── findings.csv
│   └── findings.json
├── evidence/
│   ├── technical/
│   ├── regulatory/
│   └── geographic/
├── gis/
│   ├── findings.geojson
│   └── qgis_project/
├── hashes/
├── diffs/
└── release/
```

---

# 7. Prueba de aceptación del primer servicio

Transit Data Lab podrá considerar **GTFS Audit V1 comercialmente defendible** cuando:

1. se procese un dataset real reservado que no haya sido utilizado para adaptar reglas;
2. no sea necesario modificar código específicamente para ese operador;
3. el original quede preservado;
4. el `audit_manifest` identifique dataset, motor, ruleset y baseline;
5. cada finding pueda localizarse y reproducirse;
6. los findings ambiguos requieran revisión;
7. QGIS aporte evidencia visual sin ser el único fundamento;
8. el informe ejecutivo y el anexo técnico coincidan con los resultados machine-readable;
9. los falsos positivos detectados queden identificados como fallo de herramienta y no del operador;
10. una segunda versión corregida pueda compararse con la primera;
11. el sistema distinga cambio del dataset, cambio del motor y cambio del ruleset;
12. la auditoría de regresión confirme las correcciones;
13. se genere un Release Candidate para aprobación humana;
14. toda limitación y `NOT_EVALUABLE` quede declarada.

---

# 8. North Star técnico

> Un dataset de un operador que Transit Data Lab nunca haya visto debe poder entrar en el sistema y producir una auditoría reproducible, trazable y defendible sin modificar el código específicamente para ese operador.

## North Star de mantenimiento

> Una nueva versión del mismo dataset debe permitir distinguir qué cambió en los datos, qué cambió en las reglas o en el motor, qué hallazgos se resolvieron y cuáles aparecieron.

## North Star empresarial

> Transit Data Lab debe convertirse en un paso natural antes de que un operador publique o actualice sus datos en el NAP, aportando auditoría, mejora, evidencia y mantenimiento sin crear dependencia artificial del proveedor.

---

# 9. Siguiente ejecución recomendada

No abrir todavía nuevas capacidades NeTEx.

El siguiente bloque ejecutable es:

1. formalizar `AUDIT_MANIFEST`;
2. normalizar `RuleResult`;
3. definir lifecycle de findings;
4. clasificar el corpus real en `development` y `holdout`;
5. crear golden cases;
6. cerrar matriz GTFS de reglas soportadas;
7. resolver el límite de escala;
8. ejecutar una auditoría piloto completa;
9. revisar en QGIS;
10. corregir sobre copia;
11. ejecutar segunda entrega;
12. generar diff y regression;
13. ensamblar Evidence Pack.

Ese ciclo será la primera demostración integral del producto.
