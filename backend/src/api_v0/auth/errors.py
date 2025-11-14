from src.api_v0.common.errors import BaseAppException
from starlette import status


class AccessForbiddenError(BaseAppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Access Forbidden. Insufficient role"
        )


class AuthError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message
        )


class TokenError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message
        )
