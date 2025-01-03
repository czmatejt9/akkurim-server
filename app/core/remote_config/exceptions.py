from app.core.exceptions import CustomHTTPException


class RemoteConfigNotFoundError(CustomHTTPException):
    def __init__(self, tenant_id: str) -> None:
        super().__init__(
            status_code=404,
            detail=f"Remote config not found for tenant: {tenant_id}",
        )
