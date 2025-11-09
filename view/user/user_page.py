import streamlit as st
import pandas as pd
from .konten import user_konten_page as konten_page

def show_auser_page(user):
    st.title("🍎🍋 Ensiklopedia Buah 🍇🥝")
    konten_page.show(user)