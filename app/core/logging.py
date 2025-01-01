import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log_file = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(
            log_file,
            maxBytes=5_000_000,
            backupCount=5,
        ),
    ],
)

# Create a logger instance for your app
logger = logging.getLogger("fastapi_app")

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
    default_response_class=FileResponse,
)


# use something from docs: https://fastapi.tiangolo.com/tutorial/request-files/
@router.get("/")
async def get_logs():
    return FileResponse(log_file, media_type="text/plain")
