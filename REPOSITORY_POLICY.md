# Política del repositorio Transit Data Lab

Fecha: 2026-09-27. La raíz es ROOT_REPOSITORY de gobierno, fuentes, documentación, scripts y evidencia seleccionada. No constituye por sí sola un backup completo de los datos ni un release portable.

## Repositorios independientes

No absorber árboles de trabajo ni historias anidadas; no crear gitlinks/submódulos, modificar sus configuraciones ni publicar sin autorización. Inspeccionar solo sus marcadores y referencias Git, sin recorrer sus árboles.

- `06_Products/GTFS Explorer/GTFS Explorer Artifacts`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Backups/restore_test_v0.2.2_20260924T161533Z_02`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Desktop`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.
- `06_Products/GTFS Explorer/GTFS Explorer Engineering`: NESTED_INDEPENDENT_REPOSITORY, excluido del índice raíz.

## Datos, bases y archivos grandes

DuckDB, WAL, backups de bases, feeds raw/original/extracted, entornos, cachés y builds quedan fuera de Git. Los manifests y reportes pequeños siguen versionables. Las exclusiones específicas de evidencia grande conservan los originales en disco: inventario scope_before.json, JSON/ZIP Bizkaibus y HTML de validación de 103.218.958 bytes. Su backup separado es obligatorio para recuperar la evidencia histórica.

Revisar por metadatos los archivos >10 MB, >50 MB y >100 MB antes de staging. Ningún generado sospechoso se añade automáticamente. El PDF jurídico Regulation_EU_2024_1679_ES.pdf (31.861.319 bytes) es una excepción documental ya aprobada entre los 12 PDF del corpus. No recalcular todos los hashes de PDF. No ignorar globalmente PDF, JSON, CSV, SQL o reports.

## Evidencia y baselines

Conservar éxitos, fallos, intentos corregidos, promoción fallida/resumida, decisiones, manifests y fuentes. No mover, borrar, regenerar o retocar evidencia congelada por estética. Los informes previos describen su momento histórico y no sustituyen registros de estado posteriores. PROJECT_CURRENT_STATE.md y project_baseline.json se preservan byte a byte. PROJECT_SNAPSHOT_V0.1.md conserva el intento inicialmente bloqueado; PROJECT_STATUS.md y README.md documentan el estado vigente sin modificar esas huellas.

- GTFS raw: `f4186d603c455021b807261bdac8770f5f5f4d2bed7830214eb98c223efd99fc`.
- Compliance Phase 1 histórico: `52ca421c349d4be85764e84ae1cd08750bbfee99bbc8424a8379ae60a4b0fec5`.
- Compliance Phase 2 actual: `823999a9c63e4ebe68746d52b7ba1a0048efec74a7347a4bee05f66fe03453e3`.
- Business V1 agregado: `5e0635956f40c6fbf27d6c6b16fcac8d4762f3fc1c93793d628c7df24dea30c2`.


## Saltos de línea y preservación de bytes

La política raíz `.gitattributes` controla los saltos de línea sin modificar configuración Git global, de sistema ni local. El código y la documentación ordinarios usan normalización de texto y LF en Git/checkout (`text eol=lf`; detección `text=auto` para formatos no declarados). No se exige igualdad de bytes CRLF a todos los textos.

Fuentes capturadas y evidencia histórica usan `-text -eol` por rutas: HTML/XML oficiales, evidencia de mercado, informes/ejecuciones conservados, snapshots NAP, manifests de fuentes elegibles y KML existentes. Se preservan explícitamente PROJECT_CURRENT_STATE.md, project_baseline.json y los tres documentos integrantes del baseline Business V1 con huellas registradas. Los scripts conservados dentro de evidencia de ejecución también mantienen sus bytes. Los PDF, imágenes y archivos comprimidos usan `-text -eol -diff -merge`. Filtros de contenido, ident y recodificación están desactivados mediante atributos; los datos ignorados siguen fuera de Git.

Ver alcance, excepciones y prueba aislada completa en `reports/repository_integrity/GIT_LINE_ENDING_POLICY.md`. La política resuelve la conversión Git de la evidencia; no constituye aprobación del commit ni certificación nueva de hashes jurídicos. No ejecutar renormalización, staging ni reescritura de evidencia congelada como consecuencia automática de estas reglas.

## Commit y recursos

Usar una lista de rutas auditada; nunca git add . ni force-add. Revisar secretos, baseline, tamaños y exclusiones antes de staging y después el índice. Una credencial probable bloquea staging y commit; no imprimir valores ni probar tokens contra servicios. La eliminación/exclusión de credenciales en fuentes históricas requiere una resolución trazable y una nueva revisión. El commit y la etiqueta locales no autorizan remote, push ni fases posteriores.

FULL REPOSITORY CONTENT HASHING IS PROHIBITED BY DEFAULT.

No leer >5 GB, hashear árboles completos ni enumerar datasets masivos, entornos, backups o repos anidados. Usar metadatos acotados, manifests, evidencia persistida y hashes dirigidos pequeños. Evitar git status --ignored sin acotar: en este workspace recorrió backups ignorados y produjo avisos de rutas largas. Usar --ignored=matching con pathspecs seguros y git check-ignore de rutas concretas.


Yeison Arbey Carrillo Lemus. Todos los derechos reservados.


## Compatibilidad de Git en Windows

Este repositorio requiere `core.longpaths=true` en Windows porque las rutas de archivos candidatos a versionarse pueden superar los límites de longitud heredados. Configurar únicamente este repositorio con `git config --local core.longpaths true`; no es necesario cambiar configuración global, de sistema ni políticas de Windows. El fallo y la corrección se demostraron con índices temporales y las nueve rutas largas conocidas; véase `reports/repository_integrity/GIT_LONG_PATH_DIAGNOSIS.md`.
