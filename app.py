import streamlit as st
from database.user import User
import view.admin.admin_page as ap
import view.user.user_page as up

user_db = User()

#st.set_page_config(layout="centered")

placeholder = st.empty()
# --- SESSION STATE ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- HALAMAN LOGIN ---
def login_page():
    with st.container() :
        st.title("🍎🍋 Ensiklopedia Buah 🍇🥝")
        tab1, tab2 = st.tabs(["Login","Signin"])
        with tab1 :
            st.header("Login Page")
            # --- LOGIN FORM ---
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login", key="login_btn"):
                user = user_db.verify_user(username, password)
                if user:
                    st.session_state.user = user
                    with st.empty() :
                        st.rerun()
                else:
                    st.error("Username atau password salah!")

        with tab2 :
            st.header("Belum punya akun?")

            # --- REGISTER FORM ---
            new_user = st.text_input("Username baru", key="register_user")
            new_pass = st.text_input("Password baru", type="password", key="register_pass")

            if st.button("Daftar Akun", key="register_btn"):
                if new_user and new_pass:
                    user_db.insert_user(new_user, new_pass, status="user")
                    st.success("Akun berhasil dibuat! Silakan login.")
                else:
                    st.warning("Isi username dan password terlebih dahulu.")
                
# --- HALAMAN UTAMA SESUAI ROLE ---
def main_page():
    user = st.session_state.user
    st.sidebar.write(f"Login sebagai: **{user['username']} ({user['status']})**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    
    if user["status"] == "admin":
            ap.show_admin_page(user)
    else:
            up.show_auser_page(user)

# --- ROUTER ---
if st.session_state.user is None:
    login_page()
else:
    main_page()
