with distinct_data as (
	select distinct  city, dt, "hour", temperature_c, pressure, is_rainy
	from weather_tab
	), data_with_rain_flag as 
	(
select distinct city, is_rainy, dt, "hour", 	
	case 
		when (is_rainy = 1 and lead_rainy = 0) then 1
		else 0
		end as flag
from (
	select city, dt, "hour", temperature_c, pressure, is_rainy,
	lead(is_rainy) over (partition by city order by city, dt, "hour") as lead_rainy from distinct_data
) as data_with_rain_flag
order by city, dt, "hour"
)
select city, dt, start_hour, end_hour 
from (
	select distinct city, dt, 
	min(hour)over(partition by city,dt) as start_hour,
	min(case 
		when flag = 1 then hour
	end) over(partition by city,dt) as end_hour
	from data_with_rain_flag where is_rainy = 1) as rain_data

