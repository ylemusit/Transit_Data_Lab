BEGIN TRANSACTION;

-- ============================================================
-- Regulation (EU) 2017/1926
-- Consolidated version: 04/03/2024
-- ANNEX 1.3 - Level of service 3
--
-- heading/text_content are normalized descriptions.
-- source_reference preserves the legal location.
-- ============================================================


-- ------------------------------------------------------------
-- 1.3(a)
-- Detailed fare query
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(a)',
    'Consulta detallada de tarifas normales comunes y tarifas especiales',
    'Consulta detallada de tarifas normales comunes y tarifas especiales para transporte programado y transporte a la demanda cuando proceda.',
    'Annex 1.3(a)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(i)',
    'Clases de pasajeros',
    'Clases de pasajeros, condiciones de cualificación y clases de viaje.',
    'Annex 1.3(a)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-I'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(ii)',
    'Productos tarifarios comunes',
    'Productos tarifarios comunes: derechos de acceso, elegibilidad, condiciones básicas de uso y precios estándar.',
    'Annex 1.3(a)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-II'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(iii)',
    'Productos tarifarios especiales',
    'Productos tarifarios con condiciones especiales, como promociones, grupos, abonos, productos agregados y productos suplementarios.',
    'Annex 1.3(a)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-III'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(iv)',
    'Condiciones comerciales básicas',
    'Condiciones comerciales básicas, como reembolso, sustitución, cambio o transferencia.',
    'Annex 1.3(a)(iv)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-IV'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-A-V',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(a)(v)',
    'Condiciones básicas de reserva',
    'Condiciones básicas de reserva: ventanas de compra, períodos de validez, restricciones de itinerario, secuencias zonales y estancia mínima.',
    'Annex 1.3(a)(v)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-A-V'
);


-- ------------------------------------------------------------
-- 1.3(b)
-- Demand-responsive transport booking
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-B',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(b)',
    'Servicio de información para transporte a la demanda',
    'Información sobre cómo reservar servicios de transporte a la demanda.',
    'Annex 1.3(b)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-B'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-B-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(b)(i)',
    'Reserva de transporte a la demanda',
    'Cómo reservar servicios de transporte a la demanda, incluidos canales minoristas, métodos de ejecución y métodos de pago.',
    'Annex 1.3(b)',
    'Normalized terminal data element. The legal Annex expresses this content directly under point (b), without a numbered subpoint.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-B-I'
);


-- ------------------------------------------------------------
-- 1.3(c)
-- Trip plans
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(c)',
    'Planes de viaje',
    'Datos adicionales utilizados en planes de viaje.',
    'Annex 1.3(c)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(i)',
    'Características detalladas de la red ciclista',
    'Características detalladas de la red ciclista, como firme, circulación en paralelo, superficies compartidas y restricciones de giro o acceso.',
    'Annex 1.3(c)(i)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-I'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(ii)',
    'Parámetros para calcular factores medioambientales',
    'Parámetros necesarios para calcular factores medioambientales, como emisiones de gases de efecto invernadero.',
    'Annex 1.3(c)(ii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-II'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-C-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(c)(iii)',
    'Parámetros para calcular el consumo de combustible',
    'Parámetros necesarios para calcular el consumo de combustibles convencionales y alternativos.',
    'Annex 1.3(c)(iii)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-C-III'
);


-- ------------------------------------------------------------
-- 1.3(d)
-- Trip plan computation
-- ------------------------------------------------------------

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-D',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    '1.3',
    '1.3(d)',
    'Cálculo de planes de viaje',
    'Cálculo de planes de viaje mediante tiempos de viaje estimados.',
    'Annex 1.3(d)',
    'Normalized description from consolidated Annex.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-D'
);

INSERT INTO source.provisions
SELECT
    'EU-2017-1926-ANNEX-1.3-D-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    '1.3',
    '1.3(d)(i)',
    'Tiempos de viaje estimados',
    'Tiempos de viaje estimados por tipo de día, franja horaria y modo o combinación de modos de transporte.',
    'Annex 1.3(d)',
    'Normalized terminal data element. The legal Annex expresses this content directly under point (d), without a numbered subpoint.',
    CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM source.provisions
    WHERE provision_id = 'EU-2017-1926-ANNEX-1.3-D-I'
);

COMMIT;
