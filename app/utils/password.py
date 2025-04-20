import re

def is_valid_password(password: str, max_len: int = 64) -> bool:
    if len(password) < 8 or len(password) > max_len:
        return False
    if re.search(r"\s", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

#비밀번호 조건: 8자 이상 64자 이하, 공백 없이 영어 소문자와 숫자를 무조건 포함해야함.