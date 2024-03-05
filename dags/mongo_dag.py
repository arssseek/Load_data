from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from pymongo import MongoClient
import logging
import pandas as pd


def get_data():
    hostname = 'localhost'
    port = 27023
    username = "Test"
    password = "mongo_Test"
    table_name = "employees"

    client = MongoClient(hostname, port, username=username, password=password)
    current = client["Test"]
    collections = current["employees"]

    keys = ['email', 'inactive', 'login', 'name']
    values_dict = {key: [] for key in keys}
    for doc in collections.find():
        values_dict[keys[0]].append(doc.get('email'))
        values_dict[keys[1]].append(doc.get('inactive'))
        values_dict[keys[2]].append(doc.get('login'))
        values_dict[keys[3]].append(doc.get('name'))
    df = pd.DataFrame(values_dict)

    # logging.info(f"values: {collections.find_one()}")
    values = "VALUES({})".format(",".join(["%s" for _ in keys]))
    pConn = PostgresHook(postgres_conn_id='postgres_localhost').get_conn()
    pCursor = pConn.cursor()


    logging.info(f"columns: {keys}")

    logging.info(f"values: {values}")

    insert_stmt = "INSERT INTO {} ({}) {}".format(table_name, keys, values)
    logging.info(f"values: {insert_stmt}")

    psycopg2.extras.execute_batch(pCursor, insert_stmt, df.values)

    pCursor.close()
    pConn.commit()
# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
}

dag = DAG(
    dag_id='mongodb_to_postgres',
    default_args=default_args,
    description='DAG to load data from MongoDB to PostgreSQL',
    schedule_interval='@daily',
    catchup=False
)

# Define the task
get_data = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    dag=dag,
)


get_data