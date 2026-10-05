import pandas as pd

# Membaca dataset Gramedia
df = pd.read_csv("dataset_buku.csv")

print("=== 5 DATA PERTAMA ===")
print(df.head())

print("\n=== INFORMASI DATASET ===")
print(df.info())

print("\n=== JUMLAH BARIS DAN KOLOM ===")
print(df.shape)

print("\n=== NAMA KOLOM ===")
print(df.columns.tolist())

print("\n=== JUMLAH DATA KOSONG ===")
print(df.isnull().sum())

print("\n=== JUMLAH DATA DUPLIKAT ===")
print(df.duplicated().sum())
print("\n=== DATA TERJUAL YANG KOSONG ===")
print(df[df["Terjual"].isna()][["Judul", "Terjual"]])
print("\n=== DATA HARGA ASLI YANG KOSONG ===")
print(df[df["Harga_Asli"].isna()][["Judul", "Harga", "Harga_Asli", "Diskon"]])
print("\n=== CEK HARGA ASLI KOSONG DAN DISKON ===")

cek = df[df["Harga_Asli"].isna()][
    ["Judul", "Harga", "Harga_Asli", "Diskon"]
]

print(cek["Diskon"].value_counts())
# ============================================
# CLEANING HARGA ASLI
# ============================================

df["Harga_Asli"] = df["Harga_Asli"].fillna(df["Harga"])

print("\n=== SETELAH CLEANING HARGA ASLI ===")
print("Jumlah Harga_Asli kosong:", df["Harga_Asli"].isna().sum())
print("\n=== CEK DATA TERJUAL KOSONG ===")

terjual_kosong = df[df["Terjual"].isna()][
    ["Judul", "Harga", "Harga_Asli", "Diskon"]
]

print(terjual_kosong)
# ============================================
# TRANSFORMASI HARGA
# ============================================

df["Harga_Numeric"] = (
    df["Harga"]
    .str.replace("Rp", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
    .astype(float)
)

print("\n=== HASIL TRANSFORMASI HARGA ===")
print(df[["Harga", "Harga_Numeric"]].head(10))
# ============================================
# TRANSFORMASI HARGA ASLI
# ============================================

df["Harga_Asli_Numeric"] = (
    df["Harga_Asli"]
    .str.replace("Rp", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
    .astype(float)
)

print("\n=== HASIL TRANSFORMASI HARGA ASLI ===")
print(df[["Harga_Asli", "Harga_Asli_Numeric"]].head(10))
# ============================================
# TRANSFORMASI DISKON
# ============================================

df["Diskon_Numeric"] = (
    df["Diskon"]
    .str.replace("%", "", regex=False)
    .str.strip()
    .astype(float)
)

print("\n=== HASIL TRANSFORMASI DISKON ===")
print(df[["Diskon", "Diskon_Numeric"]].head(10))
# ============================================
# TRANSFORMASI TERJUAL
# ============================================

df["Terjual_Numeric"] = (
    df["Terjual"]
    .str.extract(r"(\d+)", expand=False)
    .astype(float)
)

print("\n=== HASIL TRANSFORMASI TERJUAL ===")
print(df[["Terjual", "Terjual_Numeric"]])
# ============================================
# STATISTIK DESKRIPTIF
# ============================================

print("\n=== STATISTIK DESKRIPTIF ===")

kolom_numerik = [
    "Harga_Numeric",
    "Harga_Asli_Numeric",
    "Diskon_Numeric",
    "Terjual_Numeric"
]

print(df[kolom_numerik].describe())
# ============================================
# DETEKSI OUTLIER DENGAN METODE IQR
# ============================================

print("\n=== DETEKSI OUTLIER IQR ===")

kolom_outlier = [
    "Harga_Numeric",
    "Harga_Asli_Numeric",
    "Diskon_Numeric",
    "Terjual_Numeric"
]

for kolom in kolom_outlier:

    data = df[kolom].dropna()

    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    batas_bawah = Q1 - 1.5 * IQR
    batas_atas = Q3 + 1.5 * IQR

    outlier = data[
        (data < batas_bawah) |
        (data > batas_atas)
    ]

    print(f"\n--- {kolom} ---")
    print(f"Q1          : {Q1}")
    print(f"Q3          : {Q3}")
    print(f"IQR         : {IQR}")
    print(f"Batas bawah : {batas_bawah}")
    print(f"Batas atas  : {batas_atas}")
    print(f"Jumlah outlier : {len(outlier)}")

    if len(outlier) > 0:
        print("Nilai outlier:")
        print(outlier.tolist())
        # ============================================
# MENAMPILKAN DATA YANG MENJADI OUTLIER
# ============================================

data_terjual = df["Terjual_Numeric"].dropna()

Q1 = data_terjual.quantile(0.25)
Q3 = data_terjual.quantile(0.75)
IQR = Q3 - Q1

batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

outlier_terjual = df[
    (df["Terjual_Numeric"] < batas_bawah) |
    (df["Terjual_Numeric"] > batas_atas)
]

print("\n=== DATA OUTLIER TERJUAL ===")
print(
    outlier_terjual[
        ["Judul", "Terjual", "Terjual_Numeric", "Harga_Numeric"]
    ]
)
# ============================================
# KORELASI ANTAR FITUR NUMERIK
# ============================================

print("\n=== KORELASI ANTAR FITUR ===")

fitur = [
    "Harga_Numeric",
    "Harga_Asli_Numeric",
    "Diskon_Numeric",
    "Terjual_Numeric"
]

korelasi = df[fitur].corr()

print(korelasi)
# ============================================
# FEATURE SELECTION
# ============================================

print("\n=== FEATURE SELECTION ===")

fitur_final = [
    "Harga_Numeric",
    "Diskon_Numeric",
    "Terjual_Numeric"
]

print("Fitur yang digunakan untuk clustering:")
print(fitur_final)

data_clustering = df[fitur_final].copy()

print("\n=== DATA CLUSTERING ===")
print(data_clustering.head(10))

print("\nJumlah data sebelum menghapus missing:")
print(len(data_clustering))

# Menghapus baris yang memiliki nilai kosong
data_clustering = data_clustering.dropna()

print("\nJumlah data setelah menghapus missing:")
print(len(data_clustering))

print("\nJumlah data yang digunakan untuk clustering:")
print(data_clustering.shape)
# ============================================
# NORMALISASI DATA
# ============================================

from sklearn.preprocessing import StandardScaler

print("\n=== NORMALISASI DATA ===")

scaler = StandardScaler()

data_scaled = scaler.fit_transform(data_clustering)

data_scaled = pd.DataFrame(
    data_scaled,
    columns=data_clustering.columns,
    index=data_clustering.index
)

print(data_scaled.head(10))
# ============================================
# K-MEANS CLUSTERING
# ============================================

from sklearn.cluster import KMeans

print("\n=== K-MEANS CLUSTERING ===")

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

data_clustering["Cluster"] = kmeans.fit_predict(data_scaled)

print("\nHasil clustering:")
print(data_clustering.head(10))

print("\nJumlah data setiap cluster:")
print(data_clustering["Cluster"].value_counts().sort_index())
# ============================================
# KARAKTERISTIK SETIAP CLUSTER
# ============================================

print("\n=== KARAKTERISTIK SETIAP CLUSTER ===")

karakteristik = data_clustering.groupby("Cluster")[
    ["Harga_Numeric", "Diskon_Numeric", "Terjual_Numeric"]
].mean()

print(karakteristik)
# ============================================
# VISUALISASI CLUSTERING
# ============================================

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

for cluster in sorted(data_clustering["Cluster"].unique()):
    data_cluster = data_clustering[
        data_clustering["Cluster"] == cluster
    ]

    plt.scatter(
        data_cluster["Harga_Numeric"],
        data_cluster["Terjual_Numeric"],
        label=f"Cluster {cluster}"
    )

plt.xlabel("Harga")
plt.ylabel("Jumlah Terjual")
plt.title("Hasil K-Means Clustering Buku Gramedia")
plt.legend()
plt.grid(True)

plt.savefig("hasil_clustering_gramedia.png")
plt.show()
# ============================================
# EVALUASI CLUSTERING
# ============================================

from sklearn.metrics import silhouette_score

silhouette = silhouette_score(
    data_scaled,
    data_clustering["Cluster"]
)

print("\n=== SILHOUETTE SCORE ===")
print("Silhouette Score:", silhouette)
# ============================================
# MENYIMPAN HASIL ANALISIS
# ============================================

data_clustering.to_csv(
    "dataset_buku_hasil_analisis.csv",
    index=False
)

print("\n=== DATA HASIL ANALISIS DISIMPAN ===")
print("File: dataset_buku_hasil_analisis.csv")
print("Jumlah data:", len(data_clustering))