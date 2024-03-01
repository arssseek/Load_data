from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.mongo_hook import MongoHook


# Define function to load data from MongoDB to PostgreSQL
def load_data_mongodb_to_postgres():
    mongo_hook = MongoHook(conn_id='mongo_connection')
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connection', schema='public')

    # Fetch data from MongoDB collection
    mongo_data = mongo_hook.find('mongo_collection', {})

    # Load data into PostgreSQL table
    postgres_conn = postgres_hook.get_conn()
    cursor = postgres_conn.cursor()

    for data in mongo_data:
        cursor.execute("INSERT INTO postgres_table VALUES (%s, %s)", (data['column1'], data['column2']))

    cursor.close()
    postgres_conn.commit()
    postgres_conn.close()


# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
}

dag = DAG(
    'mongodb_to_postgres',
    default_args=default_args,
    description='DAG to load data from MongoDB to PostgreSQL',
    schedule_interval='@daily',
    catchup=False
)

# Define the task
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data_mongodb_to_postgres,
    dag=dag,
)

# Define task dependencies
load_data_task