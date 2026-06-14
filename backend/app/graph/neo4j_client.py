from neo4j import AsyncDriver, AsyncGraphDatabase

from app.config import get_settings


class Neo4jClient:
    def __init__(self):
        settings = get_settings()
        self._driver: AsyncDriver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    async def close(self):
        await self._driver.close()

    async def ping(self):
        try:
            async with self._driver.session() as session:
                result = await session.run("RETURN 1 AS Ping")
                await result.consume()
                return True
        except Exception:
            return False

    async def run_query(self, query: str, parameters: dict | None = None) -> list[dict]:
        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    async def get_prerequisites(self, node_name: str) -> list[str]:
        query = """
        MATCH (n:KnowledgeNode {name: $name})<-[:PREREQUISITE]-(pre:KnowledgeNode)
        RETURN pre.name AS name
        """
        result = await self.run_query(query, {"name": node_name})
        return [r["name"] for r in result]

    async def get_learning_path(self, subject: str, mastered_nodes: list[str]) -> list[dict]:
        query = """
        MATCH (n:KnowledgeNode {subject: $subject})
        WHERE NOT n.name IN $mastered
        RETURN n.name AS name, n.difficulty AS difficulty, n.chapter AS chapter
        ORDER BY n.difficulty
        """
        result = await self.run_query(query, {"subject": subject, "mastered": mastered_nodes})
        return result