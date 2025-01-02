from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


dag = DAG(
    "one_hour_dag",
    description="A DAG that runs for exactly one hour",
    schedule_interval=None,
)


def run_for_one_hour():
    print(f"DAG started at {datetime.now().strftime('%T')}")
    time.sleep(600)
    print(f"DAG finished at {datetime.now().strftime('%T')}")


one_hour_task = PythonOperator(
    task_id="one_hour_task",
    python_callable=run_for_one_hour,
    dag=dag,
    queue="kubernetes",
)

end_task = BashOperator(
    task_id="end_task",
    bash_command='echo "DAG finished at $(date +"%T")"',
    dag=dag,
)

one_hour_task >> end_task
