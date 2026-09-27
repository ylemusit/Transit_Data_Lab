-- ============================================================
-- TRANSIT DATA LAB
-- EU 2017/1926 - ANNEX 1.1
-- Level of service 1
--
-- Source:
-- Consolidated Regulation (EU) 2017/1926
-- Version: 04/03/2024
--
-- Purpose:
-- Preserve the legal/source hierarchy before normalization
-- into compliance.requirements.
-- ============================================================


-- ------------------------------------------------------------
-- 1.1(a) LOCATION SEARCH - ORIGIN / DESTINATION
-- ------------------------------------------------------------

INSERT INTO source.provisions VALUES

(
    'EU-2017-1926-ANNEX-1.1-A',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    'ANNEX',
    '1.1(a)',
    'Búsqueda de ubicación (origen/destino)',
    NULL,
    'ANEXO 1.1(a)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-A-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(a)(i)',
    'Direcciones',
    'Direcciones: calle, número y código postal.',
    'ANEXO 1.1(a)(i)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-A-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(a)(ii)',
    'Lugares topográficos',
    'Lugares topográficos: ciudad, pueblo, suburbio y demarcación administrativa.',
    'ANEXO 1.1(a)(ii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-A-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(a)(iii)',
    'Puntos de interés relacionados con transporte',
    'Puntos de interés relacionados con información de transporte a los que las personas pueden desear desplazarse.',
    'ANEXO 1.1(a)(iii)',
    NULL,
    CURRENT_TIMESTAMP
);


-- ------------------------------------------------------------
-- 1.1(b) TRIP PLANS / OPERATIONAL CALENDAR
-- ------------------------------------------------------------

INSERT INTO source.provisions VALUES

(
    'EU-2017-1926-ANNEX-1.1-B',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(b)',
    'Calendario operativo',
    'Planes de viaje: calendario operativo, asociando tipos de día con fechas de calendario.',
    'ANEXO 1.1(b)',
    NULL,
    CURRENT_TIMESTAMP
);


-- ------------------------------------------------------------
-- 1.1(c) ACCESS NODES
-- ------------------------------------------------------------

INSERT INTO source.provisions VALUES

(
    'EU-2017-1926-ANNEX-1.1-C',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    'ANNEX',
    '1.1(c)',
    'Búsqueda de ubicación - nodos de acceso',
    'Aplicable al transporte programado y al transporte a la demanda cuando proceda.',
    'ANEXO 1.1(c)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-C-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(c)(i)',
    'Nodos de acceso identificados',
    'Nodos de acceso identificados.',
    'ANEXO 1.1(c)(i)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-C-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(c)(ii)',
    'Geometría de los nodos de acceso',
    'Geometría o estructura cartográfica de los nodos de acceso.',
    'ANEXO 1.1(c)(ii)',
    NULL,
    CURRENT_TIMESTAMP
);


-- ------------------------------------------------------------
-- 1.1(d) TRIP PLAN COMPUTATION
-- Scheduled transport / transport on demand where relevant
-- ------------------------------------------------------------

INSERT INTO source.provisions VALUES

(
    'EU-2017-1926-ANNEX-1.1-D',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)',
    'Cálculo de planes de viaje - transporte programado y a demanda',
    'Aplicable al transporte programado y al transporte a la demanda cuando proceda.',
    'ANEXO 1.1(d)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(i)',
    'Conexión para correspondencias',
    'Conexión para las correspondencias.',
    'ANEXO 1.1(d)(i)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(ii)',
    'Tiempos de correspondencia por defecto',
    'Tiempos de correspondencia por defecto en los intercambiadores.',
    'ANEXO 1.1(d)(ii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(iii)',
    'Topología de redes y rutas/líneas',
    'Topología de las redes y rutas/líneas.',
    'ANEXO 1.1(d)(iii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-IV',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(iv)',
    'Operadores de transporte',
    'Operadores de transporte.',
    'ANEXO 1.1(d)(iv)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-V',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(v)',
    'Horarios',
    'Horarios.',
    'ANEXO 1.1(d)(v)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-VI',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(vi)',
    'Correspondencias previstas entre servicios garantizados',
    'Correspondencias previstas entre servicios programados garantizados.',
    'ANEXO 1.1(d)(vi)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-VII',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(vii)',
    'Horario de funcionamiento',
    'Horario de funcionamiento.',
    'ANEXO 1.1(d)(vii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-VIII',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(viii)',
    'Servicios en los nodos de acceso',
    'Información sobre servicios e instalaciones disponibles en los nodos de acceso.',
    'ANEXO 1.1(d)(viii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-IX',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(ix)',
    'Vehículos y accesibilidad',
    'Información sobre vehículos, su accesibilidad y la accesibilidad de los servicios a bordo.',
    'ANEXO 1.1(d)(ix)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-X',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(x)',
    'Accesibilidad de nodos e intercambiadores',
    'Accesibilidad de los nodos de acceso y recorridos dentro de un intercambiador.',
    'ANEXO 1.1(d)(x)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-D-XI',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(d)(xi)',
    'Servicios de asistencia',
    'Servicios de asistencia disponibles.',
    'ANEXO 1.1(d)(xi)',
    NULL,
    CURRENT_TIMESTAMP
);


-- ------------------------------------------------------------
-- 1.1(e) NETWORKS USED FOR TRIP PLAN COMPUTATION
-- ------------------------------------------------------------

INSERT INTO source.provisions VALUES

(
    'EU-2017-1926-ANNEX-1.1-E',
    'EU-REG-2017-1926',
    'ANNEX_GROUP',
    NULL,
    NULL,
    'ANNEX',
    '1.1(e)',
    'Redes para cálculo de planes de viaje',
    NULL,
    'ANEXO 1.1(e)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-E-I',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(e)(i)',
    'Red de carreteras',
    'Red de carreteras, incluidos carriles separados para autobús o taxi.',
    'ANEXO 1.1(e)(i)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-E-II',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(e)(ii)',
    'Red para bicicletas',
    'Red para bicicletas y sus diferentes tipos de infraestructura compartida o segregada.',
    'ANEXO 1.1(e)(ii)',
    NULL,
    CURRENT_TIMESTAMP
),

(
    'EU-2017-1926-ANNEX-1.1-E-III',
    'EU-REG-2017-1926',
    'DATA_ELEMENT',
    NULL,
    NULL,
    'ANNEX',
    '1.1(e)(iii)',
    'Red para peatones e instalaciones de accesibilidad',
    'Red para peatones e instalaciones de accesibilidad.',
    'ANEXO 1.1(e)(iii)',
    NULL,
    CURRENT_TIMESTAMP
);
