from argon2 import PasswordHasher
from pwdlib.hashers.argon2 import Argon2Hasher

password_hasher = PasswordHasher((Argon2Hasher(),))

def password_hasher(password: str)->str:
    return password_hasher.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_hasher.verify(plain_password,hashed_password)