from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .urls import URL_LOGIN, URL_ROOT


def add_main_routes(app: FastAPI):
    @app.get(URL_ROOT)
    def home():
        return HTMLResponse(f"<a href={URL_LOGIN}>Login</a>")
