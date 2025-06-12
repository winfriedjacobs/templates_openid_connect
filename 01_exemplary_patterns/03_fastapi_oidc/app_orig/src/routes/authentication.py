from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from src.auth import keycloak
from src.deps import require_group, require_role
from src.session import clear_session, set_session

from .urls import (
    URL_ADMIN,
    URL_CALLBACK,
    URL_LOGIN,
    URL_LOGOUT,
    URL_PROTECTED,
    URL_ROOT,
)


def add_auth_routes(app: FastAPI):
    @app.get(URL_LOGIN)
    async def login(request: Request):
        # redirect_uri = f"{APP_BASE_URL}{URL_CALLBACK}"
        redirect_uri = request.url_for("callback")
        return await keycloak.authorize_redirect(
            request, redirect_uri=redirect_uri, scope="openid profile email"
        )

    @app.get(URL_CALLBACK)
    async def callback(request: Request):
        token = await keycloak.authorize_access_token(request)
        user = await keycloak.parse_id_token(request, token)
        response = RedirectResponse(url=URL_PROTECTED, status_code=302)
        set_session(response, user)
        return response

    @app.get(URL_LOGOUT)
    async def logout():
        response = RedirectResponse(url=URL_ROOT, status_code=302)
        clear_session(response)
        return response

    @app.get(URL_PROTECTED)
    def protected(user=Depends(require_group("/AppAdmins"))):
        return {"message": f"Hello, {user['preferred_username']} (Group: AppAdmins)"}

    @app.get(URL_ADMIN)
    def admin_only(user=Depends(require_role("admin"))):
        return {"message": f"Hello Admin {user['preferred_username']}"}
