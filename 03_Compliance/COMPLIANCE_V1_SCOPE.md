# COMPLIANCE_V1_SCOPE

Decisión vigente: misión explícita de Yeison del 2026-09-28. Alcance engine/lab.

| Estándar | Disposición | Alcance demostrado |
|---|---|---|
| GTFS Schedule | PRIMARY / OPERATIONAL_COMPLIANCE_TRACK | Referencias de registros fixed-stop de stop_times a trips y stops; ubicación referenciada de tipo 0 o vacío. |
| NeTEx | PRIMARY / OPERATIONAL_COMPLIANCE_TRACK | Fragmento Line de EPIP: validación XSD y observación de identidad/Name. |
| SIRI | STANDBY / OUT_OF_SCOPE_V1 | DEFERRED_BY_PRODUCT_SCOPE. |
| GTFS-RT | STANDBY / OUT_OF_SCOPE_V1 | DEFERRED_BY_PRODUCT_SCOPE. |
| DATEX II, red espacial y otros | OUT_OF_SCOPE_V1 operativo | Conocimiento, mappings y decisiones históricos conservados. |

Reapertura realtime: GTFS + NeTEx V1 estables **y** apertura explícita de un track futuro.

## Identidad y límites técnicos

GTFS: referencia oficial capturada en `reports/evidence/compliance_v1_20260928/sources/gtfs_reference.md`; versión operacional identificada por SHA-256 en `source_manifest.json`. El registro histórico M03 no se reescribe ni se presupone idéntico a la captura. IDs tratados como texto; no se normalizan ni convierten a números. Flex queda NOT_EVALUABLE. La regla no valida horarios, calendarios, tarifas ni el feed completo.

NeTEx: artefacto técnico público Data4PT EPIP de 2021, basado en NeTEx XSD 1.3.1; commit `e5eaf83f15f7fd8db7991a4a8323b6ff7905c13a` del repositorio oficial TransmodelEcosystem/NeTEx-Profile-EPIP. Se fija `NeTEx_publication_EPIP.xsd` y sus dos dependencias, con hashes. El repositorio declara que ya no se mantiene. No se usa la variante NoConstraint.

La identidad operacional del XSD queda en scope, source reference, representability y contrato de regla. La capacidad legacy conserva su registro `CEN/TS 16614-4:2017`: es el contexto histórico de la relación semántica, **no** la versión del artefacto validado. No se declara equivalencia normativa entre ambos ni aplicabilidad como perfil mínimo español. Se demuestra un fragmento global Line; no una PublicationDelivery completa, referencias entre frames ni conformidad íntegra EPIP.

Ambos scopes son descomposiciones técnicas de las relaciones M04 ya aceptadas para `EU-2017-1926-REQ-A04-P01-001`. Las nuevas revisiones se atribuyen a Codex bajo la misión; no simulan una nueva revisión jurídica humana.

## Contratos

- Representability: `PARTIAL` para la capacidad amplia; AVAILABLE exclusivamente dentro de `V1-SCOPE-GTFS` o `V1-SCOPE-NETEX`, con versión, constraints, fuente y límites serializados en columnas existentes.
- Observación: `phase3-observation-envelope/1`, con dataset/hash, evaluador/hash, scope, locator, alcance y estado. `COMPLETED`, `NOT_INSPECTED`, `FAILED` separados de `PRESENT`, `ABSENCE_CONFIRMED`, `INDETERMINATE`.
- Regla: `PASS`, `FAIL_TECHNICAL`, `NOT_EVALUABLE`, `INSPECTION_ERROR`; siempre `legal_conclusion_allowed=false`.
- Evidencia V1: fixtures sintéticos identificados como tales. Cero operadores evaluados.

## Relación GTFS ↔ NeTEx

Solapamiento semántico: estructuras de la oferta programada y red de transporte del mapping M04 aceptado. Los pilotos no evalúan la misma propiedad: GTFS comprueba referencias de llamadas a paradas; NeTEx comprueba una Line nombrada. No existe equivalencia 1:1 ni conversor. Line admite identificación/versionado, operadores, modos y estructuras adicionales; esos detalles no se transforman en este piloto. La correspondencia entre rutas, líneas, viajes y paradas, y sus pérdidas de información, queda fuera de V1; trasladar solo el resultado PASS perdería el scope y sería incorrecto.

## Criterio de cierre

Phase 1/2 congeladas e íntegras; persistencia aditiva exacta; GTFS y NeTEx reproducibles en estos scopes; controles de falsos positivos; 48 requisitos y nueve familias dispuestos; coverage conciliada; gate vigente PASS. No exige todos los estándares, todos los requisitos, UI ni conclusiones jurídicas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
