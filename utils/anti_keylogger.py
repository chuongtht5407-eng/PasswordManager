# File utils/anti_keylogger.py - Chờ cập nhật code
import pyperclip
import threading
import time

def secure_copy(text: str, timeout: int = 10):
    """
    Copy văn bản vào clipboard và tự động xóa sạch sau 'timeout' giây.
    Chống lại các phần mềm theo dõi Clipboard (Clipboard Hijacker/Keylogger).
    """
    try:
        pyperclip.copy(text)
        print(f"[Bảo mật] Đã copy vào Clipboard. Tự động xóa sau {timeout} giây.")
        
        def clear_clipboard():
            time.sleep(timeout)
            # Kiểm tra xem người dùng có copy đè cái khác chưa, nếu chưa thì mới xóa
            if pyperclip.paste() == text:
                pyperclip.copy("") 
                print("[Bảo mật] Clipboard đã được làm sạch!")

        # Chạy trong một thread riêng biệt để không làm đơ giao diện chính
        clear_thread = threading.Thread(target=clear_clipboard, daemon=True)
        clear_thread.start()
        
    except Exception as e:
        print(f"[Lỗi Clipboard] Không thể copy: {e}")


def get_virtual_keyboard_layout() -> list:
    """
    Trả về cấu trúc sơ đồ bàn phím QWERTY tiêu chuẩn.
    Dùng để xây dựng giao diện bàn phím ảo nhằm chống Keylogger phần mềm.
    """
    return [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'"],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
    ]