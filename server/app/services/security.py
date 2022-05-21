import bcrypt
from passlib.hash import bcrypt as passlib


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passlib.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return passlib.hash(password)
