from typing import Any

from app.agents.base import BaseAgent


class TutorAgent(BaseAgent):
    name = "tutor"

    async def handle(self, message: str, context: dict[str, Any] | None = None) -> str:
        return f'[Tutor Agent 占位] 收到消息:{message}'

    async def get_system_prompt(self) -> str:
        return "你是一个苏格拉底式教学助手，通过引导性提问帮助学生理解知识，而不是直接给出答案。"