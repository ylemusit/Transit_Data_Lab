-- Transit Data Lab - GTFS Lab read-only integrity audit
-- Run from the Transit Data Lab root with:
-- duckdb -readonly "02_Data_Engineering/GTFS_Lab/databases/gtfs_lab.duckdb" < "02_Data_Engineering/GTFS_Lab/sql/07_tests/test_gtfs_lab_integrity.sql"
-- This file contains SELECT statements only. It is an integrity sentinel, not a
-- complete GTFS validator.

-- 1. Frozen raw row-count baseline.
WITH expected(table_name, expected_count) AS (
    VALUES
        ('agency', 41),
        ('calendar_dates', 3875),
        ('routes', 609),
        ('shapes', 774732),
        ('stop_times', 354287),
        ('stops', 6368),
        ('trips', 21015)
),
actual AS (
    SELECT 'agency' table_name, COUNT(*) actual_count FROM raw.agency
    UNION ALL SELECT 'calendar_dates', COUNT(*) FROM raw.calendar_dates
    UNION ALL SELECT 'routes', COUNT(*) FROM raw.routes
    UNION ALL SELECT 'shapes', COUNT(*) FROM raw.shapes
    UNION ALL SELECT 'stop_times', COUNT(*) FROM raw.stop_times
    UNION ALL SELECT 'stops', COUNT(*) FROM raw.stops
    UNION ALL SELECT 'trips', COUNT(*) FROM raw.trips
)
SELECT
    'RAW_COUNT' check_family,
    e.table_name check_name,
    e.expected_count expected,
    a.actual_count actual,
    CASE WHEN e.expected_count = a.actual_count THEN 'PASS' ELSE 'FAIL' END status
FROM expected e
LEFT JOIN actual a USING (table_name)
ORDER BY e.table_name;

-- 2. Expected architecture. Only raw currently exists; absent later layers are
-- reported, never created by this test.
WITH expected(schema_name) AS (
    VALUES ('raw'), ('core'), ('validation'), ('analysis')
)
SELECT
    'SCHEMA' check_family,
    e.schema_name check_name,
    'present' expected,
    CASE WHEN s.schema_name IS NULL THEN 'absent' ELSE 'present' END actual,
    CASE WHEN s.schema_name IS NULL THEN 'FAIL' ELSE 'PASS' END status
FROM expected e
LEFT JOIN (
    SELECT DISTINCT schema_name
    FROM information_schema.schemata
) s USING (schema_name)
ORDER BY e.schema_name;

WITH expected(table_schema, table_name) AS (
    VALUES
        ('raw', 'agency'),
        ('raw', 'calendar_dates'),
        ('raw', 'routes'),
        ('raw', 'shapes'),
        ('raw', 'stop_times'),
        ('raw', 'stops'),
        ('raw', 'trips'),
        ('validation', 'results')
)
SELECT
    'RELATION' check_family,
    e.table_schema || '.' || e.table_name check_name,
    'present' expected,
    CASE WHEN t.table_name IS NULL THEN 'absent' ELSE lower(t.table_type) END actual,
    CASE WHEN t.table_name IS NULL THEN 'FAIL' ELSE 'PASS' END status
FROM expected e
LEFT JOIN information_schema.tables t
  ON t.table_schema = e.table_schema
 AND t.table_name = e.table_name
ORDER BY e.table_schema, e.table_name;

-- 3. Structural duplicates, important references, coordinates and sequences.
WITH checks(check_name, expected, actual) AS (
    SELECT 'duplicate_agency_id', 0, COUNT(*) FROM (
        SELECT agency_id FROM raw.agency GROUP BY agency_id HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_calendar_service_date', 0, COUNT(*) FROM (
        SELECT service_id, date FROM raw.calendar_dates GROUP BY service_id, date HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_route_id', 0, COUNT(*) FROM (
        SELECT route_id FROM raw.routes GROUP BY route_id HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_shape_sequence', 0, COUNT(*) FROM (
        SELECT shape_id, shape_pt_sequence FROM raw.shapes GROUP BY shape_id, shape_pt_sequence HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_stop_time_sequence', 0, COUNT(*) FROM (
        SELECT trip_id, stop_sequence FROM raw.stop_times GROUP BY trip_id, stop_sequence HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_stop_id', 0, COUNT(*) FROM (
        SELECT stop_id FROM raw.stops GROUP BY stop_id HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'duplicate_trip_id', 0, COUNT(*) FROM (
        SELECT trip_id FROM raw.trips GROUP BY trip_id HAVING COUNT(*) > 1
    )
    UNION ALL SELECT 'orphan_route_agency', 0, COUNT(*)
      FROM raw.routes r LEFT JOIN raw.agency a ON r.agency_id = a.agency_id
     WHERE NULLIF(r.agency_id, '') IS NOT NULL AND a.agency_id IS NULL
    UNION ALL SELECT 'orphan_trip_route', 0, COUNT(*)
      FROM raw.trips t LEFT JOIN raw.routes r ON t.route_id = r.route_id
     WHERE r.route_id IS NULL
    UNION ALL SELECT 'orphan_trip_service', 0, COUNT(*)
      FROM raw.trips t
      LEFT JOIN (SELECT DISTINCT service_id FROM raw.calendar_dates) c
        ON t.service_id = c.service_id
     WHERE c.service_id IS NULL
    UNION ALL SELECT 'orphan_stop_time_trip', 0, COUNT(*)
      FROM raw.stop_times st LEFT JOIN raw.trips t ON st.trip_id = t.trip_id
     WHERE t.trip_id IS NULL
    UNION ALL SELECT 'orphan_stop_time_stop', 0, COUNT(*)
      FROM raw.stop_times st LEFT JOIN raw.stops s ON st.stop_id = s.stop_id
     WHERE s.stop_id IS NULL
    UNION ALL SELECT 'orphan_trip_shape', 0, COUNT(*)
      FROM raw.trips t
      LEFT JOIN (SELECT DISTINCT shape_id FROM raw.shapes) s ON t.shape_id = s.shape_id
     WHERE NULLIF(t.shape_id, '') IS NOT NULL AND s.shape_id IS NULL
    UNION ALL SELECT 'invalid_stop_coordinates', 0, COUNT(*)
      FROM raw.stops
     WHERE try_cast(stop_lat AS DOUBLE) NOT BETWEEN -90 AND 90
        OR try_cast(stop_lon AS DOUBLE) NOT BETWEEN -180 AND 180
        OR try_cast(stop_lat AS DOUBLE) IS NULL
        OR try_cast(stop_lon AS DOUBLE) IS NULL
    UNION ALL SELECT 'invalid_shape_coordinates', 0, COUNT(*)
      FROM raw.shapes
     WHERE try_cast(shape_pt_lat AS DOUBLE) NOT BETWEEN -90 AND 90
        OR try_cast(shape_pt_lon AS DOUBLE) NOT BETWEEN -180 AND 180
        OR try_cast(shape_pt_lat AS DOUBLE) IS NULL
        OR try_cast(shape_pt_lon AS DOUBLE) IS NULL
    UNION ALL SELECT 'invalid_shape_pt_sequence', 0, COUNT(*)
      FROM raw.shapes
     WHERE try_cast(shape_pt_sequence AS BIGINT) IS NULL
        OR try_cast(shape_pt_sequence AS BIGINT) < 0
    UNION ALL SELECT 'invalid_stop_sequence', 0, COUNT(*)
      FROM raw.stop_times
     WHERE try_cast(stop_sequence AS BIGINT) IS NULL
        OR try_cast(stop_sequence AS BIGINT) < 0
    UNION ALL SELECT 'invalid_arrival_or_departure_format', 0, COUNT(*)
      FROM raw.stop_times
     WHERE NOT regexp_matches(arrival_time, '^[0-9]{1,3}:[0-5][0-9]:[0-5][0-9]$')
        OR NOT regexp_matches(departure_time, '^[0-9]{1,3}:[0-5][0-9]:[0-5][0-9]$')
)
SELECT
    'DATA_INTEGRITY' check_family,
    check_name,
    expected,
    actual,
    CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END status
FROM checks
ORDER BY check_name;

-- 4. Sequence monotonicity after numeric ordering.
WITH shape_sequence AS (
    SELECT
        shape_id,
        try_cast(shape_pt_sequence AS BIGINT) sequence_value,
        lag(try_cast(shape_pt_sequence AS BIGINT)) OVER (
            PARTITION BY shape_id ORDER BY try_cast(shape_pt_sequence AS BIGINT)
        ) previous_value
    FROM raw.shapes
),
stop_sequence AS (
    SELECT
        trip_id,
        try_cast(stop_sequence AS BIGINT) sequence_value,
        lag(try_cast(stop_sequence AS BIGINT)) OVER (
            PARTITION BY trip_id ORDER BY try_cast(stop_sequence AS BIGINT)
        ) previous_value
    FROM raw.stop_times
),
checks(check_name, expected, actual) AS (
    SELECT 'non_increasing_shape_pt_sequence', 0, COUNT(*)
      FROM shape_sequence
     WHERE previous_value IS NOT NULL AND sequence_value <= previous_value
    UNION ALL
    SELECT 'non_increasing_stop_sequence', 0, COUNT(*)
      FROM stop_sequence
     WHERE previous_value IS NOT NULL AND sequence_value <= previous_value
)
SELECT
    'MONOTONICITY' check_family,
    check_name,
    expected,
    actual,
    CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END status
FROM checks
ORDER BY check_name;

-- 5. GTFS operational-time preservation. Values at/after 24:00:00 are valid.
SELECT
    'TIME_SEMANTICS' check_family,
    'times_at_or_after_24h_preserved_as_varchar' check_name,
    '>0 VARCHAR rows' expected,
    concat(COUNT(*), ' rows; max arrival hour=', max(try_cast(split_part(arrival_time, ':', 1) AS INTEGER)),
           '; max departure hour=', max(try_cast(split_part(departure_time, ':', 1) AS INTEGER))) actual,
    CASE
        WHEN COUNT(*) > 0
         AND (SELECT data_type FROM information_schema.columns
               WHERE table_schema = 'raw' AND table_name = 'stop_times' AND column_name = 'arrival_time') = 'VARCHAR'
         AND (SELECT data_type FROM information_schema.columns
               WHERE table_schema = 'raw' AND table_name = 'stop_times' AND column_name = 'departure_time') = 'VARCHAR'
        THEN 'PASS' ELSE 'FAIL'
    END status
FROM raw.stop_times
WHERE try_cast(split_part(arrival_time, ':', 1) AS INTEGER) >= 24
   OR try_cast(split_part(departure_time, ':', 1) AS INTEGER) >= 24;

-- 6. Route 440 and the duplicate main.stops snapshot.
WITH checks(check_name, expected, actual) AS (
    SELECT 'route_440_route_rows', 1, COUNT(*) FROM raw.routes WHERE route_id = '440'
    UNION ALL SELECT 'route_440_trip_rows', 2, COUNT(*) FROM raw.trips WHERE route_id = '440'
    UNION ALL SELECT 'route_440_distinct_shapes', 2, COUNT(DISTINCT shape_id) FROM raw.trips WHERE route_id = '440'
    UNION ALL SELECT 'route_440_shape_points', 814, COUNT(*)
      FROM raw.shapes WHERE shape_id IN (SELECT shape_id FROM raw.trips WHERE route_id = '440')
    UNION ALL SELECT 'main_stops_minus_raw', 0, COUNT(*)
      FROM (SELECT * FROM main.stops EXCEPT SELECT * FROM raw.stops)
    UNION ALL SELECT 'raw_stops_minus_main', 0, COUNT(*)
      FROM (SELECT * FROM raw.stops EXCEPT SELECT * FROM main.stops)
)
SELECT
    'KNOWN_ARTIFACTS' check_family,
    check_name,
    expected,
    actual,
    CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END status
FROM checks
ORDER BY check_name;

