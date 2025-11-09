import streamlit as st
from .admin_user import AdminUser

users = AdminUser()

def show(user) :
    tab_u1, tab_u2 = st.tabs(["User","Admin"])
    with tab_u1 :
        st.header("Daftar User")
        users.user()
    with tab_u2 :
        st.header("Daftar Admin")
        users.admin()