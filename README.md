# 🛡️ Secure Password Manager Pro

**Dự án môn học:** Xây dựng hệ thống quản lý mật khẩu cá nhân an toàn.
**Nhóm thực hiện:** Nhóm 3 người (Chương, Thủy, Bảo)

## 🌟 Tính năng nổi bật
Dự án hoàn thành xuất sắc các yêu cầu bảo mật cốt lõi:
1. **Mã hóa cấp cao (AES-256):** Master Password được băm bằng SHA-256 & Salt. Dữ liệu các tài khoản được mã hóa AES-256 cực kỳ an toàn.
2. **Tạo mật khẩu siêu mạnh:** Sử dụng thư viện `secrets` sinh chuỗi ngẫu nhiên chuẩn mã hóa bảo mật.
3. **Chống Keylogger (Anti-Keylogger):** Tích hợp Bàn phím ảo (Virtual Keyboard) ở màn hình đăng nhập.
4. **Chống đánh cắp Clipboard:** Tính năng Copy an toàn tự động xóa mật khẩu khỏi bộ nhớ tạm sau 10 giây.
5. **Giao diện hiện đại:** Được xây dựng bằng `CustomTkinter`.

## 🚀 Hướng dẫn cài đặt và sử dụng

**Bước 1:** Tải mã nguồn về máy:
```bash
git clone https://github.com/chuongtht5407-eng/PasswordManager.git

**Bước 2:** Cài đặt các thư viện yêu cầu: 
pip install -r requirements.txt

**Bước 3:** Khởi chạy ứng dụng: 
python main.py 
(Lưu ý: Ở lần chạy đầu tiên, hệ thống sẽ yêu cầu bạn tạo Master Password để bảo vệ kho dữ liệu).
