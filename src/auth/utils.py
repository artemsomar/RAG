from datetime import timedelta, datetime, timezone
import bcrypt
import jwt
from src.config import settings


def encode_jwt(
        payload: dict,
        expires_minutes: int,
        private_key: str = settings.auth.private_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
):
    to_encode = payload.copy()
    to_encode["sub"] = str(payload.get("sub"))
    now_time = datetime.now(timezone.utc)
    expire = now_time + timedelta(minutes=expires_minutes)
    to_encode.update(
        iat=now_time,
        exp=expire,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm,
    )
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.auth.public_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
