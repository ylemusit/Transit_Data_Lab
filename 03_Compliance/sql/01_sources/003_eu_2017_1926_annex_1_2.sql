BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
-- ANNEX 1.2 - Level of service 2
--
-- IMPORTANT:
-- heading/text_content are normalized descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 1.2(a)
-- Location search
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(a)',
    'Búsqueda de ubicación — transporte a demanda y transporte personal',
    'Búsqueda de ubicación para transporte a demanda y transporte personal.',
    'Annex 1.2(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(i)',
    'Ubicación de plazas de estacionamiento',
    'Ubicación de plazas de estacionamiento en vía pública y fuera de ella, incluidas plazas accesibles para personas con discapacidad y movilidad reducida.',
    'Annex 1.2(a)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(ii)',
    'Paradas Park & Ride',
    'Localización de paradas o instalaciones Park & Ride.',
    'Annex 1.2(a)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-II'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(iii)',
    'Paradas Park & Drive',
    'Localización de paradas o instalaciones Park & Drive.',
    'Annex 1.2(a)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-III'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(iv)',
    'Estaciones de bicicletas compartidas',
    'Localización de estaciones de bicicletas compartidas.',
    'Annex 1.2(a)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-IV'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-V',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(v)',
    'Estaciones de coches compartidos',
    'Localización de estaciones de coches compartidos.',
    'Annex 1.2(a)(v)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-V'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-VI',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(vi)',
    'Estacionamiento seguro para bicicletas',
    'Localización de estacionamiento seguro para bicicletas, como garajes cerrados.',
    'Annex 1.2(a)(vi)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-VI'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-A-VII',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(a)(vii)',
    'Zonas de estacionamiento de patinetes',
    'Localización de zonas de estacionamiento de patinetes.',
    'Annex 1.2(a)(vii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-A-VII'
);


-- ------------------------------------------------------------
-- 1.2(b)
-- Information service
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(b)',
    'Servicio de información',
    'Información relativa a adquisición de billetes y pago de estacionamiento.',
    'Annex 1.2(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(b)(i)',
    'Dónde y cómo comprar billetes',
    'Dónde y cómo comprar billetes para transporte programado, incluidos canales de venta, métodos de entrega y métodos de pago.',
    'Annex 1.2(b)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-B-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(b)(ii)',
    'Dónde y cómo pagar el estacionamiento',
    'Dónde y cómo pagar el estacionamiento, incluidos canales de venta, métodos de entrega y métodos de pago.',
    'Annex 1.2(b)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-B-II'
);


-- ------------------------------------------------------------
-- 1.2(c)
-- Auxiliary information
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.2',
    '1.2(c)',
    'Información auxiliar',
    'Información auxiliar para transporte programado y transporte a demanda cuando resulte pertinente.',
    'Annex 1.2(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(c)(i)',
    'Tarifas estándar comunes básicas',
    'Datos de red tarifaria y estructuras tarifarias estándar, incluidas zonas, paradas, etapas tarifarias y tarifas punto a punto, diarias, semanales, zonales o planas.',
    'Annex 1.2(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C-I'
);


INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.2-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.2',
    '1.2(c)(ii)',
    'Equipamiento de los vehículos',
    'Equipamiento del vehículo, incluidas clases de transporte, Wi-Fi a bordo, capacidad y condiciones de acceso para bicicletas.',
    'Annex 1.2(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.2-C-II'
);


COMMIT;
