import os
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('/opt/airflow/.env')

def get_connection(db_role: str):
    """
    Returns an SQLAlchemy engine connection to the database.
    """
    server = os.getenv('DB_SERVER')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    
    if db_role == 'source':
        database = os.getenv('SOURCE_DB')
    elif db_role == 'target':
        database = os.getenv('TARGET_DB')
    else:
        raise ValueError("Invalid db_role. Must be 'source' or 'target'.")

    connection_server = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={db_user};"
        f"PWD={db_pass};"
        f"Encrypt=yes;TrustServerCertificate=yes;"
    )

    try:
        params = urllib.parse.quote_plus(connection_server)
        engine_url = f"mssql+pyodbc:///?odbc_connect={params}"
        
        engine = create_engine(engine_url)
        return engine
        
    except Exception as e:
        print(f"Gagal terhubung ke database {db_role}: {e}")
        raise