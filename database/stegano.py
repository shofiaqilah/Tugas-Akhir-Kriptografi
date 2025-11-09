import sqlite3
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
from io import BytesIO
from .konek import DatabaseManager 
import os

class SteganoLSB(DatabaseManager):
    FERNET_KEY_FILE = "fernet.key"
    def __init__(self, db_name: str = "kripto.db"):
        super().__init__(db_name)
        self._ensure_fernet_key()
        self.key = self._load_fernet_key()
        self.fernet = Fernet(self.key)

    def _ensure_fernet_key(self):
        if not os.path.exists(self.FERNET_KEY_FILE):
            key = Fernet.generate_key()
            with open(self.FERNET_KEY_FILE, "wb") as f:
                f.write(key)

    def _load_fernet_key(self) -> bytes:
        with open(self.FERNET_KEY_FILE, "rb") as f:
            return f.read()
        
    def connect(self):
        return sqlite3.connect(self.db_name)

    def encrypt_message(self, message):
        """Enkripsi pesan pakai AES"""
        return self.fernet.encrypt(message.encode())

    def decrypt_message(self, token):
        """Dekripsi pesan"""
        return self.fernet.decrypt(token).decode()

    def insert_stegano(self, nama_file, pesan, path_gambar):
        """Sisipkan pesan terenkripsi ke gambar dan simpan ke database"""
        img = Image.open(path_gambar).convert("RGB")
        with open(path_gambar, "rb") as f:
            gambar_asli_bytes = f.read()

        # Enkripsi pesan
        cipher = self.encrypt_message(pesan)
        data = cipher + b"<END>"  # pembatas

        # Convert gambar ke array
        img_data = np.array(img)
        flat = img_data.flatten()

        # Konversi data ke bit
        bits = []
        for byte in data:
            bits.extend([(byte >> i) & 1 for i in range(8)])

        if len(bits) > len(flat):
            raise ValueError("Pesan terlalu panjang untuk gambar ini.")

        # Sisipkan bit ke LSB
        flat[:len(bits)] = (flat[:len(bits)] & 254) | bits
        new_img_data = flat.reshape(img_data.shape)
        stego_img = Image.fromarray(new_img_data.astype(np.uint8))

        # Simpan ke memory
        output = BytesIO()
        stego_img.save(output, format="PNG")
        gambar_stegano_bytes = output.getvalue()

        # Simpan ke database
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO stegano (nama_file, pesan_asli, cipher, gambar_asli, gambar_stegano)
                VALUES (?, ?, ?, ?, ?)
            ''', (nama_file, pesan, cipher.decode(), gambar_asli_bytes, gambar_stegano_bytes))
            conn.commit()

        print(f"✅ Pesan berhasil disisipkan ke '{nama_file}' dan disimpan ke database.")

    def extract_stegano(self, path_gambar):
        """Ekstrak pesan dari gambar hasil steganografi"""
        img = Image.open(path_gambar).convert("RGB")
        img_data = np.array(img)
        flat = img_data.flatten()

        bits = flat & 1
        bytes_out = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte |= bits[i + j] << j
            bytes_out.append(byte)
            if bytes_out[-5:] == list(b"<END>"):
                break

        data = bytes(bytes_out[:-5])
        try:
            pesan = self.decrypt_message(data)
            print("💬 Pesan hasil ekstraksi:", pesan)
            return pesan
        except Exception as e:
            print("❌ Gagal mendekripsi pesan:", e)
            return None
        
    def get_all_stegano_detail(self):
        """Ambil semua data steganografi (termasuk gambar)"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT id, nama_file, pesan_asli, gambar_asli, gambar_stegano FROM stegano ORDER BY id ASC")
            rows = c.fetchall()

        hasil = []
        for r in rows:
            hasil.append({
                "id": r[0],
                "nama_file": r[1],
                "pesan_asli": r[2],
                "gambar_asli": r[3],
                "gambar_stegano": r[4]
            })
        return hasil
    
    def delete_stegano(self, row_id: int) -> bool:
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM stegano WHERE id = ?', (row_id,))
            conn.commit()
            return c.rowcount > 0
 