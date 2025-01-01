from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class UpdateError(CustomHTTPException):
    def __init__(
        self,
        detail: str = "The resource was already updated by someone else before your synchronization.",
    ) -> None:
        super().__init__(status_code=409, detail=detail)
