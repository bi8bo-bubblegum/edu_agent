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