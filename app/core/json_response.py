# utils/schemas.py
import typing as t

import orjson
from fastapi.background import BackgroundTasks
from fastapi.responses import Response
from pydantic import UUID1

from app.core.base_schema import CustomBaseModel


class JSONResponse(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: t.Any = None,
        status_code: int = 200,
        headers: t.Optional[t.Mapping[str, str]] = None,
        media_type: t.Optional[str] = None,
        background: t.Optional[BackgroundTasks] = None,
    ) -> None:
        self.status_code = status_code
        if media_type is not None:
            self.media_type = media_type
        self.background = background
        self.body = self.render(content)
        self.init_headers(headers)

    def render(self, content: CustomBaseModel | list[CustomBaseModel] | t.Any):
        # This is not 100% battle proof, but as our services are controlled (only return Pydantic modules) works fine
        if isinstance(content, CustomBaseModel):
            return content.model_dump_json().encode("utf-8")
        if isinstance(content, list):
            if isinstance(content[0], CustomBaseModel):

                def uuid_decoder(obj):
                    if isinstance(obj, UUID1):
                        return str(obj)

                return orjson.dumps(
                    [item.model_dump() for item in content], default=uuid_decoder
                )
