from pathlib import Path

# Import semua fungsi yang sudah Anda buat di folder src
from src.extracts.extract_csv import extract_csv
from src.extracts.extract_xlsx import extract_xlsx
from src.extracts.extract_mssql import extract_table
from src.transform.transform import dimAccount, dimBranch, dimCustomer, factTransaction
from src.load.load import load_to_mssql
from src.config.connection import get_connection

def main():
    print("=== Memulai Pipeline ETL ===")
    
    try:
        current_dir = Path(__file__).parent
        
        # 1. EXTRACT
        print("\n1. Memulai proses Extract...")
        csv_path = current_dir / "data" / "raw" / "transaction_csv.csv"
        xlsx_path = current_dir / "data" / "raw" / "transaction_excel.xlsx"
        
        # Ekstrak data transaksi
        df_csv = extract_csv(str(csv_path))
        df_xlsx = extract_xlsx(str(xlsx_path))
        
        source_conn = get_connection('source')
        df_trx_mssql = extract_table('transaction_db', source_conn) 
        
        # Ekstrak data master (tabel pendukung) untuk Dimensi
        # Sesuaikan nama tabelnya dengan yang ada di database sumbermu
        df_customer_raw = extract_table('customer', source_conn)
        df_city_raw = extract_table('city', source_conn)
        df_state_raw = extract_table('state', source_conn)
        
        df_account_raw = extract_table('account', source_conn)
        df_branch_raw = extract_table('branch', source_conn)

        # 2. TRANSFORM
        print("\n2. Memulai proses Transform...")
        # Masukkan bahan baku yang tepat ke masing-masing cetakannya
        df_dim_customer = dimCustomer(dfCustomer=df_customer_raw, dfCity=df_city_raw, dfState=df_state_raw)
        df_dim_branch = dimBranch(df_branch_raw)
        df_dim_account = dimAccount(df_account_raw)
        
        # Sesuai rancangan join 3 tabel sebelumnya
        
        # Fact table menggabungkan ketiga sumber transaksi
        df_fact_transaction = factTransaction(dfMmsql=df_trx_mssql, dfCsv=df_csv, dfXlsx=df_xlsx)
        
        # 3. LOAD
        print("\n3. Memulai proses Load...")
        target_engine = get_connection('target')
        
        # Eksekusi proses load satu per satu untuk masing-masing tabel
        print("Loading DimCustomer...")
        load_to_mssql(df=df_dim_customer, table_name="DimCustomer", connection_engine=target_engine)

        print("Loading DimAccount...")
        load_to_mssql(df=df_dim_account, table_name="DimAccount", connection_engine=target_engine)
        
        print("Loading DimBranch...")
        load_to_mssql(df=df_dim_branch, table_name="DimBranch", connection_engine=target_engine)
        
        print("Loading FactTransaction...")
        load_to_mssql(df=df_fact_transaction, table_name="FactTransaction", connection_engine=target_engine)
        
        print("\n=== Pipeline ETL Selesai dengan Sukses! ===")
        
    except Exception as e:
        print(f"\n=== Pipeline ETL Gagal: {e} ===")

if __name__ == "__main__":
    main()