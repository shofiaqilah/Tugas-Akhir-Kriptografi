import streamlit as st
from .admin_konten import AdminKonten

contents = AdminKonten()

def show(user) :
    tab_c1, tab_c2, tab_c3, tab_c4 = st.tabs(["Daftar Konten","Daftar Enkripsi","Tambah Buah","Edit Buah"])

    with tab_c1 :
        st.header("Daftar Konten Buah")
        cols1, cols2 = st.columns([1, 5])
        with cols1 :
            st.markdown(
                "<div style='display:flex; align-items:center; height:100px; font-weight:bold;'>Cari Buah :</div>",
                unsafe_allow_html=True
            )
        content_area = st.empty()
        with cols2 :
            cari = st.text_input(" ",key = "cari")
        if cari == "semua":
            with content_area :
                contents.daftarbuah()
        elif cari:
            with content_area :
                contents.daftarcari(search=cari)
        else :
            with content_area :
                st.write(" ")
    with tab_c2 :
        st.header("Daftar Konten Buah Enkripsi")
        contents.daftarbuahenkrip()
    with tab_c3 :
        st.header("Tambah Buah Baru")
        contents.tambah_buah()
    with tab_c4 :
        st.header("Update Konten Buah")
        contents.editbuah()