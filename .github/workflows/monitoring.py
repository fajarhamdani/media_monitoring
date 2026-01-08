import feedparser
import pandas as pd
from textblob import TextBlob
import time
from datetime import datetime
from datetime import datetime, timedelta
import urllib.parse

class JabarAutoMonitor:
    def __init__(self, excel_file, keyword):
        self.excel_file = excel_file
        self.keyword = keyword
        self.all_results = []
        # Ambil tanggal hari ini dan Kemarin (Year-Month-Day)
        self.today = datetime.now().date()
        self.yesterday = self.today - timedelta(days=1)

        # Daftar sumber berita (RSS Feeds)
        self.sources = {
          "Google News": "https://news.google.com/rss/search?q={query}&hl=id&gl=ID&ceid=ID:id",
          "Antara News": "https://www.antaranews.com/rss/terkini.xml",
          "Republika": "https://www.republika.co.id/rss/",
          "Antara Jabar": "https://jabar.antaranews.com/rss/terkini.xml",
          "Republika Jabar": "https://www.republika.co.id/rss/nusantara/jawa-barat",
          "Tempo": "https://rss.tempo.co/index.php/teks/terkini"
        }

    # def fetch_feed(self, url, source_name, kab, kec):
    def fetch_feed(self, url, source_name, kab):
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            try:
                # Parsing tanggal publikasi
                pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                pub_date = pub_time.date()

                # mengandung kata kunci atau nama wilayah
                title = entry.title.lower()
                content = entry.get('summary', '').lower()
                
                # Cek apakah berita relevan dengan wilayah atau keyword
                is_relevant = any(x.lower() in (title + content) for x in [self.keyword, kab])

                # Filter: Harus Hari Ini/Kemarin dan Relevan
                if (pub_date == self.yesterday or pub_date == self.today) and is_relevant:
                    sentiment_score = TextBlob(entry.title).sentiment.polarity
                    self.all_results.append({
                        # 'Sumber': source_name,
                        'Waktu_Publikasi': pub_time.strftime('%Y-%m-%d %H:%M'),
                        'Jenis Bencana': self.keyword,
                        'Kabupaten': kab,
                        'Judul': entry.title,
                        # 'Sentimen': "Positif" if sentiment_score > 0 else "Negatif" if sentiment_score < 0 else "Netral",
                        'Link': entry.link
                    })
            except:
                continue

    def run_monitoring(self):
        # 1. Membaca daftar wilayah dari Excel
        try:
            df_wilayah = pd.read_excel(self.excel_file)
        except Exception as e:
            print(f"Gagal membaca file Excel: {e}")
            return

        print(f"--- Memulai Monitoring Otomatis untuk '{self.keyword}' ---\n")
        print(f"--- Monitoring Hari Kemarin ({self.yesterday}) s/d Hari Ini ({self.today}) ---\n")

        # 2. Iterasi setiap baris di Excel
        for index, row in df_wilayah.iterrows():
            kab = row['kabupaten_kota'].strip()
            
            print(f"[{index+1}] Memantau Berita yang berkaitan dengan {self.keyword} {kab}")
            
            # 1. Gabungkan query dan bersihkan spasi berlebih
            query_raw = f"{self.keyword} {kab}"
            query_clean = " ".join(query_raw.split()).strip() # Menghapus spasi ganda jika ada

            # 2. Encode query agar aman untuk URL (mengubah spasi jadi %20 atau +)
            query_encoded = urllib.parse.quote(query_clean)

            # 3. Cek via Google News (Spesifik wilayah)
            google_url = self.sources["Google News"].format(query=query_encoded)
            # self.fetch_feed(google_url, "Google News", kab, kec)
            self.fetch_feed(google_url, "Google News", kab)

            # 4. Cek Sumber Lain (RSS Terkini)
            # cek sekali untuk setiap sumber non-Google agar tidak redundan
            if index == 0: # Cek feed umum hanya di iterasi pertama
                for name, url in self.sources.items():
                    if name != "Google News":
                        # self.fetch_feed(url, name, kab, kec)
                        self.fetch_feed(url, name, kab)

            # Delay kecil agar tidak terkena blokir (rate limit) oleh Google
            time.sleep(1) # Jeda singkat

        self.save_results()

    def save_results(self):
        if self.all_results:
            df_final = pd.DataFrame(self.all_results)

            # --- LOGIKA SORTING & CLEANING ---
            
            # 1. PAKSA konversi kolom ke datetime (Solusi AttributeError)
            # errors='coerce' akan mengubah data yang rusak menjadi NaT (Not a Time) agar tidak error
            df_final['Waktu_Publikasi'] = pd.to_datetime(df_final['Waktu_Publikasi'], errors='coerce')

            # 2. Hapus baris jika ada yang gagal dikonversi (NaT)
            df_final = df_final.dropna(subset=['Waktu_Publikasi'])

            # 3. Sort Descending berdasarkan Waktu_Publikasi (Terbaru di atas)
            df_final = df_final.sort_values(by='Waktu_Publikasi', ascending=False)
            
            # 4. Format ulang tampilan tanggal sebelum disimpan ke Excel
            df_final['Waktu_Publikasi'] = df_final['Waktu_Publikasi'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            output_name = f"list_media_monitoring_jabar_{datetime.now().strftime('%Y-%m-%d %H%M%S')}.xlsx"
            df_final.to_excel(output_name, index=False)

            print(f"\n✅ Monitoring Selesai! Hasil disimpan di: {output_name}")
        else:
            print("\n❌ Tidak ada berita yang ditemukan untuk daftar wilayah tersebut.")

# --- EKSEKUSI ---
if __name__ == "__main__":
    # Pastikan file 'daftar_wilayah.xlsx' sudah ada di folder yang sama
    topik = input("Masukkan Jenis Bencana yang ingin dipantau: ")
    
    # app = JabarAutoMonitor("daftar_wilayah.xlsx", topik)
    app = JabarAutoMonitor("daftar_wilayah_kabkot.xlsx", topik)
    app.run_monitoring()