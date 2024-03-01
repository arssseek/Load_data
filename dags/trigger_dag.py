import os
import datetime as dt
import requests as req
import pandas as pd
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook
import logging
import psycopg2
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

args = {
    'owner': 'airflow',
    'retries': 0,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

trigger_dag = DAG(
    dag_id='1Trigger_dag',
    default_args=args,
    schedule_interval="1/20 * * * *",
    start_date=days_ago(0,0,0,0,0),
    catchup=False
)

trigger_task = TriggerDagRunOperator(
    task_id='trigger_task',
    trigger_dag_id='1Success_dag',
    execution_date='{{ ds }}',
    reset_dag_run=True,
    wait_for_completion=True,
    poke_interval=10,
    dag=trigger_dag
)

create_metric_tab = PostgresOperator(
    task_id='create_metric_tab',
    postgres_conn_id='postgres_localhost',
    sql="""
        CREATE TABLE IF NOT EXISTS metric_tab(
            id SERIAL PRIMARY KEY,
	        city varchar NULL,
	        dt date NULL,
	        hour int2 NULL,
	        temperature_c float8 NULL,
	        pressure float8 NULL,
	        is_rainy int NULL
    );""",
    dag=trigger_dag
)
insert_value = PostgresOperator(
    task_id='insert_value',
    postgres_conn_id='postgres_localhost',
    sql="""
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
            order by city,dt),
            avg_data as( 
                select city, dt, hour,
                avg(temperature_c) over (partition by city order by dt, hour rows between current row and 48 following) as avg_temp,
                avg(pressure) over (partition by city order by dt, hour rows between current row and 48 following) as avg_press
                FROM weather_tab
                ), 
	        metric_data as(
                select avg_data.city, avg_data.dt, avg_data.hour, avg_data.avg_temp,
                    avg_data.avg_press, rain_time.start_hour, rain_time.end_hour 
                from avg_data
                left join rain_time on (avg_data.city = rain_time.city and avg_data.dt = rain_time.dt)
            )
        insert into metric(city, dt, hour,
	        avg_temp, avg_press, start_hour,	end_hour)
        select * from metric_data
        where not exists (select * from metric);
    """,
    dag=trigger_dag
)
trigger_task >> create_metric_tab >> insert_value