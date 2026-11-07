import sys, requests
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import scraper
scraper.DELAY_SECONDS = 0
html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixture.html'), encoding='utf-8').read()
calls = []
class R:
    def __init__(s, t, code=200): s.text, s.status_code, s.encoding = t, code, None
    def raise_for_status(s):
        if s.status_code >= 400: raise requests.HTTPError(f"{s.status_code} Error")
def fake_get(url, timeout=None):
    calls.append(url)
    if url.endswith('page-2.html'): return R('', 404)            # acilmayan sayfa
    if 'travel_2' in url: raise requests.ConnectionError('baglanti koptu')  # ag hatasi
    return R(html)
scraper.session.get = fake_get
books = scraper.scrape_all()
for b in books: print(b)
print('istek sayisi:', len(calls))
assert books[0]['kitap_adi'] == 'Sharp Objects' and books[0]['fiyat'] == 47.82 and books[0]['puan'] == 4
assert books[1]['kitap_adi'] == 'In a Dark, Dark Wood'      # kisaltilmis metin degil, title niteligi
assert books[2]['fiyat'] is None and books[2]['puan'] is None  # bos alan -> None, cokme yok
print('TUM TESTLER GECTI')
