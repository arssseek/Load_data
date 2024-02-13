import psycopg2
import logging
#import datetime as dt
#import requests as req
from airflow.decorators import task
import pandas as pd
from datetime import datetime, timedelta
from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
#from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook

DWH_CONN_ID = 'dwh_postgres_dest'
BUFFER_LINE_NUMBER = 10000

LOAD_CSV_FILE = '/opt/airflow/data/weather.csv'
TABLE_NAME = 'weather.city_weather_details'


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 0,
    "retry_delay": timedelta(minutes=1)
}

@task()
def load_to_db():
    pConn = PostgresHook(postgres_conn_id=DWH_CONN_ID).get_conn()
    pCursor = pConn.cursor()

    df = pd.read_csv(LOAD_CSV_FILE)
    logging.info(df.head())

    if len(df) > 0:
        df_columns = list(df)

    # create (col1,col2,...)
    columns = ", ".join(df_columns)
    logging.info(f"columns: {columns}")

    # create VALUES('%s', '%s",...) one '%s' per column
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
    logging.info(f"values: {values}")

    #create INSERT INTO table (columns) VALUES('%s',...)
    insert_stmt = "INSERT INTO {} ({}) {}".format(TABLE_NAME, columns, values)

    psycopg2.extras.execute_batch(pCursor, insert_stmt, df.values)

    pCursor.close()
    pConn.commit()


with DAG('load_to_db', tags=['test'], default_args=default_args, schedule_interval='0 3 * * *', catchup=False) as dag:
    load_to_db()
