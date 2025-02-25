from airflow import DAG
from airflow.operators.python import PythonOperator
from pyfiglet import Figlet


def generate_figlet_text():
    f = Figlet(font="slant")
    print("\n" + f.renderText("DONT BE EVIL"))


with DAG(
    dag_id="figlet_dag",
    schedule=None,
    tags=["gcp demo"],
) as dag:

    python_task = PythonOperator(
        task_id="generate_figlet",
        python_callable=generate_figlet_text,
    )

    python_task

if __name__ == "__main__":
    dag.cli()
    # dag.test()
