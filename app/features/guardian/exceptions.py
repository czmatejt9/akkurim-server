from app.core.exceptions import CustomHTTPException


class GuardianNotFoundException(CustomHTTPException):
    super().__init__(status_code=404, detail="Guardian not found")
