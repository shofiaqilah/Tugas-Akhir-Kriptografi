import os
import streamlit as st
from cryptography.fernet import Fernet
from typing import Optional, List, Dict
from .konek import DatabaseManager

class Konten(DatabaseManager):
    XOR_KEY_FILE = "xor.key"
    FERNET_KEY_FILE = "fernet.key"

    def __init__(self, db_name: str = "kripto.db",):
        super().__init__(db_name)
        # pastikan key tersedia
        self._ensure_xor_key()
        self._ensure_fernet_key()
        self.fernet = Fernet(self._load_fernet_key())
        self.xor_key = self._load_xor_key()

    # ---------- Key management ----------
    def _ensure_xor_key(self, length: int = 32):
        """Buat file xor.key jika belum ada (length bytes)"""
        if not os.path.exists(self.XOR_KEY_FILE):
            key = os.urandom(length)
            with open(self.XOR_KEY_FILE, "wb") as f:
                f.write(key)

    def _load_xor_key(self) -> bytes:
        with open(self.XOR_KEY_FILE, "rb") as f:
            return f.read()

    def _ensure_fernet_key(self):
        if not os.path.exists(self.FERNET_KEY_FILE):
            key = Fernet.generate_key()
            with open(self.FERNET_KEY_FILE, "wb") as f:
                f.write(key)

    def _load_fernet_key(self) -> bytes:
        with open(self.FERNET_KEY_FILE, "rb") as f:
            return f.read()

    # ---------- XOR stream helpers ----------
    def _xor_bytes(self, data: bytes, key: bytes) -> bytes:
        """XOR stream: ulangi key jika lebih pendek dari data"""
        if len(key) == 0:
            raise ValueError("XOR key length is 0")
        out = bytearray(len(data))
        klen = len(key)
        for i, b in enumerate(data):
            out[i] = b ^ key[i % klen]
        return bytes(out)

    def xor_encrypt_text(self, plaintext: str) -> bytes:
        """Encrypt plaintext (str) -> returns raw bytes (to be stored as BLOB)"""
        data = plaintext.encode("utf-8")
        encrypted = self._xor_bytes(data, self.xor_key)
        return encrypted

    def xor_decrypt_text(self, encrypted_bytes: bytes) -> str:
        """Decrypt bytes -> returns plaintext str"""
        decrypted = self._xor_bytes(encrypted_bytes, self.xor_key)
        return decrypted.decode("utf-8")

    # ---------- Fernet helpers for images ----------
    def fernet_encrypt_bytes(self, data: bytes) -> bytes:
        """Returns encrypted bytes (Fernet token)"""
        return self.fernet.encrypt(data)

    def fernet_decrypt_bytes(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)

    # ---------- CRUD untuk konten ----------
    def add_content(self,
                    nama_buah: str,
                    nama_latin: str,
                    jenis: str,
                    asal: str,
                    famili: str,
                    musim_panen:str,
                    keping_biji: str,
                    kandungan:str,
                    warna:str,
                    rasa:str,
                    deskripsi: str,
                    gambar_bytes: Optional[bytes] = None) -> int:
        """
        Tambah konten baru.
        - nama_buah & nama_latin dienkripsi XOR stream dan disimpan sebagai BLOB.
        - gambar_bytes jika disediakan akan dienkripsi dengan Fernet dan disimpan sebagai BLOB.
        Returns: id (autoincrement) dari row yang dibuat.
        """
        enc_nama_buah = self.xor_encrypt_text(nama_buah)
        enc_nama_latin = self.xor_encrypt_text(nama_latin)
        enc_gambar = None
        if gambar_bytes is not None:
            enc_gambar = self.fernet_encrypt_bytes(gambar_bytes)

        with self.connect() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO konten (nama_buah, nama_latin, jenis, asal, famili, musim_panen, keping_biji, kandungan, warna, rasa, deskripsi, gambar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (enc_nama_buah, enc_nama_latin, jenis, asal, famili, musim_panen, keping_biji, kandungan, warna, rasa, deskripsi, enc_gambar))
            conn.commit()
            return c.lastrowid

    # ---------- Update Konten ----------
    def update_content(self,
                    id,
                    nama_buah: str,
                    nama_latin: str,
                    jenis: str,
                    asal: str,
                    famili: str,
                    musim_panen:str,
                    keping_biji: str,
                    kandungan:str,
                    warna:str,
                    rasa:str,
                    deskripsi: str,
                    gambar_bytes: Optional[bytes] = None) -> int:
        enc_nama_buah = self.xor_encrypt_text(nama_buah)
        enc_nama_latin = self.xor_encrypt_text(nama_latin)
        enc_gambar = None
        with self.connect() as conn:
            c = conn.cursor()
            if gambar_bytes is not None :
                enc_gambar = self.fernet_encrypt_bytes(gambar_bytes)
                c.execute('''
                    UPDATE konten 
                    SET nama_buah=?, nama_latin=?, jenis=?, asal=?,famili=?,musim_panen=?,keping_biji=?,kandungan=?,warna=?,rasa=?,deskripsi=?, gambar=? 
                    WHERE id=?
                    ''', (enc_nama_buah, enc_nama_latin, jenis, asal, famili, musim_panen, keping_biji, kandungan, warna, rasa, deskripsi, enc_gambar, id))
                conn.commit()
            else :
                c.execute('''
                    UPDATE konten 
                    SET nama_buah=?, nama_latin=?, jenis=?, asal=?,famili=?,musim_panen=?,keping_biji=?,kandungan=?,warna=?,rasa=?,deskripsi=?
                    WHERE id=?
                    ''', (enc_nama_buah, enc_nama_latin, jenis, asal, famili, musim_panen, keping_biji, kandungan, warna, rasa, deskripsi, id))
                conn.commit()
            return c.lastrowid

    def get_content(self, content_id: int) -> Optional[Dict]:
        """
        Ambil satu konten (decrypt nama_buah, nama_latin, dan gambar).
        Returns dict atau None jika tidak ditemukan.
        dict keys: id, nama_buah, nama_latin, ciri_ciri, deskripsi, gambar_bytes (decrypted)
        """
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM konten WHERE id = ?', (content_id,))
            row = c.fetchone()
            if not row:
                return None

            _id, enc_nama_buah, enc_nama_latin, jenis, asal, famili, musim_panen, keping_biji, kandungan, warna, rasa, deskripsi, enc_gambar = row
            # decrypt nama fields (XOR)
            nama_buah = self.xor_decrypt_text(enc_nama_buah) if enc_nama_buah is not None else None
            nama_latin = self.xor_decrypt_text(enc_nama_latin) if enc_nama_latin is not None else None
            # decrypt gambar if ada
            gambar_bytes = None
            if enc_gambar is not None:
                gambar_bytes = self.fernet_decrypt_bytes(enc_gambar)

            return {
                "id": _id,
                "nama_buah": nama_buah,
                "nama_latin": nama_latin,
                "jenis": jenis, 
                "asal": asal, 
                "famili": famili, 
                "musim_panen": musim_panen, 
                "keping_biji": keping_biji, 
                "kandungan": kandungan,
                "warna":warna,
                "rasa":rasa,
                "deskripsi": deskripsi,
                "gambar_bytes": gambar_bytes
            }

    def get_all_contents(self) -> List[Dict]:
        """Ambil semua konten, return list of dicts (decrypted nama fields and gambar)"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM konten ORDER BY id ASC')
            ids = [r[0] for r in c.fetchall()]

        results = []
        for _id in ids:
            item = self.get_content(_id)
            if item:
                results.append(item)
        return results
    
    def get_filtered_contents(self, warna=None, rasa=None, keping_biji=None, asal=None) :
        query = "SELECT id FROM konten WHERE 1=1"
        params = []

        if warna:
            query += " AND warna LIKE ?"
            params.append(f"%{warna}%")

        if rasa:
            query += " AND rasa LIKE ?"
            params.append(f"%{rasa}%")

        if keping_biji:
            query += " AND keping_biji LIKE ?"
            params.append(f"%{keping_biji}%")

        if asal:
            query += " AND asal LIKE ?"
            params.append(f"%{asal}%")

        query += " ORDER BY id ASC"

        with self.connect() as conn:
            c = conn.cursor()
            c.execute(query, params)
            ids = [r[0] for r in c.fetchall()]

        results = []
        for _id in ids:
            item = self.get_content(_id)
            if item:
                results.append(item)

        return results

    def get_search(self, search: str) -> list[dict]:
        """Cari konten berdasarkan kata kunci, lakukan filter setelah dekripsi."""
        search_lower = search.lower().strip()
        results = []

        all_contents = self.get_all_contents()  # ambil semua, sudah terdekripsi
        for item in all_contents:
            if (
                search_lower in (item['nama_buah'] or '').lower()
                or search_lower in (item['nama_latin'] or '').lower()
                or search_lower in (item['jenis'] or '').lower()
                or search_lower in (item['famili'] or '').lower()
            ):
                results.append(item)

        return results

    
    def get_raw_contents(self) -> List[Dict]:
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT id,nama_buah,nama_latin,gambar FROM konten ORDER BY id ASC')
            return c.fetchall()

    def delete_content(self, content_id: int) -> bool:
        """Hapus konten berdasarkan id. Returns True jika ada row yang dihapus."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM konten WHERE id = ?', (content_id,))
            conn.commit()
            return c.rowcount > 0

