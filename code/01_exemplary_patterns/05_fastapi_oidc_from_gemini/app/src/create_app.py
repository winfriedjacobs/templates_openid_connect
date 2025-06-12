"""
This moduLe provides the `app` object for the FastAPI application.

It is started in _main__py by doing this in the terminal:
```
( cd ./app )
uv run src
```

Code started with Gemini: https://gemini.google.com/app/2530e9b2cbbd2bf1?hl=de
"""

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config.web_session import WEB_SESSION_SECRET_KEY
from routes.api import router as api_router
from routes.authentication import router as authentication_router
from routes.main import router as main_router

# --- Configuration ---
# IMPORTANT: Replace with your actual secrets and configuration!
# For production, use environment variables for these secrets:
# - export APP_SECRET_KEY="a_long_random_string_for_session_middleware"
# - export GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
# - export GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

# Your applications secret key for session management (MUST BE LONG AND RANDOM)


def create_app() -> FastAPI:
    # FastAPI app initialization
    app = FastAPI(title="FastAPI Authlib OpenID Connect Demo")

    # Add SessionMiddleware to handle sessions (required for Authlib's client)
    app.add_middleware(SessionMiddleware, secret_key=WEB_SESSION_SECRET_KEY)

    # --- API Endpoints ---
    app.include_router(api_router)
    app.include_router(authentication_router)
    app.include_router(main_router)

    return app


__all__ = ["create_app"]
