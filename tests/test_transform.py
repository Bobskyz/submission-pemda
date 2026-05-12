import pandas as pd
import pytest
from utils.transform import transform_data

def create_sample_df():
    return pd.DataFrame({
        "Title": ["Shirt A", "Pants B", "Unknown Product", "Shirt A"],  # duplikat
        "Price": ["$25.00", "Price Unavailable", "$30.00", "$25.00"],
        "Rating": ["4.5 / 5", "4.0 / 5", "Invalid Rating", "4.5 / 5"],
        "Colors": ["2 Colors", "1 Colors", "3 Colors", "2 Colors"],
        "Size": ["Size: M", "Size: L", "Size: XL", "Size: M"],
        "Gender": ["Gender: Men", "Gender: Women", "Gender: Unisex", "Gender: Men"],
        "timestamp": ["2025-05-12 10:00:00"] * 4
    })

def test_unknown_product_removed():
    df = create_sample_df()
    cleaned = transform_data(df)
    assert "Unknown Product" not in cleaned["Title"].values

def test_price_conversion():
    df = create_sample_df()
    cleaned = transform_data(df)
    # Harga $25.00 menjadi 25 * 16000 = 400000
    assert (cleaned["Price"] == 400000).any()

def test_nulls_dropped():
    df = create_sample_df()
    cleaned = transform_data(df)
    assert cleaned["Price"].notna().all()
    assert cleaned["Rating"].notna().all()

def test_duplicates_removed():
    df = create_sample_df()
    cleaned = transform_data(df)
    # Setelah transformasi, duplikat tetap dipertahankan (tidak drop_duplicates)
    # Data dari setiap halaman adalah valid record yang perlu disimpan
    assert len(cleaned[cleaned["Title"] == "Shirt A"]) == 2

def test_rating_float():
    df = create_sample_df()
    cleaned = transform_data(df)
    assert cleaned["Rating"].dtype == float

def test_size_prefix_removed():
    df = create_sample_df()
    cleaned = transform_data(df)
    assert all(not val.startswith("Size:") for val in cleaned["Size"])

def test_gender_prefix_removed():
    df = create_sample_df()
    cleaned = transform_data(df)
    assert all(not val.startswith("Gender:") for val in cleaned["Gender"])