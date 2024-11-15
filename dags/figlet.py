from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pyfiglet import Figlet


def generate_figlet_text():
    f = Figlet(font="slant")
    print("\n" + f.renderText("HELLO DR. HALEY"))


with DAG(
    dag_id="figlet_dag",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["gcp demo"],  
) as dag:

    python_task = PythonOperator(
        task_id="generate_figlet",
        python_callable=generate_figlet_text,
    )

    python_task

if __name__ == "__main__":
    dag.cli()
