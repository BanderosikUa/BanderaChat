import bcrypt
import string
import random


def hash_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, password_in_db)

def generate_random_alphanum(length: int = 20) -> str:
    ALPHA_NUM = string.ascii_letters + string.digits
    return "".join(random.choices(ALPHA_NUM, k=length))
