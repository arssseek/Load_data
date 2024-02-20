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
	)