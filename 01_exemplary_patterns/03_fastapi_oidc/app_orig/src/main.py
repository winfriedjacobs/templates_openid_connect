from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.routes.authentication import add_auth_routes
from src.routes.main import add_main_routes

SECRET_KEY = "some-random-string"


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    add_main_routes(app)
    add_auth_routes(app)

    return app
