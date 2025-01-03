from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


dag = DAG(
    "ten_minute_dag",
    description="KubernetesPodOperator Example",
    schedule=None,
)


def run_for_ten_min():
    print(f"DAG started at {datetime.now().strftime('%T')}")
    time.sleep(600)
    print(f"DAG finished at {datetime.now().strftime('%T')}")


ten_min_task = PythonOperator(
    task_id="ten_min_task",
    python_callable=run_for_ten_min,
    dag=dag,
    queue="kubernetes",
)

end_task = BashOperator(
    task_id="end_task",
    bash_command='echo "DAG finished at $(date +"%T")"',
    dag=dag,
    queue="kubernetes",
)

ten_min_task >> end_task
