from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from pymongo import MongoClient
import logging

# Provide the connection details
hostname = 'localhost'
port = 27023  # Default MongoDB port
username = "Test"  # If authentication is required
password = "mongo_Test"  # If authentication is required
# Create a MongoClient instance

# Define function to load data from MongoDB to PostgreSQL
def get_data():
    client = MongoClient(hostname, port, username=username, password=password)
    current = client["Test"]
    collections = current["employees"]
    logging.info(f"values: {collections.find_one()}")
def load_data_mongodb_to_postgres():
    pass


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
    python_callable=load_data_mongodb_to_postgres,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data_mongodb_to_postgres,
    dag=dag,
)

# Define task dependencies
get_data >> load_data