from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

with DAG(
    dag_id = "s3_to_postgres",
    default_args={
            'owner': 'airflow',
            'depends_on_past': False,
            'start_date': days_ago(1),
            'retries': 1,
        },
    description='DAG to get data from S3 and upload it postgres warehouse',
    schedule_interval='@daily',
    catchup=False,
    tags=['s3-to-visualization']
) as dag:
    
    #tasks
    start = EmptyOperator(task_id="Start", dag=dag)
    end = EmptyOperator(task_id="End", dag=dag)

    activate_env = BashOperator(task_id="ActivateENV", dag = dag, bash_command="source /opt/airflow/s3toviz_env/bin/activate")

    extract_task = BashOperator(task_id="Extract", dag=dag, bash_command = "python3 /opt/airflow/scripts/extract.py" )

    load_task = BashOperator(task_id="Load", dag=dag, bash_command = "python3 /opt/airflow/scripts/load.py" )
    
    start >> activate_env >> extract_task >> load_task >> end


