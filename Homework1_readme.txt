1. docker build --help

2. 	docker exec -it [container_name] bash
	pip list
	
3. select count(1) from green_taxi_data where lpep_pickup_datetime >= '2019-01-15' and lpep_pickup_datetime < '2019-01-16'
Alternative: select count(1) from green_taxi_data where date(lpep_pickup_datetime)='2019-01-01'

4. select lpep_pickup_datetime, trip_distance from green_taxi_data where lpep_pickup_datetime >= '2019-01-15' and lpep_pickup_datetime < '2019-01-16' order by trip_distance DESC limit 10
Technically you would only need to do limit 1, but I wanted to confirm the values I was getting made sense against each other

5. 	2 passengers: select count(1) from green_taxi_data where passenger_count = 2 and date(lpep_pickup_datetime)='2019-01-01'
	3 passengers: select count(1) from green_taxi_data where passenger_count = 3 and date(lpep_pickup_datetime)='2019-01-01'

6. 

select green_taxi_data."PULocationID", green_taxi_data."DOLocationID", green_taxi_data.ti
p_amount, taxi_zones."Zone" from green_taxi_data inner join taxi_zones on green_taxi_data."PULocationID" = taxi_zones.
"LocationID" and taxi_zones."Zone" like 'Astoria%' order by tip_amount desc limit 10
 
select "Zone" from taxi_zones where "LocationID" = 146
