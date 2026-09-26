from airflow.sdk import dag, task

from src.extracts.extract_csv import extract_csv
from src.extracts.extract_xlsx import extract_xlsx
from src.extracts.extract_mssql import extract_table
from src.transform.transform import (
    dimAccount,
    dimBranch,
    dimCustomer,
)
from src.load.load import load_to_mssql
from src.config.connection import get_connection

@dag(
    dag_id="etl_dimensional_table",
    schedule=None,
    start_date=None,
    catchup=False,
)

def etl_dimensional_table():
    """
    DAG for ETL process of dimensional tables (DimCustomer, DimBranch, DimAccount).
    """
    @task
    def process_dim_customer():
        """
        Process of the DimCustomer table
        """
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_customer_raw = extract_table('customer', source_conn)
        df_city_raw = extract_table('city', source_conn)
        df_state_raw = extract_table('state', source_conn)

        df_dim_customer = dimCustomer(dfCustomer=df_customer_raw, dfCity=df_city_raw, dfState=df_state_raw)

        load_to_mssql(df=df_dim_customer, table_name="DimCustomer", connection_engine=target_engine)

    @task
    def process_dim_branch():
        """
        Process of the DimBranch table
        """
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_branch_raw = extract_table('branch', source_conn)

        df_dim_branch = dimBranch(df_branch_raw)

        load_to_mssql(df=df_dim_branch, table_name="DimBranch", connection_engine=target_engine)

    @task
    def process_dim_account():
        """
        Process of the DimAccount table
        """
        source_conn = get_connection('source')
        target_engine = get_connection('target')

        df_account_raw = extract_table('account', source_conn)

        df_dim_account = dimAccount(df_account_raw)

        load_to_mssql(df=df_dim_account, table_name="DimAccount", connection_engine=target_engine)

    process_dim_customer() >> process_dim_account()
    process_dim_branch()

etl_dimensional_table()