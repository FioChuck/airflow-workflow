from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryGetDatasetOperator,
    BigQueryGetDatasetTablesOperator,
)
from airflow.operators.python import PythonOperator


DATASET_NAME = "market_data"


def print_tables(**kwargs):
    ti = kwargs["ti"]
    tables = ti.xcom_pull(task_ids="get_dataset_tables")
    print("Tables in dataset {}:".format(DATASET_NAME))
    for table in tables:
        print(table)


with DAG(
    dag_id="bq_list_tables",
    schedule=None,
    tags=["gcp demo"],
) as dag:

    get_dataset = BigQueryGetDatasetOperator(
        task_id="get_dataset", dataset_id=DATASET_NAME
    )

    get_dataset_tables = BigQueryGetDatasetTablesOperator(
        task_id="get_dataset_tables", dataset_id=DATASET_NAME
    )

    print_tables = PythonOperator(task_id="print_tables", python_callable=print_tables)

    get_dataset >> get_dataset_tables >> print_tables


if __name__ == "__main__":
    dag.cli()
    # dag.test()
