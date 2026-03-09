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
            salt BLOB NOT NULL
        )
    ''')
    
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

def setup_master_account(password_hash: str, salt: bytes):
    """Lưu Master Password và Salt lần đầu tiên"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO master_user (id, password_hash, salt) VALUES (1, ?, ?)", 
                   (password_hash, salt))
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