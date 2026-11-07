# Books to Scrape – Veri Cekme, Temizleme ve Analiz

https://books.toscrape.com sitesindeki **1000 kitabin tamami** icin kitap adi, fiyat, puan (1-5), stok durumu ve kategori bilgisi cekilmis, `kitaplar.csv` dosyasina kaydedilmis ve analiz edilmistir.

## Klasor yapisi

```
kitap_projesi/
├── scraper.py                  # Veri cekme + CSV'ye kaydetme
├── analiz.py                   # Analiz + grafikler
├── kitaplar.csv                # Cekilen veri (1000 satir)
├── grafikler/
│   ├── 1_kategori_ortalama_fiyat.png
│   ├── 2_puan_dagilimi.png
│   └── 3_puan_fiyat_iliskisi.png
├── analiz_cikti.txt            # analiz.py konsol ciktisi
├── tests/
│   ├── fixture.html            # Gercek siteden alinmis ornek HTML (+ bozuk kart)
│   └── test_scraper.py         # Hata yonetimi testi (internetsiz calisir)
├── skills/etik-scraping/SKILL.md   # Bonus: AI aracina verilen proje kurallari (skill)
├── PROMPT_GUNLUGU.md
├── YANSIMA_RAPORU.md
└── requirements.txt
```

## Kurulum

Python 3.9+ gerekir.

```bash
pip install -r requirements.txt
```

## Calistirma

```bash
# 1) Veriyi cek (yaklasik 1-1.5 dakika surer; 80 sayfa x 0.7 sn bekleme)
python scraper.py

# 2) Analiz ve grafikler (grafikler/ klasorune PNG kaydeder)
python analiz.py

# (Istege bagli) Hata yonetimi testi - internet gerektirmez
cd tests && python test_scraper.py
```

`scraper.py` calisirken her kategori ve sayfa icin kac kitap bulundugunu yazar, sonunda toplam sayiyi
sitedeki 1000 ile karsilastirir. Tum uyarilar `scraper.log` dosyasina da yazilir.

## Nasil calisiyor?

1. Ana sayfanin sol menusundeki **50 kategori** bulunur.
2. Her kategori sayfasi, "next" linki bitene kadar sayfa sayfa gezilir (toplam **80 sayfa**).
   Kategori bilgisi ana listede olmadigi icin bu yol secildi; 1000 detay sayfasini tek tek acmaktan ~12 kat daha az istek yapar.
3. Her kitap kartindan: `title` niteligi (kisaltilmamis ad), fiyat, `star-rating` sinifi ve stok bilgisi alinir.
4. Her istek arasinda **0.7 sn** beklenir; acilmayan sayfa 3 kez denenir, yine olmazsa loglanip atlanir;
   bos alanlar `None` olur, program cokmez.

## CSV formati

| Sutun | Tip | Ornek |
|---|---|---|
| kitap_adi | metin | Sharp Objects |
| fiyat | ondalik sayi (£) | 47.82 |
| puan | tam sayi 1-5 | 4 |
| stok_durumu | metin | In stock |
| kategori | metin | Mystery |

## Ozet sonuclar

- Toplam: **1000 kitap**, 50 kategori, bos deger yok. Ortalama fiyat £35.07 (min £10.00, max £59.99).
- Puan dagilimi oldukca dengeli: 1★ 226, 2★ 196, 3★ 203, 4★ 179, 5★ 196.
- En pahali kategori ortalamalari: Suspense £58.33, Novels £54.81, Politics £53.61 (bu kategorilerde 1-3 kitap var, dikkatli yorumlanmali).
- **Puani yuksek kitaplar daha mi pahali? Hayir.** Puan ile fiyat arasindaki korelasyon r = 0.028 (neredeyse sifir).
  1★ kitaplarin ortalama fiyati £34.56, 5★ kitaplarinki £35.37; aradaki fark £1'in altinda ve her puan grubunda
  fiyatlar £10-£60 arasinda ayni sekilde dagiliyor. Bu sitede fiyat ve puan birbirinden bagimsiz (buyuk ihtimalle rastgele) atanmis.
