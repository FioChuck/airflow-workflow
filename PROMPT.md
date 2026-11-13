This project is designed to develop Airflow locally and deploy to Cloud Composer 3 in google cloud.

The GCP project is cf-data-analytics. The entire project leverages ADC and the admin@chasf.altostrat.com user.

I'm using the spark-orchestration branch to test FlexVMs w/ Dataproc operators. Please create a new DAG that creates a dataproc on GCE cluster, runs a spark job, and then deletes the cluster. The job should use runtime image to leverage [mutlizonal clusters](https://docs.cloud.google.com/managed-spark/docs/concepts/configuring-clusters/multi-zone). The job should leverage the latest image outlined [here](https://docs.cloud.google.com/managed-spark/docs/concepts/versioning/image-release-3.0).

The actual spark job should execture the spark code preloaded on the cluster. See an example from our serverless offering here:

```python
import uuid
from datetime import datetime

from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator

PROJECT_ID = "cf-data-analytics"
REGION = "us-central1"
BATCH_ID = str(uuid.uuid4())
BATCH_CONFIG = {
    "spark_batch": {
        "main_class": "org.apache.spark.examples.SparkPi",
        "jar_file_uris": ["file:///usr/lib/spark/examples/jars/spark-examples.jar"],
        "args": ["10"],
    },
}

with DAG(
    dag_id="dataproc_serverless_spark_pi",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    is_paused_upon_creation=True,
) as dag:
    submit_spark_pi = DataprocCreateBatchOperator(
        task_id="submit_spark_pi_batch",
        project_id=PROJECT_ID,
        region=REGION,
        batch_id=BATCH_ID,
        batch=BATCH_CONFIG,
    )
```

The operators used in this DAG are outlined [here](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/dataproc.html#starting-a-cluster)

- DataprocStartClusterOperator
- DataprocSubmitJobOperator
- DataprocStopClusterOperator

Looks like there is a new _"preffered"_ alias? _"ManagedSparkDeleteClusterOperator"_. Please use these preferred aliases?

The Cluster creation should leverage Flex VMs outlined [here](https://docs.cloud.google.com/managed-spark/docs/concepts/configuring-clusters/flexible-vms). 

I also want the FlexVMs to actually be used. For this, I previously ran some tests that explore machine types that commonly stock out and 