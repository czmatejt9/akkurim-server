import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import (
    get_middleware as supertokens_middleware,
)
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.core.auth.auth_supertokens_config import supertokens_init
from app.core.base_schema import BaseSchema
from app.core.broadcast import broadcast
from app.core.config import settings
from app.core.database import db
from app.core.logging import logger
from app.core.remote_config.router import router as remote_config_router
from app.core.response import JSONResponse
from app.core.sse.router import router as sse_router
from app.features.guardian.router import router as guardian_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        await broadcast.connect()
        yield
    finally:
        await db.disconnect()
        await broadcast.disconnect()


supertokens_init()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.add_middleware(supertokens_middleware())
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.WEBSITE_DOMAIN,
        settings.API_DOMAIN,
        settings.PUBLIC_DOMAIN,
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

app.include_router(guardian_router)
app.include_router(remote_config_router)
app.include_router(sse_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.url.path == "/" or request.url.path == "/root-custom-response":
        return await call_next(request)

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.url} took {process_time} seconds")
    return response


@app.get("/root-custom-response", response_class=JSONResponse)
def read_root_with_custom_response():
    content = HealthSchema(status="ok", app_name=settings.APP_NAME)
    return JSONResponse(content=content)


@app.get("/")
def read_root():
    content = HealthSchema(status="ok", app_name=settings.APP_NAME)
    return content


# for testing purposes
@app.post("/fake-sync-endpoint")
async def fake_sync_endpoint():
    # simulate fake data processing by sleeping for 0.5 seconds
    await asyncio.sleep(2)
    return {"message": "Synced"}


class HealthSchema(BaseSchema):
    status: str
    app_name: str
