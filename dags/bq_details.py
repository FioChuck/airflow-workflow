from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryGetDatasetOperator,
    BigQueryGetDatasetTablesOperator,
)
from airflow.utils.dates import days_ago

DATASET_NAME = "market_data"

with DAG(
    dag_id="bq_list_tables",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["gcp demo"],
) as dag:
    get_dataset = BigQueryGetDatasetOperator(
        task_id="get_dataset", dataset_id=DATASET_NAME
    )

    get_dataset_tables = BigQueryGetDatasetTablesOperator(
        task_id="get_dataset_tables", dataset_id=DATASET_NAME
    )

    get_dataset >> get_dataset_tables

if __name__ == "__main__":
    dag.cli()
