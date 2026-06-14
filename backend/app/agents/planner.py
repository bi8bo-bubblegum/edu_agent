from typing import Any

from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    name = "planner"

    async def handle(self, message: str, context: dict[str, Any] | None = None) -> str:
        return f"[Planner Agent 占位] 收到消息：{message}"

    async def get_system_prompt(self) -> str:
        return "你是一个学习路径规划助手，根据学生的知识状态规划个性化学习路径。"