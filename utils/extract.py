import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

def scrape_main() -> pd.DataFrame:
    """
    Scrape data produk dari halaman 1 sampai 50 website Fashion Studio.
    """
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for page in range(1, 51):
        # Halaman 1 tanpa suffix, halaman 2+ dengan /page{n}
        url = base_url if page == 1 else f"{base_url}/page{page}"
        try:
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Ubah ke selector yang benar: product-details
            cards = soup.find_all("div", class_="product-details")
            
            if not cards:
                print(f"Halaman {page}: Tidak ada produk ditemukan. Menghentikan paginasi.")
                break

            print(f"Halaman {page}: Ditemukan {len(cards)} produk")

            for card in cards:
                # Judul
                title_elem = card.find("h3", class_="product-title")
                title = title_elem.text.strip() if title_elem else "Unknown Product"

                # Harga
                price_elem = card.find("span", class_="price")
                price_text = price_elem.text.strip() if price_elem else "Price Unavailable"

                # Rating, Colors, Size, Gender: Cari semua tag <p> DALAM card
                # (mereka adalah anak dari product-details, bukan saudara)
                rating_text = "Invalid Rating"
                colors_text = "0 Colors"
                size_text = ""
                gender_text = ""
                
                # Cari semua tag <p> yang DIRECT CHILDREN dari card
                all_p_tags = card.find_all("p", recursive=False)
                
                for p in all_p_tags:
                    p_text = p.text.strip()
                    if "Rating:" in p_text:
                        rating_text = p_text
                    elif "Colors" in p_text:
                        colors_text = p_text
                    elif "Size:" in p_text:
                        size_text = p_text
                    elif "Gender:" in p_text:
                        gender_text = p_text

                all_products.append({
                    "Title": title,
                    "Price": price_text,
                    "Rating": rating_text,
                    "Colors": colors_text,
                    "Size": size_text,
                    "Gender": gender_text,
                    "timestamp": timestamp
                })

        except requests.exceptions.RequestException as e:
            print(f"Kesalahan mengikis halaman {page}: {e}")
            continue

        time.sleep(1)

    df = pd.DataFrame(all_products)
    print(f"Total data diekstrak: {len(df)}")
    return df