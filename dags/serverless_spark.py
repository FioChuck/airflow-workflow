import uuid
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
    dag_id="dataproc_serverless_trigger", default_args=default_args, schedule=None
) as dag:
    unique_batch_id = "demo-serverless-batch-" + str(uuid.uuid4())

    create_batch = DataprocCreateBatchOperator(
        task_id="batch_create",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": PYTHON_FILE_LOCATION,
                "args": ["--gcs_path=" + GCS_DESTINATION],
            },
            "environment_config": {
                "peripherals_config": {
                    "spark_history_server_config": {},
                },
            },
        },
        batch_id=unique_batch_id,
        deferrable=True,
    )

    list_batches = DataprocListBatchesOperator(
        task_id="list-all-batches",
    )

    create_batch >> list_batches

if __name__ == "__main__":
    dag.cli()
    # dag.test()
