from airflow import DAG
from airflow.decorators import task
from pyfiglet import Figlet
from datetime import datetime


@task
def generate_text_list():

    text_list = ["Atlanta", "Chicago", 404, "Seattle"]
    return text_list


@task
def generate_figlet_text(text):

    f = Figlet(font="slant")
    print("\n" + f.renderText(str(text)))


with DAG(
    dag_id="figlet_dag",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    tags=["gcp demo"],
) as dag:

    texts = generate_text_list()

    python_task = generate_figlet_text.expand(text=texts)

if __name__ == "__main__":
    dag.cli()
