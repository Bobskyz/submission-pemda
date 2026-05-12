# ETL Pipeline - Fashion Studio Data

Pipeline otomatis untuk **Extract, Transform, dan Load** data produk fashion dari website Fashion Studio ke berbagai storage (CSV, Google Sheets, PostgreSQL).

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
  - [Clone Repository](#1-clone-repository)
  - [Buat Virtual Environment](#2-buat-virtual-environment)
  - [Aktivasi Virtual Environment](#3-aktivasi-virtual-environment)
  - [Install Dependencies](#4-install-dependencies)
- [Konfigurasi](#️-konfigurasi)
  - [Setup Environment Variables](#1-setup-environment-variables)
  - [Google Sheets API Setup](#2-google-sheets-api-setup)
  - [PostgreSQL Setup](#3-postgresql-setup)
- [Cara Menggunakan](#-cara-menggunakan)
- [Struktur Proyek](#-struktur-proyek)
- [Testing](#-testing)
- [Dokumentasi Data](#-dokumentasi-data)
- [Keamanan](#-keamanan)
- [Troubleshooting](#-troubleshooting)
- [Lisensi](#-lisensi)
- [Support](#-support)

---

## ✨ Fitur Utama

### 1. **Extract (Ekstraksi)**
- Web scraping dari Fashion Studio website (50 halaman)
- Mengekstrak informasi produk: judul, harga, rating, warna, ukuran, gender
- Menangani error dan timeout dengan graceful handling

### 2. **Transform (Transformasi)**
- Membersihkan data: hapus duplikat, normalize format
- Konversi harga dari USD ke IDR (1 USD = 16,000 IDR)
- Validasi data dan handling missing values
- Menambahkan timestamp untuk setiap record

### 3. **Load (Menyimpan)**
- **CSV**: Simpan ke file lokal `products.csv`
- **Google Sheets**: Sinkronisasi otomatis ke Google Sheets
- **PostgreSQL**: Menyimpan ke database relasional

---

## 🔧 Prasyarat

- Python 3.8+
- pip (package manager)
- PostgreSQL (opsional, jika ingin menyimpan ke database)
- Google Sheets API credentials (opsional, jika ingin sinkronisasi)

---

## 📥 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/Bobskyz/submission-pemda.git
cd submission-pemda
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
```

### 3. Aktivasi Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfigurasi

### 1. Setup Environment Variables

Buat file `.env` di root directory, lalu edit file `.env` dan isi dengan kredensial Anda:
```env
# Google Sheets Configuration
GSHEET_ID=<your_google_sheet_id_here>

# PostgreSQL Configuration
DB_CONN=postgresql+psycopg2://<username>:<password>@localhost:5432/<database_name>
```

### 2. Google Sheets API Setup

Jika ingin menyimpan ke Google Sheets:

1. Download credentials JSON dari [Google Cloud Console](https://console.cloud.google.com/)
2. Simpan sebagai `google-sheets-api.json` di root directory
3. File ini otomatis dalam `.gitignore` untuk keamanan

### 3. PostgreSQL Setup

Jika ingin menyimpan ke database PostgreSQL, ikuti langkah-langkah berikut:

#### Step 1: Buat User PostgreSQL

Akses PostgreSQL console sebagai superuser:
```bash
psql -U postgres
```

Buat user baru dengan password:
```sql
CREATE USER developer WITH PASSWORD 'your_secure_password';
```

#### Step 2: Buat Database

Buat database untuk project:
```sql
CREATE DATABASE submission_pemda;
```

#### Step 3: Berikan Hak Kepemilikan (Ownership)

Berikan ownership database ke user yang baru dibuat:
```sql
ALTER DATABASE submission_pemda OWNER TO developer;
```

Berikan privilege yang diperlukan:
```sql
GRANT ALL PRIVILEGES ON DATABASE submission_pemda TO developer;
```

Keluar dari PostgreSQL:
```sql
\q
```

#### Step 4: Buat Tabel

Koneksi ke database dengan user baru:
```bash
psql -U developer -d submission_pemda
```

#### Step 5: Update `.env` File

Update connection string di `.env`:
```env
DB_CONN=postgresql+psycopg2://developer:your_secure_password@localhost:5432/submission_pemda
```

---

## 🚀 Cara Menggunakan

### Menjalankan Full ETL Pipeline
```bash
python main.py
```

Output yang diharapkan:
```
Memulai ekstraksi...
Scraping halaman 1-50...
Memulai transformasi...
[Transformation Details]
Menyimpan data...
Pipeline ETL selesai.
```

---

## 📁 Struktur Proyek

```
submission-pemda/
├── main.py                      # Entry point ETL pipeline
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── google-sheets-api.json       # Google API credentials (gitignored)
├── products.csv                 # Output CSV file
│
├── utils/                       # Utility modules
│   ├── extract.py              # Web scraping logic
│   ├── transform.py            # Data cleaning & transformation
│   └── load.py                 # Save to CSV/Sheets/Database
│
├── tests/                       # Unit tests
│   ├── test_extract.py         # Test extraction module
│   ├── test_transform.py       # Test transformation logic
│   └── test_load.py            # Test loading functions
│
└── htmlcov/                     # Coverage report (generated)
```

---

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_extract.py -v
```

### Generate Coverage Report
```bash
coverage run -m pytest tests
coverage report -m
python -m coverage html
```

Buka `htmlcov/index.html` di browser untuk melihat laporan coverage detail.

---

## 📊 Dokumentasi Data

### Struktur Output Data

Setelah transformasi, data akan memiliki struktur berikut:

| Column | Type | Deskripsi |
|--------|------|-----------|
| Title | String | Nama produk |
| Price | Float | Harga dalam Rupiah (IDR) |
| Rating | Float | Rating produk (0-5) |
| Colors | String | Warna yang tersedia |
| Size | String | Ukuran yang tersedia |
| Gender | String | Target gender (Male/Female/Unisex) |
| timestamp | DateTime | Waktu saat data dikumpulkan |

---

## 🔒 Keamanan

- ✅ Semua kredensial disimpan dalam `.env` (tidak di-commit)
- ✅ `google-sheets-api.json` dalam `.gitignore`
- ✅ Environment variables divalidasi saat runtime
- ✅ Use-Agent headers untuk scraping yang responsible

---

## 🐛 Troubleshooting

### Error: "GSHEET_ID environment variable not set"
**Solusi**: Pastikan `.env` file ada dan berisi `GSHEET_ID=your_id`

### Error: "DB_CONN environment variable not set"
**Solusi**: Pastikan `.env` file berisi `DB_CONN=postgresql://...`

### Error: "Connection refused" (PostgreSQL)
**Solusi**: Pastikan PostgreSQL service berjalan dan connection string benar

### Scraping Error: "Timeout"
**Solusi**: Periksa koneksi internet dan URL website masih aktif

---

## 📝 Lisensi

Project ini adalah submission untuk Proyek Akhir Kelas Belajar Fundamental Pemrosesan Data di Coding Camp

---

## 📞 Support

Jika ada pertanyaan atau issues, silakan buat issue di repository ini.

---

**Last Updated**: May 2026
