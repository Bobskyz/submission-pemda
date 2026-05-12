import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql
from sqlalchemy import create_engine
import tempfile
import os

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Title": ["T-Shirt"],
        "Price": [400000],
        "Rating": [4.5],
        "Colors": [2],
        "Size": ["M"],
        "Gender": ["Men"],
        "timestamp": ["2025-05-12 10:00:00"]
    })

@pytest.fixture
def temp_csv_file():
    """Buat file CSV sementara untuk pengujian"""
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    yield path
    # Pembersihan
    if os.path.exists(path):
        os.remove(path)

def test_save_to_csv(sample_df, temp_csv_file):
    """Tes fungsionalitas simpan CSV"""
    save_to_csv(sample_df, temp_csv_file)
    
    # Verifikasi file dibuat dan memiliki data
    assert os.path.exists(temp_csv_file)
    saved_df = pd.read_csv(temp_csv_file)
    assert len(saved_df) == 1
    assert saved_df["Title"].iloc[0] == "T-Shirt"

@patch("utils.load.build")
@patch("utils.load.service_account.Credentials.from_service_account_file")
def test_save_to_google_sheets(mock_creds, mock_build, sample_df):
    """Tes fungsionalitas unggah Google Sheets"""
    mock_service = MagicMock()
    mock_build.return_value = mock_service

    save_to_google_sheets(sample_df, "fake_sheet_id", "fake_creds.json")
    
    # Pastikan metode clear dan update dipanggil
    mock_service.spreadsheets().values().clear.assert_called_once()
    mock_service.spreadsheets().values().update.assert_called_once()

def test_save_to_postgresql(sample_df):
    """Tes fungsionalitas simpan PostgreSQL menggunakan file database SQLite nyata"""
    # Buat file database SQLite sementara
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Gunakan SQLite berbasis file (sepenuhnya kompatibel dengan SQLAlchemy, tidak munculkan peringatan)
        connection_string = f"sqlite:///{db_path}"
        
        # Panggil fungsi save_to_postgresql
        save_to_postgresql(sample_df, connection_string, "test_products_table")
        
        # Verifikasi data tersimpan dengan membaca kembali
        engine = create_engine(connection_string)
        result_df = pd.read_sql("SELECT * FROM test_products_table", engine)
        engine.dispose()  # Tutup koneksi sebelum pembersihan
        
        assert len(result_df) == 1
        assert result_df["Title"].iloc[0] == "T-Shirt"
        assert result_df["Price"].iloc[0] == 400000
    finally:
        # Pembersihan
        import time
        time.sleep(0.1)  # Jeda kecil untuk memastikan file dirilis
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except (PermissionError, OSError):
                pass  # Abaikan jika tidak dapat menghapus (kunci windows)