from .konek import DatabaseManager
from datetime import datetime
from cryptography.fernet import Fernet 
import os

class Komentar(DatabaseManager) :
    FERNET_KEY_FILE = "fernet.key"
    def __init__(self, db_name="kripto.db", key_file="fernet.key", vigenere_key="buahmanis"):
        self.db_name = db_name
        self.key_file = key_file
        self.vigenere_key = vigenere_key
        self._ensure_fernet_key()
        self.key = self._load_fernet_key()
        self.cipher = Fernet(self.key)

    def _ensure_fernet_key(self):
        if not os.path.exists(self.FERNET_KEY_FILE):
            key = Fernet.generate_key()
            with open(self.FERNET_KEY_FILE, "wb") as f:
                f.write(key)

    def _load_fernet_key(self) -> bytes:
        with open(self.FERNET_KEY_FILE, "rb") as f:
            return f.read()

    def vigenere_encrypt(self, text, key):
        result = []
        key = key.lower()
        for i, c in enumerate(text):
            if c.isalpha():
                shift = ord(key[i % len(key)]) - 97
                base = 65 if c.isupper() else 97
                result.append(chr((ord(c) - base + shift) % 26 + base))
            else:
                result.append(c)
        return ''.join(result)

    def vigenere_decrypt(self, text, key):
        result = []
        key = key.lower()
        for i, c in enumerate(text):
            if c.isalpha():
                shift = ord(key[i % len(key)]) - 97
                base = 65 if c.isupper() else 97
                result.append(chr((ord(c) - base - shift) % 26 + base))
            else:
                result.append(c)
        return ''.join(result)

    # --- CRUD ---
    def tambah_komentar(self, buah_id, user_id, isi):
        # 1. Enkripsi pakai Vigenère
        vigenere_encrypted = self.vigenere_encrypt(isi, self.vigenere_key)
        # 2. Enkripsi pakai Fernet
        final_encrypted = self.cipher.encrypt(vigenere_encrypted.encode()).decode()

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO komentar (buah_id, user_id, isi) VALUES (?, ?, ?)",
                    (buah_id, user_id, final_encrypted))
        conn.commit()
        conn.close()

    def lihat_komentar(self, buah_id):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('''SELECT k.id, k.buah_id, k.user_id, u.username, k.isi, k.waktu
            FROM komentar k INNER JOIN users u ON k.user_id = u.id
            INNER JOIN konten b ON k.buah_id = b.id
            WHERE k.buah_id = ? 
            ORDER BY k.waktu DESC''', 
            (buah_id,))
        hasil = cur.fetchall()
        conn.close()

        decrypted_comments = []
        for k in hasil:
            try:
                # k[4] = isi terenkripsi
                fernet_decrypted = self.cipher.decrypt(k[4].encode()).decode()
                original_text = self.vigenere_decrypt(fernet_decrypted, self.vigenere_key)
            except Exception:
                original_text = "[Gagal dekripsi]"
            
            decrypted_comments.append({
                "id": k[0],
                "buah_id": k[1],
                "user_id": k[2],
                "username": k[3],
                "isi": original_text,
                "waktu": k[5]
            })

        return decrypted_comments

    def edit_komentar(self, id_komentar, isi_baru):
        vigenere_encrypted = self.vigenere_encrypt(isi_baru, self.vigenere_key)
        final_encrypted = self.cipher.encrypt(vigenere_encrypted.encode()).decode()

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("UPDATE komentar SET isi = ?, waktu = ? WHERE id = ?",
                    (final_encrypted, datetime.now(), id_komentar))
        conn.commit()
        conn.close()

    def hapus_komentar(self, id_komentar):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM komentar WHERE id = ?", (id_komentar,))
        conn.commit()
        conn.close()

    def get_all_komentar(self):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT k.id, k.buah_id, u.username, k.waktu, k.isi FROM komentar k INNER JOIN users u ON k.user_id=u.id')
            return c.fetchall()
    
    def get_all_komentar_dek(self):
        conn = self.connect()
        c = conn.cursor()
        c.execute('SELECT k.id, k.buah_id, u.username, k.waktu, k.isi FROM komentar k INNER JOIN users u ON k.user_id=u.id')
        hasil = c.fetchall()
        conn.close()

        decrypted_comments = []
        for k in hasil:
            try:
                fernet_decrypted = self.cipher.decrypt(k[4].encode()).decode()
                original_text = self.vigenere_decrypt(fernet_decrypted, self.vigenere_key)
            except Exception:
                original_text = "[Gagal dekripsi]"
            
            decrypted_comments.append({
                "id": k[0],
                "buah_id": k[1],
                "username": k[2],
                "waktu": k[3],
                "isi": original_text,
            })
        return decrypted_comments
    
    def get_id(self) :
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM komentar")
            result = c.fetchall()
            return [r[0] for r in result]