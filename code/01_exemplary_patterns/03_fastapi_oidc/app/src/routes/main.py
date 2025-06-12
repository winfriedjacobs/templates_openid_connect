import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .urls import URL_LOGIN, URL_PROTECTED, URL_ROOT


def add_main_routes(app: FastAPI):
    @app.get(URL_ROOT)
    async def root_page(request: Request):
        user = request.session.get("user")
        if user:
            data_user = json.dumps(user, indent=2)
            data_session = json.dumps(request.session, indent=2)
            url_path_logout = app.url_path_for("logout")
            return HTMLResponse(
                f"""
    <a href="{url_path_logout}">logout</a>
    <pre>{url_path_logout}</pre>
    <table>
      <tr>
        <td><pre>{data_user}</pre></td>
        <td><pre>{data_session}</pre></td>
      </tr>
    </table>
                """
            )
        url_path_login = app.url_path_for("login")
        return HTMLResponse(
            f"""
    <a href="{url_path_login}">login</a>
    <pre>{url_path_login}</pre>
            """
        )

    @app.get(URL_PROTECTED)
    async def secure(request: Request):
        user = request.session.get("user")
        if not user:
            return RedirectResponse(
                url=URL_LOGIN
            )  # was: url=app.url_path_for("login"), but we don't want to reference login() from another module/function
        return HTMLResponse(f"<h1>Hello {user['preferred_username']}</h1>")
