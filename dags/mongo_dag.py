from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from pymongo import MongoClient
import logging
import pandas as pd
from airflow.providers.mongo.hooks.mongo import MongoHook

def get_data():
    mongo_uri = 'mongodb://airflow:airflow@host.docker.local:27017/test'
    db_name = 'test'
    collection_name = 'employees'

    # Подключение к MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Чтение данных из MongoDB
    data = collection.find()
    keys = ['email', 'inactive', 'login', 'name']
    values_dict = {key: [] for key in keys}
    for doc in data:
        logging.info(f"columns: {doc}")

    # hook = MongoHook(mongo_conn_id='mongo_conn')
    # client = hook.get_conn()
    # collection = hook.get_collection(mongo_collection='employees', mongo_db='test')
    #
    # client = MongoClient('mongodb://airflow:airflow@host.docker.local:27017/test')
    # current = client["test"]
    # collection = current["employees"]
    # keys = ['email', 'inactive', 'login', 'name']
    # values_dict = {key: [] for key in keys}
    # for doc in collection.find():
    #     values_dict[keys[0]].append(doc.get('email'))
    #     values_dict[keys[1]].append(doc.get('inactive'))
    #     values_dict[keys[2]].append(doc.get('login'))
    #     values_dict[keys[3]].append(doc.get('name'))
    # df = pd.DataFrame(values_dict)
    #
    # # logging.info(f"values: {collections.find_one()}")
    # values = "VALUES({})".format(",".join(["%s" for _ in keys]))
    # pConn = PostgresHook(postgres_conn_id='postgres_localhost').get_conn()
    # pCursor = pConn.cursor()
    #
    #
    # logging.info(f"columns: {keys}")
    #
    # logging.info(f"values: {values}")
    #
    # insert_stmt = "INSERT INTO {} ({}) {}".format(table_name, keys, values)
    # logging.info(f"values: {insert_stmt}")
    #
    # psycopg2.extras.execute_batch(pCursor, insert_stmt, df.values)
    #
    # pCursor.close()
    # pConn.commit()
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