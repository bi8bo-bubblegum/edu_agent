from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models import User
from app.schemas.common import ApiResponse, success
from app.schemas.user import UserResponse, UserCreate, Token, UserLogin
from app.services.auth_service import user_register, user_login

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_register(db, user_in.username, user_in.email, user_in.password, user_in.grade)
    return success(data=UserResponse.model_validate(user).model_dump(), message="注册成功")

@router.post("/login", response_model=ApiResponse[Token])
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await user_login(db, user_in.username, user_in.password)
    return success(Token(access_token=token).model_dump(), message="登录成功")

@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_active_user)):
    return success(data=UserResponse.model_validate(current_user).model_dump(), message="获取用户信息成功")