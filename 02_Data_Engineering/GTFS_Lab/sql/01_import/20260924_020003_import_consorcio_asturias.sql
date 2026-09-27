BEGIN TRANSACTION;

CREATE SCHEMA IF NOT EXISTS raw;

CREATE OR REPLACE TABLE raw.agency AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/agency.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.calendar_dates AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/calendar_dates.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.routes AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/routes.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.shapes AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/shapes.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.stop_times AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/stop_times.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.stops AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/stops.txt',
    header = true,
    all_varchar = true
);

CREATE OR REPLACE TABLE raw.trips AS
SELECT *
FROM read_csv(
    'feeds/extracted/20260924_020003_Consorcio_Asturias/trips.txt',
    header = true,
    all_varchar = true
);

COMMIT;