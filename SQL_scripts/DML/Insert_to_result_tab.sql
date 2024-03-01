with start_data as(
	select city, dt, is_rainy,
	min(hour) as start_hour
	from weather_tab 
	group by city,dt, is_rainy
	having is_rainy = 1), 
	end_data as(
	select city,dt,min(hour) as end_hour from weather_tab
	where hour > (
		select start_hour 
		from start_data
		where (weather_tab.city = start_data.city and weather_tab.dt = start_data.dt)
	)
	group by city, dt, is_rainy
	having is_rainy = 0),
	rain_time as(
	select start_data.city, start_data.dt, start_hour, end_hour
	from start_data
	left join end_data 
	on (start_data.city = end_data.city and start_data.dt = end_data.dt)
	order by city,dt
	),avg_data as( 
	SELECT city, dt, hour,
	avg(temperature_c) over (partition by city order by dt, hour rows between current row and 48 following) as avg_temp,
	avg(pressure) over (partition by city order by dt, hour rows between current row and 48 following) as avg_press
	FROM weather_tab
	), metric_data as(
	select avg_data.city, avg_data.dt, avg_data.hour, avg_data.avg_temp,
		avg_data.avg_press, rain_time.start_hour, rain_time.end_hour 
	from avg_data
	left join rain_time on (avg_data.city = rain_time.city and avg_data.dt = rain_time.dt)
	), c1 as (
	select 1 as metric_id, (dt + hour * interval '1 hour') as time, city_tab.city_id, avg_temp as value from metric_data
	join city_tab on metric_data.city = city_tab.discription_city),
	c2 as (
	select 2 as metric_id, (dt + hour * interval '1 hour') as time, city_tab.city_id, avg_press as value from metric_data
	join city_tab on metric_data.city = city_tab.discription_city
	), c3 as (
	select 3 as metric_id, (dt + hour * interval '1 hour') as time, city_tab.city_id, start_hour as value from metric_data
	join city_tab on metric_data.city = city_tab.discription_city),
	c4 as (
	select 4 as metric_id, (dt + hour * interval '1 hour') as time, city_tab.city_id, end_hour as value from metric_data
	join city_tab on metric_data.city = city_tab.discription_city
)
insert into result_tab (metric_id, time, city_id, value) 
select * from c1
where not exists (
	select * from result_tab r 
	where (r.metric_id = c1.metric_id and r.time = c1.time and r.city_id = c1.city_id)); 
------------------------------------------------------------------------------
insert into result_tab (metric_id, time, city_id, value) 
select * from c2
where not exists (
	select * from result_tab r 
	where (r.metric_id = c2.metric_id and r.time = c2.time and r.city_id = c2.city_id)); 
insert into result_tab (metric_id, time, city_id, value) 
------------------------------------------------------------------------------
select * from c3
where not exists (
	select * from result_tab r 
	where (r.metric_id = c3.metric_id and r.time = c3.time and r.city_id = c3.city_id));
------------------------------------------------------------------------------
insert into result_tab (metric_id, time, city_id, value) 
select * from c4
where not exists (
	select * from result_tab r 
	where (r.metric_id = c4.metric_id and r.time = c4.time and r.city_id = c4.city_id)); 
------------------------------------------------------------------------------