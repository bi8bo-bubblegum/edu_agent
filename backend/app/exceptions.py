from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.schemas.common import error


class BusinessException(Exception):
    def __init__(self, message: str = "业务错误", code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NoAuthException(BusinessException):
    def __init__(self, message: str = "无权限"):
        super().__init__(message=message, code=401)

class ForbiddenException(BusinessException):
    def __init__(self, message: str = "禁止访问"):
        super().__init__(message=message, code=403)

class NotFoundException(BusinessException):
    """资源不存在异常（404）。"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(message=message, code=404)


class ParamException(BusinessException):
    """参数错误异常（400）。"""

    def __init__(self, message: str = "参数错误"):
        super().__init__(message=message, code=400)

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=200,
            content=error(message=exc.message, code=exc.code)
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail
        if isinstance(detail, dict) and "code" in detail:
            return JSONResponse(
                status_code=exc.status_code,
                content=detail
            )
        return JSONResponse(
            status_code=exc.status_code,
            content=error(message=str(detail), code=exc.status_code)
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error(message="服务器内部错误", code=500),
        )