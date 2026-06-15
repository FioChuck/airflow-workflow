import uuid
from airflow.utils.task_group import TaskGroup
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
    DataprocListBatchesOperator,
)


PROJECT_ID = "cf-data-analytics"
REGION = "us-central1"
BASE_BATCH_ID = "demo-serverless-batch"
PYTHON_FILE_LOCATION = "gs://cf-spark-jobs/serverless_demo.py"
GCS_DESTINATION = "gs://cf-spark-external/wiki_aggregated"

default_args = {
    "project_id": PROJECT_ID,
    "region": REGION,
}
with models.DAG(
    dag_id="dataproc_serverless", default_args=default_args, schedule=None
) as dag:

    with TaskGroup("example_taskgroup", tooltip="task group #1") as section_1:
        create_batch_1 = DataprocCreateBatchOperator(
            task_id="query_1",
            batch={
                "pyspark_batch": {
                    "main_python_file_uri": PYTHON_FILE_LOCATION,
                    "args": ["--gcs_path=" + GCS_DESTINATION + "_1"],
                },
                "environment_config": {
                    "peripherals_config": {
                        "spark_history_server_config": {},
                    },
                },
            },
            batch_id="demo-serverless-batch-" + str(uuid.uuid4()),
            deferrable=True,
        )

        create_batch_2 = DataprocCreateBatchOperator(
            task_id="query_2",
            batch={
                "pyspark_batch": {
                    "main_python_file_uri": PYTHON_FILE_LOCATION,
                    "args": ["--gcs_path=" + GCS_DESTINATION + "_2"],
                },
                "environment_config": {
                    "peripherals_config": {
                        "spark_history_server_config": {},
                    },
                },
            },
            batch_id="demo-serverless-batch-" + str(uuid.uuid4()),
            deferrable=True,
        )

        create_batch_3 = DataprocCreateBatchOperator(
            task_id="query_3",
            batch={
                "pyspark_batch": {
                    "main_python_file_uri": PYTHON_FILE_LOCATION,
                    "args": ["--gcs_path=" + GCS_DESTINATION + "_3"],
                },
                "environment_config": {
                    "peripherals_config": {
                        "spark_history_server_config": {},
                    },
                },
            },
            batch_id="demo-serverless-batch-" + str(uuid.uuid4()),
            deferrable=True,
        )

    list_batches = DataprocListBatchesOperator(
        task_id="list-all-batches",
    )

section_1 >> list_batches

if __name__ == "__main__":
    dag.cli()
    # dag.test()
