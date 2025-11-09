import streamlit as st
from database.user import User
import pandas as pd

user_db = User()

class AdminUser :

    def user(self) :
        with st.container() :
            users = user_db.get_all_users()  # pastikan ini return [(id, username, password), ...]
            df = pd.DataFrame(users, columns=["ID", "Username", "Password"])

            # Tampilkan editor (id hanya baca)
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                disabled=["ID"],  # kolom ID gak bisa diedit
                key="user_editor",
                hide_index=True
            )
            if st.button("💾 Simpan Perubahan User"):
                for _, row in edited_df.iterrows():
                    user_id = row["ID"]
                    username = row["Username"]
                    password = row["Password"]

                    if pd.isna(user_id):  # kalau ID kosong → data baru
                        user_db.insert_user(username, password, status="user")
                    else:  # kalau ID ada → update
                        user_db.update_user(user_id, username, password)

                st.success("Perubahan tersimpan ke database.")
                st.rerun()
                # Tombol hapus baris
            st.header("Hapus User")
            id_del = user_db.get_id("user")  # asumsinya return list of ids
            if id_del:
                hapus_id = st.selectbox("Pilih ID user untuk dihapus:", id_del)
                if st.button("🗑️ Hapus User"):
                    user_db.delete_user(hapus_id)
                    st.warning(f"User dengan ID {hapus_id} dihapus.")
                    st.rerun()
            else:
                st.info("Belum ada user untuk dihapus.")

    def admin(self) :
        with st.container() :
            admins = user_db.get_all_admins()
            df = pd.DataFrame(admins, columns=["ID","Username", "Password"])
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                disabled=["ID"],  # kolom ID gak bisa diedit
                key="admin_editor",
                hide_index=True
            )
            if st.button("💾 Simpan Perubahan Admin"):
                for _, row in edited_df.iterrows():
                    user_id = row["ID"]
                    username = row["Username"]
                    password = row["Password"]

                    if pd.isna(user_id):  # kalau ID kosong → data baru
                        user_db.insert_user(username, password, status="admin")
                    else:  # kalau ID ada → update
                        user_db.update_user(user_id, username, password)

                st.success("Perubahan tersimpan ke database.")
                st.rerun()
                # Tombol hapus baris
            st.header("Hapus Admin")
            id_del = user_db.get_id("admin")  # asumsinya return list of ids
            if id_del:
                hapus_id = st.selectbox("Pilih ID admin untuk dihapus:", id_del)
                if st.button("🗑️ Hapus Admin"):
                    user_db.delete_user(hapus_id)
                    st.warning(f"User dengan ID {hapus_id} dihapus.")
                    st.rerun()
            else:
                st.info("Belum ada user untuk dihapus.")