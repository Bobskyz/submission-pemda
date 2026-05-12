import pandas as pd
import re

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dan memvalidasi data hasil scraping.
    """
    data = df.copy()
    
    print(f"\n{'='*70}")
    print(f"TRANSFORMATION DETAILS")
    print(f"{'='*70}")
    print(f"Input rows: {len(data)}")

    # Cek apakah DataFrame kosong
    if data.empty:
        print("[WARNING] DataFrame kosong. Tidak ada data untuk ditransformasi.")
        return pd.DataFrame(columns=[
            "Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"
        ])

    # 1. Price: ekstrak angka dan konversi ke Rupiah
    def clean_price(p):
        if "$" in str(p):
            try:
                numeric = float(re.sub(r"[^0-9.]", "", str(p)))
                return numeric * 16000  # Kalikan langsung di dalam fungsi
            except ValueError:
                return None
        return None

    data["Price"] = data["Price"].apply(clean_price)
    invalid_prices = data["Price"].isna().sum()
    print(f"Setelah clean_price: Harga tidak valid (None): {invalid_prices}/{len(data)}")

    # 2. Rating: ambil digit sebelum '/' (tangani emoji ⭐)
    def clean_rating(r):
        if not isinstance(r, str) or "/" not in r:
            return None
        # Regex yang lebih fleksibel: cari pola angka.angka / 5 (lewati emoji dan karakter khusus)
        match = re.search(r"([0-9.]+)\s*/\s*5", r)
        if match:
            try:
                value = float(match.group(1))
                if 0 <= value <= 5:  # Validasi rentang
                    return value
            except ValueError:
                pass
        return None
    
    # Debug: Lihat contoh rating sebelum pembersihan
    print(f"\nContoh rating dari data asli:")
    for i, rating in enumerate(df["Rating"].head(5).tolist()):
        # Bersihkan rating untuk pencetakan (hapus emoji)
        rating_clean = rating.encode('ascii', 'ignore').decode('ascii') if isinstance(rating, str) else str(rating)
        print(f"  {i+1}. '{rating_clean[:80]}'")
    
    data["Rating"] = data["Rating"].apply(clean_rating)
    invalid_ratings = data["Rating"].isna().sum()
    print(f"Setelah clean_rating: Rating tidak valid (None): {invalid_ratings}/{len(data)}")

    # 3. Colors: ambil angka pertama
    def clean_colors(c):
        if not isinstance(c, str):
            return 0
        match = re.search(r"(\d+)", c)
        if match:
            return int(match.group(1))
        return 0
    data["Colors"] = data["Colors"].apply(clean_colors)

    # 4. Size: hapus "Size: " di awal
    data["Size"] = data["Size"].fillna("")  # Handle None/NaN
    data["Size"] = data["Size"].astype(str)  # Pastikan string
    data["Size"] = data["Size"].str.replace(r"^Size:\s*", "", regex=True)
    data["Size"] = data["Size"].str.strip()

    # 5. Gender: hapus "Gender: "
    data["Gender"] = data["Gender"].fillna("")  # Handle None/NaN
    data["Gender"] = data["Gender"].astype(str)  # Pastikan string
    data["Gender"] = data["Gender"].str.replace(r"^Gender:\s*", "", regex=True)
    data["Gender"] = data["Gender"].str.strip()

    # 6. Title: hapus "Unknown Product"
    before_unknown = len(data)
    data = data[data["Title"] != "Unknown Product"]
    print(f"Setelah menghapus 'Unknown Product': {len(data)} baris (terhapus {before_unknown - len(data)})")

    # 7. Hapus baris dengan nilai null di kolom penting
    before_drop = len(data)
    print(f"\nSebelum dropna:")
    print(f"  Null di Title: {data['Title'].isna().sum()}")
    print(f"  Null di Price: {data['Price'].isna().sum()}")
    print(f"  Null di Rating: {data['Rating'].isna().sum()}")
    
    data.dropna(subset=["Title", "Price", "Rating"], inplace=True)
    print(f"Setelah dropna: {len(data)} baris (terhapus {before_drop - len(data)})")
    
    data.reset_index(drop=True, inplace=True)  # ✅ Reset index setelah drop

    # Pastikan tipe data sesuai
    data["Price"] = data["Price"].astype("float64")
    data["Rating"] = data["Rating"].astype(float)
    data["Colors"] = data["Colors"].astype(int)
    data["Size"] = data["Size"].astype(str)
    data["Gender"] = data["Gender"].astype(str)
    
    print(f"\n[OUTPUT FINAL] {len(data)} baris")
    print(f"{'='*70}\n")
    return data