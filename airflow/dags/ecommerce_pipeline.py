from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ecommerce_pipeline",
    schedule=None,
    catchup=False,
    start_date=datetime(2024, 1, 1),
    tags=["ecommerce"],
) as dag:
    ingest_raw_orders = BashOperator(
        task_id="ingest_raw_orders",
        bash_command="python ingestion/load_raw.py",
        cwd="/opt/airflow/project",
    )

    build_star_schema = BashOperator(
        task_id="build_star_schema",
        bash_command="python transformation/build_star_schema.py",
        cwd="/opt/airflow/project",
    )

    ingest_raw_orders >> build_star_schema
