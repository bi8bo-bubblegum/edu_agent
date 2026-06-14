import logging
from enum import Enum
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agents.assessor import AssessorAgent
from app.agents.base import BaseAgent
from app.agents.curator import CuratorAgent
from app.agents.planner import PlannerAgent
from app.agents.tutor import TutorAgent
from app.config import get_settings

logger = logging.getLogger(__name__)

class IntentType(str, Enum):
    QUESTION = "question"
    PLAN = "plan"
    ASSESS = "assess"
    RESOURCE = "resource"
    UNKNOWN = "unknown"

INTENT_SYSTEM_PROMPT = """你是一个意图识别助手。根据学生的消息，判断其意图属于以下哪一类：

- question：学生提出问题、寻求解释、不理解某个概念
- plan：学生想要规划学习路径、制定学习计划、了解接下来该学什么
- assess：学生想要测试自己、做练习、参加评估
- resource：学生想要推荐学习资料、教材、视频等

注意：
只回复意图类别名称（question / plan / assess / resource），不要回复其他内容。"""

class Orchestrator:

    def __init__(self):
        settings = get_settings()
        self._llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url='https://api.deepseek.com/v1',
            temperature=0,
            max_tokens=10
        )
        self.tutor: BaseAgent = TutorAgent()
        self.assessor: BaseAgent = AssessorAgent()
        self.planner: BaseAgent = PlannerAgent()
        self.curator: BaseAgent = CuratorAgent()

    async def _llm_classify(self, message: str) -> IntentType:
        """使用LLM进行意图识别"""
        response = await self._llm.ainvoke([
            SystemMessage(content=INTENT_SYSTEM_PROMPT),
            HumanMessage(content=message)
        ])
        intent_str = response.content.strip().lower()
        try:
            return IntentType(intent_str)
        except ValueError:
            logger.warning(f"LLM 返回了未知的意图类型: {intent_str}，降级为 question")
            return IntentType.QUESTION

    async def classify_intent(self, message: str) -> IntentType:
        """意图识别，LLM 优先，失败时降级为默认路由。"""
        try:
            return await self._llm_classify(message)
        except Exception as e:
            logger.error(f"LLM 意图识别失败: {e}，降级为 question")
            return IntentType.QUESTION

    async def dispatch(
            self,
            message: str,
            session_id: str,
            context: dict[str, Any] | None = None,
    ) -> str:
        """根据意图路由到对应 Agent。"""
        intent = await self.classify_intent(message)
        agent_map: dict[IntentType, BaseAgent] = {
            IntentType.QUESTION: self.tutor,
            IntentType.ASSESS: self.assessor,
            IntentType.PLAN: self.planner,
            IntentType.RESOURCE: self.curator,
            IntentType.UNKNOWN: self.tutor,
        }
        agent = agent_map.get(intent, self.tutor)
        return await agent.handle(message, context)