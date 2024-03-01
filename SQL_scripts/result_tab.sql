create table metric_tab(
	metric_id serial primary key,
	discription_metric varchar not null
);
insert into metric_tab (discription_metric) values ('avg_temp')
insert into metric_tab (discription_metric) values ('avg_press')
insert into metric_tab (discription_metric) values ('start_rain')
insert into metric_tab (discription_metric) values ('end_rain')
create table city_tab(
		city_id serial primary key,
		discription_city varchar not null
)
insert into city_tab (discription_city) values ('Москва')
insert into city_tab (discription_city) values ('Казань');
insert into city_tab (discription_city) values ('Санкт-Петербург');
insert into city_tab (discription_city) values ('Казань');
insert into city_tab (discription_city) values ('Тула');
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

