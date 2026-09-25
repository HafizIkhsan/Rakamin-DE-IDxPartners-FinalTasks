import pandas as pd
from pathlib import Path

def extract_csv(file_path: str) -> pd.DataFrame:
    """"
    Extracts data from a CSV file
    Args:
        file_path (str): The path to the CSV file
    Returns:
        pd.DataFrame: A DataFrame containing the extracted data
    """

    df = pd.read_csv(file_path)

    return df