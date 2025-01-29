### Building the docker image for data ingest to Postgres
```bash
docker build -t taxi_ingest:v1 .
```

### Ingest taxi data to the Postgres database
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
python ingest_data.py \ 
    --user=root \ 
    --password=root \ 
    --host=localhost \ 
    --port=5432 \ 
    --db=ny_taxi \ 
    --table_name=yellow_taxi_trips \ 
    --url=${URL}
```

### We are adding some more databse for sql practice purpose
```bash
python taxi_zones_data.py
```

### To check the average data amount 
```sql
SELECT COUNT(1) FROM yellow_taxi_trips;
SELECT COUNT(1) FROM zones;
```

### Joining Location with the zones city 
```sql
SELECT * FROM yellow_taxi_trips t, zones zpu, zones zdo
WHERE t."PULocationID" = zpu."LocationID" AND t."DOLocationID" = zpu."LocationID"
LIMIT 100;
```

### Joining Yellow Taxi table with Zones Lookup table (Explicit INNER JOIN)
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM 
    yellow_taxi_trips t
JOIN 
-- or INNER JOIN but it's less used, when writing JOIN postgreSQL undranstands implicitly that we want to use an INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

### Checking for records with NULL Location IDs in the Yellow Taxi table
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM 
    yellow_taxi_trips t
WHERE
    "PULocationID" IS NULL
    OR "DOLocationID" IS NULL
LIMIT 100;
```

### Checking for Location IDs in the Zones table NOT IN the Yellow Taxi table
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM 
    yellow_taxi_trips t
WHERE
    "DOLocationID" NOT IN (SELECT "LocationID" from zones)
    OR "PULocationID" NOT IN (SELECT "LocationID" from zones)
LIMIT 100;
```

### Using LEFT, RIGHT, and OUTER JOINS when some Location IDs are not in either Tables
```sql
DELETE FROM zones WHERE "LocationID" = 142;

SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM 
    yellow_taxi_trips t
LEFT JOIN 
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM 
    yellow_taxi_trips t
RIGHT JOIN 
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM 
    yellow_taxi_trips t
OUTER JOIN 
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
### Using GROUP BY to calculate number of trips per day
```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM 
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
LIMIT 100;
```

### Using ORDER BY to order the results of your query
```sql
-- Ordering by day

SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM 
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "day" ASC
LIMIT 100;

-- Ordering by count

SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count"
FROM 
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

### Other kinds of aggregations
```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM 
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

### Grouping by multiple fields
```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    "DOLocationID",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM 
    yellow_taxi_trips t
GROUP BY
    1, 2
ORDER BY
    "day" ASC, 
    "DOLocationID" ASC
LIMIT 100;
```