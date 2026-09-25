import pandas as pd
from pathlib import Path

def extract_xlsx(file_path: str) -> pd.DataFrame:
    """
    Extracts data from an XLSX file
    Args:
        file_path (str): The path to the XLSX file
    Returns:
        pd.DataFrame: A DataFrame containing the extracted data
    """
    
    df = pd.read_excel(file_path)

    return df