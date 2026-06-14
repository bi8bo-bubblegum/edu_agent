from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import NoAuthException
from app.models import User
from app.services.auth_service import decode_access_token, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_active_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    token_data = decode_access_token(token)
    if token_data is None:
        raise NoAuthException("无效的令牌")
    user = await get_current_user(db, token_data.user_id)
    if user is None:
        raise NoAuthException("用户不存在")
    return user
