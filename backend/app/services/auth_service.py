from datetime import datetime, timezone, timedelta
from uuid import UUID

import bcrypt
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.exceptions import ParamException
from app.models import User
from app.repositories import user_repo
from app.schemas.user import TokenData


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt().decode("utf-8"))

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def _create_access_token(user_id: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> TokenData | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=UUID(user_id))
    except JWTError:
        return None

async def user_register(db: AsyncSession, username: str, email: str, password: str, grade: str | None = None) -> User:
    if await user_repo.get_by_username(db, username):
        raise ParamException("用户名已存在")
    if await user_repo.get_by_email(db, email):
        raise ParamException("邮箱已存在")
    user = await user_repo.create(db, username=username, email=email, hashed_password=_hash_password(password), grade=grade)
    return user

async def user_login(db: AsyncSession, username: str, password: str) -> str:
    user = await user_repo.get_by_username(db, username)
    if user is None or not _verify_password(password, user.hashed_password):
        raise ParamException("用户名或密码错误")
    return _create_access_token(str(user.id))

async def get_current_user(db: AsyncSession, user_id: str):
    return await user_repo.get_by_id(db, UUID(user_id))