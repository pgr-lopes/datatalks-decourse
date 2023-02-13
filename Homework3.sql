--Data preparation. Ran Web to GCS modified script ("etl_web_to_gcs_csv.py" in the homework for week 3 folder) to load csv fhv dataset files into GCS bucket and create external tables from here:

CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.fhv_tripdata_external_csv`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_high-electron-375823/data/fhv/fhv_tripdata_2019-*.csv']
);


-- Question 1:
SELECT count(*) FROM `trips_data_all.fhv_tripdata_external_csv`;

-- Question 2:
CREATE OR REPLACE TABLE `trips_data_all.fhv_tripdata_nonpartitioned`
AS SELECT * FROM `trips_data_all.fhv_tripdata_external_csv`;

SELECT COUNT(DISTINCT(Affiliated_base_number)) FROM `trips_data_all.fhv_tripdata_external_csv`; -- processed 3.03GB
SELECT COUNT (DISTINCT(Affiliated_base_number)) FROM `trips_data_all.fhv_tripdata_nonpartitioned`; -- processed 336.71MB

-- Question 3:
select count(*) from `trips_data_all.fhv_tripdata_nonpartitioned` where DOlocationID IS NULL and PUlocationID IS NULL


-- Question 5:
CREATE OR REPLACE TABLE `trips_data_all.fhv_partitioned_tripdata`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS (
  SELECT * FROM `trips_data_all.fhv_tripdata_external_csv`
);

select distinct (Affiliated_base_number) from `trips_data_all.fhv_partitioned_tripdata`
where DATE(pickup_datetime) between '2019-03-01' and '2019-03-31'

select distinct (Affiliated_base_number) from `trips_data_all.fhv_tripdata_nonpartitioned`
where DATE(pickup_datetime) between '2019-03-01' and '2019-03-31'

-- Question 8:

-- Create the external table from parquet data. Parquet data was loaded into GCS via prefect flow "etl_web_to_gcs_parquet.py" file added to the github repo folder
CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.fhv_tripdata_external_parquet`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_high-electron-375823/data/fhv/fhv_tripdata_2019-*.parquet']
);

CREATE OR REPLACE TABLE `trips_data_all.fhv_tripdata_parquet`
AS SELECT * FROM `trips_data_all.fhv_tripdata_external_parquet`;

select * from `trips_data_all.fhv_tripdata_parquet` where DOlocationID IS NULL or PUlocationID IS NULL
