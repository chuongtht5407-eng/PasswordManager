import customtkinter as ctk
from tkinter import messagebox
from backend import database, security
from utils import password_gen, anti_keylogger

# --- CẤU HÌNH MÀU SẮC CHUẨN PRO (DARK THEME) ---
BG_COLOR = "#181824"          
PANEL_COLOR = "#252538"       
ACCENT_COLOR = "#00B4D8"      
ACCENT_HOVER = "#0096C7"      
DANGER_COLOR = "#E63946"      
DANGER_HOVER = "#C1121F"
SUCCESS_COLOR = "#2A9D8F"     

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Secure Password Manager Pro")
        self.geometry("900x680") # Kéo dài form ra một chút để chứa thanh search
        self.configure(fg_color=BG_COLOR)
        
        self.master_key = None 
        
        if database.has_master_account():
            self.show_login_screen()
        else:
            self.show_setup_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ================= 1. MÀN HÌNH SETUP =================
    def show_setup_screen(self):
        self.clear_screen()
        
        card = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=15)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(card, text="⚙️ THIẾT LẬP HỆ THỐNG", font=("Segoe UI", 26, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(30, 10), padx=40)
        
        info = ctk.CTkLabel(card, text="Hãy tạo Mật khẩu Master để mã hóa dữ liệu.\nTuyệt đối không được quên mật khẩu này!", 
                            font=("Segoe UI", 13), text_color="#A6A6B0")
        info.pack(pady=(0, 20))
        
        self.setup_entry = ctk.CTkEntry(card, placeholder_text="Nhập Master Password", show="●", 
                                        width=320, height=45, corner_radius=8, border_width=1, font=("Segoe UI", 16))
        self.setup_entry.pack(pady=10)
        
        btn_save = ctk.CTkButton(card, text="KHỞI TẠO KHO LƯU TRỮ", font=("Segoe UI", 14, "bold"), 
                                 width=320, height=45, corner_radius=8, 
                                 fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, command=self.save_master_password)
        btn_save.pack(pady=(20, 30))

    def save_master_password(self):
        pwd = self.setup_entry.get()
        if len(pwd) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu Master phải dài ít nhất 6 ký tự!")
            return
            
        import os
        salt = os.urandom(16) 
        hashed_pwd = security.hash_master_password(pwd)
        
        database.setup_master_account(hashed_pwd, salt)
        messagebox.showinfo("Thành công", "Thiết lập hoàn tất! Vui lòng đăng nhập.")
        self.show_login_screen()

    # ================= 2. MÀN HÌNH ĐĂNG NHẬP =================
    def show_login_screen(self):
        self.clear_screen()
        
        card = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=15)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(card, text="🔒 MỞ KHÓA BẢO MẬT", font=("Segoe UI", 26, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(30, 20), padx=50)
        
        self.login_entry = ctk.CTkEntry(card, placeholder_text="Nhập Master Password", show="●", justify="center",
                                        width=350, height=45, corner_radius=8, border_width=1, font=("Segoe UI", 18, "bold"))
        self.login_entry.pack(pady=10)
        
        btn_login = ctk.CTkButton(card, text="MỞ KHÓA", font=("Segoe UI", 15, "bold"), 
                                  width=350, height=45, corner_radius=8, 
                                  fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, command=self.verify_login)
        btn_login.pack(pady=(10, 20))
        
        vkb_label = ctk.CTkLabel(card, text="⌨️ Bàn phím ảo chống Keylogger", font=("Segoe UI", 12), text_color="#A6A6B0")
        vkb_label.pack(pady=(10, 5))
        
        keyboard_frame = ctk.CTkFrame(card, fg_color="transparent")
        keyboard_frame.pack(pady=(0, 30))
        
        layout = anti_keylogger.get_virtual_keyboard_layout()
        for row in layout:
            row_frame = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
            row_frame.pack(pady=3)
            for key in row:
                btn = ctk.CTkButton(row_frame, text=key, width=45, height=45, font=("Consolas", 16, "bold"),
                                    fg_color="#3A3A4D", hover_color=ACCENT_HOVER, text_color="white", corner_radius=8,
                                    command=lambda k=key: self.login_entry.insert("end", k))
                btn.pack(side="left", padx=3)

    def verify_login(self):
        pwd = self.login_entry.get()
        stored_data = database.get_master_data()
        
        if stored_data and security.verify_master_password(pwd, stored_data[0]):
            self.master_key = security.generate_encryption_key(pwd, stored_data[1])
            self.show_dashboard()
        else:
            messagebox.showerror("Lỗi Cửa", "Sai Master Password! Kẻ xâm nhập bị từ chối.")
            self.login_entry.delete(0, 'end')

    # ================= 3. MÀN HÌNH DASHBOARD =================
    def show_dashboard(self):
        self.clear_screen()
        
        # --- Thanh Header ---
        header = ctk.CTkFrame(self, height=70, fg_color=PANEL_COLOR, corner_radius=0)
        header.pack(fill="x")
        
        title = ctk.CTkLabel(header, text="🛡️ KHO MẬT KHẨU CÁ NHÂN", font=("Segoe UI", 20, "bold"), text_color=ACCENT_COLOR)
        title.pack(side="left", padx=30, pady=20)
        
        btn_logout = ctk.CTkButton(header, text="Đăng Xuất", width=120, height=35, corner_radius=8, font=("Segoe UI", 13, "bold"),
                                   fg_color=DANGER_COLOR, hover_color=DANGER_HOVER, command=self.logout)
        btn_logout.pack(side="right", padx=30)
        
        # --- Panel Thêm Mới ---
        add_frame = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=10)
        add_frame.pack(fill="x", padx=30, pady=20)
        
        self.app_entry = ctk.CTkEntry(add_frame, placeholder_text="Ứng dụng / Website", width=220, height=40)
        self.app_entry.pack(side="left", padx=(20, 10), pady=20)
        
        self.user_entry = ctk.CTkEntry(add_frame, placeholder_text="Tài khoản / Email", width=220, height=40)
        self.user_entry.pack(side="left", padx=10, pady=20)
        
        self.pwd_entry = ctk.CTkEntry(add_frame, placeholder_text="Mật khẩu", width=200, height=40)
        self.pwd_entry.pack(side="left", padx=10, pady=20)
        
        btn_gen = ctk.CTkButton(add_frame, text="⚡ MẠNH", width=70, height=40, corner_radius=8,
                                fg_color="#FCA311", hover_color="#E59800", text_color="black", font=("Arial", 12, "bold"), command=self.fill_generated_password)
        btn_gen.pack(side="left", padx=5)
        
        btn_add = ctk.CTkButton(add_frame, text="LƯU LẠI", width=100, height=40, corner_radius=8, font=("Segoe UI", 13, "bold"),
                                fg_color=SUCCESS_COLOR, hover_color="#21867A", command=self.save_new_password)
        btn_add.pack(side="right", padx=20)
        
        # --- Khu vực Tìm Kiếm (MỚI) ---
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Gõ để tìm kiếm App hoặc Username...", 
                                         width=350, height=35, corner_radius=8, border_width=1, border_color="#3A3A4D")
        self.search_entry.pack(side="left")
        # Bắt sự kiện mỗi khi người dùng nhả phím (gõ chữ) thì sẽ gọi hàm lọc
        self.search_entry.bind("<KeyRelease>", self.filter_passwords)
        
        # --- Danh sách Mật Khẩu ---
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=PANEL_COLOR)
        self.list_frame.pack(padx=30, pady=(0, 20), fill="both", expand=True)
        
        self.load_passwords()

    def filter_passwords(self, event):
        """Hàm kích hoạt khi người dùng gõ vào ô tìm kiếm"""
        query = self.search_entry.get().strip()
        self.load_passwords(search_query=query)

    def fill_generated_password(self):
        strong_pwd = password_gen.generate_strong_password(length=16)
        self.pwd_entry.delete(0, 'end')
        self.pwd_entry.insert(0, strong_pwd)

    def save_new_password(self):
        app = self.app_entry.get()
        user = self.user_entry.get()
        pwd = self.pwd_entry.get()
        
        if not app or not user or not pwd:
            messagebox.showwarning("Nhắc nhở", "Vui lòng nhập đầy đủ thông tin để lưu!")
            return
            
        encrypted_pwd = security.encrypt_data(pwd, self.master_key)
        database.add_entry(app, user, encrypted_pwd)
        
        self.app_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.pwd_entry.delete(0, 'end')
        
        # Nếu đang tìm kiếm thì xóa tìm kiếm đi để hiện lại toàn bộ danh sách mới nhất
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, 'end')
            
        self.load_passwords()

    def load_passwords(self, search_query=""):
        """Tải danh sách, hỗ trợ lọc theo từ khóa tìm kiếm"""
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        entries = database.get_all_entries()
        
        # Thuật toán lọc (Lọc không phân biệt hoa thường)
        if search_query:
            entries = [e for e in entries if search_query.lower() in e[1].lower() or search_query.lower() in e[2].lower()]
            
        if not entries:
            # Hiện thông báo nếu tìm không thấy hoặc kho trống
            msg = "🔍 Không tìm thấy kết quả nào phù hợp!" if search_query else "Kho lưu trữ trống. Hãy thêm mật khẩu đầu tiên!"
            empty_lbl = ctk.CTkLabel(self.list_frame, text=msg, text_color="#A6A6B0", font=("Segoe UI", 14))
            empty_lbl.pack(pady=40)
            return
            
        for entry in entries:
            row_id, app, user, enc_pwd = entry
            
            row_frame = ctk.CTkFrame(self.list_frame, fg_color=PANEL_COLOR, height=60, corner_radius=8)
            row_frame.pack(fill="x", pady=5)
            row_frame.pack_propagate(False) 
            
            lbl_app = ctk.CTkLabel(row_frame, text=app, font=("Segoe UI", 16, "bold"), text_color=ACCENT_COLOR, anchor="w", width=200)
            lbl_app.pack(side="left", padx=20)
            
            lbl_user = ctk.CTkLabel(row_frame, text=user, font=("Consolas", 14), text_color="white", anchor="w")
            lbl_user.pack(side="left", padx=20, fill="x", expand=True)
            
            btn_copy = ctk.CTkButton(row_frame, text="Copy", width=80, height=32, corner_radius=6, font=("Segoe UI", 12, "bold"),
                                     fg_color="#3A3A4D", hover_color=ACCENT_HOVER,
                                     command=lambda e=enc_pwd: anti_keylogger.secure_copy(security.decrypt_data(e, self.master_key)))
            btn_copy.pack(side="right", padx=(5, 20))
            
            btn_delete = ctk.CTkButton(row_frame, text="Xóa", width=60, height=32, corner_radius=6, font=("Segoe UI", 12, "bold"),
                                       fg_color="transparent", hover_color=DANGER_HOVER, border_width=1, border_color=DANGER_COLOR, text_color=DANGER_COLOR,
                                       command=lambda i=row_id: self.delete_password(i))
            btn_delete.pack(side="right", padx=5)

    def delete_password(self, entry_id):
        if messagebox.askyesno("Xác nhận Xóa", "Tài khoản này sẽ bị xóa vĩnh viễn khỏi kho. Bạn chắc chứ?"):
            database.delete_entry(entry_id)
            # Lấy giá trị tìm kiếm hiện tại để tải lại danh sách đúng như người dùng đang xem
            current_query = self.search_entry.get()
            self.load_passwords(search_query=current_query)

    def logout(self):
        self.master_key = None 
        self.show_login_screen()