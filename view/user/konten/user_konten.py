import streamlit as st
from database.konten import Konten
from database.komentar import Komentar

konten_db = Konten()
komen_db = Komentar()

class UserKonten :
    def daftarbuah(self,user) :
        with st.container() :
            contents = konten_db.get_all_contents()
            if not contents:
                st.info("Belum ada data buah.")
                return
            else :
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
                            st.write(f"Warna      : {item['warna']}")
                            st.write(f"Rasa       : {item['rasa']}")
                            st.write(f"Kandungan  : {item['kandungan']}")
                        with st.expander("**Deskripsi:**") :
                            st.write(f"{item['deskripsi']}")

                        # Tombol hapus
                        with st.expander("💬 Komentar"):
                            # --- tampilkan komentar yang sudah ada ---
                            komentar_list = komen_db.lihat_komentar(item['id'])
                            if komentar_list:
                                for komen in komentar_list:
                                    username = komen["username"]
                                    isi = komen["isi"]
                                    waktu = komen["waktu"]

                                    with st.container():
                                        st.markdown(
                                            f"""
                                            <div style="padding:6px 10px; background-color:#f0f2f6; border-radius:8px; margin-bottom:5px;">
                                                <b>{username}</b> <span style="color:gray; font-size:11px;">({waktu})</span><br>
                                                {isi}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                            else:
                                st.caption("Belum ada komentar.")

                            # --- tambahkan komentar baru ---
                            st.write("---")
                            komentar_baru = st.text_area(f"Tulis komentar Anda di {item['nama_buah']}:",
                                                        key=f"komen_text_{item['id']}")
                            if st.button(f"💬 Kirim Komentar", key=f"kirim_komen_{item['id']}"):
                                if komentar_baru.strip():
                                    komen_db.tambah_komentar(
                                        buah_id=item['id'],
                                        user_id=user['id'],
                                        isi=komentar_baru
                                    )
                                    st.success("Komentar berhasil dikirim!")
                                    st.rerun()  # biar langsung refresh tampilan komentar
                                else:
                                    st.warning("Komentar tidak boleh kosong!")

                        st.divider()
    def daftarcari(self,user,search) :
        with st.container() :
            contents = konten_db.get_search(search = search)
            if not contents:
                st.info("Belum ada data buah.")
                return
            else :
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
                            st.write(f"Warna      : {item['warna']}")
                            st.write(f"Rasa       : {item['rasa']}")
                            st.write(f"Kandungan  : {item['kandungan']}")
                        with st.expander("**Deskripsi:**") :
                            st.write(f"{item['deskripsi']}")

                        # Tombol hapus
                        with st.expander("💬 Komentar"):
                            # --- tampilkan komentar yang sudah ada ---
                            komentar_list = komen_db.lihat_komentar(item['id'])
                            if komentar_list:
                                for komen in komentar_list:
                                    username = komen["username"]
                                    isi = komen["isi"]
                                    waktu = komen["waktu"]

                                    with st.container():
                                        st.markdown(
                                            f"""
                                            <div style="padding:6px 10px; background-color:#f0f2f6; border-radius:8px; margin-bottom:5px;">
                                                <b>{username}</b> <span style="color:gray; font-size:11px;">({waktu})</span><br>
                                                {isi}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                            else:
                                st.caption("Belum ada komentar.")

                            # --- tambahkan komentar baru ---
                            st.write("---")
                            komentar_baru = st.text_area(f"Tulis komentar Anda di {item['nama_buah']}:",
                                                        key=f"komen_text_{item['id']}")
                            if st.button(f"💬 Kirim Komentar", key=f"kirim_komen_{item['id']}"):
                                if komentar_baru.strip():
                                    komen_db.tambah_komentar(
                                        buah_id=item['id'],
                                        user_id=user['id'],
                                        isi=komentar_baru
                                    )
                                    st.success("Komentar berhasil dikirim!")
                                    st.rerun()  # biar langsung refresh tampilan komentar
                                else:
                                    st.warning("Komentar tidak boleh kosong!")

                        st.divider()
    def daftarselect(self,user) :
        with st.container() :
            col1, col2 = st.columns(2)

            with col1:
                warna = st.selectbox("Warna", ["Merah", "Hijau", "Kuning", "Ungu", "Oranye", "Coklat"],index=None)
                rasa = st.selectbox("Rasa", ["Manis", "Asam", "Pahit", "Tawar"],index=None,)
            with col2:
                asal = st.selectbox("Asal", ["Asia", "Afrika", "Amerika", "Eropa", "Australia"],index=None,)
                keping = st.selectbox("Keping Biji", ["Monokotil", "Dikotil"],index=None,)
            
            if st.button("🔍 Cari",key="cari_buah_user") :
                contents = konten_db.get_filtered_contents(warna=warna, rasa=rasa, keping_biji=keping, asal=asal) 
                if not contents:
                    st.info("Belum ada data buah.")
                    return
                else :
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
                                st.write(f"Warna      : {item['warna']}")
                                st.write(f"Rasa       : {item['rasa']}")
                                st.write(f"Kandungan  : {item['kandungan']}")
                            with st.expander("**Deskripsi:**") :
                                st.write(f"{item['deskripsi']}")

                            # Tombol hapus
                            with st.expander("💬 Komentar"):
                                # --- tampilkan komentar yang sudah ada ---
                                komentar_list = komen_db.lihat_komentar(item['id'])
                                if komentar_list:
                                    for komen in komentar_list:
                                        username = komen["username"]
                                        isi = komen["isi"]
                                        waktu = komen["waktu"]

                                        with st.container():
                                            st.markdown(
                                                f"""
                                                <div style="padding:6px 10px; background-color:#f0f2f6; border-radius:8px; margin-bottom:5px;">
                                                    <b>{username}</b> <span style="color:gray; font-size:11px;">({waktu})</span><br>
                                                    {isi}
                                                </div>
                                                """,
                                                unsafe_allow_html=True
                                            )
                                else:
                                    st.caption("Belum ada komentar.")

                                # --- tambahkan komentar baru ---
                                st.write("---")
                                komentar_baru = st.text_area(f"Tulis komentar Anda di {item['nama_buah']}:",
                                                            key=f"komen_text_{item['id']}")
                                if st.button(f"💬 Kirim Komentar", key=f"kirim_komen_{item['id']}"):
                                    if komentar_baru.strip():
                                        komen_db.tambah_komentar(
                                            buah_id=item['id'],
                                            user_id=user['id'],
                                            isi=komentar_baru
                                        )
                                        st.success("Komentar berhasil dikirim!")
                                        st.rerun()  # biar langsung refresh tampilan komentar
                                    else:
                                        st.warning("Komentar tidak boleh kosong!")

                            st.divider()