from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import shutil
import random

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG( 
    'data_ingestion_simple',
    default_args=default_args,
    description='A simplified DAG to move data',
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)

def read_data(**kwargs):
    raw_data_folder = '/opt/airflow/data_ingestion_folder/raw_folder'
    files = [file for file in os.listdir(raw_data_folder) if file.endswith('.csv')]
    random_file = random.choice(files)
    selected_file_path = os.path.join(raw_data_folder, random_file)
    
    kwargs['ti'].xcom_push(key='file_path', value=selected_file_path)

def save_file(**kwargs):
    ti = kwargs['ti']
    file_path = ti.xcom_pull(key='file_path', task_ids='read_data')
    good_data_folder = '/opt/airflow/data_ingestion_folder/good_data'
    
    if not os.path.exists(good_data_folder):
        os.makedirs(good_data_folder)
    shutil.move(file_path, os.path.join(good_data_folder, os.path.basename(file_path)))

read_data_task = PythonOperator(
    task_id='read_data',
    python_callable=read_data,
    provide_context=True,
    dag=dag,
)

save_file_task = PythonOperator(
    task_id='save_file',
    python_callable=save_file,
    provide_context=True,
    dag=dag,
)

read_data_task >> save_file_task
