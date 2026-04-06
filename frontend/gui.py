import os
import customtkinter as ctk
from tkinter import messagebox
from backend import database, security
from utils import password_gen, anti_keylogger

# --- CẤU HÌNH MÀU SẮC CHUẨN PRO (DARK THEME) ---
BG_COLOR = "#151625"
PANEL_COLOR = "#1F2240"
PANEL_ALT = "#262A4B"
ACCENT_COLOR = "#34D399"
ACCENT_HOVER = "#22C55E"
DANGER_COLOR = "#EF4444"
DANGER_HOVER = "#DC2626"
SUCCESS_COLOR = "#10B981"
TEXT_COLOR = "#E2E8F0"
SUBTEXT_COLOR = "#94A3B8"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Secure Password Manager Pro")
        self.geometry("980x720")
        self.minsize(960, 700)
        self.configure(fg_color=BG_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.master_key = None
        self.active_screen = None

        if database.has_master_account():
            self.show_login_screen()
        else:
            self.show_setup_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _set_active_screen(self, name):
        self.active_screen = name
        self.bind("<Return>", self.handle_enter)

    def handle_enter(self, event):
        if self.active_screen == "setup":
            self.save_master_password()
        elif self.active_screen == "login":
            self.verify_login()
        elif self.active_screen == "recovery":
            self.verify_recovery_key_action()

    # ================= 1. MÀN HÌNH SETUP =================
    def show_setup_screen(self):
        self.clear_screen()
        self._set_active_screen("setup")

        card = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=20, border_width=1, border_color="#2E3250", width=540, height=380)
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(card, text="⚙️ THIẾT LẬP HỆ THỐNG", font=("Segoe UI", 26, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(30, 10))

        info = ctk.CTkLabel(card,
                            text="Tạo ngay mật khẩu Master an toàn để mã hóa toàn bộ dữ liệu của bạn.",
                            font=("Segoe UI", 13), text_color=SUBTEXT_COLOR, wraplength=460, justify="center")
        info.pack(pady=(0, 20), padx=20)

        self.setup_entry = ctk.CTkEntry(card, placeholder_text="Nhập Master Password", show="●",
                                        width=420, height=48, corner_radius=12, border_width=1, font=("Segoe UI", 16))
        self.setup_entry.pack(pady=10)

        btn_save = ctk.CTkButton(card, text="KHỞI TẠO KHO LƯU TRỮ", font=("Segoe UI", 15, "bold"),
                                 width=420, height=48, corner_radius=14,
                                 fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, command=self.save_master_password)
        btn_save.pack(pady=(20, 15))

        hint = ctk.CTkLabel(card, text="Mật khẩu dài ít nhất 6 ký tự. Giữ bí mật và an toàn.",
                            font=("Segoe UI", 12), text_color=SUBTEXT_COLOR)
        hint.pack()

    def save_master_password(self):
        pwd = self.setup_entry.get()
        if len(pwd) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu Master phải dài ít nhất 6 ký tự!")
            return
            
        import os
        salt = os.urandom(16)
        hashed_pwd = security.hash_master_password(pwd)
        recovery_key = security.generate_recovery_key()
        recovery_hash = security.hash_recovery_key(recovery_key)
        
        database.setup_master_account(hashed_pwd, salt, recovery_hash)
        self.show_recovery_key_modal(recovery_key)

    # ================= 2. MÀN HÌNH ĐĂNG NHẬP =================
    def show_login_screen(self):
        self.clear_screen()
        self._set_active_screen("login")

        card = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=20, border_width=1, border_color="#2E3250", width=600, height=460)
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(card, text="🔒 MỞ KHÓA BẢO MẬT", font=("Segoe UI", 26, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(card, text="Sử dụng mật khẩu Master để truy cập kho mật khẩu an toàn của bạn.",
                                font=("Segoe UI", 13), text_color=SUBTEXT_COLOR, wraplength=520, justify="center")
        subtitle.pack(pady=(0, 20), padx=20)

        self.login_entry = ctk.CTkEntry(card, placeholder_text="Nhập Master Password", show="●", justify="center",
                                        width=450, height=48, corner_radius=12, border_width=1, font=("Segoe UI", 18, "bold"))
        self.login_entry.pack(pady=10)

        btn_login = ctk.CTkButton(card, text="MỞ KHÓA", font=("Segoe UI", 15, "bold"),
                                  width=450, height=48, corner_radius=14,
                                  fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, command=self.verify_login)
        btn_login.pack(pady=(15, 15))

        recovery_label = "Đổi Recovery Key" if database.get_recovery_hash() else "Thiết lập Recovery Key"
        btn_setup_recovery = ctk.CTkButton(card, text=recovery_label, width=220, height=40, corner_radius=12,
                                           fg_color="transparent", hover_color=PANEL_ALT, border_width=1,
                                           border_color=ACCENT_COLOR, text_color=ACCENT_COLOR,
                                           command=self.setup_recovery_key)
        btn_setup_recovery.pack(pady=(0, 10))

        info = ctk.CTkLabel(card, text="⌨️ Bàn phím ảo chống Keylogger", font=("Segoe UI", 12), text_color=SUBTEXT_COLOR)
        info.pack(pady=(5, 5))

        btn_forgot = ctk.CTkButton(card, text="Quên mật khẩu Master?", width=220, height=40, corner_radius=12,
                                   fg_color="transparent", hover_color=PANEL_ALT, border_width=1, border_color=ACCENT_COLOR,
                                   text_color=ACCENT_COLOR, command=self.show_recovery_screen)
        btn_forgot.pack(pady=(0, 10))

        keyboard_frame = ctk.CTkFrame(card, fg_color="transparent")
        keyboard_frame.pack(pady=(0, 20))

        layout = anti_keylogger.get_virtual_keyboard_layout()
        for row in layout:
            row_frame = ctk.CTkFrame(keyboard_frame, fg_color="transparent")
            row_frame.pack(pady=4)
            for key in row:
                btn = ctk.CTkButton(row_frame, text=key, width=44, height=44, font=("Consolas", 15, "bold"),
                                    fg_color=PANEL_ALT, hover_color=ACCENT_HOVER, text_color=TEXT_COLOR, corner_radius=10,
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

    def setup_recovery_key(self):
        pwd = self.login_entry.get().strip()
        if not pwd:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Master Password để xác thực trước khi tạo Recovery Key.")
            return

        stored_data = database.get_master_data()
        if not stored_data or not security.verify_master_password(pwd, stored_data[0]):
            messagebox.showerror("Lỗi", "Master Password không chính xác. Không thể tạo Recovery Key.")
            self.login_entry.delete(0, 'end')
            return

        recovery_key = security.generate_recovery_key()
        recovery_hash = security.hash_recovery_key(recovery_key)
        database.set_recovery_hash(recovery_hash)

        messagebox.showinfo("Recovery Key", "Recovery Key đã được tạo. Hãy lưu cẩn thận để có thể khôi phục trong trường hợp quên Master Password.")
        self.show_recovery_key_modal(recovery_key)

    # ================= 3. MÀN HÌNH DASHBOARD =================
    def show_dashboard(self):
        self.clear_screen()
        self._set_active_screen(None)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, height=100, fg_color=PANEL_COLOR, corner_radius=0, border_width=1, border_color="#2E3250")
        header.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(header, text="🛡️ KHO MẬT KHẨU CÁ NHÂN", font=("Segoe UI", 22, "bold"), text_color=ACCENT_COLOR)
        title.grid(row=0, column=0, sticky="w", padx=24, pady=22)

        btn_logout = ctk.CTkButton(header, text="Đăng Xuất", width=120, height=38, corner_radius=12,
                                   fg_color=DANGER_COLOR, hover_color=DANGER_HOVER, command=self.logout)
        btn_logout.grid(row=0, column=2, sticky="e", padx=24, pady=22)

        stats_frame = ctk.CTkFrame(header, fg_color=PANEL_ALT, corner_radius=14, border_width=1, border_color="#2E3250")
        stats_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=24, pady=(0, 18))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.total_label = ctk.CTkLabel(stats_frame, text="0", font=("Segoe UI", 24, "bold"), text_color=TEXT_COLOR)
        self.total_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        total_caption = ctk.CTkLabel(stats_frame, text="Mật khẩu đã lưu", font=("Segoe UI", 12), text_color=SUBTEXT_COLOR)
        total_caption.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.safe_label = ctk.CTkLabel(stats_frame, text="AN TOÀN", font=("Segoe UI", 24, "bold"), text_color=ACCENT_COLOR)
        self.safe_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="w")
        safe_caption = ctk.CTkLabel(stats_frame, text="Dữ liệu được mã hóa", font=("Segoe UI", 12), text_color=SUBTEXT_COLOR)
        safe_caption.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")

        self.recent_label = ctk.CTkLabel(stats_frame, text="SẴN SÀNG", font=("Segoe UI", 24, "bold"), text_color=TEXT_COLOR)
        self.recent_label.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="w")
        recent_caption = ctk.CTkLabel(stats_frame, text="Truy cập nhanh, quản lý dễ dàng", font=("Segoe UI", 12), text_color=SUBTEXT_COLOR)
        recent_caption.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="w")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content.grid_rowconfigure(2, weight=1)
        content.grid_columnconfigure(0, weight=1)

        add_frame = ctk.CTkFrame(content, fg_color=PANEL_COLOR, corner_radius=16, border_width=1, border_color="#2E3250")
        add_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 12))
        add_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.app_entry = ctk.CTkEntry(add_frame, placeholder_text="Ứng dụng / Website", width=220, height=44, corner_radius=14)
        self.app_entry.grid(row=0, column=0, padx=(20, 10), pady=18, sticky="ew")

        self.user_entry = ctk.CTkEntry(add_frame, placeholder_text="Tài khoản / Email", width=220, height=44, corner_radius=14)
        self.user_entry.grid(row=0, column=1, padx=10, pady=18, sticky="ew")

        self.pwd_entry = ctk.CTkEntry(add_frame, placeholder_text="Mật khẩu", width=220, height=44, corner_radius=14)
        self.pwd_entry.grid(row=0, column=2, padx=10, pady=18, sticky="ew")

        btn_gen = ctk.CTkButton(add_frame, text="⚡ MẠNH", width=96, height=44, corner_radius=14,
                                fg_color="#F59E0B", hover_color="#D97706", text_color="black", font=("Arial", 12, "bold"),
                                command=self.fill_generated_password)
        btn_gen.grid(row=0, column=3, padx=(10, 10), pady=18, sticky="e")

        btn_add = ctk.CTkButton(add_frame, text="LƯU LẠI", width=120, height=44, corner_radius=14,
                                fg_color=SUCCESS_COLOR, hover_color="#059669", font=("Segoe UI", 14, "bold"),
                                command=self.save_new_password)
        btn_add.grid(row=0, column=4, padx=(0, 20), pady=18)

        search_frame = ctk.CTkFrame(content, fg_color=PANEL_COLOR, corner_radius=16, border_width=1, border_color="#2E3250")
        search_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 12))
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Gõ để tìm kiếm App hoặc Username...",
                                         width=360, height=44, corner_radius=14, border_width=1, border_color="#3A3A4D")
        self.search_entry.grid(row=0, column=0, padx=20, pady=18, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_passwords)

        self.list_frame = ctk.CTkScrollableFrame(content, fg_color="transparent", scrollbar_button_color=PANEL_COLOR)
        self.list_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 8))

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
            if hasattr(self, 'total_label'):
                self.total_label.configure(text="0")
            return
            
        if hasattr(self, 'total_label'):
            self.total_label.configure(text=str(len(entries)))

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

    def copy_to_clipboard(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Sao chép", "Recovery Key đã được sao chép vào bộ nhớ tạm.")

    def show_recovery_key_modal(self, recovery_key: str):
        modal = ctk.CTkToplevel(self)
        modal.title("Recovery Key")
        modal.geometry("540x260")
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()
        modal.protocol("WM_DELETE_WINDOW", lambda: [modal.destroy(), self.show_login_screen()])

        frame = ctk.CTkFrame(modal, fg_color=PANEL_COLOR, corner_radius=20, border_width=1, border_color="#2E3250")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        title = ctk.CTkLabel(frame, text="🗝️ Recovery Key Đã Tạo", font=("Segoe UI", 22, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(frame, text="Lưu lại mã này an toàn. Nếu quên Master Password, bạn sẽ cần nó để khôi phục.",
                                font=("Segoe UI", 13), text_color=SUBTEXT_COLOR, wraplength=480, justify="center")
        subtitle.pack(pady=(0, 15), padx=16)

        recovery_entry = ctk.CTkEntry(frame, width=460, height=44, corner_radius=14, font=("Segoe UI", 14))
        recovery_entry.insert(0, recovery_key)
        recovery_entry.configure(state="readonly")
        recovery_entry.pack(pady=(0, 10))

        btn_copy = ctk.CTkButton(frame, text="Sao chép Recovery Key", width=220, height=44, corner_radius=14,
                                fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, command=lambda: self.copy_to_clipboard(recovery_key))
        btn_copy.pack(pady=(0, 12))

        btn_close = ctk.CTkButton(frame, text="Tiếp tục", width=220, height=44, corner_radius=14,
                                fg_color=SUCCESS_COLOR, hover_color="#059669", command=lambda: [modal.destroy(), self.show_login_screen()])
        btn_close.pack()

    def show_recovery_screen(self):
        self.clear_screen()
        self._set_active_screen("recovery")

        card = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=20, border_width=1, border_color="#2E3250", width=600, height=520)
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(card, text="🔑 KHÔI PHỤC TÀI KHOẢN", font=("Segoe UI", 26, "bold"), text_color=ACCENT_COLOR)
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(card, text="Nhập Recovery Key và đặt lại Master Password mới. Dữ liệu cũ vẫn được giữ nguyên sau khi recovery thành công.",
                                font=("Segoe UI", 13), text_color=SUBTEXT_COLOR, wraplength=520, justify="center")
        subtitle.pack(pady=(0, 20), padx=20)

        self.recovery_entry = ctk.CTkEntry(card, placeholder_text="Nhập Recovery Key", width=450, height=48,
                                           corner_radius=12, border_width=1, font=("Segoe UI", 16))
        self.recovery_entry.pack(pady=(0, 10))

        self.new_password_entry = ctk.CTkEntry(card, placeholder_text="Nhập Master Password mới", width=450, height=48,
                                                corner_radius=12, border_width=1, font=("Segoe UI", 16), show='*')
        self.new_password_entry.pack(pady=(0, 10))

        self.confirm_password_entry = ctk.CTkEntry(card, placeholder_text="Xác nhận Master Password mới", width=450, height=48,
                                                    corner_radius=12, border_width=1, font=("Segoe UI", 16), show='*')
        self.confirm_password_entry.pack(pady=(0, 10))

        note = ctk.CTkLabel(card, text="Lưu ý: Recovery Key sẽ chỉ sử dụng được một lần. Sau khi thay mật khẩu, bạn cần tạo lại Recovery Key.",
                             font=("Segoe UI", 12), text_color=SUBTEXT_COLOR, wraplength=520, justify="center")
        note.pack(pady=(8, 16), padx=20)

        btn_verify = ctk.CTkButton(card, text="Đặt lại Master Password", font=("Segoe UI", 15, "bold"),
                                   width=450, height=48, corner_radius=14,
                                   fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
                                   command=self.verify_recovery_key_action)
        btn_verify.pack(pady=(0, 10))

        btn_back = ctk.CTkButton(card, text="Quay lại Đăng nhập", width=220, height=44, corner_radius=14,
                                 fg_color="transparent", hover_color=PANEL_ALT, border_width=1, border_color=ACCENT_COLOR,
                                 text_color=ACCENT_COLOR, command=self.show_login_screen)
        btn_back.pack()

    def verify_recovery_key_action(self):
        recovery_code = self.recovery_entry.get().strip()
        if not recovery_code:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Recovery Key để tiếp tục.")
            return

        stored_hash = database.get_recovery_hash()
        if not stored_hash:
            messagebox.showerror("Lỗi", "Recovery Key chưa được thiết lập hoặc không tồn tại.")
            self.show_login_screen()
            return

        if security.verify_recovery_key(recovery_code, stored_hash):
            new_master_pwd = self.new_password_entry.get().strip()
            confirm_pwd = self.confirm_password_entry.get().strip()
            if not new_master_pwd or len(new_master_pwd) < 6:
                messagebox.showwarning("Cảnh báo", "Master Password phải có ít nhất 6 ký tự.")
                return
            if new_master_pwd != confirm_pwd:
                messagebox.showwarning("Cảnh báo", "Mật khẩu mới và xác nhận mật khẩu không khớp.")
                return

            confirmed = messagebox.askyesno(
                "Xác nhận khôi phục",
                "Recovery Key hợp lệ. Bạn sẽ đặt lại Master Password và giữ nguyên dữ liệu đã lưu. Tiếp tục?"
            )
            if confirmed:
                hashed_pwd = security.hash_master_password(new_master_pwd)
                salt = os.urandom(16)
                database.update_master_password(hashed_pwd, salt)
                messagebox.showinfo("Thành công", "Master Password đã được đặt lại. Dữ liệu cũ được giữ nguyên. Vui lòng đăng nhập lại.")
                self.show_login_screen()
        else:
            messagebox.showerror("Lỗi", "Recovery Key không chính xác. Vui lòng thử lại.")
            self.recovery_entry.delete(0, 'end')