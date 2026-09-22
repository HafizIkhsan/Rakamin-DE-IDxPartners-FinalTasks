import pandas as pd
from src.config.connection import get_connection
from typing import Optional, List

def extract_mssql(query: str, connection) -> pd.DataFrame:
    """
    Extracts data from a Microsoft SQL Server database using a SQL query
    Args:
        query (str): The SQL query to execute
        connection: The database connection object
    Returns:    
        pd.DataFrame: A DataFrame containing the extracted data
    """

    df = pd.read_sql_query(query, connection)
    
    return df

def extract_table(table_name:str, connection, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Extracts entire table or a specific columns
    Args:
        table_name (str): Name of the table
        connection: The database connection object
        columns (Optional[List[str]]): List of columns to extract, if None extracts all columns
    Returns:
        pd.DataFrame: A DataFrame containing the extracted data
    """

    if columns:
        cols = ', '.join(columns)
        query = f"SELECT {cols} FROM {table_name}"
    else:
        query = f"SELECT * FROM {table_name}"

    df = pd.read_sql_query(query, connection)

    return df

if __name__ == "__main__":
    conn = get_connection('source')
    df = extract_table('transaction_db', conn)
    print(df.info())