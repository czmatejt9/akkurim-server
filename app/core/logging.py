import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create a directory for logs if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure rotating file handler
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
