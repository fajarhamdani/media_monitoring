# Aktifkan environment virtual terlebih dahulu
# Masuk ke Project/barata_monitoring
# Jalankan -> source ./bin/activate

import feedparser
import pandas as pd
from textblob import TextBlob
import time
import random
from datetime import datetime
from datetime import datetime, timedelta
import urllib.parse
import socket
from http.client import RemoteDisconnected

class JabarSmartMonitor:
    def __init__(self, keyword):
        self.keyword = keyword.strip().lower()
        self.all_results = []
        # Ambil tanggal hari ini dan Kemarin (Year-Month-Day)
        self.today = datetime.now().date()
        self.yesterday = self.today - timedelta(days=1)

        # Daftar wilayah target
        self.wilayah_data = [
            {"kabkot": "Kabupaten Bandung"},
            {"kabkot": "Kabupaten Bandung Barat"},
            {"kabkot": "Kabupaten Bekasi"},
            {"kabkot": "Kabupaten Bogor"},
            {"kabkot": "Kabupaten Ciamis"},
            {"kabkot": "Kabupaten Cianjur"},
            {"kabkot": "Kabupaten Cirebon"},
            {"kabkot": "Kabupaten Garut"},
            {"kabkot": "Kabupaten Indramayu"},
            {"kabkot": "Kabupaten Karawang"},
            {"kabkot": "Kabupaten Kuningan"},
            {"kabkot": "Kabupaten Majalengka"},
            {"kabkot": "Kabupaten Pangandaran"},
            {"kabkot": "Kabupaten Purwakarta"},
            {"kabkot": "Kabupaten Subang"},
            {"kabkot": "Kabupaten Sukabumi"},
            {"kabkot": "Kabupaten Sumedang"},
            {"kabkot": "Kabupaten Tasikmalaya"},
            {"kabkot": "Kota Bandung"},
            {"kabkot": "Kota Banjar"},
            {"kabkot": "Kota Bekasi"},
            {"kabkot": "Kota Bogor"},
            {"kabkot": "Kota Cimahi"},
            {"kabkot": "Kota Cirebon"},
            {"kabkot": "Kota Depok"},
            {"kabkot": "Kota Sukabumi"},
            {"kabkot": "Kota Tasikmalaya"},
        ]

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
    def fetch_feed(self, url, source_name, kab, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                # Use a real browser User-Agent to avoid being flagged as a bot
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                
                feed = feedparser.parse(url, agent=user_agent)

                # Check if Google sent a 429 (Too Many Requests)
                if hasattr(feed, 'status') and feed.status == 429:
                    wait_time = 60 * (retries + 1) # Wait 1-3 minutes
                    print(f"⚠️ Rate limited by Google. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                    continue

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
                                'Sumber': source_name,
                                'Waktu_Publikasi': pub_time.strftime('%Y-%m-%d %H:%M'),
                                'Jenis Bencana': self.keyword,
                                'Kabupaten': kab,
                                'Judul': entry.title,
                                # 'Sentimen': "Positif" if sentiment_score > 0 else "Negatif" if sentiment_score < 0 else "Netral",
                                'Link': entry.link
                            })
                    except:
                        continue
                return
            except (RemoteDisconnected, socket.timeout, ConnectionResetError) as e:
                retries += 1
                wait = random.uniform(5.0, 10.0) * retries
                print(f"🔄 Connection lost ({e}). Retry {retries}/{max_retries} in {wait:.1f}s...")
                time.sleep(wait)

        print(f"❌ Failed to fetch {source_name} after {max_retries} attempts.")

    def run_monitoring(self):
        print(f"--- Memulai Monitoring Otomatis untuk '{self.keyword}' ---\n")
        print(f"--- Monitoring Hari Kemarin ({self.yesterday}) s/d Hari Ini ({self.today}) ---\n")
        
        for index, row in enumerate(self.wilayah_data):
            kab = row['kabkot'].strip()
    
            print(f"[{index+1}] Memantau Berita dan Media Sosial yang berkaitan dengan {self.keyword} {kab}")
            
            # 1. Gabungkan query dan bersihkan spasi berlebih
            query_raw = f"{self.keyword} {kab}"
            query_clean = " ".join(query_raw.split()).strip() # Menghapus spasi ganda jika ada

            # 2. Encode query agar aman untuk URL (mengubah spasi jadi %20 atau +)
            query_encoded = urllib.parse.quote(query_clean)

            # 3. Cek via Google News (Spesifik wilayah)
            google_url = self.sources["Google News"].format(query=query_encoded)
            self.fetch_feed(google_url, "Google News", kab)

            # 4. Instagram Search via Google
            # Searches for the keyword + location on instagram.com
            query_ig = urllib.parse.quote(f"site:instagram.com {self.keyword} {kab}")
            self.fetch_feed(self.sources["Google News"].format(query=query_ig), "Instagram (via Google)", kab)

            # 5. TikTok Search via Google
            query_tt = urllib.parse.quote(f"site:tiktok.com {self.keyword} {kab}")
            self.fetch_feed(self.sources["Google News"].format(query=query_tt), "TikTok (via Google)", kab)

            # 6. Cek Sumber Lain (RSS Terkini)
            # cek sekali untuk setiap sumber non-Google agar tidak redundan
            if index == 0: # Cek feed umum hanya di iterasi pertama
                for name, url in self.sources.items():
                    if name != "Google News":
                        self.fetch_feed(url, name, kab)

            # IMPORTANT: Randomized sleep between EVERY sub-query
            wait_time = random.uniform(3.0, 7.0) 
            time.sleep(wait_time)

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
            
            output_name = f"media_monitoring_{self.keyword}_jabar_{datetime.now().strftime('%Y-%m-%d %H%M%S')}.xlsx"
            df_final.to_excel(output_name, index=False)

            print(f"\n✅ Monitoring Selesai! Hasil disimpan di: {output_name}")
        else:
            print("\n❌ Tidak ada berita yang ditemukan untuk daftar wilayah tersebut.")

# --- EKSEKUSI ---
if __name__ == "__main__":
    # Pastikan file 'daftar_wilayah.xlsx' sudah ada di folder yang sama
    topik = input("Masukkan Jenis Bencana yang ingin dipantau: ")
    
    app = JabarSmartMonitor(topik)
    app.run_monitoring()
