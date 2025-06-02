# Website Career Page Scraper

Aplikasi Python untuk mengumpulkan URL halaman karir dari website perusahaan menggunakan teknik Google Dorking dan metode scraping.

## Fitur Utama
- Pencarian URL karir menggunakan Google Dork dengan kombinasi kriteria:
  - Domain Indonesia (.co.id)
  - Domain internasional (.com)
  - Kata kunci "karir" dan "career"
- Rotasi User-Agent secara acak untuk menghindari deteksi
- Implementasi delay acak antar permintaan
- Filter duplikasi URL hasil pencarian
- Simpan hasil ke file teks

## Prerequisites
- Python 3.6+
- Library yang diperlukan:
  ```bash
  pip install requests googlesearch-python