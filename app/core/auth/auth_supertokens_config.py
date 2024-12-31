from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.recipe import dashboard, emailpassword, session, userroles

from app.core.config import settings


def supertokens_init():
    init(
        app_info=InputAppInfo(
            app_name=settings.APP_NAME,
            api_domain=settings.API_DOMAIN,
            website_domain=settings.WEBSITE_DOMAIN,
            api_base_path="/auth",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI, api_key=settings.API_KEY
        ),
        framework="fastapi",
        recipe_list=[
            session.init(),
            emailpassword.init(),
            dashboard.init(admins=[settings.DASHBOARD_ADMIN]),
            userroles.init(),
        ],
        mode="asgi",
    )
