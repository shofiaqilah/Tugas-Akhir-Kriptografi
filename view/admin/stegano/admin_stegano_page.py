import streamlit as st
from .admin_stegano import AdminStegano

stegano = AdminStegano()

def show(user) :
    tab_s1, tab_s2, tab_s3 = st.tabs(["Tambah Stegano","Daftar Stegano","Dekripsi Stegano"])
    with tab_s1 :
        st.header("Tambah Steganografi LSB Encoder")
        stegano.tambahstegano()
    with tab_s2 :
        st.header("Galeri Steganografi")
        stegano.tampilkanstegano()
    with tab_s3 :
        st.header(" Dekripsi Gambar Steganografi")
        stegano.ambilpesan()