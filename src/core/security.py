from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

_pwd_hasher = PasswordHash((Argon2Hasher(),))


def hash_password(plain: str) -> str:
    "Return the hashed password."
    return _pwd_hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    "Return true if hash matches the hashed password."
    return _pwd_hasher.verify(plain, hashed)
