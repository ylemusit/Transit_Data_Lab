-- GTFS_Lab V1 analysis query pack; execute against a run-local DuckDB.
-- Source tables are raw.* and all source values remain VARCHAR.

-- Q01 agencies
SELECT * FROM raw.agency ORDER BY agency_id;

-- Q02 routes by agency
SELECT agency_id, route_id, route_short_name, route_long_name, route_type
FROM raw.routes ORDER BY agency_id, route_id;

-- Q03 stops served by route
SELECT DISTINCT t.route_id, st.stop_id, s.stop_name
FROM raw.trips t JOIN raw.stop_times st USING (trip_id)
LEFT JOIN raw.stops s USING (stop_id)
ORDER BY t.route_id, st.stop_id;

-- Q04 trip counts by route and direction
SELECT route_id, direction_id, COUNT(*) AS trip_count
FROM raw.trips GROUP BY route_id, direction_id ORDER BY route_id, direction_id;

-- Q05 shared stops across routes
WITH route_stops AS (
  SELECT DISTINCT t.route_id, st.stop_id
  FROM raw.trips t JOIN raw.stop_times st USING (trip_id)
)
SELECT stop_id, COUNT(DISTINCT route_id) AS route_count,
       string_agg(DISTINCT route_id, ', ' ORDER BY route_id) AS route_ids
FROM route_stops GROUP BY stop_id HAVING COUNT(DISTINCT route_id) > 1
ORDER BY route_count DESC, stop_id;

-- Q06 shape inventory
SELECT shape_id, COUNT(*) AS point_count,
       MIN(try_cast(shape_pt_sequence AS BIGINT)) AS first_sequence,
       MAX(try_cast(shape_pt_sequence AS BIGINT)) AS last_sequence
FROM raw.shapes GROUP BY shape_id ORDER BY shape_id;

-- Q07 service inventory (calendar dates also valid as the only calendar source)
SELECT service_id, COUNT(*) AS exception_rows
FROM raw.calendar_dates GROUP BY service_id ORDER BY service_id;

-- Q08 route-stop matrix
SELECT t.route_id, st.stop_id, COUNT(*) AS stop_time_rows
FROM raw.trips t JOIN raw.stop_times st USING (trip_id)
GROUP BY t.route_id, st.stop_id ORDER BY t.route_id, st.stop_id;
