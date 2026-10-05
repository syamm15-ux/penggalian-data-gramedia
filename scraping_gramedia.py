import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


# ============================================
# 1. URL WEBSITE & TARGET DATA
# ============================================

URL = "https://www.gramedia.com/categories/buku/fiksi-sastra"
TARGET_DATA = 70  # Jumlah minimum data yang ingin dikumpulkan


# ============================================
# 2. KONFIGURASI BROWSER (HEADLESS)
# ============================================

def buat_driver():
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)

    return driver


# ============================================
# 3. SCROLL & KLIK MUAT LEBIH BANYAK
# ============================================

def scroll_dan_hitung_buku(driver):

    tinggi_total = driver.execute_script(
        "return document.body.scrollHeight"
    )

    posisi = 0
    langkah = 600

    while posisi < tinggi_total:

        driver.execute_script(
            f"window.scrollTo(0, {posisi});"
        )

        time.sleep(0.3)

        posisi += langkah

        tinggi_total = driver.execute_script(
            "return document.body.scrollHeight"
        )

        time.sleep(1)

    return driver.page_source.count("/products/")


def klik_muat_lebih_banyak(driver):

    try:

        tombol = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Muat Lebih Banyak')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            tombol
        )

        time.sleep(0.5)

        tombol.click()

        time.sleep(2)

        return True

    except Exception:

        return False


def ambil_halaman(driver, url, target=70):

    print(f"Membuka halaman: {url}")

    driver.get(url)

    time.sleep(4)

    try:

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a[href*='/products/']"
                )
            )
        )

    except Exception:

        print(
            "Peringatan: timeout menunggu produk pertama muncul."
        )

    klik_ke = 0

    while True:

        jumlah = scroll_dan_hitung_buku(driver)

        print(
            f" Buku termuat saat ini: ~{jumlah // 2} "
            f"(klik 'Muat Lebih Banyak': {klik_ke}x)"
        )

        if jumlah // 2 >= target:

            print(
                f" Target {target} data tercapai, mulai parsing..."
            )

            break

        berhasil = klik_muat_lebih_banyak(driver)

        if not berhasil:

            print(
                " Tombol 'Muat Lebih Banyak' tidak ditemukan."
            )

            break

        klik_ke += 1

    return driver.page_source


# ============================================
# 4. MEMBACA HTML DENGAN BEAUTIFULSOUP
# ============================================

def parse_html(page_source):

    return BeautifulSoup(
        page_source,
        "html.parser"
    )


# ============================================
# 5. MENCARI SEMUA CARD BUKU
# ============================================

def cari_semua_buku(soup):

    books = soup.find_all(
        "a",
        href=lambda h: h and "gramedia.com/products/" in h
    )

    seen = set()
    unique_books = []

    for book in books:

        href = book.get("href", "")

        if href not in seen:

            seen.add(href)

            unique_books.append(book)

    return unique_books


# ============================================
# 6. FUNGSI AMBIL DATA TIAP BUKU
# ============================================

def ambil_judul(book):

    img = book.find("img")

    if img and img.get("alt", "").strip():

        return img["alt"].strip()

    return "N/A"


def ambil_terjual(book):

    for span in book.find_all("span"):

        teks = span.get_text(strip=True)

        if "terjual" in teks:

            return teks

    return "N/A"


def ambil_harga(book):

    for span in book.find_all("span"):

        teks = span.get_text(strip=True)

        if teks.startswith("Rp"):

            return teks

    return "N/A"


def ambil_harga_asli(book):

    harga_list = [
        span.get_text(strip=True)
        for span in book.find_all("span")
        if span.get_text(strip=True).startswith("Rp")
    ]

    if len(harga_list) >= 2:

        return harga_list[1]

    return "N/A"


def ambil_diskon(book):

    for span in book.find_all("span"):

        teks = span.get_text(strip=True)

        if teks.endswith("%") and len(teks) <= 4:

            return teks

    return "0%"


def ambil_url_produk(book):

    return book.get("href", "N/A")


# ============================================
# 7. KUMPULKAN SEMUA DATA
# ============================================

def kumpulkan_data(books):

    data = []

    for book in books:

        judul = ambil_judul(book)
        terjual = ambil_terjual(book)
        harga = ambil_harga(book)
        harga_ori = ambil_harga_asli(book)
        diskon = ambil_diskon(book)
        url = ambil_url_produk(book)

        if harga == "N/A":

            continue

        data.append({
            "Judul": judul,
            "Terjual": terjual,
            "Harga": harga,
            "Harga_Asli": harga_ori,
            "Diskon": diskon,
            "URL_Produk": url,
        })

    return data


# ============================================
# 8. PROGRAM UTAMA
# ============================================

def main():

    driver = buat_driver()

    try:

        page_source = ambil_halaman(
            driver,
            URL,
            target=TARGET_DATA
        )

        soup = parse_html(page_source)

        print(
            "Judul halaman:",
            soup.title.text if soup.title else "N/A"
        )

        books = cari_semua_buku(soup)

        print(
            f"Jumlah buku ditemukan: {len(books)}"
        )

        if books:

            print("\n--- UJI SATU BUKU ---")

            satu_buku = books[0]

            print(
                "Judul :",
                ambil_judul(satu_buku)
            )

            print(
                "Terjual :",
                ambil_terjual(satu_buku)
            )

            print(
                "Harga :",
                ambil_harga(satu_buku)
            )

            print(
                "Harga Asli :",
                ambil_harga_asli(satu_buku)
            )

            print(
                "Diskon :",
                ambil_diskon(satu_buku)
            )

            print(
                "URL :",
                ambil_url_produk(satu_buku)
            )

        data = kumpulkan_data(books)

    finally:

        driver.quit()

    df = pd.DataFrame(data)

    df = df.head(TARGET_DATA)

    print("\n=== DATA HASIL SCRAPING ===")

    print(df)

    print(
        f"\nTotal data: {len(df)} buku"
    )

    df.to_csv(
        "dataset_buku.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nData berhasil disimpan!")

    print("File: dataset_buku.csv")


if __name__ == "__main__":

    main()