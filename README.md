# 🛡️ Secure Password Manager Pro

## 1. 🌟 Tổng quan về ứng dụng
* **Mô hình hoạt động:** Đây là một ứng dụng **Desktop Offline** (chạy cục bộ trên máy tính, hoàn toàn không cần kết nối internet).
* **Mục đích:** Đóng vai trò như một "Chiếc két sắt kỹ thuật số". Thay vì phải ghi nhớ hàng tá mật khẩu Facebook, Zalo, Ngân hàng... bạn chỉ cần nhớ **MỘT Mật Khẩu Chủ (Master Password)** duy nhất.
* **Triết lý bảo mật:** **"Zero-Knowledge"** (Không ai biết, kể cả hệ thống). Mọi dữ liệu đều được mã hóa cục bộ ngay trên máy của bạn. Dù ai đó có ăn cắp được file database `password_manager.db`, họ cũng chỉ nhìn thấy những đoạn mã loằng ngoằng vô nghĩa nếu không có Master Password.

---

## 2. 🔐 Các tính năng bảo mật cốt lõi ("Ăn tiền")

* **🛡️ Tầng 1: Chống Keylogger bằng Bàn phím ảo (Virtual Keyboard)**
  * **Vấn đề:** Nếu máy bị nhiễm virus theo dõi bàn phím (Keylogger), hacker có thể ghi lại được lúc bạn gõ mật khẩu.
  * **Giải pháp:** Tích hợp Bàn phím ảo trên màn hình đăng nhập. Người dùng thao tác bằng chuột, vô hiệu hóa hoàn toàn các phần mềm Keylogger.

* **🛡️ Tầng 2: Băm mật khẩu & Thêm "Muối" (Hash & Salt)**
  * **Hoạt động:** Master Password KHÔNG bao giờ được lưu trực tiếp vào Database. Hệ thống sinh ra một chuỗi ngẫu nhiên (`Salt`), trộn chung với mật khẩu, và băm nát bằng thuật toán **SHA-256**.
  * **Hiệu quả:** Chống lại các cuộc tấn công dò bảng băm (Rainbow table attacks).

* **🛡️ Tầng 3: Mã hóa dữ liệu bằng chuẩn Quân đội (AES-256)**
  * **Hoạt động:** Sử dụng Master Password làm "chìa khóa" (Key) để mã hóa toàn bộ mật khẩu các tài khoản bằng chuẩn **AES-256** (Chuẩn bảo mật cao nhất hiện nay, được các ngân hàng sử dụng).
  * **Hiệu quả:** Trong Database chỉ chứa dữ liệu đã mã hóa. Chỉ khi đăng nhập thành công, hệ thống mới dùng Key để giải mã và hiển thị.

* **🛡️ Tầng 4: Tự động xóa Clipboard (Chống đọc lén bộ nhớ tạm)**
  * **Vấn đề:** Khi copy mật khẩu, dữ liệu nằm trong Clipboard. Người khác dùng máy có thể dán (Ctrl+V) ra để lấy cắp.
  * **Giải pháp:** Tính năng an toàn tự động đếm ngược **10 giây**. Sau 10 giây, bộ nhớ Clipboard tự động bị xóa sạch.

* **🛡️ Tầng 5: Thuật toán đổi mật khẩu chủ phức tạp (Re-encryption)**
  * **Hoạt động:** Khi đổi Master Password, hệ thống sẽ tự động giải mã toàn bộ dữ liệu bằng pass cũ, sau đó **mã hóa lại từ đầu** bằng pass mới, đảm bảo tính toàn vẹn tuyệt đối.

---

## 3. 📂 Cấu trúc mã nguồn (Architecture)
Hệ thống được thiết kế theo tiêu chuẩn module hóa, dễ dàng bảo trì và phát triển:

```text
📦 PasswordManager
├── 📜 main.py               # File trung tâm, khởi chạy toàn bộ ứng dụng
├── 📂 frontend/
│   └── 📜 gui.py            # Giao diện Dark Mode hiện đại bằng CustomTkinter
├── 📂 backend/
│   ├── 📜 database.py       # Giao tiếp SQLite chuẩn mực, chống lỗi "Database is locked"
│   └── 📜 security.py       # Chuyên gia bảo mật (Hàm băm SHA-256, mã hóa AES)
├── 📂 utils/
│   ├── 📜 anti_keylogger.py # Xử lý logic Bàn phím ảo (Virtual Keyboard)
│   └── 📜 password_gen.py   # Công cụ tạo mật khẩu ngẫu nhiên siêu mạnh
└── 📜 requirements.txt      # Danh sách thư viện cần thiết

4. 🔄 Tóm tắt luồng hoạt động (Workflow):

Mở App lần đầu: App thấy database trống ➔ Yêu cầu tạo Master Password ➔ Trộn Salt ➔ Băm SHA-256 ➔ Lưu vào Database.

Mở App lần 2: Yêu cầu nhập Master Password qua bàn phím ảo ➔ Băm ra và so sánh với Database ➔ Khớp thì cho phép đăng nhập.

Thêm tài khoản mới: Nhập mật khẩu gốc (VD: "123456") ➔ Hệ thống dùng Master Password mã hóa thành b'gAAAAAB...' ➔ Lưu phần đã mã hóa vào SQLite.

Copy ra dùng: Bấm "Copy" ➔ Hệ thống giải mã lại ➔ Đưa vào Clipboard ➔ Đếm 10 giây ➔ Xóa sạch Clipboard!