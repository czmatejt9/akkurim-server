from app.core.exceptions import CustomHTTPException


class GuardianNotFoundException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = 404,
        detail: str = "Guardian not found",
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
