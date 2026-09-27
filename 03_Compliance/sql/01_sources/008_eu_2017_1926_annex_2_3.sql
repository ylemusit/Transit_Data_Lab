BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
--
-- ANNEX
-- 2.3 Level of service 3
--
-- IMPORTANT MODELING DECISION
--
-- The legal source contains no child paragraph below 2.3.
-- The substantive data category is expressed directly at 2.3.
--
-- Therefore:
--
--   NO synthetic 2.3(i)
--   NO synthetic DATA_ELEMENT child
--
-- The existing ANNEX_LEVEL provision is enriched directly.
-- ============================================================

UPDATE source.provisions

SET
    heading =
        'Nivel de servicio 3 - Información sobre ocupación del vehículo',

    text_content =
        'Información sobre la ocupación del vehículo para el transporte programado y el transporte a la demanda, cuando proceda.',

    source_reference =
        'Annex 2.3',

    notes =
        'Terminal ANNEX_LEVEL: the legal source contains the substantive data category directly at point 2.3 and has no child subparagraphs.'

WHERE provision_id = 'EU-2017-1926-ANNEX-2.3'
  AND document_id = 'EU-REG-2017-1926';

COMMIT;
