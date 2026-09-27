# Política permanente de recursos Business

FULL REPOSITORY HASHING IS PROHIBITED BY DEFAULT.

Un hash de contenido de todo el repositorio o de un árbol grande requiere autorización humana explícita. No ejecutar por defecto `evidence/verify_market.py`: contiene la comprobación histórica de 275.363 archivos, fuera del alcance actual.

Controles predeterminados: lecturas de archivos concretos, `git status`, `git diff --name-only`, manifiestos y hashes ya persistidos; nuevos hashes solo de archivos realmente modificados en la ejecución. No recorrer datasets, entornos, caches, bases de datos, backups, repositorios anidados ni binarios generados.

Antes de una operación que enumere más de 20.000 archivos, lea más de 5 GB, dure más de aproximadamente cinco minutos o calcule hashes recursivos fuera del alcance exacto: STOP. Registrar `RESOURCE_GUARD_TRIGGERED = YES`, explicar la operación y solicitar autorización humana. No fraccionar la operación para eludir los límites.

Esta revisión no repite la verificación previa de alcance. Git agrupa directorios untracked en este repositorio sin commits: diff vacío no demuestra inmutabilidad global. Se documentan las rutas de escritura explícitas dentro de Business y los controles estructurales de documentos concretos. Los hashes de V1/manifiestos ya persistidos son evidencia histórica, no una nueva certificación global. No se inspeccionan fuentes técnicas ni se ejecutan sus herramientas.

No se ha medido el total de archivos enumerados o bytes leídos durante toda la sesión, incluidas herramientas, Git y lecturas. Los conteos acotados del verificador se identifican por separado y no equivalen a totales de sesión. Resultado completo, duración de verificación y exit code en `readiness_review/`.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
