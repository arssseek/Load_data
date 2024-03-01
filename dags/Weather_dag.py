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


pd_city = []
pd_date = []
pd_time = []
temperature_c = []
is_rainy = []
pressure = []
file_name = 'weather.csv'
city_coordinats = {
    'Moscow':(55.7522, 37.6155),
    'SaintPetersburg' : (59.939, 30.316),
    'Novosibirsk' : (55.03, 82.96),
    'Kazan' : (55.7499, 49.1263),
    'Tula' : (54.2048, 37.6185)
}
TABLE_NAME = 'weather_tab'
API_KEY = "65f14802-4c56-441c-ad2d-a6367e43a6e5"
URL = 'https://api.weather.yandex.ru/v2/forecast'
headers = {
    'X-Yandex-API-Key': API_KEY
}
def get_weather():
    for city in city_coordinats.keys():
        params = {
            'lat': city_coordinats[city][0],
            'lon': city_coordinats[city][-1],
            'lang': 'ru_RU',
            'limit': 7,
            'hours': True,
            'extra': True
        }
        response = req.get(URL, params=params, headers=headers)
        weather_data = response.json()
        for i in range(len(weather_data['forecasts'])):
            for j in range(len(weather_data['forecasts'][i]['hours'])):
                pd_city.append(weather_data['geo_object']['locality']['name'])
                pd_date.append(weather_data['forecasts'][i]['date'])
                pd_time.append(weather_data['forecasts'][i]['hours'][j]['hour'])
                temperature_c.append(weather_data['forecasts'][i]['hours'][j]['temp'])
                is_rainy.append(int(weather_data['forecasts'][i]['hours'][j]['prec_strength'] + 0.75))
                pressure.append(weather_data['forecasts'][i]['hours'][j]['pressure_mm'])
        print(pd_city)
    CSV_DATA = pd.DataFrame({
        'City': pd_city,
        'dt': pd_date,
        'hour': pd_time,
        'temperature_c': temperature_c,
        'pressure': pressure,
        'is_rainy': is_rainy
    })
    print(pd_city)
    print(CSV_DATA)
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass
    print(CSV_DATA)
    CSV_DATA.to_csv(file_name, index=False, index_label=False)


def csv_db():
    print(os.getcwd())
    pConn = PostgresHook(postgres_conn_id='postgres_localhost').get_conn()
    pCursor = pConn.cursor()

    #reading file
    f = open('weather.csv', encoding="utf8")
    file_data = f.readlines()


    columns = file_data[0].replace("\n", "")
    logging.info(f"columns: {columns}")
    #remove header from file for parsing rows
    file_data.pop(0)

    #creare dict like dataframe
    values_dict = {column: [] for column in columns}
    for row in file_data:
        for i, value in enumerate(row.replace("\n", "").split(sep=','), 1):
            values_dict[columns[i - 1]].append(value)

    # create (col1,col2,...)
    logging.info(f"columns: {columns}")

    # create VALUES('%s', '%s",...) one '%s' per column
    value = "VALUES({})".format(",".join(["%s" for _ in columns.split(sep=',')]))
    logging.info(f"values: {value}")

    # create INSERT INTO table (columns) VALUES('%s',...)
    insert_stmt = "INSERT INTO {} ({}) {}".format(TABLE_NAME, columns, value)
    logging.info(f"type values: {type(values_dict)}")
    logging.info(f"type insert_stmt: {type(insert_stmt)}")

    psycopg2.extras.execute_batch(pCursor, insert_stmt, values_dict)

    pCursor.close()
    pConn.commit()
args = {
    'owner': 'airflow',
    'retries': 0,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

weather_dag = DAG(
    dag_id='1No_Pandas_Weather_DAG',
    default_args=args,
    schedule_interval="1/5 * * * *",
    start_date=days_ago(0,0,0,0,0)

)
get_weather_from_api = PythonOperator(
    python_callable=get_weather,
    task_id='get_weather',
    dag=weather_dag
)

data_to_db = PythonOperator(
    task_id='data_to_db',
    python_callable=csv_db,
    dag=weather_dag
)

select_opera = PostgresOperator(
    task_id='select_opera',
    postgres_conn_id='postgres_localhost',
    sql="""
        SELECT * FROM weather_tab""",
    dag=weather_dag
)

get_weather_from_api >> data_to_db >> select_opera