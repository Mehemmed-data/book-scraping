"""
books.toscrape.com scraper
--------------------------
Sitedeki TUM kitaplar icin: kitap adi, fiyat, puan (1-5), stok durumu, kategori
bilgilerini ceker ve kitaplar.csv dosyasina kaydeder.

Yaklasim: Ana sayfadaki 50 kategoriyi bulur, her kategorinin tum sayfalarini
("next" linkini takip ederek) gezer. Boylece kategori bilgisi, 1000 kitabin
detay sayfasini tek tek acmaya gerek kalmadan elde edilir.

Calistirma:  python scraper.py
"""

import csv
import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "kitaplar.csv"
DELAY_SECONDS = 0.7        # istekler arasi bekleme (etik scraping)
MAX_RETRIES = 3            # bir sayfa acilmazsa kac kez denensin
TIMEOUT = 15               # saniye
EXPECTED_TOTAL = 1000      # sitede yazan toplam kitap sayisi

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("scraper.log", encoding="utf-8"),
              logging.StreamHandler()],
)
log = logging.getLogger(__name__)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (egitim amacli scraper odevi)"})


def get_soup(url):
    """Sayfayi indirir; hata olursa tekrar dener, yine olmazsa None doner (program cokmez)."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            resp.encoding = "utf-8"   # site UTF-8; aksi halde '£' yerine 'Â£' gelir
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as exc:
            log.warning("Sayfa acilamadi (%d/%d): %s -> %s", attempt, MAX_RETRIES, url, exc)
            time.sleep(DELAY_SECONDS * attempt * 2)
    log.error("Sayfa atlandi: %s", url)
    return None


def parse_price(text):
    """'£51.77' -> 51.77 ; bos/bozuksa None."""
    if not text:
        return None
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch == ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_rating(tag):
    """<p class="star-rating Three"> -> 3 ; yoksa None."""
    if tag is None:
        return None
    for cls in tag.get("class", []):
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return None


def parse_book(article, category, page_url):
    """Tek bir kitap kartindan alanlari ceker. Bos alanlar None olur, hata firlatmaz."""
    link = article.select_one("h3 a")
    title = link.get("title", "").strip() if link else None
    price = parse_price(article.select_one(".price_color").get_text(strip=True)
                        if article.select_one(".price_color") else None)
    rating = parse_rating(article.select_one("p.star-rating"))
    stock_tag = article.select_one(".availability")
    stock = stock_tag.get_text(strip=True) if stock_tag else None
    url = urljoin(page_url, link["href"]) if link and link.get("href") else None
    return {"kitap_adi": title or None, "fiyat": price, "puan": rating,
            "stok_durumu": stock, "kategori": category, "url": url}


def get_categories():
    soup = get_soup(BASE_URL)
    if soup is None:
        raise SystemExit("Ana sayfa acilamadi, cikiliyor.")
    cats = []
    for a in soup.select(".side_categories ul li ul li a"):
        cats.append((a.get_text(strip=True), urljoin(BASE_URL, a["href"])))
    log.info("%d kategori bulundu.", len(cats))
    return cats


def scrape_all():
    books = []
    for name, url in get_categories():
        page = 1
        while url:
            time.sleep(DELAY_SECONDS)
            soup = get_soup(url)
            if soup is None:
                break
            items = soup.select("article.product_pod")
            for art in items:
                try:
                    books.append(parse_book(art, name, url))
                except Exception as exc:          # tek kitap bozuksa digerleri devam etsin
                    log.warning("Kitap parse edilemedi (%s): %s", url, exc)
            log.info("%-20s sayfa %d: %d kitap", name, page, len(items))
            nxt = soup.select_one("li.next a")
            url = urljoin(url, nxt["href"]) if nxt else None
            page += 1
    return books


def save_csv(books):
    # url sadece tekrar kontrolu icin kullanilir, CSV'ye istenen 5 alan yazilir
    fields = ["kitap_adi", "fiyat", "puan", "stok_durumu", "kategori"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(books)


if __name__ == "__main__":
    start = time.time()
    data = scrape_all()
    save_csv(data)
    unique = len({b["url"] for b in data})
    log.info("Toplam %d kitap (%d benzersiz) %s dosyasina yazildi. Sure: %.0f sn",
             len(data), unique, OUTPUT_FILE, time.time() - start)
    if len(data) != EXPECTED_TOTAL:
        log.warning("UYARI: Sitede %d kitap yaziyor, %d cekildi!", EXPECTED_TOTAL, len(data))
