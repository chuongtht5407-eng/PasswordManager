# File này sẽ băm mật khẩu tổng (Master Password) bằng chuẩn SHA256 và dùng thuật toán AES-256 (thông qua Fernet) để mã hóa các mật khẩu con. Đây là tiêu chuẩn bảo mật cấp công nghiệp.
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.hash import pbkdf2_sha256

def hash_master_password(password: str) -> str:
    """Băm mật khẩu Master để lưu vào DB (Không bao giờ lưu mật khẩu gốc)"""
    return pbkdf2_sha256.hash(password)

def verify_master_password(password: str, hashed_password: str) -> bool:
    """Kiểm tra xem người dùng nhập Master Password có đúng không"""
    return pbkdf2_sha256.verify(password, hashed_password)

def generate_encryption_key(master_password: str, salt: bytes) -> bytes:
    """
    Tạo khóa mã hóa (Key) AES-256 từ Master Password và Salt.
    Sử dụng thuật toán PBKDF2 để chống tấn công Brute-force.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # Băm 480,000 lần cho cực kỳ an toàn
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def encrypt_data(plain_text: str, key: bytes) -> str:
    """Mã hóa chuỗi văn bản (Mật khẩu các ứng dụng)"""
    f = Fernet(key)
    encrypted_bytes = f.encrypt(plain_text.encode())
    return encrypted_bytes.decode('utf-8')

def decrypt_data(encrypted_text: str, key: bytes) -> str:
    """Giải mã văn bản để hiển thị cho người dùng"""
    try:
        f = Fernet(key)
        decrypted_bytes = f.decrypt(encrypted_text.encode())
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        return "[Lỗi: Không thể giải mã - Sai khóa]"