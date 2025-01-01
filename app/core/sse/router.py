import orjson
from fastapi import APIRouter, Request, Response
from fastapi.responses import ORJSONResponse
from sse_starlette.sse import EventSourceResponse

from app.core.sse.broadcast import broadcast
from app.core.sse.schemas import SSEEvent

router = APIRouter(
    prefix="/sse",
    tags=["sse"],
    responses={404: {"description": "Not found"}},
)

events = []


async def event_generator():
    async with broadcast.subscribe(channel="update") as subscriber:
        async for event in subscriber:
            yield event


# Simulated data stream for SSE
@router.get("/listen")
async def sse_endpoint():
    return EventSourceResponse(event_generator())


@router.get(
    "/broadcast-test",
    response_class=ORJSONResponse,
    response_model=SSEEvent,
)
async def broadcast_event():
    event = SSEEvent(
        table_name="guardian",
        endpoint="/guardian/268f74bc-c7c4-11ef-9cd2-0242ac120002",
        id="268f74bc-c7c4-11ef-9cd2-0242ac120002",
        local_action="upsert",
    )
    await broadcast.publish(
        channel="update",
        message=orjson.dumps(
            event.model_dump(),
        ).decode("utf-8"),
    ),
    return ORJSONResponse(event.model_dump(), status_code=200)
