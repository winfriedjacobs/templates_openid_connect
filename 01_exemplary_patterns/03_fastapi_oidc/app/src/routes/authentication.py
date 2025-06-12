import logging

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.session import clear_session, set_session

from .urls import URL_AUTH_CALLBACK, URL_LOGIN, URL_LOGOUT, URL_ROOT

logger = logging.getLogger(__name__)


def add_auth_routes(app: FastAPI, keycloak: OAuth):
    @app.get(URL_LOGIN)
    async def login(request: Request):
        redirect_uri = request.url_for("auth")
        return await keycloak.authorize_redirect(
            request, redirect_uri
        )  # or: oauth.keycloak.authorize_redirect(...)

    @app.get(URL_AUTH_CALLBACK)
    async def auth(request: Request):
        try:
            token = await keycloak.authorize_access_token(
                request
            )  # or: oauth.keycloak.authorize_access_token(...)
        except OAuthError as error:
            return HTMLResponse(f"<h1>{error.error}</h1><h2>{error.description}</h2")
        user = token.get("userinfo")

        # # does not work, purpose not clear for me:
        # id_token = await keycloak.parse_id_token(token)
        # logger.error(f"id_token:\n{id_token}")

        if user:
            request.session["user"] = dict(user)
            # or/and any other values, like:
            request.session["hello"] = {"hallo": "ihr daheim"}
        return RedirectResponse(url="/")

    @app.get(URL_LOGOUT)
    async def logout(request: Request):
        response = RedirectResponse(url=URL_ROOT, status_code=307)

        # original implementation:
        request.session.pop("user", None)
        # maybe better but untested/not working
        # clear_session(response)

        return response
