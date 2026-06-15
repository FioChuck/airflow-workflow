#!/bin/bash
set -e 

sleep 10

echo "--- Initializing Airflow Database ---"
airflow db migrate

exec "$@"