# source venv/bin/activate

import feedparser
import pandas as pd
from textblob import TextBlob
import time
import random
from datetime import datetime, timedelta
import urllib.parse
import socket
from http.client import RemoteDisconnected
from tqdm import tqdm

class JabarSmartMonitor:
    def __init__(self):
        # 1. VARIABLE KEYWORD STATIS
        self.keywords_list = [
            "banjir", "longsor", "cuaca ekstrem", "puting beliung", "pohon tumbang",
            "kebakaran", "tsunami", "gempa", "gunung meletus", "erupsi gunung"
        ]
        
        self.all_results = []
        self.today = datetime.now().date()
        self.yesterday = self.today - timedelta(days=1)
        self.seen_links = set()
        
        # Tag trending untuk mempersempit pencarian medsos
        self.trending_tags = ["viral", "info", "terkini", "update", "hot", "populer", "hits", "terbaru", "explore", "fyp", "foryoupage", "trending", "news", "breaking", "headline", "berita", "jabar", "jawa barat", "bandung", "lembang", "bandung utara", "puncak bogor", "depok", "bekasi", "bogor", "sukabumi", "tasikmalaya", "tasik", "cimahi", "karawang", "purwakarta", "subang", "indramayu", "cirebon", "garut", "sumedang", "ciamis", "kuningan", "majalengka", "pangandaran", "bandung barat", "kbb", "cianjur", "ciamis", "banjar", "banjir", "longsor", "gempa", "angin kencang", "puting beliung", "tanah longsor", "banjir bandang", "erupsi", "gunung meletus", "kebakaran hutan", "kebakaran lahan", "bencana alam", "bencana", "darurat", "evakuasi", "tanggap darurat", "pohon tumbang", "jalan putus", "jembatan putus", "luapan sungai", "hujan deras", "tsunami", "letusan gunung", "gunung api", "cuaca ekstrem", "angin kencang", "hujan lebat", "banjir rob", "banjir pesisir", "angin puting beliung", "kebakaran", "bencana banjir", "bencana longsor", "bencana gempa", "bencana angin", "bencana tanah longsor", "bencana erupsi", "bencana kebakaran", "bencana cuaca ekstrem", "info bencana", "update bencana", "berita bencana", "tanggap bencana", "bencana banjir bandang", "bencana alam jabar", "bencana jawa barat", "bencana di jabar", "bencana di jawa barat", "bencana di bandung", "bencana di bekasi", "bencana di bogor", "bencana di sukabumi", "bencana di tasikmalaya", "bencana di cimahi", "bencana di karawang", "bencana di purwakarta", "bencana di subang", "bencana di indramayu", "bencana di cirebon", "bencana di garut", "bencana di sumedang", "bencana di ciamis", "bencana di kuningan", "bencana di majalengka", "bencana di pangandaran", "bencana di bandung barat", "info bencana jabar", "info bencana jawa barat", "info bencana bandung", "info bencana bekasi", "info bencana bogor", "info bencana sukabumi", "info bencana tasikmalaya", "info bencana cimahi", "info bencana karawang", "info bencana purwakarta", "info bencana subang", "info bencana indramayu", "info bencana cirebon", "info bencana garut", "info bencana sumedang", "info bencana ciamis", "info bencana kuningan", "info bencana majalengka", "info bencana pangandaran", "info bencana bandung barat", "update bencana jabar", "update bencana jawa barat", "update bencana bandung", "update bencana bekasi", "update bencana bogor", "update bencana sukabumi", "update bencana tasikmalaya", "update bencana cimahi", "update bencana karawang", "update bencana purwakarta", "update bencana subang", "update bencana indramayu", "update bencana cirebon", "update bencana garut", "update bencana sumedang", "update bencana ciamis", "update bencana kuningan", "update bencana majalengka", "update bencana pangandaran", "update bencana bandung barat", "berita bencana jabar", "berita bencana jawa barat", "berita bencana bandung", "berita bencana bekasi", "berita bencana bogor", "berita bencana sukabumi", "berita bencana tasikmalaya", "berita bencana cimahi", "berita bencana karawang", "berita bencana purwakarta", "berita bencana subang", "berita bencana indramayu", "berita bencana cirebon", "berita bencana garut", "berita bencana sumedang", "berita bencana ciamis", "berita bencana kuningan", "berita bencana majalengka", "berita bencana pangandaran", "berita bencana bandung barat", "batununggal", "ujungberung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "andir", "regol", "astanaanyar", "mandalajati", "cinambo", "rancasari", "batununggal", "ujung berung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "andir", "regol", "astana anyar", "mandalajati", "cinambo", "rancasari", "cileungsi", "cibinong", "tajur halang", "bojong gede", "gunung putri", "ciomas", "ciherang", "jasinga", "parung", "rancabungur", "sukajaya", "sukamakmur", "tajur", "cileungsi", "cibinong", "tajur halang", "bojong gede", "gunung putri", "ciomas", "ciherang", "jasinga", "parung", "rancabungur", "sukajaya", "sukamakmur", "lembang", "ciwidey", "dayeuhkolot", "banjaran", "cimenyan", "ciparay", "pangalengan", "rancaekek", "soreang", "cicalengka", "katapang", "ciwidey", "dayeuh kolot", "banjaran", "cimenyan", "cikakak", "panumbangan", "langkaplancar", "parigi", "cihampelas", "cisompet", "cibalong", "pamarican", "sukaresik", "cikakak", "panumbangan", "langkap lancar", "parigi", "cihampelas", "cisompet", "cibalong", "pamarican", "sukaresik", "jatinangor", "sumedang selatan", "sumedang utara", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "jatinangor", "sumedang selatan", "sumedang utara", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "cibeber", "cikadongdong", "cigugur", "cijulang", "langkaplancar", "pangandaran", "parigi", "cibeber", "cikadongdong", "cigugur", "cijulang", "langkap lancar", "pangandaran", "parigi", "kopo", "wanaraja", "malangbong", "sindangagung", "cikajang", "cibatu", "cikelet", "singajaya", "kopo", "wanaraja", "malangbong", "sindang agung", "cikajang", "cibatu", "cikelet", "singajaya", "cipatujah", "mangunjaya", "pancatengah", "cibalong", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cibalong", "pamarican", "sukaresik", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "gede", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "gede", "losarang", "gabuswetan", "pangenan", "jatisari", "karangsembung", "plumbon", "losarang", "gabuswetan", "pangenan", "jatisari", "karangsembung", "cilimus", "jamblang", "arjawinangun", "gede", "cikedung", "cilimus", "jamblang", "arjawinangun", "gede", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "cibingbin", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "sukaresik", "cibingbin", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "sukaresik", "losari", "gabuswetan", "pangenan", "jatisari", "karangsembung", "losari", "gabuswetan", "pangenan", "jatisari", "karangsembung", "klangenan", "karangjaya", "lelea", "sedong", "jatisari", "plumbon", "klangenan", "karangjaya", "lelea", "sedong", "jatisari", "plumbon", "sukahaji", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "cigugur", "lumbung", "kertasari", "melong", "kertajati", "sindangwangi", "dawuan", "jatisari", "lelea", "kertajati", "sindangwangi", "dawuan", "jatisari", "lelea", "wado", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "wado", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "cantigi", "cimaragas", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cantigi", "cimaragas", "pamarican", "sukaresik", "cipatujah", "mangunjaya", "pancatengah", "cisalak", "cijulang", "langkaplancar", "pangandaran", "parigi", "cisalak", "cijulang", "langkap lancar", "pangandaran", "parigi", "pamanukan", "purwadadi", "tegalwaru", "jatisari", "karangsembung", "pamanukan", "purwadadi", "tegalwaru", "jatisari", "karangsembung", "jatiluhur", "purwakarta", "sukasari", "wanayasa", "jatisari", "jatiluhur", "purwakarta", "sukasari", "wanayasa", "cibatu", "cikajang", "cikelet", "singajaya", "kopo", "cibatu", "cikajang", "cikelet", "singajaya", "kopo", "rengasdengklok", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "rengasdengklok", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "bangunrejo", "kedungwaringin", "cibitung", "sukawangi", "sukatani", "lembaran", "bangunrejo", "kedungwaringin", "cibitung", "sukawangi", "sukatani", "lembaran", "mukmin", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "mukmin", "tarumajaya", "jatiasih", "setu", "bojongmangu", "cibarusah", "serang baru", "cibitung", "kedungwaringin", "sukawangi", "sukatani", "lembaran", "cibitung", "kedungwaringin", "sukawangi", "sukatani", "lembaran", "cikarang barat", "cikarang selatan", "cikarang utara", "cikarang pusat", "cibarusah", "cilamaya", "tarumajaya", "cikarang barat", "cikarang selatan", "cikarang utara", "cikarang pusat", "cibarusah", "cilamaya", "tarumajaya", "parongpong", "cisauk", "pamulang", "serpong", "setu", "cisauk", "pamulang", "serpong", "setu", "padalarang", "ngamprah", "cipatat", "cililin", "cikalongwetan", "cipongkor", "cisurupan", "padalarang", "ngamprah", "cipatat", "cililin", "cikalongwetan", "cipongkor", "cisurupan", "cikole", "cipanas", "sukasari", "lembang", "ciwidey", "cikalongwetan", "cikole", "cipanas", "sukasari", "lembang", "ciwidey", "cikalongwetan", "regol", "andr", "astanaanyar", "mandalajati", "cinambo", "rancasari", "batununggal", "ujungberung", "cibiru", "cileunyi", "cimenyan", "cidadap", "arcamanik", "antapani", "panyileukan", "kiaracondong", "bojongloa kidul", "bojongloa kaler", "lengkong", "sukajadi", "cicendo", "bandung kulon", "bandung wetan", "sumur bandung", "regol", "andir", "astana anyar", "mandalajati", "cinambo", "rancasari", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cimanggis", "cinere", "cinangka", "sukmajaya", "sukasari", "limo", "cilodong", "bojong gede", "cihideung", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "cihideung", "cigugur", "lumbung", "kertasari", "melong", "sukahaji", "tawang", "cimalaka", "tanjungsari", "ganeas", "pamulihan", "rancakalong", "tawang", "cimalaka", "tanjung sari", "ganeas", "pamulihan", "rancakalong", "pataruman", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "pataruman", "cikedung", "cikoneng", "kedawung", "plumbon", "kapetakan", "aranis", "langensari", "cijulang", "langkaplancar", "pangandaran", "parigi", "langensari", "cijulang", "langkap lancar", "pangandaran", "parigi"]

        self.wilayah_data = [
            {"kabkot": "Bandung"}, {"kabkot": "Bandung Barat"}, {"kabkot": "Bekasi"},
            {"kabkot": "Bogor"}, {"kabkot": "Ciamis"}, {"kabkot": "Cianjur"},
            {"kabkot": "Cirebon"}, {"kabkot": "Garut"}, {"kabkot": "Indramayu"},
            {"kabkot": "Karawang"}, {"kabkot": "Kuningan"}, {"kabkot": "Majalengka"},
            {"kabkot": "Pangandaran"}, {"kabkot": "Purwakarta"}, {"kabkot": "Subang"},
            {"kabkot": "Sukabumi"}, {"kabkot": "Sumedang"}, {"kabkot": "Tasikmalaya"},
            {"kabkot": "Banjar"}, {"kabkot": "Cimahi"}, {"kabkot": "Depok"}, {"kabkot": "Jawa Barat"}
        ]

        self.sources = {
            "Top Stories": "https://news.google.com/rss/search?q={query}?+when:1d&hl=id&gl=ID&ceid=ID:id",
            "Google News": "https://news.google.com/rss/search?q={query}&hl=id&gl=ID&ceid=ID:id"
        }

    def fetch_feed(self, url, source_name, kab, current_keyword, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                feed = feedparser.parse(url, agent=user_agent)

                if hasattr(feed, 'status') and feed.status == 429:
                    time.sleep(60 * (retries + 1))
                    retries += 1
                    continue

                for entry in feed.entries:
                    if entry.link in self.seen_links:
                        continue

                    pub_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    pub_date = pub_time.date()

                    title = entry.title.lower()
                    content = entry.get('summary', '').lower()
                    
                    # Cek relevansi terhadap keyword aktif DAN wilayah
                    is_relevant = current_keyword.lower() in (title + content) and kab.lower() in (title + content)

                    if (pub_date >= self.yesterday) and is_relevant:
                        self.seen_links.add(entry.link)
                        self.all_results.append({
                            'Waktu_Publikasi': pub_time.strftime('%Y-%m-%d %H'),
                            'Keyword': current_keyword,
                            'Wilayah': kab,
                            'Sumber': source_name,
                            'Judul': entry.title,
                            'Link': entry.link
                        })
                return
            except Exception:
                retries += 1
                time.sleep(2 * retries)

    def run_monitoring(self):
        print(f"--- Memulai Monitoring Kolektif Jabar ---")
        start_total = time.time()

        # Inisialisasi Progress Bar Utama
        total_steps = len(self.keywords_list) * len(self.wilayah_data)
        
        with tqdm(total=total_steps, desc="Progres Monitoring", unit="tugas", colour='green') as pbar:
            # 2. LOOP KEYWORD (STATIS)
            for kw in self.keywords_list:
                print(f"\n MENCARI INFORMASI: {kw.upper()}")
                
                # 3. LOOP WILAYAH
                for item in self.wilayah_data:
                    kab = item['kabkot']

                    # Update pesan loading di bar
                    pbar.set_postfix({"Keyword": kw, "Wilayah": kab})
                    
                    trending_query = "(" + " OR ".join(self.trending_tags) + ")"
                    
                    # Menyiapkan Query
                    query_base = f"{kw} {kab}"
                    
                    # Media Online
                    q_online = urllib.parse.quote(f"{query_base} when:1d")
                    self.fetch_feed(self.sources["Google News"].format(query=q_online), "Media Online", kab, kw)

                    # Sosial Media (Instagram & TikTok) via Google Index
                    q_social = urllib.parse.quote(f"(site:instagram.com OR site:tiktok.com) {query_base} {trending_query} when:1d")
                    self.fetch_feed(self.sources["Google News"].format(query=q_social), "Sosial Media", kab, kw)

                    # Delay antar wilayah untuk menghindari blokir
                    time.sleep(random.uniform(2.0, 4.0))

            # 4. SIMPAN HASIL KE DALAM 1 FILE SETELAH SEMUA SELESAI
            self.save_results()
            print(f"\nTotal waktu proses: {round((time.time() - start_total)/60, 2)} menit")

    def save_results(self):
        if self.all_results:
            df = pd.DataFrame(self.all_results)
            
            # Cleaning & Sorting
            df['Waktu_Publikasi'] = pd.to_datetime(df['Waktu_Publikasi'])
            df = df.sort_values(by=['Waktu_Publikasi', 'Keyword'], ascending=[False, True])
            df = df.drop_duplicates(subset=['Link']) # Hapus duplikat link antar keyword
            
            filename = f"Laporan_Monitoring_Bencana_Jabar_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"\n✅ BERHASIL! Semua hasil (Total: {len(df)} data) disimpan di: {filename}")
        else:
            print("\n❌ Tidak ada data ditemukan untuk semua keyword.")

if __name__ == "__main__":
    app = JabarSmartMonitor()
    app.run_monitoring()
