import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import orchestrator
from app.agents.orchestrator import Orchestrator
from app.models import ChatSession, ChatMessage
from app.repositories import chat_session_repo, learning_record_repo, chat_message_repo

orchestrator = Orchestrator()

async def start_learning(
        db: AsyncSession,
        student_id: uuid.UUID,
        knowledge_node_id: uuid.UUID | None = None,
        title: str | None = None
) -> ChatSession:
    session = await chat_session_repo.create(db, student_id=student_id, knowledge_node_id=knowledge_node_id, title=title)
    if knowledge_node_id:
        existing = await learning_record_repo.get_by_id(db, knowledge_node_id)
        if existing:
            await learning_record_repo.update(db, knowledge_node_id, mastery_level="learning")
        else:
            await learning_record_repo.create(db, student_id=student_id, knowledge_node_id=knowledge_node_id, mastery_level="learning")
    return session

async def get_user_sessions(db: AsyncSession, student_id: uuid.UUID) -> list[ChatSession]:
    return await chat_session_repo.get_user_session(db, student_id)

async def get_session_messages(db: AsyncSession, session_id: uuid.UUID) -> list[ChatMessage]:
    """获取某个会话的所有消息。"""
    return await chat_message_repo.get_session_messages(db, session_id)

async def send_chat_message(db: AsyncSession, session_id: uuid.UUID, user_message: str) -> ChatMessage:
    """发送聊天消息并获取 AI 回复：保存用户消息 → 调用 Orchestrator → 保存 AI 回复。"""
    await chat_message_repo.create(db, session_id=session_id, role="student", content=user_message)

    intent = await orchestrator.classify_intent(user_message)
    response = await orchestrator.dispatch(user_message, session_id=str(session_id))

    assistant_msg = await chat_message_repo.create(
        db, session_id=session_id, role="assistant", content=response, agent_name=intent.value
    )
    return assistant_msg