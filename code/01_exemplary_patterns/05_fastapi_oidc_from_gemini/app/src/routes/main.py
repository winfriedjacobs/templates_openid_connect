from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["main"])


@router.get("/", summary="Root endpoint")
async def read_root():
    """
    Basic root endpoint.
    """
    return {
        "message": "Welcome to the FastAPI Authlib OpenID Connect Demo! Go to /auth/login to authenticate."
    }


@router.get("/login", summary="Test login, not part of the auth workflow")
async def login_test():
    """
    Basic root endpoint.
    """
    return RedirectResponse(url="/auth/login?target-url=/api/me")
