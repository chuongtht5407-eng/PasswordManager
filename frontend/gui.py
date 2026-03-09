import customtkinter as ctk
from tkinter import messagebox
from backend import database, security
from utils import password_gen, anti_keylogger

# Cấu hình giao diện mặc định
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Secure Password Manager Pro")
        self.geometry("800x600")
        
        self.master_key = None # Biến lưu khóa mã hóa (AES Key) sau khi đăng nhập
        
        # Kiểm tra xem có tài khoản Master chưa để chuyển màn hình phù hợp
        if database.has_master_account():
            self.show_login_screen()
        else:
            self.show_setup_screen()

    def clear_screen(self):
        """Xóa sạch các widget hiện tại để vẽ màn hình mới"""
        for widget in self.winfo_children():
            widget.destroy()

    # ================= MÀN HÌNH SETUP (CHẠY LẦN ĐẦU) =================
    def show_setup_screen(self):
        self.clear_screen()
        
        title = ctk.CTkLabel(self, text="⚙️ THIẾT LẬP LẦN ĐẦU", font=("Arial", 28, "bold"))
        title.pack(pady=(50, 20))
        
        info = ctk.CTkLabel(self, text="Hãy tạo Mật khẩu Master. Mật khẩu này dùng để mở khóa kho dữ liệu.\nLƯU Ý: Đừng quên nó, nếu không bạn sẽ mất toàn bộ dữ liệu!")
        info.pack(pady=10)
        
        self.setup_entry = ctk.CTkEntry(self, placeholder_text="Nhập Master Password", show="*", width=300, font=("Arial", 16))
        self.setup_entry.pack(pady=10)
        
        btn_save = ctk.CTkButton(self, text="Lưu và Bắt đầu", font=("Arial", 16, "bold"), command=self.save_master_password)
        btn_save.pack(pady=20)

    def save_master_password(self):
        pwd = self.setup_entry.get()
        if len(pwd) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu Master phải dài ít nhất 6 ký tự!")
            return
            
        import os
        salt = os.urandom(16) # Tạo muối ngẫu nhiên
        hashed_pwd = security.hash_master_password(pwd)
        
        database.setup_master_account(hashed_pwd, salt)
        messagebox.showinfo("Thành công", "Đã thiết lập xong! Vui lòng đăng nhập.")
        self.show_login_screen()

    # ================= MÀN HÌNH ĐĂNG NHẬP (CÓ BÀN PHÍM ẢO) =================
    def show_login_screen(self):
        self.clear_screen()
        
        title = ctk.CTkLabel(self, text="🔒 ĐĂNG NHẬP", font=("Arial", 28, "bold"))
        title.pack(pady=(40, 20))
        
        self.login_entry = ctk.CTkEntry(self, placeholder_text="Nhập Master Password", show="*", width=300, font=("Arial", 16))
        self.login_entry.pack(pady=10)
        
        btn_login = ctk.CTkButton(self, text="Mở Khóa", font=("Arial", 16, "bold"), command=self.verify_login)
        btn_login.pack(pady=20)
        
        # --- Vẽ Bàn Phím Ảo (Anti-Keylogger) ---
        vkb_label = ctk.CTkLabel(self, text="Bàn phím ảo (Chống Keylogger):", text_color="gray")
        vkb_label.pack(pady=(20, 5))
        
        keyboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        keyboard_frame.pack()
        
        layout = anti_keylogger.get_virtual_keyboard_layout()
        for row in layout:
            row_frame = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
            row_frame.pack(pady=2)
            for key in row:
                # Dùng lambda với tham số mặc định k=key để tránh lỗi tham chiếu muộn
                btn = ctk.CTkButton(row_frame, text=key, width=40, height=40, font=("Arial", 14),
                                    command=lambda k=key: self.login_entry.insert("end", k))
                btn.pack(side="left", padx=2)

    def verify_login(self):
        pwd = self.login_entry.get()
        stored_data = database.get_master_data()
        
        if stored_data and security.verify_master_password(pwd, stored_data[0]):
            # Nếu đúng, tạo khóa AES-256 để dùng suốt phiên làm việc
            self.master_key = security.generate_encryption_key(pwd, stored_data[1])
            self.show_dashboard()
        else:
            messagebox.showerror("Lỗi", "Sai Master Password!")
            self.login_entry.delete(0, 'end')

    # ================= MÀN HÌNH DASHBOARD =================
    def show_dashboard(self):
        self.clear_screen()
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(header_frame, text="KHO MẬT KHẨU CỦA BẠN", font=("Arial", 24, "bold"))
        title.pack(side="left")
        
        btn_logout = ctk.CTkButton(header_frame, text="Đăng xuất", width=100, fg_color="red", hover_color="darkred", command=self.logout)
        btn_logout.pack(side="right")
        
        # Khu vực thêm mật khẩu mới
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(fill="x", padx=20, pady=10)
        
        self.app_entry = ctk.CTkEntry(add_frame, placeholder_text="Tên App (VD: Facebook)", width=200)
        self.app_entry.pack(side="left", padx=10, pady=10)
        
        self.user_entry = ctk.CTkEntry(add_frame, placeholder_text="Tên đăng nhập", width=200)
        self.user_entry.pack(side="left", padx=10, pady=10)
        
        self.pwd_entry = ctk.CTkEntry(add_frame, placeholder_text="Mật khẩu", width=200)
        self.pwd_entry.pack(side="left", padx=10, pady=10)
        
        btn_gen = ctk.CTkButton(add_frame, text="Tạo MK Mạnh", width=100, command=self.fill_generated_password)
        btn_gen.pack(side="left", padx=5)
        
        btn_add = ctk.CTkButton(add_frame, text="Lưu", width=80, fg_color="green", hover_color="darkgreen", command=self.save_new_password)
        btn_add.pack(side="left", padx=10)
        
        # Khu vực danh sách mật khẩu
        self.list_frame = ctk.CTkScrollableFrame(self, width=700, height=350)
        self.list_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.load_passwords()

    def fill_generated_password(self):
        """Gọi Utils để tạo mật khẩu mạnh và điền vào ô nhập"""
        strong_pwd = password_gen.generate_strong_password(length=16)
        self.pwd_entry.delete(0, 'end')
        self.pwd_entry.insert(0, strong_pwd)

    def save_new_password(self):
        app = self.app_entry.get()
        user = self.user_entry.get()
        pwd = self.pwd_entry.get()
        
        if not app or not user or not pwd:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin!")
            return
            
        encrypted_pwd = security.encrypt_data(pwd, self.master_key)
        database.add_entry(app, user, encrypted_pwd)
        
        # Xóa form và tải lại danh sách
        self.app_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.pwd_entry.delete(0, 'end')
        self.load_passwords()

    def load_passwords(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        entries = database.get_all_entries()
        
        # Tiêu đề cột
        header = ctk.CTkLabel(self.list_frame, text=f"{'APP':<20} | {'USERNAME':<30} | {'HÀNH ĐỘNG'}", font=("Arial", 14, "bold"), anchor="w")
        header.pack(fill="x", padx=10, pady=5)
        
        for entry in entries:
            row_id, app, user, enc_pwd = entry
            
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            info_label = ctk.CTkLabel(row_frame, text=f"{app:<20} | {user:<30}", font=("Consolas", 14), anchor="w")
            info_label.pack(side="left", padx=10)
            
            # Nút Copy (Giải mã trực tiếp vào Clipboard, không hiện lên màn hình)
            btn_copy = ctk.CTkButton(row_frame, text="Copy MK", width=80, 
                                     command=lambda e=enc_pwd: anti_keylogger.secure_copy(security.decrypt_data(e, self.master_key)))
            btn_copy.pack(side="right", padx=5)
            
            # Nút Xóa
            btn_delete = ctk.CTkButton(row_frame, text="Xóa", width=60, fg_color="red", hover_color="darkred",
                                       command=lambda i=row_id: self.delete_password(i))
            btn_delete.pack(side="right", padx=5)

    def delete_password(self, entry_id):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tài khoản này?"):
            database.delete_entry(entry_id)
            self.load_passwords()

    def logout(self):
        self.master_key = None # Xóa key khỏi RAM
        self.show_login_screen()