BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
--
-- ANNEX
-- 2. TYPES OF DYNAMIC TRAVEL AND TRAFFIC DATA
-- 2.1 Level of service 1
--
-- Heading:
-- Passing times, trip plans and auxiliary information
--
-- Legal structure:
--   (i)
--   (ii)
--   (iii)
--
-- No ANNEX_GROUP nodes exist below 2.1.
--
-- heading/text_content contain normalized Spanish descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 2.1(i)
-- Disruptions
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(i)',
    'Perturbaciones',
    'Perturbaciones, como cierres de redes o desvíos y, cuando sea posible, el motivo de la perturbación.',
    'Annex 2.1(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-I'
);


-- ------------------------------------------------------------
-- 2.1(ii)
-- Real-time status information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(ii)',
    'Información sobre la situación en tiempo real',
    'Información sobre la situación en tiempo real, como horas estimadas de salida y llegada de los servicios, retrasos, anulaciones y seguimiento de correspondencias garantizadas.',
    'Annex 2.1(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-II'
);


-- ------------------------------------------------------------
-- 2.1(iii)
-- Access node feature status
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.1-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.1',
    '2.1(iii)',
    'Estado de los servicios en los nodos de acceso',
    'Estado de los servicios en los nodos de acceso, incluida información dinámica sobre andenes, ascensores o escaleras mecánicas en funcionamiento y entradas y salidas cerradas, para los transportes programados.',
    'Annex 2.1(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.1-III'
);

COMMIT;
