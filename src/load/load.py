import pandas as pd

def load_to_mssql(df: pd.DataFrame, table_name: str, connection_engine) -> None:
    """
    Loads a DataFrame into a Microsoft SQL Server database table.
    Args:
        df (pd.DataFrame): The DataFrame to load into the database.
        table_name (str): The name of the target table in the database.
        connection_engine: The SQLAlchemy engine connection to the database.
    """
    try:
        # Pandas akan langsung mengenali connection_engine dari SQLAlchemy
        df.to_sql(
            name=table_name, 
            con=connection_engine, 
            if_exists='append', 
            index=False
        )
        print(f"Berhasil load {len(df)} baris ke tabel {table_name}.")
    except Exception as e:
        print(f"Error loading data: {e}")
        raise