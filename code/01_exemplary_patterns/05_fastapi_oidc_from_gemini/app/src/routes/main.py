from fastapi import APIRouter

router = APIRouter(tags=["main"])


@router.get("/", summary="Root endpoint")
async def read_root():
    """
    Basic root endpoint.
    """
    return {
        "message": "Welcome to the FastAPI Authlib OpenID Connect Demo! Go to /auth/login to authenticate."
    }
