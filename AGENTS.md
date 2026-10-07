# Trabajo en Transit Data Lab

Responder en español de España. Aplicar las instrucciones del usuario y usar el contexto mínimo suficiente para cada tarea.

## Fuentes y alcance

- Leer primero `README.md` y `PROJECT_STATUS.md`; consultar después las instrucciones y archivos del área afectada.
- Usar `PROJECT_STATUS_TREE.md` como mapa visual vigente. Cuando un paso cambie el estado del proyecto, actualizar en la misma tarea tanto ese mapa como `PROJECT_STATUS.md`, basándose en evidencia verificada y preservando los límites de cada gate. Si no cambia el estado, no modificar el mapa.
- Transit Data Lab es el proyecto global. GTFS Explorer Desktop es un producto independiente con baseline protegida 0.2.2; no renombrar el producto ni cambiar su versión para adoptar el nombre del contenedor.
- `PROJECT_CURRENT_STATE.md` y `project_baseline.json` son instantáneas congeladas. Los informes anteriores y `PROJECT_SNAPSHOT_V0.1.md` documentan su momento histórico; el estado vigente se mantiene en `PROJECT_STATUS.md`.
- No absorber repositorios de `06_Products`, crear gitlinks ni modificar sus árboles/configuraciones como parte de tareas del padre. Una tarea específica del producto requiere sus propias instrucciones.
- Preservar cambios locales existentes, fuentes capturadas, manifests, bases y evidencia congelada. Registrar correcciones mediante documentos actuales, sin reescribir resultados históricos.
- No ejecutar imports, materializaciones, promoción de baselines ni masters históricos por defecto. Elegir comprobaciones específicas compatibles con la fase y emplear DuckDB read-only para inspección.
- Evitar recorridos y hashes globales; los datasets, backups, entornos y artefactos no forman parte de una revisión documental por defecto.
- Mantener separadas Business Phase, Compliance Phase y Business Stage. Un PASS documental no aprueba un gate humano ni acredita validación comercial o jurídica.
- No hacer commit, push, publicación, cambios de visibilidad ni contacto con terceros sin autorización para esas acciones.

Actualizar la documentación vigente cuando cambie el estado del proyecto. Informar de cambios, comprobaciones ejecutadas y pendientes reales.

Yeison Arbey Carrillo Lemus. Todos los derechos reservados.
