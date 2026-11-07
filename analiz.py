"""
kitaplar.csv uzerinde analiz ve grafikler.
Calistirma:  python analiz.py   (once scraper.py calistirilmis olmali)
Ciktilar: grafikler/ klasorunde PNG dosyalari + konsolda ozet istatistikler.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("grafikler", exist_ok=True)
df = pd.read_csv("kitaplar.csv", encoding="utf-8-sig")

# --- Veri kontrolu ---
print("Satir sayisi:", len(df))
print("Tamamen ayni satir olmayan kayit:", df.drop_duplicates().shape[0])
print("Bos deger sayilari:\n", df.isna().sum())
print("Fiyat tipi:", df["fiyat"].dtype, "| Puan tipi:", df["puan"].dtype)
print(df.describe())

BLUE = "#2a6fdb"
GRAY = "#9aa4b2"

# --- Grafik 1: En pahali 10 kategori (ortalama fiyat) ---
cat = (df.groupby("kategori")["fiyat"].agg(["mean", "count"])
         .sort_values("mean", ascending=False).head(10))
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(cat.index[::-1], cat["mean"][::-1], color=BLUE)
for i, (m, n) in enumerate(zip(cat["mean"][::-1], cat["count"][::-1])):
    ax.text(m + 0.5, i, f"£{m:.2f}  (n={n})", va="center", fontsize=9)
ax.set_title("Ortalama fiyata gore en pahali 10 kategori", fontsize=13, loc="left")
ax.set_xlabel("Ortalama fiyat (£)   |   n = kategorideki kitap sayisi (n kucukse ortalama guvenilir degildir)")
ax.axvline(df["fiyat"].mean(), color=GRAY, linestyle="--", linewidth=1)
ax.text(df["fiyat"].mean() + 0.3, 9.45, f"Genel ort. £{df['fiyat'].mean():.2f}", color="#5b6573", fontsize=8)
ax.set_xlim(0, cat["mean"].max() * 1.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafikler/1_kategori_ortalama_fiyat.png", dpi=150)
plt.close()
print("\nEn pahali 10 kategori:\n", cat.round(2))

# --- Grafik 2: Puan dagilimi ---
dist = df["puan"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(dist.index.astype(str), dist.values, color=BLUE)
for b, v in zip(bars, dist.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f"{v} (%{v / len(df) * 100:.1f})",
            ha="center", fontsize=9)
ax.set_title("Kitaplarin puan dagilimi", fontsize=13, loc="left")
ax.set_xlabel("Puan (yildiz)")
ax.set_ylabel("Kitap sayisi")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafikler/2_puan_dagilimi.png", dpi=150)
plt.close()
print("\nPuan dagilimi:\n", dist)

# --- Grafik 3: Puan vs fiyat ---
by_rating = df.groupby("puan")["fiyat"].agg(["mean", "median", "count"])
corr = df["puan"].corr(df["fiyat"])
fig, ax = plt.subplots(figsize=(8, 5))
groups = [df.loc[df["puan"] == r, "fiyat"] for r in sorted(df["puan"].unique())]
ax.boxplot(groups, tick_labels=[str(r) for r in sorted(df["puan"].unique())],
           patch_artist=True, boxprops=dict(facecolor="#d6e4fb", color=BLUE),
           medianprops=dict(color=BLUE, linewidth=2))
ax.plot(range(1, 6), by_rating["mean"].values, "o--", color="#d9480f", label="Ortalama")
ax.set_title(f"Puana gore fiyat dagilimi (korelasyon r = {corr:.3f})", fontsize=13, loc="left")
ax.set_xlabel("Puan (yildiz)")
ax.set_ylabel("Fiyat (£)")
ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1, 1.0))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafikler/3_puan_fiyat_iliskisi.png", dpi=150)
plt.close()
print("\nPuana gore fiyat:\n", by_rating.round(2))
print(f"\nPearson korelasyonu (puan, fiyat): {corr:.4f}")
