---
name: etik-scraping
description: Bir web sitesinden veri cekilecegi (scraping) her durumda kullan. Bekleme, hata yonetimi, sayfalama kontrolu, sayisal temizlik ve CSV'ye yazma kurallarini uygular.
---

# Etik ve guvenilir web scraping kurallari

Bu proje icin yazilan her scraping kodu asagidaki kurallara uymak ZORUNDADIR.

## 1. Siteyi yorma
- Her HTTP istegi arasinda en az 0.5 saniye bekle (`time.sleep(0.5-1.0)`).
- Ayni sayfayi gereksiz yere tekrar indirme; tek bir `requests.Session` kullan.
- Kodu yazmadan once `robots.txt` ve sitenin kullanim izni kontrol edilsin.

## 2. Hata yonetimi (program asla cokmemeli)
- Her istek `try/except requests.RequestException` icinde olsun, `timeout` verilsin.
- Basarisiz istek en fazla 3 kez, artan beklemeyle tekrar denensin; yine olmazsa sayfa atlanip loglansin.
- Her alan (baslik, fiyat, puan, stok...) ayri ayri kontrol edilsin: eleman yoksa `None` yaz, exception firlatma.
- Tum uyari ve hatalar `logging` ile hem konsola hem `scraper.log` dosyasina yazilsin.

## 3. Eksiksiz veri
- Sayfalama: "next" linki bitene kadar dongu kur; sayfa sayisini sabit kodlama.
- Liste sayfasinda olmayan bilgiler (ornegin kategori) icin kategori sayfalarini veya detay sayfasini gez.
- Basliklarda gorunen metni degil, kisaltilmamis `title` niteligini kullan ("In a Dark, Dark ..." hatasi).
- Is bitince toplam kayit sayisini sitede yazan sayiyla karsilastir, fark varsa uyari ver.
- Benzersiz URL sayisiyla tekrar eden kayitlari kontrol et.

## 4. Temiz CSV
- Fiyat: para birimi isaretini at, `float` yap ("£51.77" -> 51.77).
- Puan: kelimeyi sayiya cevir ("Three" -> 3).
- Yanit kodlamasini `utf-8` olarak ayarla ("Â£" bozulmasini onle).
- CSV'yi `utf-8-sig` ile yaz (Excel'de Turkce/ozel karakterler dogru gorunsun).

## 5. Dogrulama
- Kodu calistirmadan once kucuk bir ornek HTML ile test et (bozuk kart, 404 sayfa, ag hatasi senaryolari).
- Analizden once `df.isna().sum()`, `df.dtypes` ve `df.describe()` ciktilarini kontrol et.
