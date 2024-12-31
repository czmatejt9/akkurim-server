from app.core.exceptions import CustomHTTPException


class GuardianNotFoundException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = 404,
        detail: str = "Guardian not found",
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class GuardianAlreadyExistsException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: str = "Guardian already exists",
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class GuardianEmailAlreadyExistsException(CustomHTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: str = "Email already exists",
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
