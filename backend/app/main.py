from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="EduAgent",
    description="基于 Multi-Agent协作的智能自适应辅导系统",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(api_router)
register_exception_handlers(app)