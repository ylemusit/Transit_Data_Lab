# NeTEx N02 — corpus, autoridad y límites

**Corte:** 2026-10-02
**N01:** `APPROVED / CLOSED_WITH_LIMITATIONS` según el mandato de ejecución de esta misión.
**Gate N02:** `COMPLETE_FOR_V1_SCOPE_WITH_DOCUMENTED_UNRESOLVED_SOURCES`.

## Base fijada

- Mercado: España; modo: autobús regular programado; dominio: información estática de pasajero.
- Perfil de referencia: CEN/TS 16614-4:2026 / EPIP. Compatibilidad de modelo/schema con NeTEx v2: `PARTIAL`; texto normativo íntegro y cotejo de restricciones pendientes.
- Schema: release `v2.0.0`, upstream `TransmodelEcosystem/NeTEx`, commit `a94e5e1752bcc13aabb8a1f3d018dc08e6978f42`, raíz `xsd/NeTEx_publication.xsd`; las 458 dependencias XSD y SHA-256 por archivo se indexan en [schema_manifest.json](schemas/v2.0.0/schema_manifest.json).
- La rama upstream v2.0 distingue la raíz de publicación para validación y dice que v2.0.0 corresponde a NeTEx Partes 1, 2, 3 y 5. No contiene por ello un validador EPIP 2026 completo.

## Jerarquía y clasificaciones

La fuente machine-readable de 34 registros es [N02_SOURCE_MANIFEST_20261002.json](N02_SOURCE_MANIFEST_20261002.json); el [registro de partida](N02_SOURCE_REGISTER_INITIAL_20261002.md) conserva sus notas y antecedentes. Se añadieron N02-32 y N02-33, corrigenda EUR-Lex 2025/90135 y 2026/90193 a la modificación 2024/490. Ambas son ediciones FR; el registro EUR-Lex de 2026 indica que no afecta a EN. También se añadió N02-34: el Reglamento 2022/670, que derogó 2015/962 desde 2025-01-01. Se conserva esta remisión porque el artículo 4(1)(a) del Reglamento 2024/490 aún se refiere a 2015/962 para transporte por carretera. No inferimos la obligación NeTEx de autobús desde el apartado (b), dirigido a otros modos. Los cambios FR se conservan como procedencia normativa y no sustituyen la revisión humana de la versión española. `AUTHORITATIVE` identifica ley, adopción o metadatos primarios de norma; `IMPLEMENTATION_REFERENCE` identifica schemas, ejemplos o referencias de implementación; `SUPPORTING` identifica guías/procedimientos; `HISTORICAL` identifica evidencia previa. Ningún ejemplo se eleva a requisito.

| Nivel | Uso en el motor | Límite |
|---|---|---|
| L1 | Reglamento UE 2017/1926 consolidado y modificación 2024/490; actos españoles identificados | La aplicabilidad de categorías del Anexo 1 se conserva explícita; no produce dictamen jurídico automático. |
| L2 | CEN/TS 16614 serie y EPIP 2026 | El texto CEN íntegro es controlado/licenciado y no está en el corpus. El preview público no permite extraer un catálogo exhaustivo de requisitos. |
| L3 | Guías EPIP/NAP/NAPCORE públicas | Informativas salvo requisito identificado en una fuente normativa; no se identificó públicamente contrato técnico de aceptación NAP ni perfil español adicional. |
| L4 | Schema publicado, ejemplos y recomendaciones TDL | Un schema/referencia de implementación no crea una obligación L1–L3. Los ejemplos son ilustrativos. |

## Fuentes sin resolver y tratamiento

- Texto íntegro de CEN/TS 16614-4:2026 y mapeo requisito a requisito contra XSD: no disponible en material público revisado. No copiar extractos protegidos ni inferir reglas MUST.
- Preview público EPIP 2026 contiene referencia a NeTEx 1.1, mientras que la ficha oficial de publicación relaciona la revisión de la serie con v2. Ambigüedad conservada como `UNKNOWN`; no se declara incompatibilidad ni compatibilidad completa.
- Perfil adicional español y contrato público de aceptación NAP: no identificados en las fuentes revisadas; ausencia de identificación no equivale a inexistencia.
- Los XSD se prepararon localmente para verificación. El upstream combina un archivo de licencia GPL-3.0 con un aviso CEN/Crown Copyright. El árbol XSD completo no se incorpora a este repositorio ni se publica hasta revisar derechos de redistribución. El manifest fija commit y hashes; CI obtiene el snapshot de upstream en un checkout temporal.
- La copia temporal se usó solo para validar construcción, no contiene feeds de operador. HOLDOUT no fue accedido.

## Decisión del gate

El corpus es suficiente para desarrollar el runtime XSD y para registrar requisitos que sí tienen soporte visible, manteniendo explícitos los vacíos EPIP/NAP. `N02 = COMPLETE_FOR_V1_SCOPE_WITH_DOCUMENTED_UNRESOLVED_SOURCES`; el cierre no afirma texto normativo completo, aceptación NAP, cumplimiento jurídico ni permiso de redistribución de los schemas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
