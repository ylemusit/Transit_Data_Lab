# Serializar sin materializar el JSON completo

- **CONTEXT:** Los runs a escala pueden exigir una segunda representación completa del modelo en memoria.
- **PROBLEM / ROOT_CAUSE:** `json.dumps` creaba una cadena completa antes de escribir; el mecanismo quedó confirmado en la reproducción sintética.
- **DECISION_OR_SOLUTION:** Usar `JSONEncoder.iterencode`, lotes de 65.536 caracteres y el mismo formato/salto final. Verificar igualdad sobre un objeto determinista y replay semántico.
- **EVIDENCE / RELATED_COMMITS_OR_REPORTS:** [Fuente autoritativa](https://github.com/ylemusit/Transit_Data_Lab/blob/cf4e0a30f6837b077e6994305f51fbf2cca8282c/reports/WINDOWS_SELF_SERVICE_CLIENT_V1_W00_P_JSON_SERIALIZATION_OPTIMIZATION_PROOF.md).
- **IMPACT:** En S64 el pico privado muestreado bajó de 4.662.751.232 a 866.676.736 bytes, con +4,14 % de tiempo total.
- **REUSABLE_LESSON:** Medir el árbol de procesos y separar memoria muestreada de high-water marks. No extrapolar esta causa al dataset 019.
- **STATUS:** Retenido; alcance y límites de la fuente, sin nueva certificación.
