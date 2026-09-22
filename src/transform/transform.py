import pandas as pd

def dimAccount(dfAccount: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the account data
    Args:
        dfAccount (pd.DataFrame): The input DataFrame containing account data.
    Returns:
        pd.DataFrame: A transformed DataFrame with renamed columns and duplicates removed.
    """

    try:
        result = dfAccount.rename(columns={
            'account_id': 'AccountID',
            'customer_id': 'CustomerID',
            'account_type': 'AccountType',
            'balance': 'Balance',
            'date_opened': 'DateOpened',
            'status': 'Status'
        })

        result = result.drop_duplicates(subset=['AccountID'], keep='first')

        return result
    except KeyError as e:
        print(f"KeyError, please check {e}")    
        raise


def dimBranch(dfBranch: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the branch data
    Args:
        dfBranch (pd.DataFrame): The input DataFrame containing branch data.
    Returns:
        pd.DataFrame: A transformed DataFrame with renamed columns and duplicates removed.
    """
    
    try:
        result = dfBranch.rename(columns={
            'branch_id': 'BranchId',
            "branch_name": "BranchName",
            "branch_location": "BranchLocation"
        })

        result = result.drop_duplicates(subset=['BranchId'], keep='first')

        return result
    except KeyError as e:
        print(f"KeyError, please check {e}")    
        raise


def dimCustomer(
        dfCustomer: pd.DataFrame,
        dfCity: pd.DataFrame,
        dfState: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Transforms the customer data
    Args:
        dfCustomer (pd.DataFrame): The input DataFrame containing customer data.
        dfCity (pd.DataFrame): The input DataFrame containing city data.
        dfState (pd.DataFrame): The input DataFrame containing state data.
    Returns:
        pd.DataFrame: A transformed DataFrame with renamed columns and duplicates removed.
    """

    try:
        join_city = pd.merge(dfCustomer, dfCity, on='city_id', how='left')
        result = pd.merge(join_city, dfState, on='state_id', how='left')

        selected_columns = result[
            [
                'customer_id', 'customer_name', 'address', 'city_name',
                'state_name', 'age', 'gender', 'email'
            ]
        ]

        dimCustomer = selected_columns.rename(columns={
            'customer_id': 'CustomerId',
            'customer_name': 'CustomerName',
            'address': 'Address',
            'city_name': 'CityName',
            'state_name': 'StateName',
            'age': 'Age',
            'gender': 'Gender',
            'email': 'Email'
        })

        capitalized_columns = [
            'CustomerName', 'Address', 'CityName', 'StateName', 'Gender'
        ]

        for col in capitalized_columns:
            dimCustomer[col] = dimCustomer[col].str.upper()

        dimCustomer = dimCustomer.drop_duplicates(subset=['CustomerId'], keep='first')

        return dimCustomer
    except KeyError as e:
        print(f"KeyError, please check {e}")    
        raise


def factTransaction(
        dfMmsql: pd.DataFrame,
        dfCsv: pd.DataFrame,
        dfXlsx: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Transforms the transaction data
    Args:
        dfTransaction (pd.DataFrame): The input DataFrame containing transaction data.
    Returns:
        pd.DataFrame: A transformed DataFrame with renamed columns and duplicates removed.
    """

    try:
        dfCsv['transaction_date'] = pd.to_datetime(dfCsv['transaction_date'], format="%d-%m-%Y %H:%M:%S")

        dfTransaction = pd.concat([dfMmsql, dfCsv, dfXlsx], ignore_index=True)

        result = dfTransaction.rename(columns={
            'transaction_id': 'TransactionId',
            'account_id': 'AccountId',
            'transaction_date': 'TransactionDate',
            'amount': 'Amount',
            'transaction_type': 'TransactionType',
            'branch_id': 'BranchId'
        })

        result = result.drop_duplicates(subset=['TransactionId'], keep='first')

        return result
    except KeyError as e:
        print(f"KeyError, please check {e}")    
        raise
