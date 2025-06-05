# 🇮🇩 Indonesian Job Portal Scraper

Script Python untuk **mencari dan meng-crawl halaman karier** (`career`, `karir`, `jobs`, dll.) dari berbagai domain menggunakan teknik **Google Dorking**, **Serper API**, dan **async web crawling**.

## 🚀 Fitur

* 🔍 Pencarian URL menggunakan Serper (Google Search API).
* 🕷️ Async crawling menggunakan `aiohttp` & `asyncio`.
* 📄 Ekstraksi halaman dengan kata kunci karier seperti `career`, `karir`, `jobs`, dll.
* 🌐 Mendukung domain `.com`, `.co.id`, dan lainnya.
* 🛡️ Rotasi User-Agent untuk menghindari blokir.
* 📁 Output disimpan di file `career.txt`.

## 🛠️ Instalasi

```bash
git clone https://github.com/noval1802/IndonesianJobPortalScraper.git
cd IndonesianJobPortalScraper
pip install -r requirements.txt
```

```bash
pip install aiohttp nest_asyncio beautifulsoup4
```

## 🔑 Konfigurasi API Key

Daftar dan dapatkan API Key dari [https://serper.dev](https://serper.dev), lalu masukkan ke dalam variabel:

```python
SERPER_API_KEY = "API_KAMU_DI_SINI"
```

## ⚙️ Cara Penggunaan

1. Jalankan script:

```python
import nest_asyncio
nest_asyncio.apply()
await main()
```

2. Atau jalankan di lingkungan seperti Jupyter Notebook, Google Colab, atau dengan cara modifikasi sedikit agar bisa dipanggil dari script biasa.

3. Hasil URL akan disimpan di file `career.txt`.

## 🧠 Cara Kerja

1. Script akan membuat kombinasi query seperti:

   ```
   site:.com inurl:career
   site:.co.id inurl:karir
   ```
2. Menggunakan Serper API untuk mengambil hasil pencarian Google.
3. Melakukan crawling ke URL hasil pencarian dan mencari link tambahan terkait halaman karier.
4. Menyimpan semua link yang ditemukan dan cocok ke file `career.txt`.

## 📂 Struktur Output

File `career.txt` berisi daftar URL halaman karier unik, contohnya:

```
https://example.com/career
https://jobs.nama-perusahaan.co.id/karir
https://recruitment.situs.co.id/careers
```

## 📝 Kustomisasi

* Tambahkan TLD/domain lain di variabel `DOMAINS`
* Tambahkan kata kunci baru di `KEYWORDS`
* Atur `MAX_RESULTS_PER_QUERY` jika kamu berlangganan plan Serper API yang lebih tinggi
* Ubah `MIN_DELAY` dan `MAX_DELAY` untuk mengatur intensitas crawling

## ⚠️ Disclaimer

* Gunakan script ini hanya untuk tujuan pembelajaran, riset, atau personal automation.
* Jangan gunakan untuk scraping secara masif tanpa izin situs terkait.
* Tunduk pada aturan robots.txt dan Terms of Service dari masing-masing website.

## 📄 License

MIT License

---

> Dibuat oleh [@noval1802](https://github.com/noval1802) untuk eksplorasi data lowongan kerja di Indonesia 🇮🇩
