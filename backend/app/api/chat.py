import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatSessionCreate, ChatSessionResponse
from app.schemas.common import ApiResponse, success
from app.services import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/sessions", response_model=ApiResponse[ChatSessionResponse], status_code=status.HTTP_201_CREATED)
async def create_session(
    session_in: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    session = await chat_service.start_learning(
        db, current_user.id, session_in.knowledge_node_id, session_in.title
    )
    return success(ChatSessionResponse.model_validate(session).model_dump(), message="创建会话成功")


@router.get("/sessions", response_model=ApiResponse[list[ChatSessionResponse]])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    sessions = await chat_service.get_user_sessions(db, current_user.id)
    return success([ChatSessionResponse.model_validate(s).model_dump() for s in sessions])


@router.get("/sessions/{session_id}/messages", response_model=ApiResponse[list[ChatMessageResponse]])
async def get_messages(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    messages = await chat_service.get_session_messages(db, session_id)
    return success([ChatMessageResponse.model_validate(m).model_dump() for m in messages])


@router.post("/sessions/{session_id}/messages", response_model=ApiResponse[ChatMessageResponse])
async def send_message(
    session_id: uuid.UUID,
    message_in: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    assistant_msg = await chat_service.send_chat_message(db, session_id, message_in.content)
    return success(ChatMessageResponse.model_validate(assistant_msg).model_dump(), message="发送成功")