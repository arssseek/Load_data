CREATE TABLE weather_tab(
	id SERIAL PRIMARY KEY,
	city varchar NULL,
	dt date NULL,
	hour int2 NULL,
	temperature_c float8 NULL,
	pressure float8 NULL,
	is_rainy int null
);
create table metric_tab(
	metric_id serial primary key,
	discription_metric varchar not null
);
create table city_tab(
		city_id serial primary key,
		discription_city varchar not null
);
create table result_tab(
	metric_id int4 not null,
	city_id int4 not null,
	value float8,
	time timestamp not null,
	constraint metric_con
		foreign key (metric_id)
			references metric_tab(metric_id),
	constraint city_con
		foreign key (city_id)
			references city_tab(city_id)
);

