import streamlit as st
import pandas as pd
from database.komentar import Komentar

komen_db = Komentar()

class AdminKomentar :

    def daftarkomenen(self) :
        with st.container():
            komentar = komen_db.get_all_komentar()
            df_komentar = pd.DataFrame(komentar,columns = ['ID','ID_Konten','Username','Waktu','Komentar'])
            st.dataframe(df_komentar,hide_index=True) 

    def daftarkomende(self) :
        with st.container():
            komentar = komen_db.get_all_komentar_dek()
            df_komentar = pd.DataFrame(komentar,columns = ['id','buah_id','username','waktu','isi'])
            df_komentar = df_komentar.rename(columns={
                "id": "ID",
                "buah_id": "ID_Konten",
                "username": "Username",
                "waktu": "Waktu",
                "isi": "Komentar"
            })
            st.dataframe(df_komentar,hide_index=True)

    def hapuskomen(self):
        with st.container():
            id_del = komen_db.get_id()  # asumsinya return list of ids
            if id_del:
                hapus_id = st.selectbox("Pilih ID komentar untuk dihapus:", id_del)
                if st.button("🗑️ Hapus Komentar"):
                    komen_db.hapus_komentar(hapus_id)
                    st.warning(f"User dengan ID {hapus_id} dihapus.")
                    st.rerun()
            else :
                st.info("Belum ada data ditambahkan")
