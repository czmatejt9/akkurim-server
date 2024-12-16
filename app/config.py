import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PUBLIC_DOMAIN: str = (
        "https://devapi.czmatejt.me"  # TODO change to "https://devapi.akkurim.cz"
    )
    APP_NAME: str = "akkurim-server-dev"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/v1"

    SUPERTOKENS_CONNECTION_URI: str = "http://supertokens:3567"
    API_DOMAIN: str = "http://localhost:8002"
    WEBSITE_DOMAIN: str = "http://localhost:3002"
    API_KEY: str = os.getenv("API_KEY")
    DASHBOARD_ADMIN: str = "tajovsky.matej@gmail.com"

    DATABASE_URL: str = str(os.getenv("DATABASE_URL"))
    MIN_CONNECTIONS: int = 1
    MAX_CONNECTIONS: int = 10

    model_config = {"case_sensitive": True}


settings = Settings()
