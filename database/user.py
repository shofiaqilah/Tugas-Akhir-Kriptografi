import sqlite3
import hashlib
from .konek import DatabaseManager

class User(DatabaseManager):
    """Kelas untuk manajemen user"""

    def __init__(self):
        super().__init__()
        self.create_default_admin()  # buat admin otomatis kalau belum ada

    def hash_password(self, password):
        return hashlib.sha224(password.encode()).hexdigest()

    def create_default_admin(self):
        """Buat akun admin default jika belum ada"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE status='admin'")
            if not c.fetchone():
                # kalau belum ada admin, bikin satu
                admin_user = "admin"
                admin_pass = self.hash_password("admin123")
                c.execute("INSERT INTO users (username, password_hash, status) VALUES (?, ?, ?)",
                          (admin_user, admin_pass, "admin"))
                conn.commit()
                print("✅ Admin default dibuat: username='admin', password='admin123")

    def insert_user(self, username, password, status="user"):
        """Tambah user baru"""
        with self.connect() as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO users (username, password_hash, status) VALUES (?, ?, ?)',
                          (username, self.hash_password(password), status))
                conn.commit()
                print(f"✅ User '{username}' berhasil ditambahkan.")
            except sqlite3.IntegrityError:
                print(f"⚠️ User '{username}' sudah ada.")

    def delete_user(self, user_id):
        """Hapus user berdasarkan ID"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            print(f"🗑️ User dengan ID {user_id} berhasil dihapus (jika ada).")

    def update_user(self, user_id, username=None, password=None, status=None):
        """Update data user berdasarkan ID"""
        with self.connect() as conn:
            c = conn.cursor()
            fields = []
            values = []

            if username:
                fields.append("username = ?")
                values.append(username)
            if password:
                fields.append("password_hash = ?")
                values.append(self.hash_password(password))
            if status:
                fields.append("status = ?")
                values.append(status)

            if not fields:
                print("⚠️ Tidak ada perubahan.")
                return

            values.append(user_id)
            sql = f'UPDATE users SET {", ".join(fields)} WHERE id = ?'
            c.execute(sql, values)
            conn.commit()
            print(f"✏️ User dengan ID {user_id} berhasil diupdate.")

    def get_all_users(self):
        """Ambil semua user"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT id,username, password_hash FROM users WHERE status = "user"')
            return c.fetchall()
    
    def get_all_admins(self):
        """Ambil semua admin"""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('SELECT id,username, password_hash FROM users WHERE status = "admin"')
            return c.fetchall()
    
    def get_id(self, status) :
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE status=?", (status,))
            result = c.fetchall()
            return [r[0] for r in result]
    
    def verify_user(self, username, password):
        password_hash = hashlib.sha224(password.encode()).hexdigest()
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, status FROM users WHERE username=? AND password_hash=?",
                      (username, password_hash))
            row = c.fetchone()

        if row:
            return {"id":row[0],"username": row[1], "status": row[2]}
        else:
            return None
