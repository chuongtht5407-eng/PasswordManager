# File này quản lý file database password_manager.db. Code được viết tách bạch các hàm thêm, sửa, xóa, và tự động đóng/mở kết nối để tránh lỗi "Database is locked" (một lỗi sinh viên rất hay mắc phải).

import sqlite3



DB_FILE = "password_manager.db"



def get_connection():

    """Tạo kết nối tới database SQLite"""

    return sqlite3.connect(DB_FILE)



def init_db():

    """Khởi tạo cấu trúc bảng nếu chạy lần đầu"""

    conn = get_connection()

    cursor = conn.cursor()

   

    # Bảng 1: Lưu Master Password (Chỉ chứa duy nhất 1 dòng)

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS master_user (

            id INTEGER PRIMARY KEY DEFAULT 1,

            password_hash TEXT NOT NULL,

            salt BLOB NOT NULL,

            recovery_hash TEXT

        )

    ''')

   

    cursor.execute("PRAGMA table_info(master_user)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    if "recovery_hash" not in existing_columns:
        cursor.execute("ALTER TABLE master_user ADD COLUMN recovery_hash TEXT")

    # Bảng 2: Lưu các mật khẩu được mã hóa

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS vault (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            app_name TEXT NOT NULL,

            username TEXT NOT NULL,

            encrypted_password TEXT NOT NULL

        )

    ''')

   

    conn.commit()

    conn.close()



# ======== CÁC HÀM XỬ LÝ TÀI KHOẢN MASTER ========



def has_master_account() -> bool:

    """Kiểm tra xem người dùng đã thiết lập Master Password chưa"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM master_user WHERE id = 1")

    row = cursor.fetchone()

    conn.close()

    return row is not None



def setup_master_account(password_hash: str, salt: bytes, recovery_hash: str = None):

    """Lưu Master Password, Salt và Recovery Hash lần đầu tiên"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO master_user (id, password_hash, salt, recovery_hash) VALUES (1, ?, ?, ?)",

                   (password_hash, salt, recovery_hash))

    conn.commit()

    conn.close()



def get_master_data():

    """Lấy Hash và Salt để kiểm tra lúc đăng nhập"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, salt FROM master_user WHERE id = 1")

    row = cursor.fetchone()

    conn.close()

    return row # Trả về tuple: (password_hash, salt)


def set_recovery_hash(recovery_hash: str):

    """Lưu hash của recovery key vào cơ sở dữ liệu"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("UPDATE master_user SET recovery_hash = ? WHERE id = 1", (recovery_hash,))

    conn.commit()

    conn.close()


def get_recovery_hash():

    """Lấy recovery hash để xác thực recovery key"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT recovery_hash FROM master_user WHERE id = 1")

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None


def has_recovery_key() -> bool:

    """Kiểm tra xem recovery key đã được cấu hình chưa."""

    return get_recovery_hash() is not None


def update_master_password(new_password_hash: str, new_salt: bytes):
    """Cập nhật Master Password mới mà không xóa dữ liệu vault. Đồng thời xóa recovery_hash để vô hiệu hóa recovery key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE master_user
        SET password_hash = ?, salt = ?, recovery_hash = NULL
        WHERE id = 1
    """, (new_password_hash, new_salt))
    conn.commit()
    conn.close()


def reset_all_data():

    """Xóa toàn bộ dữ liệu vault và thông tin master để cấu hình lại từ đầu"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM vault")

    cursor.execute("DELETE FROM master_user WHERE id = 1")

    conn.commit()

    conn.close()


# ======== CÁC HÀM QUẢN LÝ KHO MẬT KHẨU (VAULT) ========



def add_entry(app_name: str, username: str, encrypted_password: str):

    """Thêm một tài khoản mới vào kho"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO vault (app_name, username, encrypted_password) VALUES (?, ?, ?)",

                   (app_name, username, encrypted_password))

    conn.commit()

    conn.close()



def get_all_entries() -> list:

    """Lấy danh sách tất cả các tài khoản"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT id, app_name, username, encrypted_password FROM vault")

    rows = cursor.fetchall()

    conn.close()

    return rows



def delete_entry(entry_id: int):

    """Xóa một tài khoản khỏi kho"""

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM vault WHERE id = ?", (entry_id,))

    conn.commit()

    conn.close()