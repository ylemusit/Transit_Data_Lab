# TDL — calidad de auditoría y doble entrega V1

Actualizado: 2026-10-09. Estado: estándar propuesto; TDL-AUD-01–11, 14–18 y 21–22 comprobadas en sus alcances; 19/20 parciales. La 21 demuestra un [recorrido operativo interno](audit_service_v1/README.md), con acuerdos/aceptaciones simulados e integración de aplicación pendiente. La 22 registra [frases y límites comerciales](../07_Business/03_Market/TDL_GTFS_NETEX_CLAIMS_REGISTER_20261009.md) sin autorizar publicación ni cambiar la baseline Business congelada. TDL-AUD-18 tiene lista aplicada sin revisión humana independiente ni autorización de emisión; 19 tiene especificación/prototipo sin interacción de navegador comprobada; 20 tiene protocolo sin sesiones. Diseño 10/11, medición sintética 15, replay aislado misma máquina 16 y seguimiento con comunicaciones/aceptaciones simuladas 17. Sin precisión universal ni aceptación externa. [Doble entrega y portabilidad](audit_delivery_v1/README.md), [gestión del corpus](audit_corpus_v1/README.md), [banco inicial](audit_reference_bank_v1/README.md) y [revisión/UX](audit_quality_gate_v1/README.md). Los objetivos restantes no son capacidades verificadas ni abren fases comerciales. No cambia motores, corpus congelado, readiness o autorización externa.

## Resultado que perseguimos

Que un productor pueda localizar y corregir un problema, que dirección pueda decidir qué hacer y que un tercero pueda reproducir el resultado dentro del alcance declarado. Aspirar a ser referente requiere demostrar esas tres cosas; contar reglas, normas o páginas no basta.

La entrega tiene dos vistas de una misma evidencia:

* **Dirección:** 2–3 páginas con conclusión, consecuencias demostradas y posibles claramente diferenciadas, decisiones, funciones responsables, siguiente paso y límites. Sin códigos de reglas ni catálogo normativo en el cuerpo. No se inventan costes, retorno de inversión o viajeros afectados.
* **Desarrollo / productor:** alcance, versiones, criterios, filas y entidades afectadas, cobertura, denominadores, acción y prueba de cierre; matrices y evidencias completas.
* **Anexos:** cartografía y contexto normativo consultables por separado. El expediente R4 actual es documentación complementaria, no una demostración de comprensión ejecutiva.

Ambas vistas deben conservar identidad, cifras, estados y criterios de cierre. Una corrección comunicada requiere una ejecución nueva antes de declararse resuelta.

## Estado observado frente al objetivo

Las cifras de cada entrega deben conciliar con su fuente y distinguir registros, eventos y referencias duplicadas. Los resultados aplicados se conservan en expedientes privados.

Compliance V1 declara 48 requisitos: ninguno completo, seis parciales, doce con revisión humana, veinte diferidos y diez fuera de alcance. Las capturas jurídicas contextualizan; no amplían por sí mismas lo que comprueba el motor. NeTEx distingue XML, XSD, perfil, semántica, calidad y regulación; sus reglas iniciales son pequeñas y la conformidad EPIP necesita revisión humana. No hay equivalencia demostrada entre la cobertura GTFS y NeTEx.

## Condiciones de aceptación objetivo

Estos umbrales son compromisos de diseño pendientes de implementación o prueba donde no exista evidencia vinculada.

| Área | Condición de aceptación | Evidencia necesaria |
|---|---|---|
| Análisis y desarrollo | Cada control identifica ámbito, condición de aplicación, versión, resultado y casos límite. Un caso positivo y negativo representativos por regla; denominador o motivo de ausencia. | Registro de controles, fixtures y ejecución versionada. |
| Cobertura | Cada requisito del alcance tiene decisión explícita: comprobable, humano, diferido o excluido. Cada no evaluable explica causa, parte no cubierta y comprobación alternativa disponible. | Matriz con correspondencias estables entre motor, informe y corpus. |
| Corpus | Fuente, autoridad, versión, vigencia conocida, captura e integridad; responsable de revisión y desencadenante de actualización. Separar regla de formato, perfil y obligación aplicable. | Registro de fuentes y revisión de aplicabilidad; incertidumbres visibles. |
| Reproducibilidad | Misma fuente, configuración, corpus y versiones producen resultados semánticamente equivalentes en un entorno independiente. Todo hallazgo tiene localizador verificable. | Receta offline, manifiesto, comparación normalizada y acta de replay. Las fechas de generación no exigen PDFs idénticos. |
| Integridad de entrega | Cero enlaces o referencias de fichero rotos dentro del paquete conjunto; inventario completo, sin alteración de fuentes y verificación de hashes. | Prueba de traslado a otra carpeta y comprobación automatizada de referencias. |
| UI | Navegación y estados consistentes; contraste y texto legible; uso con teclado en pantallas; errores que indiquen cómo continuar. | Revisión visual y funcional por soporte; PDF con texto seleccionable. Accesibilidad formal exige su propia evaluación. |
| UX | Un productor localiza un hallazgo y su criterio de cierre sin ayuda; dirección identifica decisión, responsable propuesto y límite. Objetivo inicial: al menos 4 de 5 participantes de cada perfil realizan la tarea en 5 minutos. | Protocolo, tiempos y observaciones de usuarios autorizados; muestra exploratoria, no prueba estadística de mercado. |
| CX | El cliente entiende qué compró, cuándo recibe resultados y cómo se cierra una corrección. No recibe mensajes contradictorios entre contratación, interfaz e informe. | Recorrido completo y comprobación de cada comunicación; prueba con participantes autorizados. |
| Diseño del servicio (SD) | Entrada → alcance acordado → auditoría → revisión → doble entrega → respuesta → nueva auditoría → aceptación, con responsable, entrada, salida y excepción por etapa. | Mapa del servicio, expediente de decisiones y estados de seguimiento. |
| Comercial y gestión | Toda afirmación de capacidad enlaza una prueba vigente y un alcance. Diferenciar capacidad disponible, en desarrollo y prevista. Beneficios económicos solo con medición y supuestos visibles. | Registro de afirmaciones, evidencia de necesidad y disposición a pagar; aprobación según gobernanza Business. |

## Recorrido del servicio

| Momento | Lo que necesita el cliente | Trabajo de TDL y prueba de salida |
|---|---|---|
| Antes del análisis | Saber qué se revisa, qué aporta y qué necesita aportar. | Acordar formato, perfil, destino y calendario; conservar alcance aceptado. |
| Recepción | Confirmación de versión y tratamiento del fichero. | Identificar fuente, integridad y restricciones; bloquear entradas inválidas con explicación. |
| Análisis | Confianza en la cobertura y en la localización del problema. | Ejecutar controles versionados, registrar omisiones y revisar interpretación. |
| Entrega | Dirección decide; productor actúa. | Dos informes coherentes, anexos y referencias portátiles verificadas. |
| Corrección | Saber quién responde y qué demuestra el cierre. | Registrar respuesta y nueva versión, repetir comprobaciones comparables. |
| Aceptación | Saber qué queda resuelto y qué limitaciones se aceptan. | Acta de cierre con destinatario, evidencias y pendientes; conservar versiones. |

## Orden de mejora

Lista ejecutable con IDs, prioridades, dependencias y criterios de aceptación: [backlog V1](TDL_AUDIT_IMPROVEMENT_BACKLOG_V1.md).

1. **Entrega comprensible:** vista ejecutiva implementada en alcance limitado; validar su comprensión y conectar ambas vistas mediante un índice portable. Pendiente generalizar el generador a modelos y formatos distintos. No sustituye el informe técnico.
2. **Coherencia verificable:** correspondencia 24/32, explicación de no evaluables, denominadores y distinción campo opcional / valor inválido. Resolver dependencias externas de R4 en un paquete conjunto nuevo, preservando los sellados.
3. **Confianza reproducible:** probar replay independiente, comparación de versiones, trazabilidad del cierre y fallos de entrada. Conservar diferencias técnicas y de servicio; un PASS técnico no decide la aceptación del destinatario.
4. **Profundidad por alcance:** inventario de brechas GTFS y NeTEx separado y priorizado por destinatario y evidencia. Definir cada ampliación como tarea propia con reglas, fuente y fixtures; no modificar baselines congelados dentro de este trabajo.
5. **Servicio y negocio:** comprobar tareas con usuarios, luego necesidad, compra y beneficios. Contactos, envío y pilotos requieren la autorización correspondiente; este documento no los realiza ni abre Offering, Economics o GoToMarket.

La selección de riesgo y urgencia requiere destino, fechas y consecuencias demostradas. El orden anterior es una secuencia de dependencias, no una clasificación de gravedad de los hallazgos.
