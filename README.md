# 🛡️ Secure Password Manager Pro

## 📋 Báo Cáo Tóm Tắt Ứng Dụng Quản Lý Mật Khẩu

### 🌟 Tổng Quan
Ứng dụng **Secure Password Manager Pro** là một phần mềm quản lý mật khẩu cá nhân được phát triển bằng **Python**, sử dụng giao diện đồ họa **CustomTkinter** với theme tối chuyên nghiệp. Ứng dụng lưu trữ mật khẩu của các tài khoản trực tuyến một cách an toàn, mã hóa toàn bộ dữ liệu bằng thuật toán **AES-256** và bảo vệ bằng **Master Password**.

### 🏗️ Kiến Trúc Hệ Thống
- **Ngôn ngữ lập trình**: Python 3.x
- **Giao diện người dùng**: CustomTkinter (dark theme)
- **Cơ sở dữ liệu**: SQLite (file `password_manager.db`)
- **Bảo mật**:
  - Mã hóa **AES-256** qua Fernet (cryptography library)
  - Băm mật khẩu bằng **PBKDF2-SHA256** (passlib)
  - Salt ngẫu nhiên cho mỗi tài khoản
  - **Recovery Key** cho khôi phục
- **Các module phụ**: Tạo mật khẩu mạnh, bàn phím ảo chống keylogger

### 🚀 Các Tính Năng Chính

#### 1. ⚙️ Thiết Lập Ban Đầu
- **Tạo Master Password**: Người dùng nhập mật khẩu chính (tối thiểu 6 ký tự) để bảo vệ toàn bộ kho dữ liệu.
- **Tạo Recovery Key**: Tự động tạo một khóa khôi phục ngẫu nhiên (32 ký tự) để sử dụng trong trường hợp quên Master Password. Khóa này chỉ hiển thị một lần và phải được lưu trữ an toàn.
- **Mã hóa dữ liệu**: Master Password được băm và sử dụng để tạo khóa mã hóa cho toàn bộ vault.

#### 2. 🔒 Đăng Nhập và Xác Thực
- **Đăng nhập bằng Master Password**: Nhập mật khẩu chính để truy cập ứng dụng.
- **Bàn phím ảo**: Giao diện bàn phím ảo chống keylogger khi nhập Master Password.
- **Thiết lập/Đổi Recovery Key**: Sau khi đăng nhập thành công, người dùng có thể tạo hoặc cập nhật Recovery Key mới.

#### 3. 📂 Quản Lý Kho Mật Khẩu (Vault)
- **Thêm mật khẩu mới**: Nhập tên ứng dụng/website, tài khoản/email, và mật khẩu. Mật khẩu được mã hóa trước khi lưu.
- **Tạo mật khẩu mạnh**: Nút "⚡ MẠNH" tự động tạo mật khẩu ngẫu nhiên 16 ký tự (bao gồm chữ hoa, chữ thường, số, ký tự đặc biệt).
- **Xem danh sách**: Hiển thị tất cả mật khẩu đã lưu với thông tin thống kê (tổng số mật khẩu, trạng thái an toàn).
- **Tìm kiếm**: Ô tìm kiếm theo tên ứng dụng hoặc tài khoản, lọc kết quả theo thời gian thực.
- **Sao chép mật khẩu**: Nút "Copy" để sao chép mật khẩu đã giải mã vào clipboard một cách an toàn (chống keylogger).
- **Xóa mật khẩu**: Xóa từng entry với xác nhận.

#### 4. 🛡️ Bảo Mật và Khôi Phục
- **Mã hóa toàn bộ**: Tất cả mật khẩu được mã hóa bằng khóa AES-256 được tạo từ Master Password và salt.
- **Recovery Key**: Nếu quên Master Password, nhập Recovery Key để reset toàn bộ dữ liệu và tạo Master Password mới.
- **Đăng xuất**: Xóa khóa mã hóa khỏi bộ nhớ khi đăng xuất.

#### 5. 🎨 Giao Diện Người Dùng
- **Thiết kế chuyên nghiệp**: Theme tối với màu sắc xanh lá (#34D399) và đỏ (#EF4444) cho các nút quan trọng.
- **Responsive**: Giao diện thích ứng với kích thước cửa sổ (tối thiểu 960x700).
- **Trải nghiệm người dùng**: Các màn hình riêng biệt cho setup, login, dashboard, và recovery. Hỗ trợ phím Enter để nhanh chóng.

### 🗄️ Cơ Sở Dữ Liệu
- **Bảng master_user**: Lưu hash Master Password, salt, và hash Recovery Key (chỉ 1 dòng).
- **Bảng vault**: Lưu các entry mật khẩu (id, app_name, username, encrypted_password).

### 🔐 Bảo Mật và An Toàn
- **Thuật toán mã hóa**: AES-256 với PBKDF2 (480.000 iterations) chống brute-force.
- **Băm mật khẩu**: PBKDF2-SHA256 cho Master Password và Recovery Key.
- **Chống keylogger**: Bàn phím ảo và sao chép an toàn.
- **Recovery**: Reset dữ liệu nếu cần, nhưng không khôi phục dữ liệu cũ (thiết kế bảo mật).

### ⚠️ Hạn Chế và Lưu Ý
- Không hỗ trợ đồng bộ hóa đám mây hoặc đa thiết bị.
- Recovery Key chỉ cho phép reset, không khôi phục dữ liệu cũ.
- Phụ thuộc vào file database SQLite cục bộ.

### 🎯 Kết Luận
Ứng dụng cung cấp giải pháp quản lý mật khẩu cá nhân **an toàn**, **dễ sử dụng** với giao diện thân thiện. Các tính năng bảo mật cấp công nghiệp đảm bảo dữ liệu được bảo vệ tốt, phù hợp cho cá nhân sử dụng hàng ngày.

