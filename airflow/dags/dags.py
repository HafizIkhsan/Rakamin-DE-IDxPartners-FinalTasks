import sys
from pathlib import Path
from airflow.sdk import dag, task

from src.extracts.extract_csv import extract_csv
from src.extracts.extract_xlsx import extract_xlsx
from src.extracts.extract_mssql import extract_table
from src.transform.transform import (
    dimAccount,
    dimBranch,
    dimCustomer,
    factTransaction,
)
from src.load.load import load_to_mssql
from src.config.connection import get_connection

@dag(
    dag_id="etl_pipeline_idx",
    schedule=None,
    start_date=None,
    catchup=False,
)

def etl_pipeline():
    @task
    def process_dim_customer():
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_customer_raw = extract_table('customer', source_conn)
        df_city_raw = extract_table('city', source_conn)
        df_state_raw = extract_table('state', source_conn)

        df_dim_customer = dimCustomer(dfCustomer=df_customer_raw, dfCity=df_city_raw, dfState=df_state_raw)

        load_to_mssql(df=df_dim_customer, table_name="DimCustomer", connection_engine=target_engine)

    @task
    def process_dim_branch():
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_branch_raw = extract_table('branch', source_conn)

        df_dim_branch = dimBranch(df_branch_raw)

        load_to_mssql(df=df_dim_branch, table_name="DimBranch", connection_engine=target_engine)

    @task
    def process_dim_account():
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_account_raw = extract_table('account', source_conn)

        df_dim_account = dimAccount(df_account_raw)

        load_to_mssql(df=df_dim_account, table_name="DimAccount", connection_engine=target_engine)

    @task
    def process_fact_transaction():
        project_dir = Path('/opt/airflow')

        csv_path = project_dir / "data" / "raw" / "transaction_csv.csv"
        xlsx_path = project_dir / "data" / "raw" / "transaction_excel.xlsx"

        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_trx_mssql = extract_table('transaction_db', source_conn)
        df_csv = extract_csv(str(csv_path))
        df_xlsx = extract_xlsx(str(xlsx_path))

        df_fact_transaction = factTransaction(dfMmsql=df_trx_mssql, dfCsv=df_csv, dfXlsx=df_xlsx)

        load_to_mssql(df=df_fact_transaction, table_name="FactTransaction", connection_engine=target_engine)

    process_dim_customer() >> process_dim_account()

    [
        process_dim_branch()
    ] >> process_fact_transaction()

etl_pipeline()