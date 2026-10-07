# Local Environment Reconciliation V2

Fecha: 2026-10-07. Resultado final local: **CLOSED_WITH_PROTECTED_RESIDUALS**.

## Resolución comprobada

Se reutilizó el inventario V2 de 484 unidades y se resolvieron familias, sin repetir el descubrimiento global. La raíz canónica se reconcilió contra `origin/main` posterior a PR #55 (`04cb988944c6979e483835cb19ece7b76aa67401`). Las versiones iniciales locales de G08/G11, estados antiguos y diferencias de presentación quedaron sustituidas por sus versiones publicadas. La regla útil de actualizar conjuntamente los dos documentos de estado se conserva en `AGENTS.md`. Los inventarios privados y diseños manuales se trasladaron fuera del repositorio con verificación SHA-256. No quedan modificaciones locales sin explicación.

| Resultado | Valor |
| --- | ---: |
| Bytes lógicos retirados en esta resolución | 13.113.888.114 |
| Copias únicas conservadas antes de retirar sus ubicaciones anteriores | 81.321.963 bytes |
| Material eliminado en esta pasada, descontando esas copias | **13.032.566.151 bytes** |
| Total V2, incluida la primera pasada | **13.278.198.318 bytes** |
| Worktrees históricos / copias independientes retirados | 58 / 7 |
| Otras unidades de temporales/outputs/builds resueltas | 383 |
| Copias ZIP DEVELOPMENT / extracciones idénticas eliminadas | 20 / 14 |
| Archivos de outputs/cachés reproducibles retirados | 18.019 |
| Raíces adicionales de build obsoleto retiradas | 6 |
| Runtime exclusivo TDL retirado | 1 entorno virtual obsoleto |
| Nuevas lecciones / grupos de decisión humana pendientes | 0 / 0 |

Son longitudes lógicas de archivos, con manifiesto previo y comprobación posterior; no son espacio físico asignado ni una diferencia exhaustiva antes/después del disco. La cuenta descuenta las copias conservadas y no atribuye recuperación adicional a movimientos dentro del mismo volumen. Los nuevos manifests y cambios del checkout tampoco constituyen bytes eliminados. Los 6.395.371.423 bytes de R1 no se vuelven a contar.

Los commits laterales de Product Readiness están representados por las PR #53/#54 mediante squash. Los candidatos M04-B2 de triage/transición/aprobación están sustituidos por el evaluator, parser, tests, manifiestos de aprobación e informes publicados; no se reintrodujeron implementaciones antiguas. Cada retirada verificó cobertura Git y separó cambios locales, evidencia original, schemas y salidas generadas. Los originales seleccionados se verificaron por SHA-256 en su destino antes del borrado. Las recetas históricas conservadas requieren reconstruir su contexto por Git; no se presentan como herramientas vigentes.

## Estructura y residuos protegidos

La raíz Git canónica sigue siendo `Transit Data Lab`; `C:\TDL_DATA` es la única raíz externa general para datos, evidencia, material privado y la copia operacional aceptada. Los 14 ZIP DEVELOPMENT coinciden con el inventario aprobado y viven allí; junctions conservan las rutas contractuales originales. Las extracciones eliminadas se compararon con los miembros del ZIP. El snapshot XSD NeTEx y su licencia conservan la estructura de imports; una junction mantiene el default del runtime sin cambiar código ni manifiesto fijado.

Se conservan estos grupos justificados:

1. **Datos/evidencia contractual:** Test Bank en su ruta corta vigente, fuentes físicas HOLDOUT y evidencia de aceptación/congelación. Tres worktrees identificados como HOLDOUT, un cuarto con checkpoint local congelado y una raíz de ejecución HOLDOUT conservan sus ubicaciones. No reciben trabajo nuevo.
2. **Prerrequisitos y capturas canónicas:** bases locales, fuentes normativas capturadas y evidencia congelada que no puede sustituirse con seguridad por un output sintético. Permanecen ignorados por Git; los datos externos nuevos siguen la política de `C:\TDL_DATA`.
3. **Material privado/manual:** sistema visual, código, plantillas y referencia TUVISA conservados privadamente por decisión expresa de Yeison; diseños e informes manuales originales, capturas NeTEx y diagnósticos compactos. No se publicaron ni se infieren derechos de distribución.
4. **Configuración necesaria:** ajustes privados del editor y junctions verificadas. Aplicaciones compartidas y productos/repositorios independientes quedan fuera del cleanup TDL; no se desinstalaron Python, Git, QGIS ni DuckDB compartidos.

Ningún checkout se conserva únicamente por representar un hito. Los límites de descubrimiento por nombres se registran como límites de cobertura, sin convertirlos en decisiones pendientes ni afirmar ausencia de material en todo el disco. Rutas completas e inventarios de máquina permanecen externos y sin publicar.

## Validación y límites

- Git: `fsck --connectivity-only --no-dangling` PASS; raíz preparada desde `origin/main`; ningún worktree registrado apunta a una ruta eliminada.
- Tests focalizados: **34/34 PASS** para cliente, worker empaquetado, informes, G08 y remediación; **10/10 PASS** para intake, audit y schema NeTEx, incluidos imports e identidad fijada.
- Fuentes DEVELOPMENT y aliases: **14/14 SHA-256 PASS**. Copias únicas retenidas: SHA-256 PASS. Test Bank y schemas siguen accesibles; las rutas históricas de outputs retirados quedan explicadas en el manifiesto de resolución.
- Ejecutable aceptado: SHA-256 **3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266**, comprobado tras el traslado; una sola copia operacional onedir, con dependencias incluidas. Rol: **INTERNAL_OPERATIONAL_TOOL**.
- Fuentes físicas HOLDOUT: metadatos/rutas presentes; no se abrieron, inspeccionaron ni hashearon sus contenidos y quedaron fuera de todos los targets de escritura. Se retiraron copias de informes versionados en checkouts redundantes; no se modificó su evidencia canónica ni las fuentes físicas protegidas.

La publicación GitHub se verifica sobre los SHAs efectivos de PR y merge, con evidencia operacional local. No se reconstruyó el ejecutable ni se repitió aceptación humana o clean-machine; no cambia readiness interno, cobertura del motor, gates comerciales ni afirmaciones jurídicas.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
