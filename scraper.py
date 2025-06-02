import requests
from googlesearch import search
import time
import random

# Daftar User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def scrape_career_urls():
    # Daftar kata kunci yang lebih spesifik menggunakan intext
    keywords = [
        "inurl:karir intext:karir site:.co.id",
        "inurl:career intext:career site:.co.id",
        "inurl:karir intext:karir site:.com",
        "inurl:career intext:career site:.com"
    ]
    career_urls = []

    for keyword in keywords:
        try:
            # Melakukan pencarian menggunakan Google Dorking
            for url in search(keyword, num_results=100):
                # Memeriksa apakah URL mengandung kata kunci "career" atau "karir"
                if "career" in url.lower() or "karir" in url.lower():
                    career_urls.append(url)

                # Tambahkan delay acak antara 2 hingga 5 detik
                delay = random.uniform(2, 5)
                time.sleep(delay)

        except Exception as e:
            print(f"Error searching {keyword}: {e}")

    # Menghapus duplikat URL
    career_urls = list(set(career_urls))

    # Menyimpan hasil ke file career.txt
    with open("career.txt", "w") as file:
        for url in career_urls:
            file.write(f"{url}\n")
    print(f"Found {len(career_urls)} unique career URLs. Saved to career.txt")

if __name__ == "__main__":
    scrape_career_urls()