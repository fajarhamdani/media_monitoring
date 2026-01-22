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
        self.seen_links = set()
        self.trending_tags = ["viral", "info", "terkini", "update", "hot", "populer", "hits", "terbaru", "explore", "fyp", "foryoupage", "trending", "news", "breaking", "headline", "berita", "jabar", "jawa barat", "bandung", "lembang", "bandung utara", "puncak bogor", "depok", "bekasi", "bogor", "sukabumi", "tasikmalaya", "tasik", "cimahi", "karawang", "purwakarta", "subang", "indramayu", "cirebon", "garut", "sumedang", "ciamis", "kuningan", "majalengka", "pangandaran", "bandung barat", "kbb", "cianjur", "ciamis", "banjar", "banjir", "longsor", "gempa", "angin kencang", "puting beliung", "tanah longsor", "banjir bandang", "erupsi", "gunung meletus", "kebakaran hutan", "kebakaran lahan", "bencana alam", "bencana", "darurat", "evakuasi", "tanggap darurat", "pohon tumbang", "jalan putus", "jembatan putus", "luapan sungai", "hujan deras", "tsunami", "letusan gunung", "gunung api", "cuaca ekstrem", "angin kencang", "hujan lebat", "banjir rob", "banjir pesisir", "angin puting beliung", "kebakaran", "bencana banjir", "bencana longsor", "bencana gempa", "bencana angin", "bencana tanah longsor", "bencana erupsi", "bencana kebakaran", "bencana cuaca ekstrem", "info bencana", "update bencana", "berita bencana", "tanggap bencana", "bencana banjir bandang", "bencana alam jabar", "bencana jawa barat", "bencana di jabar", "bencana di jawa barat", "bencana di bandung", "bencana di bekasi", "bencana di bogor", "bencana di sukabumi", "bencana di tasikmalaya", "bencana di cimahi", "bencana di karawang", "bencana di purwakarta", "bencana di subang", "bencana di indramayu", "bencana di cirebon", "bencana di garut", "bencana di sumedang", "bencana di ciamis", "bencana di kuningan", "bencana di majalengka", "bencana di pangandaran", "bencana di bandung barat", "info bencana jabar", "info bencana jawa barat", "info bencana bandung", "info bencana bekasi", "info bencana bogor", "info bencana sukabumi", "info bencana tasikmalaya", "info bencana cimahi", "info bencana karawang", "info bencana purwakarta", "info bencana subang", "info bencana indramayu", "info bencana cirebon", "info bencana garut", "info bencana sumedang", "info bencana ciamis", "info bencana kuningan", "info bencana majalengka", "info bencana pangandaran", "info bencana bandung barat", "update bencana jabar", "update bencana jawa barat", "update bencana bandung", "update bencana bekasi", "update bencana bogor", "update bencana sukabumi", "update bencana tasikmalaya", "update bencana cimahi", "update bencana karawang", "update bencana purwakarta", "update bencana subang", "update bencana indramayu", "update bencana cirebon", "update bencana garut", "update bencana sumedang", "update bencana ciamis", "update bencana kuningan", "update bencana majalengka", "update bencana pangandaran", "update bencana bandung barat", "berita bencana jabar", "berita bencana jawa barat", "berita bencana bandung", "berita bencana bekasi", "berita bencana bogor", "berita bencana sukabumi", "berita bencana tasikmalaya", "berita bencana cimahi", "berita bencana karawang", "berita bencana purwakarta", "berita bencana subang", "berita bencana indramayu", "berita bencana cirebon", "berita bencana garut", "berita bencana sumedang", "berita bencana ciamis", "berita bencana kuningan", "berita bencana majalengka", "berita bencana pangandaran", "berita bencana bandung barat", "batununggal", "ujungberung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "andir", "regol", "astanaanyar", "mandalajati", "cinambo", "rancasari", "batununggal", "ujung berung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "andir", "regol", "astana anyar", "mandalajati", "cinambo", "rancasari", "cileungsi", "cibinong", "tajur halang", "bojong gede", "gunung putri", "ciomas", "ciherang", "jasinga", "parung", "rancabungur", "sukajaya", "sukamakmur", "tajur", "cileungsi", "cibinong", "tajur halang", "bojong gede", "gunung putri", "ciomas", "ciherang", "jasinga", "parung", "rancabungur", "sukajaya", "sukamakmur", "lembang", "ciwidey", "dayeuhkolot", "banjaran", "cimenyan", "ciparay", "pangalengan", "rancaekek", "soreang", "cicalengka", "katapang", "ciwidey", "dayeuh kolot", "banjaran", "cimenyan", "cikakak", "panumbangan", "langkaplancar", "parigi", "cihampelas", "cisompet", "cibalong", "pamarican", "sukaresik", "cikakak", "panumbangan", "langkap lancar", "parigi", "cihampelas", "cisompet", "cibalong", "pamarican", "sukaresik", "jatinangor", "sumedang selatan", "sumedang utara", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "jatinangor", "sumedang selatan", "sumedang utara", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "cibeber", "cikadongdong", "cigugur", "cijulang", "langkaplancar", "pangandaran", "parigi", "cibeber", "cikadongdong", "cigugur", "cijulang", "langkap lancar", "pangandaran", "parigi", "kopo", "wanaraja", "malangbong", "sindangagung", "cikajang", "cibatu", "cikelet", "singajaya", "kopo", "wanaraja", "malangbong", "sindang agung", "cikajang", "cibatu", "cikelet", "singajaya", "cipatujah", "mangunjaya", "pancatengah", "cibalong", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cibalong", "pamarican", "sukaresik", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "gede", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "gede", "losarang", "gabuswetan", "pangenan", "jatisari", "karangsembung", "plumbon", "losarang", "gabuswetan", "pangenan", "jatisari", "karangsembung", "cilimus", "jamblang", "arjawinangun", "gede", "cikedung", "cilimus", "jamblang", "arjawinangun", "gede", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "cibingbin", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "sukaresik", "cibingbin", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "sukaresik", "losari", "gabuswetan", "pangenan", "jatisari", "karangsembung", "losari", "gabuswetan", "pangenan", "jatisari", "karangsembung", "klangenan", "karangjaya", "lelea", "sedong", "jatisari", "plumbon", "klangenan", "karangjaya", "lelea", "sedong", "jatisari", "plumbon", "sukahaji", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "cigugur", "lumbung", "kertasari", "melong", "kertajati", "sindangwangi", "dawuan", "jatisari", "lelea", "kertajati", "sindangwangi", "dawuan", "jatisari", "lelea", "wado", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "wado", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "cantigi", "cimaragas", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cantigi", "cimaragas", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cisalak", "cijulang", "langkaplancar", "pangandaran", "parigi", "cisalak", "cijulang", "langkap lancar", "pangandaran", "parigi", "pamanukan", "purwadadi", "tegalwaru", "jatisari", "karangsembung", "pamanukan", "purwadadi", "tegalwaru", "jatisari", "karangsembung", "jatiluhur", "purwakarta", "sukasari", "wanayasa", "jatisari", "jatiluhur", "purwakarta", "sukasari", "wanayasa", "cibatu", "cikajang", "cikelet", "singajaya", "kopo", "cibatu", "cikajang", "cikelet", "singajaya", "kopo", "rengasdengklok", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "rengasdengklok", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "bangunrejo", "kedungwaringin", "cibitung", "sukawangi", "sukatani", "lembaran", "bangunrejo", "kedungwaringin", "cibitung", "sukawangi", "sukatani", "lembaran", "mukmin", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "mukmin", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "cibitung", "kedungwaringin", "sukawangi", "sukatani", "lembaran", "cibitung", "kedungwaringin", "sukawangi", "sukatani", "lembaran", "cikarang barat", "cikarang selatan", "cikarang utara", "cikarang pusat", "cibarusah", "cilamaya", "tarumajaya", "cikarang barat", "cikarang selatan", "cikarang utara", "cikarang pusat", "cibarusah", "cilamaya", "tarumajaya", "parongpong", "cisauk", "pamulang", "serpong", "setu", "cisauk", "pamulang", "serpong", "setu", "padalarang", "ngamprah", "cipatat", "cililin", "cikalongwetan", "cipongkor", "cisurupan", "padalarang", "ngamprah", "cipatat", "cililin", "cikalongwetan", "cipongkor", "cisurupan", "cikole", "cipanas", "sukasari", "lembang", "ciwidey", "cikalongwetan", "cikole", "cipanas", "sukasari", "lembang", "ciwidey", "cikalongwetan", "regol", "andr", "astanaanyar", "mandalajati", "cinambo", "rancasari", "batununggal", "ujungberung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "regol", "andir", "astana anyar", "mandalajati", "cinambo", "rancasari", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cihideung", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "cihideung", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "tawang", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "tawang", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "pataruman", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "pataruman", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "langensari", "cijulang", "langkaplancar", "pangandaran", "parigi", "langensari", "cijulang", "langkap lancar", "pangandaran", "parigi"]

        # Daftar wilayah target
        self.wilayah_data = [
            {"kabkot": "Bandung"},
            {"kabkot": "Bandung Barat"},
            {"kabkot": "Bekasi"},
            {"kabkot": "Bogor"},
            {"kabkot": "Ciamis"},
            {"kabkot": "Cianjur"},
            {"kabkot": "Cirebon"},
            {"kabkot": "Garut"},
            {"kabkot": "Indramayu"},
            {"kabkot": "Karawang"},
            {"kabkot": "Kuningan"},
            {"kabkot": "Majalengka"},
            {"kabkot": "Pangandaran"},
            {"kabkot": "Purwakarta"},
            {"kabkot": "Subang"},
            {"kabkot": "Sukabumi"},
            {"kabkot": "Sumedang"},
            {"kabkot": "Tasikmalaya"},
            {"kabkot": "Banjar"},
            {"kabkot": "Cimahi"},
            {"kabkot": "Depok"},
            {"kabkot": "Jawa Barat"},
        ]

        # Daftar sumber berita (RSS Feeds)
        self.sources = {
          "Top Stories": "https://news.google.com/rss/search?q={query}?+when:1d&hl=id&gl=ID&ceid=ID:id",
          "Google News": "https://news.google.com/rss/search?q={query}&hl=id&gl=ID&ceid=ID:id"
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

                for entry in feed.entries:
                    try:
                        # Validasi Duplikasi Link
                        current_link = entry.link
                        if current_link in self.seen_links:
                            continue # Lewati jika link sudah pernah ditemukan sebelumnya

                        # Parsing tanggal publikasi
                        pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                        pub_date = pub_time.date()

                        # mengandung kata kunci atau nama wilayah
                        title = entry.title.lower()
                        content = entry.get('summary', '').lower()
                        
                        # Cek apakah berita relevan dengan wilayah atau keyword
                        is_relevant = any(x.lower() in (title + content) for x in [self.keyword, kab])

                        self.seen_links.add(current_link)

                        # Filter: Harus Hari Ini/Kemarin dan Relevan
                        if (pub_date == self.yesterday or pub_date == self.today) and is_relevant:
                            sentiment_score = TextBlob(entry.title).sentiment.polarity
                            self.all_results.append({
                                'Sumber': source_name,
                                'Waktu_Publikasi': pub_time.strftime('%Y-%m-%d'),
                                'Jenis Bencana': self.keyword,
                                'Kab Kota': kab,
                                'Judul': entry.title,
                                # 'Sentimen': "Positif" if sentiment_score > 0 else "Negatif" if sentiment_score < 0 else "Netral",
                                'Link': current_link
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
        
        # Gabungkan trending tags menjadi string untuk query: (viral OR hot OR ...)
        trending_query = "(" + " OR ".join(self.trending_tags) + ")"

        for index, row in enumerate(self.wilayah_data):
            kab = row['kabkot'].strip()
    
            print(f"[{index+1}] Memantau Media Online dan Media Sosial tentang {self.keyword} {kab}")
            
            # 1. Gabungkan query dan bersihkan spasi berlebih
            query_raw = f"{self.keyword} {kab}"
            query_clean = " ".join(query_raw.split()).strip() # Menghapus spasi ganda jika ada

            # 2. Encode query agar aman untuk URL (mengubah spasi jadi %20 atau +)
            query_encoded = urllib.parse.quote(query_clean)

            # 3. Cek via Google News (Top Stories)
            url_top = self.sources["Google News"].format(query=query_encoded)
            self.fetch_feed(url_top, "Media Online", kab)

            # 4. Cek via Google News (Spesifik wilayah)
            google_url = self.sources["Google News"].format(query=query_encoded)
            self.fetch_feed(google_url, "Media Online", kab)

            # 5. Instagram
            # Searches for the keyword + location on instagram.com
            query_ig = urllib.parse.quote(f"site:instagram.com {self.keyword} {kab} {trending_query} when:1d")
            self.fetch_feed(self.sources["Google News"].format(query=query_ig), "Instagram", kab)

            # 6. TikTok
            query_tt = urllib.parse.quote(f"site:tiktok.com {self.keyword} {kab} {trending_query} when:1d")
            self.fetch_feed(self.sources["Google News"].format(query=query_tt), "TikTok", kab)

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
            # df_final = df_final.dropna(subset=['Waktu_Publikasi'])

            # 3. Sort Descending berdasarkan Waktu_Publikasi (Terbaru di atas)
            df_final = df_final.sort_values(by='Waktu_Publikasi', ascending=False)
            
            # 4. Format ulang tampilan tanggal sebelum disimpan ke Excel
            df_final['Waktu_Publikasi'] = df_final['Waktu_Publikasi'].dt.strftime('%Y-%m-%d')
            
            output_name = f"{datetime.now().strftime('%Y-%m-%d %H%M%S')}_media_monitoring_{self.keyword}_jabar.xlsx"
            df_final.to_excel(output_name, index=False)

            print(f"\n✅ Monitoring Selesai! Hasil disimpan di: {output_name}")
        else:
            print("\n❌ Tidak ada berita yang ditemukan untuk daftar wilayah tersebut.")

# --- EKSEKUSI ---
if __name__ == "__main__":
    topik = input("Masukkan Jenis Bencana yang ingin dipantau: ")
    
    app = JabarSmartMonitor(topik)
    app.run_monitoring()


# ============================================================
#        SMART NEWS & SOCIAL MEDIA MONITORING (v3.0)
# ============================================================

# Aplikasi ini dirancang untuk memantau berita terkini dan 
# konten viral dari berbagai sumber (News, Instagram, TikTok) 
# berdasarkan wilayah Kabupaten, Kecamatan, dan Desa di Jawa Barat.

# CARA PENGGUNAAN:
# ----------------
# 1.  Klik dua kali pada file 'MediaMonitoring_V3.exe'.
# 2.  Sebuah jendela hitam (Terminal) akan terbuka.
# 3.  Tunggu hingga proses monitoring selesai. Aplikasi akan 
#     memproses wilayah satu per satu.
# 4.  Laporan hasil pemantauan akan otomatis tersimpan dalam 
#     format Excel (.xlsx) di folder yang sama dengan aplikasi.

# FITUR UTAMA:
# ------------
# - Pencarian Berita Lokal (Antara Jabar, Republika, dll).
# - Deteksi Konten Viral (Instagram & TikTok).
# - Analisis Sentimen Otomatis (Positif, Negatif, Netral).
# - Laporan Terstruktur dalam format Excel.

# MASALAH YANG MUNGKIN TERJADI (FAQ):
# -----------------------------------
# 1. Windows Defender / Antivirus Muncul:
#    Karena aplikasi ini dibuat secara mandiri (tidak memiliki 
#    sertifikat berbayar), Windows mungkin akan menampilkan 
#    "Windows protected your PC".
#    SOLUSI: Klik "More Info" lalu pilih "Run Anyway".

# 2. Error Koneksi (Rate Limit):
#    Jika aplikasi berhenti lama atau muncul pesan "Rate Limited", 
#    itu berarti Google membatasi akses sementara. 
#    Aplikasi akan otomatis mencoba lagi (Retry) dalam beberapa menit.

# 3. File Excel Tidak Terbuka:
#    Pastikan Anda telah menutup file Excel hasil monitoring 
#    sebelum menjalankan ulang aplikasi untuk menghindari error.

# Dibuat untuk monitoring efisien tingkat kewilayahan.
# ============================================================
