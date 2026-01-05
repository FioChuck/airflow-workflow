
gcloud composer environments create etl-orchestration \
--location=us-central1 \
--image-version=composer-2.11.5-airflow-2.10.2 \
--environment-size=small \
--storage-bucket=gs://cf-cloud-composer-dags \
--service-account=1089470781238-compute@developer.gserviceaccount.com

gcloud composer environments storage dags import \
--environment=etl-orchestration \
--location=us-central1 \
--source=gs://cf-cloud-composer-dags/dags/serverless_spark.py