BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
--
-- ANNEX
-- 2. TYPES OF DYNAMIC TRAVEL AND TRAFFIC DATA
-- 2.2 Level of service 2
--
-- Legal structure:
--
-- (a) terminal element
--
-- (b) availability check and location
--     (i)
--     (ii)
--
-- IMPORTANT:
-- No artificial ANNEX_GROUP is created for 2.2(a).
-- heading/text_content contain normalized Spanish descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 2.2(a)
-- Parking tariff information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-A',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(a)',
    'Información sobre tarifas de estacionamiento',
    'Servicio de información sobre tarifas de estacionamiento para transporte a la demanda y transporte personal.',
    'Annex 2.2(a)',
    'Terminal legal element. Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-A'
);


-- ------------------------------------------------------------
-- 2.2(b)
-- Availability check and location
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '2.2',
    '2.2(b)',
    'Consulta de disponibilidad y localización',
    'Consulta de disponibilidad y localización para transporte a la demanda y transporte personal cuando proceda.',
    'Annex 2.2(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B'
);


-- ------------------------------------------------------------
-- 2.2(b)(i)
-- Shared vehicles
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(b)(i)',
    'Disponibilidad y localización de vehículos compartidos',
    'Disponibilidad y localización de coches compartidos, bicicletas compartidas, patinetes compartidos y otros vehículos compartidos.',
    'Annex 2.2(b)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B-I'
);


-- ------------------------------------------------------------
-- 2.2(b)(ii)
-- Available parking spaces
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-2.2-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '2.2',
    '2.2(b)(ii)',
    'Plazas de estacionamiento disponibles',
    'Plazas de estacionamiento disponibles, tanto en vía pública como fuera de ella.',
    'Annex 2.2(b)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-2.2-B-II'
);

COMMIT;
