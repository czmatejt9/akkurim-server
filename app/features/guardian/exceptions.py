from app.core.exceptions import CustomHTTPException


class GuardianNotFoundException(CustomHTTPException):
    status_code = 404
    message = "Guardian not found"
