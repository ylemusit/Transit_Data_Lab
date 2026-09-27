BEGIN TRANSACTION;

-- ============================================================
-- ANNEX 1.4 - LEVEL OF SERVICE 4
--
-- Consolidated Regulation (EU) 2017/1926
-- Version: 04/03/2024
--
-- IMPORTANT:
-- 1.4(a) and 1.4(d) are terminal legal elements.
-- Only (b) and (c) are represented as ANNEX_GROUP.
-- ============================================================


-- ------------------------------------------------------------
-- 1.4(a)
-- Historic travel and traffic data
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-A',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(a)',
    'Datos históricos de desplazamientos y tráfico sobre retrasos',
    'Datos históricos de desplazamientos y tráfico sobre retrasos para transporte programado y transporte a la demanda cuando proceda.',
    'Annex 1.4(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-A'
);


-- ------------------------------------------------------------
-- 1.4(b)
-- Observed delays and passing times
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.4',
    '1.4(b)',
    'Datos observados sobre retrasos y tiempos de paso',
    'Datos observados sobre retrasos y tiempos de paso para transporte programado.',
    'Annex 1.4(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(i)',
    'Retrasos ferroviarios de al menos 60 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos de al menos 60 minutos en servicios ferroviarios de viajeros.',
    'Annex 1.4(b)(i)',
    'Threshold linked by the Regulation to Regulation (EU) 2021/782.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(ii)',
    'Retrasos marítimos y por vías navegables superiores a 90 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos en la salida superiores a 90 minutos en servicios de pasajeros por mar y vías navegables interiores.',
    'Annex 1.4(b)(ii)',
    'Threshold linked by the Regulation to Regulation (EU) No 1177/2010.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(iii)',
    'Retrasos de autobús y autocar superiores a 120 minutos',
    'Duración y, cuando sea posible, motivo de los retrasos en la salida desde una terminal superiores a 120 minutos para servicios regulares de autobús y autocar con distancia programada de 250 km o más.',
    'Annex 1.4(b)(iii)',
    'Threshold linked by the Regulation to Regulation (EU) No 181/2011.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-B-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(b)(iv)',
    'Retrasos de vuelos',
    'Duración y, cuando sea posible, motivo de retrasos de vuelos en salida de al menos 120 minutos y en llegada de al menos 180 minutos.',
    'Annex 1.4(b)(iv)',
    'Threshold linked by the Regulation to Regulation (EC) No 261/2004.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-B-IV'
);


-- ------------------------------------------------------------
-- 1.4(c)
-- Observed cancellations
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.4',
    '1.4(c)',
    'Datos observados sobre cancelaciones',
    'Datos observados sobre cancelaciones para transporte programado.',
    'Annex 1.4(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(i)',
    'Cancelaciones ferroviarias',
    'Cancelaciones y, cuando sea posible, motivo de la cancelación de servicios ferroviarios de viajeros.',
    'Annex 1.4(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(ii)',
    'Cancelaciones marítimas y por vías navegables',
    'Cancelaciones y, cuando sea posible, motivo de servicios de pasajeros por mar y vías navegables interiores.',
    'Annex 1.4(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(iii)',
    'Cancelaciones de autobús y autocar',
    'Cancelaciones y, cuando sea posible, motivo de servicios regulares de autobús y autocar con distancia programada de 250 km o más.',
    'Annex 1.4(c)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-C-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(c)(iv)',
    'Cancelaciones de vuelos',
    'Cancelaciones y, cuando sea posible, motivo de cancelación de vuelos.',
    'Annex 1.4(c)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-C-IV'
);


-- ------------------------------------------------------------
-- 1.4(d)
-- Parking tariffs
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.4-D',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.4',
    '1.4(d)',
    'Información sobre tarifas de estacionamiento',
    'Información sobre tarifas de estacionamiento.',
    'Annex 1.4(d)',
    'Terminal legal element.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.4-D'
);


COMMIT;
