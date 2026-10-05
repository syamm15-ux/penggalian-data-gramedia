# Penggalian Data - Web Scraping dan K-Means Clustering Gramedia

## Deskripsi

Project ini dibuat untuk memenuhi tugas mata kuliah Penggalian Data.

Project melakukan pengambilan data buku dari website Gramedia menggunakan web scraping, kemudian data yang diperoleh diproses melalui tahap preprocessing, analisis statistik, pemilihan fitur, standardisasi, dan K-Means Clustering.

## Tujuan

Tujuan project ini adalah:

1. Mengambil data buku dari website Gramedia menggunakan web scraping.
2. Melakukan preprocessing terhadap data hasil scraping.
3. Mengubah data yang masih berbentuk teks menjadi data numerik.
4. Melakukan analisis statistik dan deteksi outlier.
5. Melakukan analisis korelasi antarfitur.
6. Mengelompokkan data buku menggunakan algoritma K-Means.
7. Mengevaluasi hasil clustering menggunakan Silhouette Score.

## Dataset

Dataset diperoleh dari kategori Fiksi & Sastra pada website Gramedia.

Jumlah data hasil scraping:

- 70 data buku
- 6 atribut:
  - Judul
  - Terjual
  - Harga
  - Harga_Asli
  - Diskon
  - URL_Produk

## Preprocessing

Tahapan preprocessing yang dilakukan meliputi:

- Pemeriksaan data kosong
- Penanganan data kosong
- Transformasi harga menjadi numerik
- Transformasi diskon menjadi numerik
- Transformasi jumlah terjual menjadi numerik
- Deteksi outlier menggunakan metode IQR
- Analisis korelasi
- Pemilihan fitur

Dari 70 data awal, terdapat 51 data lengkap yang digunakan dalam proses clustering.

## Clustering

Algoritma yang digunakan:

**K-Means Clustering**

Fitur yang digunakan:

- Harga
- Diskon
- Terjual

Jumlah cluster:

**3 cluster**

Hasil pengelompokan:

| Cluster | Jumlah Data |
|---|---:|
| Cluster 0 | 32 |
| Cluster 1 | 18 |
| Cluster 2 | 1 |

## Evaluasi

Evaluasi clustering dilakukan menggunakan Silhouette Score.

Hasil:

**Silhouette Score = 0.4645**

## File Project

### `scraping_gramedia.py`

Program untuk melakukan web scraping data buku dari website Gramedia.

### `analisis_gramedia.py`

Program untuk melakukan preprocessing, analisis data, standardisasi, K-Means Clustering, dan evaluasi.

### `dataset_buku.csv`

Dataset mentah hasil web scraping sebanyak 70 data.

### `dataset_buku_hasil_analisis.csv`

Dataset hasil analisis yang digunakan dalam proses clustering sebanyak 51 data.

### `hasil_clustering_gramedia.png`

Visualisasi hasil K-Means Clustering.

## Tools dan Library

Project dibuat menggunakan Python dengan beberapa library:

- Pandas
- NumPy
- BeautifulSoup
- Selenium
- Matplotlib
- Scikit-learn

## Hasil

Hasil clustering menunjukkan adanya tiga kelompok buku dengan karakteristik yang berbeda berdasarkan harga, diskon, dan jumlah terjual.

Cluster 0 memiliki jumlah anggota paling banyak, yaitu 32 data. Cluster 1 memiliki 18 data, sedangkan Cluster 2 hanya memiliki 1 data dengan jumlah penjualan yang sangat tinggi.

## Catatan

Dataset dan hasil analisis dalam repository ini digunakan untuk keperluan pembelajaran dan praktikum mata kuliah Penggalian Data.
