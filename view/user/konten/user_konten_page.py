import streamlit as st
from .user_konten import UserKonten

contents = UserKonten()

def show(user) :
    cols1, cols2 = st.columns([1, 5])
    with cols1 :
        st.markdown(
            "<div style='display:flex; align-items:center; height:100px; font-weight:bold;'>🔍 Cari Buah :</div>",
            unsafe_allow_html=True
        )
    content_area = st.empty()
    with cols2 :
        cari = st.text_input(" ",key = "cari")
    
    if cari == "semua":
        with content_area :
            contents.daftarbuah(user)
    elif cari.strip() != "" :
        with content_area :
            contents.daftarcari(user=user,search=cari)
    else :
        with content_area :
            st.subheader("🔍 Pilih Filter")
            contents.daftarselect(user=user)