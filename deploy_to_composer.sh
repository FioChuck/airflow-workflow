#!/bin/bash
set -e

for dag in dags/*.py; do
  gcloud composer environments storage dags import \
    --project="cf-data-analytics" \
    --environment="etl-orchestration" \
    --location="us-central1" \
    --source="$dag"
done
