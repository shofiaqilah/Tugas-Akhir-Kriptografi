# 🍎 Aplikasi Ensiklopedia Buah-Buahan dengan Implementasi Kriptografi dan Steganografi

## 👩‍💻 Anggota Kelompok
Kelompok 3 (IF-A):
1. Mufidah Shofi Aqilah (123230133)
2. Sarah Aryandi Nugrahaeni (123230136)

## 📋 Deskripsi Proyek
Proyek ini merupakan tugas akhir mata kuliah **Kriptografi** yang mengembangkan aplikasi ensiklopedia buah-buahan berbasis web menggunakan **Streamlit** dan **Python**.  
Aplikasi ini menampilkan berbagai informasi mengenai buah, seperti nama buah, nama latin, deskripsi, serta gambar.  
Untuk menjaga keamanan data, aplikasi ini mengimplementasikan dua teknik utama:
- **Kriptografi**: digunakan untuk mengenkripsi data teks, gambar, dan password.
- **Steganografi**: digunakan untuk menyembunyikan pesan dalam gambar.

---

## 🎯 Tujuan
1. Membangun aplikasi ensiklopedia buah-buahan yang interaktif menggunakan **Python** dan **Streamlit**.  
2. Menerapkan konsep **kriptografi** untuk mengamankan data pengguna dan konten.  
3. Mengimplementasikan **steganografi (LSB)** untuk menyisipkan pesan rahasia ke dalam gambar.  

---

## 🔐 Fitur Utama

### 🔸 Mode Admin
- Login menggunakan username dan password terenkripsi.  
- Melihat dan mengelola data dari seluruh tabel database (user, konten, komentar, dan steganografi).  
- Menambah atau menghapus data user dan konten.  
- Menyisipkan dan mengekstrak pesan pada gambar menggunakan **steganografi (LSB)**.  
- Melihat komentar yang telah terenkripsi.  

### 🔸 Mode User
- Login atau membuat akun baru.  
- Melihat daftar buah lengkap dengan deskripsi dan gambar.  
- Menambahkan komentar yang akan otomatis **dienkripsi** sebelum disimpan.  

---

## 🔢 Algoritma yang Digunakan

| Jenis Data | Algoritma | Keterangan |
|-------------|------------|-------------|
| Password (login) | **SHA-224** | Hashing satu arah untuk keamanan password |
| Nama & Nama Latin Buah | **Stream Cipher** | Enkripsi karakter demi karakter |
| File Gambar | **AES (Fernet)** | Enkripsi blok menggunakan kunci rahasia |
| Komentar User | **Super Enkripsi (Vigenere Cipher + Block Cipher)** | Enkripsi ganda untuk perlindungan berlapis |
| Pesan Tersembunyi | **Steganografi (LSB)** | Menyembunyikan pesan di dalam gambar |

---

## 🧰 Teknologi yang Digunakan
- **Bahasa Pemrograman:** Python 3  
- **Framework UI:** Streamlit  
- **Database:** SQLite3  
- **Library Tambahan:**
  - `cryptography` / `pycryptodome`
  - `hashlib`
  - `sqlite3`
  - `stegano`
  - `PIL` / `OpenCV`

---

## 🚀 Cara Menjalankan Aplikasi
1. **Clone repository ini:**
   ```bash
   git clone https://github.com/usshofiaqilah/Tugas-Akhir-Kriptografi.git
   cd Tugas-Akhir-Kriptografi
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Jalankan aplikasi:**
    ```bash
    streamlit run app.py
