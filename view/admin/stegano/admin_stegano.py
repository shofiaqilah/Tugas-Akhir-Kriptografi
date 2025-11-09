import tempfile
from database.stegano import SteganoLSB
from PIL import Image
import io
import streamlit as st
import pandas as pd

stegano_db = SteganoLSB()

class AdminStegano :

    def tambahstegano(self):
        with st.container():
            file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])
            nama_file = st.text_input("Nama File (judul data):")
            message = st.text_area("Masukkan pesan yang ingin disembunyikan")

            if st.button("🔒 Enkripsi dan Simpan"):
                if file and message:
                    with tempfile.NamedTemporaryFile(delete=False) as temp:
                        temp.write(file.read())
                        temp_path = temp.name
                    stegano_db.insert_stegano(nama_file, message, temp_path)
                    st.success("✅ Gambar dengan pesan telah disimpan ke database.")
                else:
                    st.error("⚠️ Harap upload gambar dan isi pesan dulu.")

    def tampilkanstegano(self) :
        data_stegano = stegano_db.get_all_stegano_detail()

        with st.container():
            if not data_stegano:
                st.info("Belum ada data steganografi tersimpan.")
            else:
                for item in data_stegano:
                    st.subheader(f"📁 {item['nama_file']} (ID: {item['id']})")
                    st.write(f"💬 Pesan disisipkan: `{item['pesan_asli']}`")

                    col1, col2 = st.columns(2)

                    # Gambar asli
                    with col1:
                        st.markdown("**Sebelum (Asli)**")
                        img_asli = Image.open(io.BytesIO(item["gambar_asli"]))
                        size_asli = len(item['gambar_asli'])
                        st.image(img_asli, use_container_width=True)
                        st.write(f"Size : {size_asli}")

                    # Gambar hasil stego
                    with col2:
                        st.markdown("**Sesudah (Dengan Pesan)**")
                        img_stegano = Image.open(io.BytesIO(item["gambar_stegano"]))
                        size_hasil = len(item['gambar_stegano'])
                        st.image(img_stegano, use_container_width=True)
                        st.write(f"Size : {size_hasil}")

                    # Tombol hapus
                    if st.button(f"🗑️ Hapus Data ID {item['id']}", key=f"hapus_{item['id']}"):
                        stegano_db.delete_stegano(item["id"])
                        st.warning(f"Data steganografi ID {item['id']} berhasil dihapus.")
                        st.rerun()
                    st.divider()

    def ambilpesan(self) :
        with st.container():
            file = st.file_uploader("Upload gambar steganografi (yang sudah disisipi pesan)", type=["png", "jpg", "jpeg"])

            if st.button("🔓 Dekripsi Pesan"):
                if file:
                    with tempfile.NamedTemporaryFile(delete=False) as temp:
                        temp.write(file.read())
                        temp_path = temp.name

                    try:
                        # Pakai fungsi decode dari SteganoLSB
                        message = stegano_db.extract_stegano(temp_path)
                        if message:
                            st.success("✅ Pesan berhasil didekripsi:")
                            st.code(message, language=None)
                        else:
                            st.warning("⚠️ Tidak ditemukan pesan tersembunyi di gambar ini.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat dekripsi: {e}")
                else:
                    st.error("⚠️ Harap upload gambar terlebih dahulu.")
