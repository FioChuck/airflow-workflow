from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator


args = {"owner": "packt-developer"}

query = f"""
    CREATE OR REPLACE TABLE
    `cf-data-analytics.market_data.googl_daily_bar` AS
    WITH
    daily_bar AS (
    SELECT
        symbol,
        prevDailyBar.c AS price,
        EXTRACT(DATE
        FROM
        PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', prevdailyBar.t)) current_dt
    FROM
        `cf-data-analytics.market_data.googl`)
    SELECT
    symbol,
    current_dt as dt,
    ARRAY_AGG(price
    ORDER BY
        price DESC) [
    OFFSET
    (0)] AS closing_price,
    FROM
    daily_bar
    GROUP BY
    symbol,
    dt
    ORDER BY current_dt DESC;
"""

with DAG(
    dag_id="bq_ctas",
    default_args=args,
    schedule=None,
    max_active_runs=1,
    is_paused_upon_creation=False,
    tags=["gcp demo"],
) as dag:

    ctas_query = BigQueryInsertJobOperator(
        task_id="aggregation_query",
        configuration={"query": {"query": query, "useLegacySql": False}},
    )

    ctas_query


if __name__ == "__main__":
    dag.cli()
