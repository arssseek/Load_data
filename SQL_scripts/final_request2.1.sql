/*create table metric(
	metric_id serial primary key,
	city varchar,
	dt date,
	hour int2,
	avg_temp float8,
	avg_press float8,
	start_hour int2,
	end_hour int2
);*/
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
)
insert into metric(city, dt, hour,
	avg_temp, avg_press, start_hour,	end_hour)
select * from metric_data
where not exists (select * from metric);