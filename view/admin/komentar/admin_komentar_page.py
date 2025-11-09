import streamlit as st
from .admin_komentar import AdminKomentar

komen = AdminKomentar() 

def show(user) :
    tab_k1, tab_k2, tab_k3 = st.tabs(["Komentar Enkripsi","Komentar Dekripsi","Hapus Komentar"])
    with tab_k1 :
        st.header("Daftar Komentar Terenkripsi")
        komen.daftarkomenen()
    with tab_k2 :
        st.header("Daftar Komentar")
        komen.daftarkomende()
    with tab_k3 :
        st.header("Hapus Komentar")
        komen.hapuskomen()
