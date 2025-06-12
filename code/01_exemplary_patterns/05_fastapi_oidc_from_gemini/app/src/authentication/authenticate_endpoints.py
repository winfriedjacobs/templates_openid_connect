"""
--- Authentication Dependency ---
"""

from typing import Optional

from fastapi import Depends, HTTPException
from starlette import status
from starlette.requests import Request

from model.user_session import UserSession


async def get_current_user_from_session(request: Request) -> Optional[UserSession]:
    """
    Dependency to get the current authenticated user from the session.
    """
    user_info = request.session.get("user")
    if user_info:
        return UserSession(**user_info)
    return None


def require_auth(current_user: UserSession = Depends(get_current_user_from_session)):
    """
    Dependency to enforce authentication. If no user is in session, raises 401.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in: /auth/login.",
            headers={
                "WWW-Authenticate": "Bearer"
            },  # Still good practice for API clients
        )
    return current_user
