from typing import Any

from app.agents.base import BaseAgent


class CuratorAgent(BaseAgent):
    name = "curator"

    async def handle(self, message: str, context: dict[str, Any] | None = None) -> str:
        return f"[Curator Agent 占位] 收到消息：{message}"

    async def get_system_prompt(self) -> str:
        return "你是一个学习资源推荐助手，负责为学生推荐适合的学习材料。"