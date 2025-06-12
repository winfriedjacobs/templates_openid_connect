from typing import Optional

from fastapi import APIRouter, Depends

from authentication.authenticate_endpoints import (
    get_current_user_from_session,
    require_auth,
)
from model.user_session import UserSession


router = APIRouter(prefix="/api", tags=["api"])


@router.get(
    "/protected", summary="Access a protected resource (requires OIDC authentication)"
)
async def read_protected_resource(current_user: UserSession = Depends(require_auth)):
    """
    An example endpoint that requires a valid OIDC authentication session.
    """
    return {
        "message": f"Hello {current_user.name or current_user.email or current_user.id}! You accessed a protected resource.",
        "user_info": current_user.model_dump(),
    }


@router.get("/me", summary="Get current user info (if authenticated)")
async def get_my_info(
    current_user: Optional[UserSession] = Depends(get_current_user_from_session),
):
    """
    Returns information about the current user if authenticated, otherwise returns None.
    """
    if current_user:
        return {"authenticated": True, "user": current_user.model_dump()}
    return {"authenticated": False, "user": None}
