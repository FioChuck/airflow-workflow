import uuid
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
    DataprocListBatchesOperator
)

PROJECT_ID = "cf-data-analytics"
REGION = "us-central1"
BASE_BATCH_ID = "demo-serverless-batch"

default_args = {
    "project_id": PROJECT_ID,
    "region": REGION,
}
with models.DAG(
        dag_id="dataproc_serverless",
        default_args=default_args,
        schedule=None
) as dag:
    unique_batch_id = BASE_BATCH_ID + "-" + str(uuid.uuid4())

    create_batch = DataprocCreateBatchOperator(
        task_id="batch_create",
        batch={
            "spark_batch": {
                "main_jar_file_uri": "gs://cf-spark-jobs/jars/ServerlessSpark-3.0.0-jar-with-dependencies.jar"
            },
            "runtime_config": {
                "version": "2.2",
            }
        },
        batch_id=unique_batch_id,
        deferrable=True
    )

    list_batches = DataprocListBatchesOperator(
        task_id="list-all-batches",
    )

    create_batch >> list_batches

if __name__ == "__main__":
    dag.cli()
    # dag.test()
