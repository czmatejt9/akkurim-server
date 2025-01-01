import json

from fastapi import APIRouter, Request, Response
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
    async with broadcast.subscribe(channel="updates") as subscriber:
        async for event in subscriber:
            yield {
                "event": "update",
                "data": json.dumps(event),
            }


# Simulated data stream for SSE
@router.get("/listen")
async def sse_endpoint():
    return EventSourceResponse(event_generator())
