import os
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_connection(db_role: str):
    """
    Returns an SQLAlchemy engine connection to the database.
    """
    server = os.getenv('DB_SERVER')
    
    if db_role == 'source':
        database = os.getenv('SOURCE_DB')
    elif db_role == 'target':
        database = os.getenv('TARGET_DB')
    else:
        raise ValueError("Invalid db_role. Must be 'source' or 'target'.")

    # String koneksi aslimu
    connection_server = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"Encrypt=yes;TrustServerCertificate=yes;"
    )

    try:
        # Ubah string menjadi format SQLAlchemy
        params = urllib.parse.quote_plus(connection_server)
        engine_url = f"mssql+pyodbc:///?odbc_connect={params}"
        
        # Cetak mesin koneksinya
        engine = create_engine(engine_url)
        return engine
        
    except Exception as e:
        print(f"Gagal terhubung ke database {db_role}: {e}")
        raise