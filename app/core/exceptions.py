from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class AlreadyUpdatedError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "The resource was already updated by someone else before your synchronization.",
    ) -> None:
        super().__init__(status_code=409, detail=f"{table} with ID {id}. {detail}")


class NotFoundError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "Resource not found.",
    ) -> None:
        super().__init__(status_code=404, detail=f"{table} with ID {id}. {detail}")


class AlreadyExistsError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "Resource already exists.",
    ) -> None:
        super().__init__(status_code=409, detail=f"{table} with ID {id}. {detail}")


class UniqueViolationErrorHTTP(CustomHTTPException):
    def __init__(
        self,
        table: str,
        column: str,
        value: str,
        detail: str = "Unique violation error.",
    ) -> None:
        super().__init__(
            status_code=409, detail=f"{table} with {column} {value}. {detail}"
        )
