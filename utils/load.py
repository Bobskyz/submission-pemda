import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import logging

def save_to_csv(df: pd.DataFrame, filename: str = "products.csv") -> None:
    """Simpan DataFrame ke file CSV."""
    try:
        if df.empty:
            print(f"[PERINGATAN] DataFrame kosong. File '{filename}' tidak disimpan.")
            return
        
        df.to_csv(filename, index=False)
        print(f"[OK] Data tersimpan ke {filename} ({len(df)} baris)")
    except Exception as e:
        logging.error(f"Failed to save CSV: {e}")
        raise

def save_to_google_sheets(df: pd.DataFrame, sheet_id: str, credentials_file: str = "google-sheets-api.json") -> None:
    """Simpan DataFrame ke Google Sheets."""
    try:
        if df.empty:
            print(f"[PERINGATAN] DataFrame kosong. Data tidak diunggah ke Google Sheets.")
            return
        
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        service = build("sheets", "v4", credentials=creds)

        values = [df.columns.tolist()] + df.values.tolist()

        body = {"values": values}
        service.spreadsheets().values().clear(
            spreadsheetId=sheet_id, range="Sheet1"
        ).execute()
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"[OK] Data terunggah ke Google Sheets ({len(df)} baris)")
    except FileNotFoundError:
        logging.error(f"Credentials file '{credentials_file}' not found!")
        raise
    except Exception as e:
        logging.error(f"Failed to upload to Google Sheets: {e}")
        raise

def save_to_postgresql(df: pd.DataFrame, connection_string: str, table_name: str = "products") -> None:
    """Simpan DataFrame ke PostgreSQL."""
    try:
        if df.empty:
            print(f"[PERINGATAN] DataFrame kosong. Data tidak disimpan ke PostgreSQL.")
            return
        
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"[OK] Data tersimpan ke tabel PostgreSQL '{table_name}' ({len(df)} baris)")
    except Exception as e:
        print(f"[PERINGATAN] Gagal menyimpan ke PostgreSQL: {e}")
        print(f"  (Pastikan PostgreSQL berjalan dan kredensial benar)")
        logging.error(f"Gagal menyimpan ke PostgreSQL: {e}")