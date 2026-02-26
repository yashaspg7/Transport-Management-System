from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from src.core.config import settings

_pwd_hasher = PasswordHash((Argon2Hasher(),))


def hash_password(plain: str) -> str:
    "Return the hashed password."
    return _pwd_hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    "Return true if hash matches the hashed password."
    return _pwd_hasher.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    "Create a JWT access token"
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
