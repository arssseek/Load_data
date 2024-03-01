SELECT city, dt, hour,
avg(temperature_c) over (partition by city order by dt, hour rows between current row and 48 following) as avg_temp_for_last_two_days,
avg(pressure) over (partition by city order by dt, hour rows between current row and 48 following) as avg_press_for_last_two_days
FROM weather_tab
