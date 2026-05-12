import pytest
import pandas as pd
from unittest.mock import patch, Mock, MagicMock
from utils.extract import scrape_main

# Contoh HTML yang sesuai dengan struktur sebenarnya
sample_html = """
<div class="product-details">
    <h3 class="product-title">Cool T-Shirt</h3>
    <div class="price-container">
        <span class="price">$29.99</span>
    </div>
    <p style="font-size: 14px; color: #777;">Rating: 4.7 / 5</p>
    <p style="font-size: 14px; color: #777;">3 Colors</p>
    <p style="font-size: 14px; color: #777;">Size: M</p>
    <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
</div>
"""

@patch("utils.extract.time.sleep")  # Mock time.sleep untuk mempercepat pengujian
@patch("utils.extract.requests.get")
def test_scrape_returns_dataframe(mock_get, mock_sleep):
    # Simulasikan respons sukses untuk semua halaman
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = f"<html><body>{sample_html * 20}</body></html>"  # 20 produk per halaman
    mock_get.return_value = mock_response

    df = scrape_main()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1000  # 50 halaman * 20 produk
    assert "Title" in df.columns
    assert "timestamp" in df.columns
    # Verifikasi time.sleep dipanggil (pembatasan kecepatan)
    assert mock_sleep.call_count == 50

@patch("utils.extract.time.sleep")  # Mock time.sleep
@patch("utils.extract.requests.get")
def test_scrape_handles_request_error(mock_get, mock_sleep):
    # Halaman 1 gagal dengan RequestException, halaman 2-50 sukses
    import requests
    
    mock_response_ok = Mock()
    mock_response_ok.status_code = 200
    mock_response_ok.text = f"<html><body>{sample_html * 20}</body></html>"

    # Efek samping: halaman 1 munculkan RequestException, halaman 2-50 sukses
    mock_get.side_effect = [requests.exceptions.ConnectionError("Koneksi gagal")] + [mock_response_ok] * 49

    df = scrape_main()
    
    # Harus tetap mendapatkan 49 halaman * 20 = 980 data (halaman 1 dilewati)
    assert len(df) == 980
    # time.sleep harus dipanggil 49 kali (halaman 2-50)
    assert mock_sleep.call_count == 49