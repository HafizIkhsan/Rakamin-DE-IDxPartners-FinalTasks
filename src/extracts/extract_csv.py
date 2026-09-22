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

if __name__ == "__main__":
    curr_dir = Path(__file__).parent.parent.parent
    file_path = curr_dir / "data" / "raw" / "transaction_csv.csv"
    df = extract_csv(file_path)
    print(df.info())