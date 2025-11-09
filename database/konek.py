import sqlite3

class DatabaseManager:
    def __init__(self, db_name="kripto.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        """Bikin koneksi ke database"""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Buat tabel users dan tabel konten jika belum ada"""
        with self.connect() as conn:
            c = conn.cursor()
            # users (jika belum ada)
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password_hash TEXT,
                    status TEXT
                )
            ''')
            # konten
            c.execute('''
                CREATE TABLE IF NOT EXISTS konten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_buah BLOB,
                    nama_latin BLOB,
                    jenis TEXT,
                    asal TEXT,
                    famili TEXT,
                    musim_panen TEXT,
                    keping_biji TEXT,
                    kandungan TEXT,
                    warna TEXT,
                    rasa TEXT,
                    deskripsi TEXT,
                    gambar BLOB
                )
            ''')
            #stegano
            c.execute('''
                CREATE TABLE IF NOT EXISTS stegano (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_file TEXT,
                    pesan_asli TEXT,
                    cipher TEXT,
                    gambar_asli BLOB,
                    gambar_stegano BLOB
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS komentar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    buah_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    isi TEXT NOT NULL,
                    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (buah_id) REFERENCES konten(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

