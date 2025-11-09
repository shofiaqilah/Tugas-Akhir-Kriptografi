import streamlit as st
import pandas as pd
from database.konten import Konten
from io import BytesIO

konten_db = Konten()

class AdminKonten :
    def daftarbuah(self) :
        contents = konten_db.get_all_contents()
        if not contents:
            st.info("Belum ada data buah.")
            return

        with st.container():
            for item in contents:
                st.subheader(f"{item['nama_buah']} (*{item['nama_latin']}*)")

                col1, col2 = st.columns([1, 2])
                with col1:
                    if item["gambar_bytes"]:
                        st.image(item["gambar_bytes"], use_container_width=True)
                    else:
                        st.write("📷 Tidak ada gambar")

                with col2:
                    st.write("**Ciri-ciri:**")
                    st.write(f"Jenis      : {item['jenis']}")
                    st.write(f"Asal       : {item['asal']}")
                    st.write(f"Famili     : {item['famili']}")
                    st.write(f"Panen      : {item['musim_panen']}")
                    st.write(f"Keping biji: {item['keping_biji']}")
                    st.write(f"Kandungan  : {item['kandungan']}")
                    st.write(f"Warna      : {item['warna']}")
                    st.write(f"Rasa       : {item['rasa']}")
                with st.expander("**Deskripsi:**") :
                    st.write(f"{item['deskripsi']}")

                # Tombol hapus
                if st.button(f"🗑️ Hapus {item['nama_buah']}", key=f"hapus_{item['id']}"):
                    konten_db.delete_content(item["id"])
                    st.warning(f"{item['nama_buah']} dihapus dari database.")
                    st.rerun()

                st.divider()

    def daftarcari(self,search) :
        contents = konten_db.get_search(search)
        if not contents:
            st.info("Data tidak ditemukan.")
            return

        with st.container():
            for item in contents:
                st.subheader(f"{item['nama_buah']} (*{item['nama_latin']}*)")

                col1, col2 = st.columns([1, 2])
                with col1:
                    if item["gambar_bytes"]:
                        st.image(item["gambar_bytes"], use_container_width=True)
                    else:
                        st.write("📷 Tidak ada gambar")

                with col2:
                    st.write("**Ciri-ciri:**")
                    st.write(f"Jenis      : {item['jenis']}")
                    st.write(f"Asal       : {item['asal']}")
                    st.write(f"Famili     : {item['famili']}")
                    st.write(f"Panen      : {item['musim_panen']}")
                    st.write(f"Keping biji: {item['keping_biji']}")
                    st.write(f"Kandungan  : {item['kandungan']}")
                    st.write(f"Warna      : {item['warna']}")
                    st.write(f"Rasa       : {item['rasa']}")
                with st.expander("**Deskripsi:**") :
                    st.write(f"{item['deskripsi']}")

                # Tombol hapus
                if st.button(f"🗑️ Hapus {item['nama_buah']}", key=f"hapus_{item['id']}"):
                    konten_db.delete_content(item["id"])
                    st.warning(f"{item['nama_buah']} dihapus dari database.")
                    st.rerun()

                st.divider()

    def daftarbuahenkrip(self) :
        contents = konten_db.get_raw_contents()
        if not contents:
            st.info("Belum ada data buah.")
            return
        else :
            df_contents = pd.DataFrame(contents,columns=['id','nama_buah','nama_latin','gambar'])
        st.dataframe(df_contents,hide_index=True)

    def editbuah(self) :
        # ambil semua konten dulu
        konten_list = konten_db.get_all_contents()
        with st.container():
            if konten_list :
                pilihan = {f"{k['id']} - {k['nama_buah']}": k['id'] for k in konten_list}  # contoh k[0]=id, k[1]=nama_buah
                selected = st.selectbox("Pilih buah untuk diupdate", list(pilihan.keys()))
                selected_id = pilihan[selected]
                konten = konten_db.get_content(selected_id)
                #form
                nama_buah = st.text_input("Nama Buah", konten['nama_buah'])
                nama_latin = st.text_input("Nama Latin", konten['nama_latin'])
                jenis = st.text_input("Jenis",konten['jenis'])
                asal = st.text_input("Asal",konten['asal'])
                famili = st.text_input("Famili",konten['famili'])
                musim_panen = st.text_input("Musim Panen",konten['musim_panen'])
                keping_biji = st.text_input("Keping Biju",konten['keping_biji'])
                kandungan = st.text_input("Kandungan",konten['kandungan'])
                warna = st.text_input("Warna",konten['warna'])
                rasa = st.text_input("Rasa",konten['rasa'])
                deskripsi = st.text_area("Deskripsi Buah",konten['deskripsi'])
                gambar = st.file_uploader("Upload gambar baru (kosongkan kalau tidak diubah)", type=["jpg", "png"])
                
                if st.button("💾 Simpan Perubahan Buah"):
                    if gambar is not None:
                        gambar_data = gambar.read()
                    else:
                        gambar_data = None # gak edit

                    konten_db.update_content(
                        selected_id,
                        nama_buah,
                        nama_latin,
                        jenis,
                        asal,
                        famili,
                        musim_panen,
                        keping_biji,
                        kandungan,
                        warna,
                        rasa,
                        deskripsi,
                        gambar_data)
                    st.success("Konten berhasil diperbarui!")
                st.rerun()
            else :
                st.info("Belum ada data")

    def tambah_buah(self):
        # Form input
        with st.form(key="add_fruit_form"):
            nama_buah = st.text_input("Nama Buah")
            nama_latin = st.text_input("Nama Latin")
            jenis = st.text_input("Jenis")
            asal = st.text_input("Asal")
            famili = st.text_input("Famili")
            musim_panen = st.text_input("Musim Panen")
            keping_biji = st.text_input("Keping Biju")
            kandungan = st.text_input("Kandungan")
            warna = st.text_input("Warna")
            rasa = st.text_input("Rasa")
            deskripsi = st.text_area("Deskripsi Buah")
            gambar_file = st.file_uploader("Upload Gambar (opsional)", type=["jpg", "jpeg", "png"])

            submitted = st.form_submit_button("💾 Simpan")

            if submitted:
                if not nama_buah or not nama_latin:
                    st.error("Nama buah dan nama latin wajib diisi.")
                else:
                    # ambil bytes dari file jika ada
                    gambar_bytes = None
                    if gambar_file is not None:
                        gambar_bytes = gambar_file.read()

                    konten_db.add_content(
                        nama_buah=nama_buah,
                        nama_latin=nama_latin,
                        jenis=jenis,
                        asal=asal,
                        famili=famili,
                        musim_panen=musim_panen,
                        keping_biji=keping_biji,
                        kandungan=kandungan,
                        warna=warna,
                        rasa=rasa,
                        deskripsi=deskripsi,
                        gambar_bytes = gambar_bytes
                    )

                    st.success(f"Buah '{nama_buah}' berhasil ditambahkan!")
                    st.rerun()
