from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


dag = DAG(
    "one_hour_dag",
    description="A DAG that runs for exactly one hour",
    schedule_interval=None,
)


start_task = BashOperator(
    task_id="start_task",
    bash_command='echo "DAG started at $(date +"%T")" && sleep 3600',
    dag=dag,
)

end_task = BashOperator(
    task_id="end_task",
    bash_command='echo "DAG finished at $(date +"%T")"',
    dag=dag,
)

start_task >> end_task
