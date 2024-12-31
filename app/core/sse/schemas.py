from typing import Any, Dict

from pydantic import UUID1

from app.core.base_schema import MyBase


class SSEEvent(MyBase):
    action: str
    table_name: str
    object_id: int | UUID1
    object_data: Dict[str, Any]
