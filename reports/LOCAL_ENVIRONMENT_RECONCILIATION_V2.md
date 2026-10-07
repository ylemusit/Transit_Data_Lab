# Local Environment Reconciliation V2

Fecha: 2026-10-07. Resultado: **BLOCKED_BY_AMBIGUOUS_ITEMS**.

## Resultado comprobado

Descubrimiento amplio por nombres y metadatos desde C:\: 35 ubicaciones base y 497 unidades relevantes disjuntas (archivo o subárbol). Se usaron además las raíces del inventario anterior, verificando su existencia actual. Las coincidencias ajenas al proyecto se descartaron del inventario de TDL. No se leyó contenido HOLDOUT ni se modificaron sus rutas.

| Medida | Bytes lógicos observados |
| --- | ---: |
| Clasificados | 19,199,555,647 |
| Eliminados | 245,632,167 |
| Retenidos de esas unidades | 18,953,923,480 |
| Movidos | 0 |

Estas cifras excluyen almacenes Git, datos protegidos, repositorios independientes, enlaces/reparse points y rutas inaccesibles. No son espacio físico asignado ni una medición exhaustiva del disco. Los archivos añadidos por esta tarea tampoco forman parte del tamaño inicial. El descubrimiento por nombres tiene profundidades acotadas; no acredita ausencia de material en todo C:\.

Se eliminaron 145 directorios: 5 de trabajo/entorno de build y 140 cachés. Cada borrado tiene un manifiesto de hojas/tamaños previo y verificación de ausencia posterior. Las cachés no estaban versionadas; sus fuentes coinciden con blobs de commits alcanzables desde `main` descargado de GitHub. Los builds tienen source commit preservado y receta de dependencias publicada. Se conservaron los directorios `dist`, metadatos y evidencia de aceptación. No se quitaron checkouts enteros, datasets, informes históricos congelados ni software.

## Fuente y validación

Base remota comprobada: `cf4e0a30f6837b077e6994305f51fbf2cca8282c`. `git fsck --connectivity-only --no-dangling`: PASS. Ejecutable aceptado: SHA-256 `3030F518A68C86534B777CB7D56B973A3B11E329B4C09F6D8D2A45D11F715266`, comprobado después de limpiar. No se reconstruyó el RC ni se repitió aceptación humana/clean-machine. Tests post-cleanup: 15/15 PASS (shell y worker empaquetado con éxito, ZIP inválido, PDF/manifests y rutas Unicode); el primer intento tuvo un error en cancelación al leer vacío el fichero child.pid. La repetición específica pasó 3/3 y la repetición completa 15/15. El patrón es compatible con una carrera del test entre creación y escritura; causa inferida, no defecto de cleanup demostrado. CI remoto se verifica sobre los SHAs de publicación; el alcance es sintético, no validación comercial o jurídica.

La raíz local sigue en una rama histórica con modificaciones preexistentes. Se preservaron esas modificaciones y los archivos no rastreados; no se incorporan automáticamente a la publicación. La edición documental se prepara contra `main` usando un índice temporal, sin crear otro checkout y sin tocar el índice del usuario. El objetivo de una única raíz limpia **no está conseguido**.

## Documentación y conocimiento

Se consolidan el estado vigente y la navegación arquitectónica: `PROJECT_STRUCTURE.md` remite a `ARCHITECTURE.md`; `PROJECT_STATUS.md` remite a informes autoritativos en vez de repetir cronologías, y elimina el párrafo duplicado de aceptación. Los estados anteriores siguen recuperables en Git. Se conservan las instantáneas y evidencias congeladas.

No se encontró un repositorio de experiencias específico de TDL utilizable: las coincidencias personales/sistema y la carpeta vacía de knowledge de otra herramienta no son el destino del proyecto. Se crea `knowledge/` con cinco lecciones concisas y enlaces a fuentes Git. No se copian informes completos ni se modifican memorias de Codex. No se contabiliza como ruido eliminado material que no se ha borrado.

## Software y ubicación

Python 3.12/3.14, Git/GitHub tooling, DuckDB y QGIS permanecen: su exclusividad para TDL no está probada; Python 3.12.10 sigue siendo la versión de la receta de build. Ninguna instalación se clasifica SAFE_TO_REMOVE. `C:\TDL_DATA` permanece como raíz aprobada para nuevo material externo persistente. No se trasladan datasets/evidencia mientras no estén resueltas identidad, retención y dependencias.

## Revisión requerida

Cinco grupos, con miembros y metadatos en evidencia local no publicada:

1. Raíz canónica: reconciliar cambios locales con `main` conservando trabajo único.
2. Checkouts históricos: hay contenido protegido/ignorado/no rastreado; una referencia Git no permite borrar el árbol completo.
3. Ejecuciones y evidencia externa: falta procedencia completa por claim para retirar outputs grandes.
4. Datasets/exports descargados e independientes: falta prueba de duplicación y dependencia antes de mover o borrar.
5. Límites del descubrimiento: accesos denegados/profundidad acotada; no hay prueba exhaustiva de ausencia.

No se solicita aprobación genérica de borrado: primero hay que resolver la prueba de conservación. HOLDOUT queda retenido fuera de la limpieza. El detalle operacional permanece local en `reports/evidence/local_environment_reconciliation_v2/` (inventario, plan, ejecución, reviews, validación y resumen); no se publica información específica de máquina.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
