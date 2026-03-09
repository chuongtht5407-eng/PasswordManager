from backend import database
from frontend.gui import PasswordManagerApp

def main():
    print("[Hệ thống] Đang khởi động Secure Password Manager...")
    
    # 1. Khởi tạo Database nếu chưa có
    database.init_db()
    
    # 2. Khởi chạy Giao diện
    app = PasswordManagerApp()
    app.mainloop()

if __name__ == "__main__":
    main()