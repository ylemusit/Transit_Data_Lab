# Implementación delimitada TDL-AUD-12/13 — 2026-10-09

Se añaden dos diagnósticos estáticos, opt-in y versionados, sin modificar las salidas ni los motores congelados. Son incrementos de cobertura concreta, no una declaración de auditoría universal.

## GTFS — TDL-AUD-12

`02_Data_Engineering/GTFS_Lab/gtfs_lab/condition_rules_v1.py` implementa G-PLAN-01 y G-PLAN-02 sobre `agency.txt` y `routes.txt`:

- exige `agency_id` en ambas tablas cuando se declaran varias agencias;
- permite omitirlo para una agencia;
- comprueba referencias suministradas de ruta a agencia;
- devuelve `NOT_EVALUABLE` cuando falta el contexto para resolverlas.

El resultado usa un contrato lateral `TDL_GTFS_CONDITIONAL_RULES_V1` e identidad SHA-256. No se integra en el pipeline congelado y no reescribe el feed.
Siete pruebas cubren multi-agencia válida, ausencias, referencia huérfana, feed de una agencia e incertidumbre de cardinalidad.

Desde `02_Data_Engineering/GTFS_Lab`:

```powershell
python -m gtfs_lab.condition_rules_v1 input.zip --json output.json
python -m unittest tests.test_condition_rules_v1 tests.test_client_report
```

## NeTEx — TDL-AUD-13

`02_Data_Engineering/NeTEx_Lab/netex_lab/reference_context_v1.py` implementa el candidato `TDL-CAND-NETEX-REFERENCE-CONTEXT` como diagnóstico TDL: compara referencias simples `*Ref/@ref` con objetos locales del tipo inferido, usando `versionRef` si se proporciona.

- Los enlaces exactos locales quedan en `PASS`.
- Los destinos ausentes quedan `NOT_EVALUABLE` por defecto.
- `--closed-scope` registra que quien ejecuta declara completo el conjunto XML aportado; una referencia no resuelta pasa a revisión humana, nunca a incumplimiento normativo.
- Un XML no interpretable deja incompleto el inventario y fuerza abstención.

No se interpretan alias, referencias textuales ni mapeos específicos de perfil. Esto no valida XSD, EPIP, perfil español, NAP ni cumplimiento legal. El motor NeTEx V1 conserva su contrato y salida.

Desde `02_Data_Engineering/NeTEx_Lab`:

```powershell
python -m netex_lab.reference_context_v1 input.zip --json output.json
python -m netex_lab.reference_context_v1 input.zip --closed-scope --json output.json
python -m unittest tests.test_reference_context_v1 tests.test_netex_audit
```

## Coherencia de informes y diagnósticos por archivo

`GTFS_Lab/gtfs_lab/client_report.py` proyecta ahora el agregado técnico G03–G07 por separado de la validación legacy y de su resumen almacenado. Un `PASS` legacy no oculta un `FAIL_TECHNICAL` del motor en el resumen ejecutivo ni en el informe.

`NeTEx_Lab/netex_lab/intake.py` limpia el registro de errores de libxml antes de validar cada miembro. La regresión cubre dos XML inválidos consecutivos con mensajes distintos y un tercero válido; cada informe conserva solo el mensaje de su propio XML.

Estas correcciones se han comprobado en regresiones sintéticas. No se regeneró ni alteró el expediente del operador sellado; una nueva ejecución separada deberá producir informes actualizados.

## Límites operativos pendientes

No existe una versión corregida del operador entregada por su productor ni una respuesta o aceptación humana del operador. El ciclo real de corrección y aceptación queda pendiente de esos artefactos; el recorrido interno simulado de TDL-AUD-17 no lo reemplaza.

Estos cambios amplían auditoría estática. No crean ni convierten feeds, no los despliegan, y no añaden GTFS-RT/SIRI. Para generar NeTEx de producción falta identificar el perfil/destino y acordar las correspondencias de campos y el catálogo de datos del operador; el XSD NeTEx 2.0.0 no resuelve esas decisiones.
