import streamlit as st
from .komentar import admin_komentar_page as komentar_page
from .konten import admin_konten_page as konten_page
from .user import admin_user_page as user_page
from .stegano import admin_stegano_page as stegano_page

def show_admin_page(user):
    st.title("Admin Dashboard")
    menu = st.sidebar.radio("Pilih menu:", ["🍎 Data Konten", "👥 Data User", "🧩 Steganografi", "💬 Komentar"])
    
    if menu == "🍎 Data Konten":
        konten_page.show(user)

    elif menu == "👥 Data User":
        user_page.show(user)

    elif menu == "🧩 Steganografi":
        stegano_page.show(user)
    
    elif menu == "💬 Komentar":
        komentar_page.show(user)
