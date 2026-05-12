import os
from dotenv import load_dotenv
from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

# Load environment variables from .env file
load_dotenv()

def main():
    # 1. Ekstrak
    print("Memulai ekstraksi...")
    raw_df = scrape_main()

    # 2. Transformasi
    print("Memulai transformasi...")
    clean_df = transform_data(raw_df)

    # 3. Muat
    print("Menyimpan data...")
    save_to_csv(clean_df, "products.csv")

    # Google Sheets - Get from environment variable
    GSHEET_ID = os.getenv("GSHEET_ID")
    if not GSHEET_ID:
        raise ValueError("GSHEET_ID environment variable not set. Please add it to .env file.")
    save_to_google_sheets(clean_df, GSHEET_ID)

    # PostgreSQL - Get from environment variable
    DB_CONN = os.getenv("DB_CONN")
    if not DB_CONN:
        raise ValueError("DB_CONN environment variable not set. Please add it to .env file.")
    save_to_postgresql(clean_df, DB_CONN)

    print("Pipeline ETL selesai.")

if __name__ == "__main__":
    main()