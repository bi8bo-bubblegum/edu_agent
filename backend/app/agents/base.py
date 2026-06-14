from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """所有 Agent 的抽象基类"""
    name: str = "base"

    @abstractmethod
    async def handle(self, message: str, context: dict[str, Any] | None = None) -> str:
        """处理用户消息，返回Agent响应"""
        ...

    @abstractmethod
    async def get_system_prompt(self) -> str:
        """获取系统提示语"""
        ...