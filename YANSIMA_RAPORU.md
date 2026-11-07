# Yansima Raporu

**AI en cok nerede yardimci oldu?**
Plan asamasinda: kategori bilgisinin ana listede olmadigini fark edip 1000 detay sayfasi yerine 50 kategoriyi sayfalamayla gezmeyi onerdi (80 istek). Hata yonetimi, tekrar deneme, loglama ve sahte 404/baglanti hatasiyla test kodunu cok hizli yazdi. Grafiklerin duzenli ve okunur olmasinda da zaman kazandirdi.

**AI nerede yanildi veya eksik kaldi?**
Fetch araciyla okunan sayfada puanlar `UNKNOWN` geldi; cunku puan sadece CSS sinifinda (`star-rating Three`) ve arac HTML'i metne cevirirken bunu siliyor. AI'in calistigi ortamin internete cikamamasi da ilk plani bozdu. Analizde ilk grafik, sadece 1 kitabi olan kategorileri "en pahali" diye gosteriyordu; bu istatistiksel olarak yaniltici oldugu icin kitap sayisi (n) eklettim.

**Sonuclarin dogru oldugundan nasil emin oldum?**
- Toplam kitap sayisi sitede yazan **1000** ile ayni; 1000 benzersiz URL, tekrar yok.
- Hicbir sutunda bos deger yok; fiyat `float64`, puan `int64`; fiyatlar £10.00–£59.99, puanlar 1–5 araliginda.
- Tarayicidan dosyaya aktarilan veri SHA-256 ozetleri ve fiyat toplamiyla (£35,070.35) birebir karsilastirildi.
- Ornek kitaplar (ornegin *Sharp Objects* £47.82, 4★; *In a Dark, Dark Wood* £19.63, 1★) sitenin kendi HTML'i ile karsilastirildi.
- Hata yonetimi ornek HTML ile test edildi ("TUM TESTLER GECTI").

**Puani yuksek kitaplar daha mi pahali?** Hayir. Korelasyon r = 0.028 (neredeyse sifir); 1★ ortalama £34.56, 5★ ortalama £35.37.

**Bir dahaki sefere neyi farkli yapardim?**
Bir aracin ciktisini kullanmadan once 2-3 satirini elle kontrol ederdim (puan hatasini hemen yakaladim ama planlamadan once yapsaydim daha hizli olurdu). Kurallari (skill dosyasini) ise baslamadan once yazardim. Stok adedini (ornegin "22 available") de istersem detay sayfalarini ayri, daha yavas bir adimda cekerdim.

---

## Bonus: Kullanilan MCP ve skill

**1) Tarayici MCP'si (Claude masaustu uygulamasindaki yerlesik tarayici)**
- *Kurulum:* Claude masaustu uygulamasi acik → sohbette tarayici araclari etkinlestirildi → ilk erisimde cikan izin penceresinde `books.toscrape.com` icin izin verildi.
- *Ne kazandirdi:* Sayfanin gercek HTML'ine (DOM) eristigi icin puan sinifini okuyabildim; 80 sayfayi 0.5 sn beklemeyle tek seferde cekip benim scraper'imin sonuclarini dogrulamak icin bir "ikinci kaynak" oldu. Kullanmasaydim AI'in ortami internete cikamadigi icin veriyi dogrulayamazdim; fetch araci da puanlari veremedi.

**2) Fetch araci**
- Ana sayfadaki "1000 results" sayisini ve 50 kategori linkini hizlica okumak icin kullanildi (toplam sayi kontrolu buradan geldi).

**3) Skill / kural dosyasi:** `skills/etik-scraping/SKILL.md`
- *Kurulum:* Claude icin klasoru skill olarak eklemek yeterli (Cursor'da ayni metin `.cursor/rules/` altina konabilir).
- *Ne kazandirdi:* Bu calismada yasanan hatalari (kisaltilmis baslik, `Â£` kodlama hatasi, puan sinifi, toplam sayi kontrolu, bekleme) kural haline getirdi; bir sonraki scraping isinde AI bunlari bastan uygular, ayni hatalar tekrar yasanmaz.
