from typing import Any

from app.agents.base import BaseAgent


class AssessorAgent(BaseAgent):
    name = "assessor"

    async def handle(self, message: str, context: dict[str, Any] | None = None) -> str:
        return f'[Assessor Agent 占位] 收到消息:{message}'

    async def get_system_prompt(self) -> str:
        return "你是一个知识评估助手，负责出题和批改答案来评估学生的知识掌握程度。"