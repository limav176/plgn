from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import pendulum

local_tz = pendulum.timezone("America/Sao_Paulo")

def check_business_day(**context):
    # valida se é dia útil (calendário B3 simplificado)
    pass

def extract_taxas(**context):
    execution_date = context["ds"]
    curvas = ["DI_PRE", "AJUSTE_PRE", "DI_TR"]
    for curva in curvas:
        # scraping da B3 para a data_base
        pass

def validate_raw(**context):
    pass
  # passei a funcao vazia aqui, propositalmente
def transform_to_silver(**context):
    pass
  # passei a funcao vazia aqui, propositalmente
def publish_gold(**context):
    pass
  # passei a funcao vazia aqui, propositalmente
def update_control_table(**context):
    pass
  # passei a funcao vazia aqui, propositalmente
with DAG(
    dag_id="pipeline_taxas_referenciais_b3",
    start_date=datetime(2015, 1, 1, tzinfo=local_tz),
    schedule="0 20 * * 1-5",
    catchup=True,
    max_active_runs=2,
    default_args={
        "retries": 3,
        "retry_delay": 300,
    },
    tags=["b3", "taxas", "financeiro"],
) as dag:

    check_day = PythonOperator(
        task_id="check_business_day",
        python_callable=check_business_day,
    )

    extract = PythonOperator(
        task_id="extract_taxas",
        python_callable=extract_taxas,
    )

    validate = PythonOperator(
        task_id="validate_raw",
        python_callable=validate_raw,
    )

    silver = PythonOperator(
        task_id="transform_to_silver",
        python_callable=transform_to_silver,
    )

    gold = PythonOperator(
        task_id="publish_gold",
        python_callable=publish_gold,
    )

    control = PythonOperator(
        task_id="update_control_table",
        python_callable=update_control_table,
    )

    check_day >> extract >> validate >> silver >> gold >> control
