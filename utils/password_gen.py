# File utils/password_gen.py - Chờ cập nhật code
import string
import secrets

def generate_strong_password(length: int = 16, 
                             use_upper: bool = True, 
                             use_lower: bool = True, 
                             use_digits: bool = True, 
                             use_special: bool = True) -> str:
    """
    Tạo mật khẩu ngẫu nhiên siêu mạnh.
    Sử dụng thư viện 'secrets' thay vì 'random' để đảm bảo an toàn mã hóa.
    """
    if length < 4:
        length = 4 # Ép độ dài tối thiểu để đảm bảo an toàn

    character_pool = ""
    guaranteed_chars = []

    if use_upper:
        character_pool += string.ascii_uppercase
        guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        character_pool += string.ascii_lowercase
        guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        character_pool += string.digits
        guaranteed_chars.append(secrets.choice(string.digits))
    if use_special:
        # Giới hạn các ký tự đặc biệt phổ biến, dễ nhập
        special_chars = "!@#$%^&*()-_=+<>?"
        character_pool += special_chars
        guaranteed_chars.append(secrets.choice(special_chars))

    if not character_pool:
        # Nếu người dùng bỏ chọn tất cả, mặc định dùng chữ thường và số
        character_pool = string.ascii_lowercase + string.digits
        guaranteed_chars = [secrets.choice(string.ascii_lowercase), secrets.choice(string.digits)]

    # Điền phần còn lại của mật khẩu bằng các ký tự ngẫu nhiên trong pool
    remaining_length = length - len(guaranteed_chars)
    random_chars = [secrets.choice(character_pool) for _ in range(remaining_length)]

    # Gộp lại và xáo trộn vị trí để không ai đoán được quy luật
    password_list = guaranteed_chars + random_chars
    
    # secrets không có hàm shuffle, nên ta phải tự viết thuật toán trộn an toàn
    secure_password_list = []
    while password_list:
        element = secrets.choice(password_list)
        secure_password_list.append(element)
        password_list.remove(element)

    return "".join(secure_password_list)