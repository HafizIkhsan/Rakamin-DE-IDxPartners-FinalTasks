import os
from pathlib import Path
from airflow.sdk import dag, task

from src.extracts.extract_csv import extract_csv
from src.extracts.extract_xlsx import extract_xlsx
from src.extracts.extract_mssql import extract_table
from src.transform.transform import (
    factTransaction,
)
from src.load.load import load_to_mssql
from src.config.connection import get_connection

from airflow.providers.google.common.hooks.base_google import GoogleBaseHook

@dag(
    dag_id="etl_fact_table",
    schedule=None,
    start_date=None,
    catchup=False,
)

def etl_fact_table():
    """
    DAG for ETL process of the FactTransaction table.
    """
    @task
    def process_fact_transaction():
        """
        Process of the FactTransaction table
        """
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

    @task
    def load_fact_bq():
        """
        Load the FactTransaction table into Google BigQuery
        """
        gcp_hook = GoogleBaseHook(gcp_conn_id='gcp_default')
        credentials = gcp_hook.get_credentials()

        table_id = os.getenv('BQ_TABLE_ID')

        df = extract_table('FactTransaction', get_connection('target'))

        df.to_gbq(
            destination_table=table_id,
            project_id=credentials.project_id,
            if_exists='replace',
            credentials=credentials
        )

    process_fact_transaction() >> load_fact_bq()

etl_fact_table()