from secrets import token_urlsafe

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.authentication.oidc import create_oauth_keycloak
from src.routes.authentication import add_auth_routes
from src.routes.main import add_main_routes


def create_app() -> FastAPI:
    SECRET_KEY = token_urlsafe(32)

    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    keycloak = create_oauth_keycloak()

    add_main_routes(app)
    add_auth_routes(app, keycloak=keycloak)

    return app
