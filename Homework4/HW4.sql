--Q1
SELECT count(*) FROM `high-electron-375823.trips_data_all.fact_trips` where pickup_datetime>timestamp('2019-01-01 00:00:00') and pickup_datetime<timestamp('2020-12-31 00:00:00'); --115215057

--Q3
select count(*) from `high-electron-375823.trips_data_all.stg_fhv_tripdata`

--Q4
select count(*) from `high-electron-375823.trips_data_all.fact_fhv` where pickup_datetime>timestamp('2019-01-01 00:00:00') and pickup_datetime<timestamp('2019-12-31 00:00:00');
