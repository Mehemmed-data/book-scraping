# Prompt Gunlugu

Kullanilan AI araci: **Claude (Anthropic)** – kod yazma, dosya olusturma, tarayici (browser) MCP'si ve fetch araci olan ajan modunda.
Asagida calismanin yonunu belirleyen en onemli 8 prompt ve sonuclari var.

---

### 1. Gorevin tamamini vermek
**Prompt:** "Odev metnini aynen veriyorum: books.toscrape.com'daki tum kitaplar icin ad, fiyat, puan, stok, kategori cek; kitaplar.csv'ye sayisal formatta kaydet; 2 grafik + 'puani yuksek kitaplar daha mi pahali' cevabi; bekleme ve hata yonetimi olsun. Hepsini harfiyen yap."

**AI ne uretti:** Once bir plan cikardi: kategori bilgisi ana listede olmadigi icin 50 kategori sayfasini sayfalamayla gezmeyi onerdi (1000 detay sayfasi yerine 80 istek). Ortami kontrol etti: Python, requests, BeautifulSoup, pandas, matplotlib kurulu.

**Calisti mi?** Kismen. AI'in calistigi ortamin terminali internete cikamiyordu (`curl` → `000`, baglanti yok).
**Nasil duzelttim:** Kodu yine requests + BeautifulSoup ile yazdirdim (benim bilgisayarimda calisacak), veriyi ise AI'in tarayici araciyla cekmesine karar verdik (bkz. 3).

---

### 2. Fetch araci ile sayfayi okumak
**Prompt:** "Travel kategori sayfasindaki her kitabi 'ad | fiyat | yildiz sinifi | stok' formatinda listele."

**AI ne uretti:** 11 kitabin ad, fiyat ve stok bilgisini dogru verdi ama puan sutununa hep `UNKNOWN` yazdi.
**Calisti mi?** Hayir. Fetch araci HTML'i markdown'a cevirirken `<p class="star-rating Three">` sinifini kaybediyor; puan sadece CSS sinifinda var.
**Nasil duzelttim:** Puan icin HTML'in kendisine (DOM) erisebilen tarayici MCP'sine gectim. **Ders:** Bir aracin ciktisini kontrol etmeden kullanmak eksik veri demek.

---

### 3. Tarayici MCP'si ile tum veriyi cekmek
**Prompt:** "Tarayicida books.toscrape.com'u ac; 50 kategorinin her sayfasini 'next' bitene kadar gez, her istek arasinda 0.5 sn bekle, hata olursa 3 kez dene ve hatayi kaydet; ad (title niteligi), fiyat, puan (sayi), stok, kategori topla."

**AI ne uretti:** Sayfa icinde calisan bir JavaScript (fetch + DOMParser) yazdi. Ilk denemede site izni gerekti; izni verdikten sonra calisti.
**Calisti mi?** Evet. **80 sayfa, 1000 kitap, 1000 benzersiz URL, 0 hata, hicbir alan bos degil.** Sitede yazan "1000 results" ile birebir ayni.

---

### 4. Python scraper'ini yazdirmak
**Prompt:** "Ayni mantigi requests + BeautifulSoup ile scraper.py olarak yaz. Fiyat float, puan int olsun; sayfa acilmazsa veya alan bos gelirse program cokmesin; 0.5-1 sn bekleme olsun; sonunda toplami 1000 ile karsilastirsin."

**AI ne uretti:** `get_soup()` (timeout + 3 deneme + log), `parse_price()`, `parse_rating()`, `parse_book()` fonksiyonlari; `logging` ile `scraper.log`; `utf-8-sig` CSV.
**Dikkat edilen hata:** Sayfadaki baglanti metni uzun adlari kisaltiyor (`In a Dark, Dark ...`). AI tam adi `title` niteliginden aldi. Ayrica `resp.encoding = "utf-8"` ekledi, yoksa fiyat `Â£47.82` gibi bozuk gelebiliyor.

---

### 5. Hata yonetimini test ettirmek
**Prompt:** "Kodu internetsiz test et: gercek siteden alinmis ornek bir HTML kullan, bir sayfa 404 donsun, bir sayfada baglanti kopsun, bir kitap kartinda fiyat ve puan olmasin."

**AI ne uretti:** `tests/test_scraper.py` ve `tests/fixture.html`. `session.get` sahte bir fonksiyonla degistirildi.
**Calisti mi?** Evet. 404 ve baglanti hatasi 3 kez denenip loglandi, program devam etti; bos kartta fiyat/puan `None` oldu; tam baslik dogru alindi. "TUM TESTLER GECTI".

---

### 6. Tasinan verinin dogrulugunu kontrol etmek
**Prompt:** "Tarayicidaki veriyi dosyaya aktardiktan sonra hicbir satirin bozulmadigini kanitla."

**AI ne uretti:** Hem tarayicida hem Python'da ayni hesaplari yapti: satir sayisi, fiyat toplami (£35,070.35), puan sayilari ve 3 parcanin SHA-256 ozetleri.
**Calisti mi?** Evet, tum degerler birebir eslesti.

---

### 7. Analiz ve grafikler
**Prompt:** "kitaplar.csv ile: (1) en pahali 10 kategorinin ortalama fiyati, (2) puan dagilimi, (3) puan-fiyat iliskisi grafigi ve korelasyon. PNG kaydet."

**AI ne uretti:** `analiz.py`, 3 grafik ve konsol ozeti.
**Calisti mi?** Evet, ama iki sorun gordum ve duzelttirdim:
- En pahali kategoriler (Suspense, Novels) sadece **1 kitaptan** olusuyordu; ortalama yaniltici olabilir. → Her cubuga `n=` kitap sayisi ve genel ortalama cizgisi eklendi.
- 3. grafikte aciklama kutusu (legend) bir cizginin uzerine biniyordu. → Grafigin disina tasindi.

---

### 8. Proje kurallari (skill) dosyasi
**Prompt:** "Bundan sonraki scraping isleri icin AI'a verilecek bir kural dosyasi yaz: bekleme, hata yonetimi, sayfalama, title niteligi, encoding, toplam sayi kontrolu."

**AI ne uretti:** `skills/etik-scraping/SKILL.md` – Claude skill formatinda, Cursor rules olarak da kullanilabilir.
**Calisti mi?** Dosya hazir; bu calismada karsilasilan hatalarin hepsi (puan sinifinin kaybolmasi haric, o arac sorunu) kural olarak icinde.
