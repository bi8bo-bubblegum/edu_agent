from typing import TypeVar, Generic, Any

from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 200,
    message: str = "success"
    data: T | None = None

def success(data: Any = None, message: str = "success", code: int = 200):
    return {"code": code, "message": message, "data": data}

def error(message: str = "error", code: int = 400):
    return {"code": code, "message": message, "data": None}