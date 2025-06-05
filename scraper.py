import asyncio
import nest_asyncio
import aiohttp
import time
import random
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Masukkan API KEY Serper kamu di sini
SERPER_API_KEY = "8690b8d764824ba633fb8475d67b9ad5b6b9****"

HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
]

DOMAINS = [
    ".com",
    ".co.id",
    # Tambah domain yang ingin dicari di sini
]

KEYWORDS = ["career", "karir", "jobs", "lowongan", "careers"]

# Jumlah hasil maksimal per query (cek batasan Serper API)
MAX_RESULTS_PER_QUERY = 200

# Delay antar request (detik)
MIN_DELAY = 1.5
MAX_DELAY = 3.0

def get_random_user_agent():
    return random.choice(USER_AGENTS)

async def search_with_serper(session, query, num_results=MAX_RESULTS_PER_QUERY):
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": num_results
    }
    try:
        async with session.post(url, headers=HEADERS, json=payload, timeout=30) as response:
            response.raise_for_status()
            data = await response.json()
            return [item["link"] for item in data.get("organic", []) if "link" in item]
    except Exception as e:
        print(f"Error saat mencari dengan Serper query '{query}': {e}")
        return []

async def fetch(session, url):
    headers = {"User-Agent": get_random_user_agent()}
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            response.raise_for_status()
            text = await response.text()
            return text
    except Exception as e:
        print(f"Error fetch {url}: {e}")
        return None

def extract_career_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text().lower()
        href_lower = href.lower()
        # Cek keyword di href atau teks link
        if any(k in href_lower or k in text for k in KEYWORDS):
            # Buat URL absolut jika relatif
            if href.startswith('http'):
                full_url = href
            elif href.startswith('/'):
                full_url = urljoin(base_url, href)
            else:
                # Skip link yang bukan http(s) atau path relatif
                continue
            links.add(full_url)
    return links

async def crawl_domain(session, start_url, domain, career_urls, visited_urls, max_depth=2, current_depth=0):
    if current_depth > max_depth:
        return
    if start_url in visited_urls:
        return
    visited_urls.add(start_url)

    html = await fetch(session, start_url)
    if not html:
        return

    found_links = extract_career_links(start_url, html)

    for link in found_links:
        if urlparse(link).netloc.endswith(domain):
            if link not in career_urls:
                career_urls.add(link)
    # Crawl deeper ke link internal dengan kata kunci
    tasks = []
    for link in found_links:
        if urlparse(link).netloc.endswith(domain) and link not in visited_urls:
            tasks.append(crawl_domain(session, link, domain, career_urls, visited_urls, max_depth, current_depth + 1))
    if tasks:
        await asyncio.gather(*tasks)

async def main():
    career_urls = set()
    scraped_domains = set()

    async with aiohttp.ClientSession() as session:
        # Buat semua kombinasi query per domain dan keyword
        queries = []
        for domain in DOMAINS:
            for kw in KEYWORDS:
                queries.append(f"site:{domain} inurl:{kw}")

        for query in queries:
            print(f"\n🔍 Mencari dengan query: {query}")
            urls = await search_with_serper(session, query)
            print(f"  Ditemukan {len(urls)} URL hasil pencarian")

            for url in urls:
                domain_url = urlparse(url).netloc
                if domain_url not in scraped_domains:
                    scraped_domains.add(domain_url)
                    print(f"  🚀 Memproses domain: {domain_url}")

                    # Jika url sudah mengandung kata kunci karir, langsung simpan
                    if any(k in url.lower() for k in KEYWORDS):
                        career_urls.add(url)
                        print(f"    ✅ Ditambahkan URL langsung: {url}")

                    # Crawl halaman untuk temukan link karir tambahan
                    await crawl_domain(session, url, domain_url, career_urls, set())

                    # Delay kecil supaya gak terlalu agresif
                    delay = random.uniform(MIN_DELAY, MAX_DELAY)
                    print(f"    ⏳ Menunggu {delay:.2f} detik...")
                    await asyncio.sleep(delay)
                else:
                    print(f"  ⚠️ Domain {domain_url} sudah diproses, lewati.")

    # Simpan hasil ke career.txt
    with open("career.txt", "w") as f:
        for url in sorted(career_urls):
            f.write(url + "\n")

    print(f"\n✅ Selesai! Ditemukan total {len(career_urls)} URL unik. Disimpan di career.txt")

nest_asyncio.apply()

await main()