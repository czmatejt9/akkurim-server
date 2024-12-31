from app.core.exceptions import BaseException


class GuardianNotFoundException(BaseException):
    status_code = 404
    message = "Guardian not found"
