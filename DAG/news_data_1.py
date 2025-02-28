from airflow import DAG 
from datetime import datetime, timedelta
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python_operator import PythonOperator
from lambda_function import lambda_handler

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 27),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': 'durgaprasadreddy85@gmail.com'
}

with DAG(
    dag_id='news_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Invoke Lambda Function
    invoke_lambda = PythonOperator(
        task_id='invoke_lambda',
        python_callable=lambda_handler,  
        dag=dag,
    )

    # Task 2: Check if S3 File Exists
    def s3_file_check():
        s3_hook = S3Hook(aws_conn_id='aws_default')
        file_key = 'newsdata.csv'
        bucket_name = 'newsdata-dp'

        if not s3_hook.check_for_key(file_key, bucket_name):
            raise ValueError('S3 file does not exist')

    check_s3 = PythonOperator(
        task_id='check_s3',
        python_callable=s3_file_check,
        dag=dag,
    )

    # Task 3: Create Table in Snowflake
    create_table = SnowflakeOperator(
        task_id='create_snowflake_table',
        snowflake_conn_id='snowflake_default',
        sql='/home/airflow/dags/create_table.sql',
        dag=dag,
    )

    # Task 4: Load Data into Snowflake
    load_data = SnowflakeOperator(
        task_id='load_data_into_snowflake',
        snowflake_conn_id='snowflake_default',
        sql='/home/airflow/dags/load_data.sql',
        dag=dag,
    )

    # Task 5: Send Success Email
    success_email = EmailOperator(
        task_id='success_email',
        to='durgaprasadreddy85@gmail.com',
        subject='News Data Pipeline Success',
        html_content='The News Data Pipeline has successfully completed.',
        dag=dag,
    )

    # Task Dependencies
    invoke_lambda >> check_s3 >> create_table >> load_data >> success_email
